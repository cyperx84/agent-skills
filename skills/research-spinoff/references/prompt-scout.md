# Competition Scout — Validate Top Ideas

You are validating product ideas against existing competition. For each idea, determine if the market is open or crowded.

## Input

Top 10 ranked ideas:

{{TOP_10_IDEAS}}

## Process

For EACH idea:

1. **Search GitHub** — repos with similar functionality (star count matters)
2. **Search ProductHunt** — launched products in same space
3. **Search Google** — "[idea concept] app/tool/CLI"
4. **Search App Store / Chrome Web Store** if relevant

## Output Format

For each idea:

### [Rank]. [Name]

**Competitors found:**
- [Name] — [URL] — [brief description, user count if known]
- ...

**Verdict:** 🟢 Blue Ocean (0 direct competitors) | 🟡 Few Competitors (1-3) | 🔴 Crowded (4+)

**Differentiation opportunity:** One sentence on how this idea could differentiate even in a crowded space.

---

Be thorough but fast. We need signal, not exhaustive market research.
