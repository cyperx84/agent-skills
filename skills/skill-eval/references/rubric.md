# Skill Evaluation Rubric

Score each criterion 1–10. Provide evidence and specific fix for any score < 8.

## Criteria

### 1. Frontmatter — Description Quality
- Does the description clearly state what the skill does?
- Does it list specific trigger phrases/contexts?
- Does it say when NOT to use the skill?
- Is it "pushy" enough to avoid under-triggering?
- Is it free of non-standard fields (only `name` and `description` in YAML)?

### 2. Body — Conciseness
- Does every paragraph justify its token cost?
- Is there information the model already knows being restated?
- Are there redundant sections (e.g., principles that repeat workflow steps)?
- Is the body under 500 lines?

### 3. Progressive Disclosure
- Is content split appropriately between SKILL.md and references/?
- Are reference files clearly linked with guidance on when to read them?
- For large reference files (>300 lines), is there a table of contents?
- Are references one level deep (no nested chains)?

### 4. Degrees of Freedom
- High freedom for subjective/variable tasks?
- Low freedom (exact scripts/commands) for fragile operations?
- Are examples used instead of verbose explanations where possible?

### 5. Triggering Accuracy
- Will the description reliably match intended queries?
- Are there false-positive risks from generic phrases?
- Does it disambiguate from similar/adjacent skills?

### 6. Practical Completeness
- Are all CLI commands/flags documented?
- Are workflows actionable (can be followed step-by-step)?
- Are common failure modes and edge cases covered?
- Is there enough context for the model to handle partial workflows?

### 7. Anti-Patterns
- No README-like fluff or extraneous documentation files?
- No CHANGELOG, INSTALLATION_GUIDE, etc.?
- No deeply nested references?
- Imperative form used throughout?

## Scoring

- **9–10**: Production quality, ships as-is
- **7–8**: Good, minor improvements possible
- **5–6**: Functional but needs work
- **3–4**: Significant issues
- **1–2**: Fundamentally broken

## Output Format

For each criterion, output:
```
### [Criterion Name] — [Score]/10
**Evidence:** [What you observed]
**Fix:** [Specific, actionable change — or "None needed" if 9+]
```

Then:
```
### Overall — [Average]/10
**Summary:** [1-2 sentences]
**Top 3 Fixes (priority order):**
1. [Most impactful fix]
2. [Second fix]
3. [Third fix]
```
