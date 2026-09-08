---
name: knowledge-worker-automation-recommender
description: >-
  Analyze a knowledge worker's project folder and recommend Claude Code automations in plain
  language (connected tools, reusable skills, automatic guardrails, specialist delegates, skill
  bundles). Detects the person's work type (content creator, coach/consultant, entrepreneur,
  knowledge worker) from their real files instead of a tech stack. Use when a student or non-
  technical user asks what to set up, what to automate, what to build next, how to improve their
  Claude Code system, or how to get more out of Claude Code for writing, research, client work,
  content, or planning. Read-only: it recommends, it does not build.
---

# Knowledge Worker Automation Recommender

Look at how a person actually works, then recommend the Claude Code automations that will save them the most time on real work.

This skill is for non-technical people: writers, coaches, consultants, founders, analysts, and operators who use Claude Code on their own projects (drafts, client files, research, reports, content). It is NOT for software projects. There is no code to analyze. The signal lives in their folders, filenames, and the kind of work they keep.

**This skill is read-only.** It looks at the project and outputs recommendations. It does NOT create or change any files. The person implements the recommendations themselves, or asks Claude separately to help build them.

## Output Guidelines

- **Plain language first.** Lead with what the automation does for the person in everyday terms. Put the real Claude Code term in parentheses so they learn the vocabulary, but never make the term carry the explanation. "A helper that checks your draft sounds like you before you call it done (a subagent)" beats "a PostToolUse voice-validation subagent."
- **Recommend 1-2 of each type.** Surface the top 1-2 most valuable automations per category. Do not dump a list of twelve. They can ask for more.
- **Meet them where they are.** Use the maturity signals in Phase 1 to skip categories that do not fit yet. Do not recommend a specialist delegate to someone who has not written a project home base. Recommend the next useful thing, not the most advanced thing.
- **Be specific to their work.** A content creator and a consultant should never get the same recommendation. Name their files. "Turn your three best newsletters into a voice reference" lands. "Set up a skill" does not.
- **Name specific products, not categories.** When you recommend a connected tool, name the actual tools, with two or three options so the person can pick the one they already use or prefer. "Connect a meeting tool" is useless. "Connect Granola, Fathom, or Fireflies so your client calls turn into summaries and next actions" is a recommendation. Same for projects (Notion, ClickUp, Monday), research (Tavily, Perplexity, Exa), and so on.
- **Recommend only the gaps.** Use the inventory from Phase 1. If a tool is already connected, a guardrail already exists, or a delegate is already built, do not recommend it again. Acknowledge what they have, then point at what is missing or underused.
- **Go beyond the reference lists.** The reference files cover common patterns. Use web search to find tools and integrations specific to where this person's work actually lives. The connector landscape moves fast, so when you are not certain a named tool has a current connector, do a quick web search to confirm before you present it, and offer the closest working option if it does not.
- **Tell them they can ask for more,** and offer to build any recommendation with them.

## The Five Automation Types

| Plain-language name | Real Claude Code term | What it does for the person | Course week |
|---|---|---|---|
| **Connected Tools** | MCP servers | Lets Claude read, research, create, or update inside the apps their work already lives in (email, docs, notes, calendar, the web) | Week 9 |
| **Reusable Skills** | Skills | Packages a task they do over and over so it never starts from a blank prompt | Week 5 |
| **Automatic Guardrails** | Hooks | Makes Claude do something every time without being asked (run a quality check, protect source files) | Week 8 |
| **Specialist Delegates** | Subagents | A focused helper that sees only what it needs, so big work does not overwhelm the main chat | Week 7 |
| **Skill Bundles** | Plugins / Skill Library | A ready-made set of skills they can install in one move instead of building each by hand | Week 5 |

## Workflow

### Phase 1: Understand the Person's Work

You are not detecting a programming language. You are figuring out two things: **what kind of work this is** (their archetype) and **how far along their Claude Code setup is** (their maturity). Run these read-only commands from the project folder:

