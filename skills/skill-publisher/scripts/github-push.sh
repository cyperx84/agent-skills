#!/usr/bin/env bash
set -euo pipefail

# github-push.sh — Copy skill to mono-repo and push as a branch
# Usage: github-push.sh <skill-path> [--dry-run]

SKILL_PATH="${1:?Usage: github-push.sh <skill-path> [--dry-run]}"
DRY_RUN=false
if [[ "${2:-}" == "--dry-run" ]]; then
  DRY_RUN=true
fi

# Determine mono-repo root (script lives at skills/skill-publisher/scripts/)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MONO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

NAME=$(basename "$SKILL_PATH")
DEST="$MONO_ROOT/skills/$NAME"

echo "Pushing skill: $NAME"
echo "Mono-repo root: $MONO_ROOT"

# Validate first
echo ""
echo "Step 1: Validating..."
bash "$SCRIPT_DIR/validate-skill.sh" "$SKILL_PATH"

# Check if skill already exists in mono-repo
if [ -d "$DEST" ]; then
  echo "❌ Skill '$NAME' already exists in mono-repo at $DEST"
  echo "   Remove it first or use a different name."
  exit 1
fi

if [ "$DRY_RUN" = true ]; then
  echo ""
  echo "=== DRY RUN — would copy $SKILL_PATH → $DEST ==="
  echo "=== Branch: skill/$NAME ==="
  exit 0
fi

# Copy skill
echo ""
echo "Step 2: Copying to mono-repo..."
cp -r "$SKILL_PATH" "$DEST"
echo "✅ Copied to $DEST"

# Create branch and commit
echo ""
echo "Step 3: Creating branch and committing..."
cd "$MONO_ROOT"
BRANCH="skill/$NAME"
git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"
git add "skills/$NAME/"
git commit -m "Add $NAME skill"

# Push
echo ""
echo "Step 4: Pushing..."
git push -u origin "$BRANCH"
echo "✅ Pushed branch $BRANCH"
echo ""
echo "Next: Create a PR at https://github.com/cyperx84/agent-skills/compare/$BRANCH?expand=1"
