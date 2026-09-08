---
name: sync-skills
description: >-
  Copy every skill the user has installed into a project's .claude/skills/ folder, so the skills
  travel with that project as editable, checked-in copies. Use when the user asks to bring, copy,
  or sync their installed skills into a project, wants a portable copy of their skills inside a
  repo, or asks why a skill works in one project but not another. This is a one-time copy, not
  ongoing synchronization; re-run it after installing or updating skills to refresh the copies.
  Verify the real source path before copying and confirm before replacing existing copies.
---

# Sync Claude Skills Into a Project

This skill copies all of the user's installed Claude skills into a target
project's `.claude/skills/` folder. Placing skills there makes them available
as project-level skills for that workspace, and gives the user a portable,
checked-in copy that travels with the repo.

Skills the user has installed live in a **read-only cache** managed by Claude.
This skill reads from that cache and writes plain, editable copies into the
project. Because they're copies, they don't auto-update — re-run this skill any
time the user installs or updates skills and wants the project refreshed.

## What you need before running

1. **The target project folder** — where the skills should land. Default to the
   folder the user currently has connected / is working in. If it's ambiguous
   (e.g. they mention "my other project"), ask which folder.
2. **The skills cache path** — the read-only directory that contains the
   installed skill folders. See "Finding the cache" below.

## Finding the cache

The cache is the directory whose subfolders are the installed skills (each has a
`SKILL.md` inside). You can locate it without guessing:

- The available-skills list in your context shows a `location` (or base
  directory) for each skill, e.g. `.../plugins/<hash>/skills/<skill-name>`. The
  **parent** of those per-skill paths is the cache root. Every skill shares the
  same parent, so any one of them reveals it.
- In the bash sandbox this read-only cache is typically mounted at a path ending
  in `/.claude/skills/` (note: this is the *system* cache mount, not the target
  project's `.claude/skills`). Confirm by listing it — it should contain many
  skill folders, each with a `SKILL.md`.

Translate the path you found into the form the bash tool expects (use the
path-mapping shown in your environment), then verify before copying:

```bash
ls -1 "<CACHE>" | head            # should list skill folder names
ls "<CACHE>"/*/SKILL.md | head    # confirms they're real skills
```

## Running the sync

Use the bundled script — it creates the destination, copies every folder that
contains a `SKILL.md`, makes the copies writable (the source is read-only), and
prints a summary. Pass the cache path and the **project root** (the script
appends `.claude/skills` itself):

```bash
bash scripts/sync_skills.sh "<CACHE>" "<PROJECT_ROOT>"
```

Example:

```bash
bash scripts/sync_skills.sh \
  /sessions/<id>/mnt/.claude/skills \
  /sessions/<id>/mnt/my-other-project
```

If the script can't run for any reason, the equivalent by hand is: make
`<PROJECT_ROOT>/.claude/skills`, then for each folder in the cache that has a
`SKILL.md`, copy it in and `chmod -R u+w` the copy.

## Handling write protection

Some environments protect the project's `.claude/` path or block deletes. If a
copy or cleanup fails with "Operation not permitted" or a blocked-path error:

- Run the copy through the **bash tool** (it usually can write where the file
  tools can't), and
- If a delete is blocked, request delete permission for that folder rather than
  telling the user it's impossible.

## After running

Report back plainly: how many skills were copied and the destination path. Then
list the skill names so the user can confirm everything they expected is there.
Remind them, briefly, that these are static copies and they can re-trigger this
skill to refresh after installing or updating skills.
