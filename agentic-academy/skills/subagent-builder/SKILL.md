---
name: subagent-builder
description: >-
  Interview the user and build custom subagents as files in .claude/agents/. Reads the project
  first and suggests subagents worth building based on the work that actually happens there. Use
  this skill whenever the user asks to build, create, design, or set up a subagent or custom
  agent; asks what subagents they should build; asks "should this be a subagent?"; wants to hand
  part of their work to a separate worker; or wants to turn a repeated handoff into something they
  can call by name. Also use it when the user wants a panel of several subagents reviewing the
  same piece of work, or a skill that runs several subagents and combines what they return.
---

# Subagent Builder

Help the user build subagents they will actually keep using.

A subagent is a small Markdown file in `.claude/agents/`. It runs in its own conversation, sees only the task and material handed to it, does its part, and returns a result. It does not see the main conversation's history. That fresh start is the whole point: it is why a subagent catches what the main conversation has gone blind to, and it is also why a badly designed handoff fails.

Writing the file is the easy part. You can generate one from a sentence. The hard parts are choosing what deserves a subagent at all, and writing a handoff specific enough to survive being done by someone who was not in the room. This skill spends its effort there.

The user judges. You find, ask, draft, and push back. Never write a file into `.claude/agents/` without showing it first and getting a yes.

## Two ways in

**Discovery mode:** the user asks what subagents they should build, hands over a project, or does not yet know what to hand off. Read the project, propose candidates, then interview on the ones they pick. Start at "Discovery mode".

**Direct mode:** the user already knows what they want built. Skip discovery and start at "The interview".

**Panel mode:** the user wants several subagents on the same piece of work, or a saved skill that runs them together and combines results. Go to "Panel mode" at the end of this file. Build the individual subagents through the normal interview first, then come back for the combining half.

If the user opens with "build me a subagent" but cannot say what it does, treat that as discovery mode.

---

## Discovery mode

### 1. Read the project before suggesting anything

Do not suggest subagents from general knowledge about what people usually automate. Suggestions have to come from this project's real work, or the user gets a generic list they ignore.

Read, in this order:

1. `CLAUDE.md` or `AGENTS.md` at the project root, and any nested ones. This tells you what the project is, what the standards are, and what the user keeps having to repeat.
2. The folder structure. Names and what lives where. Folders with many similar files are where repeated work happens.
3. `.claude/agents/` if it exists. What already exists, so you do not propose a duplicate.
4. `.claude/skills/` and `.claude/commands/` if they exist. A job already covered by a skill usually does not need a subagent, and knowing what is there prevents proposing both.
5. Any rules in `.claude/rules/`. Standards written down here are exactly what a review subagent would check against.
6. Three to five real work files from the biggest folders. You are looking for what the output actually looks like, not reading everything.

While reading, look for these four signals. They are where real subagents come from:

- **A standard written down but checked by hand.** Anywhere CLAUDE.md or a rules file says "never do X" or "always include Y", there is a review subagent that could check it.
- **A stage that repeats across many files.** Same folder, same shape, many files, means the work happens often enough to be worth saving.
- **A big side task that fills the conversation.** Research sweeps, archive checks, competitor scans. Work whose intermediate output the user never needs to see, only the conclusion.
- **A perspective the user keeps having to fake.** Anywhere they argue with themselves, defend a decision to an imagined critic, or ask "how would this land with someone who does not already know this."

### 2. Propose, and keep it short

Present three to five candidates. Not more. A project with three subagents that get used beats one with ten that were built once.

For each candidate, exactly this shape:

```
**<name>**: <perspective or employee>
- Does: <the job in one line>
- Returns: <what lands back in the main conversation>
- Why separate: <what the fresh start buys, in one line>
- Saw this in: <the actual file, folder, or CLAUDE.md line that suggested it>
```

The last line is required. A candidate you cannot ground in something you actually read is a guess, and guesses become files nobody opens.

If the project genuinely does not have three good candidates, propose two, or one. Say that the rest of what you found is better served by a skill, or by asking in plain language when it comes up. Padding the list to hit a number is how the user ends up with dead files.

