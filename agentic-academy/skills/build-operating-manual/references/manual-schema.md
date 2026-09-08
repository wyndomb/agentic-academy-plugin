# Operating Manual Schema

Use this schema after the proposal has been approved. Every generated manual uses the
same five blocks, in this order: Orient, Guardrails, Playbooks, Routing, Map. Adapt the
depth of each block to the project. Do not leave placeholders in a finished manual.

Open each manual with a one-line frame:

```markdown
# CLAUDE.md: [Project name]

This file tells you how to work in this project. It routes you to the right files
instead of containing every detail.
```

## Shared blocks

Keep these facts aligned in `CLAUDE.md` and `AGENTS.md`.

### 1. Orient

What this project is and what the agent is helping improve.

- State what the project exists to do in one short paragraph. Use project language and
  evidence. Do not include an owner biography.
- Name who the output serves and what the owner is trying to improve right now, but only
  when the project states it or the user confirmed it.
- Include the operating model as a compact table:

```markdown
| Element | Definition | Location |
| --- | --- | --- |
| Work | <repeated job> | <project route> |
| Input | <required source material> | `<relative path>` |
| Output | <finished deliverable> | `<relative path>` |
| Key Standard | <most important quality requirement> | `<relative path or check>` |
```

The location may be a file, folder, command, or test. If the Key Standard is confirmed
but has no project artifact yet, state the rule without inventing a path.

### 2. Guardrails

The rules the agent must always follow and the boundaries that require approval.

**Critical rules.** Include only rules supported by evidence or confirmed by the user.
Strong rules are observable:

- Read named source files before producing the output.
- Preserve an approved schema or template.
- Run a named check before handoff.
- Keep one client's material out of another client's output.
- Separate observed facts from inference.

Weak rules such as "write clearly" or "make it high quality" do not belong here.

**Decision rules.** When the evidence supports them, add rules in the form
"When [situation], choose [action] because [reason]," and state what the agent should do
when information is missing or conflicting.

**Confirmation boundaries.** State actions that require approval and actions that are
safe to perform directly. Tailor the list to real project actions:

```markdown
Ask before:

- <hard-to-reverse project action>

Proceed without asking for:

- <small, reversible project action>
```

Do not grant permission for external sending, publishing, deletion, or record changes
unless the project or user explicitly grants it.

### 3. Playbooks

The behavior that should trigger when a recurring request comes in. Connect requests to
real processes:

```markdown
| Request | Required input | Process or Skill | Output destination | Check |
| --- | --- | --- | --- | --- |
| <repeated task> | `<path>` | `<Skill path or documented process>` | `<path>` | <standard or command> |
```

If no repeatable process exists, omit the Process or Skill value or write
`No documented process yet`. Never fabricate a Skill name.

Every playbook ends with a check the agent runs before treating the output as complete.
Name real checks and commands. If the project has no automated check, describe a manual
comparison against an observed standard or example.

### 4. Routing

The files the agent should read first for a specific kind of task. Name only routes that
change behavior:

```markdown
| When the task involves... | Read first |
| --- | --- |
| <task or file type> | `<relative path>` |
```

Prefer 3 to 10 high-value routes. Do not list the entire project.

### 5. Map

Where things live and where new work should be saved.

- Where input, output, and standards live.
- Where finished work should be saved.
- Naming patterns the project already uses for new files.
- The folder structure, trimmed to the part that changes behavior. Do not convert the
  entire project inventory into a tree.

## Claude-specific additions

Add these only to `CLAUDE.md`, inside the Routing block:

```markdown
### Claude-specific routing

- Project Skills: `.claude/skills/` when that directory exists
- Project rules: `.claude/rules/` when that directory exists
- Commands or hooks: include only detected, documented behavior
```

Adapt the entries to what exists. Do not add empty platform folders.

## Codex-specific additions

Add these only to `AGENTS.md`, inside the Routing block:

```markdown
### Codex-specific routing

- Project Skills: `.agents/skills/` when that directory exists
- Nested `AGENTS.md` files: explain their narrower scope when detected
- Local verification: include only commands supported by project evidence
```

Adapt the entries to what exists. Do not claim access to tools or services that were not
verified.

## Mature project option

For a large project with strong source-of-truth files, keep each root manual short but
keep all five blocks:

1. Orient: purpose plus the operating model table.
2. Guardrails: only the critical rules and confirmation boundaries.
3. Playbooks: a small table covering the most repeated requests.
4. Routing: pointers to the deeper rule and standard files, plus platform-specific
   routing.
5. Map: the trimmed folder structure and save locations.

Point to deeper rules instead of copying them. This reduces drift.

## Cross-file alignment check

Before handoff, compare the manuals block by block:

- Orient means the same thing in both files: same purpose, same Work, Input, Output, and
  Key Standard.
- Guardrails do not conflict, and confirmation boundaries match.
- Playbooks reference the same processes, destinations, and checks.
- Claude paths appear only in `CLAUDE.md`. Codex paths and nested instruction scope
  appear only in `AGENTS.md`.
- A shared block changed in one file has been reviewed in the other.