```bash
# See the overall shape of the project
ls -la
find . -maxdepth 2 -type d 2>/dev/null | grep -v '/\.' | head -40

# Count the real work files so you know if there's enough past work to draw on
find . -type f \( -name "*.md" -o -name "*.docx" -o -name "*.pdf" -o -name "*.txt" -o -name "*.rtf" \) 2>/dev/null | grep -v '/\.' | wc -l

# Read folder and file names for archetype signals
find . -maxdepth 3 -type f 2>/dev/null | grep -v '/\.' | grep -iE "draft|post|newsletter|episode|script|voice|client|proposal|case.?study|deliverable|discovery|onboard|engagement|market|positioning|interview|customer|strategy|okr|pitch|investor|meeting|status|report|stakeholder|decision|standup|transcript" | head -40

# Check how far along their Claude Code setup already is
ls -la CLAUDE.md .claude 2>/dev/null
ls .claude/skills .claude/agents 2>/dev/null
find .claude/skills -name "SKILL.md" 2>/dev/null | wc -l
test -f CLAUDE.md && echo "HAS home base" || echo "NO home base yet"
```

**Then take inventory of what is already connected and built.** This is the step that keeps you from recommending something they already have. Read it, do not guess at it:

```bash
# Which connected tools (MCP servers) are already wired up
claude mcp list 2>/dev/null
cat .mcp.json 2>/dev/null

# Which automatic guardrails (hooks) already exist
grep -A 30 '"hooks"' .claude/settings.json .claude/settings.local.json 2>/dev/null

# Which specialist delegates (subagents) already exist, and what each one does
for f in .claude/agents/*.md; do echo "=== $f ==="; head -5 "$f" 2>/dev/null; done

# Which skills they already have
ls .claude/skills 2>/dev/null
```

Hold this inventory through Phase 2. The rule is simple: **recommend the gap, not the thing they already have.** If they already run Granola, do not recommend a meeting tool. If a voice-check guardrail already exists, do not recommend one. Recommend the next missing piece, and if something they already built is sitting unused, say so and suggest putting it to work instead of adding more.

**Archetype signals** (what their files tell you about their work):

| If filenames and folders lean toward... | Likely archetype | Their work in one line |
|---|---|---|
| drafts, posts, newsletters, episodes, scripts, voice memos, content calendar, social | **Content Creator** | Turning ideas into published pieces in their voice |
| clients, proposals, case studies, deliverables, discovery, onboarding, engagements, SOWs | **Coach / Consultant** | Turning client work into prep, proposals, and deliverables |
| market research, positioning, customer interviews, product specs, strategy, OKRs, pitch, investor updates | **Entrepreneur** | Turning research and insight into decisions and execution |
| meeting notes, status reports, project plans, stakeholders, decision logs, cross-team updates | **Knowledge Worker** | Turning scattered inputs into reports, summaries, and next actions |

If the signals are mixed, say so and ask one quick question, or recommend for the dominant pattern and note the second.

**Maturity signals** (where they are, which decides what to recommend FIRST):

| What you see | Where they are | Lead your recommendations with |
|---|---|---|
| No `CLAUDE.md`, no `.claude/` | Just starting | A Skill Bundle to install + one Connected Tool. Keep it to two moves. Note that a project home base comes first (Week 2). |
| Has `CLAUDE.md`, no skills | Has context, no automation | Reusable Skills + the archetype Skill Bundle |
| Has a few skills, no agents | Building skills | A repeatable workflow + their first Specialist Delegate |
| Has skills and agents, no hooks | Fairly built out | Automatic Guardrails + Connected Tools |
| Built out across the board | Mature | The 1-2 highest-leverage gaps only, across any category |

Skipping categories that do not fit yet is the point. A short, well-aimed list beats a complete one.

### Phase 2: Generate Recommendations

