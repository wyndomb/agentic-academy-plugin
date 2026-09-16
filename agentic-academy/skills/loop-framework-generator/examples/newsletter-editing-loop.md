# Example: Newsletter Editing Loop

## User Input

I have an 80 percent newsletter draft. I want Claude to improve it in passes without changing the core argument or making it sound too polished.

## Loop Fit Verdict

Loop-ready. The artifact already exists, the improvement can be checked in passes, and the final call still belongs to the author.

## Generated Prompt

```text
/loop 20m

You are improving an existing newsletter draft.

Read the current draft, outline, and style rules I provide.

Run one editing pass per loop tick.

Goal:
Improve the draft from 80 percent to publishable without changing the core argument or replacing the author's voice.

Allowed actions:
- Improve one layer per pass.
- Edit the draft only when the issue is clear.
- Mark uncertainty instead of hiding it.
- Keep a loop log after each pass.
- Read the loop log before starting each new pass.
- Do not repeat a completed pass unless the log says the previous pass failed or new issues appeared.
- Stop when the finish checklist passes, the pass cap is reached, or a human decision is needed.

Pass order:
1. Structure: every section has one job.
2. Redundancy: no two sections repeat the same point.
3. Argument: every section moves the core idea forward.
4. Evidence: claims have examples, caveats, sources, or softer wording.
5. Voice: remove language that sounds too polished, too certain, or too generic.
6. Rules: remove banned punctuation, banned phrases, unsupported metrics, and style-rule violations.
7. Finish: produce a final change log and list anything that still needs human judgment.

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
- The draft keeps the original argument.
- No two sections do the same job.
- No repeated claim appears in adjacent sections.
- Every major claim has an example, caveat, source, or softer wording.
- The draft follows the style rules.
- The final output includes a change log.

Cap:
Stop after seven passes even if the checklist has not fully passed.
If two passes in a row make no meaningful improvement, stop and explain why.

Human gate:
Do not publish, send, or mark this as final.
Stop and ask for human judgment if:
- Fixing the issue would change the core argument.
- Two possible edits are both valid but lead to different meanings.
- A claim needs evidence the current files do not provide.
- The draft needs a new example, story, or opinion from the author.

End by telling me what changed, what passed, what remains unresolved, and what still needs my judgment.
```
