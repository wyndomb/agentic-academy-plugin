---
name: loop-framework-generator
description: Interview the user and generate safe ready-to-run /loop prompts for improving existing artifacts such as drafts, landing pages, briefs, specs, research notes, SEO drafts, SOPs, proposals, and other knowledge-work outputs. Use when the user wants to design a Claude /loop workflow, turn "make this better" into checkable passes, decide whether a task is loop-ready, create a loop checker, set pass caps, add loop logs, define stop rules, or build a prompt that repeatedly improves an artifact without drifting away from human judgment.
---

# Loop Framework Generator

Turn a vague improvement request into a loop framework with an artifact, checker, cap, loop log, and human gate.

The skill should protect the user from weak loops. If the task is too early, too vague, or missing a real artifact, recommend a normal prompt or a `/goal` prompt (built with `/agentic-academy:goal-prompt-builder`) before generating a `/loop` prompt.

## Output Contract

This skill runs in two steps. Do not collapse them into one.

**Step 1, Intake.** Ask the required intake questions (see Intake Floor). Never skip straight to a generated prompt on a vague request. This is the point of the skill: the details live in the user's head, not in the artifact.

**Step 2, Generate.** Only after the user answers, produce:

1. Loop fit verdict
2. Ready-to-run `/loop` prompt
3. Human review notes

If the user explicitly asks for only the prompt, still run the intake, then return only the fenced prompt.

Keep the final prompt runnable. Do not return a strategy essay.

## Intake Floor

Always ask these three questions before generating a prompt, unless the user already answered them in their message. Do not skip them because the artifact "looks self-explanatory" or because you have background context on the user. The artifact tells you what exists. It does not tell you what the user wants changed, and that is the one thing you cannot guess.

1. **Intent:** What is the actual problem you want fixed? (Not converting, reads generic, weak section, just a polish pass, etc.)
2. **Source of truth:** Which file, URL, or note is the artifact, and are there other sources the loop should read?
3. **Off-limits:** Anything the loop must not touch, change, invent, or publish? (Pricing, claims, numbers, specific sections, live actions.)

Rules for the intake:

- Keep it short. Three questions is the floor and the default. Add more only if the answers reveal a genuine gap.
- If the user already answered one of the three in their opening message, do not re-ask it. Acknowledge what you have and ask only what is missing.
- If the user answers "I don't know" to intent, do not proceed. That means the task is not loop-ready yet (see Loop Fit Verdict) and they need a normal prompt first.
- When the user is unsure about a question, offer 2-4 concrete options rather than asking them to invent the answer.

After intake, reflect back the intent in one line before generating: "Building a loop to [intent], reading [source], never touching [off-limits]." Then generate.

## Interview Workflow

The Intake Floor above is required. The inputs below are the fuller set the loop prompt needs. Fill any the intake did not surface from the artifact patterns or by asking, but never let this longer list become an excuse to interrogate the user. Ask no more than 7 questions at once.

Collect these inputs:

1. Artifact: what already exists and where it lives.
2. Current state: rough first version, 60 percent, 80 percent, almost done, or unclear.
3. Desired improvement: what better should mean.
4. Allowed sources: files, notes, pages, data, screenshots, docs, or URLs the loop can read.
5. Allowed edits: what the loop may change.
6. Protected areas: what the loop must not change, invent, delete, publish, send, deploy, or mark final.
7. Checker: observable conditions that prove each pass helped.
8. Pass order: 5-7 improvement or QA passes.
9. Cap: max passes, max time, max token budget, or no-progress stop rule.
10. Human gate: decisions that must come back to the user.
11. Final report: what the loop should report at the end.

If the user is unsure, offer 2-4 concrete suggestions rather than asking them to invent the answer from scratch.

## Loop Fit Verdict

Before generating a prompt, classify the request:

- `Loop-ready`: an artifact exists, improvement can be checked, and there is a clear stop rule.
- `Use /goal first`: the user wants an end-to-end build with a verifiable finish line, not repeated timed passes. Hand off to `/agentic-academy:goal-prompt-builder`.
- `Use a normal prompt first`: the user is still exploring the idea, audience, argument, offer, or direction.
- `Needs human decision`: the next step depends on judgment, missing evidence, approval, or a choice the agent should not make.

Reject weak loop tasks plainly. Do not generate a `/loop` prompt for:

- Blank-page strategy.
- A draft where the core point is unknown.
- Creative work with no checkable criteria.
- Long unattended runs with unclear cost.
- Tasks where the next step is an owner decision.
- Anything that requires publishing, sending, deploying, purchasing, deleting, or changing live data without explicit approval.

When rejecting, give the smallest useful next prompt instead.

## Using The Artifact Patterns

