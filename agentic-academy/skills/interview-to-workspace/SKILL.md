---
name: interview-to-workspace
description: >-
  Interview someone about their real work, then build them a Claude Code working folder from what
  they say, with no chat-history export required. Produces a CLAUDE.md + AGENTS.md home base,
  context files capturing who they are and how they work, an organized material/ space, a work
  portrait report, a recommended #1 project, and one runnable starter skill. Use when someone
  wants to get set up for agentic AI / Claude Code but has no export to analyze, would rather not
  hand over their chat history, or says things like "set up my Claude Code folder", "build me a
  workspace", "interview me and build my project folder", "I don't have a chat export", "what
  should I build first", or "get me ready for the cohort" without handing over files. This is the
  interview-driven sibling of chat-to-workspace: same folder output, sourced from a conversation
  instead of an export. Neither is the fallback for the other; take the person's stated preference
  at face value.
---

# Interview to Workspace

Turn a short interview about someone's real work into a working Claude Code folder they can
start building on immediately.

## Why this exists

`chat-to-workspace` (Chat X-Ray) builds a great starter workspace, but it needs an export of
the person's past AI history. That's a real barrier: plenty of people don't have one, don't
want to export, or have a history too thin to read. This skill removes the barrier. It gets
the same signal — who they are, what they repeat, what "good" looks like — by **asking**, then
builds the identical folder. Same destination, no export required.

It does two things in one pass:

1. **Understands the person** — through a short, adaptive interview about their role, their
   week, where their time goes, and what makes their work good.
2. **Builds their workspace** — a real folder with a `CLAUDE.md` + `AGENTS.md` home base,
   context files, an organized `material/` space, a work-portrait report, a recommended #1
   project, and one runnable starter skill.

The goal is to get someone from "empty folder" to "real home base an agent can work inside" in
one conversation.

## Relationship to chat-to-workspace (read this)

This skill deliberately **reuses chat-to-workspace's building blocks**: the same archetypes,
folder scaffolds, CLAUDE.md/AGENTS.md/context templates, project-scoring, and starter-skill
template all live in this skill's `assets/` and `references/`. The ONLY thing that changes is
the front end — an interview replaces the export parser — and the report, which is a work
portrait built from the interview instead of a data-driven X-Ray.

- Person **has an export** → prefer `chat-to-workspace`. Its numbers are richer.
- Person **has no export** (or prefers to talk) → this skill.

Same scope boundary as chat-to-workspace: report + folder + project + **one** starter skill.
Don't build a skill library here. If the person wants more skills afterwards, point them to
`/agentic-academy:skill-finder`.

## What it produces

A new folder (default name `<name>-workspace/`) containing:

```
<name>-workspace/
├── CLAUDE.md                      # home base for Claude Code (reads this first)
├── AGENTS.md                      # same substance, for Codex / portable agents
├── work-portrait.md               # the interview portrait: your week, time cost, opportunities
├── start-here.md                  # what this folder is + what to do next
├── context/                       # the "understand me" layer
│   ├── operator-profile.md        # who they are, what they do, their domains
│   ├── voice-and-style.md         # how they write / think (from real samples if given)
│   ├── decision-rules.md          # how they make calls about their work
│   └── domain-map.md              # their topics, tools, recurring people/projects
├── project/
│   └── project-brief.md           # the recommended #1 project (scored)
├── .claude/
│   └── skills/
│       └── <skill-name>/
│           └── SKILL.md           # ONE runnable starter skill from their top task
└── material/                      # organized home for their real files (starts empty)
    └── README.md                  # what to drop here and how it gets used
```

Adjust folder names and `material/` subfolders to fit the person's archetype (see
`references/archetypes.md`).

## Voice rules (this is Wyndo's audience)

- Plain, direct, talking-to-a-smart-friend. No corporate jargon. Banned: "leverage,"
  "ecosystem," "synergy," "persistent context," "workspace" (as jargon), "transform/maximize/
  dominate/master/revolutionize/10x/game-changing/ultimate." Name the actual thing that
  changed instead.
- No em dashes. No "It's not X, it's Y" constructions (use "It's X, but also Y").
- Be honest, including about limits. If part of the work stays human, say so.
- It's "Claude Code," never "Cloud Code."

## The workflow

Run these phases in order. Read a reference file only when you reach the phase that needs it,
to keep context lean.

### Phase 1 — Interview

Run the adaptive interview. Full question flow, the time gate, and what each answer feeds is in
`references/interview.md` — read it now. Collect, at minimum: top 3-4 recurring tasks, a
confirmed time-per-task and frequency for the top 2-3, a rough mechanical-vs-judgment split
for those same tasks, what "good" looks like for the biggest task, 2-3 concrete things that go
wrong when AI or a junior does it, and (ideally) a folder of their past work to read, or one or
two pasted samples. Do not proceed until you have the numbers and the avoid-list.

### Phase 2 — Build the portrait (the "understand me" layer)

Nothing is written to disk yet. From the interview, infer and hold:

- **What they do**: role(s), domain(s), who their work serves.
- **Recurring tasks**: the work they do again and again.
- **Voice and thinking**: if they pointed you at real files or pasted samples, observe the
  voice there and pull *real quotes* as evidence — don't invent it. Interview answers are
  spoken and casual; they are not voice evidence. If there are no samples, leave an explicit
  fill-in prompt in `voice-and-style.md` (a half-filled file beats a fabricated one).
- **What "good" looks like**: their standard for the biggest task. This drives `CLAUDE.md` and
  the starter skill's quality bar.
- **What to avoid**: the 2-3 things they said go wrong when someone else does the task. These
  go into `CLAUDE.md` "What to avoid" and the starter skill, in their words.
