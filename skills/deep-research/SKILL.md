---
name: deep-research
description: "Recursive breadth/depth research using parallel sub-agents. Spawns workers to search, scrape, and extract findings iteratively, then synthesizes a final report. OpenClaw-native (web_search/web_fetch only, no external APIs). Use when the user says 'research [topic]', 'deep research', 'deep dive', 'investigate', 'look into', 'find out about', or wants thorough multi-source research on any topic. NOT for quick single-query lookups."
license: MIT
metadata:
  { "author": "cyperx", "version": "1.0.0", "openclaw": true, "categories": ["research", "productivity"] }
---

# deep-research

Recursive breadth/depth research skill. Spawns parallel worker sub-agents to search, scrape, and extract findings iteratively — then synthesizes a final report. OpenClaw-native: no external APIs beyond web_search/web_fetch.

## Trigger

Use when the user says any of:
- "research [topic]"
- "deep research [topic]"
- "do a deep dive on [topic]"
- "investigate [topic]"
- "find out everything about [topic]"

## Parameters

- `--breadth N` — parallel search queries per iteration (default: 4, max: 8)
- `--depth N` — recursive depth levels (default: 2, max: 4)
- `--output vault` — write result to Obsidian vault (default: true)
- `--output discord` — post summary to Discord (default: true)

## Execution Flow

### Step 1 — Initialize state

Create a research state file at `research/active/{slug}.json`:

```json
{
  "id": "{slug}",
  "query": "{original query}",
  "breadth": 4,
  "depth": 2,
  "currentDepth": 0,
  "currentGoal": "{original query}",
  "learnings": [],
  "visitedUrls": [],
  "nextDirections": [],
  "status": "running",
  "startedAt": "{iso timestamp}",
  "completedAt": null
}
```

### Step 2 — Spawn Orchestrator

Spawn a sub-agent (Orchestrator) with this task, injecting the state file path and params:

```
You are a deep research orchestrator. Your job is to run a breadth/depth research loop.

State file: {state_file_path}
Query: {query}
Breadth: {breadth} (parallel queries per level)
Depth: {depth} (levels remaining, counts down to 0)
Current goal: {current_goal}
Prior learnings: {learnings_summary}

## Your Loop

1. Generate {breadth} specific, diverse search queries for the current goal.
   - Queries should cover different angles: definitions, examples, comparisons, recent developments
   - Each query should be something you'd type into Google

2. For each query, spawn a Worker sub-agent (all in parallel, same turn):
   Task for each worker:
   ```
   Search query: "{query}"
   Research goal: "{current_goal}"
   Prior context: {learnings_summary}

   Steps:
   1. Call web_search with the query (10 results)
   2. Pick the 3 most relevant results
   3. Call web_fetch on each URL
   4. Extract: specific facts, numbers, names, dates relevant to the goal
   5. Identify: what follow-up directions would deepen understanding?

   Write your findings to: research/workers/{worker_id}.json
   Format:
   {
     "query": "...",
     "url": "...",
     "learnings": ["specific fact 1", "specific fact 2"],
     "nextDirections": [{"goal": "...", "rationale": "...", "priority": 8}]
   }
   ```

3. After all workers complete, read all worker files, merge:
   - Append new learnings to state (deduplicate)
   - Append new URLs to state (deduplicate)
   - Collect all nextDirections, sort by priority descending
   - Save updated state file

4. Check stopping criteria:
   - If depth remaining > 1: take the top nextDirection, recurse:
     Spawn a NEW Orchestrator sub-agent with depth-1, breadth/2, new currentGoal
   - If depth remaining == 1: proceed to synthesis

5. Synthesis (only at depth == 1):
   - Read complete state file (all accumulated learnings + sources)
   - Write a comprehensive research report to: research/reports/{id}.md
   - Format: Executive Summary → Key Findings (cited) → Detailed Analysis → Gaps → Recommendations
   - Update state file: status = "complete", completedAt = now
   - Report completion

## Rules
- Write state to disk after every merge — this is the checkpoint
- Never skip deduplication — learnings list must stay clean
- Mark URLs as visited before fetching — avoid re-scraping
- Be specific: extract facts, not summaries
- If web_search returns no results for a query, skip it and note in state
```

### Step 3 — Monitor and report

After the orchestrator completes:
1. Read the final report from `research/reports/{id}.md`
2. If --output vault: run `node scripts/vault-write.mjs research/reports/{id}.md` to write structured note to Obsidian vault
3. Post summary (first 500 words + link to full note) to Discord (if --output discord)
4. Move state file to `research/completed/{slug}.json`

## Progress Updates (during run)

The Orchestrator MUST post a Discord progress update after each depth level completes.
Use the `message` tool (channel=discord, target=#researcher or the originating channel).

**After each depth level merge:**
```
🔍 Research update — [{query}] depth {n}/{total}
✅ {n_learnings} findings so far from {n_sources} sources
🎯 Next: {nextDirection.goal}
⏳ Continuing to depth {n+1}...
```

**On completion:**
```
✅ Research complete — [{query}]
📊 {total_learnings} findings · {total_sources} sources · {depth} depth levels
📝 Report: research/reports/{id}.md
```

## Fleet Integration — Any Agent Can Dispatch

Any agent in the fleet can dispatch a research job to the Researcher agent:

```js
// From any agent (Claw, Builder, Ops, etc.):
sessions_send({
  label: "researcher",   // or sessionKey if known
  message: `RESEARCH_DISPATCH:
query: "what is the best vector DB for local embeddings"
breadth: 4
depth: 2
notify_channel: #general
requestedBy: claw`
})
```

When Researcher receives a `RESEARCH_DISPATCH:` message:
1. Parse the structured fields
2. Run the full research flow
3. Post results to `notify_channel` when done (not just #researcher)
4. Credit `requestedBy` in the completion message

## File Layout

```
research/
  active/           ← in-progress state files ({slug}.json)
  workers/          ← worker output files (ephemeral, cleaned up after each merge)
  reports/          ← final markdown reports
  completed/        ← archived state files
```

## Resume

If interrupted mid-run, check `research/active/` for existing state files.
If found: read state, report current status, offer to resume from last checkpoint.
Resume = spawn new Orchestrator with existing state (same file path).

## Model Strategy

- Orchestrator: default model (sonnet) — needs reasoning for synthesis
- Workers: GLM-5 (cheap, fast) — just search + extract
- Override in sessions_spawn: `model: "GLM"`

## Example

User: "research how LangGraph handles state persistence"

Generates:
- breadth=4, depth=2
- Level 1: 4 workers research LangGraph state persistence in parallel
- Level 2: top follow-up direction (e.g. "checkpointer backends comparison") → 2 workers
- Synthesis: report combining all findings
- Output: Obsidian note + Discord summary
