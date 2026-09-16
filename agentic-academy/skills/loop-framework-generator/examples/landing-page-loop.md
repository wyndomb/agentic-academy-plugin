# Example: Landing Page Improvement Loop

## User Input

I have a landing page that is mostly built. I want Claude to clean up the final 20 percent: CTA clarity, missing proof, placeholders, mobile readability, and broken links.

## Loop Fit Verdict

Loop-ready if the page files or rendered page are available. Mark visual and mobile checks unresolved if Claude cannot inspect the page.

## Generated Prompt

```text
/loop 20m

You are improving an existing landing page.

Read the current page files, offer notes, CTA instructions, proof material, and design or copy rules I provide.

Run one improvement or QA pass per loop tick.

Goal:
Improve the landing page from rough-but-working to ready for human review without changing the offer promise, inventing proof, or adding unsupported claims.

Allowed actions:
- Improve one layer per pass.
- Edit the page only when the issue is clear.
- Mark uncertainty instead of hiding it.
- Keep a loop log after each pass.
- Read the loop log before starting each new pass.
- Do not repeat a completed pass unless the log says the previous pass failed or new issues appeared.
- Stop when the finish checklist passes, the pass cap is reached, or a human decision is needed.

Pass order:
1. Offer clarity: the first screen explains what this is, who it is for, and why it matters.
2. CTA consistency: the page has one primary CTA and the button language is consistent.
3. Section completeness: required sections are present and no section is doing the same job twice.
4. Proof and caveats: claims have proof, context, caveats, or softer wording.
5. Mobile readability: the page is readable on mobile and no important text or buttons are awkwardly placed.
6. Links and placeholders: links work, placeholders are removed, and unfinished copy is flagged.
7. Final QA: produce a final change log and list anything that still needs human judgment.

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
- The first screen clearly explains the offer.
- The page has one primary CTA.
- CTA wording is consistent across the page.
- No placeholders remain.
- Every major claim has proof, context, caveat, or softer wording.
- Required sections are present.
- Links work, or broken links are listed.
- Mobile readability has been checked, or marked unresolved if the page cannot be inspected.
- The final output includes a change log.

Cap:
Stop after seven passes even if the checklist has not fully passed.
If two passes in a row make no meaningful improvement, stop and explain why.

Human gate:
Do not publish, deploy, send, or mark this as final.
Stop and ask for human judgment if:
- Fixing the issue would change the offer promise.
- A claim needs proof the current files do not provide.
- Pricing, guarantee, deadline, or availability is unclear.
- Two CTA directions are both plausible but lead to different reader expectations.
- Visual or mobile QA cannot be completed from the available files.

End by telling me what changed, what passed, what remains unresolved, and what still needs my judgment.
```
