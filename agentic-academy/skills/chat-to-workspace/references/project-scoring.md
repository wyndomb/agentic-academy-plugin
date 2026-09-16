# Recommending the #1 project (leverage scoring)

The person needs **one** project to build their system on — not a menu. This is the same
three-stage framework the cohort uses in pre-work, applied here using evidence from their
chat history or their interview answers instead of a blank brainstorm. Read this in Phase 3.

## Stage 1 — Generate candidates from the evidence

List everything the person *already does repeatedly*. Don't filter yet. Where the
candidates come from depends on the source:

From a chat export (`digest/samples.md` and the repeated-opener clusters):
- Repeated openers (high count = recurring work).
- The longest context dumps (work important enough to re-explain at length).
- Clusters of conversations on the same topic (a workflow split across many chats).

From an interview:
- The top 3-4 recurring tasks they named when walking through a normal week.
- The tasks with the highest confirmed time-per-task x frequency.
- Anything they said they already have a template, checklist, or standard for.

Either way: anything they clearly do every week.

Aim for 5-8 raw candidates.

## Stage 2 — Triage with five criteria

Keep only candidates that pass MOST of these. Drop the rest.

1. **Volume** — they spend real time on it (recurring in the history, not a one-off).
2. **File-shaped output** — it produces a draft, report, brief, deliverable, or similar.
3. **Examples exist** — they have (or can gather) ~20 examples of past work to draw on.
   (In an interview, ask this directly; don't assume.)
4. **Describable quality** — they can say what "good" and "bad" look like in plain words.
5. **Real payoff** — systematizing it removes pain or frees them for better work.

You should be left with 2-4 candidates.

## Stage 3 — Score by leverage (1-5 each, highest total wins)

Score each remaining candidate on three axes:

- **Time leverage** — how much time it saves, or how much faster it lets them work at the
  same quality.
- **Quality leverage** — how much it raises output quality in the same time, or
  strengthens inputs that feed everything else.
- **Strategic leverage** — how much it unlocks things they aren't doing now, or expands
  the scope of what they can take on.

Pick the highest total. On ties, prefer the one with the richest existing example base
(it'll produce better output sooner) and the clearest quality definition.

## Output: `project/project-brief.md`

Write the recommendation as:

```markdown
# Your #1 Project: [name]

## What it is
[one paragraph — the recurring work this systematizes]

## Why this one
[the scores, briefly, and what the evidence (chat history or interview) shows about how
often / how painfully they do this today]

| Candidate | Time | Quality | Strategic | Total |
|-----------|------|---------|-----------|-------|
| [winner]  | x | x | x | xx |
| [runner-up] | x | x | x | xx |

## The workflow to systematize
[name the single input-to-output workflow inside this project — e.g. "voice memo ->
researched draft -> voice-checked edit"]

## Your first step
[one concrete action: the 5-10 files to add to material/, and the first task to run]
```

Keep it decisive. The person can change projects later, but they should leave with a clear
single recommendation and a reason they believe it.