Then ask which they want to build. Interview them one at a time.

---

## The interview

Ask these in order. One at a time, waiting for the answer, not as a block of six questions the user has to work through at once. Each answer changes what you ask next.

Do not move to the next question until the current answer is specific enough to build from. Pushing back here is the job.

### Q1. What should this subagent do?

Get the job in one or two sentences.

**Push back when the answer is a topic rather than a task.** "Help with my newsletter" is a topic. "Read a finished draft and list every claim that needs a source" is a task. The test: could someone who was not in this conversation read the answer and know when they were done?

If the answer is a topic, ask what the subagent hands back when it finishes. That question usually converts a topic into a task on its own.

### Q2. Is this a perspective or an employee?

Two kinds, and the answer changes how the file gets written.

**A perspective** brings a point of view to work that already exists. A customer, an expert, a competitor, a skeptic, a first-time reader. The user already knows the work; they need someone else's eyes on it. A perspective reports and does not edit.

**An employee** does a piece of the work itself. Research, generation, production, review against a checklist. The user knows what needs doing and wants it done without them.

The dividing question: is the work already done, or not? Finished work that needs judging points to a perspective. Work that has not been done yet points to an employee.

Say which one you think it is based on their Q1 answer, and let them correct you. Do not make them classify it cold.

This matters because it decides the shape of the instructions. Perspectives get a stance to hold and a report-only boundary. Employees get a procedure and a defined output.

### Q3. What does it need to see?

Two parts, and both matter.

**The material:** what gets handed to it each time it runs. A draft, a file path, a pasted block of text, a topic.

**The standing context:** files it should read every time before doing the job. Standards, style guides, rules files, examples of good output. These are what let a subagent apply the user's judgment instead of generic judgment.

If the project has a CLAUDE.md, rules files, or a style guide, name the specific ones and ask whether this subagent should read them. Do not make the user remember what exists. You just read the project; use it.

Be honest about the limit here: a subagent does not inherit the main conversation. Anything not in the material or the standing context is not available to it. If the user describes something the subagent needs to know that lives nowhere but their head, that is a real problem to solve now, either by writing it into the instructions or by pointing out that this file needs to exist first.

### Q4. What exactly does it return?

The most-skipped question and the one that decides whether the subagent is useful.

**Push back on any answer that is a category rather than a shape.** "Feedback" is a category. "A list of every passage a first-time reader would stumble on, each with the sentence that caused it and a suggested fix" is a shape.

Ask: what lands back in your main conversation, and what do you do with it next? If the user cannot say what they would do with the result, the handoff is not designed yet.

Also settle length and form. A ranked list of five. A short report with three named sections. A yes or no with reasoning. Vague result definitions produce subagents that return essays the user skims and ignores.

### Q5. What should it leave alone?

The boundary line. Usually one of:

- Report only, do not edit any file.
- Do not rewrite, suggest changes and let me decide.
- Stay inside this folder.
- Do not touch the source material.

For perspectives, report-only is almost always right, and you can suggest it directly.

Say the honest thing once, briefly: these are instructions in the file, not hard locks. They work because the subagent follows its instructions. Real restrictions on what a subagent can touch are a separate mechanism, and the user does not need it to build this.

### Q6. Which model should run it?

Recommend, do not just present options.

Most subagents run well on **Sonnet**, and that is the default to suggest. It is the right pick for a defined job against standards that are already written down.

Suggest **Opus** when the subagent has to weigh things that genuinely conflict and make a call. A skeptic arguing against the user's own decision. A synthesizer resolving disagreement between several other subagents. Judgment under real ambiguity is where the stronger model earns its cost.

Suggest **Haiku** when the job is pulling out facts with no judgment. Extracting headings, listing links, collecting metadata.

Give your pick with the one-line reason, then let them override.

### Q7. When should Claude reach for this on its own?

The description field decides whether the subagent ever gets used without being named. A weak description means the user has to remember it exists and call it by name every time, which for most people means they stop using it within two weeks.

Ask: what would you be saying or doing at the moment you would want this to fire?

