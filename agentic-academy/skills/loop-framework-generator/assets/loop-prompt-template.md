# Loop Prompt Template

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
