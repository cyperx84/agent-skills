---
name: skill-publisher
description: "Validate, publish, and distribute OpenClaw skills to the agent-skills mono-repo and ClawHub. Checks SKILL.md structure, frontmatter compliance, and line counts. Use when the user says 'publish a skill', 'ship this skill', 'validate a skill', 'distribute skill', 'add skill to repo', or mentions skill-publisher."
license: MIT
metadata:
  { "author": "cyperx", "version": "1.0.0", "openclaw": true, "categories": ["dev", "productivity"] }
---

# skill-publisher

Validates, packages, and distributes agent skills across all channels from a single mono-repo.

## Trigger

Use when the user says any of:
- "publish [skill]"
- "ship this skill"
- "distribute [skill]"
- "validate [skill]"
- "skill-publisher [validate|publish|prs|social]"

## Commands

### `validate <path>`
Validates a skill directory against the AgentSkills spec.

Checks:
1. SKILL.md exists with valid YAML frontmatter (name, description)
2. Name matches directory name (lowercase, hyphens only)
3. No symlinks anywhere in the skill directory
4. SKILL.md under 500 lines
5. Scripts in `scripts/` are executable (if present)
6. No unexpected top-level files (only SKILL.md, scripts/, references/, assets/, package.json)

Run: `bash skills/skill-publisher/scripts/validate-skill.sh <path>`

### `publish <path> [--dry-run]`
Copies a validated skill into the mono-repo `skills/` directory, creates a branch, commits, and pushes.

Steps:
1. Run `validate` first (fails if invalid)
2. Check skill doesn't already exist in mono-repo
3. Copy skill into `skills/<name>/`
4. Create branch `skill/<name>`
5. Commit with message: `Add <name> skill`
6. Push branch (or show diff if `--dry-run`)

Run: `bash skills/skill-publisher/scripts/github-push.sh <path> [--dry-run]`

### `prs <skill-name>`
Generates copy-paste-ready PR bodies for all 6 awesome-lists.

Tier 2 targets:
- VoltAgent/awesome-agent-skills
- VoltAgent/awesome-openclaw-skills
- skillmatic-ai/awesome-agent-skills
- CommandCodeAI/agent-skills
- github/awesome-copilot
- sickn33/antigravity-awesome-skills

Run: `bash skills/skill-publisher/scripts/generate-prs.sh <skill-name>`

### `social <skill-name>`
Generates posts for Reddit, X (Twitter), and DEV.to.

Platforms:
- Reddit: r/aiagents, r/AI_Agents, r/OpenClaw, r/claudecode
- X: Thread with hashtag
- DEV.to: Article draft

Run: `bash skills/skill-publisher/scripts/generate-social.sh <skill-name>`

### `clawhub <path> [--slug name] [--version 1.0.0]`
Publishes to ClawHub using the `clawhub` CLI.

Requires: `clawhub` CLI installed (`clawhub install` or `brew install clawhub`).

Run: `bash skills/skill-publisher/scripts/clawhub-publish.sh <path> [--slug name] [--version 1.0.0]`

## Workflow

```
1. Build skill → 2. Validate → 3. Test → 4. Push to mono-repo → 5. CI passes → 6. Merge to main
                                                                                       ↓
                                                                    7. ClawHub publish → 8. Generate PRs → 9. Generate social posts
```

## References

- `references/distribution-channels.md` — all channels with URLs and PR targets
- `references/quality-checklist.md` — pre-publish checklist
