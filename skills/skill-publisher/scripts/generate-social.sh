#!/usr/bin/env bash
set -euo pipefail

# generate-social.sh — Generate social media posts for a skill
# Usage: generate-social.sh <skill-name>

SKILL_NAME="${1:?Usage: generate-social.sh <skill-name>}"
MONO_ROOT="$(cd "$(dirname "$0")"/../../.. && pwd)"
SKILL_PATH="$MONO_ROOT/skills/$SKILL_NAME"

if [ ! -f "$SKILL_PATH/SKILL.md" ]; then
  echo "❌ Skill not found: $SKILL_NAME"
  exit 1
fi

# Extract metadata
NAME=$(grep '^name:' "$SKILL_PATH/SKILL.md" | head -1 | sed 's/name: *//' | tr -d '"'"'")
DESC=$(grep '^description:' "$SKILL_PATH/SKILL.md" | head -1 | sed 's/description: *>[[:space:]]*//' | sed 's/description: *//' | tr -d '"' | tr -d "'" | xargs)
VERSION=$(grep 'version:' "$SKILL_PATH/SKILL.md" | head -1 | sed 's/.*version: *//' | tr -d '"' | tr -d "'")
[ -z "$VERSION" ] && VERSION="1.0.0"

GITHUB_URL="https://github.com/cyperx84/agent-skills"

echo "## Social Posts for $NAME (v$VERSION)"
echo ""

# Reddit
echo "### Reddit"
echo ""
SUBREDDITS=("r/aiagents" "r/AI_Agents" "r/OpenClaw" "r/claudecode")
for sub in "${SUBREDDITS[@]}"; do
  echo "**$sub**"
  echo ""
  echo "Title: [$NAME] - $DESC"
  echo ""
  echo "Body:"
  cat <<REDDIT
$DESC

**Install:** \`npx skills add cyperx84/agent-skills/$NAME\`

Works with: Claude Code, Cursor, Codex, Copilot, Windsurf, Gemini CLI, OpenClaw, and any AgentSkills-compatible agent.

Source: $GITHUB_URL
REDDIT
  echo ""
  echo "---"
  echo ""
done

# X (Twitter)
echo "### X (Twitter)"
echo ""
cat <<XPOST
$DESC

Install: npx skills add cyperx84/agent-skills/$NAME

Works across Claude Code, Cursor, Codex, Copilot + more

#AgentSkills #ClaudeCode #AI
XPOST
echo ""
echo "---"
echo ""

# DEV.to
echo "### DEV.to"
echo ""
cat <<DEVTO
# $NAME

$DESC

## Install

\`\`\`bash
npx skills add cyperx84/agent-skills/$NAME
\`\`\`

## What It Does

[Paste key features from SKILL.md here]

## Compatible Agents

Claude Code, Cursor, Codex, Copilot, Windsurf, Gemini CLI, OpenClaw, and any [AgentSkills](https://agentskills.io) compatible agent.

## Source

[$GITHUB_URL]($GITHUB_URL)
DEVTO
echo ""
echo "---"
echo ""
echo "Done. Copy each post and publish manually."
