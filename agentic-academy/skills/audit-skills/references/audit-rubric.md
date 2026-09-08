# Skill Audit Rubric

Use this rubric to make conservative, evidence-backed decisions about a Skill routing
layer. Audit Skills as a system that competes for requests, not as isolated files.

## Evidence labels

- **Observed:** Directly supported by a SKILL.md file, a project file, a command
  result, a trigger test, or explicit user confirmation.
- **Inferred:** Strongly suggested by project evidence but not directly stated.
- **Unknown:** Depends on owner judgment or a fresh-session trigger test.

An inference can support a question or a **Test** decision. It should not be the sole
basis for archiving or merging a Skill.

Activation-log evidence is asymmetric. A recorded activation is **Observed** evidence
that a Skill is live. Absence of one is **Unknown**, not **Inferred** disuse, because
the log does not capture description-match activation. Treat a blank activation record
as a reason to ask the owner, never as a finding on its own.

## Provenance

Provenance is evidence about why a Skill was built and what repeated work or failure
it was meant to capture. Establish it from the SKILL.md itself and current project
files first. Use targeted version-control history only for a Skill whose purpose
remains unclear and only when that history is available.

Label provenance **Observed**, **Inferred**, or **Unknown**. Do not infer the original
purpose from the Skill's name alone. Age is not evidence that a Skill is stale, and
absence of recent output is not evidence that the Skill is unwanted.

## Finding types

### Overlap

Two or more descriptions plausibly claim the same request. Confirm by writing one
realistic prompt that both descriptions cover and explaining which Skill ought to win.
Shared vocabulary alone is not overlap; two Skills that mention "LinkedIn" may own
cleanly separate jobs. The test is whether a reasonable request has two claimants.

Distinguish two shapes:

- **Divided ownership:** the Skills split one job that belongs together. Candidate for
  **Merge**.
- **Boundary blur:** the Skills own different jobs but their descriptions fail to draw
  the line. Candidate for **Clarify** on one or both sides.

### Overbroad description

The description claims requests the body cannot serve well, or triggers on request
shapes the owner never intended. Evidence is a realistic prompt that would activate
the Skill and then be poorly served by it.

### Overnarrow description

The Skill does useful work but its description names only one narrow phrasing, so
natural variants of the request miss it. Evidence is a realistic prompt the Skill
should own that the description does not cover. Undertriggering is invisible in daily
use, which makes this finding easy to miss and worth actively hunting.

### Missing exclusion boundary

The description says what the Skill does but not what it does not do, and a nearby
Skill, command, or default behavior needs that line. Only a finding when a concrete
misroute is plausible; do not demand exclusion language from every Skill.

### Vague description

The description cannot route because it names a topic instead of a task, or relies on
language like "helps with content" that fits almost any request in the project.

### Description-body mismatch

The description promises one job and the body performs another, or the body has grown
capabilities the description never mentions. The routing contract and the procedure
must tell the same story.

### Stale

The body names a tool, path, command, model, format, or workflow that project
evidence shows has changed or disappeared, or the Skill serves a project or campaign
that evidence shows has ended.

### Broken reference

The Skill points to a bundled file, script, or project path that does not exist, or a
bundled script fails on invocation. Distinguish a missing file from one that needs
authorization.

### Oversized

The Skill front-loads content that belongs in bundled references, so every activation
pays for context that most runs never use. A long SKILL.md is not automatically a
finding; the question is whether the body mixes always-needed workflow with
rarely-needed detail that progressive disclosure would keep out of context.

### Wrong activation mode

The Skill's cost or risk does not match how it activates:

- an expensive, destructive, or externally visible workflow activates automatically
  when it should wait for an explicit invocation
- a routine Skill is marked manual-only and the owner keeps forgetting it exists

### Duplicate procedure

The same procedure lives in this Skill and in `CLAUDE.md`, a rule file, a hook, or
another Skill. Decide which home is authoritative before proposing removal from the
other, and confirm the copies actually agree; silently diverged duplicates are the
more urgent version of this finding.