Generate across the five types, but only include the ones that fit their archetype and maturity. For each, the reference file holds the full detection-to-recommendation table.

#### A. Connected Tools (MCP servers)

See [references/connected-tools.md](references/connected-tools.md) for the full list of named tools by job, with alternatives and connector notes.

Name specific products. Give two or three options per job so the person can pick what they already use. Skip anything the Phase 1 inventory shows is already connected. When you are not certain a named tool has a current connector, confirm with a quick web search before presenting it.

| What you see in their work | Specific tools to name (they pick one) |
|---|---|
| Lots of meetings, calls, or transcripts | **Granola, Fathom, Fireflies, or Otter** so calls become summaries and next actions |
| Manages many projects or tasks | **Notion, ClickUp, Monday, Asana, or Linear** so Claude reads project state and updates it |
| Work lives in Google apps | **Google Workspace (Docs, Gmail, Drive, Calendar, Sheets)** so Claude works inside them, not on copies |
| A notes or knowledge base | **Notion, Obsidian, or Coda** so Claude reads the right page for a task |
| Research is core to the work | **Tavily, Perplexity, or Exa** so Claude pulls live, cited sources |
| Manages clients or a sales pipeline | **HubSpot, Attio, or Salesforce** so Claude pulls client and deal context |
| Publishes content | **Typefully or Buffer** so drafts get scheduled without copy-paste |
| Produces visuals or decks | **Canva or Figma** so Claude can create and edit designs |
| Tracks data in spreadsheets or tables | **Airtable or Google Sheets** so Claude reads and updates records |

#### B. Reusable Skills (Skills)

See [references/skill-library.md](references/skill-library.md).

The fastest win is a skill for the one task they do most. Look at what repeats in their folders.

| If their repeated task is... | Skill to recommend building |
|---|---|
| Writing in their own voice from a blank page | **Draft from voice and archive** |
| Turning one piece into platform versions | **Repurpose across platforms** |
| Prepping for a client before a call | **Client prep brief** |
| Writing proposals from past wins | **Proposal draft** |
| Turning messy notes into a structured summary | **Notes to summary** |
| Pulling research into one usable brief | **Research brief** |
| A weekly report they rebuild every time | **Status report from project files** |

#### C. Automatic Guardrails (Hooks)

See [references/guardrails.md](references/guardrails.md).

Guardrails matter once they trust Claude with real output. Frame them as "Claude does this every time, so you stop having to remember."

| What you see | Guardrail to recommend |
|---|---|
| Voice-sensitive writing | A voice check that runs before a draft is called done |
| A report or deliverable with a strict format | A format check before it is handed off |
| Important source files they reuse (style guide, client records) | Protect those files from accidental edits |
| A quality bar they keep re-explaining | A checklist that runs automatically at the end of a task |

#### D. Specialist Delegates (Subagents)

See [references/delegates.md](references/delegates.md).

Recommend a delegate when work is big enough that the main chat loses the thread, or needs a fresh pair of eyes.

| What you see | Delegate to recommend |
|---|---|
| Drafts that drift out of their voice | A voice-check delegate that reads with fresh eyes |
| Research that spans several angles | Parallel research delegates, then one that combines the findings |
| Proposals or deliverables that need review | A review delegate that scores against their own quality bar |
| Three updates that become one report | Parallel summarizers, then one that writes the combined report |

#### E. Skill Bundles (Plugins / Skill Library)

See [references/skill-bundles.md](references/skill-bundles.md).

For someone early on, a bundle is the highest-leverage single move: ten working skills on day one.

| Archetype | Bundle to recommend |
|---|---|
| Content Creator | The **Content Creator Skill Library** (drafting, editing, repurposing, ideation, research) |
| Coach / Consultant | The **Coach/Consultant Skill Library** (prep, proposals, follow-ups, case studies) |
| Entrepreneur | The **Entrepreneur Skill Library** (research, positioning, founder content, decision memos) |
| Knowledge Worker | The **Knowledge Worker Skill Library** (notes to summary, status reports, briefs, updates) |

