#!/usr/bin/env python3
"""
parse_exports.py — Turn raw Claude and/or ChatGPT exports into a compact,
context-sized digest the skill can reason over.

Why this exists:
  Real exports are huge (tens of MB, hundreds of conversations). Loading the raw
  JSON into the model's context is wasteful and often impossible. This script does
  the deterministic, boring work — counting, clustering, sampling — and writes small
  files the model actually reads:
    - digest.json   : hard stats, repeated-opener clusters, longest context dumps,
                      a data-richness verdict, and a lightweight time-cost estimate.
    - samples.md    : a readable spread of the user's own words (for voice / topic /
                      automation-opportunity analysis by the model).
    - memory.md     : the user's saved memory / project memories / custom instructions,
                      extracted from memories.json / users.json (Claude) or the
                      equivalent ChatGPT files. THIS IS OFTEN THE RICHEST SIGNAL —
                      especially when the conversation export itself is thin.

Usage:
  python parse_exports.py --out <out_dir> [paths...]
  python parse_exports.py --out ./digest ~/Downloads/claude-export
  python parse_exports.py --out ./digest --scan ~/Downloads

It auto-detects Claude vs ChatGPT conversation exports, and separately looks for
memory/profile files (memories.json, users.json, user.json, *memory*.json) next to
them. Point it at a folder and it finds everything; point it at individual files and
it sorts them out.

A Claude export typically contains: conversations.json, memories.json, projects.json,
users.json. A ChatGPT export typically contains: conversations.json plus user/memory
files. The conversation file is optional here — if only memory is present, the script
still produces a usable digest (thin-data path).
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone

# ----------------------------------------------------------------------------
# Word regex (defined early; used by memory extraction and analysis alike)
# ----------------------------------------------------------------------------

WORD_RE = re.compile(r"\b\w+\b")
PUNCT_RE = re.compile(r"[^a-z0-9\s]")
WS_RE = re.compile(r"\s+")

# ----------------------------------------------------------------------------
# File discovery
# ----------------------------------------------------------------------------

CONVO_HINTS = ("conversation",)
MEMORY_NAMES = {"memories.json", "memory.json"}
PROFILE_NAMES = {"users.json", "user.json"}
PROJECT_NAMES = {"projects.json", "project.json"}


def _walk_json(path):
    out = []
    for root, _dirs, files in os.walk(path):
        for f in files:
            if f.lower().endswith(".json"):
                out.append(os.path.join(root, f))
    return out


def find_input_files(paths, scan_dir=None):
    """Collect candidate export JSON files, bucketed by kind.

    Returns dict with lists: conversations, memory, profile, project, other.
    Classification is by filename; conversation files are confirmed later by
    format detection so a misnamed file still gets handled correctly.
    """
    candidates = []
    for p in list(paths or []) + ([scan_dir] if scan_dir else []):
        p = os.path.expanduser(p)
        if os.path.isfile(p) and p.lower().endswith(".json"):
            candidates.append(p)
        elif os.path.isdir(p):
            candidates.extend(_walk_json(p))

    seen, uniq = set(), []
    for f in candidates:
        if f not in seen:
            seen.add(f)
            uniq.append(f)

    buckets = {"conversations": [], "memory": [], "profile": [], "project": [], "other": []}
    for f in uniq:
        name = os.path.basename(f).lower()
        if name in MEMORY_NAMES or "memor" in name:
            buckets["memory"].append(f)
        elif name in PROFILE_NAMES:
            buckets["profile"].append(f)
        elif name in PROJECT_NAMES:
            buckets["project"].append(f)
        elif name == "conversations.json" or any(h in name for h in CONVO_HINTS):
            buckets["conversations"].append(f)
        else:
            buckets["other"].append(f)
    return buckets


def _load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_format(data):
    """Return 'claude', 'chatgpt', or 'unknown' from parsed conversation JSON."""
    if isinstance(data, list) and data:
        sample = data[0]
        if isinstance(sample, dict):
            if "chat_messages" in sample:
                return "claude"
            if "mapping" in sample:
                return "chatgpt"
    return "unknown"


# ----------------------------------------------------------------------------
# Normalizing conversations into a common shape
# conversation -> {title, created, messages:[{role, text, ts}]}
# ----------------------------------------------------------------------------

def _aware(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _to_ts(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        try:
            return _aware(datetime.fromtimestamp(value, tz=timezone.utc))
        except Exception:
            return None
    if isinstance(value, str):
        for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ",
                    "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z"):
            try:
                return _aware(datetime.strptime(value, fmt))
            except Exception:
                continue
        try:
            return _aware(datetime.fromisoformat(value.replace("Z", "+00:00")))
        except Exception:
            return None
    return None


def _claude_message_text(msg):
    if isinstance(msg.get("text"), str) and msg["text"].strip():
        return msg["text"]
    parts = []
    for block in msg.get("content", []) or []:
        if isinstance(block, dict):
            if isinstance(block.get("text"), str):
                parts.append(block["text"])
        elif isinstance(block, str):
            parts.append(block)
    return "\n".join(parts)


def normalize_claude(data):
    convos = []
    for c in data:
        msgs = []
        for m in c.get("chat_messages", []) or []:
            sender = m.get("sender")
            role = "human" if sender == "human" else "assistant" if sender == "assistant" else None
            if not role:
                continue
            text = _claude_message_text(m)
            if not text.strip():
                continue
            msgs.append({"role": role, "text": text, "ts": _to_ts(m.get("created_at"))})
        if msgs:
            convos.append({
                "title": c.get("name") or "",
                "created": _to_ts(c.get("created_at")),
                "messages": msgs,
            })
    return convos


def _chatgpt_message_text(message):
    if not message:
        return ""
    content = message.get("content") or {}
    parts = content.get("parts")
    out = []
    if isinstance(parts, list):
        for p in parts:
            if isinstance(p, str):
                out.append(p)
            elif isinstance(p, dict):
                if isinstance(p.get("text"), str):
                    out.append(p["text"])
    elif isinstance(content.get("text"), str):
        out.append(content["text"])
    return "\n".join(out)


def normalize_chatgpt(data):
    convos = []
    for c in data:
        mapping = c.get("mapping") or {}
        nodes = []
        for _nid, node in mapping.items():
            msg = node.get("message") if isinstance(node, dict) else None
            if not msg:
                continue
            author = (msg.get("author") or {}).get("role")
            role = "human" if author == "user" else "assistant" if author == "assistant" else None
            if not role:
                continue
            text = _chatgpt_message_text(msg)
            if not text.strip():
                continue
            nodes.append({"role": role, "text": text, "ts": _to_ts(msg.get("create_time"))})
        nodes.sort(key=lambda n: (n["ts"] is None, n["ts"] or datetime.min.replace(tzinfo=timezone.utc)))
        if nodes:
            convos.append({
                "title": c.get("title") or "",
                "created": _to_ts(c.get("create_time")),
                "messages": nodes,
            })
    return convos


# ----------------------------------------------------------------------------
# Memory / profile extraction  (the high-signal layer)
# ----------------------------------------------------------------------------

def extract_user_name(profile_files):
    """Pull a display name from users.json / user.json if present."""
    for path in profile_files:
        try:
            data = _load(path)
        except Exception:
            continue
        records = data if isinstance(data, list) else [data]
        for rec in records:
            if not isinstance(rec, dict):
                continue
            for key in ("full_name", "name", "fullName", "displayName"):
                if isinstance(rec.get(key), str) and rec[key].strip():
                    return rec[key].strip()
    return None


def _stringify_memory(value, depth=0):
    """Flatten a memory value (str / list / dict) into readable markdown text."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(s for s in (_stringify_memory(v, depth + 1) for v in value) if s)
    if isinstance(value, dict):
        chunks = []
        for k, v in value.items():
            text = _stringify_memory(v, depth + 1)
            if not text:
                continue
            if depth == 0 and len(value) > 1:
                chunks.append(f"### {k}\n{text}")
            else:
                chunks.append(text)
        return "\n\n".join(chunks)
    return ""


