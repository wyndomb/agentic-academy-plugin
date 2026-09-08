# Automatic Guardrails (Hooks)

A guardrail makes Claude do something every time, without being asked. For a knowledge worker, that means quality checks that run on their own and protection for files they must not lose. The point is simple: they stop having to remember.

Guardrails live in `.claude/settings.json`.

**When to recommend these**: once the person trusts Claude with real output and has a quality bar or source files worth protecting. This is Week 8 in the course. For someone early, note it as "later."

## Quality checks that run on their own

### Voice or tone check before a draft is "done"
| Recommend when you see | What it does |
|---|---|
| Voice-sensitive writing (newsletters, posts, founder content) | Claude runs a voice check at the end of a draft and flags anything that drifts |

**Plain-language value**: "Claude checks that the draft sounds like you before it hands it back, so you stop catching the same tone problems."

### Format check before a deliverable goes out
| Recommend when you see | What it does |
|---|---|
| Reports or deliverables with a required structure | Claude verifies the format (sections, headers, fields) before handing off |

**Plain-language value**: "Claude makes sure the report has every section in the right shape before you send it."

### Required checklist at the end of a task
| Recommend when you see | What it does |
|---|---|
| A quality bar they keep re-explaining | Claude runs the checklist automatically and reports what passed and what did not |

## Protecting files they cannot lose

### Block edits to source and reference files
| Recommend when you see | What it does |
|---|---|
| A style guide, voice reference, or client record they reuse | Blocks Claude from editing those files by accident |
| Original research or raw notes | Keeps the source intact so derived work never corrupts it |

**Plain-language value**: "Claude can read your style guide and client files but cannot accidentally overwrite them."

## Helpful nudges

### Sound or notification when Claude needs them
| Recommend when you see | What it does |
|---|---|
| Someone who multitasks while Claude works | A sound or desktop alert when Claude finishes or needs a decision |

**Plain-language value**: "You get a ping when Claude is done or needs you, so you can step away without watching the screen."

## Quick reference: what you see to what you recommend

| If you see | Recommend this guardrail |
|---|---|
| Voice-sensitive content | Voice check before a draft is done |
| A strict report or deliverable format | Format check before handoff |
| A quality bar they keep restating | Auto-run checklist at the end |
| Important source or reference files | Block edits to those files |
| They multitask while Claude works | Sound or notification when done |

## Recommending in plain language

Never say "PostToolUse hook." Say what becomes automatic. "Claude checks your draft sounds like you before it calls it finished" is the recommendation. The word "hook" goes in parentheses, once, so they learn the term.
