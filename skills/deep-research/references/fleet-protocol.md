# Fleet Protocol — Cross-Agent Research Dispatch

This document defines the protocol for dispatching research jobs between agents in the OpenClaw fleet. Any agent can dispatch; Researcher handles execution.

---

## 1. Dispatch Message Format

Send via `sessions_send` to the Researcher agent session.

```
RESEARCH_DISPATCH:
query: "what to research"
breadth: 4
depth: 2
notify_channel: 1234567890
requestedBy: claw
dispatchId: some-unique-slug-abc123
```

**Fields:**
| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `query` | ✅ | — | The research question or topic |
| `breadth` | ❌ | 4 | Number of parallel search directions |
| `depth` | ❌ | 2 | Recursive follow-up depth |
| `notify_channel` | ❌ | requester's channel | Discord channel ID to post results |
| `requestedBy` | ❌ | unknown | Agent name that sent the dispatch |
| `dispatchId` | ❌ | — | Unique job identifier (from pending.json) |

---

## 2. Helper Script

To generate a dispatch message and register it in pending.json:

```bash
node ~/.openclaw/skills/deep-research/scripts/dispatch.mjs "query here" \
  --breadth 4 \
  --depth 2 \
  --notify-channel 1234567890 \
  --requested-by claw
```

Output: the formatted RESEARCH_DISPATCH string. Paste it as the `message` in `sessions_send`.

Pending jobs are tracked at:
`/Users/cyperx/.openclaw/agents/researcher/research/pending.json`

---

## 3. Researcher Acknowledgement Format

When Researcher receives a RESEARCH_DISPATCH, it immediately replies:

```
🔍 Got it — researching "[query]". Will post results to [channel].
```

If no channel specified:
```
🔍 Got it — researching "[query]". Results will be posted here when done.
```

---

## 4. Result Delivery Format

When research is complete, Researcher posts to `notify_channel`:

```
## 🔍 Research Complete: [query]

**Summary:** [2-3 sentence executive summary]

**Key Findings:**
- Finding 1
- Finding 2
- Finding 3

**Sources:** [list of key URLs]

**Confidence:** [High / Medium / Low] — [brief note on source quality]

**Full report:** [path or link if saved to vault/disk]
```

---

## 5. Pending Job Tracking

File: `/Users/cyperx/.openclaw/agents/researcher/research/pending.json`

Format:
```json
[
  {
    "id": "slug-abc123",
    "query": "...",
    "breadth": 4,
    "depth": 2,
    "notifyChannel": "1234567890",
    "requestedBy": "claw",
    "dispatchedAt": "2025-01-01T00:00:00.000Z",
    "status": "pending"
  }
]
```

Status values: `pending` | `in-progress` | `complete` | `failed`

---

## 6. Error Handling

| Scenario | Researcher action |
|----------|-------------------|
| Researcher busy with another job | Queue the request; acknowledge receipt; run sequentially |
| Deep-research script fails | Retry once; if still fails, post error to notify_channel with partial findings |
| notify_channel invalid/missing | Post results back to requester via sessions_send reply |
| Query too vague | Attempt best-effort research; note ambiguity in results |

---

## 7. Dispatch Decision Guide (for Claw)

**Dispatch to Researcher when:**
- User says "research X", "deep dive on X", "investigate X", "look into X", "I need research on X"
- Task requires multi-source synthesis
- Topic needs breadth/depth beyond a quick web search
- User explicitly asks for a report or analysis

**Handle inline when:**
- Quick factual lookup (single web_search is enough)
- User asks a direct question with a known answer
- The task takes < 30 seconds to answer competently

---

*This protocol is agent-readable. Agents should follow exact message formats for reliable parsing.*
