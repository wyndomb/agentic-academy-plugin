---
name: audit-skills
description: Audit an existing Claude Code Skills setup after a model change, a routing failure, or Skill accumulation. Use when Claude activates the wrong Skill, misses a useful one, when two Skills overlap, when a Skills or commands folder feels bloated or stale, or before archiving old Skills. Produces a trigger map plus evidence-backed Keep, Clarify, Manual only, Merge, Test, and Archive recommendations. Does not audit CLAUDE.md instructions, inspect MCP connections, build new Skills from scratch, or edit files without approval.
---

# Audit Skills

Audit the Skill routing layer of the target project. Find Skills whose descriptions
still route the right work to the right procedure, Skills that collide with each other,
and Skills whose continued value depends on model behavior that only a fresh-session
test can confirm.

The goal is reliable activation with fewer collisions. Do not optimize for a smaller
Skill count. An archived Skill that was quietly doing useful work is a worse outcome
than an untouched folder.

## Modes

- **Audit:** Inspect and return a proposal plus a trigger map. This is the default.
  Do not edit.
- **Apply:** Patch only the finding IDs the user explicitly approves.
- **Verify:** Design or review fresh-session trigger tests for approved changes.

If the project has no `.claude/skills/` and no `.claude/commands/` directory, stop.
Explain that there is no Skill layer to audit and suggest building Skills from real
repeated work first. Do not create Skills inside this audit.

## How routing works, and why it shapes the audit

Claude sees every available Skill as a name plus a description in each session. The
body of a Skill loads only after it triggers. Two consequences drive this audit:

1. The description is the routing contract. A Skill can have an excellent body and
   still fail because its description claims too much, too little, or the same ground
   as a neighbor.
2. Descriptions are always-loaded context. Every Skill added to the folder makes each
   description compete with more neighbors for the same request.

Audit the descriptions as a routing system first. Audit individual Skill bodies second,
and only as deep as the findings require.

## Audit workflow

### 1. Resolve the target and scope

Use the current project root unless the user supplies another path.

Include by default:

- project Skills in `.claude/skills/*/SKILL.md`
- project commands in `.claude/commands/**/*.md`, which also route by description
- personal Skills and commands under `~/.claude/skills/` and `~/.claude/commands/`,
  read for collision detection because they compete with project Skills in the same
  session
- each in-scope Skill's bundled `references/`, `scripts/`, and `assets/` files, as
  evidence

Exclude by default:

- plugin and marketplace Skills: list their names as competing routes when visible,
  but never propose edits to files outside the user's own Skill folders
- sub-agents in `.claude/agents/`: a separate routing layer; name an agent only when
  it visibly competes with an audited Skill for the same task
- `CLAUDE.md` and rule files, except where a Skill and an instruction duplicate the
  same procedure
- MCP connections and hooks, except as evidence that a behavior is already enforced
  elsewhere

State the exclusions in the report. Personal-layer files are in scope for findings but
propose edits to them separately from project files, because they change behavior in
every project the user opens.

### 2. Build the skill inventory

Run the bundled inventory from the target project:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/inventory_skills.py" "${CLAUDE_PROJECT_DIR}" --format markdown
```

The inventory lists each Skill and command with its layer, description length, body
size, activation mode, bundled resources, broken references, and description-overlap
hints. Overlap hints are lexical signals, not verdicts. Two Skills can share words and
own different jobs, and two Skills can collide without sharing a single distinctive
term. Confirm or dismiss every hint by reading the descriptions.

From the inventory, build a context-load picture: how many descriptions load in every
session, which Skills carry unusually long descriptions or bodies, and which bundled
files never get referenced. Size is a lens for finding routing and maintenance
problems, never a goal by itself.

Then run the activation log to find when each route was last invoked:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/skill_activation_log.py"
```

It reads Claude Code session transcripts and reports, per Skill and command, how many
activations it has, when the last one was, and whether each came from a Skill tool call
or a typed slash command. Add `--days N` to scope the window, or `--project SUBSTR` to
read only the audited project's transcripts. Scanning every project is the default
because personal-layer Skills compete in every session, and a pattern across projects
is stronger evidence than one project's silence.

The log records two invocation paths: an explicit Skill tool call, and a typed slash
command. It does NOT reliably record description-match activation, which is the exact
mechanism most of this audit reasons about. Read it accordingly:

- An activation record is **Observed** evidence that a Skill is live. It strengthens
  **Keep** and raises the risk of changing that Skill.
- A blank or stale activation record is **not** evidence of disuse. It means the Skill
  was not explicitly invoked, which is a fact about invocation path, not about value.
  Never treat it as the basis for **Archive**.
- The split between Skill-tool and slash-command activations tells you how the owner
  actually reaches their routing layer. When slash commands dominate, missing command
  descriptions become a high-priority finding rather than a tidiness note.

Carry the log into the Evidence field of findings, never into the Decision field on
its own.

### 3. Read the routing layer in full

Read every in-scope description. Read the full SKILL.md body for any Skill that a
finding touches. Sample bundled references only when a finding depends on them, such
as a broken reference or a suspected stale procedure.

Gather only the evidence needed to confirm or challenge each Skill:

- the work products the Skill claims to produce, located in the project
- recent project files that show whether the Skill's task still recurs
- the tools, paths, commands, and file formats the Skill names
- targeted version-control history only when current files cannot show why a Skill
  exists or whether its output was ever produced

