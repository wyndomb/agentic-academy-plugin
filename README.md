# Agentic Academy plugin

Fourteen skills for Claude Code, installed as one plugin. They cover the setup work that knowledge workers keep running into: building a project folder, writing the instructions Claude reads, finding what to automate, planning a bigger build, creating and auditing skills, turning corrections into rules, reviewing memory, and building subagents.

Every skill runs inside your own project, reads your real files, and asks before it changes anything.

## Install

Open Claude Code in any project and run these two commands once:

```text
/plugin marketplace add wyndomb/agentic-academy-plugin
```

```text
/plugin install agentic-academy@ai-maker
```

When the install panel asks for a scope, pick **user** so the skills follow you into every project. Then restart Claude Code or run `/reload-plugins`.

Prefer the terminal? The same two steps:

```bash
claude plugin marketplace add wyndomb/agentic-academy-plugin
```

```bash
claude plugin install agentic-academy@ai-maker
```

To confirm it worked, run `claude plugin list` in a terminal. You should see `agentic-academy@ai-maker` marked enabled.

## Two ways to use it

**Open the menu.** Type this and pick a number:

```text
/agentic-academy:academy-guide
```

**Or just describe the problem.** Every skill has a description Claude reads at the start of each session, so a sentence like "my CLAUDE.md feels bloated" or "what should I turn into a skill" lands on the right one without any command. Once you know the names, you can also call one directly, for example `/agentic-academy:rule-builder`.

Both routes end in the same place. The menu is there for when you do not know the names yet.

## Skills

Every skill is called as `/agentic-academy:<name>`, or reached by describing the need. Names link to the skill's folder.

### Start here

| Skill | Use when |
| --- | --- |
| [`/agentic-academy:academy-guide`](agentic-academy/skills/academy-guide) | **Read first** when you do not know which skill you need. Shows thirteen options in plain language, asks one question if your request could go two ways, then hands off to the right skill with your goal and files carried along. Does no work itself. |

### Get set up

| Skill | Use when |
| --- | --- |
| [`/agentic-academy:chat-to-workspace`](agentic-academy/skills/chat-to-workspace) | A **Claude or ChatGPT history export** (the full export file, not one pasted chat) → a project folder with `CLAUDE.md`, context files on who you are and how you work, a Chat X-Ray report on your patterns, a recommended first project, and one starter skill. Needs `python3`. |
| [`/agentic-academy:interview-to-workspace`](agentic-academy/skills/interview-to-workspace) | **No export**, or you would rather **talk than hand over chat history** → the same project folder, built from an interview about your real work, plus a work portrait report. Never asks for an export first. |

### Project instructions

| Skill | Use when |
| --- | --- |
| [`/agentic-academy:build-operating-manual`](agentic-academy/skills/build-operating-manual) | **No `CLAUDE.md` yet**, or one file without its `AGENTS.md` twin → a content-free scan, a proposal marking each claim observed / inferred / unknown, then both files written as a matched pair after you approve. Never writes before approval. Needs `python3`. |
| [`/agentic-academy:claude-md-upgrader`](agentic-academy/skills/claude-md-upgrader) | An **existing `CLAUDE.md` that feels thin or stale** → 5 to 10 ranked upgrade ideas across `CLAUDE.md`, `AGENTS.md`, rules, and skills, then patches for the ones you pick. Can draft a first `CLAUDE.md` alone when that single file is all you want. Does not find new skills. |
| [`/agentic-academy:audit-claude-md`](agentic-academy/skills/audit-claude-md) | A `CLAUDE.md` that is **bloated, contradictory, or untouched since a model change** → one verdict per instruction (Keep, Rewrite, Move, Test, or Retire), each with evidence. Judges only; does not create or edit. Needs `python3`. |

Three skills, one line between them: no file yet, use `build-operating-manual`; a file you want better, use `claude-md-upgrader`; a file you want judged, use `audit-claude-md`.

### Skills, rules, and helpers

