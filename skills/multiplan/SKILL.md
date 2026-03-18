---
name: multiplan
description: "Run multi-model parallel planning workflows using the multiplan CLI. Sends a task simultaneously to Claude (correctness lens), Gemini (scale lens), Codex (speed lens), and GLM-5 (critic lens), cross-examines the results, then converges on a weighted final plan. Use when the user asks to: plan something with multiple models, run a multiplan, get a stress-tested technical plan, use multiplan on a task, plan with all models, or run parallel planning. NOT for simple one-model plans — use this when the user explicitly wants multi-model or multiplan."
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins:
        - multiplan
---

# multiplan

Run a task through 4 models in parallel → cross-examine → converge on a weighted final plan.

**Binary:** `multiplan` (installed at `~/.local/bin/multiplan`)
**Runs saved to:** `~/.multiplan/runs/<timestamp>/`

## Setup check

```bash
multiplan --version   # should print "multiplan v0.4.0"
```

Required env vars (at least one model must be available):
- `ANTHROPIC_API_KEY` — Claude (Opus)
- `GOOGLE_AI_API_KEY` or `GEMINI_API_KEY` — Gemini
- `OPENAI_API_KEY` — Codex/GPT
- `ZAI_API_KEY` — GLM-5

## Basic usage

```bash
# Run planning on a task
multiplan "Design a rate limiting system for the API"

# With requirements and constraints
multiplan "Build a real-time notification system" \
  --req "Must support 10k concurrent users, WebSocket-based" \
  --con "No new infrastructure — use existing Redis + Postgres"

# Verbose (see each model finish in real time)
multiplan "Design an auth system" --verbose

# JSON output (for piping/scripting)
multiplan "Design a caching layer" --json

# Quiet (errors + final plan only)
multiplan "Design a webhook system" --quiet
```

## Output files

After a run, `~/.multiplan/runs/LATEST/` contains:

| File | Contents |
|------|----------|
| `plan-claude.md` | Correctness + edge cases lens |
| `plan-gemini.md` | Scale + ops simplicity lens |
| `plan-codex.md` | Implementation speed lens |
| `plan-glm5.md` | Failure analysis + critic lens |
| `debate.md` | Cross-examination of all 4 plans |
| `final-plan.md` | ✅ Weighted synthesis — start here |

## Eval

```bash
# Eval a single plan
multiplan eval ~/.multiplan/runs/LATEST/final-plan.md

# Eval all plans in a run directory
multiplan eval ~/.multiplan/runs/LATEST/

# With a fixture (task + expected topics + min score)
multiplan eval ~/.multiplan/runs/LATEST/ --fixture eval/fixtures/rate-limiter.json

# JSON output
multiplan eval ~/.multiplan/runs/LATEST/ --json
```

## Config file

Create `~/.config/multiplan/config.yml` to set defaults:

```yaml
debate_model: claude
converge_model: claude
timeout_ms: 120000
verbose: false
```

CLI flags always override config file.

## Workflow for user requests

1. Extract the task, requirements, and constraints from what the user said
2. Run `multiplan "<task>" --req "<reqs>" --con "<constraints>" --verbose`
3. When complete, read `~/.multiplan/runs/LATEST/final-plan.md` and present it
4. Optionally run `multiplan eval ~/.multiplan/runs/LATEST/` and show scores

## Tips

- **Always use `--verbose`** so the user can see models completing in real time
- If a model is unavailable (missing API key), multiplan skips it and continues with the rest
- The final plan is already a synthesis — no need to re-summarise it; just present it directly
- For big tasks, add `--timeout 180000` (3 min) to give models more time
