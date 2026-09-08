---
name: chat-to-workspace
description: >-
  Analyze a person's past AI chat history (Claude and/or ChatGPT exports) and turn it into a
  ready-to-use Claude Code working folder: a CLAUDE.md home base, context files capturing who they
  are, their voice, and how they work, an organized space for their real material, a "Chat X-Ray"
  report, and a recommended #1 project. Use whenever someone is onboarding into agentic AI /
  Claude Code and needs a real workspace to start from, or says things like "analyze my chat
  history", "set up my Claude Code folder", "Chat X-Ray", "what should I build first", "I exported
  my ChatGPT/Claude conversations", or "help me get ready for the cohort". Also use when they hand
  over a conversations.json export to understand their own patterns, voice, workflows, or
  automation opportunities. Do NOT use for one-off content generation or a single pasted
  conversation (it expects a full export). If the person has no export or would rather not share
  their chat history, use interview-to-workspace instead.
---

# Chat to Workspace

Turn someone's past AI conversations AND saved memory into a working Claude Code folder they
can start building on immediately.

## Why this exists

Most people arrive at agentic AI with no real folder to work in. They've spent months
(sometimes years) building expertise inside chat — prompts they re-paste, a voice they've
trained the model into, frameworks they rebuilt from scratch every time a conversation
closed. All of it is trapped in history that can't talk to itself.

This skill reads that history and does two things at once:

1. **Understands the person** — who they are, what they work on, the workflows they
   repeat, their voice and thinking patterns, and where the automation opportunities are.
2. **Builds their workspace** — a real folder containing a CLAUDE.md + AGENTS.md home base,
   context files, organized space for their material, an analysis report, a clear first
   project, and one runnable starter skill. So instead of starting from an empty directory,
   they start from months of their own expertise, finally in a place where it compounds.

The goal is to get someone from "empty folder" to "real home base an agent can work inside"
in one pass.

## Where this sits in the concierge suite (scope)

This skill is the **first touchpoint**: it produces the Chat X-Ray report, the workspace
scaffold, the #1 project, and **exactly one** starter skill. It deliberately does NOT try to
be the whole suite. Hand the rest off to the later tools:
- More skills → **Skills Library Builder** (Week 5).
- Consolidating multi-chat workflows → **Pipeline Builder**.
- Organizing exported data/frameworks → **Knowledge Repository Builder**.
- Suggesting/upgrading skills → **Skill Finder / Skill Upgrader**.

Stay in your lane: report + folder + project + one skill. Point to the others; don't build them.

## What it produces

A new folder (default name `<name>-workspace/`) containing:

```
<name>-workspace/
├── CLAUDE.md                      # home base for Claude Code (reads this first)
├── AGENTS.md                      # same substance, for Codex / portable agents
├── chat-xray-report.md            # the analysis: patterns, costs, voice, opportunities
├── start-here.md                  # what this folder is + what to do next
├── context/                       # the "understand me" layer
│   ├── operator-profile.md        # who they are, what they do, their domains
│   ├── voice-and-style.md         # how they write / think, with real examples
│   ├── decision-rules.md          # how they make calls about their work
│   └── domain-map.md              # their topics, tools, recurring people/projects
├── project/                       # the recommended #1 project + workspace
│   └── project-brief.md           # what to build, why, how to start (scored)
├── .claude/
│   └── skills/
│       └── <skill-name>/
│           └── SKILL.md           # ONE runnable starter skill from their top pattern
└── material/                      # organized home for their real files (starts empty)
    └── README.md                  # what to drop here and how it gets used
```

Adjust folder names and `material/` subfolders to fit the person's archetype (see
`references/archetypes.md`).

## The workflow

Run these phases in order. Each phase points to a reference file when you need more detail —
read the reference only when you reach that phase, to keep context lean.

### Phase 0 — Get the exports

You need at least one of: a Claude export or a ChatGPT export. **Export more than just
conversations** — the saved memory / custom instructions are usually the single richest
signal, and they rescue thin conversation histories.

- **Claude** export contains `conversations.json`, **`memories.json`**, `projects.json`,
  **`users.json`** — get all of them. See `references/claude-export.md`.
- **ChatGPT** export — get `conversations.json` plus their **memory / custom-instructions**
  file. See `references/chatgpt-export.md`.

Ask where the export folder lives, or which folder to scan. Pointing at the unzipped folder
is enough — the parser finds and sorts the files itself.

Reassure them on privacy if they hesitate: the export stays on their machine, the parser
runs locally, and nothing is uploaded. (See "Privacy" below.)

### Phase 1 — Parse into a digest

Raw exports are too large to read directly. Run the parser to compress them:

```bash
python scripts/parse_exports.py --out <work_dir>/digest <path-to-export-folder>
# or scan a directory:
python scripts/parse_exports.py --out <work_dir>/digest --scan ~/Downloads
```

It auto-detects Claude vs ChatGPT conversations, and separately finds memory/profile files.
It writes three files:
- `digest/digest.json` — hard stats (conversation/message counts, words typed, date range,
  context-re-establishment count, repeated openers, longest dumps), the user's name, plus
  two verdicts you must honor: **`data_richness`** (how much to trust conversations vs.
  memory) and **`time_cost_estimate`** (a rough, caveated blank-slate-tax figure).
