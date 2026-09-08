# Ad Hoc Subagent Briefs

Use these briefs when the environment supports one-off subagents or an Agent/Task tool. These are not persistent `.claude/agents/` files. They are prompts the main skill can hand to separate subagents during a `skill-finder` run.

If ad hoc subagents are unavailable, run both passes yourself in the main conversation.

## How to run them

Two passes, launched **in parallel** in a single message. Both read the real files directly. Neither depends on the other's output, so neither waits.

1. **Evidence pass** - what the project produces and what work repeats.
2. **Inventory pass** - what is already automated.

Then score and rank in the main thread, where both reports are in context. Do not delegate scoring: it needs the project's stated priorities, both reports, and the mode decision at once, and handing that to a fourth agent only adds a summarization layer that loses filenames.

Why parallel rather than a chain: the whole skill depends on citing concrete filenames and sampled sections. Every hand-off between agents replaces real evidence with someone's prose summary of it, and cited evidence is the thing that makes the output arguable rather than merely plausible.

### When to delegate at all

Delegate when the repo is large enough that reading it would crowd out the reasoning: roughly 50+ content files, or an existing `.claude/` setup with more than a handful of entries.

Skip delegation and work inline when the repo is small, or when a directory listing is already in context and reading a few samples is cheap. A small project does not need four agents to find three candidates.

## Evidence Pass

Purpose: understand what the repo produces and find the repeated work, with citations.

Prompt:

```text
You are the evidence pass for a skill-finder run.

First, read the project home base if present: CLAUDE.md, AGENTS.md, README, plan.md, or similar. Note explicitly any stated priority, current focus, or goal the project claims about itself, and quote it. This gets used for scoring later.

Then inspect the folder structure, naming patterns, and a real sample of files from each main folder. Actually open files. Do not infer content from folder names.

Where git history is available, run git log over the busiest folders to see what is still active versus what is a dead pattern. Recent commits are the best available frequency evidence.

Then find possible skill candidates. Look for:

1. Volume clusters.
2. Naming-convention pipelines.
3. Folder-as-stage flows.
4. Described but not automated tasks.
5. Manual-glue synthesis across files.
6. Repeated-correction surfaces.
7. Template-shaped work.
8. Role or responsibility clues.
9. Knowledge-worker outputs such as status reports, meeting summaries, decision memos, stakeholder updates, research briefs, action item lists, and weekly reviews.
10. Half-automated pipelines: scripts, hooks, or build steps that consume a hand-written input file. The expensive half is built and a human still writes the input. These are often the strongest candidates.

Return:

1. What this project produces, in plain English.
2. Any stated priority or goal, quoted, with its source file.
3. The main folders and what each is for.
4. Frequency evidence per active area, from git where available.
5. 8-15 possible candidates. For each: name, the repeated task, concrete evidence (folders, filenames, headings, sampled sections), which signals fired, and whether the evidence is strong, medium, or thin.
6. Evidence limits: thin areas, dead folders, anything you could not verify.

Cite real filenames throughout. A candidate without a filename behind it is a guess, and should be labeled as one.

Do not dedup against existing skills, that is the other pass. Do not write files. Weak candidates are fine here; they get cut or labeled later.
```

## Inventory Pass

Purpose: establish what is already automated, so the scoring pass can dedup honestly.

Prompt:

```text
You are the inventory pass for a skill-finder run.

Your job is to map everything that already automates work in this project. Missing a surface is how a skill-finder run ships a duplicate recommendation, so check all of them.

Read and report:

1. .claude/commands/ - name plus first descriptive line of each.
2. .claude/skills/ - name plus description frontmatter of each.
3. .claude/agents/ - name plus description of each. Frequently overlooked, and often where content generation already lives.
4. .claude/rules/ - what each governs. Rules prove work recurs AND prove part of it is handled.
5. Skills installed outside the project: plugin skills, user-level skills, anything in the session's available-skills listing. These do not appear in the repo tree but they still cover the work. If a skill listing is visible in your context, read it and include it.
6. CLAUDE.md / AGENTS.md routing tables or playbook sections naming workflows.
7. Hooks in .claude/settings.json, and any scripts/ directory. For each, note what it does and whether it consumes a hand-written input file.

Return:

1. A coverage map: each distinct kind of work that is already automated, and what automates it.
2. Partial coverage: work where something exists but visibly stops short. Name exactly where it stops.
3. Whether this project is greenfield (little or no setup) or mature (meaningful existing automation). This decides how many candidates the run should return.
4. Anything that looks half-built: a script with no generator, a rule with no skill, a documented workflow nothing runs.

Be specific. "Content stuff is covered" is useless. "/newsletter-to-linkedin plus the linkedin-post-expander agent cover newsletter-to-LinkedIn; nothing covers transcript-to-LinkedIn" is what the scoring pass needs.

Do not propose skill candidates. Do not write files.
```
