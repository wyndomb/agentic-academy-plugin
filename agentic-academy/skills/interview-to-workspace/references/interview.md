# The interview (Phase 1 detail)

Adapted from the `agentic-outcome-finder` skill. Same conversational interview, but here it
feeds a real workspace build, so it collects a bit more: enough to fill the context files and
scaffold one starter skill. Read this when you reach Phase 1.

Run it as a short, friendly conversation, not a form. Ask in **small batches (2-3 questions),
then adapt**. Aim for about three rounds plus one voice round. Do not interrogate. Thin answer
→ one follow-up. Rich answer → move on.

Open with a one-line framing: *"I'm going to ask about your real work for a few minutes, then
build you a starter folder an agent can work inside — shaped around what you actually do."*

## Round 1 — the shape of the job (always ask both)

1. "What's your role, and what field are you in?" (Prime if they hesitate: marketing, HR,
   consulting, real estate, sales, ops, finance, recruiting, compliance, analyst, founder.)
2. "Walk me through a normal week. What are the handful of things you do over and over?"

## Round 2 — where the time and the work live (adapt to Round 1)

3. "Of those, which eat the most time? Roughly how long each, and how often?"
   **You need a rough number for the top 2-3 tasks.** See the time gate below.
3b. For those same top 2-3 tasks: "How much of that time is the mechanical part — gathering,
   drafting, formatting — and how much is your judgment?" Get a rough split (e.g. "mostly
   mechanical, maybe 70/30"). This is the **agent share** the report's time-back math needs.
   If they can't say, estimate out loud from the task type and ask them to confirm, exactly
   like the time gate.
4. "Where does that work happen? What tools, files, or apps are you living in?"
   (docs, email, spreadsheets, slides, CRM, project tool, PDFs, transcripts) — this maps
   directly to the `material/` subfolders and the routing table.

**Time gate (do not skip).** You cannot write the "where the time goes" section or the
time-saved math without a rough time-per-task and frequency for the top 2-3 tasks. People
answer question 3 by telling you *where* or *what steps*, and skip *how long / how often*.
When that happens, **estimate it yourself out loud and ask them to confirm.** A number is far
easier to react to than to invent: *"Pulling a client report is probably ~45 min, weekly per
client, so ~3 a week? Correct me if that's off."* Once confirmed, you have your numbers.

## Round 3 — judgment and standards (adapt)

5. "When you do [their biggest task], what makes the output actually good? A standard, a
   checklist, a format, or your own judgment every time?" This is what separates an agentic
   build from a chatbot one — it becomes `CLAUDE.md`'s "what good looks like" and the starter
   skill's quality bar.
5b. "When AI, or a junior colleague, does [their biggest task] for you, what do they usually
   get wrong? What do you end up fixing every time?" **Do not skip this.** Get 2-3 concrete
   things. These become `CLAUDE.md`'s "What to avoid" section, the starter skill's "What to
   avoid" list, and the trade-offs in `decision-rules.md`. Without this answer, "what to
   avoid" is guessed, and a guessed avoid-list is the fastest way to lose their trust.
6. "How are you using AI today, if at all?" Locates the gap. Do not judge the answer.

## Round 4 — voice and real material (this skill adds this)

7. Ask for a folder first, a paste second. You are running inside Claude Code, which can read
   files on their machine, so use it: "So the folder starts with real evidence, not guesses:
   is there a folder on your computer with past examples of [their biggest task]? Finished
   posts, sent proposals, delivered reports, whatever's closest to your best. Point me at it
   and I'll read a few." One folder gives you three things at once: real voice evidence, a
   count of how many past examples exist (project scoring needs roughly 20), and real files
   for `material/` instead of an empty folder.
   - Read only what they point at. Never scan their disk or open folders they didn't name.
   - Skim 5-10 files, not all of them. Note the count, the formats, and 2-4 verbatim quotes.
   - Before copying anything into `material/`, ask. Some people want copies, some want the
     folder left where it is with a pointer in `material/README.md`. Either is fine.
   If they have no folder handy, fall back: "Then can you paste one or two short pieces? A
   post, a proposal intro, an email you're proud of." One or two real samples still let you
   observe (not invent) their voice. If they have nothing at hand, that's fine — note it, and
   `voice-and-style.md` gets a fill-in prompt instead of a fabricated voice.

If their role is unusual or highly specialized, don't bluff domain expertise. Ask one extra
question about the repeatable part of their work, and be honest later about which parts an
agent takes and which stay human judgment.

## When you're done interviewing

Stop once you can name their **top 3-4 recurring tasks**, have a **confirmed time-per-task and
frequency for the top 2-3** (your estimate they signed off on counts), have a **rough
mechanical-vs-judgment split** for those same tasks, know **what "good" looks like** for the
biggest one, have **2-3 concrete things that go wrong** when someone else does it, and have
(ideally) **a folder of past work or one or two pasted samples**. If you don't have the
numbers or the avoid-list, you are not done.

## What each answer feeds

| Interview answer | Fills |
|---|---|
| Role, field, who you serve | `CLAUDE.md` "what this project is"; `operator-profile.md` |
| Normal week / recurring tasks | Archetype detection; automation opportunities; project candidates |
| Time per task + frequency | Report "where the time goes"; time-back math |
| Mechanical vs judgment split | Report "time you could get back" (agent share); the starter skill's judgment split |
| Tools / where work happens | `material/` subfolders; routing table in `CLAUDE.md`; `domain-map.md` |
| What "good" looks like | `CLAUDE.md` "what good looks like"; starter skill quality bar; `decision-rules.md` |
| What goes wrong when AI / a junior does it | `CLAUDE.md` "what to avoid"; starter skill "what to avoid"; trade-offs in `decision-rules.md` |
| How they use AI now | Report framing (the gap); handoff |
| Folder of past work (or pasted samples) | `voice-and-style.md` (observed, quoted); example count for project scoring; real files or a pointer in `material/` |
