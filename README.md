# Agent Skills

Agent skills by [CyperX](https://github.com/cyperx84) — write once, run everywhere.

Works with any [AgentSkills](https://agentskills.io) compatible agent: Claude Code, Cursor, Codex, Copilot, Windsurf, Gemini CLI, OpenClaw, and more.

## Skills

### Core

| Skill | Description |
|-------|-------------|
| [skill-publisher](skills/skill-publisher/) | Meta-skill: validate, publish, and distribute skills |
| [deep-research](skills/deep-research/) | Recursive breadth/depth research with parallel sub-agents |
| [clwatch](skills/clwatch/) | Detect coding tool updates and merge changelog deltas at session start |
| [research-spinoff](skills/research-spinoff/) | Research spin-off product ideas from an existing project |
| [research-flywheel](skills/research-flywheel/) | Mine conversations for research topics, deep research them, and produce digests |
| [multiplan](skills/multiplan/) | 4-model parallel planning workflow (Claude, Gemini, Codex, GLM-5) |
| [content-breakdown](skills/content-breakdown/) | Turn articles, videos, and docs into structured findings and notes |
| [clawforge](skills/clawforge/) | Agent swarm workflow — spawn, monitor, review, and manage coding agents |

### Productivity

| Skill | Description |
|-------|-------------|
| [lattice](skills/lattice/) | Mental models and cognitive frameworks for decisions and analysis |
| [cyperx-voice](skills/cyperx-voice/) | Write in CyperX's exact voice — direct, casual, internet-native |
| [instagram](skills/instagram/) | Control Instagram — browse feed, DMs, stories, post content |

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

## Add a Skill

```bash
# 1. Validate it meets the spec
bash skills/skill-publisher/scripts/validate-skill.sh path/to/your-skill

# 2. Add to mono-repo and push
git add skills/your-skill && git commit -m "Add your-skill" && git push
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
