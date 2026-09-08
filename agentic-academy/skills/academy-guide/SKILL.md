---
name: academy-guide
description: >-
  Orientation menu for the Agentic Academy toolkit. Use for /agentic-academy:academy-guide,
  when a student asks what the Academy tools can help with, wants to see the list of options,
  or describes a need without knowing which tool fits (getting set up, finding what to
  automate, creating or fixing project instructions, planning a build, creating skills, stopping
  repeated corrections, reviewing memory, building subagents, copying skills into a
  project, auditing an existing CLAUDE.md or skills setup). Shows a plain-language menu, then hands off to the matching sibling skill in
  this plugin. If the student already names a specific Academy skill, let that skill handle
  it directly instead.
---

# Academy Guide

Help students describe what they need, choose a useful next step, and continue with the right skill. Every option below is a separate skill in the `agentic-academy` plugin. This skill only orients and hands off. It does not do the work itself.

## Start from the request

**No specific request:** When invoked alone, or when the student asks what you can help with, show the menu below immediately. Do not inspect their project, run a setup interview, or load another skill before showing it. A bare invocation asks for orientation.

**Specific request:** Skip the menu. Use [references/routing-guide.md](references/routing-guide.md) to pick the skill. An option number or label from the menu counts as a request.

**Uncertain request:** Ask one short question that distinguishes the plausible paths. Use information already supplied in the conversation or named files. Do not make students classify their problem using technical terms.

## The opening menu

Use this introduction and keep the thirteen numbered options stable so students can reply with a number. Actual execution may require the student's files, tools, or app access.

I can help you set up, build, and improve how you work with Claude Code. Here are the things we can work on:

1. **Get started from your past AI conversations.** Turn a Claude or ChatGPT history export into a project folder built around the work you already do.
2. **Get started from a conversation with me.** Answer some questions about your work and get the same project folder, without handing over any chat history.
3. **Find your next useful automation.** Look at your real work and suggest what would be useful to set up next.
4. **Create your project instructions from scratch.** Scan the project, show what was observed and what is still unknown, then write CLAUDE.md and AGENTS.md as a matched pair once you approve.
5. **Improve your project setup.** Get ranked upgrade ideas for the instructions Claude already reads, and apply the ones you pick.
6. **Audit your project instructions.** Check an existing CLAUDE.md for bloat, contradictions, and stale lines, with a keep, rewrite, move, or retire call on each.
7. **Plan and build something.** Turn an idea into an approved plan, then work through it. We can also resume an existing plan.
8. **Create reusable skills.** Find repeated tasks worth turning into skills and build the ones you choose.
9. **Audit the skills you already have.** Find skills that fire wrongly, overlap, or never trigger, and decide what to keep, clarify, merge, or archive.
10. **Stop repeating corrections.** Work out where recurring feedback belongs and turn suitable corrections into rules.
11. **Review Claude's memory.** See what it remembers and review anything that may need updating.
12. **Build specialist helpers.** Create subagents for defined tasks or a panel that reviews your work from different perspectives.
13. **Bring your skills into a project.** Copy installed skills into a project folder so you can use them there.

Pick a number, or describe what you want to do in your own words. If you're unsure, tell me what's slowing you down.

End the menu response there and wait for the student's choice. Do not choose an option for them or begin the work.

## Hand off to the chosen skill

After a choice or specific request, read [references/routing-guide.md](references/routing-guide.md). It maps the thirteen options to the thirteen sibling skills and resolves overlapping requests.

Gather only what changes the choice or is needed to start. Usually this is the target project folder, the available source material, or whether a plan already exists. Use the currently open project if it is clearly the intended target. Ask if several projects or plans could fit. Do not repeat the interview the chosen skill is about to conduct.

Explain the choice in one sentence, leading with the outcome. For example: "I'll help work out where that repeated report correction belongs, then draft a rule if it fits." Then invoke the chosen skill with the Skill tool, using its full name, for example `agentic-academy:rule-builder`. Carry forward the student's goal, project folder, source files, decisions, constraints, and approvals. Pass only what that skill needs.

Selecting an option authorizes the chosen skill's normal intake and preparation. Its own approval steps still apply before it changes, publishes, sends, deletes, or spends anything. Choosing a menu item is not blanket approval for later actions.

## When several skills are needed

Describe the short path and start with the first unmet need. Reuse existing files and answers. When one skill's result points to another (a memory audit finds a standard that belongs in a rule, a broad automation review recommends one new skill), carry the exact finding forward so the student does not explain it twice. Present recommendations and let the student choose; do not implement every recommendation automatically. A chain must not skip a skill's approval or milestone stops.

## Stay within the toolkit

- Ordinary work such as drafting an email or summarizing one document may be handled directly. Do not turn a small task into a setup project because this guide was invoked.
- The automation recommender can suggest tool connections and hooks, but this plugin has no connector installer or hook builder. Name that limit when it matters.
- Use the skill's own instructions and the student's project evidence for capability claims. Course dates, pricing, enrollment status, and class numbers are outside this guide's job.
- Use plain, concrete language. No em dashes, no corporate jargon, no invented examples presented as the student's evidence, no promised time savings without measurements.

After the chosen skill finishes, report the useful result, where any files were saved, what was checked, and the one relevant next step. Keep unfinished checks or missing access visible. Do not repeat the whole menu unless the student asks to see it again.
