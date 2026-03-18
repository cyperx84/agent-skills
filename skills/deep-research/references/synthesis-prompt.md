# Synthesis Prompt Template

Used by the Orchestrator at the final depth level to write the report.

```
You are writing a comprehensive research report. You have completed {total_queries} searches across {depth_levels} depth levels and collected {n_learnings} distinct findings from {n_sources} sources.

## Research Query
"{original_query}"

## All Findings
{learnings_formatted}
(Each finding is a specific fact extracted from a real source)

## Sources
{sources_formatted}

## Your Task

Write a thorough research report in markdown. Structure:

# {Report Title}

## Executive Summary
2-3 paragraphs. Lead with the most important answer to the query. What should the reader know immediately?

## Key Findings
Bullet list of the 5-10 most important, specific, actionable findings. Cite sources inline.

## Detailed Analysis

### [Section 1 — main angle]
### [Section 2 — second angle]
### [Section 3 — third angle]
(Create sections organically based on what the research revealed — don't force a template)

## Gaps & Limitations
What did the research NOT find? What questions remain open? Where is the evidence weak?

## Recommendations
If the user needs to act on this research, what should they do first?

## Sources
Full list of all URLs consulted.

---

## Rules
- Every specific claim must be traceable to a finding in the list above
- Do not invent facts — only synthesize what the findings contain
- Be direct — lead with conclusions, detail follows
- Use markdown headers, code blocks where relevant, tables for comparisons
- Aim for 800-1500 words (longer if the topic warrants it)
```
