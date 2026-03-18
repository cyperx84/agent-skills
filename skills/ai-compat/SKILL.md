---
name: ai-compat
description: >
  Search and compare AI model + harness compatibility from the local ai-compat
  dataset. Use when an agent needs to search models, harnesses, or combos,
  or compare pairings. Triggers: "ai compat", "model compatibility", "which harness".
license: MIT
metadata:
  author: cyperx
  version: "1.0.0"
  openclaw: true
  categories: [dev, productivity]
---

# ai-compat

OpenClaw skill scaffold for selecting an AI model and harness pairing from the local `ai-compat` dataset.

## Purpose

Use this skill when an agent needs to:

- search available models, harnesses, or combos
- compare two models or two harnesses
- inspect one exact combo
- recommend the best stack for a use case

## Data source

Read from the repository dataset at `src/data/compat.json`.

The same data also powers:

- the Astro site
- the JSON API under `/api`
- the `aicomp` CLI

## Preferred interface

Use the local CLI first.

### Search

```bash
aicomp search claude
aicomp search local --json
```

### Compare

```bash
aicomp compare claude-opus-4 claude-sonnet-4
aicomp compare codex-cli openclaw --json
```

### Combo lookup

```bash
aicomp combo --model gpt-4.1 --harness codex-cli
aicomp combo --model claude-opus-4 --harness openclaw --json
```

### Recommendations

```bash
aicomp best
aicomp best --for coding
aicomp best --for autonomous --json
aicomp tiers models
```

## API fallback

If the site is running, these endpoints expose the same data:

- `GET /api/models.json`
- `GET /api/harnesses.json`
- `GET /api/combos.json`
- `GET /api/recommend.json?usecase=coding`
- `GET /api/tiers/models.json`
- `GET /api/best/autonomous.json`

## Agent guidance

Recommendation heuristics:

- prefer the highest score unless the user asks for a specific provider or workflow
- use `coding` for implementation-heavy software work
- use `research` for synthesis, review, and long-context analysis
- use `autonomous` for tool-using agent systems
- use `local` when portability and self-hosting matter
- use `budget` when the user wants the best value option

## Expected outputs

Good responses should include:

- the selected combo name
- the score
- the model and harness slugs
- the relevant use case
- one short reason grounded in the dataset notes
