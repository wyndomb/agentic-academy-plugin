# Agentic Academy plugin

One install gives you the full Agentic Academy toolkit inside Claude Code: thirteen skills for setting up a project, finding what to automate, improving and auditing your instructions, planning a build, creating and auditing skills, turning corrections into rules, reviewing memory, building subagents, and copying skills into a project.

## Install

Open Claude Code in any project and run these two commands once:

```text
/plugin marketplace add wyndomb/agentic-academy-plugin
```

```text
/plugin install agentic-academy@ai-maker
```

When the install panel asks for a scope, pick **user** so the skills are available in every project. Restart Claude Code or run `/reload-plugins`.

Prefer the terminal? The same two steps:

```bash
claude plugin marketplace add wyndomb/agentic-academy-plugin
```

```bash
claude plugin install agentic-academy@ai-maker
```

## Start here

```text
/agentic-academy:academy-guide
```

That shows a twelve-option menu. Pick a number or describe what you need in your own words.

You can also go straight to any skill, or just describe the task and let Claude pick:

| Skill | What it does |
| --- | --- |
| `/agentic-academy:chat-to-workspace` | Build a project folder from a Claude or ChatGPT history export |
| `/agentic-academy:interview-to-workspace` | Build the same folder from a short interview, no export needed |
| `/agentic-academy:knowledge-worker-automation-recommender` | Look at your real work and suggest what to automate next |
| `/agentic-academy:claude-md-upgrader` | Create or improve your CLAUDE.md and AGENTS.md |
| `/agentic-academy:audit-claude-md` | Audit an existing CLAUDE.md for bloat, contradictions, and stale lines |
| `/agentic-academy:plan-and-execute` | Turn a substantial project into an approved plan and work through it |
| `/agentic-academy:skill-finder` | Find repeated tasks worth turning into skills, then build the ones you pick |
| `/agentic-academy:audit-skills` | Audit the skills you already have: wrong triggers, overlaps, stale folders |
| `/agentic-academy:rule-builder` | Turn corrections you keep repeating into rules |
| `/agentic-academy:memory-review` | See what Claude remembers and clean up what needs it |
| `/agentic-academy:subagent-builder` | Build subagents for defined tasks, or a review panel |
| `/agentic-academy:sync-skills` | Copy your installed skills into a project folder |

## Updates

New versions arrive through the marketplace. Claude Code checks for updates in the background; when one lands you will see a prompt to run `/reload-plugins`. To check manually:

```text
/plugin marketplace update ai-maker
```

## Coming from the zip version

If you installed the earlier `academy-guide` zip into a project's `.claude/skills/` folder, you can delete that folder after installing the plugin. The plugin version is the same toolkit, kept up to date automatically, with each skill reachable on its own.
