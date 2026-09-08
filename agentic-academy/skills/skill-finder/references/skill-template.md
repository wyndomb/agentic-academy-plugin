# Skill Scaffold Template

Use this when the user selects a candidate to build. Write one `.claude/skills/<slug>/SKILL.md` per selected skill. Match the conventions of skills already in the project (look at a neighbor first). Keep the generated skill lean and runnable, not aspirational.

## Slug rules

- Lowercase, hyphenated, short, verb-or-noun first (`draft-from-archive`, `client-prep-brief`, `weekly-digest`).
- The slug is the folder name and the `name:` field. They must match.

## File structure to generate

```
.claude/skills/<slug>/SKILL.md
```

Only add a `references/` subfolder if the skill genuinely needs calibration material (a rubric, a style sample, a checklist) that would bloat the main file. For a v1 skill, usually it does not. Do not create empty folders.

## SKILL.md template to fill in

```markdown
---
name: <slug>
description: >-
  <One or two sentences on what the skill does and the output it produces.>
  Use when <natural trigger phrase>, <another trigger phrase>, or /<slug>.
---

# <Human Readable Name>

<One paragraph: the single repeated problem this skill solves and the messy
input to useful output it turns around. Name the real friction, not a generic
benefit.>

## When this runs

<The trigger moment in plain language. What the user is doing or saying when
this should fire.>

## What it reads

<The specific files, folders, or sources this skill should pull context from
before producing anything. Be concrete: name the folders.>

## Workflow

1. <First step.>
2. <Second step.>
3. <Continue. Keep steps concrete and in order.>

## Output

<The exact shape of what it produces: the format, the structure, where it
saves if it saves. Show a short example skeleton if the format is non-obvious.>

## Quality standard

<What good output looks like for this task, in plain language. The one or two
checks that separate a usable result from a throwaway one.>
```

## Filling-in rules

- Pull the trigger phrases, the files-to-read, and the quality standard from what you actually learned about the project in the scan. Do not leave placeholders.
- Ground the workflow in how the user already does this task by hand. The skill should encode their real process, not an idealized one.
- If the project has a house style, banned words, or naming conventions (check `CLAUDE.md` and any rules files), bake the relevant ones into the quality standard so the skill respects them.
- Keep the first version small. One clear pass beats a sprawling skill that tries to handle every edge case. The user will refine it after testing.

## Verification checklist

Run this against every generated `SKILL.md` before reporting it as created. Each check is mechanical: it either passes or it does not. Fix failures and re-check.

### Structure

1. **File is at `.claude/skills/<slug>/SKILL.md`** - exact path, correct case, `SKILL.md` capitalized.
2. **Frontmatter parses.** Opens with `---` on line 1, closes with `---`, valid YAML between. The most common break is an unquoted `:` inside the description: a colon followed by a space in plain YAML scalar starts a new key and the parse fails. The `>-` block form in the template avoids this, so keep it.
3. **No empty folders.** If you created `references/`, it contains at least one real file. If it does not, remove it.

### Identity

4. **`name:` matches the folder name exactly.** A mismatch means the skill may not resolve when invoked. Check the literal strings, not your memory of what you typed.
5. **Slug follows the rules above** - lowercase, hyphenated, no spaces or underscores.
6. **Slug does not collide** with an existing skill, command, or agent found in the Step 2 coverage inventory. A collision is a user decision, not something to silently rename around.

### Triggering

7. **`description:` contains concrete trigger phrases**, not just a summary of what the skill does. A description that only describes capability will not fire reliably. It needs the words someone would actually say, quoted as phrases.
8. **The trigger phrases match the `Triggers when` line** from the candidate the user selected. That phrasing came from how they already talk about the work; do not quietly substitute your own.
9. **Slash invocation is included when the user will reach for it by name.** Write `/<slug>` into the description for skills invoked deliberately (a report, a review, a generator). Skip it for skills that should fire from natural phrasing alone. This is a judgment call, not a hard requirement — plenty of good skills never name a slash command.

### Content

10. **No placeholders survive.** Search the file for `<`, `TODO`, `TBD`, and bracketed template text. Every field is filled with something specific to this project.
11. **Named files and folders exist.** The "What it reads" section points at real paths in this repo. Verify them; a skill that reads a folder you invented fails on first run.
12. **House rules are respected.** If the project has a style guide, banned words, or naming conventions (check `CLAUDE.md` and any rules files), the generated skill does not violate them and bakes the relevant ones into its quality standard.

## After writing

For each skill created, tell the user:

1. The exact path you wrote.
2. Verification result: pass, or what you fixed to make it pass. If a check could not be resolved without their input, name it.
3. One concrete first test they can run to see it work, phrased as the thing they would actually type.
4. The one thing most likely to need adjustment after that first test.
