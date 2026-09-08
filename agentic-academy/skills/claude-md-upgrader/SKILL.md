---
name: claude-md-upgrader
description: >-
  Reviews a knowledge-work project and recommends 5-10 practical ways to improve its CLAUDE.md,
  AGENTS.md, rules files, or skills. Can also build a first CLAUDE.md from scratch or patch
  selected improvements after the user chooses. Project-state-driven: it works from real files,
  not from a chat session. Use this WHENEVER the user says "build my CLAUDE.md", "set up my
  project home base", "I don't have a CLAUDE.md", "improve my CLAUDE.md", "audit my project home
  base", "is my CLAUDE.md any good", "improve my AGENTS.md", or hands over a project and wants a
  home base Claude or Codex can read. Written for knowledge work (content, consulting, founders,
  analysts), not for codebases. It does NOT mine the current chat session for learnings, and it
  does NOT find new skills (use skill-finder for that).
---

# CLAUDE.md Upgrader

A project's `CLAUDE.md` or `AGENTS.md` is its home base: the file that decides whether an agent acts like a blank chatbot or like something that actually understands the work. Most people either have no home base, or have a thin one full of nice-sounding lines that never change what the agent does.

This skill fixes both. It reads what the project actually contains, recommends the highest-value upgrades, then builds or patches only after the user chooses what to apply.

It is **project-state-driven**. It works from the real files in the project, not from the current chat. If the user wants to fold learnings from this conversation into the home base, that is a different job (`revise-claude-md`). If they want to find new skills to build, that is `skill-finder`.

## The three modes

The default mode is RECOMMEND. BUILD and PATCH happen when the user asks for them or approves specific recommendations.

- **RECOMMEND mode.** Read the project, inspect `CLAUDE.md` and `AGENTS.md` if present, then return 5-10 ranked upgrade ideas. Do not edit yet. This is the default for `/agentic-academy:claude-md-upgrader`, "review my CLAUDE.md", "audit my home base", or "how can I improve this?"
- **BUILD mode.** If the user explicitly asks to build a first home base, or approves the recommendation to create one, read the project, ask only the few things you cannot infer, and write a first `CLAUDE.md`.
- **PATCH mode.** If the user picks recommendations to apply, make targeted edits to `CLAUDE.md`, `AGENTS.md`, rules files, or skill files. Patch only the selected items.

## The target structure

A knowledge-work home base has six parts. The full definition of each part, what strong vs thin looks like, the per-archetype variations, and the audit checklist all live in `references/home-base-structure.md`. Read it before building or auditing.

The six parts in short:

1. Project overview (what this is, in plain language)
2. Who the work serves (the real audience or client)
3. What the person is trying to grow or improve (the goal the work serves)
4. Five critical rules (hard, checkable rules Claude must never break)
5. Three decision rules (when to ask vs move, and the defaults)
6. Key files (the short list of what to read for which task)

When both `CLAUDE.md` and `AGENTS.md` exist, audit them together. Shared project truth can appear in both if needed, but tool-specific behavior belongs in the file for that tool. Flag contradictions, stale duplication, missing routing, and places where one file should point to the other.

## Respect what already works

The single most important judgment in this skill: **do not impose the beginner structure on a home base that has outgrown it.** A mature project may have a router-style `CLAUDE.md` or `AGENTS.md` that points to other files instead of holding everything inline. That is correct, not a flaw. When you meet a strong home base, behave like an auditor. Find genuine staleness and gaps. Do not flatten it back to the six-part starter. The maturity ladder in the reference tells you how to treat empty, beginner, working, and mature home bases differently.

## Workflow

### Step 1: Detect files and mode

Check for these at the project root:

- `CLAUDE.md`
- `AGENTS.md`
- `.claude/rules/`
- `.claude/skills/`
- `.claude/commands/`
- other obvious instruction, rules, prompt, template, or process files

Say which mode you are in before continuing. Default to RECOMMEND unless the user explicitly asked to build or patch.

### Step 2: Scan the project

Use a consistent scan so the recommendations come from evidence:

1. Map the root files and top-level folders.
2. Read any existing `CLAUDE.md`, `AGENTS.md`, rules, command, skill, prompt, or template files.
3. Sample 3-5 representative project files across the main folders.
4. Identify recurring output types, repeated processes, file naming patterns, and current routing.
5. Check for stale references, missing files, contradictions, vague rules, and duplicated instructions.
6. Detect the likely archetype: content creator, coach or consultant, entrepreneur, or knowledge worker.

### Step 3 (RECOMMEND): Return 5-10 upgrade ideas

Audit the current setup against the six-part structure, the actual project, and the user's likely work. Return 5-10 ideas ranked by expected usefulness. Each idea must include:

- Impact: High, Medium, or Low
- Put it in: `CLAUDE.md`, `AGENTS.md`, rules file, command, skill, or another named file
- Why it matters
- Evidence from the project
- Effort: Low, Medium, or High
- Expected improvement

End with a beginner-friendly "Best first move" and ask which recommendations to apply.

### Step 4 (BUILD): Ask only what you cannot infer

Some parts cannot be read off the files: who exactly the work serves, what the person is trying to grow, and which mistakes are hard rules. Ask a short focused interview for only those gaps. Ask no more than 5 questions, fewer if the files already answer them. Do not interview about anything you can infer yourself.

### Step 5 (BUILD): Draft and save the home base

Write the home base against the six-part structure using `references/build-template.md`. Fill every section from what you learned. Leave no placeholders. Keep it a router if the project is large (point to other files); keep it inline and simple if the project is small. Save as `CLAUDE.md` at the project root and tell the user what you wrote.

### Step 6 (PATCH): Apply selected recommendations

Make targeted edits that fix only the recommendations the user approved. Preserve the person's voice, decisions, and any working router structure. Confirm before any change large enough to reshape the original argument. Prefer the smallest set of edits that fixes the real problems.

### Step 7: Suggest a before and after test

After BUILD or PATCH mode, suggest one small task the user can run before and after the upgrade. The test should connect to the project's real work, such as a draft, brief, report, client follow-up, decision memo, or stakeholder update. Keep it simple enough that a non-technical user can judge whether the output improved.

## Output contracts

**RECOMMEND mode** produces a ranked list before any edit, in this shape:

```markdown
HOME BASE UPGRADE IDEAS - <project name>   [maturity: empty | beginner | working | mature]

Detected project type: <content creator | coach or consultant | entrepreneur | knowledge worker | mixed>
Files reviewed: <short list of the files/folders that mattered>

Top upgrade ideas:

1. <idea>
   Impact: <High | Medium | Low>
   Put it in: <CLAUDE.md | AGENTS.md | rules file | command | skill | other file>
   Why it matters: <behavior this changes>
   Evidence: <file, folder, pattern, or contradiction that triggered this>
   Effort: <Low | Medium | High>
   Expected improvement: <what should get better>

Best first move:
<one recommendation>

Tell me which numbers to apply and I'll patch only those.
```

**BUILD mode** produces a saved `CLAUDE.md` plus a short note: what archetype you detected, what you inferred vs what the user told you, and one suggested next step. Usually, that next step is to run `skill-finder` to find skills for this project now that the home base exists.

**PATCH mode** produces a change summary plus a before and after test:

```
Applied:
- <selected recommendation> -> <file changed>

Left alone:
- <recommendations not selected or strong parts preserved>

Before and after test:
<one small task to rerun so the user can compare quality>
```

## Guardrails

- Project-state-driven only. Never mine the current chat session for content. Point to `revise-claude-md` if the user wants that.
- Never downgrade a mature, router-style home base into the beginner six-part starter.
- In RECOMMEND mode, do not edit. In PATCH mode, edit only what the user selected.
- Build the home base to change behavior, not to sound complete. Every rule must be checkable. Cut lines that read as nice but tell Claude nothing.
- Adapt to the archetype. A content repo's rules are about voice and tier. A consulting folder's rules are about client boundaries and deliverable standards. Read what the project is first.
- Keep routing in the home base and depth in the files it points to. Do not pull everything inline just to look thorough.
- When both `CLAUDE.md` and `AGENTS.md` exist, prevent drift. Flag contradiction and duplication instead of copying everything into both files.