### Unverified model workaround

The Skill exists mainly to script behavior an older model could not do reliably, and
files cannot show whether the current model still needs the scripted steps.
Recommend **Test**.

### Protected

The Skill controls a high-cost failure. Protected categories include:

- safety and privacy behavior
- approval before sending, publishing, deleting, purchasing, or changing external data
- source-of-truth precedence and required routes
- required output formats
- checks and standards the project verifies

Protected does not mean immutable. It means changes need direct evidence, explicit
approval, and a trigger test proportional to the risk. A Skill that weakens an
approval boundary or leaks sensitive data is a risk finding, not a protected one.

## The six decisions

### Keep

Use when the Skill:

- owns a task that project evidence shows is real
- has a description that routes that task and excludes its neighbors well enough
- does not materially collide with another Skill

### Clarify

Use when the Skill is worth having but its description misroutes: overbroad,
overnarrow, vague, missing an exclusion boundary, or mismatched with the body. The
proposal names the new positive boundary, the new negative boundary, and the
neighboring Skill each boundary protects against. Clarify changes the routing
contract, not the procedure.

### Manual only

Use when the Skill should exist but should never activate on description matching
alone: it is expensive, slow, destructive, externally visible, or so specialized that
automatic activation causes more misroutes than it saves. The proposal names the
activation-mode setting to add and the invocation the owner will use.

### Merge

Use when two Skills hold divided ownership of one job. The proposal names the
surviving Skill, what it absorbs, and what happens to both original trigger
boundaries. Merge only on **Observed** overlap. Do not merge Skills that share a
topic but produce different outputs for different destinations.

### Test

Use when the right decision depends on how the current model actually routes or
performs, which files cannot prove: a suspected collision that lexical evidence
cannot confirm, a workaround the current model may no longer need, or a Skill whose
value the owner doubts. Define the positive, negative, and competing prompts, and
the observed result that would settle the decision.

### Archive

Use only when there is strong structural evidence:

- the task the Skill owns no longer exists in the project
- the Skill's job has been absorbed by an approved merge
- the Skill is explicitly superseded by a named replacement
- the user confirms the work is no longer wanted

Archive moves the Skill to a recoverable location. Do not use **Archive** merely
because a Skill is old, rarely used, or unfashionable. Rare, high-consequence Skills
earn their place through what they prevent.

An empty or stale activation record never satisfies this bar. It shows the Skill was
not explicitly invoked, which says nothing about whether it activated by description
match or whether the owner still wants it.

## Operational priority

Operational priority determines which findings deserve attention first. It is
separate from risk and from patch order.

For routing findings, weigh:

1. **Collision breadth:** how many realistic request shapes hit the ambiguity.
2. **Task frequency:** how often project evidence shows the affected work recurs.
3. **Consequence:** the cost of the wrong Skill winning, from mild inefficiency to a
   wrong-destination publish.

Use **High**, **Medium**, **Low**, or **Unknown**. When frequency cannot be supported
by project evidence, say **Unknown** for that factor and prioritize conservatively on
breadth and consequence.

## Risk

- **High:** Changes touching approval boundaries, publishing or sending flows,
  deletion, source-of-truth routes, or any Skill whose failure is externally visible.
- **Medium:** Routing changes to Skills used by recurring work, merges, and
  activation-mode changes.
- **Low:** Confirmed broken references, dead paths, description typos, and boundary
  wording with a narrow effect.

When confidence is low and risk is medium or high, prefer **Keep** or **Test**.

## Collision precedence

When two Skills claim a request and both are worth keeping, do not invent a winner.
Resolve using, in order:

1. an ownership boundary the project already documents
2. the more specific applicable description
3. the Skill whose output the project's evidence shows this request historically
   produced
4. user confirmation

If none resolves it, mark the winner **Unknown** and ask one focused question.
