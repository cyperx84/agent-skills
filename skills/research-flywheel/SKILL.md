---
name: research-flywheel
description: Mine conversations for research-worthy topics, deep research them via deep-research skill, store findings, and report digests. A research flywheel that closes the loop between conversations and knowledge.
license: MIT
allowed-tools:
  - lcm_grep
  - lcm_describe
  - lcm_expand
  - web_search
  - web_fetch
  - read
  - write
  - exec
  - message
metadata:
  author: cyperx84
  version: 0.1.0
---

# Research Flywheel

Mine conversations for topics worth researching, dispatch deep research, store findings, and produce digests. Closes the loop between what Chris talks about and what gets properly researched.

## Trigger

Use when the user says any of:
- "research flywheel"
- "mine conversations for research topics"
- "what should I research"
- "research digest"
- "flywheel status"
- "flywheel run"

## Commands

### `research-flywheel mine` — Find research candidates

Scans conversation history for research-worthy topics.

```bash
research-flywheel mine [--since "2026-03-17"] [--agents all|researcher|claw|builder]
```

**Flow:**
1. Run configurable mine patterns (from `references/mine-patterns.md`) via `lcm_grep`
2. Extract topic mentions with source references (conversation ID + message context)
3. Deduplicate against already-completed research in state
4. Score candidates: frequency × recency × Chris-initiated bonus
5. Store as pending candidates in state file
6. Print ranked list

**Patterns:** See `references/mine-patterns.md`. Configurable, not hardcoded regex. Default patterns look for:
- Questions about topics ("how does X work", "what's the best Y")
- Mentions of tools/products/technologies in context of evaluation
- "research this", "look into", "investigate" directives
- Topics mentioned across multiple conversations (high frequency signal)

### `research-flywheel research "<topic>"` — Dispatch deep research

Wraps the existing `deep-research` skill to research a specific topic.

```bash
research-flywheel research "edge AI for snow sports" --breadth 6 --depth 3
```

**Flow:**
1. Look up topic in pending candidates (or add if new)
2. Delegate to `~/.openclaw/skills/deep-research/scripts/deep-research.mjs` with the topic
3. Monitor progress via state file updates
4. On completion: store report path in state, update candidate status to "completed"
5. Optionally write vault note via `obsidian-cli`

### `research-flywheel status` — Show research state

```bash
research-flywheel status [--topic "snow"]
```

Prints:
- Completed research (topic, report path, date)
- Pending candidates (ranked by score)
- Gaps (topics mentioned but never researched)

### `research-flywheel digest` — Produce summary

```bash
research-flywheel digest [--since "2026-03-17"] [--output discord|vault|stdout]
```

**Flow:**
1. Read all completed reports since the date
2. Generate a concise digest (key findings per topic, 2-3 sentences each)
3. Deliver to specified output channel
4. Discord delivery uses the `message` tool
5. Vault delivery uses `obsidian-cli create`

### `research-flywheel run` — Full cycle

```bash
research-flywheel run [--dry-run] [--auto] [--top N]
```

**Flow:**
1. Mine for candidates
2. Filter to top N (default 3)
3. Research each (unless --dry-run)
4. Generate digest
5. If --auto: skip all confirmations
6. If --dry-run: print what would happen, exit

## State File

`~/.openclaw/agents/researcher/research/flywheel/state.json`:

```json
{
  "candidates": [
    {
      "topic": "edge AI for snow sports",
      "source": "conv:27/msg:8251",
      "priority": "high",
      "score": 8.5,
      "status": "pending",
      "tags": ["snowboard", "edge-ai"],
      "discoveredAt": "2026-03-18T10:00:00+10:00"
    }
  ],
  "completed": [
    {
      "topic": "snowboard apps competitive analysis",
      "reportPath": "research/reports/snowboard-apps-competitive-v3.md",
      "completedAt": "2026-03-18T14:06:00+10:00",
      "vaultNote": "snowboard-apps-competitive",
      "digest": "ShredApp leads with AI coaching, Snocru has best social features..."
    }
  ],
  "config": {
    "defaultBreadth": 4,
    "defaultDepth": 2,
    "topN": 3,
    "notifyChannel": "1483345530363973768",
    "dryRun": false
  }
}
```

## Integration Points

- **deep-research skill** — `research` delegates to `~/.openclaw/skills/deep-research/scripts/deep-research.mjs`
- **LCM tools** — `mine` uses `lcm_grep` + `lcm_describe` for conversation mining
- **Obsidian vault** — `digest` and `research` can write notes via `obsidian-cli`
- **Discord** — digest delivery via `message` tool
- **OpenClaw cron** — schedulable for automated daily runs (mine + digest cycle)

## Cron Integration

```bash
# Daily flywheel: mine topics overnight, research top 1, post morning digest
# 0 7 * * * research-flywheel run --auto --top 1
```

## Edge Cases

- **No LCM data:** If `lcm_grep` returns nothing, report "No conversation data available for mining" and exit cleanly
- **Empty state file:** Initialize with defaults on first run
- **Duplicate topics:** Dedupe by normalized topic string (lowercase, stripped)
- **Researcher agent:** Primary runner is the Researcher agent, but any agent can dispatch via `sessions_send`

## Example Session

```
User: "flywheel status"
→ Shows 2 completed, 5 pending candidates

User: "flywheel run --dry-run"
→ Would mine 3 new candidates, research "GLM-5 turbo benchmarks", post digest

User: "flywheel run"
→ Mines, asks "Research top 3 topics?", confirms, runs deep-research on each, posts digest
```
