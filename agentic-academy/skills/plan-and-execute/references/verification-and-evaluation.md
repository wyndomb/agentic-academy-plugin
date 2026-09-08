# Verification And Evaluation Guide

Use this guide to create evidence-based checks for each milestone. Do not use every method. Choose the smallest set that can show whether the milestone is actually complete.

## Verification Proves That A Requirement Was Met

Use verification to answer: did the deliverable meet the stated acceptance criteria?

| Project type | Useful verification | Evidence to record |
| --- | --- | --- |
| Software or automation | Tests, build, lint, type checks, representative run, diff review | Commands, pass or fail result, output, changed paths |
| Research | Source check, citation review, coverage against questions, fact check | Source links, retrieval dates, unresolved claims |
| Writing or content | Brief check, source check, format check, link check, claim review | Draft path, source list, checklist result |
| Design | Requirements check, rendering or export check, visual review against brief | Export path, screenshots, review note |
| Operations | Dry run, checklist, access check, sample run, outcome audit | Run record, system result, outstanding manual step |
| Strategy or planning | Decision check, dependency review, stakeholder review, scenario check | Decision log, assumptions, questions still open |

If a planned test fails, record the failure. Fix it only if the fix is inside the approved milestone. Rerun the check after the fix.

## Evaluation Judges The Quality Of The Result

Run evaluation after verification. The same agent may evaluate its work, but it must switch from builder to reviewer and judge the output against explicit criteria and evidence.

Use these questions when relevant:

1. **Requirements met:** Does every acceptance criterion have evidence, or is one missing?
2. **Correctness:** Does the output behave, state, or claim what it should? Were important edge cases checked?
3. **Quality and usability:** Is the result clear, coherent, complete enough for its intended user, and usable without hidden knowledge?
4. **Scope and safety:** Did the work stay inside the approved plan? Did it avoid unapproved external or irreversible actions?
5. **Maintainability:** Can a future user or agent understand, rerun, or update the result?

Add domain-specific criteria when the project needs them. For example: factual accuracy for research, voice for writing, accessibility for a public interface, or security for software.

## Report Honest Results

Use one of these states for each check or evaluation criterion:

- **Pass:** Evidence supports the requirement or criterion.
- **Needs changes:** The evidence shows a problem that needs correction.
- **Not assessed:** A needed check could not be run or requires human judgment.

Do not mark a milestone complete if a required result is `needs changes` or `not assessed`. Use `needs review` when human judgment is the only remaining requirement. Use `blocked` when work cannot continue without a user decision, access, or source material.
