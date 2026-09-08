# Getting a ChatGPT conversation export

Walk the person through this if they haven't exported yet.

1. Go to **chatgpt.com** and sign in.
2. Click their profile (top-right) → **Settings**.
3. Open **Data controls**.
4. Click **Export data** → **Export**, then confirm.
5. OpenAI emails a download link (can take a few minutes to a day). The link expires, so
   download promptly.
6. The download is a `.zip`. Unzip it and keep the **whole folder**:
   - **`conversations.json`** — the chat history.
   - **`user.json`** — may hold custom instructions / profile text the parser can use.
   - (`chat.html`, `message_feedback.json`, etc. — not required.)

### Also grab your saved memory

ChatGPT's persistent memory isn't always in the data export. To capture it (high-signal,
worth the two minutes):
1. **Settings → Personalization → Memory → Manage** — copy the saved memories into a plain
   text or markdown file named **`memory.md`** (or `memories.json`) and drop it in the export
   folder.
2. **Settings → Personalization → Custom instructions** — copy both boxes ("what should
   ChatGPT know about you" and "how should ChatGPT respond") into the same file.

The parser picks up any `memory*.json`/`memories.json` and custom-instruction fields it
finds. Memory is often the richest portrait signal, so don't skip this.

Tell them to unzip it and note the folder, e.g. `~/Downloads/chatgpt-export/`, then point the
parser at the folder.

## Format the parser expects (for reference)

ChatGPT's `conversations.json` is a JSON array of conversation objects. Each conversation
stores its messages as a **tree** under `mapping` (not a flat list):

```json
{
  "title": "Conversation title",
  "create_time": 1704450000.0,
  "mapping": {
    "node-id": {
      "id": "node-id",
      "message": {
        "author": { "role": "user" },
        "create_time": 1704450001.0,
        "content": { "content_type": "text", "parts": ["the message text"] }
      },
      "parent": "parent-id",
      "children": ["child-id"]
    }
  }
}
```

The parser walks every node in `mapping`, keeps `user` and `assistant` messages, reads
text from `content.parts` (strings, or dict parts with a `text` field), and orders
messages by `create_time`. Empty/system/tool nodes are skipped.
