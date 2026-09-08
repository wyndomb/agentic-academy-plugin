# Memory Audit Rubric

Use this rubric to make conservative, evidence-backed decisions about auto memory.
Audit memories as claims about the user and the project that may or may not still
hold, not as files to trim.

## Evidence labels

- **Observed:** Directly supported by the memory file, a project file, the index, a
  command result, or explicit user confirmation.
- **Inferred:** Strongly suggested by project evidence but not directly stated.
- **Unknown:** Only the user can settle it.

An inference can support a **Confirm** or **Sharpen** decision. It should not be the
sole basis for **Delete** or **Merge**.

## Memory types and how they age

- **user:** Who the user is. Meant to be stable. Age is never evidence of staleness.
  Flag only on contradiction with newer evidence.
- **feedback:** A correction or confirmed approach. Ages when it graduates into a
  standard elsewhere, or when the behavior it corrects no longer occurs. Check whether
  it stuck before judging it.
- **project:** Ongoing work, goals, constraints. Ages fastest. Any memory naming a
  phase, deadline, open question, or next step is a dated claim; check it against the
  files and the calendar.
- **reference:** Pointers to external resources. Ages when the target moves or the
  workflow it supports ends.
- **untyped:** No type in frontmatter. Assign the likely type in the finding and
  propose adding it under **Sharpen**.

## Finding types

### Stale

A project or reference memory whose claim project evidence contradicts: a named file
or folder that no longer exists, a deadline that has passed, a phase the project's
own files show is over, or a next step that was visibly taken. Quote the claim and
the evidence. When evidence is absent rather than contradictory, use **Confirm**.

### Graduated

A feedback memory whose rule now also lives in `CLAUDE.md`, a rule file, an output
style, or a foundational file. The memory did its job and is now a duplicate of a
stronger source. Confirm both say the same thing before proposing removal; a memory
that carries a nuance the standard dropped is a **Sharpen** of the standard, which
belongs in a separate audit, and a **Keep** here.

### Unactionable

A feedback or project memory with no Why line, no How-to-apply line, or wording too
vague to change behavior. The fact is real; the memory just cannot be used.

### Contradiction

Two memories, or a memory and a project file, state different rules for the same
behavior. Quote both sides. This is the most urgent finding type, because a future
session picks a winner silently.

### Duplicate

Two memories cover substantially the same fact. Shared wording is not enough; confirm
that merging loses no nuance, scope, or example.

### Misplaced

The memory is useful but lives in the wrong layer:

| Content | Likely home |
| --- | --- |
| Standard for one kind of output | Path-scoped rule in `.claude/rules/` |
| Stable, project-wide, day-one knowledge | Project `CLAUDE.md` |
| Preference that holds in every project | User-level layer |
| Working state, corrections, evolving facts | Memory, where it is |

The table is a routing guide. Do not move a memory the user has said they want to
keep in memory, and do not move anything into a file this audit is not allowed to
edit without first proposing the destination as a separate step.

### Index problem

An orphan file the index does not list, an index line pointing at a missing file, an
index line carrying content instead of a pointer, or an index approaching the
auto-load limit. Structural, low-risk, and worth fixing first.

### Broken link

A `[[wikilink]]` that matches no memory name, or a project path the memory names
that no longer exists. A dangling wikilink can be intentional, marking something
worth writing later; say so and propose nothing unless the target clearly should
exist.

### Protected

A memory that encodes a hard-won correction with a specific trigger: a name that gets
mistranscribed, a construction the user rejects on sight, a tool that must not be
used for a task. These are cheap to keep and expensive to lose. Changes need direct
evidence and explicit approval.

## The six decisions

### Keep

The memory is true, actionable, in the right layer, and not duplicated. Say so
briefly; healthy memories deserve confirmation, not silence.

### Sharpen

The fact is real but the memory cannot be used well: missing Why or How-to-apply,
vague wording, missing type, or a nuance that needs stating. Propose the new wording
and let the user correct it. Never change the underlying fact under **Sharpen**.

### Move

The memory belongs in a different layer. Name the destination. The move completes
only after the destination holds the rule.

### Merge

Two memories cover one fact. Name the survivor and show that the merged body keeps
every fact, example, and scope from both.

### Confirm

Only the user can say whether the memory is still true. Ask one focused question per
finding. On a yes, stamp a review date. On a no, the follow-up is a **Sharpen** with
the corrected fact or a **Delete** with the user's confirmation as evidence.

### Delete

Use only when the memory fails all four tests in the Guardrails, or the user confirms
the fact is no longer wanted, or an approved **Merge** or **Move** has absorbed it.
Show the structural evidence. Do not delete on age, on a hunch, or to shorten the
index.

## Risk

- **High:** Deleting or moving a protected memory, resolving a contradiction by
  choosing a winner without the user, or any change to a user-type memory.
- **Medium:** Merges, moves into a rule or `CLAUDE.md`, and sharpens that reword a
  rule the user gave verbatim.
- **Low:** Index fixes, broken-link cleanup, adding a missing type, and adding Why or
  How-to-apply lines the user then approves.

When confidence is low and risk is medium or high, prefer **Keep** or **Confirm**.

## Operational priority

Rank attention by consequence first: a contradiction that changes how drafts are
written outranks an orphaned reference. Then by breadth: a memory that shapes every
session outranks one scoped to a single client. Frequency claims need evidence from
the project files; mark them **Unknown** otherwise.
