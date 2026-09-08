# Fresh-Session Test Protocol

Use this protocol when a finding depends on current model behavior or when an approved
change could materially affect recurring work.

## Tier 1: structural check

Run this after every Apply operation. Without starting a new session:

1. Re-read each changed file in full.
2. Confirm every route and import the changed blocks reference still resolves.
3. Confirm protected instructions survived the patch unchanged.
4. Confirm the patch introduced no new duplicate or conflict with a source that loads in
   the same scope.

Report the result as a structural check only. It never supports "behavior improved,"
"the model still complies," or any other behavioral claim. When the user wants speed
over certainty, they may stop here, with the report stating that the behavioral
comparison was not run.

## Tier 2: fresh-session comparison

Required before claiming any behavioral effect and before finalizing removal of an
instruction under a **Test** finding. The rest of this protocol defines it.

## Choose the test

Use one real task the project repeats. Prefer a task that exercises the instruction being
tested. Record:

- the exact prompt
- the input files
- the expected output
- the instruction or behavior under test
- the failure that would require restoring the instruction

Avoid a synthetic prompt written merely to prove the recommendation.

## Control the comparison

Keep these constant:

- Claude model and effort setting
- Claude Code version
- starting project state
- prompt and input files
- permissions
- available Skills, hooks, and tools
- output destination

Use a fresh Claude Code session for each run. `CLAUDE.md` content loaded in the session
that performed the edit is not a clean candidate test.

## Run the baseline

Before changing the instruction:

1. Record the current file state or commit.
2. Start a fresh session.
3. Run the task once.
4. Save the output and any clarification questions.

## Run the candidate

After applying only the approved change:

1. Start another fresh session with the same model and settings.
2. Run the identical task and inputs.
3. Save the output and any clarification questions.

## Compare behavior

Judge only criteria connected to the audited instruction:

- task correctness
- compliance with project-specific requirements
- required output shape
- correct routing to project sources
- unnecessary clarification
- safety and approval behavior

Record **Better**, **Equivalent**, **Worse**, or **Inconclusive** for each relevant
criterion and explain the observable evidence.

One comparison supports a local decision for that task. It does not prove a universal
model improvement.

## Decide

- **Better or Equivalent:** Keep the candidate change and record what was tested.
- **Worse:** Restore the instruction, then consider a narrower rewrite.
- **Inconclusive:** Keep the current instruction or run another representative task.

If the project is version controlled, use its normal diff and restore process. If it is
not, create a sibling backup only after the user approves it. Never delete the baseline
copy until the user accepts the result.
