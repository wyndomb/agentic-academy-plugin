# Generating the one starter skill

The cohort promises students arrive at Week 1 with "1 to 3 starter skills generated from
patterns in your AI history" — not an empty `.claude/skills/` folder. This skill generates
**one** strong starter skill (the highest-frequency, most-systematizable pattern). When the
person wants more, `/agentic-academy:skill-finder` builds the rest; the job here is to ship
one real, runnable skill so the person sees the payoff on day one.

Read this in Phase 3.5 (after the #1 project is chosen, before final assembly).

## Pick the pattern (not the project)

The #1 *project* is the home you build in. The starter *skill* is the single most-repeated
*task* inside (or adjacent to) that project. They're related but not the same:
- Project = "AI Maker Content Engine" (a workspace).
- Starter skill = "generate 20 Substack Notes from a theme/draft in my voice" (one task
  they demonstrably run again and again).

Choose the pattern with the **highest evidence of repetition** and the **clearest quality
bar**. The signals depend on the source.

From a chat export, in order:
1. Repeated openers with the highest counts in `digest.json`.
2. Tasks named repeatedly in `memory.md` (e.g. "batches of 20-40 notes", "repurpose into
   LinkedIn/Twitter", "thumbnail concepts").
3. The recurring work called out in `context/voice-and-style.md` / `domain-map.md`.
If conversation data is thin, lean on `memory.md` — recurring task language there is enough
to justify a starter skill.

From an interview, in order:
1. The task with the highest confirmed time-per-task x frequency.
2. The task they gave the clearest "what good looks like" answer for.
3. The task they said they already have a template, checklist, or standard for.

Either way, pick the one task you could write the clearest "what good looks like" for; a
sharp narrow skill beats a vague broad one.

## Build it

1. Copy `assets/starter-skill-template/SKILL.md.template` to
   `<workspace>/.claude/skills/<skill-name>/SKILL.md`.
2. Fill every bracket from real evidence:
   - **description** — include the exact phrases the person uses to ask for this, so it
     triggers reliably. Quote from `samples.md` / `memory.md`, or from how they said they
     would ask for this work in the interview.
   - **standards / what good looks like / what to avoid** — pull from
     `context/voice-and-style.md` and `decision-rules.md`. Do not invent a quality bar;
     restate theirs.
   - **inputs / output** — match how they actually work (where the input lives, what format
     they want back).
3. Make it runnable as-is. A student should be able to invoke it on real input immediately
   and get something 80% right, then correct the last 20%.
4. Keep it to ONE skill. Resist scaffolding a library — when they want more, point them to
   `/agentic-academy:skill-finder`.

## Wire it in

- Mention the new skill in `CLAUDE.md` and `AGENTS.md` under "Most important files" / the
  routing table, so the agent knows it exists.
- In `start-here.md`, tell the person how to run it on their first real input, and that
  every correction they make should be folded back into the skill (or into
  `context/voice-and-style.md`).

## Output

`<workspace>/.claude/skills/<skill-name>/SKILL.md` — one complete, runnable skill, plus a
one-line pointer to it from `start-here.md` and the CLAUDE.md/AGENTS.md routing tables.
