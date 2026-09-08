#!/usr/bin/env bash
#
# sync_skills.sh — copy every installed Claude skill from the read-only
# skills cache into a target project's .claude/skills folder.
#
# Usage:
#   sync_skills.sh <SRC_CACHE> <DST_PROJECT_ROOT>
#
#   SRC_CACHE         Directory that holds the installed skill folders
#                     (each subfolder has a SKILL.md). This is the read-only
#                     plugin/skills cache.
#   DST_PROJECT_ROOT  The project folder to copy into. The script creates
#                     <DST_PROJECT_ROOT>/.claude/skills if it doesn't exist.
#
# Behaviour:
#   - Creates the destination .claude/skills folder if missing.
#   - Copies each skill folder that contains a SKILL.md.
#   - Makes the copies writable (the source cache is read-only).
#   - Skips anything without a SKILL.md (junk / partial folders).
#   - Prints a summary of what was copied.

set -euo pipefail

SRC="${1:-}"
DST_ROOT="${2:-}"

if [[ -z "$SRC" || -z "$DST_ROOT" ]]; then
  echo "ERROR: need two arguments: <SRC_CACHE> <DST_PROJECT_ROOT>" >&2
  echo "Example: sync_skills.sh /path/to/cache/skills /path/to/my-project" >&2
  exit 1
fi

if [[ ! -d "$SRC" ]]; then
  echo "ERROR: source cache not found: $SRC" >&2
  exit 1
fi

DST="$DST_ROOT/.claude/skills"
mkdir -p "$DST"

copied=0

for dir in "$SRC"/*/; do
  [[ -d "$dir" ]] || continue
  name="$(basename "$dir")"

  # only treat it as a skill if it has a SKILL.md
  if [[ ! -f "$dir/SKILL.md" ]]; then
    continue
  fi

  # The source cache is read-only, so a plain `cp -R` would recreate the
  # folders read-only and then fail to write files inside them. Copy without
  # preserving modes; fall back to tar (which fixes dir modes on extract) if
  # the cp flag isn't supported. Then force the copies writable.
  chmod -R u+w "${DST:?}/$name" 2>/dev/null || true
  rm -rf "${DST:?}/$name" 2>/dev/null || true
  if ! cp -R --no-preserve=mode "$dir" "$DST/$name" 2>/dev/null; then
    rm -rf "${DST:?}/$name" 2>/dev/null || true
    ( cd "$SRC" && tar cf - "$name" ) | ( cd "$DST" && tar xf - )
  fi
  chmod -R u+w "$DST/$name" 2>/dev/null || true
  copied=$((copied + 1))
  echo "  copied  $name"
done

echo ""
echo "Done. $copied skill(s) copied into:"
echo "  $DST"
echo ""
echo "Skills now in project:"
ls -1 "$DST"