# Keys most likely to hold real memory text across Claude / ChatGPT exports.
MEMORY_KEYS = (
    "conversations_memory", "project_memories", "memory", "memories",
    "custom_instructions", "about_user_message", "about_model_message",
    "user_profile", "model_set_context", "notes", "content", "text",
)


def extract_memory(memory_files, profile_files):
    """Return (markdown_text, sources_list, word_count).

    Handles the Claude shape:
      [{"conversations_memory": "...", "project_memories": {id: "..."}, ...}]
    and best-effort for ChatGPT custom-instructions / memory shapes. Falls back to
    dumping any long string values it finds so a non-standard export still yields text.
    """
    blocks = []
    sources = []

    def harvest(data, label):
        records = data if isinstance(data, list) else [data]
        found_here = []
        for rec in records:
            if isinstance(rec, str):
                if len(rec) > 40:
                    found_here.append(rec.strip())
                continue
            if not isinstance(rec, dict):
                continue
            hit = False
            for key in MEMORY_KEYS:
                if key in rec and rec[key]:
                    text = _stringify_memory(rec[key])
                    if text and len(text) > 20:
                        found_here.append(f"## {key}\n\n{text}")
                        hit = True
            if not hit:
                for k, v in rec.items():
                    if isinstance(v, str) and len(v) > 200:
                        found_here.append(f"## {k}\n\n{v.strip()}")
        if found_here:
            sources.append(label)
            blocks.append(f"# Source: {label}\n\n" + "\n\n".join(found_here))

    for path in memory_files:
        try:
            harvest(_load(path), os.path.basename(path))
        except Exception:
            continue

    # Custom instructions sometimes live in user.json/profile rather than a memory file.
    for path in profile_files:
        try:
            data = _load(path)
        except Exception:
            continue
        records = data if isinstance(data, list) else [data]
        for rec in records:
            if not isinstance(rec, dict):
                continue
            for key in ("custom_instructions", "about_user_message",
                        "about_model_message", "model_set_context"):
                if rec.get(key):
                    text = _stringify_memory(rec[key])
                    if text and len(text) > 20:
                        sources.append(os.path.basename(path))
                        blocks.append(f"# Source: {os.path.basename(path)} ({key})\n\n{text}")

    md = "\n\n---\n\n".join(blocks)
    words = len(WORD_RE.findall(md)) if md else 0
    seen, uniq_sources = set(), []
    for s in sources:
        if s not in seen:
            seen.add(s)
            uniq_sources.append(s)
    return md, uniq_sources, words