Do not use the current conversation as hidden evidence of what triggers. Do not use
connected services or the internet unless the user explicitly puts them in scope.

### 4. Build the trigger map

For each in-scope Skill, record:

- **Owns:** the task and output it is responsible for
- **Should trigger on:** the request shapes that ought to activate it
- **Should not trigger on:** the nearby request shapes that ought to miss it
- **Mode:** automatic, or manual-only via `disable-model-invocation` or equivalent
- **Competes with:** every other Skill, command, or visible agent whose description
  could plausibly claim the same request

The map is a deliverable, not scratch work. It appears in the report even when a Skill
gets no finding, because it is the artifact that lets the owner reason about routing
after the audit ends.

Derive "should trigger" and "should not trigger" from the description and the Skill's
evident purpose. When the description and the body disagree about what the Skill is
for, that disagreement is itself a finding.

### 5. Audit each skill

For each Skill with a material problem, identify:

- the task it was built to own and the failure or repetition that motivated it
- whether project evidence shows that task still recurring
- how its description performs as a routing contract: too broad, too narrow, vague,
  missing an exclusion boundary, or colliding with a neighbor
- whether its activation mode matches its cost and risk
- whether its body has drifted from the project: stale tools, dead paths, broken
  bundled references, procedures the current model may no longer need spelled out
- whether it duplicates a procedure that also lives in `CLAUDE.md`, a rule file, a
  hook, or another Skill
- the risk of changing it
- whether its value can be confirmed from files or requires fresh-session trigger
  testing

Read [audit-rubric.md](references/audit-rubric.md) before assigning decisions.

### 6. Return the audit proposal

Read [report-template.md](references/report-template.md) and follow its output
contract. Use stable finding IDs such as `S01`, `S02`, and `S03`.

Every material finding must recommend one decision:

- **Keep**
- **Clarify**
- **Manual only**
- **Merge**
- **Test**
- **Archive**

Use exactly one of these six labels in the Decision field. Put uncertainty in the
Confidence, Evidence, or Proposed change or test fields rather than inventing hybrid
labels. When owner intent could change the decision, recommend **Keep** or
**Clarify**, ask one focused question, and describe the conditional follow-up
separately.

Use **Test** when the claim depends on how the current model routes requests, which
cannot be proven from files. Routing behavior must not be inferred from confidence,
release notes, or how obvious the description seems when read directly.

End the Audit mode report by asking the user to select finding IDs. Do not edit during
the same turn that first presents the audit.

## Apply approved findings

A user selection such as "apply S02 and S05" authorizes only those findings.

Before editing:

1. Re-read each affected SKILL.md and its neighbors in the trigger map.
2. Confirm that each finding still matches the current file.
3. If the project is not version controlled, offer to create a sibling backup before a
   substantial change.
4. For a **Test** finding, record the trigger prompts and current description before
   applying a candidate change.

Then:

- make the smallest patch that implements the approved decision
- for **Clarify**, change the description's boundaries without silently changing what
  the Skill does; body edits need their own approval
- for **Manual only**, add the activation-mode setting and leave the body alone
- for **Merge**, build the merged Skill first, confirm it covers both original scopes,
  and archive the absorbed Skill only after the user accepts the merged version
- for **Archive**, move the Skill folder to an archive location inside the project;
  never delete it
- do not modify plugin Skills, agents, hooks, settings, MCP connections, or
  `CLAUDE.md` inside this audit
- read every changed file back
- show the resulting diff or a concise before-and-after excerpt
- report approved findings that were skipped because the evidence changed

## Verify behavior

Read [trigger-test-protocol.md](references/trigger-test-protocol.md) for any **Test**
finding and after a material Apply operation. It defines two tiers:

- **Structural check:** confirm frontmatter parses, references resolve, and the
  changed descriptions introduce no new lexical collision. Cheap enough to run after
  every Apply. It supports no claim about routing behavior.
- **Fresh-session trigger comparison:** required before claiming any Skill now
  activates correctly, and required before finalizing a **Test** finding.

An edited description does not prove routing in the session that edited it, because
that session already has the audit in context. Use fresh sessions with realistic,
substantive prompts: positive prompts that should activate the Skill, negative prompts
that should miss it, and competing prompts that a neighboring Skill should win.

Do not claim improved routing from structural validation alone. Report exactly what
was inspected, what was changed, which tier ran, and whether fresh-session trigger
tests remain pending.

## Guardrails

- Protect Skills that encode safety boundaries, approval steps, source-of-truth
  routes, required output formats, or checks the project verifies. Loosening their
  descriptions or activation mode is high risk.
- Treat "no evidence of recent use" as a question, not a verdict. Skills for rare but
  important work earn their place through consequence, not frequency.
- Keep the audit project-local unless the user expands the scope. Propose personal-
  layer changes separately from project changes.
- Keep `CLAUDE.md` and MCP cleanup as separate audits.
- Never delete a Skill. Archive means moving it somewhere recoverable.
- Never expose secrets, private records, or sensitive local values in the report.
- Never mention system prompts, host metadata, account details, or runtime context
  unrelated to the Skill audit.
- Before returning, remove any finding whose evidence cites hidden system context
  rather than a project file, command result, trigger test, or explicit user answer.
