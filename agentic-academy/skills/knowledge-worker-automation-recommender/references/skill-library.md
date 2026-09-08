# Reusable Skills (Skills)

A skill packages a task the person does over and over so it never starts from a blank prompt. It holds the steps, the context to use, and what good output looks like. They run it by name, or Claude picks it up when the task comes up.

A skill lives at `.claude/skills/<name>/SKILL.md`.

## How to pick the first skill to recommend

Look at what repeats in their folders. The best first skill is the task they do most often that has a clear "good" and "bad." Recommend that one, not the most impressive one.

A good skill has five parts, and the recommendation should hint at all five:
1. **What triggers it** (when they run it)
2. **What context it should use** (which of their files)
3. **What steps it follows**
4. **What output format it produces**
5. **What quality standard it meets**

## Common first skills by archetype

These mirror the archetype Skill Libraries the course installs in Week 5. If the person has not installed the bundle yet, point them there first (see skill-bundles.md). If they have, recommend a custom skill for a task the library does not cover.

### Content Creator
| Repeated task | Skill to build |
|---|---|
| Writing from a blank page in their voice | Draft from voice and archive |
| Turning one piece into platform versions | Repurpose across platforms |
| Editing for the same voice and structure issues | Edit for voice and structure |
| Raw notes into a developed idea | Idea expansion from notes |
| Research into a usable brief | Research synthesis to brief |

### Coach / Consultant
| Repeated task | Skill to build |
|---|---|
| Prepping before a client call | Client meeting prep brief |
| Writing proposals from past wins | Proposal draft |
| Turning call notes into next actions | Meeting summary to action items |
| Writing the follow-up email | Client follow-up |
| Pulling case studies from outcomes | Case study extraction |

### Entrepreneur
| Repeated task | Skill to build |
|---|---|
| Synthesizing market research | Market research synthesis |
| Customer interviews into insight | Customer interview to insight |
| Drafting positioning and messaging | Positioning draft |
| Founder content (LinkedIn, investor updates) | Founder content |
| A decision that needs evidence | Decision memo with evidence |

### Knowledge Worker
| Repeated task | Skill to build |
|---|---|
| Meeting notes into a structured summary | Notes to summary |
| The weekly status report | Status report from project files |
| Many sources into one brief | Research brief |
| One update, tailored per audience | Stakeholder update by audience |
| Several projects into one view | Cross-project synthesis |

## Install vs customize vs build

Help the person make the right call:

- **Install** when a ready-made skill in the bundle already does it. Fastest.
- **Customize** when a bundle skill is close but does not match their standards or their files. Adapt it.
- **Build from scratch** when the task is specific to them and nothing covers it.

## Recommending in plain language

Say what the skill removes from their week, not what it is. "A skill that drafts your weekly status report from your project files, so Friday afternoon stops being a scramble" lands. "A status-report skill" does not.