### Phase 3: Output the Recommendations Report

Format it clearly and warmly. Include only the categories that fit. Skip the rest without apology. Lead each recommendation with the plain-language win, then the real term, then the concrete first step.

```markdown
## Your Claude Code Setup: What to Build Next

I looked at your project and here is what I found, plus the handful of automations that will save you the most time on your real work.

### What your work looks like
- **Work type**: [Content Creator / Coach-Consultant / Entrepreneur / Knowledge Worker]
- **Where you are**: [just starting / has a home base / building skills / fairly built out]
- **What I saw**: [the actual files and folders that told you this]
- **Already set up**: [connected tools, guardrails, and delegates the inventory found, so they know these were skipped on purpose, not missed]

---

### 🔌 Connect Claude to where your work lives (Connected Tool)

**[tool name]**
**Why it helps you**: [specific to their files, in plain language]
**First step**: [the one command or action to set it up]
**We cover this in**: Week 9

---

### 🎯 Stop starting from a blank page (Reusable Skill)

**[skill name]**
**Why it helps you**: [the repeated task it removes]
**First step**: Build a skill at `.claude/skills/[name]/SKILL.md`, or ask me to draft it with you
**We cover this in**: Week 5

---

### 🛟 Let Claude check its own work (Automatic Guardrail)

**[guardrail name]**
**Why it helps you**: [the thing they keep having to remember, now automatic]
**We cover this in**: Week 8

---

### 🤝 Hand off the big stuff (Specialist Delegate)

**[delegate name]**
**Why it helps you**: [the work that overwhelms the main chat today]
**We cover this in**: Week 7

---

### 📦 Get ten skills in one move (Skill Bundle)

**[bundle name]**
**Why it helps you**: [immediate firepower for their archetype]
**We cover this in**: Week 5

---

**Want more options for any of these?** Just ask, like "show me more ways to connect my tools" or "what other skills would help me."

**Want to build one of these together right now?** Tell me which one and I'll walk you through it.
```

## Decision Framework

### When to recommend a Connected Tool (MCP server)
- Their work clearly lives in another app (email, docs, notes, calendar) and copy-pasting into Claude is the bottleneck.
- Research is part of the job and Claude needs live sources.
- They publish, and the last mile is manual.
- Only recommend a tool that helps Claude read, research, create, publish, or update something they already use. Do not recommend tools for their own sake.

### When to recommend a Reusable Skill
- A task shows up again and again in their folders (weekly report, draft, prep brief).
- They keep re-explaining the same instructions.
- The output is file-shaped and has a clear "good" and "bad."

### When to recommend an Automatic Guardrail
- They have a quality bar they keep restating.
- There are source files they must not let Claude overwrite.
- A deliverable has a format that has to be right every time.

### When to recommend a Specialist Delegate
- Work is big enough that the main chat gets confused or loses context.
- A task needs fresh eyes (a reviewer that has not seen the draft being written).
- Several research angles could run at once and then be combined.

### When to recommend a Skill Bundle
- They are early and want firepower fast.
- They match an archetype with a ready-made library.
- They would rather start from ten working skills than build from scratch.

## A Few Things to Get Right

- **No jargon walls.** If a sentence only makes sense to a developer, rewrite it. Test: would a smart friend who has never coded understand the first line of each recommendation?
- **Respect where they are.** Recommending advanced things to a beginner is not helpful, it is discouraging. Two well-aimed moves beat five.
- **Name their real files.** Generic advice reads as "you did not actually look." Specific advice reads as "this was built for me."
- **Stay read-only.** This skill recommends. It does not build. Offer to build at the end, but do not start editing files inside this skill.
- **One project, deep.** Recommend for the project they pointed you at, not their whole life. Depth on one workflow beats breadth across many.
