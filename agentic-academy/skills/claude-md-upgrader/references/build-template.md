# Home Base Build Template

Use this in BUILD mode, when the project has no CLAUDE.md yet. Fill every section from what you learned reading the project and from the short interview. Leave no placeholders. Match the project's own language, not generic AI-speak.

## Before you write

- Decide router vs inline. If the project is large (many folders, lots of files, other reference docs), keep the home base short and route to those files. If it is small, hold the content inline. Do not pull everything inline just to look thorough.
- Confirm the archetype you detected and let it shape the examples in each section.

## CLAUDE.md skeleton to fill in

```markdown
# CLAUDE.md

## Project Overview

<One short paragraph: what this project is, in plain language, and the one
thing that makes it distinct. Written so a stranger could act on it.>

## Who The Work Serves

<The real audience or client. Specific enough to change word choice, examples,
and what counts as good. Name their level and what they care about.>

## What I'm Trying To Grow

<The goal the work serves, so Claude can weigh tradeoffs the way the owner
would. Include the one thing that matters more than speed or volume.>

## Critical Rules

<Five hard, checkable rules Claude must never break. Each one must be
catchable by looking at the output. No preferences dressed as rules.>

1.
2.
3.
4.
5.

## Decision Rules

<Three rules for when to ask vs move, and the default to pick when unsure.>

1.
2.
3.

## Key Files

<A short routing list: which file to read for which task. Only the files that
change the answer. For a small project, this can be three or four lines.>

| File | Read when... |
| --- | --- |
|  |  |
```

## Filling-in rules

- Pull every section from real evidence: the files you sampled, the naming conventions you saw, the answers from the interview. If you state a rule, it should be one the project actually follows.
- Make each critical rule checkable. "Never use em dashes" is checkable. "Write clearly" is not. If you cannot describe how to catch a violation, it does not belong in Critical Rules.
- Keep decision rules concrete: name the action that triggers a pause (publish, send, overwrite, delete) and the action safe to do without asking (small reversible edits).
- For Key Files, route rather than dump. The test is whether each line would actually send Claude to the right place for a real task.

## After writing

Tell the user:

1. The path you wrote (`CLAUDE.md` at the project root).
2. The archetype you detected, and which parts you inferred vs which came from their answers.
3. One before and after test they can run against a real project task.
4. One suggested next step: run `skill-finder` to find the skills worth building for this project, now that the home base exists.

## Before and after test format

Keep the test small and tied to the user's real work:

```markdown
Before and after test:
1. Ask Claude to do <one real task> without relying on the new home base.
2. Ask Claude to do the same task with the new home base active.
3. Compare: accuracy, rule-following, usefulness, and how much correction was needed.
```

Examples:

- Content creator: turn one messy note into a newsletter outline.
- Coach or consultant: draft a client follow-up from meeting notes.
- Entrepreneur: summarize research into a decision memo.
- Knowledge worker: turn project updates into a stakeholder-ready status report.
