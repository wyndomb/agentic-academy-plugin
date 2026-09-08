# Connected Tools (MCP servers)

A connected tool lets Claude reach into an app the person already uses: their meeting recorder, their project tool, their docs, their notes, their CRM, the web. Instead of copying things in and pasting results out, Claude reads, researches, creates, or updates right where the work happens.

This file names specific products on purpose. "Connect a meeting tool" is not a recommendation. "Connect Granola, Fathom, or Fireflies" is. Always name two or three real options per job so the person can pick the one they already use or already pay for.

## Two rules before you recommend

1. **Recommend the gap, not what they have.** Check the Phase 1 inventory (`claude mcp list`, `.mcp.json`). If a tool is already connected, do not recommend it. If they already run Granola, do not pitch a meeting tool.
2. **Verify the connector exists before you present it.** The connector landscape changes fast and beyond this skill's knowledge cutoff. When you are not certain a named tool has a current MCP server, do a quick web search to confirm. If there is no MCP yet, say so and offer the closest option that does, or note it can connect through its own API or CLI.

Connectors come in a few shapes. Mention the shape so expectations are right:
- **Official or community MCP server** (the cleanest, when it exists).
- **API or CLI** (works, slightly more setup).
- **Read the files directly** (for local tools like Obsidian, Claude Code already reads the folder. No connector needed.)

## Named tools by job

### Record and summarize meetings
For anyone with a lot of calls, where notes are the raw material.

| Tools to name | Recommend when you see |
|---|---|
| **Granola, Fathom, Fireflies, Otter, tl;dv, Read.ai** | Folders of meeting notes or transcripts, client or discovery calls, standup notes |

**What it unlocks**: calls turn into structured summaries with decisions, owners, and next actions, instead of the person re-reading a transcript. For consultants, the last call becomes prep for the next one.

### Manage projects and tasks
For anyone juggling many projects, clients, or workstreams.

| Tools to name | Recommend when you see |
|---|---|
| **Notion, ClickUp, Monday, Asana, Linear, Todoist, Trello** | Project plans, task lists, status tracking, multiple active clients or workstreams |

**What it unlocks**: Claude reads real project state (what is done, what is blocked, who owns what) and can update it, so status reports and next actions come from live data, not memory.

### Work inside docs, email, and files
For people whose work lives in Google or Microsoft apps.

| Tools to name | Recommend when you see |
|---|---|
| **Google Workspace (Docs, Gmail, Drive, Calendar, Sheets, Slides), Microsoft 365 (Outlook, Word, OneDrive)** | Drafts and reports in Docs, heavy email back-and-forth, files scattered in Drive, calendar-driven work |

**What it unlocks**: Claude drafts inside the actual document, triages and replies to email with real thread context, finds the right file, and preps around real calendar events.

### Notes and knowledge base
For people who keep a second brain or reference library.

| Tools to name | Recommend when you see |
|---|---|
| **Notion, Obsidian, Coda, Confluence** | A notes vault, a knowledge base, reference docs, a style guide |

**What it unlocks**: Claude reads the right page for the task. Note for **Obsidian**: it is local Markdown, so Claude Code already reads it directly when the vault is in the project folder. No connector needed, which is a nice early win.

### Research the web with sources
For anyone whose work has a real research component.

| Tools to name | Recommend when you see |
|---|---|
| **Tavily, Perplexity, Exa** | Market or competitor research, research briefs, literature reviews, founder or customer research |

**What it unlocks**: Claude pulls live, current sources and cites them, instead of guessing from training data. Research stays current and trustworthy.

### Clients and sales pipeline
For consultants, coaches, and founders who track relationships.

| Tools to name | Recommend when you see |
|---|---|
| **HubSpot, Attio, Salesforce, Pipedrive** | A client roster, deal stages, a sales pipeline, recurring proposals |

**What it unlocks**: Claude pulls client and deal context into prep, proposals, and follow-ups, so nothing is rebuilt from memory.

### Customer and user research
For entrepreneurs and product people.

| Tools to name | Recommend when you see |
|---|---|
| **Dovetail, Notion, plus an interview transcriber (Otter, Fireflies)** | Customer interviews, user research, feedback notes |

**What it unlocks**: interviews become themes and quotes Claude can pull into positioning and copy.

### Publish and distribute content
For creators and founders who put work out into the world.

| Tools to name | Recommend when you see |
|---|---|
| **Typefully, Buffer, Hypefury** | Finished posts that get copy-pasted out, repurposing into many platforms |

**What it unlocks**: drafts get scheduled and queued without the manual last mile. One piece becomes platform versions, ready to go.

### Visuals and decks
For anyone who produces design or presentations.

| Tools to name | Recommend when you see |
|---|---|
| **Canva, Figma** | Carousels, thumbnails, decks, branded visuals |

**What it unlocks**: Claude can create and edit designs instead of handing off a text brief.

### Spreadsheets and structured data
For people who track things in tables.

| Tools to name | Recommend when you see |
|---|---|
| **Airtable, Google Sheets** | Trackers, content calendars, client databases, simple dashboards |

**What it unlocks**: Claude reads the numbers and updates rows, so reporting and tracking stop being manual.

## Lead with these, by archetype

Recommend at most one or two. Pick the highest-leverage gap for their work.

| Archetype | Lead with |
|---|---|
| **Content Creator** | Research (Tavily / Perplexity) + Publishing (Typefully / Buffer). Visuals (Canva) if they post carousels. |
| **Coach / Consultant** | A meeting tool (Granola / Fathom / Fireflies) + a CRM (HubSpot / Attio). |
| **Entrepreneur** | Research (Tavily / Perplexity / Exa) + customer research (Dovetail) or a project tool. |
| **Knowledge Worker** | A project tool (Notion / ClickUp / Asana / Linear) + meetings (Granola / Fathom). |

## Setup notes for non-technical people

- Connect one tool at a time. Get it working and actually used before adding a second.
- Connect a tool only when a workflow they already built needs it. A tool sitting unused is clutter, not progress.
- This is Week 9 territory in the course. If the person is early, name the tool that fits but note it as "later," not "now."
