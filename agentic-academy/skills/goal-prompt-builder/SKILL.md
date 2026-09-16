---
name: goal-prompt-builder
description: Interview users and generate ready-to-run goal prompts for long-running AI agent tasks. Use when the user wants help writing a /goal, goal condition, completion criteria, finish line, autonomous agent task, end-to-end agent delegation prompt, or a prompt that makes Claude Code, Codex, or another AI agent work, check, fix, and stop cleanly without babysitting.
---

# Goal Prompt Builder

Create a finishable agent goal by interviewing the user, then outputting one ready-to-run goal prompt.

Use this skill for long-running tasks where the agent must work across multiple steps, check progress, repair failures, and report completion or blockers. Do not use it for one-shot prompts, tiny edits, or tasks where the user only wants general advice.

## Output Contract

- First ask only the missing interview questions needed to write the goal.
- Ask no more than 7 questions at once. Prefer 4-6.
- If the user already gave enough detail, skip the interview and generate the goal prompt.
- The final answer must contain only the ready-to-run goal prompt in a fenced `text` block, unless the user asks for explanation.
- Do not add a checklist, planning doc, task board, commentary, or implementation steps to the final output.
- Make the prompt tool-agnostic by default. Use `/goal` only when the user says the target tool supports it or asks for a slash-goal prompt.

## Interview Workflow

Build the goal around six parts:

1. Outcome: what should be true when the work is finished.
2. Proof: what evidence the agent must surface before calling the work done.
3. Guardrails: what must not change, break, invent, or overwrite.
4. Boundaries: what files, tools, sources, folders, accounts, or connectors the agent may use.
5. Next-move rule: what to do after a failed check.
6. Stop clause: when to stop and report instead of grinding.

Ask questions in this order, skipping anything the user already answered:

1. "What is the exact task and final output you want?"
2. "What inputs should the agent use, and where should the outputs go?"
3. "What proof should the agent show before it says the job is done?"
4. "What should the agent avoid changing, inventing, deleting, or touching?"
5. "Which sources, files, tools, folders, or connectors are allowed?"
6. "If a check fails, what should the agent try next?"
7. "When should the agent stop and report a blocker?"

If the user is vague, help make the finish line concrete. Prefer counts, file paths, source lists, row counts, render checks, output folders, completion tables, and explicit "unverified" handling over abstract quality language.

## Goal Prompt Shape

Use this structure for the final prompt:

```text
[optional /goal] [Outcome in one concise paragraph]

The work is done when:
- [Proof item]
- [Proof item]
- [Proof item]

Do not:
- [Guardrail]
- [Guardrail]

Only use or touch:
- [Boundary]
- [Boundary]

If a check fails:
- [Next-move rule]
- [Next-move rule]

Stop when:
- [Stop clause]
- [Stop clause]
```

Use natural wording when the task needs it, but keep all six sections present unless the user explicitly asks for a shorter prompt.

## Quality Rules

- Build the finish line from evidence, not assertion.
- Replace "do a good job," "make it better," "organize this," or "finish everything" with observable outputs.
- For batch work, include source count, output count, skipped items, failed items, and a completion table.
- For research, require source links and mark unverifiable claims instead of guessing.
- For writing or repurposing, require source tags, platform labels, output counts, and format checks.
- For landing pages or built artifacts, require the file to exist, render checks, required sections, and unresolved issues.
- For file operations, protect source files and name allowed folders clearly.
- For current facts, require the agent to verify with reliable sources.
- For metrics, require provided numbers or bracketed placeholders. Never instruct the agent to invent metrics.

## Common Goal Types

Use these patterns when relevant:

- Company research from a sheet: finish line is every source company having one completed output row with source links and unverifiable fields flagged.
- Landing page build: finish line is a real rendered file with required sections, honest metrics, benefit-led CTA, and browser check.
- Repurposing batch: finish line is an empty queue with exact outputs per source, platform rules followed, and source tags attached.
- Inbox or task cleanup: finish line is all allowed items classified or updated, judgment-needed items separated, and no sends/deletes unless explicitly allowed.
- Code or artifact repair: finish line is passing checks, changed files reported, regressions protected, and repeated failures stopped with blocker details.

For full worked examples, read `references/goal-examples.md` only when the user asks for examples or when adapting one of those exact patterns.
