# Archetype detection and folder scaffolds

The cohort is built around four kinds of work. The underlying system is the same; the
folder, the context files, and the recommended project change by archetype. Detect the
dominant archetype from the chat evidence, scaffold for it, and note any secondary.

Read this in Phase 2 (portrait) and Phase 4 (assembly).

## How to detect

Read `digest/samples.md` and the repeated openers in `digest/digest.json`. Match the
*work the person actually brings to AI*, not their job title. Signals below.

### Content Creator
For newsletter writers, bloggers, podcasters, YouTubers, social writers, creators.
- Signals: drafting, editing, repurposing, "turn this into a thread/post", headlines,
  voice/tone requests, audience, content calendar, "rewrite in my voice".
- They care about: voice fit, originality, platform fit, publishing cadence.

### Coach / Consultant
For solo consultants, coaches, agency owners, advisors, service providers.
- Signals: clients (often named), proposals, discovery calls, follow-up emails,
  deliverables, frameworks, prep for meetings, case studies, onboarding.
- They care about: client relevance, professionalism, deliverable standards, reuse.

### Entrepreneur
For founders, product managers, marketers, operators building a business.
- Signals: market/customer research, positioning, competitors, pitch, strategy,
  product specs, pricing, founder content, "should we...", go/no-go decisions.
- They care about: strategic usefulness, evidence quality, execution readiness.

### Knowledge Worker
For analysts, researchers, project managers, team leads, corporate professionals.
- Signals: meeting notes, status reports, stakeholder updates, synthesizing sources,
  decision memos, exec summaries, action items, cross-team reporting.
- They care about: completeness, accuracy, structure, action clarity.

If two fit, pick the one with more conversation volume for the scaffold; record the other
as "secondary" in `operator-profile.md`.

## Folder scaffolds by archetype

Every archetype gets the same top-level shape (CLAUDE.md, context/, project/, material/,
chat-xray-report.md, start-here.md). What changes is the `material/` subfolders and the
emphasis in the context files. Create the `material/` subfolders below as empty dirs with
a one-line README each, so the person knows where their files go.

### Content Creator — `material/`
- `published/` — past posts/episodes (the voice + quality corpus)
- `drafts/` — in-progress pieces
- `ideas/` — raw notes, voice memos, sparks
- `audience/` — audience research, reader questions, survey data
- `swipe/` — references, examples they admire

### Coach / Consultant — `material/`
- `clients/` — one folder per active client (notes, history)
- `offers/` — services, proposal templates, pricing
- `frameworks/` — their methods and IP
- `deliverables/` — past deliverables that define "good"
- `calls/` — meeting notes and transcripts

### Entrepreneur — `material/`
- `customers/` — interviews, support themes, customer language
- `market/` — research, competitor notes, industry context
- `product/` — specs, roadmap, positioning
- `strategy/` — plans, decisions, OKRs
- `content/` — founder posts, investor updates

### Knowledge Worker — `material/`
- `projects/` — one folder per active project
- `meetings/` — notes and transcripts
- `reports/` — past reports/templates that define the format
- `research/` — sources and briefs
- `decisions/` — decision logs

## Context emphasis by archetype

When filling `context/*.md`, weight toward what the archetype relies on:
- **Creator**: `voice-and-style.md` is the centerpiece — get the voice exact.
- **Consultant**: `domain-map.md` should capture clients and deliverable standards.
- **Entrepreneur**: `decision-rules.md` and `domain-map.md` (market, customers, product).
- **Knowledge Worker**: `decision-rules.md` (report formats, level of detail) and
  `domain-map.md` (stakeholders, projects).
