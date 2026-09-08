#!/usr/bin/env python3
"""Inventory project-scoped Claude Code instruction sources without printing content."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from collections import deque
from pathlib import Path
from typing import Any


EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
    ".next",
    ".cache",
}

SENSITIVE_PARTS = {
    ".ssh",
    ".gnupg",
    ".aws",
    ".kube",
    ".secrets",
    "secrets",
}

MEMORY_NAMES = {"CLAUDE.md", "CLAUDE.local.md"}
AGENT_MANUAL_NAMES = {"AGENTS.md"}
IMPORT_RE = re.compile(r"(?<![\w.+-])@([~./A-Za-z0-9_-][^\s\x60\"'<>()[\]{}]*)")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
INLINE_CODE_RE = re.compile(r"\x60[^\x60\n]*\x60")


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve())
        return True
    except ValueError:
        return False


def display_path(path: Path, root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def is_sensitive(path: Path) -> bool:
    for part in path.parts:
        if part in SENSITIVE_PARTS or part.startswith(".env"):
            return True
    return False


def under_claude_subdir(path: Path, root: Path, subdir: str) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return False
    for index in range(len(parts) - 1):
        if parts[index] == ".claude" and parts[index + 1] == subdir:
            return True
    return False


def under_output_styles_dir(path: Path, root: Path) -> bool:
    return under_claude_subdir(path, root, "output-styles")


def under_rules_dir(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return False
    for index in range(len(parts) - 1):
        if parts[index] == ".claude" and parts[index + 1] == "rules":
            return True
    return False


def discover_sources(root: Path) -> list[Path]:
    sources: set[Path] = set()

    for current, dirnames, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        kept_dirs = []
        for dirname in dirnames:
            candidate = current_path / dirname
            if dirname in EXCLUDED_DIRS:
                continue
            if candidate.is_symlink():
                continue
            kept_dirs.append(dirname)
        dirnames[:] = kept_dirs

        for filename in filenames:
            candidate = current_path / filename
            if candidate.is_symlink() and not is_within(candidate, root):
                continue
            if filename in MEMORY_NAMES or filename in AGENT_MANUAL_NAMES:
                sources.add(candidate)
            elif candidate.suffix.lower() == ".md" and (
                under_rules_dir(candidate, root)
                or under_output_styles_dir(candidate, root)
            ):
                sources.add(candidate)

    return sorted(sources, key=lambda item: display_path(item, root).lower())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_paths_frontmatter(text: str) -> list[str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return []

    closing_index = None
    for index in range(1, min(len(lines), 200)):
        if lines[index].strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        return []

    frontmatter = lines[1:closing_index]
    results: list[str] = []
    collecting = False

    for line in frontmatter:
        match = re.match(r"^\s*paths\s*:\s*(.*)$", line)
        if match:
            collecting = True
            value = match.group(1).strip()
            if value.startswith("[") and value.endswith("]"):
                value = value[1:-1]
                results.extend(
                    item.strip().strip("'\"")
                    for item in value.split(",")
                    if item.strip()
                )
            elif value:
                results.append(value.strip("'\""))
                collecting = False
            continue

        if collecting:
            item_match = re.match(r"^\s*-\s*(.+?)\s*$", line)
            if item_match:
                results.append(item_match.group(1).strip().strip("'\""))
            elif line.strip():
                collecting = False

    return results


def strip_code_and_comments(text: str) -> str:
    text = HTML_COMMENT_RE.sub("", text)
    output: list[str] = []
    fence: str | None = None

    for line in text.splitlines():
        stripped = line.lstrip()
        if fence is None and (
            stripped.startswith(chr(96) * 3) or stripped.startswith("~~~")
        ):
            fence = stripped[:3]
            continue
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            continue
        output.append(INLINE_CODE_RE.sub("", line))

    return "\n".join(output)


def find_import_tokens(text: str) -> list[str]:
    cleaned = strip_code_and_comments(text)
    tokens: list[str] = []

    for match in IMPORT_RE.finditer(cleaned):
        token = match.group(1).rstrip(".,;:!?")
        if not token:
            continue
        pathish = (
            "/" in token
            or "." in token
            or token.startswith("~")
            or token.upper() == token
        )
        if pathish and token not in tokens:
            tokens.append(token)

    return tokens


def resolve_import(token: str, source: Path) -> Path:
    if token.startswith("~"):
        return Path(token).expanduser()
    candidate = Path(token)
    if candidate.is_absolute():
        return candidate
    return source.parent / candidate


def classify_source(path: Path, root: Path, imported: bool = False) -> tuple[str, str]:
    relative = display_path(path, root)
    if imported:
        return "imported", "loaded by import"
    if path.name == "CLAUDE.local.md":
        return "local memory", "project-local"
    if under_rules_dir(path, root):
        return "rule", "project or path-specific"
    if under_output_styles_dir(path, root):
        return "output style", "global when the style is active"
    if path.name in AGENT_MANUAL_NAMES:
        parent = Path(relative).parent.as_posix()
        if parent in {"", "."}:
            return "agent manual", "other agents; not loaded by Claude Code"
        return "agent manual", f"other agents; not loaded by Claude Code (under {parent})"
    if relative in {"CLAUDE.md", ".claude/CLAUDE.md"}:
        return "project memory", "project"
    if path.name == "CLAUDE.md":
        parent = Path(relative).parent.as_posix()
        return "nested memory", f"on demand under {parent}"
    return "instruction", "project"


def source_record(path: Path, root: Path, imported: bool = False) -> dict[str, Any]:
    text = read_text(path)
    kind, scope = classify_source(path, root, imported=imported)
    path_patterns = parse_paths_frontmatter(text) if kind == "rule" else []
    if path_patterns:
        scope = "paths: " + ", ".join(path_patterns)

    return {
        "path": display_path(path, root),
        "kind": kind,
        "scope": scope,
        "lines": len(text.splitlines()),
        "bytes": path.stat().st_size,
        "path_patterns": path_patterns,
    }


def import_map(
    initial_sources: list[Path], root: Path, max_depth: int
) -> tuple[list[dict[str, Any]], list[Path]]:
    edges: list[dict[str, Any]] = []
    imported_sources: set[Path] = set()
    queue = deque((source, 0, (source.resolve(strict=False),)) for source in initial_sources)
    parsed_depth: dict[Path, int] = {}

    while queue:
        source, depth, lineage = queue.popleft()
        canonical_source = source.resolve(strict=False)
        if canonical_source in parsed_depth and parsed_depth[canonical_source] <= depth:
            continue
        parsed_depth[canonical_source] = depth

        try:
            tokens = find_import_tokens(read_text(source))
        except OSError:
            continue

        for token in tokens:
            unresolved = resolve_import(token, source)
            resolved = unresolved.resolve(strict=False)
            edge: dict[str, Any] = {
                "from": display_path(source, root),
                "token": token,
                "target": display_path(unresolved, root),
                "depth": depth + 1,
                "status": "ok",
            }

            if not is_within(resolved, root):
                edge["status"] = "external"
            elif resolved in lineage:
                edge["status"] = "cycle"
            elif not resolved.exists():
                edge["status"] = (
                    "missing-sensitive" if is_sensitive(resolved) else "missing"
                )
            elif is_sensitive(resolved):
                edge["status"] = "blocked-sensitive"
            elif not resolved.is_file():
                edge["status"] = "not-a-file"
            elif depth + 1 > max_depth:
                edge["status"] = "depth-limit"
            else:
                imported_sources.add(resolved)
                if depth + 1 < max_depth:
                    queue.append((resolved, depth + 1, lineage + (resolved,)))

            edges.append(edge)

    return edges, sorted(imported_sources, key=lambda item: display_path(item, root).lower())


def build_inventory(root: Path, max_depth: int) -> dict[str, Any]:
    discovered = discover_sources(root)
    imports, imported = import_map(discovered, root, max_depth)
    discovered_set = {path.resolve(strict=False) for path in discovered}

    sources = [source_record(path, root) for path in discovered]
    for path in imported:
        if path.resolve(strict=False) not in discovered_set:
            sources.append(source_record(path, root, imported=True))

    sources.sort(key=lambda item: item["path"].lower())
    imports.sort(key=lambda item: (item["from"].lower(), item["depth"], item["token"]))

    notes = [
        "Project-scoped inventory only. User and organization instructions are excluded.",
        "File contents are not printed.",
        "External and sensitive imports are reported but not read.",
        "Symlinked directories are not followed.",
        "Project output styles are listed when present. A user-level output style is out "
        "of scope here but can still shape behavior; name the active style in the report.",
        "AGENTS.md is listed for cross-agent alignment. Claude Code does not load it as "
        "project memory.",
    ]
    if not discovered:
        notes.append(
            "No project instruction sources found: no CLAUDE.md, CLAUDE.local.md, "
            "AGENTS.md, .claude/rules, or .claude/output-styles Markdown files."
        )

    return {
        "project_root": str(root),
        "max_import_depth": max_depth,
        "sources": sources,
        "imports": imports,
        "notes": notes,
    }


def markdown_escape(value: Any) -> str:
    return html.escape(str(value), quote=False).replace("|", "\\|").replace("\n", " ")


def render_markdown(inventory: dict[str, Any]) -> str:
    mark = chr(96)
    lines = [
        "# Claude Code Instruction Inventory",
        "",
        f"Project root: {mark}{inventory['project_root']}{mark}",
        "",
        "## Sources",
        "",
    ]

    if inventory["sources"]:
        lines.extend(
            [
                "| Path | Kind | Scope | Lines | Bytes |",
                "| --- | --- | --- | ---: | ---: |",
            ]
        )
        for source in inventory["sources"]:
            lines.append(
                "| {path} | {kind} | {scope} | {lines} | {bytes} |".format(
                    path=markdown_escape(source["path"]),
                    kind=markdown_escape(source["kind"]),
                    scope=markdown_escape(source["scope"]),
                    lines=source["lines"],
                    bytes=source["bytes"],
                )
            )
    else:
        lines.append("No project instruction sources found.")

    lines.extend(["", "## Imports", ""])
    if inventory["imports"]:
        lines.extend(
            [
                "| From | Import | Target | Depth | Status |",
                "| --- | --- | --- | ---: | --- |",
            ]
        )
        for edge in inventory["imports"]:
            lines.append(
                "| {source} | {token} | {target} | {depth} | {status} |".format(
                    source=markdown_escape(edge["from"]),
                    token=markdown_escape(edge["token"]),
                    target=markdown_escape(edge["target"]),
                    depth=edge["depth"],
                    status=markdown_escape(edge["status"]),
                )
            )
    else:
        lines.append("No imports detected.")

    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in inventory["notes"])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory project-scoped Claude Code instruction sources."
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
        "--max-import-depth",
        type=int,
        default=4,
        help="Maximum recursive import depth. Defaults to 4.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).expanduser().resolve()

    if not root.exists() or not root.is_dir():
        print(f"error: project root is not a directory: {root}", file=sys.stderr)
        return 2
    if args.max_import_depth < 0:
        print("error: --max-import-depth must be zero or greater", file=sys.stderr)
        return 2

    try:
        inventory = build_inventory(root, args.max_import_depth)
    except OSError as exc:
        print(f"error: unable to inventory instructions: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(inventory, indent=2, sort_keys=True))
    else:
        print(render_markdown(inventory))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
