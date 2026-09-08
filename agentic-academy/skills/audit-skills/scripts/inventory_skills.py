#!/usr/bin/env python3
"""Inventory Claude Code Skills and commands without printing full bodies."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from itertools import combinations
from pathlib import Path
from typing import Any


LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+)\)")
STOPWORDS = {
    "a", "an", "and", "any", "are", "as", "at", "be", "by", "can", "do", "does",
    "for", "from", "has", "have", "how", "if", "in", "into", "is", "it", "its",
    "not", "of", "on", "or", "should", "that", "the", "their", "them", "then",
    "this", "to", "use", "used", "uses", "user", "want", "wants", "when", "whenever",
    "which", "while", "will", "with", "you", "your", "also", "asks", "says",
    "skill", "skills", "claude", "code", "file", "files", "trigger", "triggered",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return (frontmatter fields, body). Handles simple single-line YAML values."""
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

    fields: dict[str, str] = {}
    current_key: str | None = None
    for raw in lines[1:closing]:
        match = re.match(r"^([A-Za-z][\w-]*)\s*:\s*(.*)$", raw)
        if match:
            current_key = match.group(1).lower()
            value = match.group(2).strip().strip("'\"")
            if value in {">", "|", ">-", "|-"}:
                value = ""
            fields[current_key] = value
        elif current_key and raw.startswith((" ", "\t")) and raw.strip():
            joined = (fields[current_key] + " " + raw.strip().strip("'\"")).strip()
            fields[current_key] = joined
    body = "\n".join(lines[closing + 1 :])
    return fields, body


def find_reference_targets(body: str, base: Path) -> tuple[list[str], list[str]]:
    """Return (resolved, broken) relative reference targets inside the skill folder."""
    resolved: list[str] = []
    broken: list[str] = []
    seen: set[str] = set()

    for match in LINK_RE.finditer(body):
        target = match.group(1).strip()
        if target in seen:
            continue
        seen.add(target)
        if ":" in target or target.startswith(("#", "/")):
            continue
        first_segment = target.split("/")[0]
        if (
            "/" in target
            and re.fullmatch(r"[\w-]+(\.[\w-]+)+", first_segment)
            and not (base / first_segment).exists()
        ):
            continue
        candidate = base / target
        if candidate.exists():
            resolved.append(target)
        else:
            broken.append(target)

    return resolved, broken


def content_words(text: str) -> set[str]:
    words = re.findall(r"[a-z][a-z0-9-]{2,}", text.lower())
    return {word for word in words if word not in STOPWORDS}


