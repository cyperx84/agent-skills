# Anthropic Skills Research — Findings & Action Items

> Research done 2026-03-19 after Anthropic published `anthropics/skills` repo and the Agent Skills spec at agentskills.io.

## What Anthropic Shipped

Anthropic published an official **skills repository** (`anthropics/skills` on GitHub) with:
- The **Agent Skills specification** (now at agentskills.io/specification)
- A **skill-creator plugin** with evals, benchmarking, and trigger optimization
- 18 example skills covering creative, technical, enterprise, and document tasks
- Document skills (docx, pdf, pptx, xlsx) powering Claude's built-in file capabilities

### Engineering Blog: "Equipping agents for the real world with Agent Skills"

Key architecture insights from the blog post:

**Progressive disclosure is the core design principle.** Three levels:
1. **Metadata** (~100 tokens) — name + description loaded at startup in system prompt
2. **Instructions** (<5k tokens) — full SKILL.md loaded when skill triggers (via bash read)
3. **Resources** (unlimited) — scripts, references, assets loaded on demand

**Skills run in Claude's VM/code execution environment.** Claude reads SKILL.md via bash, then optionally reads referenced files or runs scripts. Script code never enters context — only output does. This means skills can bundle unlimited reference material with zero context penalty until accessed.

**Code execution is the differentiator.** Scripts provide deterministic reliability that token generation can't match. Sorting, form filling, PDF extraction — all better as code than as LLM output.

**Best practices from Anthropic:**
- Start with evaluation — identify capability gaps by running agents on representative tasks, then build skills to address shortcomings
- Structure for scale — split SKILL.md when unwieldy, keep mutually exclusive contexts on separate paths
- Think from Claude's perspective — monitor how Claude uses skills in real scenarios, iterate on name/description which drive triggering
- Iterate with Claude — ask it to capture successful approaches and mistakes into reusable skill content

**Security:** Install only from trusted sources. Audit scripts and instructions for exfiltration or external network connections. Skills provide new capabilities through both instructions and code.

**Future direction:** Agents creating/editing/evaluating skills on their own. Skills complementing MCP servers. Plugin marketplace for discovery and sharing.

### Platform Docs & Cookbook

**Claude API supports skills via the `container` parameter:**
```python
response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    container={"skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]},
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"],
)
```

Three beta headers required: `code-execution-2025-08-25`, `skills-2025-10-02`, `files-api-2025-04-14`.

**Token efficiency:** Skills cost ~100 tokens per skill at metadata level vs 5k-10k tokens for equivalent manual instructions. The 98% savings applies to initial context — once triggered, full instructions load (~5k tokens).

**Custom skills work identically** — create locally, upload via API, or add in claude.ai settings. Same progressive disclosure, same loading model.

### Official Validation Tool: `skills-ref`

Python CLI from `agentskills/agentskills` repo:
- Validates frontmatter fields (only `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility` allowed)
- Checks name format (lowercase, alphanumeric + hyphens, max 64 chars, matches directory name)
- Checks description length (max 1024 chars)
- Checks compatibility length (max 500 chars)
- NFKC Unicode normalization on names
- Pytest test suite included

Install: `pip install` from the repo's `skills-ref/` directory.

### The Agent Skills Spec

The spec defines a standard format any agent can implement:

**Required:** `SKILL.md` with YAML frontmatter (`name` + `description`) and Markdown instructions.

**Optional directories:** `scripts/` (executable code), `references/` (docs loaded on demand), `assets/` (templates/resources).

**Key constraints:**
- `name`: 1-64 chars, lowercase alphanumeric + hyphens, no consecutive hyphens, must match directory name
- `description`: 1-1024 chars, should include both what it does AND when to use it
- `SKILL.md` body: recommended <500 lines
- Progressive disclosure: metadata (~100 tokens) → instructions (<5k tokens) → resources (on demand)

**Validation tool:** `skills-ref` CLI from `agentskills/agentskills` repo.

### The skill-creator Plugin (The Big One)

Anthropic's skill-creator is a full development environment, not just a template generator:

**485-line SKILL.md** with:
- Intent capture from conversation history
- User interview workflow
- Progressive disclosure architecture guidance
- Domain organization patterns
- Writing style guidelines

**8 Python scripts** in `scripts/`:
| Script | Purpose |
|--------|---------|
| `run_eval.py` | Run skill vs baseline, spawn parallel agents |
| `aggregate_benchmark.py` | Compile A/B results with variance analysis |
| `generate_report.py` | HTML report with side-by-side comparisons |
| `improve_description.py` | Optimize trigger descriptions via Claude Code |
| `quick_validate.py` | Fast SKILL.md validation |
| `package_skill.py` | Bundle for distribution |
| `run_loop.py` | Iterative improvement loop |
| `utils.py` | Shared helpers |