# ----------------------------------------------------------------------------
# Conversation analysis
# ----------------------------------------------------------------------------

CONTEXT_SIGNALS = [
    "for context", "as a reminder", "to remind you", "you are", "you're a",
    "act as", "i am a", "i'm a", "my name is", "here's my", "here is my",
    "background:", "context:", "as i mentioned", "like i said",
    "to recap", "remember that", "my company", "my business", "my client",
    "as you know", "reminder:", "just to reiterate", "recall that",
]


def normalize_opener(text, n_words=12):
    t = text.lower().strip()
    t = PUNCT_RE.sub(" ", t)
    t = WS_RE.sub(" ", t).strip()
    return " ".join(t.split()[:n_words])


def word_count(text):
    return len(WORD_RE.findall(text))


def analyze(convos, source_label):
    user_msgs = []
    total_user_words = 0
    context_signal_hits = 0
    opener_keys = Counter()
    opener_samples = {}
    lengths = []

    for ci, conv in enumerate(convos):
        first_user_seen = False
        for m in conv["messages"]:
            if m["role"] != "human":
                continue
            text = m["text"]
            is_opener = not first_user_seen
            first_user_seen = True
            wc = word_count(text)
            total_user_words += wc
            lengths.append(wc)
            user_msgs.append((text, ci, is_opener))
            low = text.lower()
            if any(sig in low for sig in CONTEXT_SIGNALS):
                context_signal_hits += 1
            if is_opener:
                key = normalize_opener(text)
                if key:
                    opener_keys[key] += 1
                    opener_samples.setdefault(key, text[:300])

    lengths.sort()

    def pct(p):
        if not lengths:
            return 0
        idx = min(len(lengths) - 1, int(p / 100 * len(lengths)))
        return lengths[idx]

    repeated = [
        {"count": cnt, "normalized": key, "example": opener_samples.get(key, "")}
        for key, cnt in opener_keys.most_common(40) if cnt >= 2
    ]

    longest = sorted(user_msgs, key=lambda x: len(x[0]), reverse=True)[:20]
    longest_dumps = [
        {"chars": len(t), "words": word_count(t), "opener": op,
         "excerpt": (t[:600] + ("..." if len(t) > 600 else ""))}
        for (t, _ci, op) in longest
    ]

    return {
        "source": source_label,
        "conversations": len(convos),
        "user_messages": len(user_msgs),
        "total_user_words": total_user_words,
        "context_signal_messages": context_signal_hits,
        "msg_word_length": {
            "p50": pct(50), "p90": pct(90), "p99": pct(99),
            "max": lengths[-1] if lengths else 0,
        },
        "repeated_openers": repeated,
        "longest_context_dumps": longest_dumps,
        "_user_msgs": user_msgs,
    }


