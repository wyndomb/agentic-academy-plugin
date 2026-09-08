---
name: audit-claude-md
description: Audit an existing Claude Code instruction setup after a model, tool, or project change. Use when CLAUDE.md feels bloated, contradictory, vague, stale, or overly specific, or before removing old instructions. Produces evidence-backed Keep, Rewrite, Move, Test, and Retire recommendations. Does not create a first CLAUDE.md, audit Skill routing, inspect MCP connections, or edit files without approval.
---

# Audit CLAUDE.md

Audit the instruction system that affects the target project. Find rules that still earn
their place, structural problems that can be confirmed from files, and model-dependent
assumptions that need a fresh-session test.

The goal is useful behavior with fewer conflicts. Do not optimize for a target line count
or removal percentage.

## Modes

- **Audit:** Inspect and return a proposal. This is the default. Do not edit.
- **Apply:** Patch only the finding IDs the user explicitly approves.
- **Verify:** Design or review a controlled before-and-after test for approved changes.

If no project `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` exists, stop.
Explain that there is no manual to audit and suggest creating one first. Do not build it
inside this Skill.

## Audit workflow

### 1. Resolve the target and scope

Use the current project root unless the user supplies another path.

Include by default:

- project-root and `.claude/CLAUDE.md` files
- project-local `CLAUDE.local.md`
- nested `CLAUDE.md` files
- `.claude/rules/**/*.md`
- `.claude/output-styles/**/*.md` when the project defines its own styles
- project `AGENTS.md` files, for alignment against `CLAUDE.md` only
- `.claude/settings.json` and `.claude/settings.local.json`, as evidence only
- files imported by an in-scope instruction file when they remain inside the project

Exclude by default:

- user and organization instructions outside the project
- MCP configuration and connection status
- general Skill-routing quality
- unrelated project content
- external imports, unless the user explicitly places them in scope

State the exclusions in the report. An instruction from outside the project may still
affect behavior, so mention that the audit is project-scoped.

`AGENTS.md` is read for one purpose: to find places where it and `CLAUDE.md` state
different rules for the same behavior. Claude Code does not load `AGENTS.md` as project
memory, so never treat it as an active instruction source or propose edits to it inside
this audit. Report the divergence and let the owner decide which file changes.

Name the active output style in the Scope section whenever the session is running one.
An active style injects instructions into every turn and can contradict `CLAUDE.md` voice,
format, or workflow rules. A user-level style stays out of scope for edits, but a conflict
between it and a project rule is a reportable finding. Say plainly whether the style is
project-level or user-level, and never propose editing a user-level file.

### 2. Build the instruction map

