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
| [multiplan](skills/multiplan/) | 4-model parallel planning workflow (Claude, Gemini, Codex, GLM-5) |
| [content-breakdown](skills/content-breakdown/) | Turn articles, videos, and docs into structured findings and notes |
| [clawforge](skills/clawforge/) | Agent swarm workflow — spawn, monitor, review, and manage coding agents |

### Productivity

| Skill | Description |
|-------|-------------|
| [lattice](skills/lattice/) | Mental models and cognitive frameworks for decisions and analysis |
| [cyperx-voice](skills/cyperx-voice/) | Write in CyperX's exact voice — direct, casual, internet-native |
| [imagegen](skills/imagegen/) | Generate and edit images from text prompts (Google Gemini) |
| [ai-compat](skills/ai-compat/) | Search and compare AI model + harness compatibility pairings |
| [instagram](skills/instagram/) | Control Instagram — browse feed, DMs, stories, post content |

### Dotfiles (10 skills)

| Skill | Description |
|-------|-------------|
| [pre-commit-guardian](skills/dotfiles/pre-commit-guardian/) | Validate config files before git commits |
| [stow-health-manager](skills/dotfiles/stow-health-manager/) | Monitor GNU Stow symlink health |
| [service-orchestrator](skills/dotfiles/service-orchestrator/) | Manage dotfile-dependent services (restart, reload, validate) |
| [theme-switcher](skills/dotfiles/theme-switcher/) | Switch between dotfile themes (Alacritty, Ghostty, tmux, nvim) |
| [sketchybar-plugin-dev](skills/dotfiles/sketchybar-plugin-dev/) | Scaffold and develop SketchyBar plugins |
| [api-doc-generator](skills/dotfiles/api-doc-generator/) | Generate API documentation from source |
| [db-migration-assistant](skills/dotfiles/db-migration-assistant/) | Generate and run database migrations |
| [dependency-update-manager](skills/dotfiles/dependency-update-manager/) | Check and update project dependencies |
| [environment-setup-validator](skills/dotfiles/environment-setup-validator/) | Validate dev environment setup |
| [test-coverage-analyzer](skills/dotfiles/test-coverage-analyzer/) | Analyze and improve test coverage |

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
