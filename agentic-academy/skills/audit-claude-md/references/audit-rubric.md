# CLAUDE.md Audit Rubric

Use this rubric to make conservative, evidence-backed decisions. Audit meaningful
instruction blocks rather than chasing a smaller file.

## Evidence labels

- **Observed:** Directly supported by an instruction file, project file, command,
  directory, test, or explicit user confirmation.
- **Inferred:** Strongly suggested by project evidence but not directly stated.
- **Unknown:** Depends on owner judgment or a behavioral comparison.

An inference can support a question or a **Test** decision. It should not be the sole
basis for retiring a meaningful instruction.

## Provenance

Provenance is evidence about why an instruction was added and what failure it was meant
to prevent. Establish it from current project files first. Use targeted version-control
history only for a material block whose purpose remains unclear and only when that
history is available.

Label provenance **Observed**, **Inferred**, or **Unknown** using the evidence definitions
above. Do not infer the original failure from the instruction's wording alone. Age is not
evidence that an instruction is stale, and missing history is not evidence that it is
unnecessary.

## Finding types

### Duplicate

Two blocks control substantially the same behavior in scopes that load together.
Repeated wording is not enough. Confirm that removing one copy does not remove a narrower
scope, exception, or ownership boundary.

### Conflict

Two applicable blocks request incompatible behavior, priorities, formats, tools, or
approval boundaries. Quote or paraphrase both sides and explain when they load together.

### Style-layer conflict

An active output style requests different voice, format, or workflow behavior than a
project instruction covering the same output. Name both sides and say which layer is
project-level. Recommend a change to the project file, never to a user-level style file.

### Vague

The rule cannot be checked because it relies on language such as "be helpful," "use good
judgment," or "make it high quality" without naming observable behavior.

### Stale

The rule names a command, path, tool, model, team, output, or process that project
evidence shows has changed or disappeared.

### Broken route

The instruction points to a missing, inaccessible, external, or circular destination.
Distinguish a missing path from an external path that simply needs authorization.

### Misplaced

The content is useful but lives in a scope that loads too broadly or in the wrong control:

| Guidance | Likely home |
| --- | --- |
| Project fact or always-applicable rule | Root `CLAUDE.md` |
| File-type or subdirectory rule | Path-scoped rule or nested `CLAUDE.md` |
| Multi-step task procedure | Skill |
| Action that must be enforced deterministically | Hook, permission, test, or script |
| Personal project preference | `CLAUDE.local.md` |

This table is a routing guide. Existing project structure and scope take priority.

When a hook, permission, or script in `.claude/settings.json` already enforces the
behavior on every matching tool call, the prose rule is a duplicate of a deterministic
control. Prefer **Rewrite** to point at the enforced boundary, or **Retire** only when the
hook covers every path the rule covers. A hook that runs on a narrower matcher than the
rule's scope is not full coverage.

### Overprescribed

The instruction has a useful intent but dictates a route in more detail than the desired
result requires. Test whether the same intent can be stated as:

- what the finished result looks like
- what it must contain or preserve
- what would make it wrong

Recommend **Rewrite** when an outcome description can replace unnecessary steps without
changing the intended decision. Recommend **Move** when the sequence is a genuinely
repeatable task procedure that belongs in a Skill or narrower control. Recommend **Keep**
when the order encodes a dependency, safety or approval boundary, deterministic check,
or project-specific process that cannot be recovered from the outcome alone. Use
**Test** when the recommendation depends on whether the current model can choose the
route reliably without the steps.

Never compress a procedure merely to make it shorter. Name every constraint preserved in
the proposed outcome description and identify anything the rewrite might lose.

### Overbroad

The rule applies globally even though evidence supports it only for a specific task,
folder, output type, or file pattern.

### Unverified model workaround

The rule was likely added to compensate for earlier model behavior, but the files cannot
show whether the current model still needs it. Recommend **Test**.

### Protected

The rule controls a high-cost failure. Protected categories include:

- safety and privacy
- legal and compliance requirements
- approval before sending, publishing, deleting, purchasing, or changing external data
- source-of-truth precedence
- required output formats
- project-specific terminology or business rules
- commands or checks verified by the project

Protected does not mean immutable. It means changes need direct evidence, explicit
approval, and a test proportional to the risk.

Do not label a dangerous instruction as protected merely because it creates a safety or
privacy risk. Protected means the behavior should be preserved. An instruction that
imports secrets, bypasses approval, or weakens a safety boundary is a risk finding.

## The five decisions

### Keep

Use when the instruction:

- controls useful project-specific behavior
- is supported by current evidence
- is in an appropriate scope
- does not materially conflict with another applicable instruction

### Rewrite

Use when the intent remains useful but the wording is vague, overly broad,
contradictory, or difficult to verify. Preserve the original decision unless the user
approves changing it.

### Move

Use when the instruction is useful but belongs in a narrower rule, nested manual, Skill,
hook, test, or local instruction file. Name the proposed destination and confirm it
exists. If it does not exist, describe the move as a separate proposed change.

### Test

Use when the instruction may be unnecessary with the current model, but project files
cannot prove that. Define one representative task, one expected behavior, and the failure
that would require restoring the instruction.

### Retire

Use only when there is strong structural evidence:

- the same semantic instruction exists in an equally applicable authoritative source
- the named path, command, tool, or process no longer exists and the rule has no
  remaining purpose
- the rule is explicitly expired or superseded
- the user confirms that the behavior is no longer wanted

Do not use **Retire** merely because the rule is long, old, generic, or apparently
understood by the current model.

## Operational priority

Operational priority determines which findings deserve attention first. It is separate
from risk and from the order in which approved patches should be applied.

For conflicts, weigh:

1. **Activation breadth:** whether both blocks load broadly or only in a narrow scope.
2. **Task frequency:** how often project evidence shows the affected work recurs.
3. **Consequence:** the cost of Claude choosing or combining the wrong instruction.

Use **High**, **Medium**, **Low**, or **Unknown**. A broadly loaded rule shows exposure,
not proof that its affected task is frequent. When frequency cannot be supported by
project evidence, say **Unknown** for that factor and prioritize conservatively based on
observed breadth and consequence.

## Risk

- **High:** Safety, external actions, deletion, permissions, compliance, critical
  commands, source precedence, or project-specific rules with costly failure.
- **Medium:** Quality standards, task routing, output format, or a rule used by several
  recurring jobs.
- **Low:** Confirmed duplication, dead links, expired notes, or wording cleanup with a
  narrow effect.

When confidence is low and risk is medium or high, prefer **Keep** or **Test**.

## Conflict precedence

Do not invent a winner. Resolve conflicts using, in order:

1. explicit managed or project precedence already documented
2. the more specific applicable scope
3. the current source of truth named by the project
4. user confirmation

If none resolves the conflict, mark it **Unknown** and ask one focused question.
