# Detection Patterns and Scoring

This is the calibration reference for `skill-finder`. It holds the signal catalog (how to spot a skill opportunity), the exploration rules for thin projects, and the scoring bar (how to judge whether it is worth building).

## Output goal

The right number of candidates depends on how much is already automated. Pick the mode from the coverage inventory, not from repo size.

### Greenfield or thin mode

Use when the project has little or no `.claude/` setup. Return **5-10 candidates**. The user needs a menu, and breadth is the point:

1. Strong candidates they can build now.
2. Promising candidates they should customize first.
3. Exploratory candidates that may become useful once they add more examples.

If the project has limited files, still generate candidates from the available evidence. Say what the evidence can and cannot prove.

### Mature mode

Use when the coverage inventory already shows meaningful automation (existing commands, skills, agents, or rules covering the obvious work). Return **3-7 candidates**.

In this mode, "most of the obvious work here is already covered" is a **finding, not a failure**. Say it plainly and name what covers it. Three well-evidenced candidates on a mature repo are worth more than seven where four are padding.

Do not manufacture candidates to hit a count. If honest dedup leaves you with three, return three and explain why the list is short. A user with a mature setup is asking what is genuinely missing, not for a longer list.

## The signal catalog

Walk each signal against the project. A candidate that fires on two or more signals is usually real. A candidate that fires on one signal may still be worth exploring if it has a clear file-shaped output and the user likely repeats it.

### 1. Volume cluster

Many files of the same shape sitting in one folder (30 LinkedIn posts, 50 drafts, 40 meeting notes). High volume of similar outputs means the person is doing the same kind of production over and over by hand. That is the clearest skill signal there is.

**Read it as:** "You produce a lot of X. A skill can give X a repeatable starting point instead of a blank page."

### 2. Naming-convention pipeline

Filenames that encode stages or dates with a consistent pattern (`MMDDYY-dailynote.md`, `YYYY-MM-DD-topic-notes.md`, `proposal-v2-clientname.md`). A consistent naming convention is a fossil of a repeated process the human runs manually.

**Read it as:** "You follow the same naming ritual every time. The work behind that ritual is a candidate skill."

### 3. Folder-as-stage flow

Folders that represent steps in a flow, where content visibly moves from one to the next (brain-dump → notes → linkedin-posts → twitter-thread; or notes → prep-brief → proposal → follow-up). Movement of content across folders is a pipeline, and pipelines are the richest skill and workflow territory.

**Read it as:** "Your content travels a known path. Each hop is a candidate skill, and the whole path is a candidate workflow."

### 4. Described but not automated

The `CLAUDE.md` or a planning doc describes a recurring task in words ("Flow: brain dump to daily notes to social posts") but no command or skill actually runs it end to end. The gap between a documented process and an automated one is a ready-made skill.

**Read it as:** "You already wrote down how this works. Nothing runs it yet. That is the skill."

### 5. Manual-glue synthesis

Outputs that clearly stitch several source files together by hand: a report that pulls from three data files, a digest that reads a stats file plus an archive, a status update assembled from multiple project notes. Synthesis across files is valuable because it is slow and draining to do manually.

**Read it as:** "You assemble this from several places by hand every time. A skill can do the gather-and-synthesize in one step."

### 6. Repeated-correction surface

Rules, memory files, or correction logs about recurring mistakes in a specific kind of work. If a task generates enough corrections to need its own rules, it is done often enough to deserve a skill with those guardrails baked in.

**Read it as:** "You keep correcting the same thing in this kind of work. A skill can carry those corrections so you stop repeating them."

### 7. Template-shaped work

Files that share repeated sections, headings, checklists, tables, or output formats. This can appear even in a small project. A folder with three reports using the same sections may not prove high frequency, but it does show a repeatable shape.

**Read it as:** "You already have a format. A skill can turn messy input into that format."

### 8. Role or responsibility clue

Project docs, README files, plans, meeting notes, or course materials describe a role the user keeps playing: project manager, operator, researcher, content lead, consultant, founder, team lead. These clues can suggest likely recurring work even when examples are thin.

**Read it as:** "Your files show the kind of job you keep doing. A skill can support the repeated output that job requires."

### 9. Knowledge-worker output

Look specifically for status updates, meeting summaries, decision logs, project plans, executive summaries, research briefs, stakeholder updates, weekly reviews, action item lists, roadmaps, handoffs, and synthesis notes. These are often valuable skill candidates because they convert scattered information into a clear artifact.

