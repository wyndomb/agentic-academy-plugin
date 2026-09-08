# Choose the right skill

Read this after a student selects a menu item or gives a specific request. These are selection notes. The chosen skill carries its own full instructions; invoke it with the Skill tool by its full name.

## Routes

| Menu | Skill | Choose it when | Input and useful result |
| --- | --- | --- | --- |
| 1 | `agentic-academy:chat-to-workspace` | Starting from a full Claude or ChatGPT history export. | Export plus available memory/profile material becomes a project folder, context files, Chat X-Ray report, recommended project, and one starter skill. A single pasted chat does not satisfy this route. |
| 2 | `agentic-academy:interview-to-workspace` | Starting without an export, or the student prefers to talk. | An interview about real work becomes a project folder, context files, work portrait, recommended project, and one starter skill. |
| 3 | `agentic-academy:knowledge-worker-automation-recommender` | The student wants broad advice about what to automate or improve next in an existing knowledge-work project. | Real project files and current setup become recommendations across suitable tools, skills, hooks, subagents, and bundles. Read-only. |
| 4 | `agentic-academy:build-operating-manual` | The project has no `CLAUDE.md` yet, or has one file but not the other, and the student wants both written from what the project actually contains. | A content-free scan plus sampled files become a proposal (observed, inferred, unknown), then `CLAUDE.md` and `AGENTS.md` as a matched pair after approval. It never writes before the proposal is approved. |
| 5 | `agentic-academy:claude-md-upgrader` | A `CLAUDE.md` exists and the student wants ranked ideas to make it better, and may want them applied. | Project files become 5 to 10 ranked improvements, then selected patches after approval. Can also draft a first `CLAUDE.md` alone when the student only wants that one file. |
| 6 | `agentic-academy:audit-claude-md` | An existing `CLAUDE.md` feels bloated, contradictory, vague, or stale, usually after a model, tool, or project change, or before removing old instructions. | Every instruction gets an evidence-backed Keep, Rewrite, Move, Test, or Retire recommendation. Does not create a first file or edit without approval. |
| 7 | `agentic-academy:plan-and-execute` | A substantial project needs an approved milestone plan and a record for resuming work. | Goal and source material become `plan.md` and `progress.md`; execution proceeds one approved milestone at a time. |
| 8 | `agentic-academy:skill-finder` | The student wants to discover recurring tasks worth packaging into NEW skills in an existing project. | Real work plus an inventory of existing automation become ranked opportunities; selected candidates become skill files. |
| 9 | `agentic-academy:audit-skills` | Claude activates the wrong skill, misses a useful one, two skills overlap, or the skills folder feels bloated or stale. | A trigger map plus Keep, Clarify, Manual only, Merge, Test, or Archive recommendations for existing skills. Does not build new skills or edit without approval. |
| 10 | `agentic-academy:rule-builder` | Repeated corrections or output-specific standards need a durable home. | Actual feedback and project evidence become a placement recommendation and, when appropriate and approved, a scoped rule file. It first checks whether the correction belongs in a rule, project instructions, personal context, memory, or only today's task. |
| 11 | `agentic-academy:memory-review` | The student wants to see what Claude remembers, inspect stale or conflicting memories, or investigate a correction that was not remembered. | Existing Claude memory and user-level instructions become an audit proposal with one decision per finding; only approved changes are applied. |
| 12 | `agentic-academy:subagent-builder` | The student wants a separate helper for a defined handoff, wants to discover useful helpers, or wants a review panel. | Project evidence and an interview become approved subagent files; panel mode also defines how a coordination skill combines their results. |
| 13 | `agentic-academy:sync-skills` | The student wants installed skills copied into a specified project. | A verified accessible skill source and target folder become local copies. A copy operation, with no ongoing synchronization. |

## Resolve overlapping requests

### Starting from nothing or improving an existing project

"Help me get set up" can mean two different starting points. If the student needs their work understood and a first project chosen, use option 1 or 2. If they already have a project and real material, and need instructions for it, use one of the three project-instruction routes below.

Options 1 and 2 reach the same kind of result through different source material, and neither is the fallback for the other. Option 1 reads a full export. Option 2 asks questions instead, which is the right route for a student who has no export and equally for one who would rather not hand over their chat history. Take the student's stated choice at face value and do not argue them toward the other route.

Confirm the needed material before starting. If a student chose option 1 and has no usable export, say what the route needs, then offer option 2 as the other real way in. If a student chose option 2, do not ask them to produce an export first. Preserve an established project instead of generating a second starter folder without a reason.

### Broad automation advice or new skills specifically

Use `knowledge-worker-automation-recommender` for "What should I automate next?" when the answer could involve several kinds of setup. Use `skill-finder` when the student specifically wants repeated tasks turned into new skills. Do not run both discovery scans by default.

If the student selects a new-skill recommendation from the broad review, carry its evidence into `skill-finder` and focus on the selected task.

### Planning and completing a project

Use `plan-and-execute` for option 7. If `plan.md` and `progress.md` already exist, that skill reads them and preserves the current plan and approval state. If the student brings a separate specification, clarify which document governs before creating or changing a plan. Never silently replace their specification or overwrite a progress record.

### Repeated mistakes, project instructions, or memory

- "Every client report needs the action items first" suggests `rule-builder`, which verifies that the correction belongs in a rule before drafting.
- "What do you remember about me?" or "That saved memory is wrong" goes directly to `memory-review`.
- Project instructions have three routes. Pick by what exists and what the student wants back:
  - No `CLAUDE.md` yet, or one file without its `AGENTS.md` twin, and they want both written from evidence: `build-operating-manual`. It scans, shows a proposal with observed, inferred, and unknown items, and writes only after approval.
  - A `CLAUDE.md` exists and they want it better: `claude-md-upgrader`. It returns ranked upgrade ideas and applies the ones they choose. It can also draft a first `CLAUDE.md` alone when they only want that single file.
  - A `CLAUDE.md` exists and they want a verdict on it ("feels bloated," "contradicts itself," "I changed models"): `audit-claude-md`. It judges each line and does not build.
  - When two could fit, ask one question: "Do you want a new pair of files, ideas to improve what you have, or a line-by-line verdict?"
- "Claude keeps forgetting" without a concrete example needs one clarifying question: ask what it forgot or which correction keeps recurring. Not every forgotten instruction is a memory problem.

If a memory audit identifies an output-specific standard, offer `rule-builder` for the placement change and carry the exact finding forward.

### Skills or separate helpers

Use `subagent-builder` for a defined job handed to a separate helper, an independent review, or a panel. Use `skill-finder` to discover repeatable procedures worth packaging as NEW skills. Use `audit-skills` when the problem is with skills that already exist: the wrong one fires, a useful one never triggers, two overlap, or the folder has grown stale. Do not run `skill-finder` and `audit-skills` together by default; one finds gaps, the other judges what is there.

For "improve my existing skill," start with `audit-skills` to get the trigger map and a Keep, Clarify, Merge, or Archive call, then make the approved edits directly. `claude-md-upgrader` can flag skill problems in passing during a broader setup review, but `audit-skills` is the dedicated route.

### Copying installed skills

`sync-skills` copies from the installed-skills location into a project. Inspect its script before running it and verify the real source path fits this environment. Confirm how existing destination copies will be handled before any replacement the student has not already authorized. Never point a bulk copy at its own destination.