def list_bundled(base: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for sub in ("references", "scripts", "assets", "agents", "evals"):
        folder = base / sub
        if folder.is_dir():
            counts[sub] = sum(1 for item in folder.rglob("*") if item.is_file())
    return counts


def record_for(path: Path, layer: str, kind: str, root: Path) -> dict[str, Any]:
    text = read_text(path)
    fields, body = parse_frontmatter(text)
    base = path.parent if kind == "skill" else path.parent
    resolved, broken = find_reference_targets(body, base)

    description = fields.get("description", "")
    manual_only = fields.get("disable-model-invocation", "").lower() in {"true", "yes"}

    try:
        shown_path = path.relative_to(root).as_posix()
    except ValueError:
        shown_path = str(path)

    name = fields.get("name") or (
        path.parent.name if path.name == "SKILL.md" else path.stem
    )

    return {
        "name": name,
        "path": shown_path,
        "layer": layer,
        "kind": kind,
        "mode": "manual-only" if manual_only else "automatic",
        "description": description,
        "description_words": len(description.split()),
        "body_lines": len(body.splitlines()),
        "bundled": list_bundled(base) if kind == "skill" else {},
        "references_resolved": len(resolved),
        "references_broken": broken,
        "has_description": bool(description),
        "allowed_tools": fields.get("allowed-tools", ""),
    }


def discover_layer(base: Path, layer: str, root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    skills_dir = base / ".claude" / "skills"
    if skills_dir.is_dir():
        for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
            records.append(record_for(skill_md, layer, "skill", root))

    commands_dir = base / ".claude" / "commands"
    if commands_dir.is_dir():
        for command_md in sorted(commands_dir.rglob("*.md")):
            records.append(record_for(command_md, layer, "command", root))

    return records


def overlap_hints(
    records: list[dict[str, Any]], threshold: float, max_hints: int
) -> list[dict[str, Any]]:
    hints: list[dict[str, Any]] = []
    described = [r for r in records if r["has_description"]]

    for left, right in combinations(described, 2):
        left_words = content_words(left["description"])
        right_words = content_words(right["description"])
        if not left_words or not right_words:
            continue
        shared = left_words & right_words
        union = left_words | right_words
        score = len(shared) / len(union)
        if score >= threshold and len(shared) >= 3:
            hints.append(
                {
                    "a": left["name"],
                    "b": right["name"],
                    "score": round(score, 3),
                    "shared_terms": sorted(shared)[:12],
                }
            )

    hints.sort(key=lambda item: item["score"], reverse=True)
    return hints[:max_hints]


def build_inventory(
    root: Path, include_personal: bool, threshold: float, max_hints: int
) -> dict[str, Any]:
    records = discover_layer(root, "project", root)
    if include_personal:
        home = Path.home()
        if home.resolve() != root.resolve():
            records.extend(discover_layer(home, "personal", root))

    always_loaded_words = sum(
        r["description_words"] for r in records if r["mode"] == "automatic"
    )

    notes = [
        "Skill and command layers only. Plugin skills, agents, hooks, and MCP are "
        "not inventoried; name visible plugin skills and agents in the report as "
        "competing routes.",
        "Full bodies are not printed. Descriptions are truncated in markdown output.",
        "Overlap hints are lexical signals, not verdicts. Confirm or dismiss each by "
        "reading both descriptions.",
        "Broken references are relative link targets that do not exist on disk.",
    ]
    if not include_personal:
        notes.append("Personal layer excluded by flag.")
    if not records:
        notes.append("No skills or commands found in the inspected layers.")

    return {
        "project_root": str(root),
        "layers": ["project", "personal"] if include_personal else ["project"],
        "skill_count": sum(1 for r in records if r["kind"] == "skill"),
        "command_count": sum(1 for r in records if r["kind"] == "command"),
        "always_loaded_description_words": always_loaded_words,
        "sources": records,
        "overlap_hints": overlap_hints(records, threshold, max_hints),
        "notes": notes,
    }


def markdown_escape(value: Any) -> str:
    return html.escape(str(value), quote=False).replace("|", "\\|").replace("\n", " ")


def truncate(text: str, limit: int = 110) -> str:
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def render_markdown(inventory: dict[str, Any]) -> str:
    mark = chr(96)
    lines = [
        "# Claude Code Skill Inventory",
        "",
        f"Project root: {mark}{inventory['project_root']}{mark}",
        f"Layers: {', '.join(inventory['layers'])}",
        f"Skills: {inventory['skill_count']}  Commands: {inventory['command_count']}",
        "Always-loaded description words (automatic mode): "
        f"{inventory['always_loaded_description_words']}",
        "",
        "## Sources",
        "",
    ]

    if inventory["sources"]:
        lines.extend(
            [
                "| Name | Layer | Kind | Mode | Desc words | Body lines | Broken refs | Description |",
                "| --- | --- | --- | --- | ---: | ---: | ---: | --- |",
            ]
        )
        for record in inventory["sources"]:
            lines.append(
                "| {name} | {layer} | {kind} | {mode} | {dwords} | {blines} | {broken} | {desc} |".format(
                    name=markdown_escape(record["name"]),
                    layer=record["layer"],
                    kind=record["kind"],
                    mode=record["mode"],
                    dwords=record["description_words"],
                    blines=record["body_lines"],
                    broken=len(record["references_broken"]),
                    desc=markdown_escape(truncate(record["description"]))
                    or "(missing)",
                )
            )
    else:
        lines.append("No skills or commands found.")

    broken_records = [r for r in inventory["sources"] if r["references_broken"]]
    lines.extend(["", "## Broken references", ""])
    if broken_records:
        for record in broken_records:
            targets = ", ".join(
                markdown_escape(target) for target in record["references_broken"]
            )
            lines.append(f"- {markdown_escape(record['name'])}: {targets}")
    else:
        lines.append("None detected.")

    lines.extend(["", "## Overlap hints", ""])
    if inventory["overlap_hints"]:
        for hint in inventory["overlap_hints"]:
            shared = ", ".join(hint["shared_terms"])
            lines.append(
                f"- {markdown_escape(hint['a'])} and {markdown_escape(hint['b'])} "
                f"(score {hint['score']}): {markdown_escape(shared)}"
            )
    else:
        lines.append("None above threshold.")

    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in inventory["notes"])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory Claude Code Skills and commands."
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Project root to inspect. Defaults to the current directory.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--project-only",
        action="store_true",
        help="Skip the personal layer under the home directory.",
    )
    parser.add_argument(
        "--overlap-threshold",
        type=float,
        default=0.18,
        help="Minimum description-similarity score to report. Defaults to 0.18.",
    )
    parser.add_argument(
        "--max-hints",
        type=int,
        default=25,
        help="Maximum overlap hints to report. Defaults to 25.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).expanduser().resolve()

    if not root.exists() or not root.is_dir():
        print(f"error: project root is not a directory: {root}", file=sys.stderr)
        return 2

    try:
        inventory = build_inventory(
            root,
            include_personal=not args.project_only,
            threshold=args.overlap_threshold,
            max_hints=args.max_hints,
        )
    except OSError as exc:
        print(f"error: unable to inventory skills: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(inventory, indent=2, sort_keys=True))
    else:
        print(render_markdown(inventory))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
