# Audit Report Contract

Adapt the amount of detail to the project, but preserve these sections and fields.

## 1. Scope

Report:

- project root
- mode
- model or Claude Code change being investigated, if the user named one
- instruction sources reviewed
- the active output style, if any, and whether it is project-level or user-level
- whether a project `AGENTS.md` exists and whether it agrees with `CLAUDE.md`
- hooks or permissions inspected as evidence
- project evidence sampled
- any targeted version-control history inspected for provenance
- external, user-level, MCP, and Skill-routing exclusions
- any unreadable or unauthorized sources

Do not identify host metadata, account information, hidden system context, or unrelated
runtime details as an audit source or exclusion.

State whether version-control evidence is available. When it is unavailable, call
`CLAUDE.md` project-level. Do not call it tracked, committed, checked in, shared, or
team-wide.

## 2. Instruction map

Summarize each source:

| Source | Loads when | Approximate size | Role | Notes |
| --- | --- | ---: | --- | --- |

Mention broken imports, external imports, overlapping scopes, and nested files that load
only for part of the project.

### Context load

Report how much instruction text loads in every session versus per path scope, in lines
per group. Name any content that repeats across sources loading together and any content
loading far more broadly than the work it governs, and point each observation at its
finding ID. Present this as exposure information, not a reduction target, and do not
attach a size number the audit should aim for.

## 3. Audit summary

Name the two or three highest-priority findings and explain the behavior or risk each one
affects. Rank attention using activation breadth, evidenced task frequency, and
consequence. Do not use ease of patching, removal percentages, or decision counts as
success measures.

## 4. Protected instructions

List the high-risk rules that should remain untouched during this audit and explain the
failure each one prevents. Avoid reproducing private values or unnecessary file content.

If no protected instruction blocks were identified, write exactly:

> No protected instruction blocks identified.

Add nothing else to this section.

## 5. Findings

Use stable IDs. Render each finding as a compact block, not a wide table. The report is
read in a terminal, and a many-column row wraps into unreadable text:

### A01. Short name of the instruction block

- **Source and scope:** file, location, and when it loads
- **Finding:** the finding type and one sentence stating the problem
- **Evidence and provenance:** what supports the finding, the failure the block was meant
  to prevent, and its provenance label
- **Decision:** one of the five labels, then Confidence, Risk, and Operational priority
- **Proposed change or test:** the concrete action or test definition

Requirements:

- Keep source locations precise enough for review.
- Support claims about tracked or shared files with version-control evidence. Otherwise
  describe only the file's location and Claude Code scope.
- State what failure the block was meant to prevent. Label its provenance **Observed**,
  **Inferred**, or **Unknown**, and name any targeted history inspected.
- Paraphrase sensitive instructions.
- Name both sides of a conflict.
- For each conflict, assign operational priority from activation breadth, evidenced task
  frequency, and consequence. Mark unsupported frequency **Unknown** rather than guessing.
- For **Overprescribed**, show the proposed outcome description and name every constraint
  or failure condition it preserves.
- For **Move**, name the destination.
- For **Test**, define the task and restoration condition.
- For **Retire**, show the structural evidence that makes testing unnecessary.
- Make each proposed action match its Decision label. Do not pair **Retire** with an
  alternative to create or rewrite the same rule.
- A **Retire** finding proposes removal only. If creating, restoring, or rewriting the
  instruction remains a plausible outcome, use **Rewrite** or **Keep** and ask one focused
  owner question.

Omit low-value commentary on blocks that are clearly healthy unless they are protected
or help explain the system.

## 6. Proposed patch order

Group the findings:

1. Low-risk structural fixes
2. Rewrites and moves
3. Behavioral tests
4. High-risk decisions requiring owner judgment

Call out dependencies. For example, create or approve a destination before moving a
procedure out of `CLAUDE.md`.

This is implementation order, not attention priority. A high-priority conflict may still
depend on owner judgment or a behavioral test and therefore appear later in the patch
sequence.

## 7. Approval boundary

End Audit mode with:

> No files changed. Select the finding IDs you want to apply. I will patch only those
> items. Findings marked Test need a baseline task before removal.

If there are no material problems, say so. Do not manufacture recommendations to fill the
table.

Before returning, scan the report for references to system context, host metadata,
account details, or unverified claims that a file is tracked or shared. Remove or replace
them with project evidence. When version-control status is unavailable, replace
"shared," "tracked," "committed," and "checked in" with "project-level."

## Apply handoff

After approved edits, report:

- finding IDs applied
- files changed
- approved findings skipped and why
- protected instructions preserved
- validation completed
- whether the fresh-session comparison remains pending

Do not describe a static diff check as behavioral proof.