**3 agent templates** for subagents:
- `analyzer.md` — qualitative analysis of outputs
- `comparator.md` — side-by-side comparison
- `grader.md` — quantitative assertion grading

**Eval viewer** — generates HTML with side-by-side skill vs baseline comparisons.

### Key Insight: Evals Change Everything

The skill-creator's eval system runs **parallel A/B benchmarks**:
1. Generate test cases (evals.json)
2. Spawn N agents WITH skill + N agents WITHOUT skill (baseline)
3. Grade against assertions (pass/fail criteria)
4. Compile metrics: pass rate, token usage, latency
5. Generate HTML review playground
6. Iterate: fix gaps, re-benchmark

Real example from the wild: WordPress security review skill went from 90.5% → 100% pass rate after one eval iteration. Baseline Claude missed WooCommerce-specific patterns that the skill caught.

### Trigger Optimization

The `improve_description.py` script specifically optimizes the `description` field for better triggering. This matters because Claude has a documented tendency to **undertrigger** skills. Anthropic recommends making descriptions "a little bit pushy" — including every possible context where the skill should fire.

### Plugin Marketplace Integration

Skills can be distributed via Claude Code's plugin system:
```
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

## How We Compare

| Feature | Anthropic skill-creator | Our skill-publisher |
|---------|------------------------|-------------------|
| SKILL.md generation | ✅ Full interview workflow | ✅ Basic |
| Evals & benchmarks | ✅ A/B parallel, graded assertions | ❌ None |
| Trigger optimization | ✅ Automated description improvement | ❌ None |
| Validation | ✅ quick_validate.py + skills-ref | ✅ CI workflow |
| Packaging | ✅ package_skill.py | ❌ None |
| Iterative loop | ✅ run_loop.py | ❌ None |
| HTML review viewer | ✅ eval-viewer/ | ❌ None |
| Spec compliance | ✅ IS the spec | ✅ Compatible |
| Claude Code native | ✅ /plugin install | ❌ Manual copy |
| Multi-agent support | ✅ 3 agent templates | ❌ None |
| Progressive disclosure | ✅ Explicit guidance | ⚠️ Basic |

## What We Should Do

### Immediate (copy the good parts)

1. **Port the eval system** — The biggest gap. Our skills have zero testing. Port `run_eval.py`, `aggregate_benchmark.py`, and `grader.md` agent. Adapt for OpenClaw (use `sessions_spawn` instead of `claude -p`).

2. **Add trigger optimization** — Port `improve_description.py`. Even a simplified version that rewrites descriptions based on test results would help. OpenClaw's `available_skills` list shows descriptions to the model at startup, so this matters.

3. **Use `skills-ref validate`** — Switch from our custom CI to the official validator. Add it as a Makefile target.

4. **Merge skill-creator into skill-publisher** — Our skill-publisher (98 lines) is a subset of what Anthropic's skill-creator does. Either port Anthropic's version or clearly differentiate (ours = distribution, theirs = development).

### Short-term

5. **Add evals.json to each skill** — Even 3-5 test cases per skill. The eval framework needs test data to be useful.

6. **Progressive disclosure audit** — Check all 11 skills against the <500 line recommendation. We already did this for the dotfiles skills but haven't verified the rest.

7. **Description pushiness audit** — Anthropic explicitly says Claude undertriggers skills. Review all 11 descriptions and make them more aggressive about when to fire.

### Medium-term

8. **OpenClaw plugin compatibility** — Investigate if OpenClaw can register as a plugin marketplace. The `/plugin install` flow would be ideal for our mono-repo.

9. **Cross-agent evals** — Anthropic's evals only test against Claude Code. We could benchmark skills across Claude Code, Codex, Gemini CLI, and OpenCode — since our skills claim to be agent-agnostic.

10. **CI eval pipeline** — Add eval runs to the GitHub Actions workflow. Not just "does SKILL.md parse?" but "does the skill actually improve output?"

## Things We're Already Doing Right

- ✅ Spec-compliant SKILL.md format with proper frontmatter
- ✅ Progressive disclosure with references/ and scripts/
- ✅ CI validation on every push
- ✅ Mono-repo structure (Anthropic does the same thing)
- ✅ Line count compliance (we enforced this during migration)
- ✅ skill-creator built-in skill for OpenClaw agents

## Files Referenced

- Anthropic skills repo: https://github.com/anthropics/skills
- Agent Skills spec: https://agentskills.io/specification
- Validation tool: https://github.com/agentskills/agentskills
- Anthropic blog post: https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