def merge_stats(stats_list):
    return {
        "sources": [s["source"] for s in stats_list],
        "conversations": sum(s["conversations"] for s in stats_list),
        "user_messages": sum(s["user_messages"] for s in stats_list),
        "total_user_words": sum(s["total_user_words"] for s in stats_list),
        "context_signal_messages": sum(s["context_signal_messages"] for s in stats_list),
        "per_source": [{k: v for k, v in s.items() if k != "_user_msgs"} for s in stats_list],
    }


def date_range(convos):
    dates = [c["created"] for c in convos if c["created"]]
    if not dates:
        return {"first": None, "last": None, "span_days": None}
    first, last = min(dates), max(dates)
    return {"first": first.date().isoformat(), "last": last.date().isoformat(),
            "span_days": (last - first).days}


# ----------------------------------------------------------------------------
# Data-richness verdict + lightweight time-cost estimate
# ----------------------------------------------------------------------------

def assess_richness(merged, memory_words):
    """Tell the model how much to trust conversations vs. lean on memory.

    Thin conversation data is the common case (recent or sparse exporters). When
    conversations are thin but memory is rich, the model should build the portrait
    primarily from memory.md and say so honestly in the report.
    """
    um = merged["user_messages"]
    words = merged["total_user_words"]
    convo_level = "rich" if (um >= 200 or words >= 8000) else \
                  "moderate" if (um >= 50 or words >= 1500) else "thin"
    memory_level = "rich" if memory_words >= 1500 else \
                   "moderate" if memory_words >= 300 else "thin"

    if convo_level == "thin" and memory_level in ("rich", "moderate"):
        guidance = ("Conversation export is THIN — build the portrait primarily from "
                    "memory.md, and say so in the report. Use conversation samples only "
                    "for voice texture, not for breadth.")
    elif convo_level == "thin" and memory_level == "thin":
        guidance = ("Both conversation and memory data are thin. Build what you can, mark "
                    "gaps explicitly, and leave fill-in prompts. Do not fabricate a portrait.")
    elif memory_level in ("rich", "moderate"):
        guidance = ("Good signal on both sides. Cross-check the conversation patterns "
                    "against memory.md; prefer memory for stable facts (role, goals, "
                    "tools) and conversations for voice and recurring tasks.")
    else:
        guidance = ("Conversations carry the signal; memory is thin. Read samples.md "
                    "closely for voice, topics, and recurring work.")

    return {"conversation_data": convo_level, "memory_data": memory_level,
            "guidance": guidance}


