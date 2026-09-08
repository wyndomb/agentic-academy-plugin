# Home Base Structure and Audit Reference

This is the calibration reference for `claude-md-upgrader`. It defines the six parts of a knowledge-work home base, what strong vs thin looks like, how each archetype fills them, the audit checklist for RECOMMEND mode, and the maturity ladder.

## The six parts

### 1. Project overview

**What it is:** one short paragraph naming what this project is, in plain language, so Claude stops guessing.

**Strong:** "The AI Maker is a Substack newsletter about practical AI workflows for non-technical knowledge workers. The work is building systems that compound, not chasing tools."

**Thin:** "This is my content project." Says nothing Claude can act on.

### 2. Who the work serves

**What it is:** the real audience or client, specific enough to change word choice and examples.

**Strong:** "Readers are regular AI users who want to level up, not beginners and not engineers. They want implementation they can copy, and they distrust hype."

**Thin:** "People interested in AI." Too broad to shape any output.

### 3. What the person is trying to grow or improve

**What it is:** the goal the work serves, so Claude can weigh tradeoffs the way the owner would.

**Strong:** "Growing the paid tier while keeping free content trustworthy. Reader trust matters more than publishing speed."

**Thin:** "Get bigger." No direction Claude can use.

### 4. Five critical rules

**What it is:** the hard, checkable rules Claude must never break. These are the hook-checkable non-negotiables, not preferences.

**Strong:** "Never use em dashes in content. Never invent reader quotes or metrics. Free posts must deliver a complete lesson, never a teaser."

**Thin:** "Write well. Be helpful." Not checkable, so not a rule.

**Test for a real rule:** could you catch a violation by looking? If not, it is a preference, not a critical rule. Move it out.

### 5. Three decision rules

**What it is:** when Claude should ask vs move, and the default it should pick when unsure.

**Strong:** "Ask before publishing, sending, or overwriting a full draft. Move without asking on small reversible edits that follow an existing rule. When tier is unclear and it changes the depth, ask once."

**Thin:** "Use good judgment." Hands the decision back with no guidance.

### 6. Key files

**What it is:** the short routing list of what to read for which task. Not every file. The ones that change the answer.

**Strong:** a small table of file plus "read when" condition.

**Thin:** a dump of every file in the project, or nothing at all.

## Per-archetype fill guide

The six parts stay the same. What goes in them changes by archetype.

| Part | Content Creator | Coach / Consultant | Entrepreneur | Knowledge Worker |
| --- | --- | --- | --- | --- |
| Who it serves | the audience and their level | client types and their context | customers and the market | stakeholders and their needs |
| What to grow | reach, trust, paid tier | client results, capacity, rate | traction, positioning, revenue | clarity, decision speed, signal |
| Critical rules | voice, banned phrases, tier lines | client confidentiality, deliverable standards | brand and positioning consistency | report format, level of detail |
| Key files | voice guide, best posts, archive | case studies, templates, client notes | research, positioning, strategy | project files, templates, decision logs |

## Audit checklist (RECOMMEND mode)

Run every existing `CLAUDE.md` and `AGENTS.md` through these checks. Order findings by severity: stale and wrong first, then thin, then missing.

1. **Stale references.** Does it name files, folders, or commands that no longer exist? Does it describe a structure the project no longer has?
2. **Wrong claims.** Does any rule or fact contradict what the project actually contains now?
3. **Uncheckable rules.** Are the "rules" actually preferences that no one could catch a violation of?
4. **Vague parts.** Is any of the six parts so broad it would not change an output?
5. **Missing parts.** Which of the six parts is absent entirely?
6. **Dump vs route.** Does it pull everything inline when the project is large enough to need a routing table instead?
7. **Behavior test.** For each rule, would removing it actually change what Claude does? If not, it is decoration.
8. **Cross-file drift.** If both `CLAUDE.md` and `AGENTS.md` exist, do they contradict each other, duplicate stale rules, or fail to explain what belongs where?
9. **Upgrade placement.** Would the fix work better in `CLAUDE.md`, `AGENTS.md`, a rules file, command, skill, or another project file?

## Upgrade idea quality bar

Each recommendation should be useful enough that a non-technical knowledge worker can say yes or no without needing to understand the implementation.

A strong idea includes:

1. The behavior it will change.
2. The file where it belongs.
3. The evidence that triggered it.
4. The likely impact.
5. The effort required.
6. A concrete expected improvement.

Weak ideas sound nice but do not change future behavior. Examples: "make it clearer," "add more detail," or "improve structure" without naming what Claude would do differently.

## CLAUDE.md vs AGENTS.md placement

Use this placement guide when both files are possible:

| Put it in... | When... |
| --- | --- |
| `CLAUDE.md` | The instruction is mainly for Claude Code, Claude skills, Claude commands, or Claude-specific routing. |
| `AGENTS.md` | The instruction is mainly for Codex or another coding agent that reads `AGENTS.md`. |
| Both | The instruction is core project truth that both agents must follow, such as audience, hard writing rules, or safety boundaries. Keep it short and avoid stale duplication. |
| Rules file | The instruction is path-specific, platform-specific, or too detailed for the root home base. |
| Skill | The instruction describes a repeatable task with steps, examples, references, or quality checks. |
| Command | The instruction is a named workflow the user expects to run repeatedly. |

## The maturity ladder

Treat the home base differently depending on where it sits.

- **Empty:** no `CLAUDE.md` and no `AGENTS.md`. Recommend building the full six-part starter, or build it if the user explicitly asked for BUILD mode.
- **Beginner:** a short or vague home base. Fill it toward the six-part structure, keep what is there, make rules checkable.
- **Working:** all six parts present and mostly concrete. Tighten vague lines, fix any staleness, do not restructure.
- **Mature:** a router-style home base that points to deeper files (foundational docs, rules folders). This is correct for a large project. Audit only for staleness and genuine gaps. Never flatten it back to the starter structure. The goal here is maintenance, not a rebuild.
