---
name: pre-commit-guardian
description: >
  Validates configuration files before git commits to prevent broken configs from entering the repository. Automatically selects appropriate validators (yabai, shellcheck, luacheck, etc.) based on file type and blocks commits on validation failure. Use when user wants to commit dotfiles changes safely. Triggers: validate before commit, check configs before push, verify dotfiles integrity, safe commit, pre-commit check
license: MIT
metadata:
  author: cyperx
  version: "1.0.0"
  openclaw: true
  categories: [dev, dotfiles]
---


# Pre-Commit Guardian Skill

## Purpose

The Pre-Commit Guardian prevents catastrophic dotfiles failures by validating all configuration files before they're committed to git. A single syntax error in a yabai config or shell script can break your entire window management system. This skill catches those errors before they're committed, preventing broken configs from entering your repository and potentially spreading to other machines.

## When to Use This Skill

Activate when the user:
- Wants to commit changes to dotfiles safely
- Asks to "validate configs before commit"
- Mentions "pre-commit check" or "verify before push"
- Is about to commit changes to critical config files (yabai, skhd, sketchybar, tmux, zsh, etc.)
- Wants to install automated pre-commit validation
- Mentions keywords like: "safe commit", "validate dotfiles", "check syntax", "pre-commit hook"

## Workflow

### Phase 1: Detection & Analysis

**Detect Staged Changes**:

```bash
# Get list of staged files
git diff --cached --name-only

# Categorize files by type
# - .yabairc, yabai.yml → Yabai configs
# - .skhdrc, skhd.yml → SKHD configs
# - sketchybarrc, *.lua → SketchyBar configs
# - .zshrc, .bashrc, *.sh → Shell scripts
# - *.lua → Lua scripts
# - *.toml → TOML configs
# - *.json → JSON configs
# - .tmux.conf → Tmux configs
```

**Determine Validators Needed**:

Map each file type to appropriate validator:
- **Yabai configs** → `yabai --check-config`
- **SKHD configs** → `skhd --check-config` (if available) or parse manually
- **Shell scripts** → `shellcheck`
- **Lua scripts** → `luacheck` or `lua -c`
- **TOML files** → `taplo check` or custom parser
- **JSON files** → `jq` validation
- **Tmux configs** → `tmux -f <file> source-file <file>`

**Check Validator Availability**:

```bash
# Check which validators are installed
command -v yabai >/dev/null 2>&1 && echo "yabai: available"
command -v shellcheck >/dev/null 2>&1 && echo "shellcheck: available"
command -v luacheck >/dev/null 2>&1 && echo "luacheck: available"
command -v jq >/dev/null 2>&1 && echo "jq: available"
command -v taplo >/dev/null 2>&1 && echo "taplo: available"
```