def estimate_time_cost(merged):
    """A deliberately rough, clearly-caveated 'blank-slate tax' estimate.

    NOT a precise measurement — a directional figure for the report. Counts the
    cheapest-to-defend overhead: messages spent re-establishing context. Reported as a
    range with the assumption stated, so it never looks like false precision.
    """
    resets = merged["context_signal_messages"]
    return {
        "context_reset_messages": resets,
        "estimated_overhead_minutes_low": resets * 1,
        "estimated_overhead_minutes_high": resets * 2,
        "assumption": ("Rough: ~1-2 min of overhead per context-re-establishment message "
                       "(re-typing/re-pasting who you are and what you're doing). "
                       "Directional only — present as a range, not a hard number. If "
                       "resets is 0, the heuristic under-counts; lean on words-typed and "
                       "repeated-openers instead."),
    }


# ----------------------------------------------------------------------------
# Sampling for qualitative reading
# ----------------------------------------------------------------------------

def write_samples(all_user_msgs, out_path, max_samples=300, per_msg_chars=600):
    if not all_user_msgs:
        with open(out_path, "w") as f:
            f.write("# User message samples\n\n(No user messages found — this is a "
                    "memory-only / thin-conversation export. Build the portrait from "
                    "memory.md.)\n")
        return 0

    by_len = sorted(all_user_msgs, key=lambda x: len(x[0]), reverse=True)
    top = by_len[: max_samples // 2]
    rest = by_len[max_samples // 2:]
    stride = max(1, len(rest) // max(1, (max_samples - len(top))))
    spread = rest[::stride][: max_samples - len(top)]
    chosen = top + spread

    with open(out_path, "w") as f:
        f.write("# User message samples\n\n")
        f.write("A representative spread of the user's *own* messages (assistant\n")
        f.write("replies omitted). Use these to read voice, recurring topics, the\n")
        f.write("kinds of tasks they bring to AI, and automation opportunities.\n\n")
        for i, (text, _ci, _op) in enumerate(chosen, 1):
            snippet = text[:per_msg_chars].replace("\r", " ")
            f.write(f"## Sample {i}\n{snippet}\n\n")
    return len(chosen)


def write_memory(memory_md, sources, out_path, cap_chars=60000):
    if not memory_md:
        with open(out_path, "w") as f:
            f.write("# Saved memory / custom instructions\n\n"
                    "(No memory files found. If the user is on Claude, ask them to also "
                    "export memories.json and users.json; on ChatGPT, their memory / "
                    "custom-instructions file. This is usually the richest signal.)\n")
        return
    body = memory_md[:cap_chars]
    truncated = len(memory_md) > cap_chars
    with open(out_path, "w") as f:
        f.write("# Saved memory / custom instructions\n\n")
        f.write("This is the user's own saved memory and/or custom instructions, pulled\n")
        f.write("straight from their export. It is the HIGHEST-SIGNAL source for the\n")
        f.write("portrait — who they are, their work, voice, tools, and goals — and it\n")
        f.write("is especially important when the conversation export is thin.\n\n")
        f.write(f"Sources: {', '.join(sources)}\n\n---\n\n")
        f.write(body)
        if truncated:
            f.write("\n\n[...truncated for length...]")


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Parse Claude/ChatGPT exports into a digest.")
    ap.add_argument("paths", nargs="*", help="Files or folders to read.")
    ap.add_argument("--scan", help="Directory to scan for export files.")
    ap.add_argument("--out", required=True, help="Output directory for digest.")
    ap.add_argument("--max-samples", type=int, default=300)
    args = ap.parse_args()

    buckets = find_input_files(args.paths, args.scan)
    if not any(buckets[k] for k in ("conversations", "memory", "profile")):
        print("No usable export files found. Point me at a Claude or ChatGPT export "
              "folder (conversations.json and/or memories.json / users.json).",
              file=sys.stderr)
        sys.exit(2)

    os.makedirs(args.out, exist_ok=True)

    # --- conversations ---
    all_convos = []
    stats_list = []
    file_reports = []
    for path in buckets["conversations"]:
        try:
            data = _load(path)
        except Exception as e:
            file_reports.append({"file": path, "error": str(e)})
            continue
        fmt = detect_format(data)
        if fmt == "claude":
            convos = normalize_claude(data)
        elif fmt == "chatgpt":
            convos = normalize_chatgpt(data)
        else:
            file_reports.append({"file": path, "format": "unknown", "skipped": True})
            continue
        file_reports.append({"file": path, "format": fmt, "conversations": len(convos)})
        all_convos.extend(convos)
        stats_list.append(analyze(convos, source_label=fmt))

    if stats_list:
        merged = merge_stats(stats_list)
    else:
        merged = {"sources": [], "conversations": 0, "user_messages": 0,
                  "total_user_words": 0, "context_signal_messages": 0, "per_source": []}
    merged["date_range"] = date_range(all_convos)

    # --- memory + profile (high-signal) ---
    user_name = extract_user_name(buckets["profile"])
    memory_md, memory_sources, memory_words = extract_memory(buckets["memory"], buckets["profile"])
    merged["user_name"] = user_name
    merged["memory_sources"] = memory_sources
    merged["memory_words"] = memory_words

    # --- verdicts ---
    merged["data_richness"] = assess_richness(merged, memory_words)
    merged["time_cost_estimate"] = estimate_time_cost(merged)
    merged["files"] = file_reports
    merged["inputs_found"] = {k: [os.path.basename(p) for p in v] for k, v in buckets.items() if v}

    # --- write outputs ---
    all_user_msgs = []
    for s in stats_list:
        all_user_msgs.extend(s.pop("_user_msgs", []))

    samples_path = os.path.join(args.out, "samples.md")
    n_samples = write_samples(all_user_msgs, samples_path, max_samples=args.max_samples)
    merged["samples_written"] = n_samples
    merged["samples_file"] = samples_path

    memory_path = os.path.join(args.out, "memory.md")
    write_memory(memory_md, memory_sources, memory_path)
    merged["memory_file"] = memory_path

    digest_path = os.path.join(args.out, "digest.json")
    with open(digest_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, default=str)

    # --- human-readable summary ---
    name = f" for {user_name}" if user_name else ""
    print(f"Parsed export{name}.")
    if file_reports:
        print(f"Conversation files: {len(buckets['conversations'])}  |  "
              f"Formats: {', '.join(r.get('format','?') for r in file_reports)}")
    print(f"Conversations: {merged['conversations']}  |  "
          f"User messages: {merged['user_messages']}  |  "
          f"Words typed by user: {merged['total_user_words']:,}")
    print(f"Memory captured: {merged['memory_words']:,} words "
          f"from {', '.join(memory_sources) if memory_sources else 'none'}")
    print(f"Data richness: conversations={merged['data_richness']['conversation_data']}, "
          f"memory={merged['data_richness']['memory_data']}")
    print(f"Context-re-establishment messages: {merged['context_signal_messages']}")
    dr = merged["date_range"]
    print(f"Date range: {dr['first']} -> {dr['last']} ({dr['span_days']} days)")
    print(f"Wrote: {digest_path}")
    print(f"Wrote: {samples_path} ({n_samples} samples)")
    print(f"Wrote: {memory_path}")


if __name__ == "__main__":
    main()
