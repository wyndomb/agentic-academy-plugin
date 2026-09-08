# Getting a Claude conversation export

Walk the person through this if they haven't exported yet.

1. Go to **claude.ai** and sign in.
2. Click the account menu (bottom-left, their name/initials) → **Settings**.
3. Open **Privacy** (or **Account**, depending on the current UI).
4. Find **Export data** and request the export.
5. Anthropic emails a download link, usually within minutes to a few hours.
6. The download is a `.zip`. Unzip it and keep the **whole folder** — the parser uses
   several files, not just one:
   - **`conversations.json`** — the chat history.
   - **`memories.json`** — saved memory + per-project memories. **This is the highest-signal
     file; don't skip it.** It often carries more usable portrait detail than the
     conversations themselves, and it rescues thin or recent chat histories.
   - **`users.json`** — the person's name (used to personalize the workspace).
   - `projects.json` — optional; not currently parsed, fine to leave in the folder.

Tell them to unzip it and note the folder, e.g. `~/Downloads/claude-export/`, then point the
parser at the folder (it finds and sorts the files itself).

## Format the parser expects (for reference)

`conversations.json` is a JSON array of conversation objects. Each looks roughly like:

```json
{
  "uuid": "...",
  "name": "Conversation title",
  "created_at": "2026-01-05T10:00:00.000000Z",
  "updated_at": "...",
  "chat_messages": [
    {
      "uuid": "...",
      "sender": "human",
      "created_at": "2026-01-05T10:00:00.000000Z",
      "text": "the message text",
      "content": [ { "type": "text", "text": "..." } ]
    }
  ]
}
```

The parser reads `sender` ("human" / "assistant"), and message text from either `text`
or the `content` blocks. It tolerates missing fields.