`references/artifact-patterns.md` holds default pass orders, checkers, and human gates by artifact type. Treat these as a **starting point you present to the user, not a template you fill in silently.**

The difference matters. Applying the template silently is what turns this skill into a guess-generator. Presenting it turns the template into a conversation starter.

After intake, when the user is unsure about pass order or checks, show them the default and invite edits:

- "Here's the default pass order I'd run for a landing page: offer clarity, CTA consistency, section completeness, proof, mobile readability, links, final QA. Want to add, drop, or reorder anything based on the problem you described?"

Default patterns available:

- Newsletter draft: structure, redundancy, argument, evidence, voice, rules, finish.
- Landing page: offer clarity, CTA consistency, section completeness, proof, mobile readability, links/placeholders, final QA.
- Brief or spec: ambiguity, missing decisions, evidence, acceptance criteria, next action, risks, final handoff.

Never let the existence of a complete template be the reason you skip asking. The template covers loop mechanics. It does not cover the user's intent.

## Required Prompt Shape

Every generated `/loop` prompt must include:

1. `/loop [interval]`
2. Role and artifact statement.
3. Source material to read.
4. Goal.
5. Allowed actions.
6. Pass order.
7. Loop state.
8. Checker.
9. Cap.
10. Human gate.
11. Final report instruction.

Use 20 minutes as the default interval unless the user gives another interval. Use 5-10 minutes for short checks and 30-60 minutes for heavier research, QA, or code-adjacent work.

## Loop State Requirements

Always include loop state. This is what makes the prompt a loop instead of a repeated prompt.

Require the agent to update a loop log after each pass with:

- Pass number
- Pass type completed
- Files changed
- Main issue found
- Change made
- Checker result
- Remaining issue, if any
- Next recommended pass
- Stop reason, if stopping

Require the agent to read the loop log before each new pass, continue with the next unfinished pass, avoid repeating completed passes unless there is a clear reason, and stop if two passes in a row make no meaningful improvement.

## Human Gate Requirements

Always include a human gate. Customize it to the artifact.

Common human-gate triggers:

- The fix would change the core argument, offer, requirement, or meaning.
- Two valid edits lead to different reader or user expectations.
- A claim needs evidence the available sources do not provide.
- Pricing, guarantee, deadline, availability, priority, budget, or scope is unclear.
- The artifact needs a new example, story, opinion, constraint, or tradeoff from the owner.
- The agent cannot inspect something it is being asked to verify.

## Final Prompt Template

Use this shape, adapting it to the user's artifact:

```text
/loop [interval]

You are improving [existing artifact].

Read [allowed sources].

Run one [improvement/checking] pass per loop tick.

Goal:
[Specific outcome without changing protected areas.]

Allowed actions:
- Improve one layer per pass.
- Edit only when the issue is clear.
- Mark uncertainty instead of hiding it.
- Keep a loop log after each pass.
- Read the loop log before starting each new pass.
- Do not repeat a completed pass unless the log says the previous pass failed or new issues appeared.
- Stop when the checklist passes, the pass cap is reached, or a human decision is needed.

Pass order:
1. [Pass]
2. [Pass]
3. [Pass]
4. [Pass]
5. [Pass]
6. [Pass]
7. [Pass]

Loop state:
After each pass, update a short loop log with:
- Pass number
- Pass type completed
- Files changed
- Main issue found
- Change made
- Checker result
- Remaining issue, if any
- Next recommended pass
- Stop reason, if stopping

Before starting each new pass:
- Read the loop log first.
- Continue with the next unfinished pass.
- Do not repeat a pass unless there is a clear reason.
- If two passes in a row make no meaningful improvement, stop and explain why.
- If the next step requires human judgment, stop and ask for it.

Checker:
- [Observable check]
- [Observable check]
- [Observable check]
- [Observable check]
- The final output includes a change log.

Cap:
Stop after [number] passes even if the checklist has not fully passed.
If two passes in a row make no meaningful improvement, stop and explain why.

Human gate:
Do not [publish/send/deploy/delete/mark final].
Stop and ask for human judgment if:
- [Decision trigger]
- [Decision trigger]
- [Decision trigger]

End by telling me what changed, what passed, what remains unresolved, and what still needs my judgment.
```

## Quality Gate

Before returning the final answer, verify:

- The three intake questions were asked, or the user already answered them in their message. Never generate a prompt on a vague request without asking.
- The intent was reflected back in one line before generating.
- A real artifact exists or the verdict explains why `/loop` is premature.
- The checker uses observable conditions, not "make it good."
- The cap includes a pass limit and no-progress stop rule.
- The human gate protects judgment and live actions.
- The prompt includes loop state and a final report.
- The prompt does not ask the agent to invent proof, metrics, sources, pricing, claims, or facts.
