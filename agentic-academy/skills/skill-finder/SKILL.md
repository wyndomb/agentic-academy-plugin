---
name: skill-finder
description: >-
  Reads a whole project, works out what it actually produces, inventories what is already
  automated, and hands back a ranked list of skill opportunities that are genuinely missing. After
  the user selects, it scaffolds real SKILL.md files for the chosen ones. Use this WHENEVER the
  user asks "what should I turn into a skill", "what can I automate here", "scan my project for
  skills", "find skill opportunities", "what workflows could be skills", or hands over a project
  folder and wants to know which repeated tasks are worth packaging. This finds NEW skills only.
  It does not improve, audit, or upgrade skills that already exist.
---

# Skill Finder

This skill solves the single hardest step in turning a project into an AI work system: knowing *which* recurring task deserves to become a skill. Most people can write a skill once they know what to build. The bottleneck is staring at a folder of work and not seeing which parts are repeatable enough to package.

Your job: read the project, inventory what is already automated, find repeated or likely-repeatable file-shaped work that is *not* yet covered, score each candidate against a real bar, and hand back a short ranked list with the reasoning visible. Then, after the user picks, write real skill files for the chosen ones.

You are NOT a skill auto-generator that fires blind. The value is in showing the user a list they can react to, where each item explains *why it qualifies*. That reasoning is the teaching layer. It is how someone learns to spot skill opportunities themselves, instead of depending on this skill forever.

## What counts as a skill opportunity

A skill opportunity is **recurring or likely-repeatable file-shaped work with a definable good-vs-bad standard**. The full catalog of signals to look for (volume clusters, naming-convention pipelines, folder-as-stage flows, described-but-not-automated tasks, manual-glue synthesis, repeated-correction surfaces, template-shaped work, role clues, knowledge-worker outputs, and half-automated pipelines) lives in `references/detection-patterns.md`. Read it before scanning.

A one-off task is not a strong skill opportunity, but a thin project may still contain useful starter candidates. Be honest about the difference. If the evidence is thin, still generate ideas, but label them as lower-confidence or "explore later" candidates instead of pretending they are proven.

## The scoring bar

Each candidate is scored 0-10 on skill-worthiness using the criteria in `references/detection-patterns.md` (frequency, strategic fit, file-shaped output, definable quality, and examples available). Also assign a confidence label: High, Medium, or Low.

How many candidates to return depends on how much is already automated:

- **Greenfield or thin project** (little or no existing `.claude/` setup): return 5-10. The user needs a menu.
- **Mature project** (existing commands, skills, agents, or rules already cover the obvious work): return 3-7. Padding the list dilutes it.

Pick the mode from the coverage inventory in Step 2. On a mature project, "most of the obvious work is already covered" is a real finding and you should say it. If fewer candidates are possible than the mode suggests, say exactly what limited the scan.

## Workflow

### Step 1 - Understand the project

Read the project's `CLAUDE.md` (or note its absence), list the folder structure, read the file-naming conventions, and sample real files across the main folders. Produce a short plain-English model of what this project produces and what work appears to repeat. Do not skip the sampling. The detection quality depends entirely on actually reading the work, not guessing from folder names.

While reading the home base, note any **stated priority** the project claims about itself: a current focus, a goal, a "what I'm working on right now" line. Quote it. Step 5 scores strategic fit against it, and reading it here costs nothing extra.

Where git history exists, `git log` over the busiest folders is the cheapest frequency evidence you will get. Dated filenames prove work happened; commits prove it is still happening.

If the project has only a few files, still continue. Name the limitation clearly: "This project has limited examples, so several candidates below are exploratory." Then infer possible recurring work from filenames, folder names, templates, plans, examples, repeated sections, or described responsibilities.

**Delegating steps 1 and 2:** when the repo is large enough that reading it would crowd out the reasoning (roughly 50+ content files, or an existing `.claude/` setup with more than a handful of entries), run the evidence pass and the inventory pass as two subagents launched in parallel, using the briefs in `references/subagent-briefs.md`. They do not depend on each other. Do not require named agent files in `.claude/agents/` — this skill must stay transferable as a single folder. If subagents are unavailable, or the repo is small, run both passes yourself. Score in the main thread either way.

### Step 2 - Build the coverage inventory

Do this **before** generating candidates. Knowing what already exists shapes what you look for, and it stops you from spending a whole generation pass on work that is already automated. On a mature repo this step is the majority of the real work.

Read every one of these surfaces. Missing one is how a run ships a duplicate:

1. `.claude/commands/` - names and the first descriptive line of each.
2. `.claude/skills/` - names and `description:` frontmatter of each.
3. `.claude/agents/` - names and descriptions. Easy to forget, and often where the content-generation work already lives.
4. `.claude/rules/` - these do double duty. A rule file proves the work is recurring (signal 6) *and* tells you part of that work is already governed.
5. **Skills installed outside the project** - plugin skills, user-level skills, and anything in the session's available-skills listing. These are invisible in the repo tree but they still cover the work. If you can see a skill listing for this session, read it.
6. `CLAUDE.md` / `AGENTS.md` routing tables - these name workflows that may already be wired up.
7. Hooks in `.claude/settings.json` and any `scripts/` directory - see signal 10 in `references/detection-patterns.md`.

