---
name: build-operating-manual
description: Scan a project and create or improve its root CLAUDE.md and AGENTS.md operating instructions using the Work, Input, Output, and Key Standard framework. Use when someone asks for a project operating manual, wants an /init-style setup for Claude and Codex, needs instructions generated from an existing repository, wants to route agents to project files and Skills, or asks to create, align, or refresh CLAUDE.md and AGENTS.md as a matched pair across a code or non-code project. It proposes before it writes. For upgrade ideas on an existing CLAUDE.md use claude-md-upgrader; for a verdict on one, use audit-claude-md.
---

# Build Operating Manual

Create project instructions from evidence in the target project. First show what was
observed, inferred, and still unknown. Write `CLAUDE.md` and `AGENTS.md` only after the
user approves that proposal.

Keep the result specific to the target project and portable across machines. Do not carry
personal details, preferences, memories, or facts from another project into the manuals.

## Core model

Identify four elements:

1. **Work:** the repeated job the project exists to complete.
2. **Input:** the source material required before the job begins.
3. **Output:** the deliverable that should exist when the job is complete.
4. **Key Standard:** the most important requirement the output must pass.

Map those elements to the project:

- Project folders hold the repeated job.
- Input folders or source files hold real material.
- Output folders or named destinations hold deliverables.
- Standards, tests, examples, or review rules define quality.
- `CLAUDE.md` and `AGENTS.md` route the agent through the project.
- A Skill contains the exact process for one repeatable task.
- External tools provide access outside the project only when the job requires it.

## Workflow

### 1. Resolve the target and mode

Use the current project root unless the user provides another path. Ask for the path only
when the target is genuinely ambiguous.

Choose one mode:

- **Create:** neither instruction file exists.
- **Align:** one file exists, or both exist but differ in shared project truth.
- **Improve:** both exist and the user wants stronger routing or clearer rules.

Always begin with a preview. Creating new files and changing existing files happen only
after the user approves the preview. Never silently overwrite a mature instruction file.

### 2. Run the safe inventory

Run:

```bash
python3 <skill-directory>/scripts/scan_repo.py <project-root> --format markdown
```

The script inventories structure and candidate routing files without reading file
contents. Treat its output as leads, not conclusions.

Then inspect the project directly:

1. Read existing `CLAUDE.md` and `AGENTS.md` in full.
2. Read root-level overview and configuration files that explain the project.
3. Read existing rules and relevant `SKILL.md` files.
4. Sample 3 to 7 representative files across likely inputs, outputs, standards, tests,
   templates, or process documentation.
5. Prefer templates and schemas over private records. Never copy secrets, credentials,
   personal identifiers, client details, or unrelated content into an instruction file.
6. Do not scan outside the target project or use connected services unless the user
   explicitly places them in scope.

Do not treat generated folders, dependency folders, archives, or build output as evidence
of how the project should operate.

### 3. Build an evidence map

For every proposed instruction, assign one confidence label:

- **Observed:** directly supported by a file, folder, test, command, or existing rule.
- **Inferred:** the evidence strongly suggests it, but the project does not state it.
- **Unknown:** owner judgment is required.

Identify:

- Work, Input, Output, and Key Standard
- How the work repeats: by channel, client, time, project, pipeline stage, or another
  observed organizing axis
- Important project routes
- Repeatable tasks and existing Skills
- Checkable quality rules
- Commands or checks that actually exist
- Actions requiring confirmation
- Tool-specific routing for Claude and Codex

Never infer biography, audience, business goals, tone, policies, tool access, or approval
rights from generic folder names. Use them only when the project states them or the user
confirms them.

### 4. Present the proposal

Use this exact shape:

```markdown
# Operating Manual Proposal

Mode: <Create | Align | Improve>
Project root: <path>
Files reviewed: <short list>

## Core job

| Element | Proposed definition | Evidence | Confidence |
| --- | --- | --- | --- |
| Work |  |  | Observed / Inferred / Unknown |
| Input |  |  | Observed / Inferred / Unknown |
| Output |  |  | Observed / Inferred / Unknown |
| Key Standard |  |  | Observed / Inferred / Unknown |

## Proposed playbooks and routing

| Request or task | Read first | Process or Skill | Save to |
| --- | --- | --- | --- |
|  |  |  |  |

## Proposed guardrails

- <checkable rule or approval boundary, with evidence>

## Unknowns that would change the manuals

- <only material unknowns>

## Files to create or update

- `CLAUDE.md`: <five-block manual plus Claude-specific routing>
- `AGENTS.md`: <five-block manual plus Codex-specific routing>
```

Ask no more than five focused questions, and only for unknowns that would change agent
behavior. If the user corrects an inference, treat the correction as confirmed project
truth for this run.

Wait for approval before writing.

### 5. Generate the manuals

Read [manual-schema.md](references/manual-schema.md) before drafting. Every manual uses
the same five blocks, in order: Orient, Guardrails, Playbooks, Routing, Map.

Apply these rules:

1. Keep shared project truth synchronized across both files.
2. Put Claude-specific paths and behavior only in `CLAUDE.md`.
3. Put Codex-specific paths and behavior only in `AGENTS.md`.
4. Use a short router for a large project. Use a compact inline manual for a small one.
5. Preserve strong existing instructions. Patch around them instead of flattening them.
6. Reference only files, folders, commands, and Skills that exist.
7. Flag a useful missing route or Skill in the handoff instead of inventing it.
8. Keep rules checkable. Remove advice such as "be helpful" or "use best judgment."
9. Do not create extra folders, standards, Skills, integrations, or automation unless the
   user separately requests them.
10. Use relative project paths. Avoid machine-specific absolute paths.

### 6. Validate

Read both generated files back and check:

- Both files use the five blocks in order: Orient, Guardrails, Playbooks, Routing, Map.
- Every referenced local path exists.
- Every named command or check exists in project configuration or documentation.
- Shared Work, Input, Output, Key Standard, rules, and confirmation boundaries agree.
- Tool-specific paths are in the correct file.
- Existing nested instruction files are respected.
- No secrets, personal profile material, private records, or facts from another project
  were introduced.
- Every section changes routing, quality, or decision behavior.

For an existing manual, review the diff and confirm that unrelated instructions remain
unchanged.

### 7. Hand off

Report:

- Files created or updated
- What came from observed evidence
- What the user confirmed
- Any unresolved unknowns left out
- One real repeated task to run as a before-and-after test

Do not claim the setup works until both files pass readback and path validation.

## Guardrails

- Keep all inspection local to the target project by default.
- Do not use current-chat history as hidden source material. Use only explicit answers
  about the target project.
- Do not expose sensitive file contents in the proposal.
- Do not convert an entire project inventory into an instruction file.
- Do not duplicate detailed task procedures in the root manuals. Route to a Skill.
- Do not add agent teams, hooks, schedules, or multiple integrations to a first manual
  unless the project already uses them.
- Require confirmation before publishing, sending, deleting, overwriting substantial
  work, changing external records, or other hard-to-reverse actions.
