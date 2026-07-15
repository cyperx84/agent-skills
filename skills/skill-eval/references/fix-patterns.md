# Common Fix Patterns

Reference for applying improvements after evaluation. Each pattern includes what to look for and how to fix it.

## Description Fixes

### Under-triggering
**Symptom:** Score < 7 on Triggering Accuracy. Description is too narrow.
**Fix:** Add "pushy" phrases: "Use this skill whenever...", "even if they don't explicitly ask for...". Add trigger variants (casual, formal, keyword-adjacent).

### False-positive risk
**Symptom:** Generic phrases like "set up", "create", "build" without qualifiers.
**Fix:** Qualify with domain: "set up my agent fleet" not "set up". Add NOT-for section if missing.

### Non-standard frontmatter
**Symptom:** Fields beyond `name` and `description` in YAML frontmatter.
**Fix:** Move metadata elsewhere or remove. Only `name` and `description` are standard.

## Body Fixes

### Token waste — restating model knowledge
**Symptom:** Explanations of concepts the model already knows (what JSON is, how git works).
**Fix:** Delete. Replace with the specific detail the model needs (your schema, your branch convention).

### Redundant sections
**Symptom:** A "Principles" or "Guidelines" section that repeats what the workflow already says.
**Fix:** Collapse into inline callouts within the workflow steps. Delete the standalone section.

### Missing schema/example
**Symptom:** "Edit the config file" with no example of what the config looks like.
**Fix:** Add a minimal example (3-5 lines). Not a full spec — just enough to act.

## Structure Fixes

### Monolithic SKILL.md
**Symptom:** Body > 300 lines with distinct sections that aren't always needed.
**Fix:** Extract variant-specific or rarely-needed sections to references/. Link with "See references/X.md when Y."

### Missing error guidance
**Symptom:** Commands documented but no mention of what goes wrong.
**Fix:** Add 1-2 lines for common failure modes: what the error looks like, what to do.

## CLI Skill Fixes

### Incomplete command coverage
**Symptom:** Some subcommands or important flags not documented.
**Fix:** Run `<tool> --help` for each subcommand. Document flags that affect behavior.

### No workflow for partial use
**Symptom:** Only the "full flow" is documented. No guidance for "I just need to do X."
**Fix:** Add a "Partial Workflows" section with one-liner mappings: "User says X → run Y."
