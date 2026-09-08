#!/usr/bin/env python3
"""Report when each Skill or slash command was last activated.

Reads Claude Code session transcripts (~/.claude/projects/*/*.jsonl) and counts
activations. An activation is one of:

  - a Skill tool call (the model invoking a skill explicitly)
  - a <command-name> block (a slash command typed by the user)

LIMIT: description-match activation, where a skill loads because its description
matched the request without an explicit call, does not always leave a distinct
record. A skill absent from this report was not necessarily unused.

Usage:
  python3 skill_activation_log.py [--project SUBSTR] [--days N]
"""
import argparse, collections, glob, json, os, re, sys
from datetime import datetime, timedelta, timezone

CPAT = re.compile(r'<command-name>/?([a-zA-Z0-9_:-]+)</command-name>')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", help="only transcripts whose dir name contains this")
    ap.add_argument("--days", type=int, help="only activations in the last N days")
    ap.add_argument("--root", default=os.path.expanduser("~/.claude/projects"))
    a = ap.parse_args()

    cutoff = ""
    if a.days:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=a.days)).isoformat()

    act = collections.defaultdict(
        lambda: {"n": 0, "last": "", "how": collections.Counter(), "projects": set()})
    files = glob.glob(os.path.join(a.root, "*", "*.jsonl"))
    if a.project:
        files = [f for f in files if a.project in os.path.dirname(f)]

    for f in files:
        proj = os.path.basename(os.path.dirname(f))
        try:
            fh = open(f, errors="replace")
        except OSError:
            continue
        with fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                ts = d.get("timestamp") or ""
                if cutoff and ts < cutoff:
                    continue

                def hit(name, how):
                    e = act[name]
                    e["n"] += 1
                    e["how"][how] += 1
                    e["projects"].add(proj)
                    if ts > e["last"]:
                        e["last"] = ts

                content = (d.get("message") or {}).get("content")
                if isinstance(content, list):
                    for c in content:
                        if (isinstance(c, dict) and c.get("type") == "tool_use"
                                and c.get("name") == "Skill"):
                            n = (c.get("input") or {}).get("skill")
                            if n:
                                hit(n, "Skill tool")
                if d.get("type") == "user":
                    txt = content if isinstance(content, str) else json.dumps(content)
                    for m in CPAT.finditer(txt):
                        hit(m.group(1), "slash cmd")

    if not act:
        print("No activations found.")
        return 0

    print(f"Scanned {len(files)} transcripts\n")
    print(f"{'route':<44} {'acts':>5}  {'last activated':<12}  how")
    for name, e in sorted(act.items(), key=lambda kv: kv[1]["last"], reverse=True):
        how = ",".join(f"{k}:{v}" for k, v in e["how"].most_common())
        print(f"{name:<44} {e['n']:>5}  {e['last'][:10]:<12}  {how}")
    print(f"\n{len(act)} routes with an activation record.")
    print("Absent from this list is not proof of disuse: description-match "
          "activation is not always recorded.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
