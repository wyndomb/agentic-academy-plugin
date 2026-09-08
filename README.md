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

## Which skill do I need?

| You are thinking... | Use |
| --- | --- |
| "I want to get set up and I have a ChatGPT or Claude export" | `chat-to-workspace` |
| "I want to get set up but I would rather just talk" | `interview-to-workspace` |
| "What should I automate next?" | `knowledge-worker-automation-recommender` |
| "This project has no CLAUDE.md. Write one from what is here." | `build-operating-manual` |
| "I have a CLAUDE.md. How do I make it better?" | `claude-md-upgrader` |
| "My CLAUDE.md feels bloated or contradicts itself" | `audit-claude-md` |
| "This is a big project. Plan it properly and let me resume later." | `plan-and-execute` |
| "Which of my repeated tasks should become skills?" | `skill-finder` |
| "The wrong skill keeps firing" or "I have too many skills" | `audit-skills` |
| "I keep correcting the same thing" | `rule-builder` |
| "What does Claude remember about me?" | `memory-review` |
| "I want a separate helper for this one job" or "a review panel" | `subagent-builder` |
| "Copy my installed skills into this project" | `sync-skills` |

Three of these deal with project instructions, and the line between them matters. `build-operating-manual` creates `CLAUDE.md` and `AGENTS.md` as a pair from scratch, with a proposal first. `claude-md-upgrader` improves a `CLAUDE.md` you already have. `audit-claude-md` gives a verdict on one without changing it. If you are unsure, the menu will ask you one question and route you.

## The skills in detail

Each entry says what the skill does, when to reach for it, what you might say, what you get back, and what it will not do.

### academy-guide

The menu. Shows thirteen options in plain language, asks one question if your request could go two ways, then hands off to the right skill with your goal and files carried along.

**Reach for it when** you do not know the skill names, or want to see what is possible.

**Try saying** `/agentic-academy:academy-guide`, or "what can the Academy tools help me with?"

**You get** the menu, then whatever the chosen skill produces.

**It will not** do any work itself. It only routes.

### chat-to-workspace

Reads a full Claude or ChatGPT history export and builds a Claude Code project folder from what it finds: who you are, how you work, what you keep asking for.

**Reach for it when** you are starting from nothing and you have an export.

**Try saying** "I exported my ChatGPT conversations, set up my Claude Code folder," or "run the Chat X-Ray on this export."

**You get** a project folder with `CLAUDE.md`, context files (operator profile, voice, decision rules, domain map), a place for your real material, a Chat X-Ray report on your patterns, a recommended first project, and one starter skill.

**It will not** work from a single pasted conversation. It needs the full export file. Parsing the export uses a bundled Python script, so `python3` needs to be available.

### interview-to-workspace

The same project folder as above, built from a conversation instead of an export. It asks about your real work, then writes the files.

**Reach for it when** you have no export, or you would rather not hand over your chat history. Both are equally good reasons.

**Try saying** "interview me and build my project folder," or "I don't have a chat export, get me set up."

**You get** a project folder with `CLAUDE.md` and `AGENTS.md`, context files, a material space, a work portrait report, a recommended first project, and one starter skill.

**It will not** ask you to produce an export first.

### knowledge-worker-automation-recommender

Looks at how you actually work (your folders, filenames, the kinds of documents you keep) and recommends what to set up next: connected tools, reusable skills, guardrails, specialist helpers, or bundles. Built for writers, consultants, founders, analysts, and operators, not for codebases.

**Reach for it when** you have a project with real files in it and want broad advice on what would help most.

**Try saying** "look at my project and tell me what to automate," or "how do I get more out of Claude Code for my client work?"

**You get** a ranked set of recommendations in plain language, each tied to something it saw in your files.

**It will not** build anything. It reads and recommends. Pick one recommendation and the menu carries it into the right builder.

### build-operating-manual

Scans a project without reading private file contents, samples a few representative files, and works out the project's core job: the Work it repeats, the Input it needs, the Output it produces, and the Key Standard the output must pass. It shows you a proposal with every claim marked observed, inferred, or unknown. After you approve, it writes `CLAUDE.md` and `AGENTS.md` as a matched pair so both Claude and Codex read the same project truth.

**Reach for it when** a project has no instruction files yet, or has one without the other, and you want them written from evidence rather than from a template.

**Try saying** "this project has no CLAUDE.md, write one from what is here," or "create the operating manual for this folder."

**You get** the proposal first, then both files, each with the same five blocks: Orient, Guardrails, Playbooks, Routing, Map.

**It will not** write before you approve the proposal, copy anything personal or sensitive into the files, or overwrite a mature instruction file silently. The scan uses a bundled Python script.

### claude-md-upgrader

Reads a knowledge-work project and returns 5 to 10 ranked ways to improve its `CLAUDE.md`, `AGENTS.md`, rules, or skills. Pick the ones you want and it applies them. It can also draft a first `CLAUDE.md` alone when that single file is all you need.

**Reach for it when** you already have a `CLAUDE.md` and it feels thin, generic, or out of date.

