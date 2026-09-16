# Example: Brief Or Spec Hardening Loop

## User Input

I have a rough project brief. I want Claude to harden it so another person or agent can act from it without guessing what I meant.

## Loop Fit Verdict

Loop-ready if the rough brief exists. The loop should surface ambiguity and missing decisions instead of silently resolving them.

## Generated Prompt

```text
/loop 20m

You are hardening an existing brief or spec so another person or agent can act from it without guessing what was meant.

Read the current brief, source notes, project goals, constraints, and any style or format rules I provide.

Run one hardening pass per loop tick.

Goal:
Improve the brief until it is clear, checkable, and ready for human review without inventing decisions, evidence, or requirements.

Allowed actions:
- Improve one layer per pass.
- Edit the brief only when the issue is clear.
- Mark uncertainty instead of hiding it.
- Keep a loop log after each pass.
- Read the loop log before starting each new pass.
- Do not repeat a completed pass unless the log says the previous pass failed or new issues appeared.
- Stop when the handoff checklist passes, the pass cap is reached, or a human decision is needed.

Pass order:
1. Ambiguity: find places a reader could interpret the brief two different ways.
2. Missing decisions: list choices the owner still needs to make.
3. Evidence: mark claims as sourced, assumption, unsupported, or needs example.
4. Acceptance criteria: turn vague requirements into checkable conditions.
5. Next action: make sure the next person knows what to do first.
6. Caveats and risks: name limits, risks, dependencies, and open questions.
7. Final handoff: produce the cleaned brief plus unresolved decisions.

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
- No important section can be read two ways without an open question.
- Every major claim is sourced, marked as an assumption, softened, or flagged.
- Every requirement has acceptance criteria or is marked as unresolved.
- Missing decisions are listed instead of silently filled in.
- The next action is clear.
- Risks, caveats, and dependencies are named.
- The final output includes a change log and unresolved decision list.

Cap:
Stop after seven passes even if the checklist has not fully passed.
If two passes in a row make no meaningful improvement, stop and explain why.

Human gate:
Do not mark the brief as final or ready to hand off.
Stop and ask for human judgment if:
- A decision is missing and cannot be inferred from the source material.
- Two interpretations are both plausible.
- A claim needs evidence the current files do not provide.
- A requirement depends on priority, budget, timing, or audience.
- The brief needs a new example, constraint, or tradeoff from the owner.

End by telling me what changed, what passed, what remains unresolved, and what still needs my judgment.
```
