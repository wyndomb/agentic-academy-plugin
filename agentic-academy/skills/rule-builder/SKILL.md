---
name: rule-builder
description: >-
  Turn the user's repeated corrections into path-specific rules in .claude/rules/, so their
  standards apply automatically without being repeated. Use this skill whenever the user asks to
  build, create, or set up rules; asks "should this be a rule?"; complains that Claude keeps
  making the same mistake or that they keep repeating the same correction; asks why an instruction
  in CLAUDE.md isn't sticking; or wants their quality standards for a specific kind of work
  (posts, client emails, reports, briefs) to apply on their own. Also use it right after the user
  corrects the same thing a second time, even if they don't mention rules.
---

# Rule Builder

Help the user turn corrections they keep repeating into rules: small instruction files in `.claude/rules/` that load only when the matching kind of work is happening.

Why rules instead of more lines in CLAUDE.md: CLAUDE.md loads in full at the start of every session, and the longer it gets, the worse its instructions are followed. A rule with a `paths:` header loads only when files matching those paths are being worked on. The user's standards still show up exactly when they should, and cost nothing the rest of the time.

You do the finding and drafting. The user does the judging. Never write a rule file without showing the draft and getting a yes first.

## Two ways in

**Discovery mode** — the user asks to build their rules, set up rules, or find what should become rules. Scan the project and propose candidates. Follow "Discovery mode" below.

**Reactive mode** — the user just corrected something and asks "should this be a rule?", or you notice they have corrected the same thing at least twice. Judge that one correction. Follow "Reactive mode" below.

## First: is a rule even the right home?

Every correction has exactly one right home. A rule is only one of five. Before drafting anything, sort the correction:

| The correction is... | Right home |
| --- | --- |
| One-time, only about today's task | Nowhere. Use it and let it go. |
| A personal preference that applies to every kind of work (voice, formats, how they like answers) | A context file (my-voice.md, how-i-work.md) or CLAUDE.md's preferences section |
| Stable and true for the whole project | CLAUDE.md |
| Only true for one kind of output or one folder | **A rule. This skill.** |
| A lesson discovered through repeated work that doesn't map to one file type | Memory |

If the correction belongs somewhere other than a rule, say so, name the right home, and offer to put it there instead. Routing honestly matters more than producing a rule: a rules folder padded with misplaced instructions recreates the exact problem rules exist to solve.

## Discovery mode

### 1. Scan

Read, in this order: CLAUDE.md, the folder structure (names and what lives where), any auto memory or correction log if present, and a sample of the user's actual work files in each major folder (3-5 per folder is enough — you are looking for patterns, not reading everything).

You are looking for:
- Repeated formats: many files in one folder following the same structure.
- Repeated standards: things every file in a folder does (or carefully avoids).
- Corrections that repeat: the same guidance appearing in CLAUDE.md, memory, or chat history in different wordings.
- Output-specific instructions currently sitting in CLAUDE.md that only apply to one kind of work. These are rule candidates AND a chance to slim CLAUDE.md.

### 2. Propose

Present 3-5 candidates, no more. For each, exactly this format:

```
**Rule: <name>.md**
- Enforces: <the standard, in one or two lines>
- Loads when: <folder or file pattern, in plain words>
- Why a rule, not CLAUDE.md: <one line>
- Evidence: <what you saw in their project that suggests it>
```

The evidence line is required. A candidate without evidence from their real files is a guess, and guesses produce rules the user never needed.

Ask the user to pick which ones to build. Fewer is better: a project with three rules that fire reliably beats one with ten that half-apply.

### 3. Fill the gaps, then draft

For each accepted candidate, ask only what you cannot infer (usually: the exact standard when the files show a pattern but not the reason for it, and whether known exceptions exist). Keep it to one short round of questions.

Then draft each rule using the anatomy below and show it for approval before writing the file.

## Reactive mode

The user corrected something and wants to know if it should be a rule.

1. Apply the junk-drawer test. It earns saving only if at least one is true: it has been corrected at least twice; it affects multiple future sessions; it meaningfully changes quality; or the user would be annoyed if it were forgotten. If none hold, say "keep it in the chat for now" and stop.
2. Sort it with the five-homes table. If the right home is not a rule, route it there (offer to do it).
3. If it is rule-shaped: check whether a matching rule file already exists. Extending an existing rule beats creating a near-duplicate.
4. Draft the rule (or the addition), show it, get a yes, write it.

## Rule anatomy

Every rule has three layers. Hold all three or the rule is not done.

**`paths:` = WHEN.** YAML frontmatter listing glob patterns. The rule loads only when files matching these paths are being worked on. Scope as tightly as the work actually is: `linkedin-posts/**/*` not `**/*`.

**The body = WHAT.** The standards, written from the user's real corrections. Each instruction must be specific enough to check: "summaries are 3 bullets max, one line each" works; "be concise" does not. Where it helps future judgment, include the why in a short clause — a model that knows the reason can apply the standard to cases the rule never listed.

**Reference files = WHERE.** Point at the user's real material instead of cramming it in: their framework or style doc, a folder of strong examples. "Read X for voice. Study the files in Y/ before writing." A rule that makes Claude study the user's actual work beats a rule that tries to describe it.

Format:

```markdown
---
paths:
  - "<folder>/**/*"
---

# <Kind of Work> Rules

## <Standard group>
- <Specific, checkable instruction>
- <Specific, checkable instruction, with the why when it aids judgment>

## Reference files
- Read `<their real doc>` for <what it provides>
- Study examples in `<their real folder>/` before producing new work
```

Keep each rule under ~60 lines. If a rule wants to grow past that, the detail probably belongs in a reference file the rule points to.

For worked examples across different kinds of work (creators, consultants, entrepreneurs, knowledge workers), read `references/archetype-examples.md` — useful when proposing candidates for a project type you have less signal on.

## After writing: the fresh-session test

A rule is not done when the file exists. It is done when it survives a fresh session. After writing, tell the user to run this test, in these words or close to them:

1. Start a fresh session.
2. Ask for the same kind of work that used to need the correction. Do not mention the correction.
3. Run `/context` to confirm the rule loaded.
4. Compare the output to the old one.

If the mistake still appears: sharpen the wording, move the instruction to a better home, or remove it. Offer to help with whichever is needed.

## What not to do

- Do not create a rule from a single correction unless the user insists after hearing the junk-drawer test.
- Do not duplicate instructions that already live in CLAUDE.md — move them into the rule and offer to remove the CLAUDE.md line, so there is one source of truth.
- Do not invent standards the user's files and corrections don't support. Every line in a rule should trace back to something they did, said, or approved.
- Do not exceed five rules in one discovery pass. The user can run discovery again after this batch proves itself.
