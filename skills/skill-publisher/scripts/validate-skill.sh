#!/usr/bin/env bash
set -euo pipefail

# validate-skill.sh — Validate a skill directory against AgentSkills spec
# Usage: validate-skill.sh <skill-path>

SKILL_PATH="${1:?Usage: validate-skill.sh <skill-path>}"
ERRORS=0
WARNINGS=0

if [ ! -d "$SKILL_PATH" ]; then
  echo "❌ Not a directory: $SKILL_PATH"
  exit 1
fi

NAME=$(basename "$SKILL_PATH")
echo "Validating skill: $NAME"

# 1. SKILL.md must exist
if [ ! -f "$SKILL_PATH/SKILL.md" ]; then
  echo "❌ Missing SKILL.md"
  ERRORS=$((ERRORS + 1))
  exit 1
fi
echo "✅ SKILL.md exists"

# 2. YAML frontmatter check
SKILL_FILE="$SKILL_PATH/SKILL.md"
if ! head -1 "$SKILL_FILE" | grep -q '^---'; then
  echo "❌ SKILL.md must start with YAML frontmatter (---)"
  ERRORS=$((ERRORS + 1))
fi

# Extract frontmatter (between first two --- lines)
FM=$(awk '/^---/{n++; next} n==1' "$SKILL_FILE")
if [ -z "$FM" ]; then
  echo "❌ SKILL.md frontmatter is empty"
  ERRORS=$((ERRORS + 1))
fi

# 3. Required fields
if ! echo "$FM" | grep -q '^name:'; then
  echo "❌ Missing 'name' field in frontmatter"
  ERRORS=$((ERRORS + 1))
fi

if ! echo "$FM" | grep -q '^description:'; then
  echo "❌ Missing 'description' field in frontmatter"
  ERRORS=$((ERRORS + 1))
fi

# 4. Name validation
if echo "$FM" | grep -q '^name:'; then
  SKILL_NAME=$(echo "$FM" | grep '^name:' | sed 's/name: *//' | tr -d '"' | tr -d "'")
  if ! echo "$SKILL_NAME" | grep -qE '^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$'; then
    echo "❌ name '$SKILL_NAME' must be lowercase, hyphens only, no leading/trailing hyphens"
    ERRORS=$((ERRORS + 1))
  fi
  if [ "$SKILL_NAME" != "$NAME" ]; then
    echo "❌ name '$SKILL_NAME' must match directory name '$NAME'"
    ERRORS=$((ERRORS + 1))
  fi
  echo "✅ name: $SKILL_NAME"
fi

# 5. Description length
if echo "$FM" | grep -q '^description:'; then
  DESC=$(echo "$FM" | awk '/^description:/{sub(/^description:[[:space:]]*>?[[:space:]]*/, ""); found=1} found && /^[[:space:]]/{sub(/^[[:space:]]/, ""); print} found && !/^[[:space:]]/{if(found && !printed){print ""; printed=1}}' | tr -s ' ' | tr -d "'" | tr -d '"' | xargs)
  [ -z "$DESC" ] && DESC=$(echo "$FM" | grep '^description:' | sed 's/description: *//' | sed 's/^> *//' | tr -d '"' | tr -d "'" | xargs)
  DESC_LEN=${#DESC}
  if [ "$DESC_LEN" -gt 1024 ]; then
    echo "⚠️  description is ${DESC_LEN} chars (max 1024)"
    WARNINGS=$((WARNINGS + 1))
  fi
  echo "✅ description: ${DESC_LEN} chars"
fi

# 6. Line count
LINES=$(wc -l < "$SKILL_FILE" | tr -d ' ')
if [ "$LINES" -gt 500 ]; then
  echo "⚠️  SKILL.md is ${LINES} lines (recommended max: 500)"
  WARNINGS=$((WARNINGS + 1))
else
  echo "✅ SKILL.md: ${LINES} lines"
fi

# 7. No symlinks
SYMLINKS=$(find "$SKILL_PATH" -type l)
if [ -n "$SYMLINKS" ]; then
  echo "❌ Contains symlinks:"
  echo "$SYMLINKS"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ No symlinks"
fi

# 8. Structure check
ALLOWED="SKILL.md scripts references assets package.json"
for item in "$SKILL_PATH"/*; do
  [ -e "$item" ] || continue
  base=$(basename "$item")
  if ! echo "$ALLOWED" | grep -qw "$base"; then
    echo "⚠️  Unexpected top-level file/directory: $base"
    WARNINGS=$((WARNINGS + 1))
  fi
done
echo "✅ Structure check passed"

# 9. Scripts executable
if [ -d "$SKILL_PATH/scripts" ]; then
  for script in "$SKILL_PATH/scripts"/*; do
    [ -f "$script" ] || continue
    if file "$script" | grep -q "script" && [ ! -x "$script" ]; then
      echo "⚠️  $(basename "$script") is not executable"
      WARNINGS=$((WARNINGS + 1))
    fi
  done
  echo "✅ Script permissions checked"
fi

# Summary
echo ""
if [ "$ERRORS" -gt 0 ]; then
  echo "❌ Validation FAILED: $ERRORS error(s), $WARNINGS warning(s)"
  exit 1
elif [ "$WARNINGS" -gt 0 ]; then
  echo "⚠️  Validation passed with $WARNINGS warning(s)"
else
  echo "✅ Validation passed"
fi
