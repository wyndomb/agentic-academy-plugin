#!/usr/bin/env python3
"""Create a bounded, content-free inventory for an operating-manual scan."""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from pathlib import Path
from typing import Iterable


EXCLUDED_DIRS = {
    ".git",
    ".aws",
    ".credentials",
    ".hg",
    ".svn",
    ".gnupg",
    ".kube",
    ".secrets",
    ".ssh",
    ".tox",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
    "credentials",
    "target",
    "tmp",
    "secrets",
    "temp",
    "cache",
    ".cache",
    ".next",
    ".nuxt",
    ".turbo",
}

SENSITIVE_NAMES = {
    ".env",
    ".envrc",
    ".env.local",
    ".env.production",
    ".npmrc",
    ".pypirc",
    "id_rsa",
    "id_ed25519",
    "credentials.json",
    "secrets.json",
}

SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}

MANUAL_NAMES = {"CLAUDE.md", "AGENTS.md"}

OVERVIEW_NAMES = {
    "README.md",
    "README.txt",
    "CONTRIBUTING.md",
    "PROJECT.md",
    "project.md",
    "OVERVIEW.md",
    "overview.md",
    "pyproject.toml",
    "package.json",
    "Cargo.toml",
    "go.mod",
    "Makefile",
    "justfile",
}

ROUTING_TERMS = {
    "rule",
    "rules",
    "standard",
    "standards",
    "guide",
    "guidelines",
    "process",
    "workflow",
    "template",
    "templates",
    "schema",
    "schemas",
    "test",
    "tests",
    "input",
    "inputs",
    "output",
    "outputs",
    "skill",
    "skills",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory a project without reading file contents."
    )
    parser.add_argument("root", nargs="?", default=".", help="Project root")
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="markdown",
        help="Output format",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=5000,
        help="Maximum files to inventory before truncating",
    )
    parser.add_argument(
        "--max-candidates",
        type=int,
        default=80,
        help="Maximum candidate routing files to print",
    )
    return parser.parse_args()


def is_sensitive(path: Path) -> bool:
    name = path.name.lower()
    if (
        name in SENSITIVE_NAMES
        or name.startswith(".env.")
        or path.suffix.lower() in SENSITIVE_SUFFIXES
    ):
        return True
    return any(term in name for term in ("secret", "credential", "private-key"))


def safe_relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def walk_files(root: Path, max_files: int) -> tuple[list[Path], bool]:
    files: list[Path] = []
    truncated = False

    for current, dirs, names in os.walk(root, followlinks=False):
        current_path = Path(current)
        dirs[:] = sorted(
            directory
            for directory in dirs
            if directory not in EXCLUDED_DIRS
            and not (current_path / directory).is_symlink()
        )

        for name in sorted(names):
            path = current_path / name
            if path.is_symlink() or is_sensitive(path):
                continue
            files.append(path)
            if len(files) >= max_files:
                truncated = True
                return files, truncated

    return files, truncated


def top_level_entries(root: Path) -> list[str]:
    entries: list[str] = []
    for path in sorted(root.iterdir(), key=lambda item: item.name.lower()):
        if path.name in EXCLUDED_DIRS or is_sensitive(path):
            continue
        suffix = "/" if path.is_dir() else ""
        entries.append(f"{path.name}{suffix}")
    return entries


def candidate_score(path: Path, root: Path) -> tuple[int, str]:
    relative = safe_relative(path, root)
    parts = [part.lower() for part in path.parts]
    stem_tokens = {
        token
        for part in parts
        for token in part.replace("_", "-").replace(".", "-").split("-")
    }
    score = 0

    if path.name in MANUAL_NAMES:
        score += 100
    if path.name in OVERVIEW_NAMES:
        score += 70
    if path.name == "SKILL.md":
        score += 60
    if ROUTING_TERMS.intersection(stem_tokens):
        score += 35
    if ".claude" in parts or ".agents" in parts:
        score += 25
    if len(path.relative_to(root).parts) <= 2:
        score += 10

    return score, relative


def collect_candidates(
    files: Iterable[Path], root: Path, max_candidates: int
) -> list[str]:
    scored = [candidate_score(path, root) for path in files]
    return [
        relative
        for score, relative in sorted(scored, key=lambda item: (-item[0], item[1]))
        if score > 0
    ][:max_candidates]


def extension_counts(files: Iterable[Path]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for path in files:
        extension = path.suffix.lower() or "[no extension]"
        counts[extension] += 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:20])


def detect_platform_paths(files: Iterable[Path], root: Path) -> dict[str, list[str]]:
    detected = {"manuals": [], "claude": [], "codex": []}
    for path in files:
        relative = safe_relative(path, root)
        parts = path.relative_to(root).parts
        if path.name in MANUAL_NAMES:
            detected["manuals"].append(relative)
        if parts and parts[0] == ".claude":
            detected["claude"].append(relative)
        if parts and parts[0] == ".agents":
            detected["codex"].append(relative)
    return {key: sorted(values)[:40] for key, values in detected.items()}


def build_inventory(root: Path, max_files: int, max_candidates: int) -> dict:
    files, truncated = walk_files(root, max_files)
    return {
        "project_root": str(root),
        "inventory_is_content_free": True,
        "top_level_entries": top_level_entries(root),
        "file_count_scanned": len(files),
        "truncated": truncated,
        "extension_counts": extension_counts(files),
        "platform_paths": detect_platform_paths(files, root),
        "candidate_files_to_review": collect_candidates(
            files, root, max_candidates
        ),
        "excluded_directory_names": sorted(EXCLUDED_DIRS),
        "sensitive_files_omitted": True,
    }


def render_markdown(inventory: dict) -> str:
    lines = [
        "# Project Inventory",
        "",
        f"Project root: `{inventory['project_root']}`",
        f"Files scanned: {inventory['file_count_scanned']}",
        f"Truncated: {'yes' if inventory['truncated'] else 'no'}",
        "File contents read: no",
        "Sensitive filenames omitted: yes",
        "",
        "## Top-level entries",
        "",
    ]
    lines.extend(f"- `{entry}`" for entry in inventory["top_level_entries"])

    lines.extend(["", "## Existing agent files", ""])
    for label, paths in inventory["platform_paths"].items():
        lines.append(f"### {label.title()}")
        lines.extend(f"- `{path}`" for path in paths)
        if not paths:
            lines.append("- None detected")
        lines.append("")

    lines.extend(["## Candidate files to review", ""])
    lines.extend(
        f"- `{path}`" for path in inventory["candidate_files_to_review"]
    )
    if not inventory["candidate_files_to_review"]:
        lines.append("- None detected")

    lines.extend(["", "## Common file types", ""])
    lines.extend(
        f"- `{extension}`: {count}"
        for extension, count in inventory["extension_counts"].items()
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Project root is not a directory: {root}")
    if args.max_files < 1 or args.max_candidates < 1:
        raise SystemExit("--max-files and --max-candidates must be positive")

    inventory = build_inventory(root, args.max_files, args.max_candidates)
    if args.format == "json":
        print(json.dumps(inventory, indent=2))
    else:
        print(render_markdown(inventory))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
