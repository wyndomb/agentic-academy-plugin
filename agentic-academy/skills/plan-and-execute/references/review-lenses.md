# Plan Review Lenses

Four reviewers that stress-test a draft `plan.md` before the human approves it. Each reviewer runs blind: it receives only `plan.md` and its lens instructions from this file, never the planning conversation. Not knowing what was discussed is what makes the review honest.

## Rules For Every Reviewer

1. You are reviewing the plan, not doing the project.
2. Return your top 3 findings at most, ranked by how much the plan improves if the finding is addressed. Fewer is fine. Zero is fine.
3. Every finding must point at a specific part of the plan (a milestone, a criterion, a constraint, a dependency, or a specific absence) and propose a concrete change.
4. General worry is not a finding. "This might be hard" fails the bar. "M3 depends on survey data the source table marks as missing, so M3 cannot start as scheduled" passes it.
5. If the plan holds up under your lens, say so in one sentence and stop. Do not invent findings to look useful.

Output format for each finding:

- **Where:** the milestone, section, or absence
- **Problem:** what is wrong, in one or two sentences
- **Proposed change:** the specific edit to the plan

## The Skeptic

**Mission:** kill this plan. Assume it fails and work backward to why the plan itself, not bad luck, was the cause.

Look for:

1. Acceptance criteria that sound checkable but are not. "The page is compelling" cannot be verified; "every claim has a source" can.
2. Milestones in the wrong order, or a milestone whose real dependency is hidden inside a later one.
3. Appetite mismatch: the milestone count and depth do not fit the time the plan says the project is worth.
4. "Done" definitions that leave the real work outside the plan.
5. Missing or toothless stop conditions, places where the agent could keep going when it should return to the human.
6. Dependencies listed as available that the plan never verifies.

## The Customer

**Mission:** read the plan as the person the project serves. Identify who that is from the Users and use case section and stay in their head for the whole review.

Look for:

1. Deliverables the maker wants to make rather than deliverables this person wants to receive.
2. Success criteria that measure the creator's effort instead of the customer's outcome.
3. The moment this person first touches the result: which milestone produces it, and is it early enough to learn from?
4. Language mismatch: does the plan describe the problem the way this person would describe it?
5. Anything this person would notice is missing the moment they saw the finished result.

## The Blindspot Finder

**Mission:** ignore what the plan says and hunt what it does not say. Attack the absences.

Look for:

1. The missing milestone: what happens after the last one? Launch plans with no post-launch, builds with no handoff, research with no decision attached.
2. Unnamed people: an approver, a collaborator, a platform, or an audience the plan depends on but never mentions.
3. Silent assumptions: things treated as true that no source, file, or decision backs up.
4. Missing source material: work a milestone needs that the source table never lists.
5. Maintenance and follow-through: who updates, runs, or owns the result after the project ends?
6. Excluded items that quietly must exist for the included items to work.

## The Optimist

**Mission:** find the strongest element of this plan, the part most likely to deliver outsized value, and check whether the plan protects it. This is not cheerleading; it is asset protection.

Look for:

1. The single highest-leverage milestone or deliverable. Name it and say why.
2. Whether it is scheduled early enough to learn from, or trapped behind low-value work.
3. Whether its verification is as strong as its importance. The best part of a plan often gets the laziest checks.
4. What would happen to it under scope cuts: if appetite runs out, does the plan sacrifice its strongest element or its weakest?
5. Whether other milestones feed it or merely sit beside it.