| Skill | Use when |
| --- | --- |
| [`/agentic-academy:knowledge-worker-automation-recommender`](agentic-academy/skills/knowledge-worker-automation-recommender) | **"What should I automate next?"** on a project with real files → ranked recommendations across connected tools, skills, guardrails, subagents, and bundles, each tied to something it saw in your folders. Read-only; pick one and the menu carries it into the right builder. |
| [`/agentic-academy:skill-finder`](agentic-academy/skills/skill-finder) | **"What should I turn into a skill?"** → reads the whole project, inventories what is already automated, returns a ranked list of repeated tasks worth packaging, then writes `SKILL.md` files for the ones you choose. New skills only. |
| [`/agentic-academy:audit-skills`](agentic-academy/skills/audit-skills) | The **wrong skill keeps firing**, one never triggers, two overlap, or the folder has gone stale → a trigger map plus Keep, Clarify, Manual only, Merge, Test, or Archive per skill. Does not build. Needs `python3`. |
| [`/agentic-academy:rule-builder`](agentic-academy/skills/rule-builder) | You have **said the same correction twice** → checks whether it belongs in a rule, `CLAUDE.md`, memory, or just today's task; when a rule fits, writes a scoped file in `.claude/rules/` that loads only for matching work. |
| [`/agentic-academy:subagent-builder`](agentic-academy/skills/subagent-builder) | You want a **separate helper for one defined job**, or a **review panel** → reads the project, suggests helpers, interviews you on the handoff, writes files in `.claude/agents/`; panel mode adds the skill that runs them together. |

### Plan, memory, and housekeeping

| Skill | Use when |
| --- | --- |
| [`/agentic-academy:plan-and-execute`](agentic-academy/skills/plan-and-execute) | A job **too big for one sitting** (research, a content series, an ops overhaul, a bounded build) → an interview-led `plan.md` for approval and a `progress.md` record; work runs one approved milestone at a time and resumes across sessions. |
| [`/agentic-academy:memory-review`](agentic-academy/skills/memory-review) | **"What do you remember about me?"**, or a saved correction did not stick → a report of project and user-level memory, then one decision per stale, duplicated, or contradicted item for you to approve. Does not audit `CLAUDE.md`, rules, or skills. Needs `python3`. |
| [`/agentic-academy:sync-skills`](agentic-academy/skills/sync-skills) | You want a project to **carry its own copies** of your installed skills → editable copies in that project's `.claude/skills/`. One-time copy; re-run to refresh. |

### Example prompts

```text
Using /agentic-academy:academy-guide, help me work out where to start.
```

```text
My CLAUDE.md feels bloated and contradicts itself.
```

```text
I keep telling Claude to put the action items first in client reports.
```

```text
Interview me and build my project folder.
```

The first opens the menu. The other three go straight to `audit-claude-md`, `rule-builder`, and `interview-to-workspace` without naming them.

## Requirements

Claude Code with plugin support. Six skills run a small bundled Python script (`chat-to-workspace`, `build-operating-manual`, `audit-claude-md`, `audit-skills`, `memory-review`, `sync-skills` uses a shell script), so `python3` should be on your path. Nothing else is installed.

## Updates

New versions arrive through the marketplace. Claude Code checks for updates in the background; when one lands you will see a prompt to run `/reload-plugins`. To check by hand:

```text
/plugin marketplace update ai-maker
```

## Coming from the zip version

If you installed the earlier `academy-guide` zip into a project's `.claude/skills/` folder, delete that folder after installing the plugin. The plugin is the same toolkit, kept up to date automatically, with each skill reachable on its own.

## Troubleshooting

**Skills do not show up.** Restart Claude Code or run `/reload-plugins`. Then check `claude plugin list` in a terminal.

**A skill asks for a file I do not have.** Some skills need real material: an export for `chat-to-workspace`, an existing `CLAUDE.md` for the two audit and upgrade skills, a project with files in it for the recommender. The skill will say what it needs; the menu will offer the nearest route that works without it.

**A script fails.** Check that `python3` runs in your terminal. The skills fall back to doing the same inventory by hand if a script cannot run.
