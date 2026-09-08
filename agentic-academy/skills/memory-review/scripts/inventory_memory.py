#!/usr/bin/env python3
"""Inventory a project's Claude Code auto memory and run the deterministic checks."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from typing import Any


INDEX_ENTRY_RE = re.compile(r"^\s*-\s*\[([^\]]*)\]\(([^)]+)\)")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
ISO_DATE_RE = re.compile(r"\b(20\d{2})-(\d{2})-(\d{2})\b")
MONTH_YEAR_RE = re.compile(
    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2},?\s+)?(20\d{2})\b"
)
MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}
STOPWORDS = {
    "a", "an", "and", "any", "are", "as", "at", "be", "by", "can", "do", "does",
    "for", "from", "has", "have", "how", "if", "in", "into", "is", "it", "its",
    "not", "of", "on", "or", "should", "that", "the", "their", "them", "then",
    "this", "to", "use", "used", "uses", "user", "want", "wants", "when", "which",
    "while", "will", "with", "you", "your", "also", "why", "apply", "always",
    "never", "claude", "memory", "file", "files", "just", "than", "was",
    "were", "been", "being", "one", "two", "all", "but", "out", "about", "more",
    "what", "who", "his", "her", "they", "our", "we", "so", "up", "no", "yes",
}
PATHISH_SUFFIXES = (".md", ".py", ".json", ".csv", ".html", ".txt", ".yml", ".yaml", ".sh")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    closing = None
    for index in range(1, min(len(lines), 200)):
        if lines[index].strip() == "---":
            closing = index
            break
    if closing is None:
        return {}, text

    fields: dict[str, Any] = {}
    parent: str | None = None
    for raw in lines[1:closing]:
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip())
        match = re.match(r"^\s*([A-Za-z][\w-]*)\s*:\s*(.*)$", raw)
        if not match:
            continue
        key = match.group(1)
        value = match.group(2).strip().strip("'\"")
        if indent == 0:
            if value == "":
                fields[key] = {}
                parent = key
            else:
                fields[key] = value
                parent = None
        elif parent and isinstance(fields.get(parent), dict):
            fields[parent][key] = value
    return fields, "\n".join(lines[closing + 1 :])


def memory_dir_for(root: Path) -> tuple[Path | None, str]:
    projects = Path.home() / ".claude" / "projects"
    converted = str(root).replace("/", "-").replace(" ", "-")
    direct = projects / converted / "memory"
    if direct.is_dir():
        return direct, "direct"
    if projects.is_dir():
        suffix = "-" + root.name.replace(" ", "-")
        for candidate in sorted(projects.iterdir()):
            if candidate.name.endswith(suffix) and (candidate / "memory").is_dir():
                return candidate / "memory", "suffix-match"
    return None, "not-found"


def slugify(value: str) -> str:
    return re.sub(r"[\s_]+", "-", value.strip().lower())


def project_basenames(root: Path) -> set[str]:
    skip = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".cache"}
    names: set[str] = set()
    for current, dirnames, filenames in __import__("os").walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        names.update(dirnames)
        names.update(filenames)
    return names


def content_words(text: str) -> set[str]:
    words = re.findall(r"[a-z][a-z0-9-]{3,}", text.lower())
    return {word for word in words if word not in STOPWORDS}


def memory_type(fields: dict[str, Any]) -> str:
    meta = fields.get("metadata")
    if isinstance(meta, dict) and meta.get("type"):
        return str(meta["type"]).lower()
    if fields.get("type"):
        return str(fields["type"]).lower()
    return "untyped"


def past_dates(body: str, today: datetime, horizon_days: int) -> list[str]:
    found: list[str] = []
    for year, month, day in ISO_DATE_RE.findall(body):
        try:
            when = datetime(int(year), int(month), int(day), tzinfo=timezone.utc)
        except ValueError:
            continue
        if (today - when).days > horizon_days:
            found.append(f"{year}-{month}-{day}")
    for mon, _day, year in MONTH_YEAR_RE.findall(body):
        month = MONTHS.get(mon.lower()[:4]) or MONTHS.get(mon.lower()[:3])
        if not month:
            continue
        when = datetime(int(year), month, 1, tzinfo=timezone.utc)
        if (today - when).days > horizon_days:
            found.append(f"{mon} {year}")
    return sorted(set(found))


def missing_paths(body: str, root: Path, basenames: set[str]) -> list[str]:
    missing: list[str] = []
    for token in BACKTICK_RE.findall(body):
        token = token.strip()
        if " " in token or "://" in token or "{" in token or "}" in token:
            continue
        pathish = "/" in token or token.endswith(PATHISH_SUFFIXES)
        if not pathish or token.startswith(("-", "$", "~", "@", "/", "*")):
            continue
        if token.startswith((".", "..")) and "/" not in token:
            continue
        candidate = root / token
        if candidate.exists():
            continue
        last = token.rstrip("/").split("/")[-1]
        if last in basenames:
            continue
        if token not in missing:
            missing.append(token)
    return missing


def record_for(path: Path, root: Path, today: datetime, stale_days: int, basenames: set[str]) -> dict[str, Any]:
    text = read_text(path)
    fields, body = parse_frontmatter(text)
    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    meta = fields.get("metadata") if isinstance(fields.get("metadata"), dict) else {}
    modified = meta.get("modified") or fields.get("modified") or ""
    lower_body = body.lower()

    return {
        "file": path.name,
        "name": fields.get("name") or path.stem,
        "type": memory_type(fields),
        "description": fields.get("description", ""),
        "modified_field": modified,
        "age_days": (today - mtime).days,
        "body_lines": len(body.splitlines()),
        "has_frontmatter": bool(fields),
        "has_why": "**why:**" in lower_body or "\nwhy:" in lower_body,
        "has_how": "how to apply" in lower_body,
        "wikilinks": WIKILINK_RE.findall(body),
        "past_dates": past_dates(body, today, stale_days),
        "missing_paths": missing_paths(body, root, basenames),
        "name_is_slug": bool(fields.get("name")) and fields.get("name") == slugify(fields.get("name", "")),
        "words": sorted(content_words(body + " " + fields.get("description", ""))),
    }


def parse_index(index_path: Path) -> dict[str, Any]:
    if not index_path.exists():
        return {"exists": False, "lines": 0, "entries": [], "content_lines": 0}
    text = read_text(index_path)
    entries: list[dict[str, str]] = []
    content_lines = 0
    for line in text.splitlines():
        match = INDEX_ENTRY_RE.match(line)
        if match:
            entries.append({"title": match.group(1), "target": match.group(2)})
        elif line.strip().startswith("-") and len(line) > 160:
            content_lines += 1
    return {
        "exists": True,
        "lines": len(text.splitlines()),
        "entries": entries,
        "content_lines": content_lines,
    }


# Folder names projects commonly use for always-on context that a correction can
# graduate into. Checked case-insensitively; absent names are skipped.
CONTEXT_FOLDER_NAMES = ("foundational", "context", "docs", "guidelines", "standards")


def context_folders(root: Path) -> list[Path]:
    """Return project context folders that exist, whatever the project calls them."""
    folders = [root / ".claude" / "rules", root / ".claude" / "output-styles"]
    try:
        entries = sorted(p for p in root.iterdir() if p.is_dir())
    except OSError:
        entries = []
    for entry in entries:
        if entry.name.lower() in CONTEXT_FOLDER_NAMES:
            folders.append(entry)
    return folders


def project_sources(root: Path) -> list[tuple[str, set[str]]]:
    sources: list[tuple[str, set[str]]] = []
    candidates = [root / "CLAUDE.md", root / ".claude" / "CLAUDE.md", root / "AGENTS.md"]
    for folder in context_folders(root):
        if folder.is_dir():
            candidates.extend(sorted(folder.glob("*.md")))
    for path in candidates:
        if path.is_file():
            try:
                sources.append((path.relative_to(root).as_posix(), content_words(read_text(path))))
            except OSError:
                continue
    return sources


def build_inventory(root: Path, stale_days: int, overlap_threshold: float, placement_threshold: float) -> dict[str, Any]:
    today = datetime.now(timezone.utc)
    memory_dir, how_found = memory_dir_for(root)
    result: dict[str, Any] = {
        "project_root": str(root),
        "memory_dir": str(memory_dir) if memory_dir else None,
        "memory_dir_resolution": how_found,
        "user_layer": {
            "claude_md": (Path.home() / ".claude" / "CLAUDE.md").is_file(),
            "rules_dir": (Path.home() / ".claude" / "rules").is_dir(),
        },
        "notes": [
            "Deterministic checks only. Whether a memory is still true, still needed, or "
            "contradicted in meaning requires reading it against the project.",
            "Overlap and placement hints are lexical signals, not verdicts.",
            "Past dates are dates the memory mentions that fall outside the staleness "
            "window; they flag a claim to check, not a stale memory.",
            "Missing paths are backticked project-relative paths that do not exist now.",
        ],
    }
    if memory_dir is None:
        result["notes"].append("No memory folder found for this project.")
        return result

    files = sorted(p for p in memory_dir.glob("*.md") if p.name != "MEMORY.md")
    basenames = project_basenames(root)
    records = [record_for(p, root, today, stale_days, basenames) for p in files]
    index = parse_index(memory_dir / "MEMORY.md")

    file_names = {r["file"] for r in records}
    indexed_targets = {e["target"] for e in index["entries"]}
    orphans = sorted(file_names - indexed_targets)
    broken_entries = sorted(t for t in indexed_targets if t not in file_names)

    names = {slugify(r["name"]) for r in records} | {slugify(Path(r["file"]).stem) for r in records}
    for record in records:
        record["broken_wikilinks"] = sorted({w for w in record["wikilinks"] if slugify(w) not in names})

    overlaps: list[dict[str, Any]] = []
    for left, right in combinations(records, 2):
        lw, rw = set(left["words"]), set(right["words"])
        if not lw or not rw:
            continue
        shared = lw & rw
        score = len(shared) / len(lw | rw)
        if score >= overlap_threshold and len(shared) >= 6:
            overlaps.append({"a": left["file"], "b": right["file"], "score": round(score, 3), "shared_terms": sorted(shared)[:12]})
    overlaps.sort(key=lambda o: o["score"], reverse=True)

    sources = project_sources(root)
    placements: list[dict[str, Any]] = []
    for record in records:
        mw = set(record["words"])
        if len(mw) < 8:
            continue
        best = None
        for source_name, source_words in sources:
            containment = len(mw & source_words) / len(mw)
            if containment >= placement_threshold and (best is None or containment > best[1]):
                best = (source_name, containment)
        if best:
            placements.append({"memory": record["file"], "type": record["type"], "project_file": best[0], "containment": round(best[1], 3)})
    placements.sort(key=lambda p: p["containment"], reverse=True)

    type_counts: dict[str, int] = {}
    for record in records:
        type_counts[record["type"]] = type_counts.get(record["type"], 0) + 1

    for record in records:
        record.pop("words", None)
        record.pop("wikilinks", None)

    result.update(
        {
            "stale_days": stale_days,
            "memory_count": len(records),
            "type_counts": type_counts,
            "index": {"exists": index["exists"], "lines": index["lines"], "entry_count": len(index["entries"]), "content_lines": index["content_lines"], "orphans": orphans, "broken_entries": broken_entries},
            "memories": records,
            "overlap_hints": overlaps[:20],
            "placement_hints": placements[:20],
            "project_sources_checked": [name for name, _ in sources],
        }
    )
    return result


def esc(value: Any) -> str:
    return html.escape(str(value), quote=False).replace("|", "\\|").replace("\n", " ")


def render_markdown(inv: dict[str, Any]) -> str:
    mark = chr(96)
    out = ["# Claude Code Memory Inventory", "", f"Project root: {mark}{inv['project_root']}{mark}"]
    if not inv.get("memory_dir"):
        out += ["", "No memory folder found for this project.", "", "## Notes", ""]
        out += [f"- {n}" for n in inv["notes"]]
        return "\n".join(out)

    idx = inv["index"]
    out += [
        f"Memory folder: {mark}{inv['memory_dir']}{mark} ({inv['memory_dir_resolution']})",
        f"Memories: {inv['memory_count']}  Types: " + ", ".join(f"{k} {v}" for k, v in sorted(inv["type_counts"].items())),
        f"Index: {'present' if idx['exists'] else 'missing'}, {idx['lines']} lines, {idx['entry_count']} entries" + (f", {idx['content_lines']} long lines that may carry content" if idx["content_lines"] else ""),
        "User layer: " + ("~/.claude/CLAUDE.md present" if inv["user_layer"]["claude_md"] else "no ~/.claude/CLAUDE.md") + (", ~/.claude/rules present" if inv["user_layer"]["rules_dir"] else ""),
        "",
        "## Memories",
        "",
        "| File | Type | Age (days) | Why | How | Past dates | Missing paths | Broken links |",
        "| --- | --- | ---: | :-: | :-: | --- | --- | --- |",
    ]
    for r in inv["memories"]:
        out.append(
            "| {f} | {t} | {a} | {w} | {h} | {d} | {m} | {b} |".format(
                f=esc(r["file"]), t=r["type"], a=r["age_days"],
                w="yes" if r["has_why"] else "no", h="yes" if r["has_how"] else "no",
                d=esc(", ".join(r["past_dates"])) or "", m=esc(", ".join(r["missing_paths"])) or "", b=esc(", ".join(r["broken_wikilinks"])) or "",
            )
        )

    out += ["", "## Frontmatter hygiene", ""]
    hygiene = []
    for r in inv["memories"]:
        problems = []
        if not r["has_frontmatter"]:
            problems.append("no frontmatter")
        elif r["type"] == "untyped":
            problems.append("no type")
        if r["has_frontmatter"] and not r["name_is_slug"]:
            problems.append("name is not a slug, so [[wikilinks]] to it will not resolve by name")
        if problems:
            hygiene.append(f"- {esc(r['file'])}: " + "; ".join(problems))
    out += hygiene or ["Every memory has frontmatter, a type, and a slug name."]

    out += ["", "## Index health", ""]
    if idx["orphans"]:
        out.append("- Orphans not in MEMORY.md: " + ", ".join(esc(o) for o in idx["orphans"]))
    if idx["broken_entries"]:
        out.append("- Index entries pointing at missing files: " + ", ".join(esc(b) for b in idx["broken_entries"]))
    if idx["lines"] >= 180:
        out.append(f"- Index is {idx['lines']} lines; roughly the first 200 load automatically.")
    if not (idx["orphans"] or idx["broken_entries"] or idx["lines"] >= 180):
        out.append("No structural index problems detected.")

    out += ["", "## Staleness candidates", ""]
    stale = [r for r in inv["memories"] if r["type"] in {"project", "reference", "untyped"} and (r["past_dates"] or r["missing_paths"] or r["age_days"] > inv["stale_days"])]
    if stale:
        for r in stale:
            reasons = []
            if r["age_days"] > inv["stale_days"]:
                reasons.append(f"untouched {r['age_days']} days")
            if r["past_dates"]:
                reasons.append("mentions " + ", ".join(r["past_dates"]))
            if r["missing_paths"]:
                reasons.append("names missing " + ", ".join(r["missing_paths"]))
            out.append(f"- {esc(r['file'])} ({r['type']}): " + "; ".join(esc(x) for x in reasons))
    else:
        out.append("None flagged.")

    out += ["", "## Unactionable candidates", ""]
    weak = [r for r in inv["memories"] if r["type"] in {"feedback", "project"} and not (r["has_why"] and r["has_how"])]
    if weak:
        for r in weak:
            missing = [x for x, ok in (("Why", r["has_why"]), ("How to apply", r["has_how"])) if not ok]
            out.append(f"- {esc(r['file'])} ({r['type']}): missing " + " and ".join(missing))
    else:
        out.append("Every feedback and project memory carries Why and How-to-apply lines.")

    out += ["", "## Overlap hints between memories", ""]
    out += [f"- {esc(o['a'])} and {esc(o['b'])} (score {o['score']}): {esc(', '.join(o['shared_terms']))}" for o in inv["overlap_hints"]] or ["None above threshold."]

    out += ["", "## Placement hints (memory content largely present in a project file)", ""]
    out += [f"- {esc(p['memory'])} ({p['type']}) overlaps {esc(p['project_file'])} (containment {p['containment']})" for p in inv["placement_hints"]] or ["None above threshold."]

    out += ["", "## Notes", ""]
    out += [f"- {n}" for n in inv["notes"]]
    out.append("- Project files checked for placement: " + ", ".join(esc(s) for s in inv["project_sources_checked"]))
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory Claude Code auto memory for a project.")
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--stale-days", type=int, default=45, help="Age and date horizon for staleness candidates. Defaults to 45.")
    parser.add_argument("--overlap-threshold", type=float, default=0.12)
    parser.add_argument("--placement-threshold", type=float, default=0.45)
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    if not root.is_dir():
        print(f"error: project root is not a directory: {root}", file=sys.stderr)
        return 2
    try:
        inventory = build_inventory(root, args.stale_days, args.overlap_threshold, args.placement_threshold)
    except OSError as exc:
        print(f"error: unable to inventory memory: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(inventory, indent=2, sort_keys=True) if args.format == "json" else render_markdown(inventory))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
