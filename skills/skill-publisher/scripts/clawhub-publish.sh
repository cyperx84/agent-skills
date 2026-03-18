#!/usr/bin/env bash
set -euo pipefail

# clawhub-publish.sh — Publish a skill to ClawHub
# Usage: clawhub-publish.sh <skill-path> [--slug name] [--version 1.0.0]

SKILL_PATH="${1:?Usage: clawhub-publish.sh <skill-path> [--slug name] [--version 1.0.0]}"
shift

SLUG=""
VERSION=""

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --slug) SLUG="$2"; shift 2 ;;
    --version) VERSION="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

NAME=$(basename "$SKILL_PATH")

# Defaults
if [ -z "$SLUG" ]; then
  SLUG="$NAME"
fi
if [ -z "$VERSION" ]; then
  # Try to extract version from frontmatter
  VERSION=$(grep 'version:' "$SKILL_PATH/SKILL.md" 2>/dev/null | head -1 | sed 's/.*version: *//' | tr -d '"' | tr -d "'")
  if [ -z "$VERSION" ]; then
    VERSION="1.0.0"
  fi
fi

echo "Publishing to ClawHub..."
echo "  Skill: $NAME"
echo "  Slug: $SLUG"
echo "  Version: $VERSION"

# Check clawhub CLI
if ! command -v clawhub &> /dev/null; then
  echo "❌ clawhub CLI not found. Install with: brew install clawhub"
  exit 1
fi

# Validate first
echo ""
echo "Validating..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
bash "$SCRIPT_DIR/validate-skill.sh" "$SKILL_PATH"

# Publish
echo ""
echo "Publishing..."
clawhub publish "$SKILL_PATH" --slug "$SLUG" --version "$VERSION"

echo ""
echo "✅ Published $NAME@$VERSION to ClawHub"
