---
name: plan-and-execute
description: >-
  Create, approve, and run a detailed multi-session project plan with a human. Use when a user
  wants to turn a substantial coding, research, content, operations, or build project into an
  interview-led plan.md and progress.md; resume work from those files; complete one milestone at a
  time; verify work; and run a structured self-evaluation before reporting results. Also use when
  the user says "plan this out", "let's build this properly", "resume my plan", or "where did we
  leave off".
---

# Plan And Execute

Use this skill to make a long project survivable across sessions without losing the user's intent or claiming work is complete without evidence.

Create two project files in the project root unless the user names another location:

1. `plan.md` is the approved source of truth for the goal, scope, milestones, acceptance criteria, and checks.
2. `progress.md` is the running record of execution, evidence, decisions, blockers, and self-evaluation results.

Keep the plan stable. Record execution in `progress.md`. Never silently change the plan to make unfinished work look complete.

## Choose The Mode

Start by identifying the state of the project.

1. **New project:** Interview the user, draft both files, and wait for explicit approval of `plan.md`.
2. **Plan revision:** Read both files, identify the requested change, revise the plan, and ask for approval again before executing work affected by the change.
3. **Approved plan execution:** Read both files, complete only the next planned milestone, verify it, evaluate it, update the files, and stop.
4. **Resume:** Read both files before making any claim or taking any action. Reconstruct the current milestone from the files, not chat history.

If `plan.md` exists but does not show explicit human approval, treat it as a draft. Do not execute the project.

## Size The Project First

Before interviewing, triage the project:

1. **Quick:** it fits in one sitting, the stakes are low, and redoing it would be cheap. Say so plainly, skip the planning files, and offer to just do the work now.
2. **Standard:** it spans multiple sessions, getting it wrong is expensive, or "done" is hard to state in one sentence. Run the full interview and create both files.

If the user still wants a plan for a quick task, proceed, but keep it to two or three milestones.

For standard projects, ask about appetite early: how much time is this project worth, and is it still worth doing if it takes longer than that? Record the answer under Constraints in `plan.md` and shape the milestone count to fit it.

## Interview Before Planning

Ask focused questions in small groups. Do not interrogate the user for details already supplied.

Two disciplines govern how you ask:

1. **Push once for the concrete version.** Treat a vague answer ("make it good," "for my audience," "soon") as the polished version, not the real one. Ask once more for specifics, which reader, which file, what number, by when, then move on.
2. **Take a position.** When an answer, a milestone order, or a scope choice looks wrong, say so and propose a better option with your reasoning. A planning partner who disagrees out loud is more useful than a transcriber. Never respond with only "that could work."

Get enough information to write a plan that another agent can execute without guessing:

1. The outcome: What must exist or be true when the project is done?
2. The user and use case: Who will use it, and what real problem should it solve?
3. Deliverables: Which files, systems, decisions, or external outcomes are expected?
4. Scope: What is included, explicitly excluded, fixed, or still undecided?
5. Source material: What files, examples, systems, constraints, or instructions must the agent use?
6. Success: What would make the user say the result is right? What should be tested, checked, or reviewed?
7. Execution: What milestones make sense, and what dependencies exist? Then run a short pre-mortem: imagine the project failed or got abandoned, what went wrong? Turn the answers into named guardrails in the plan.
8. Boundaries: Which decisions, external actions, spending, deletions, publishing steps, or scope changes require the user's permission?

If an answer is missing and it could materially change the plan, ask the user. Put smaller unknowns in an `Open questions` section. Do not invent requirements to make a plan look complete.

When the information is sufficient, briefly restate the project in plain language before writing the files.

## Draft The Plan

Use `assets/plan-template.md` as the starting structure. Use `assets/progress-template.md` to create the matching progress record. Adapt the fields to the project, but do not remove the approval, milestone, verification, evaluation, decision, or handoff sections.

Write each item in the Excluded section as an explicit negative constraint the executing agent can check its own work against, not just a list of omissions.

Build milestones around meaningful, independently checkable outcomes. Each milestone must have:

1. A clear outcome and the files or systems it changes.
2. A bounded task list in execution order.
3. Dependencies and required user decisions.
4. Acceptance criteria that describe what must be true.
5. A verification method and the evidence it should produce.
6. A structured self-evaluation rubric appropriate to the work.
7. A stop condition. One completed milestone is the default maximum for a session.

