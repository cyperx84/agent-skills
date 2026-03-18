#!/usr/bin/env bash
set -euo pipefail

# generate-prs.sh — Generate PR bodies for awesome-lists
# Usage: generate-prs.sh <skill-name>

SKILL_NAME="${1:?Usage: generate-prs.sh <skill-name>}"
MONO_ROOT="$(cd "$(dirname "$0")"/../../.. && pwd)"
SKILL_PATH="$MONO_ROOT/skills/$SKILL_NAME"

if [ ! -f "$SKILL_PATH/SKILL.md" ]; then
  echo "❌ Skill not found: $SKILL_NAME"
  exit 1
fi

# Extract metadata
NAME=$(grep '^name:' "$SKILL_PATH/SKILL.md" | head -1 | sed 's/name: *//' | tr -d '"'"'")
DESC=$(grep '^description:' "$SKILL_PATH/SKILL.md" | head -1 | sed 's/description: *>[[:space:]]*//' | sed 's/description: *//' | tr -d '"' | tr -d "'" | xargs)
LICENSE=$(grep '^license:' "$SKILL_PATH/SKILL.md" | head -1 | sed 's/license: *//' | tr -d '"' | tr -d "'")
VERSION=$(grep 'version:' "$SKILL_PATH/SKILL.md" | head -1 | sed 's/.*version: *//' | tr -d '"' | tr -d "'")
[ -z "$VERSION" ] && VERSION="1.0.0"
[ -z "$LICENSE" ] && LICENSE="MIT"

GITHUB_URL="https://github.com/cyperx84/agent-skills/tree/main/skills/$NAME"
INSTALL_CMD="npx skills add cyperx84/agent-skills/$NAME"

PR_BODY="## $NAME

$DESC

**Install:** \`$INSTALL_CMD\`

**Source:** [$GITHUB_URL]($GITHUB_URL)

**License:** $LICENSE

---
*Skill from [cyperx84/agent-skills](https://github.com/cyperx84/agent-skills)*"

TARGETS=(
  "VoltAgent/awesome-agent-skills"
  "VoltAgent/awesome-openclaw-skills"
  "skillmatic-ai/awesome-agent-skills"
  "CommandCodeAI/agent-skills"
  "github/awesome-copilot"
  "sickn33/antigravity-awesome-skills"
)

echo "## PR Bodies for $NAME (v$VERSION)"
echo ""
echo "$PR_BODY"
echo ""
echo "---"
echo ""
echo "### Targets (copy-paste into each repo)"
echo ""

for target in "${TARGETS[@]}"; do
  echo "#### $target"
  echo "PR title: \`Add $NAME skill\`"
  echo "File: Edit README.md — add under appropriate category"
  echo "Entry: \`- [$NAME]($GITHUB_URL) — ${DESC:0:80}...\`"
  echo "URL: https://github.com/$target/compare/main...PR_BRANCH?expand=1"
  echo ""
done

echo "Done. Copy each PR body and submit manually."
