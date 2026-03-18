# Evaluator — Dedupe, Score & Rank

You are evaluating product ideas from two research agents. Your job: deduplicate, score, and rank.

## Input

Below are raw ideas from two research passes. Many will overlap or be variations of each other.

### Agent A Results
{{AGENT_A_RESULTS}}

### Agent B Results
{{AGENT_B_RESULTS}}

## Process

1. **Deduplicate** — merge ideas that are essentially the same concept with different names
2. **Score each idea** on 3 axes (1-5 each):
   - **Uniqueness** — does anything like this exist? (5 = blue ocean, 1 = crowded)
   - **Build Speed** — how fast to MVP? (5 = weekend, 1 = quarter+)
   - **Revenue Potential** — can it make money? (5 = clear paid market, 1 = hard to monetize)
3. **Composite score** = Uniqueness × Build Speed × Revenue Potential (max 125)
4. **Rank** top 10 by composite score

## Output Format

Markdown table:

| Rank | Name | Pitch | Audience | Build Time | Revenue | Score | Why |
|------|------|-------|----------|-----------|---------|-------|-----|
| 1 | ... | ... | ... | ... | ... | 100 | Brief justification |

Then a **"Top 3 Picks"** section with 2-3 sentences each on why these are the strongest bets.

Keep it concise. No fluff.
