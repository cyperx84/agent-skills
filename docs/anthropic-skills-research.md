# Anthropic Skills Research — OpenClaw-First Lens

> Research done 2026-03-19. Chris's skills are built for OpenClaw. Anthropic's work is reference material, not the target platform.

## What Anthropic Did (Reference)

Anthropic published `anthropics/skills` repo, the Agent Skills spec (agentskills.io), a skill-creator plugin with evals/benchmarking, and 18 example skills. Their blog covers progressive disclosure architecture, code execution in VMs, and security practices.

**Key takeaway:** The spec format (SKILL.md + frontmatter) is the same standard OpenClaw follows. But the runtime, loading, gating, and distribution are completely different.

## OpenClaw Skills vs Anthropic Skills — Key Differences

| Aspect | Anthropic (Claude Code) | OpenClaw |
|--------|------------------------|----------|
| Loading | Agent reads SKILL.md via bash on trigger | Gateway pre-indexes, injects `<available_skills>` XML into system prompt at session start |
| Discovery | Plugin marketplace, `/plugin install` | ClawHub (`clawhub install`), bundled, managed (`~/.openclaw/skills`), workspace (`<workspace>/skills/`) |
| Gating | None (all installed skills always available) | Rich: `requires.bins`, `requires.env`, `requires.config`, `metadata.openclaw.os`, `enabled` flag |
| Config | N/A | Per-skill env injection, API keys, custom config in `openclaw.json` |
| Metadata | `name`, `description`, `license`, `metadata`, `compatibility`, `allowed-tools` | Same base fields + OpenClaw extensions: `metadata.openclaw.requires`, `metadata.openclaw.install`, `metadata.openclaw.emoji`, `metadata.openclaw.homepage`, `metadata.openclaw.os`, `user-invocable`, `disable-model-invocation`, `command-dispatch`, `homepage` |
| Precedence | Last installed wins | Workspace > managed (`~/.openclaw/skills`) > bundled > extraDirs |
| Token cost | ~100 tokens/skill at metadata level | ~24 tokens base + field lengths per skill (XML format) |
| Hot reload | Restart Claude Code | Skills watcher auto-refreshes on SKILL.md changes |
| Remote nodes | N/A | macOS nodes can make platform-specific skills available to Linux gateways |
| Scripts | Agent runs via bash in VM | Agent runs via exec tool (respects sandboxing, elevated permissions) |
| Frontmatter format | Standard YAML | Single-line keys only, `metadata` must be single-line JSON object |

## What We Can Learn (OpenClaw-Specific)

### 1. Description quality matters more than we think

Anthropic found Claude **undertriggers** skills. OpenClaw has the same problem — the model sees `<available_skills>` XML and has to decide which skill matches. Our descriptions need to be explicit about:
- What the skill does
- When to use it (specific trigger phrases/contexts)
- What it does NOT do (avoid false triggers)

**Action:** Audit all 11 skill descriptions. Make them "pushy" — include every context where the skill should fire. Example: instead of "Manage Apple Notes via memo CLI", write "Manage Apple Notes via memo CLI. Use when the user asks to add a note, list notes, search notes, or manage note folders. Also use for any mention of Apple Notes, macOS notes, or memo CLI."

### 2. Progressive disclosure is already working for us

OpenClaw loads only metadata (~24 tokens/skill) at session start. The agent reads SKILL.md body only when it decides the skill is relevant. This is the same three-level model Anthropic describes. We're already doing this right.

**Action:** Ensure no SKILL.md exceeds 500 lines. We already enforced this during dotfiles migration but haven't checked the 11 top-level skills.

### 3. Evals are the gap — but adapted for OpenClaw

Anthropic's eval system spawns parallel `claude -p` agents with/without skills and grades outputs. For OpenClaw, we'd use `sessions_spawn` with the skill enabled/disabled. The eval framework concept is sound, but the execution layer is different.

**Action:** Build an OpenClaw-native eval runner that:
- Takes a skill + test cases (evals.json)
- Spawns parallel sub-agents via `sessions_spawn` with the skill in context
- Spawns baseline sub-agents without the skill
- Grades outputs against assertions
- Reports pass rate, token usage, latency

### 4. Trigger optimization

Anthropic's `improve_description.py` rewrites descriptions based on eval results. Same principle applies — if a skill triggers 50% of the time, we're leaving value on the table. The description is the only thing the model sees at decision time.

**Action:** After evals exist, build a trigger test that sends ambiguous prompts and measures whether the agent loads the right skill.

### 5. Validation — use `skills-ref` but add OpenClaw checks

The official `skills-ref` validator checks spec compliance (name format, description length, frontmatter fields). But it doesn't know about OpenClaw's extensions:
- `metadata.openclaw.requires.*` (gating)
- `metadata.openclaw.install` (installer specs)
- `user-invocable`, `disable-model-invocation`, `command-dispatch` (slash commands)
- Single-line JSON constraint on metadata

**Action:** Extend our CI to run `skills-ref validate` for base spec compliance + our own checks for OpenClaw-specific fields.

### 6. The spec is converging — but OpenClaw has extensions

OpenClaw follows the AgentSkills spec for layout and intent. The `skills-ref` validator's allowed fields are: `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`. OpenClaw adds: `homepage`, `user-invocable`, `disable-model-invocation`, `command-dispatch`, `command-tool`, `command-arg-mode`. These extensions are fine — the spec's `metadata` field is intentionally extensible — but we should document them clearly.

## Revised Action Plan (OpenClaw-First)

### Phase 1: Quality (quick wins)
1. **Description audit** — rewrite all 11 descriptions to be trigger-explicit
2. **Line count audit** — verify all SKILL.md files are under 500 lines
3. **CI: add `skills-ref validate`** alongside our existing checks
4. **Document OpenClaw extensions** in the repo README

### Phase 2: Testing
5. **Build evals.json for each skill** — 3-5 test cases per skill
6. **Build OpenClaw eval runner** — `sessions_spawn` based A/B testing
7. **Add eval results to CI** — not just "does it parse?" but "does it improve output?"

### Phase 3: Distribution
8. **ClawHub sync** — ensure all 11 skills are publishable via `clawhub`
9. **Trigger optimization** — automated description improvement based on eval data

## Sources
- Anthropic skills repo: https://github.com/anthropics/skills
- Agent Skills spec: https://agentskills.io/specification
- Anthropic blog: https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills
- Platform docs: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- skills-ref validator: https://github.com/agentskills/agentskills
- OpenClaw skills docs: ~/openclaw/docs/tools/skills.md
- OpenClaw creating-skills docs: ~/openclaw/docs/tools/creating-skills.md