Take their answer and write a description that includes the trigger phrasing they actually use, not a summary of the job. Then show it to them and ask if that is how they would phrase it.

---

## Writing the file

Show the complete file in the conversation before writing anything to disk.

Match the format that the project's existing `.claude/agents/` files already use. Read one before writing if any exist. If the folder is empty, use this shape:

```markdown
---
name: <kebab-case, matches the filename>
description: <when Claude should reach for this, in the user's own trigger language>
model: <sonnet | opus | haiku>
---

<One or two sentences: what this subagent is and what it is not.>

## Read first

<The standing context files, listed. Skip this section if there are none.>

## What you do

<The job. For a perspective: the stance to hold and what to look for.
For an employee: the procedure, in order.>

## What you return

<The exact shape of the output. Be specific enough that two runs
produce the same structure.>

## Boundaries

<What it leaves alone.>
```

Two rules for the frontmatter:

**The `name` must match the filename.** `first-time-reader` lives in `first-time-reader.md`.

**Do not add fields the user did not ask for.** No tool restrictions, no extra settings. If the project's existing agent files carry a field consistently, such as a color, match it and say you matched it. Every line in the file should trace back to something the user said or a file that exists.

Then walk the mapping out loud, briefly. Q1 and Q4 became the job and the return shape. Q3 became the read-first list. Q5 became the boundary. This is the inspection step, and it is where invented lines get caught. Ask the user to confirm before you write.

Write to `.claude/agents/<name>.md` in the project. Mention that `~/.claude/agents/` is the option if they want it available in every project, but default to the project folder.

---

## After the first run

Once the user has run it on real material, ask these three:

1. Did it return the result the handoff promised?
2. What did it need that it did not have?
3. What did it receive that it never used?

The third one is the sharp one. Handing a subagent everything just in case feels safe and usually means the handoff was never really designed. Cutting unused material is how a subagent gets fast and stops wandering off its job.

If the answers point to a fix, edit the file with them. A subagent that has been through one real run and one revision is the one that survives.

---

## Panel mode

Several subagents on the same piece of work, plus something that combines what they return.

Build each subagent through the normal interview first. Perspectives usually, and they should be genuinely different from each other. Five reviewers who all check quality return five versions of the same feedback. A customer, a skeptic, an expert, a first-time reader, and a competitor return five different things, and the differences are the point.

Then build the coordination skill. It has two halves.

**The easy half** is sending the work out: hand the same material to each subagent, run them together.

**The half that makes it worth saving** is what the main conversation does with what comes back. Do not write a skill that stops at the easy half. A skill that returns five reviews stacked in a list has done nothing the user could not do by asking.

Before writing the coordination skill, get answers to these:

1. When two subagents raise the same concern, what does that mean and how should it be treated?
2. When two subagents disagree, how does the main conversation decide, or does it surface the disagreement and leave the call to the user?
3. What makes one recommendation rank above another for this user?
4. What does the final output look like? How many items, in what order, with what attached to each?

Those four answers become the combine instruction, and the combine instruction is the actual content of the skill. Write it as explicit steps: find agreement across responses, surface disagreements with both positions named, apply the ranking standard, produce the final list.

A useful check before calling it done: could this skill return a result the user disagrees with? If the answer is no, because it only stacks everything up and stays neutral, it is not making judgment calls yet, and it needs the ranking standard written in more sharply.

---

## When a subagent is the wrong answer

Say so. Routing honestly matters more than producing a file.

**It is a skill, not a subagent,** when the job needs the main conversation's context to make sense, or when it is a procedure the user wants to run themselves rather than hand off. A subagent starts fresh and cannot see the conversation. If the job only works with everything that came before, handing it off breaks it.

**It is a rule, not a subagent,** when it is a standard that should apply automatically to a kind of file, with nothing to hand off and nothing to return.

**It is nothing,** when the job happens rarely. A subagent for something that comes up once a year costs more to remember than to just ask for.

That last one is worth checking early, before the interview rather than after. If the user cannot name a real occasion in the last month when they needed this, say so and ask whether it is worth building yet. Better to catch it at the first question than after they have a file they never open.