**Read it as:** "You are repeatedly turning scattered context into a usable work document."

### 10. Half-automated pipeline

A script, hook, build step, or command that consumes a hand-written input file. The expensive half is already built; a human still writes the input by hand every time. Look for `scripts/` directories, `build_*.py` files, hooks in `.claude/settings.json`, and any place where a markdown file is clearly the input to a generated artifact (a deck, a PDF, a published page).

This is often the single best candidate type in a mature repo, because the surrounding machinery already proves the work recurs and the missing piece is exactly the kind of content generation a skill does well.

**Read it as:** "You already automated the back half. The skill writes the input the back half is waiting for."

## Frequency evidence

Frequency is the heaviest single criterion in the scoring bar, so do not infer it from file counts alone. A folder of 40 dated files proves the work happened; it does not prove it is still happening.

Cheapest reliable check: `git log` over the candidate's folder. Recent commits mean the work is live. A folder with no commits in six months is a dead pattern, and a skill for it is maintenance you will not use. When there is no git history, fall back to the newest file date in the folder and say that is what you used.

## Thin-project mode

Use thin-project mode when the repo has fewer than 20 useful examples for most candidate tasks, or when the folder is early, messy, or mostly planning material.

In thin-project mode:

1. Still produce 5-10 candidates if possible.
2. Label each candidate with confidence: High, Medium, or Low.
3. Include the evidence that produced the idea, even if the evidence is only folder names, filenames, headings, or one sample file.
4. Prefer "Customize first" or "Explore later" for weakly evidenced candidates.
5. Ask for one missing input only when the candidate cannot be scaffolded without it.

## The scoring bar (0-10)

Score each candidate by adding the points it earns. Frequency and strategic fit carry the most weight, because a skill for rare work, or for work that does not serve what the project is actually trying to do, is not worth maintaining.

| Criterion | Points | Test |
| --- | --- | --- |
| Frequency | 0-3 | Done weekly or more = 3. Monthly = 2. Rare = 0-1. Check git history, not just file counts. |
| Strategic fit | 0-2 | Directly serves a priority the project states about itself = 2. Useful but off-priority = 1. Unrelated to any stated goal = 0. |
| File-shaped output | 0-2 | Produces a draft, report, brief, or deliverable = 2. Produces a vague "answer" = 0-1. |
| Definable quality | 0-2 | You can describe good vs bad in plain language = 2. Fuzzy = 0-1. |
| Examples available | 0-1 | 20+ past examples to learn the pattern from = 1. Fewer = 0. |

### Reading strategic fit

Most projects say what they are trying to do. Read `CLAUDE.md`, `AGENTS.md`, a README, or a `plan.md` for a stated priority, current focus, or goal. You are already reading these in Step 1, so this costs nothing.

Score the candidate against that stated priority, not against your own sense of what matters. If a project says its current focus is deepening revenue, a candidate that serves revenue outranks a higher-frequency candidate that does not. If the project states no priority anywhere, score every candidate 1 here and say you found no stated goal to judge against.

This criterion is what breaks ties in the final ranking. Two candidates scoring the same overall should be ordered by strategic fit.

**Default cutoff:** a candidate that scores 5-6 is worth listing with a note on its weakest criterion. A candidate scoring 7+ is a strong build. In thin-project mode, candidates below 5 can appear only to complete a useful menu, and they must be labeled Low confidence or Explore later. In mature mode, do not list candidates below 5 at all.

## Confidence labels

- **High:** multiple examples, repeated format, clear output, clear quality standard.
- **Medium:** some examples or strong folder/process evidence, but one part still needs user preference.
- **Low:** plausible from the repo, but limited examples or unclear quality bar.

## Readiness labels

- **Build now:** enough evidence to scaffold a useful v1 skill.
- **Customize first:** useful idea, but ask the user for one or two standards before building.
- **Explore later:** promising pattern, but the project needs more examples or clearer standards first.

## Honesty rules

- Do not inflate frequency or example counts to push a candidate over the line. Score what is actually in the project.
- If a project is thin, say so plainly and label confidence. Do not hide uncertainty.
- A list of mixed-confidence candidates is useful when the user is exploring a greenfield project. A long list of weak candidates with no evidence is not.
- On a mature project, do not pad. Returning three real gaps and naming what already covers the rest is a better answer than seven candidates where four are filler. The user with an existing setup is asking what is genuinely missing.
