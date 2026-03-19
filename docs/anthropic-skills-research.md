# Anthropic Skills Research — Findings & Action Items

> Research done 2026-03-19 after Anthropic published `anthropics/skills` repo and the Agent Skills spec at agentskills.io.

## What Anthropic Shipped

Anthropic published an official **skills repository** (`anthropics/skills` on GitHub) with:
- The **Agent Skills specification** (now at agentskills.io/specification)
- A **skill-creator plugin** with evals, benchmarking, and trigger optimization
- 18 example skills covering creative, technical, enterprise, and document tasks
- Document skills (docx, pdf, pptx, xlsx) powering Claude's built-in file capabilities

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