- **Automation opportunities**: the repeated work a skill or workflow would eliminate.

Detect which of the four archetypes fits — content creator, coach/consultant, entrepreneur, or
knowledge worker. Read `references/archetypes.md` for signals, the `material/` scaffold, and
context emphasis. Straddling two → pick the dominant, note the secondary.

Draft the context files (`context/*.md`) from the templates in `assets/context-templates/`.
Fill from what they said; mark inferred sections and leave fill-in prompts where the interview
was thin. **This is honest interview-sourced work, not a data X-Ray** — say so in the portrait.

### Phase 3 — Recommend the #1 project

The person needs *one* real project, not a list. Use `references/project-scoring.md` to
generate 2-4 candidates from the interview, score them, and pick the single highest-scoring
one. Draft `project/project-brief.md`: what to build, why it scored highest, the recurring
input-to-output workflow inside it, and the first step.

### Phase 3.5 — Choose and draft one starter skill

Pick **one** runnable skill from their most-repeated, most-systematizable task (usually the #1
automation opportunity). Read `references/starter-skill.md` and draft it from
`assets/starter-skill-template/SKILL.md.template`, filled from the interview — their trigger
phrases, their tools, their quality bar, and their avoid-list. Keep it to ONE skill. It gets
written to `<workspace>/.claude/skills/<skill-name>/SKILL.md` in Phase 4.

### Phase 4 — Confirm, then assemble the folder

**Stop and check your read before writing anything.** Show the person, in a few short lines:

- Who the portrait says they are (role, who they serve, archetype, secondary if any).
- The 2-3 things you will tell Claude to avoid, in their words.
- The #1 project you picked and the runner-up, with one line on why.
- The starter skill you will build.
- The folder name and exactly where it will be created.

Ask "Does this match? Anything to change before I build it?" and wait. Adjust on their
answer. Only then write files. A wrong read caught here costs one message; caught after
fifteen files, it costs the person's trust.

**Where the folder goes.** Create `<name>-workspace/` inside the current working directory,
unless they name another location. Before creating it, check whether the current directory
already contains a `CLAUDE.md` or `AGENTS.md`:

- If it does, do not create a second starter folder and never overwrite the existing file.
  Ask: build into this existing project (add `context/`, `project/`, `material/`, and the
  starter skill alongside what is there, and propose additions to the existing `CLAUDE.md`
  as a diff for approval), or hand off to `/agentic-academy:build-operating-manual` for a
  fresh pair of instruction files. Their call.
- If the target folder name already exists, ask before touching it.

Then create the structure (see "What it produces", adapted per archetype). Generate:

- `context/*.md` from the drafts in Phase 2.
- `project/project-brief.md` from the draft in Phase 3.
- `.claude/skills/<skill-name>/SKILL.md` from the draft in Phase 3.5.
- `CLAUDE.md` from `assets/CLAUDE.md.template`, filled from the portrait. "What good looks
  like" comes from their standard; **"What to avoid" comes from the what-goes-wrong answers,
  in their words**. Build the routing table from the tools/files they named.
- `AGENTS.md` from `assets/AGENTS.md.template` — **identical substance to CLAUDE.md**, so the
  folder transfers to Codex. Keep the two in sync.
- `work-portrait.md` from `assets/interview-report.template.md` — include the honest
  data-source note (interview, not export) and the confirmed time-back math.
- `start-here.md` — orientation: what's in the folder, what to do first (including running the
  starter skill), and the 5-10 real files to add first based on the project and the skill's
  inputs.
- `material/README.md` + archetype subfolders — what to drop in and how it gets used. If they
  pointed you at a folder of past work, either copy the files they approved into the right
  subfolder or record the folder's path in `material/README.md`, whichever they chose. If they
  pasted samples, save each as a file in the right subfolder. Otherwise the folder starts
  **empty on purpose**, and `start-here.md` says what to add first.

### Phase 5 — Hand off

Tell the person, in plain language:

- The headline from the portrait: their top time sinks and the confirmed hours-per-week the
  recurring work is costing (make the hidden cost visible without overclaiming).
- Who the portrait says they are, the #1 project, and the starter skill you built.
- The single next action: open the folder, point Claude Code at it, add the first files
  `start-here.md` lists, and run the starter skill on real input.

Keep the handoff warm and concrete. The point is momentum, not a lecture.

## Notes for doing this well

- **The interview is the whole input — get the numbers.** Without a confirmed time-per-task,
  frequency, and mechanical-vs-judgment split for the top 2-3 tasks, the portrait's time-back
  math and the recommendation lose their spine. Estimate out loud and have them confirm; don't move on without it.
- **Confirm before you write.** The Phase 4 check-in is not optional. Fifteen files built on a
  wrong read are worse than none.
- **Never overwrite an existing `CLAUDE.md`.** If one is there, build alongside it and propose
  changes as a diff, or hand off.
- **Observe, don't flatter.** If they gave a sample, the voice file should sound like *them*,
  drawn from their words. If they didn't, say the voice is a placeholder until they add files —
  don't fabricate a voice from a job title.
- **Be honest about the evidence.** This is a portrait from a conversation, not a history. It's
  sharp on workflow and standards, thinner on voice texture until `material/` has real files.
  Present time figures as confirmed-rough, never false precision.
- **One skill, not a library.** Resist scaffolding more than one starter skill; when they want
  more, point them to `/agentic-academy:skill-finder`.
- **The folder is a starting point, not a monument.** A clean, real scaffold they'll actually
  extend beats an elaborate one they never touch.
- **`material/` empty + fill-in is the default.** The interview names where files go; the person
  supplies the files. One real sample from Phase 1 is a bonus first file, not a requirement.
