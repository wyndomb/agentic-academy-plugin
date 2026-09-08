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
Point to the later tools (Skills Library Builder, Pipeline Builder, Knowledge Repository
Builder), don't build them here.

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
confirmed time-per-task and frequency for the top 2-3, what "good" looks like for the biggest
task, and (ideally) one or two real work samples. Do not proceed until you have the numbers.

### Phase 2 — Build the portrait (the "understand me" layer)

From the interview, infer and write:

- **What they do**: role(s), domain(s), who their work serves.
- **Recurring tasks**: the work they do again and again.
- **Voice and thinking**: if they gave real samples, observe the voice and pull *real quotes*
  as evidence — don't invent it. If they gave no sample, write what you can and leave an
  explicit fill-in prompt in `voice-and-style.md` (a half-filled file beats a fabricated one).
- **What "good" looks like**: their standard for the biggest task. This drives `CLAUDE.md` and
  the starter skill's quality bar.
- **Automation opportunities**: the repeated work a skill or workflow would eliminate.

Detect which of the four archetypes fits — content creator, coach/consultant, entrepreneur, or
knowledge worker. Read `references/archetypes.md` for signals, the `material/` scaffold, and
context emphasis. Straddling two → pick the dominant, note the secondary.

Write the context files (`context/*.md`) from the templates in `assets/context-templates/`.
Fill from what they said; mark inferred sections and leave fill-in prompts where the interview
was thin. **This is honest interview-sourced work, not a data X-Ray** — say so in the portrait.

### Phase 3 — Recommend the #1 project

The person needs *one* real project, not a list. Use `references/project-scoring.md` to
generate 2-4 candidates from the interview, score them, and recommend the single
highest-leverage one. Write `project/project-brief.md`: what to build, why it scored highest,
the recurring input-to-output workflow inside it, and the first step.

### Phase 3.5 — Generate one starter skill

Scaffold **one** runnable skill from their most-repeated, most-systematizable task (usually the
#1 automation opportunity). Read `references/starter-skill.md`, copy
`assets/starter-skill-template/SKILL.md.template` into
`<workspace>/.claude/skills/<skill-name>/SKILL.md`, and fill it from the interview — their
trigger phrases, their tools, their quality bar. Keep it to ONE skill.

### Phase 4 — Assemble the folder

Create the structure (see "What it produces", adapted per archetype). Generate:

- `CLAUDE.md` from `assets/CLAUDE.md.template`, filled from the portrait. Build the routing
  table from the tools/files they named in the interview.
- `AGENTS.md` from `assets/AGENTS.md.template` — **identical substance to CLAUDE.md**, so the
  folder transfers to Codex. Keep the two in sync.
- `work-portrait.md` from `assets/interview-report.template.md` — include the honest
  data-source note (interview, not export) and the confirmed time-cost math.
- `start-here.md` — orientation: what's in the folder, what to do first (including running the
  starter skill), and the 5-10 real files to add first based on the project and the skill's
  inputs.
- `material/README.md` + archetype subfolders — what to drop in and how it gets used. The
  folder starts **empty on purpose**; if the person gave a real work sample in Phase 1, save
  it into the right subfolder as the first real file, and say so.

### Phase 5 — Hand off

Tell the person, in plain language:

- The headline from the portrait: their top time sinks and the confirmed hours-per-week the
  recurring work is costing (make the hidden cost visible without overclaiming).
- Who the portrait says they are, the #1 project, and the starter skill you built.
- The single next action: open the folder, point Claude Code at it, add the first files
  `start-here.md` lists, and run the starter skill on real input.

Keep the handoff warm and concrete. The point is momentum, not a lecture.

## Notes for doing this well

- **The interview is the whole input — get the numbers.** Without a confirmed time-per-task and
  frequency for the top 2-3 tasks, the portrait's time-cost and the recommendation lose their
  spine. Estimate out loud and have them confirm; don't move on without it.
- **Observe, don't flatter.** If they gave a sample, the voice file should sound like *them*,
  drawn from their words. If they didn't, say the voice is a placeholder until they add files —
  don't fabricate a voice from a job title.
- **Be honest about the evidence.** This is a portrait from a conversation, not a history. It's
  sharp on workflow and standards, thinner on voice texture until `material/` has real files.
  Present time figures as confirmed-rough, never false precision.
- **One skill, not a library.** Resist scaffolding more than one starter skill; that's a later
  cohort deliverable.
- **The folder is a starting point, not a monument.** A clean, real scaffold they'll actually
  extend beats an elaborate one they never touch.
- **`material/` empty + fill-in is the default.** The interview names where files go; the person
  supplies the files. One real sample from Phase 1 is a bonus first file, not a requirement.
