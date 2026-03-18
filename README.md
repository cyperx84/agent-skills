# Agent Skills

Agent skills by [CyperX](https://github.com/cyperx84) — write once, run everywhere.

Works with any [AgentSkills](https://agentskills.io) compatible agent: Claude Code, Cursor, Codex, Copilot, Windsurf, Gemini CLI, OpenClaw, and more.

## Skills

| Skill | Description | Install |
|-------|-------------|---------|
| [deep-research](skills/deep-research/) | Recursive breadth/depth research with parallel sub-agents | `npx skills add cyperx84/agent-skills/deep-research` |
| [skill-publisher](skills/skill-publisher/) | Meta-skill: validate, publish, and distribute skills | `npx skills add cyperx84/agent-skills/skill-publisher` |

## Install a Skill

```bash
# Via skills.sh (works with 18+ agents)
npx skills add cyperx84/agent-skills/<skill-name>

# Via ClawHub (OpenClaw users)
clawhub install <skill-name>

# Manual: just copy the skill folder into your agent's skills directory
```

## Use a Skill

Each skill has a `SKILL.md` with trigger phrases and instructions. Your agent loads it automatically when the trigger matches.

## Publish a Skill

```bash
# 1. Validate
bash skills/skill-publisher/scripts/validate-skill.sh path/to/your-skill

# 2. Push to mono-repo
bash skills/skill-publisher/scripts/github-push.sh path/to/your-skill

# 3. Publish to ClawHub
bash skills/skill-publisher/scripts/clawhub-publish.sh path/to/your-skill

# 4. Generate PRs for awesome-lists
bash skills/skill-publisher/scripts/generate-prs.sh your-skill-name

# 5. Generate social posts
bash skills/skill-publisher/scripts/generate-social.sh your-skill-name
```

## Skill Standard

Every skill follows the [AgentSkills spec](https://agentskills.io/specification):

```
skill-name/
├── SKILL.md              # Required — frontmatter + instructions (<500 lines)
├── scripts/              # Optional — executable automation
├── references/           # Optional — docs loaded on-demand
└── assets/               # Optional — templates, images, static files
```

SKILL.md frontmatter requires `name` and `description`. Optional: `license`, `allowed-tools`, `metadata`.

## CI

GitHub Actions validates every skill on push/PR:
- SKILL.md exists with valid frontmatter
- Name matches directory
- No symlinks
- Under 500 lines
- Clean directory structure
- Scripts executable

## License

MIT — [CyperX](https://github.com/cyperx84)