Run the bundled inventory from the target project:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/inventory_instructions.py" "${CLAUDE_PROJECT_DIR}" --format markdown
```

The inventory identifies instruction files, scope, path-specific rules, imports, broken
imports, and files that require separate authorization. It does not decide whether an
instruction is good.

From the inventory, build a context-load picture: which sources load in every session,
which load only for specific paths, and how many lines each group contributes. Use it to
spot blocks that repeat across files loading together and content that loads far more
broadly than the work it governs. Size is a lens for finding Duplicate, Misplaced, and
Overbroad problems, never a goal by itself, and no block gets a finding because of its
length alone.

Read every in-scope instruction file in full. Follow in-project imports. Do not read an
external import, a sensitive path, or a symlink resolving outside the project without
explicit permission.

Claude Code may have expanded imports while starting the current session, before this
Skill runs. The inventory can state that its script did not open a sensitive or external
target. It cannot prove that Claude Code never loaded that target. Never quote or rely on
sensitive imported content during the audit.

### 3. Gather only the evidence needed

Inspect project evidence that can confirm or challenge the instructions:

- root overview and configuration files
- commands that the instructions name
- files and folders used as routes
- two to five representative inputs, outputs, standards, tests, or templates
- a referenced Skill only when `CLAUDE.md` appears to duplicate its procedure
- `.claude/settings.json` hooks and permissions, to find behavior already enforced
  deterministically
- targeted version-control history for a material block only when current files do not
  explain why it was added or what failure it was meant to prevent

Do not scan the entire project when a smaller sample can answer the question. Do not use
the current conversation as hidden project evidence. Do not use connected services or
the internet unless the user explicitly puts them in scope.

Do not inspect history for every instruction. Start with current project evidence. The
rubric's Provenance section defines how to label what the history does or does not show.

Do not describe a file as tracked, committed, shared, or team-wide merely because of its
name or location. Verify tracked status with the project's version-control metadata when
that status matters. If the project is not version controlled, describe only its scope
and location.

### 4. Audit instruction blocks

Treat a heading with its bullets, a paragraph rule, or a related rule group as one
instruction block. Preserve the meaning created by nearby lines. Do not classify isolated
sentences when their section changes their scope.

For each material block, identify:

- the behavior it is meant to control
- the failure it was meant to prevent and any project evidence of its origin
- where and when it loads
- the evidence supporting it
- any duplicate, conflict, broken route, vague language, misplaced procedure, or
  overprescribed process
- whether a hook, permission, or script in `.claude/settings.json` already enforces the
  same behavior deterministically
- whether procedural steps could become a direct description of the finished result,
  required constraints, and failure conditions
- the risk of changing it
- whether its value can be proven from files or requires behavioral testing

For each conflict, assign operational priority from the evidence: how broadly the
conflicting blocks can activate, how often the affected task appears to recur, and the
consequence when they collide. Keep this attention ranking separate from patch order.
If task frequency cannot be supported by project evidence, mark that part **Unknown**
rather than guessing.

Read [audit-rubric.md](references/audit-rubric.md) before assigning decisions.

### 5. Return the audit proposal

Read [report-template.md](references/report-template.md) and follow its output contract.
Use stable finding IDs such as `A01`, `A02`, and `A03`.

Every material finding must recommend one decision:

- **Keep**
- **Rewrite**
- **Move**
- **Test**
- **Retire**

Use exactly one of these five labels in the Decision field. Put uncertainty in the
Confidence, Evidence, or Proposed change or test fields rather than inventing hybrid
labels. Make the proposed action match that decision. When owner intent could change the
decision, recommend **Keep** or **Rewrite**, ask one focused question, and describe the
conditional follow-up separately.

Use **Test** when the claim depends on what the current model can do without the
instruction. Model capability must not be inferred from confidence, release notes, or a
shorter-file preference.

End the Audit mode report by asking the user to select finding IDs. Do not edit during
the same turn that first presents the audit.

## Apply approved findings

A user selection such as "apply A02 and A05" authorizes only those findings.

Before editing:

1. Re-read the selected blocks and nearby instructions.
2. Confirm that each finding still matches the current file.
3. If the project is not version controlled, offer to create a sibling backup before a
   substantial change.
4. For a **Test** finding, capture the baseline task and current file state before
   applying a candidate change.

Then:

- make the smallest patch that implements the approved decision
- preserve unrelated wording and mature router structure
- do not modify a Skill, hook, setting, MCP connection, or external file
- do not delete an instruction file
- read every changed file back
- show the resulting diff or a concise before-and-after excerpt
- report approved findings that were skipped because the evidence changed

When a block should move into a Skill, rule, or hook, remove it from `CLAUDE.md` only
after the destination already exists or the user separately approves creating it.

## Verify behavior

Read [test-protocol.md](references/test-protocol.md) for any **Test** finding and after a
material Apply operation. It defines two tiers:

- **Structural check:** confirm routes resolve, protected rules survived intact, and no
  new duplicate or conflict was introduced. Cheap enough to run after every Apply. It
  supports no claim about behavior.
- **Fresh-session comparison:** required before claiming any behavioral effect, and
  required before finalizing a **Test** finding's removal.

A changed `CLAUDE.md` does not prove behavior in the session that edited it. Use fresh
Claude Code sessions for the baseline and candidate runs, with the same model, task,
inputs, permissions, and available tools.

Do not claim improved performance from structural validation alone. Report exactly what
was inspected, what was changed, which tier ran, and whether a fresh-session behavioral
comparison remains pending.

## Guardrails

- Protect safety, privacy, legal, approval, destructive-action, source-of-truth, required
  format, and project-specific terminology rules.
- Treat a missing or contradictory protected rule as high risk.
- Keep the audit project-local unless the user expands the scope.
- Keep Skill routing and MCP cleanup as separate audits.
- Never expose secrets, private records, or sensitive local values in the report.
- Never mention system prompts, host metadata, account details, or runtime context that is
  unrelated to the project audit.
- Before returning, remove any finding whose evidence cites hidden system context rather
  than a project file, command result, behavioral test, or explicit user answer.
- Never silently convert a mature router into an inline manual.
