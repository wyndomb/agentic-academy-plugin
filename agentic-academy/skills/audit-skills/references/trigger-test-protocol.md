# Trigger Test Protocol

Use this protocol when a finding depends on how the current model routes requests, or
when an approved change could materially affect which Skill wins recurring work.

## Tier 1: structural check

Run this after every Apply operation. Without starting a new session:

1. Re-read each changed SKILL.md in full and confirm the frontmatter parses.
2. Confirm every bundled reference and project path the changed Skill names still
   resolves.
3. Confirm protected Skill boundaries survived the patch unchanged.
4. Re-read the descriptions of every neighbor in the changed Skill's trigger map and
   confirm the patch introduced no new plausible collision.

Report the result as a structural check only. It never supports "routing improved,"
"the Skill now triggers correctly," or any other behavioral claim. When the user
wants speed over certainty, they may stop here, with the report stating that trigger
tests were not run.

## Tier 2: fresh-session trigger comparison

Required before claiming any routing effect, before finalizing a **Test** finding,
and before archiving a Skill whose removal rests on the claim that another route now
covers its work. The rest of this protocol defines it.

## Why fresh sessions

The session that ran the audit has the audit itself in context: the trigger map, the
descriptions, the reasoning. Asking that session whether a Skill triggers proves
nothing about a cold start. Every test run must be a fresh session that knows only
what a normal session knows.

## Write the prompts

For each Skill under test, write three groups of prompts:

- **Positive:** requests the Skill should win. Vary the phrasing; include at least one
  that does not use the Skill's name or signature vocabulary.
- **Negative:** nearby requests the Skill should miss. The valuable negatives are
  near-misses that share vocabulary with the Skill but belong elsewhere. Obviously
  unrelated prompts test nothing.
- **Competing:** requests a specific neighboring Skill should win. Name the expected
  winner before running.

Make every prompt realistic and substantive, the kind of request the owner actually
types, with concrete details. Trivial one-step prompts are poor tests: a model can
reasonably handle them directly without consulting any Skill, so a miss on a trivial
prompt is not evidence of a routing problem.

Record each prompt with its expected outcome before running anything.

## Control the comparison

Keep these constant across baseline and candidate runs:

- Claude model and effort setting
- Claude Code version
- project state, apart from the change under test
- the prompt set
- permissions and available tools
- the set of other Skills present

Run each prompt in its own fresh session. For a before-and-after comparison, run the
full prompt set against the original descriptions first, apply only the approved
change, then run the identical set again.

## Observe the routing

For each run, record which Skill activated, or that none did, and whether the
resulting behavior served the request. Activation alone is not success: a Skill that
triggers and then misfits the task is evidence for a description or body problem, and
the note belongs in the result.

Descriptions route probabilistically. One clean run is weak evidence; one miss is not
proof of failure. When a result surprises, run the prompt again before concluding
anything, and report the spread rather than the best run.

## Decide

- **Candidate routes better or equally on positives and negatives:** keep the change
  and record what was tested.
- **Candidate loses positives it previously won, or triggers on negatives:** restore
  the original description, then consider a narrower revision.
- **Inconclusive:** keep the current version or expand the prompt set.

A passing prompt set supports a local decision for those request shapes. It does not
prove the Skill routes correctly for every phrasing.

If the project is version controlled, use its normal diff and restore process. If it
is not, create a sibling backup only after the user approves it. Never remove the
original version of a merged or archived Skill until the user accepts the result.
