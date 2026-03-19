---
name: lattice
description: "Apply mental models and cognitive frameworks to problems, decisions, and content analysis. Use when the user asks to 'think through' a problem, says 'apply mental models', mentions specific models like inversion/second-order thinking/bottlenecks/first principles, needs structured decision analysis, wants to understand cognitive biases at play, or asks 'what framework should I use'."
metadata:
  { "openclaw": { "emoji": "🧠", "requires": { "bins": ["lattice"] } } }
---

# Lattice — Mental Models Engine

Apply Charlie Munger's latticework of 98 mental models to any problem.

## Commands

### Recommend models (fast, no LLM)
```bash
lattice suggest "<situation>"
lattice suggest "<situation>" --count 10
lattice suggest "<situation>" --json
```
Use when user asks "what framework should I use" or "help me think about X". Returns top models with relevance explanation.

### Think through a problem (applies models)
```bash
lattice think "<problem>"                    # top 3 models, with LLM synthesis
lattice think "<problem>" --no-llm           # instant, static steps only
lattice think "<problem>" --models inversion,bottlenecks  # force specific models
lattice think "<problem>" --json             # structured output
```

### Apply a specific model
```bash
lattice apply <slug> "<context>"             # with LLM synthesis
lattice apply <slug> "<context>" --no-llm    # static thinking steps
```

### Search and browse
```bash
lattice search "<keyword>"
lattice list
lattice list --category "Economics"
lattice info <slug>
lattice info <slug> --json
```

### Add custom models
```bash
lattice add "Network Effects"
lattice add "Lindy Effect" --from "https://fs.blog/lindy-effect/"
```

### Remove user-added models
```bash
lattice remove <slug>   # only works on ~/.config/lattice/models/ files
```

### Record a decision
```bash
lattice decide "<decision>"                          # guided: models + thinking + prediction prompt
lattice decide "<decision>" --quick                  # skip thinking, just prediction
lattice decide "<decision>" --prediction "expected"  # inline prediction
lattice decide "<decision>" --project                # save to ./decisions/ (ADR-style)
lattice decide "<decision>" --models inversion,trade-offs  # force models
```
Use when user says "I need to decide", "record this decision", "help me think through this choice", or "track this decision".

### View decision journal
```bash
lattice journal                    # recent 20 decisions
lattice journal --due              # decisions due for review
lattice journal --all              # all decisions
lattice journal --project          # read from ./decisions/
lattice journal --json             # structured output
lattice journal review <id>       # review a past decision, record outcome
```

## Model Categories (98 total)
- **General Thinking Tools** (m01-m09): First principles, inversion, second-order thinking, probabilistic thinking, Occam's razor
- **Physics/Chemistry/Biology** (m10-m29): Leverage, inertia, feedback loops, ecosystems, evolution, activation energy
- **Systems Thinking** (m30-m40): Bottlenecks, scale, margin of safety, emergence, network effects
- **Mathematics** (m41-m47): Randomness, regression to mean, surface area, local vs global maxima
- **Economics** (m48-m59): Trade-offs, scarcity, creative destruction, supply & demand, efficiency
- **Art** (m60-m70): Framing, audience, contrast, rhythm, narrative
- **Strategy/Warfare** (m71-m75): Asymmetric warfare, seeing the front, mutually assured destruction
- **Human Nature & Judgment** (m76-m98): Cognitive biases, incentives, social proof, confirmation bias, denial

## Common Patterns

User says "help me decide" → `lattice decide "<their decision>"`
User says "record this decision" → `lattice decide "<decision>" --quick`
User asks "what decisions are due" → `lattice journal --due`
User mentions a model by name → `lattice apply <slug> "<context>"`
User asks "think through X" → `lattice think "<X>"`
User asks "what biases am I missing" → `lattice search "bias"` then apply relevant ones
User wants to browse → `lattice list` or `lattice list --category "Human Nature & Judgment"`

## Ecosystem Integration

Lattice works standalone and also integrates with:
- **multiplan** — auto-injects Phase 0 mental model framing before parallel planning
- **content-breakdown** — `--think` flag appends model analysis; `mental-models` lens available
- **clwatch** — `clwatch think <harness>` tags changelogs with mental models

## Output

All commands support `--json` for structured output. Use `--no-llm` for instant results without API calls.