- `digest/samples.md` — a spread of the person's own messages (voice, topics, tasks).
- `digest/memory.md` — **their saved memory / project memories / custom instructions.** Read
  this carefully; it is the highest-signal source for the portrait.

Read all three. Let `data_richness.guidance` tell you where to lean: when conversations are
thin but memory is rich (a common case), build the portrait primarily from `memory.md` and
say so in the report.

### Phase 2 — Build the portrait (the "understand me" layer)

Read `memory.md` first (highest signal), then `samples.md` (voice texture) and the stats in
`digest.json`. Then infer:

- **What they do**: role(s), domain(s), who their work serves.
- **Recurring tasks**: the work they bring to AI again and again.
- **Voice and thinking**: how they phrase things, how they reason, what they care about.
  Pull *real quotes* from `samples.md`/`memory.md` as evidence — don't invent a voice,
  observe it.
- **Trapped knowledge**: frameworks, standards, visual systems, or reference material they've
  rebuilt across conversations (repeated openers, long dumps, and memory are strong signals).
- **Automation opportunities**: repeated work a skill or workflow would eliminate.

Detect which of the four archetypes fits best — content creator, coach/consultant,
entrepreneur, or knowledge worker. Read `references/archetypes.md` for signals, scaffold, and
context emphasis. If they straddle two, pick the dominant one and note the secondary.

Write the context files (`context/*.md`) from the templates in `assets/context-templates/`.
Fill them from evidence, not assumption. Where the data is thin on something, say so and
leave a fill-in prompt — a half-filled file they can finish beats a confident fabrication.
**Cite which source each claim came from when it matters** (memory vs. conversations), so the
report is honest about its evidence base.

### Phase 3 — Recommend the #1 project

The person needs *one* real project, not a list. Use the leverage-scoring framework in
`references/project-scoring.md` to generate 2-4 candidates from the evidence, score them, and
recommend the single highest-leverage one. Write `project/project-brief.md`: what to build,
why it scored highest, the recurring input-to-output workflow inside it, and the first step.

### Phase 3.5 — Generate one starter skill

So the person doesn't arrive at Week 1 with an empty `.claude/skills/`, scaffold **one**
runnable skill from their most-repeated, most-systematizable task. Read
`references/starter-skill.md`, copy `assets/starter-skill-template/SKILL.md.template` into
`<workspace>/.claude/skills/<skill-name>/SKILL.md`, and fill it from real evidence (their
trigger phrases, their quality bar). Keep it to ONE skill — the Skills Library Builder makes
the rest later.

### Phase 4 — Assemble the folder

Create the structure (see "What it produces", adapted per archetype). Generate:
- `CLAUDE.md` from `assets/CLAUDE.md.template`, filled from the portrait.
- `AGENTS.md` from `assets/AGENTS.md.template` — **identical substance to CLAUDE.md**, so
  the workspace transfers to Codex. Keep the two in sync.
- `chat-xray-report.md` from `assets/analysis-report.template.md` (include the data-source
  transparency and the caveated time-cost from `digest.json`).
- `start-here.md` — orientation: what's in the folder, what to do first (including running
  the starter skill), how it maps to the cohort's next steps.
- `material/README.md` + archetype subfolders — what to drop in and how it gets used.

The `material/` folder starts empty on purpose. `start-here.md` should tell them the 5-10
files to add first, based on the recommended project and the starter skill's inputs.

### Phase 5 — Hand off

Tell the person, in plain language:
- The headline numbers from the X-Ray (words typed, repeated prompts, date span, and the
  caveated time-cost) — make the hidden cost visible without overclaiming.
- Who the portrait says they are, the #1 project, and the starter skill you built.
- The single next action: open the folder, point Claude Code at it, add the first files
  `start-here.md` lists, and run the starter skill on real input.

Keep the handoff warm and concrete. The point is momentum, not a lecture.

## Privacy (say this if the person hesitates)

The export and everything generated stays in their folder on their machine. The parser runs
locally and uploads nothing. The skill never sends conversation or memory contents anywhere.
If they're still uneasy, they can run it on a Claude-only export first, or delete the raw
export once the digest and workspace are built.

## Notes for doing this well

- **Memory is the richest signal — read it first.** A thin conversation export (recent or
  sparse) can still produce a strong portrait if `memory.md` is rich. Honor
  `data_richness.guidance`.
- **Observe, don't flatter.** The portrait should sound like *them*, drawn from their own
  words. Specific evidence ("opens by stating constraints before asking for options") beats
  generic praise ("you're a strategic thinker!").
- **Be honest about your evidence.** Say when a claim comes from memory vs. conversations,
  and when data was thin. Present the time-cost as a range, never false precision.
- **One skill, not a library.** Resist scaffolding more than one starter skill; that's a
  later cohort deliverable.
- **The folder is a starting point, not a monument.** Bias toward a clean, real scaffold the
  person will actually extend over an elaborate structure they'll never touch.
