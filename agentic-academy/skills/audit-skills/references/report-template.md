# Skill Audit Report Contract

Adapt the amount of detail to the project, but preserve these sections and fields.

## 1. Scope

Report:

- project root
- mode
- model or Claude Code change being investigated, if the user named one
- Skill and command layers reviewed: project, personal, or both
- plugin Skills and agents named as competing routes but excluded from edits
- project evidence sampled
- any targeted version-control history inspected for provenance
- `CLAUDE.md`, MCP, hook, and agent exclusions
- any unreadable or unauthorized sources

Do not identify host metadata, account information, hidden system context, or
unrelated runtime details as an audit source or exclusion.

State whether version-control evidence is available. When it is unavailable, describe
Skills as project-level or personal. Do not call them tracked, committed, shared, or
team-wide.

## 2. Skill inventory

Summarize each in-scope Skill and command:

| Skill | Layer | Kind | Mode | Description length | Body lines | Notes |
| --- | --- | --- | --- | ---: | ---: | --- |

Mention broken references, unusually long descriptions or bodies, and bundled files
that nothing references.

### Context load

Report how much description text loads in every session across the audited layers,
and name the largest contributors. Present this as exposure information, not a
reduction target, and do not attach a size number the audit should aim for.

### Activation record

Report when each route was last invoked, from the activation log. Cover the routes a
finding touches plus the most and least recently active. Give the count, the last date,
and whether activations came from a Skill tool call or a typed slash command:

| Route | Layer | Activations | Last invoked | How |
| --- | --- | ---: | --- | --- |

Say which invocation path dominates. That shapes finding priority: a routing layer the
owner reaches mostly by typing slash commands has different failure modes than one
reached by description match.

Print this caveat in the report itself, not only in your reasoning:

> The activation log records explicit Skill tool calls and typed slash commands. It
> does not reliably record description-match activation. A route with no activation
> record was not necessarily unused.

Never present a blank or old activation date as grounds for removing a Skill.

## 3. Trigger map

The map is a deliverable. Include every in-scope Skill, including healthy ones.
Render each entry as a compact block, not a wide table:

### skill-name

- **Owns:** the task and output it is responsible for
- **Should trigger on:** representative request shapes
- **Should not trigger on:** the nearby request shapes that ought to miss it
- **Mode:** automatic or manual-only
- **Competes with:** neighboring Skills, commands, or agents, or "none observed"

Keep each entry short. The map shows ownership at a glance; the findings carry the
argument.

## 4. Audit summary

Name the two or three highest-priority findings and explain the routing behavior or
risk each one affects. Rank attention using collision breadth, evidenced task
frequency, and consequence. Do not use ease of patching, archive counts, or decision
tallies as success measures.

## 5. Protected skills

List the Skills whose boundaries should remain untouched during this audit and
explain the failure each one prevents. Avoid reproducing private values or
unnecessary file content.

If no protected Skills were identified, write exactly:

> No protected skills identified.

Add nothing else to this section.

## 6. Findings

Use stable IDs. Render each finding as a compact block, not a wide table. The report
is read in a terminal, and a many-column row wraps into unreadable text:

### S01. Short name of the finding

- **Skill and layer:** the Skill or Skills involved and where they live
- **Finding:** the finding type and one sentence stating the problem
- **Evidence and provenance:** what supports the finding, the work the Skill was
  built to own, and its provenance label
- **Decision:** one of the six labels, then Confidence, Risk, and Operational
  priority
- **Proposed change or test:** the concrete action or test definition

Requirements:

- Keep file locations precise enough for review.
- For **Overlap**, quote or paraphrase both descriptions and include one realistic
  prompt both could claim.
- For **Clarify**, show the proposed positive boundary, the proposed negative
  boundary, and the neighbor each protects against.
- For **Manual only**, name the activation-mode setting and the invocation the owner
  will use instead.
- For **Merge**, name the surviving Skill and what happens to both trigger
  boundaries.
- For **Test**, define the positive, negative, and competing prompts and the observed
  result that settles the decision.
- For **Archive**, show the structural evidence that makes testing unnecessary and
  name the archive destination.
- Make each proposed action match its Decision label. Do not pair **Archive** with an
  alternative that rebuilds the same Skill. If rebuilding remains plausible, use
  **Clarify** or **Keep** and ask one focused owner question.
- Paraphrase sensitive content.

Omit low-value commentary on Skills that are clearly healthy; their trigger map
entries are enough.

## 7. Proposed patch order

Group the findings:

1. Low-risk structural fixes such as broken references and dead paths
2. Description clarifications and activation-mode changes
3. Merges, which need the merged Skill built and accepted before anything is archived
4. Trigger tests
5. High-risk decisions requiring owner judgment

Call out dependencies. This is implementation order, not attention priority. A
high-priority collision may still depend on owner judgment or a trigger test and
therefore appear later in the patch sequence.

## 8. Approval boundary

End Audit mode with:

> No files changed. Select the finding IDs you want to apply. I will patch only those
> items. Findings marked Test need fresh-session trigger prompts before any archive
> or merge is finalized.

If there are no material problems, say so. Do not manufacture recommendations to fill
the report.

Before returning, scan the report for references to system context, host metadata,
account details, or unverified claims that a file is tracked or shared. Remove or
replace them with project evidence.

## Apply handoff

After approved edits, report:

- finding IDs applied
- files changed
- approved findings skipped and why
- protected Skills preserved
- structural validation completed
- whether fresh-session trigger tests remain pending

Do not describe a static description diff as routing proof.