Write a short coverage map: what work is already automated, and by what. Keep it in context for Steps 3 and 4.

If there is no `.claude/` setup at all, say so and note that the project is greenfield. Nothing to dedup against, so propose the foundational set.

### Step 3 - Detect candidates

Walk the signal catalog in `references/detection-patterns.md` against what you found. For each repeated workflow, name it as a concrete task ("turn a brain dump into a polished social note"), not a vague capability ("content help").

Generate a broad first pass, skipping anything the coverage map already shows as fully automated. Aim for 10-15 possibilities on a greenfield project and 6-10 on a mature one. Include strong candidates and useful exploratory candidates. Do not invent tasks unrelated to the project, but do not stop at three ideas just because the evidence is early.

### Step 4 - Dedup and name the gaps

Check each candidate against the coverage map from Step 2. Drop any candidate already fully covered. For candidates *partially* covered, keep them but state the gap in terms of the specific thing that exists ("`/seo-review` runs the review; nothing sequences it with the style check and thumbnail pass").

Two failure modes to watch:

- **Silent duplicate.** A skill outside the project covers the candidate and you never looked. Re-check surface 5 above before finalizing.
- **Fake gap.** You keep a covered candidate by describing the gap so narrowly that it is not worth a skill. If the gap is one prompt line, it is not a gap.

State plainly in your final output which candidates you dropped for coverage and what covered them. That is useful information, not scan overhead.

### Step 5 - Score and rank

Score each surviving candidate against the bar. Rank highest-worthiness first, breaking ties by strategic fit. Use three readiness labels:

- **Build now:** strong evidence, clear output, clear quality standard.
- **Customize first:** likely useful, but needs one or two user preferences before building. You must name the question in the `Needs from you` field.
- **Explore later:** plausible, but thin evidence or unclear quality standard.

Hold the list to the mode's range: 5-10 on a greenfield project, 3-7 on a mature one. A candidate scoring below 5 can appear only to complete a useful menu in thin-project mode, labeled Low confidence or Explore later. In mature mode, cut it.

### Step 6 - Present the list

Output the ranked list in the format below. Every item must show *why it qualifies* and the evidence behind it. Then stop and let the user select. Do not write any files yet.

### Step 7 - Auto-scaffold the selected skills

For each skill the user picks, write a real `.claude/skills/<slug>/SKILL.md` using the template and rules in `references/skill-template.md`. Match the conventions of skills already in this project.

### Step 8 - Verify what you wrote

A generated skill that does not parse, or that never triggers, is worse than no skill: it looks done and fails silently later. Run the verification checklist in `references/skill-template.md` against every file you just wrote, then report the result.

Do not skip this because the file looked right as you wrote it. The checks are mechanical and take one pass.

Fix anything that fails, then re-check. If something cannot be fixed without a decision from the user (usually a slug collision with an existing skill), say so plainly instead of writing a near-miss file and moving on.

Report per skill:

1. The exact path you wrote.
2. Verification result: pass, or what you fixed to make it pass.
3. One concrete first test the user can run to see it work, phrased as the thing they would actually type.
4. The one part most likely to need adjustment after that first test.

## Output contract for the list

Present candidates as a ranked list. Each item uses this shape:

```
N. <Skill name>                        [skill-worthiness: X/10 | confidence: High/Medium/Low | readiness: Build now/Customize first/Explore later]
   Triggers when: <the natural phrase or moment that should fire it>
   Automates: <the repeated task, in one line>
   Evidence found: <2-3 concrete folders, filenames, patterns, or sampled sections that support the idea>
   Why it qualifies: <which signals fired + which scoring criteria it meets>
   Gap: <what no existing command/skill/agent/rule already does, if relevant>
   Needs from you: <required when readiness is Customize first: the one or two decisions that block building>
   Weakest criterion: <required when the score is 5-6: which criterion it lost points on and why>
   Input → Output: <messy input> → <useful output>
```

`Needs from you` and `Weakest criterion` are omitted when they do not apply. Every other field is required.

After the list, add:

1. A short **Already covered** note naming candidates you dropped and what covers them. On a mature project this is often the most useful part of the output.
2. The line: "Tell me which numbers to build and I'll scaffold them."

## Guardrails

- Find new skills only. Never propose improving, merging, or deleting an existing skill. That is out of scope.
- Never auto-write a skill the user did not select.
- Never report a skill as created without running the verification checklist on it. An unparseable or untriggerable skill fails silently weeks later, which is worse than not writing it. If a check fails and you cannot fix it without a decision from the user, say which check failed rather than reporting a pass.
- Never propose a candidate already covered by an existing command, skill, agent, or rule without naming the specific gap. Check skills installed outside the project too, not just `.claude/skills/`.
- Do not present one-off tasks as proven skills. If a task is only inferred from thin evidence, label it exploratory.
- Keep the "why it qualifies" line concrete and tied to evidence you actually found in the project, not generic justification.
- Adapt examples to the project. A content repo gets drafting and repurposing candidates. A consulting folder gets client-prep and proposal candidates. Read what the project is before naming candidates.
- Match the count to the mode: 5-10 on a greenfield project, 3-7 on a mature one. Never manufacture candidates to hit a number. A short, well-evidenced list is the correct output for a repo that is already well automated, and saying so is a finding.
