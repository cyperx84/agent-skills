---
name: research-spinoff
description: "Research spin-off product ideas from an existing project or concept. Use when: the user says 'research spinoff', 'spin off ideas', 'what else could we build from X', 'what other apps/tools from this', or wants to explore new products derived from an existing project. Runs a multi-agent evaluation chain: research → evaluate → scout competition → rank → present."
---

# Research Spinoff — Multi-Agent Evaluation Chain

Take an existing project/tool/concept and discover what other products could be spun out from it.

## Workflow

```
Step 1: Parallel Research (2 agents, GLM-5)
   ├── Agent A: Surfaces, audiences, domains, monetization
   └── Agent B: AI-native, creative, non-obvious, dev tools
         │
Step 2: Evaluate + Rank (1 agent, GLM-5)
         │ dedupe, score on uniqueness × speed × revenue
         │ output: top 10 ranked
         │
Step 3: Competition Scout (1 agent, GLM-5)
         │ for each top 10: search GitHub, ProductHunt, AppStore
         │ tag: "blue ocean" / "crowded" / "few competitors"
         │
Step 4: Lattice Frame (local, no LLM)
         │ lattice suggest on top 5
         │ attach relevant mental models to each decision
         │
Step 5: Post results to thread
Step 6: User picks → auto-scaffold project
```

## Execution

### Step 1: Spawn Research Agents (parallel)

Spawn 2 sub-agents with `runtime: subagent`, `model: GLM`, `mode: run`.

**Agent A prompt** — see `references/prompt-agent-a.md`
**Agent B prompt** — see `references/prompt-agent-b.md`

Replace `{{PROJECT}}` and `{{CONTEXT}}` placeholders with the actual project name and description.

### Step 2: Evaluate + Rank

After BOTH research agents return, spawn 1 evaluator agent:

- Input: combined raw ideas from Agent A + Agent B
- Task: deduplicate, score each idea on a 3-axis matrix (uniqueness 1-5, build speed 1-5, revenue potential 1-5), multiply scores, rank top 10
- Output: markdown table with columns: Rank, Name, Pitch, Audience, Build Time, Revenue Model, Score
- See `references/prompt-evaluator.md`

### Step 3: Competition Scout

Spawn 1 competition scout agent on the top 10:

- For each idea: search GitHub, ProductHunt, Google for direct competitors
- Tag each: `🟢 blue ocean` (0 competitors), `🟡 few competitors` (1-3), `🔴 crowded` (4+)
- Add competitor names/URLs where found
- See `references/prompt-scout.md`

### Step 4: Lattice Frame

Run locally (no sub-agent needed):

```bash
# For each top 5 idea
lattice suggest "<idea pitch>" --count 3 --no-llm --json
```

Attach the suggested mental models to each idea in the final output.

### Step 5: Post Results

Create a Discord thread (or post to existing thread):
- Thread name: `🔬 Spin-off Product Ideas from {{PROJECT}}`
- Post: ranked table + competition tags + lattice framing
- Ask user which to build

### Step 6: Auto-Scaffold (on user pick)

When user picks an idea:

```bash
mkdir -p ~/github/{{project-name}}
# Generate: README.md, PRD.md from research pitch
# Init: go mod init / npm init / etc based on stack
# Copy: CI template from references/
```

## Thread Management

- Always create a new thread in the user's current channel for results
- Keep the source thread clean — only post the final summary there
- Reference the results thread from the source

## Notes

- All research agents use GLM-5 (fast, cheap, good at web search)
- Steps 1 is parallel; steps 2-4 are sequential (each depends on previous)
- Total wall-clock time: ~8-12 minutes
- If lattice is not installed, skip Step 4 gracefully