**Try saying** "improve my CLAUDE.md," "is my CLAUDE.md any good?", or "set up my project home base."

**You get** a ranked list of upgrades with the reasoning visible, then targeted patches for the ones you choose.

**It will not** find new skills (that is `skill-finder`) or mine your chat history for lessons.

### audit-claude-md

Audits an existing instruction setup and gives each instruction an evidence-backed verdict: Keep, Rewrite, Move, Test, or Retire. Useful after a model change, a tool change, or when a file has grown by accretion.

**Reach for it when** your `CLAUDE.md` feels bloated, contradicts itself, or has lines you suspect no longer do anything.

**Try saying** "audit my CLAUDE.md," "I switched models, check my setup," or "which of these instructions can I delete?"

**You get** a report with one call per instruction and the evidence behind it. Some findings include a quick test you can run to check whether an instruction still matters.

**It will not** create a first `CLAUDE.md`, audit skill routing, or edit anything without approval. Bundled scripts need `python3`.

### plan-and-execute

Turns a substantial project into two files: `plan.md` (the approved plan, milestone by milestone) and `progress.md` (what is done, what is next). Work proceeds one approved milestone at a time, with verification and a self-check before each report, so you can close the session and pick up later without losing the thread.

**Reach for it when** the job is too big for one sitting: a research project, a content series, an operations overhaul, a bounded build.

**Try saying** "plan this out properly," "let's build this in milestones," or "resume my plan."

**You get** an interview-led plan for approval, then execution and a running progress record.

**It will not** skip the approval step or run past one milestone without checking in. If you already have a spec, it asks which document governs before writing a plan.

### skill-finder

Reads a whole project, works out what it actually produces, checks what is already automated, and returns a ranked list of repeated tasks worth turning into new skills. Pick the ones you want and it writes real `SKILL.md` files for them.

**Reach for it when** you suspect you keep doing the same thing by hand and want to know which of those are worth packaging.

**Try saying** "what should I turn into a skill?", "scan my project for skill opportunities," or "what can I automate here?"

**You get** a short ranked list with the reasoning shown, then skill files for the ones you choose.

**It will not** improve, audit, or upgrade skills that already exist. That is `audit-skills`.

### audit-skills

Audits the skills you already have. Builds a trigger map showing what each skill fires on, then gives each one a call: Keep, Clarify, Manual only, Merge, Test, or Archive.

**Reach for it when** Claude activates the wrong skill, misses one that should have fired, two skills overlap, or your skills folder has grown stale.

**Try saying** "the wrong skill keeps firing," "audit my skills," or "I have too many skills and some overlap."

**You get** the trigger map and one recommendation per skill, with evidence. Some findings include a trigger test you can run.

**It will not** build new skills or edit files without approval. Bundled scripts need `python3`.

### rule-builder

Turns corrections you keep repeating into rules: small files in `.claude/rules/` that load only when Claude is working on matching files. Your standards for posts, client emails, or reports apply on their own, and cost nothing the rest of the time. It first checks whether the correction belongs in a rule at all, or in `CLAUDE.md`, personal context, memory, or just today's task.

**Reach for it when** you have said the same thing to Claude twice.

**Try saying** "I keep telling it to put action items first in client reports," "should this be a rule?", or "why isn't this instruction sticking?"

**You get** a placement recommendation, and when a rule is the right home, a scoped rule file after you approve it.

**It will not** write a rule for a one-off correction.

### memory-review

Reads Claude Code's auto memory for the current project (and the user-level layer), then audits it: stale, vague, duplicated, orphaned, misplaced, or contradicted memories each get one proposed decision. Works in the desktop app without the `/memory` terminal command.

**Reach for it when** you want to know what Claude has picked up about you, or a saved correction did not stick.

**Try saying** "what do you remember about me?", "review my memory," or "that saved memory is wrong."

**You get** a report of what lives in memory and where, then one decision per finding for you to approve.

**It will not** audit `CLAUDE.md`, rules, or skills, or edit or delete without approval. Uses a bundled Python script.

### subagent-builder

Interviews you and builds subagents as files in `.claude/agents/`. It reads the project first and suggests helpers based on the work that actually happens there. It can also build a panel: several subagents reviewing the same piece of work, plus a skill that runs them and combines what they return.

**Reach for it when** you want to hand one defined job to a separate worker, or you want an independent review from more than one angle.

**Try saying** "build me a subagent that checks my drafts for voice," "should this be a subagent?", or "I want a review panel."

**You get** approved subagent files, and for a panel, the coordination skill too.

**It will not** guess at a handoff. It asks what the helper needs to receive and return, because a subagent starts fresh and only sees what you pass it.

### sync-skills

Copies every skill you have installed into a project's `.claude/skills/` folder, so the skills travel with that project as editable, checked-in copies.

**Reach for it when** you want a project to carry its own skills, for example a repo you share with someone else.

**Try saying** "copy my installed skills into this project."

**You get** plain copies in the project, and a list of what was copied.

**It will not** keep the copies in sync afterwards. Re-run it after installing or updating skills. It verifies the source path and confirms before replacing existing copies.

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