Use `references/verification-and-evaluation.md` to choose checks and evaluation criteria that fit the work.

After creating the draft, summarize the milestones and ask the user to approve `plan.md`. Do not begin setup, implementation, research, or any other project work until they explicitly approve it.

## Offer A Review Before Approval

When presenting the draft plan, offer to stress-test it with reviewer lenses before approval. The lenses are defined in `references/review-lenses.md`: The Skeptic, The Customer, The Blindspot Finder, and The Optimist.

Recommend, do not run everything. Read the plan and suggest the lenses that fit, two by default:

1. Public-facing or revenue work (a launch, sales assets, publishing): The Customer and The Skeptic.
2. Unfamiliar territory or a first attempt at this kind of project: The Blindspot Finder and The Skeptic.
3. Internal or operations work: The Skeptic alone.
4. A large plan, long appetite, or expensive failure: all four.

The user chooses the lenses or skips review entirely. Skipping is a valid choice for smaller plans.

Run each chosen lens as a separate subagent with a fresh context. Give it only the contents of `plan.md` and its lens instructions from `references/review-lenses.md`, never the planning conversation. The reviewer not knowing what was discussed is what makes it honest. If subagents are unavailable, run the lenses one at a time against `plan.md` alone and tell the user the result is weaker.

Then synthesize. Never forward raw reviews:

1. Merge duplicate findings across lenses.
2. Translate each surviving finding into either a concrete plan edit (split a milestone, fix an uncheckable criterion, add a missing dependency) or a named risk to accept as-is.
3. Present one short list of proposed edits and accepted risks. Apply only the edits the user approves.

One round only: review, revise, approve. Do not offer to re-review the revision. Record which lenses ran and what changed in the approval log entry.

## Execute An Approved Milestone

At the beginning of every execution session:

1. Read `plan.md` and `progress.md` in full.
2. Confirm that the plan is approved and identify the next incomplete milestone.
3. Check that its dependencies, source material, and required access are available.
4. Ask the user before proceeding if a required decision, missing input, or change in scope blocks accurate work.

Then execute only the next milestone. Follow its task order and acceptance criteria. Keep useful evidence as you work: changed file paths, commands and results, links, screenshots, source references, or a concise manual-check note.

The Excluded list is active during execution, not just documentation. If the work starts drifting toward an excluded item, stop and ask: amend the plan to include it, or skip it. Never build it quietly.

Do not start a second milestone in the same session, even if the first one finishes quickly. Update the records, report the result, and let the user decide when to continue.

## Verify And Evaluate Before Reporting

Do not call a task complete because the output looks plausible.

Before reporting a milestone as complete:

1. Run every planned check that is available and record the result.
2. Compare the output against every acceptance criterion.
3. Perform a separate self-review pass using the milestone's evaluation rubric.
4. Fix issues that are inside the approved scope, then rerun the affected checks.
5. Mark the milestone complete only when all required checks and evaluation criteria pass.

If a check cannot run, an evaluation criterion cannot be assessed, or the work still needs human judgment, say so plainly. Mark the milestone `blocked` or `needs review`, record why, and ask the user for the next decision. Never replace evidence with confidence.

## Keep The Files Current

After each milestone, update both files:

1. In `plan.md`, update only the project status, task or milestone state, and approved amendment log.
2. In `progress.md`, add the session record, evidence, verification results, evaluation results, blockers, decisions needed, and the exact next handoff.

Use status words consistently: `not started`, `in progress`, `blocked`, `needs review`, and `complete`.

## Protect The User's Control

Pause and ask the user before:

1. Changing the goal, deliverables, success criteria, milestone order, or scope.
2. Making an assumption that could change the result.
3. Deleting, overwriting, publishing, sending, spending money, changing production systems, or taking another consequential external action.
4. Starting work that belongs to a later milestone.

When the user approves a change, add it to the plan amendment log with the reason, date, and affected milestone. Then update the progress record.

## Completion Standard

The project is complete only when every required milestone is complete, the final checks and evaluation pass, all known limitations are documented, and the user has the information needed to review or use the result.

End each response with:

1. The milestone status.
2. What changed.
3. Verification and evaluation results.
4. Any remaining risk, limitation, or user decision.
5. The one next milestone or handoff.