**What to check**:
- Number of staged files to validate
- Which validators are needed
- Which validators are available
- Any missing validators (warn but don't block)
- Estimated validation time

### Phase 2: Pre-Validation Preparation

**Backup Current State**:

Create safety backup before validation testing:

```bash
# Create temporary backup of staged changes
git stash push --keep-index -m "pre-commit-guardian-backup-$(date +%s)"
```

**Set Up Validation Environment**:

```bash
# Create temporary validation directory
VALIDATION_DIR=$(mktemp -d)
export VALIDATION_DIR

# Copy staged files to validation directory
git diff --cached --name-only | while read file; do
  mkdir -p "$VALIDATION_DIR/$(dirname "$file")"
  git show ":$file" > "$VALIDATION_DIR/$file"
done
```

**Key Decisions**:
- If no validators available → Warn but allow commit (user choice)
- If critical validators missing (yabai, shellcheck) → Strong warning
- If staged changes include critical configs → Require validation success
- If only documentation changed → Skip validation
- Otherwise → Proceed with full validation

### Phase 3: Validation Execution

**Run Validators Sequentially**:

For each staged file, run appropriate validator:

```bash
# Example: Validate yabai config
if [[ $file == *"yabairc"* ]]; then
  echo "Validating yabai config..."
  yabai --check-config 2>&1
  YABAI_EXIT=$?

  if [ $YABAI_EXIT -ne 0 ]; then
    echo "❌ Yabai config validation failed!"
    VALIDATION_FAILED=true
  fi
fi

# Example: Validate shell script
if [[ $file == *.sh ]] || [[ $file == *"zshrc"* ]]; then
  echo "Validating shell script: $file"
  shellcheck "$file" 2>&1
  SHELL_EXIT=$?

  if [ $SHELL_EXIT -ne 0 ]; then
    echo "❌ Shellcheck failed: $file"
    VALIDATION_FAILED=true
  fi
fi

# Example: Validate Lua script
if [[ $file == *.lua ]]; then
  echo "Validating Lua script: $file"
  if command -v luacheck >/dev/null 2>&1; then
    luacheck "$file" 2>&1
  else
    lua -c "$file" 2>&1
  fi
  LUA_EXIT=$?

  if [ $LUA_EXIT -ne 0 ]; then
    echo "❌ Lua validation failed: $file"
    VALIDATION_FAILED=true
  fi
fi

# Example: Validate JSON
if [[ $file == *.json ]]; then
  echo "Validating JSON: $file"
  jq empty "$file" 2>&1
  JSON_EXIT=$?

  if [ $JSON_EXIT -ne 0 ]; then
    echo "❌ JSON validation failed: $file"
    VALIDATION_FAILED=true
  fi
fi
```

**Collect Validation Results**:

```bash
# Track results per file
declare -A VALIDATION_RESULTS
VALIDATION_RESULTS[$file]="$VALIDATOR_EXIT_CODE"

# Track overall status
TOTAL_FILES=0
PASSED_FILES=0
FAILED_FILES=0
SKIPPED_FILES=0
```

**Error Handling**:

If validation fails for any file:
1. **Capture error output** with line numbers and specific issues
2. **Parse error messages** to extract actionable information
3. **Map to source file locations** (critical for includes/imports)
4. **Generate fix suggestions** based on error type
5. **Prepare detailed failure report**

### Phase 4: Results Analysis

**Parse Validation Errors**:

Extract meaningful information from validator output:

```bash
# Example: Parse shellcheck errors
# SC2034: var appears unused. Verify use (or export if used externally).
# Line 42: FOO="bar"

# Example: Parse yabai errors
# yabai: configuration file '/Users/user/.yabairc' line 23: unknown command 'invalid_command'

# Example: Parse Lua errors
# syntax error: /path/to/file.lua:15: unexpected symbol near '}'
```

**Categorize Issues**:

- **Syntax errors** (blocking): Must fix before commit
- **Style warnings** (non-blocking): Can commit but should fix
- **Unused variables** (non-blocking): Informational
- **Security issues** (blocking): Must fix before commit
- **Deprecation warnings** (non-blocking): Should fix soon

**Determine Commit Gate Status**:

```bash
# Block commit if:
# - Any syntax errors found
# - Any security issues found
# - Critical config files failed validation
# - User previously requested strict mode

# Allow commit if:
# - Only style warnings
# - Only informational messages
# - User explicitly overrides (--no-verify)
```

### Phase 5: Auto-Fix Attempts (Optional)

**Attempt Safe Auto-Fixes**:

For certain types of issues, offer automatic fixes:

```bash
# Example: Fix trailing whitespace
sed -i '' 's/[[:space:]]*$//' "$file"

# Example: Fix missing newline at EOF
echo "" >> "$file"

# Example: Format JSON
jq '.' "$file" > "$file.tmp" && mv "$file.tmp" "$file"

# Example: Format shell scripts
shfmt -w "$file"
```

**Re-validate After Fixes**:

```bash
# Run validators again on auto-fixed files
# Update validation results
# Report which fixes were successful
```

**User Interaction**:

For fixes that can't be automated:
- Show exact error location
- Suggest specific fix
- Offer to open file in editor at error line
- Provide documentation links

### Phase 6: Commit Gate Decision

**Block Commit**:

If validation failed with blocking errors:

```bash
# Exit with non-zero status to block git commit
exit 1
```

**Report blocking errors**:
```
❌ Pre-Commit Validation FAILED - Commit Blocked

🛑 Blocking Issues Found:

1. yabai/.config/yabai/yabairc:23
   ❌ Unknown command 'invalid_command'
   💡 Fix: Check yabai documentation for valid commands

2. zsh/.zshrc:142
   ❌ SC2086: Double quote to prevent globbing and word splitting
   💡 Fix: Change $var to "$var"

📋 Summary:
❌ 2 files failed validation
⚠️ 3 warnings found
✅ 5 files passed

🚫 COMMIT BLOCKED - Fix errors above before committing

💡 To see full details: git diff --cached
💡 To skip validation (NOT recommended): git commit --no-verify
```

**Allow Commit**:

If validation passed or only non-blocking warnings:

```bash
# Exit with zero status to allow git commit
exit 0
```

**Report success**:
```
✅ Pre-Commit Validation PASSED

📊 Validation Results:
✅ 8 files validated
✅ 0 errors
⚠️ 2 warnings (non-blocking)

⚠️ Warnings:
1. zsh/.zshrc:89
   SC2034: FOO appears unused

2. sketchybar/plugins/battery.lua:42
   Unused variable: old_value

✅ COMMIT ALLOWED - Consider fixing warnings

⏱️ Validation time: 2.1 seconds
```

### Phase 7: Cleanup & Reporting

**Clean Up Temporary Files**:

```bash
# Remove validation directory
rm -rf "$VALIDATION_DIR"

# Pop git stash if created
git stash pop >/dev/null 2>&1 || true
```

**Generate Validation Report**:

```
🛡️ Pre-Commit Guardian - Validation Report

📊 Files Validated:
- yabai/.config/yabai/yabairc ✅
- skhd/.config/skhd/skhdrc ✅
- zsh/.zshrc ⚠️ (warnings)
- tmux/.tmux.conf ✅
- sketchybar/sketchybarrc ✅
- sketchybar/plugins/battery.lua ⚠️ (warnings)

🔍 Validators Used:
- Yabai config checker ✅
- Shellcheck ✅
- Luacheck ✅
- JSON validator (jq) ✅

📈 Statistics:
Total files: 8
Passed: 6
Warnings: 2
Failed: 0
Skipped: 0

⏱️ Total validation time: 2.1 seconds

🎯 Result: ✅ COMMIT ALLOWED
```

**Update Metrics**:

Track validation effectiveness:
- Total validations run
- Errors caught before commit
- Auto-fixes applied
- Time saved (vs debugging after commit)

## Examples

### Example 1: All Validations Pass

**User**: "Commit my yabai config changes"

**Skill Actions**:
```
1. Detect staged files: yabai/.config/yabai/yabairc
2. Select validator: yabai --check-config
3. Run validation: PASSED ✅
4. Check for warnings: None

---

*Extended details: [references/guidelines.md](references/guidelines.md)*
