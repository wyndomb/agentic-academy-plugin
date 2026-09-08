# Memory Audit Report Contract

Adapt the amount of detail to the project, but preserve these sections and fields.
Present in chat as markdown. Write no file unless the user asks.

## 1. Memory Report

Always present this first, in both Report and Audit modes.

```
# Memory Report: <project name>

Location: ~/.claude/projects/<name>/memory/
Index: MEMORY.md, <N> lines (roughly the first 200 load automatically)
Files: <N> memories: <n> user, <n> feedback, <n> project, <n> reference, <n> untyped
```

Then one table per type, one row per file:

| Memory | What it says | Age |
| --- | --- | --- |

"What it says" is a one-line gist in plain words, not the raw description field. Keep
gists honest and specific; the value of the report is that the user can scan their
whole memory in thirty seconds.

Close the report with the user-level layer, summarized in a few lines, labeled as
applying to every project and out of scope for edits.

In Report mode, stop here.

## 2. Scope

Report:

- project root and resolved memory folder
- mode
- what the inventory script checked and what it could not
- project files sampled to test project-type memories
- the user-level layer read, marked read-only
- anything unreadable

Do not identify host metadata, account information, hidden system context, or
unrelated runtime details as an audit source.

## 3. Audit summary

Name the two or three highest-priority findings and the behavior each one affects.
Contradictions and stale project memories usually lead. Do not use file counts,
deletion counts, or index length as success measures.

## 4. Protected memories

List the memories that should remain untouched and the failure each one prevents.
If none, write exactly:

> No protected memories identified.

## 5. Findings

Use stable IDs. Render each as a compact block, not a wide table:

### M01. Short name of the memory or pair

- **Memory and type:** file name, type, and age
- **Finding:** the finding type and one sentence stating the problem
- **Evidence:** the quoted line, the project evidence, and its label (Observed,
  Inferred, Unknown)
- **Decision:** one of the six labels, then Confidence and Risk
- **Proposed change or question:** the concrete edit, the destination, the merged
  wording, or the single question the user must answer

Requirements:

- For **Stale**, quote the claim and name the file, date, or folder that contradicts it.
- For **Graduated**, name the file that now holds the same rule and confirm they agree.
- For **Contradiction**, quote both sides and do not pick a winner.
- For **Sharpen**, show the proposed wording.
- For **Move**, name the destination and whether it exists.
- For **Merge**, name the survivor and show the merged body keeps every fact.
- For **Confirm**, ask exactly one question.
- For **Delete**, show that the memory fails all four retention tests or cite the
  user's confirmation.
- Make each proposed action match its Decision label.

Healthy memories get a one-line **Keep** only when confirming them helps the user
trust the audit; otherwise their row in the Memory Report is enough.

## 6. Proposed patch order

1. Index fixes and broken links
2. Sharpens
3. Confirms that need the user's answer
4. Moves and merges, which need destinations built first
5. Deletes, which need approval and, where relevant, a completed move or merge

## 7. Approval boundary

End Audit mode with:

> No files changed. Select the finding IDs you want to apply, or answer the Confirm
> questions first. I will patch only those items and keep MEMORY.md in sync.

If there are no material problems, say so. Do not manufacture findings.

## Apply handoff

After approved edits, report:

- finding IDs applied
- files changed, including `MEMORY.md`
- approved findings skipped and why
- protected memories preserved
- Confirm answers recorded and review dates stamped
