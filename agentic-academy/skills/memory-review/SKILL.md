---
name: memory-review
description: Read and audit Claude Code's auto memory for this project (and the user-level layer) without needing the /memory terminal command. Use this skill whenever the user asks to see, show, review, audit, or clean up their memory; asks "what do you remember about me?" or "what have you learned about this project?"; asks why something wasn't remembered or why a saved correction didn't stick; or mentions that a memory is wrong, stale, duplicated, or contradicts something. Also use it when the user asks where their memory lives or wants to check what Claude knows before a fresh-session test. Finds stale, vague, duplicated, orphaned, misplaced, and contradicted memories and proposes one decision per finding. Does not audit CLAUDE.md, rules, or Skills, and does not edit or delete without approval.
---

# Memory Review

Show the user what lives in their auto memory, then find the memories that have stopped
earning their place. Memory is markdown on disk, so this works anywhere Claude Code can
read files.

Memory drifts differently from `CLAUDE.md`. Nobody edits it deliberately. It fills up
one correction at a time, each one true on the day it was saved, and nothing revisits
them. The goal is a memory the user can trust, not a smaller one.

## Modes

- **Report:** Read everything and present the Memory Report. No findings, no changes.
  Use for "show my memory" or "what do you remember about me?"
- **Audit:** The report, then the full analysis and a proposal with one decision per
  finding. This is the default for "review," "audit," "clean up," "is my memory
  healthy," or any complaint that a memory is wrong or didn't stick.
- **Apply:** Patch only the finding IDs the user explicitly approves.

When the request is ambiguous, run the Audit. The Report on its own answers a question
the user rarely asks twice; the Audit is where the value is.

## Audit workflow

### 1. Locate the memory

Run the bundled inventory from the target project:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/inventory_memory.py" "${CLAUDE_PROJECT_DIR}" --format markdown
```

The script locates the project memory folder under `~/.claude/projects/`, parses every
memory file and the `MEMORY.md` index, and reports the checks that do not need
judgment: file types and ages, missing Why and How-to-apply lines, orphans and broken
index entries, index length against the auto-load limit, broken wikilinks, project
paths a memory names that no longer exist, dates a memory mentions that have passed,
lexical overlap between memories, and lexical overlap between a memory and the
project's `CLAUDE.md`, rules, and foundational files.

Overlap and staleness hints are signals, not verdicts. Confirm or dismiss every hint by
reading the files.

If the script finds no memory folder, say plainly that no auto memory exists for this
project yet. That is a normal state for a young project, not an error. Explain how
memories get created and stop.

### 2. Read every memory in full

Read `MEMORY.md` first, then every memory file. The script sees structure; only reading
sees meaning. Also read the user-level layer, `~/.claude/CLAUDE.md` and `~/.claude/rules/`
when present, so the user can see which layer each piece of knowledge lives in. Report
the user-level layer separately and never propose edits to it inside a project audit.

### 3. Check each memory against the project

This is the step the old version of this skill skipped. For each memory, ask:

- **Is it still true?** Compare project-type memories against the current state of the
  files they describe. A memory that names a phase, deadline, open question, or next
  step is a claim about the world that may have expired. Check the referenced files,
  folders, and dates before deciding.
- **Did it stick?** For feedback-type memories, check whether the same rule now lives in
  `CLAUDE.md`, a rule file, an output style, or a foundational file. A correction that
  graduated into a standard is a duplicate in memory. A correction that never graduated
  but keeps recurring is a candidate to move.
- **Can it be acted on?** A memory needs to tell a future session what to do
  differently. A bare fact with no Why or How-to-apply line gets ignored and cannot
  generalize.
- **Does it agree with its neighbors?** Two memories, or a memory and a project file,
  that state different rules for the same behavior are the most urgent finding, because
  the loser is silently chosen every session.
- **Is it in the right layer?** A standard for one kind of output belongs in a
  path-scoped rule. Stable day-one project knowledge belongs in `CLAUDE.md`. A
  preference that holds in every project belongs in the user-level layer.

Read [audit-rubric.md](references/audit-rubric.md) before assigning decisions.

### 4. Return the audit proposal

Read [report-template.md](references/report-template.md) and follow its output contract.
Use stable finding IDs such as `M01`, `M02`, and `M03`.

Every material finding recommends exactly one decision:

- **Keep**
- **Sharpen**
- **Move**
- **Merge**
- **Confirm**
- **Delete**

Use **Confirm** when only the user can say whether a memory is still true. Do not guess
staleness from age alone, and never treat a user-type memory as stale because it is old;
those are supposed to be stable.

End the Audit mode report by asking the user to select finding IDs. Do not edit during
the same turn that first presents the audit.

## Apply approved findings

A user selection such as "apply M02 and M05" authorizes only those findings.

Before editing:

1. Re-read each affected memory file and the index.
2. Confirm that each finding still matches the current file.
3. For a **Confirm** finding, record the user's answer in the memory body and stamp a
   review date; do not delete on a **Confirm**.

Then:

- make the smallest patch that implements the approved decision
- for **Sharpen**, keep the original fact and add or fix the Why and How-to-apply
  lines; propose the wording, let the user correct it
- for **Move**, create or extend the destination first, then remove the memory only
  after the destination holds the same rule; when the destination is a rule file,
  hand off to `agentic-academy:rule-builder`
- for **Merge**, write the surviving memory so it preserves every fact from both, then
  remove the absorbed file
- for **Delete**, remove the file and its index line together
- keep `MEMORY.md` in sync with every change, one line per memory, no content
- never edit `~/.claude/CLAUDE.md`, `~/.claude/rules/`, or another project's memory
  inside this audit
- read every changed file back and summarize what changed

## Guardrails

- Deletion is proposed only when a memory fails all four of: corrected or confirmed at
  least twice, affects multiple future sessions, meaningfully changes output quality,
  and the user would be annoyed if it were forgotten. A memory that passes even one
  test stays; sharpen it if the wording is weak.
- Sensitive-looking content, such as client names and money figures, belongs in the
  report. It is the user's own file and seeing it is the point of the review. It does
  not belong in any file outside the memory folder.
- Keep the audit to this project's memory plus the user-level layer as read-only
  context. Never open another project's memory folder.
- `CLAUDE.md`, rules, and Skills are separate audits. Name a duplicate or contradiction
  with them as a finding; do not propose edits to them here.
- Close every audit by noting that this review takes a few minutes and is worth
  running after any stretch of heavy correction, not on a fixed schedule.
