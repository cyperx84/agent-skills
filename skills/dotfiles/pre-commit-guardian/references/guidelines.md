# Extended Reference

<!-- Moved from SKILL.md to keep it under 500 lines -->

5. Result: ✅ Commit allowed

Pre-Commit Guardian: All validations passed
- yabai config: ✅ Valid
- 0 errors, 0 warnings
- Safe to commit!
```

### Example 2: Syntax Error Caught

**User**: "Commit dotfiles changes"

**Skill Actions**:
```
1. Detect staged files: yabai/.config/yabai/yabairc, zsh/.zshrc
2. Validate yabai config: FAILED ❌
   Error: Line 23: unknown command 'invalid_command'
3. Validate zsh script: PASSED ✅
4. Result: ❌ Commit BLOCKED

Pre-Commit Guardian: Validation FAILED
❌ yabai config has syntax error at line 23
   Found: invalid_command
   Expected: valid yabai command

💡 Fix:
1. Open file: nvim +23 yabai/.config/yabai/yabairc
2. Check documentation: yabai --help
3. Fix the error
4. Try commit again

🚫 Commit blocked to prevent broken config
```

### Example 3: Auto-Fix Applied

**User**: "Safe commit my shell scripts"

**Skill Actions**:
```
1. Detect staged files: setup.sh, install.sh
2. Validate with shellcheck:
   - setup.sh: 2 warnings (missing quotes)
   - install.sh: 1 warning (trailing whitespace)
3. Offer auto-fix: User confirms
4. Apply fixes:
   - Added quotes around variables
   - Removed trailing whitespace
5. Re-validate: All PASSED ✅
6. Stage auto-fixes
7. Result: ✅ Commit allowed

Pre-Commit Guardian: Auto-fixes applied
✨ Fixed 3 issues automatically:
- setup.sh: Added quotes (2 places)
- install.sh: Removed trailing whitespace

✅ All validations now pass
📝 Auto-fixes staged for commit
```

### Example 4: Missing Validator Warning

**User**: "Commit my Lua plugins"

**Skill Actions**:
```
1. Detect staged files: 5 .lua files
2. Check for Lua validator:
   - luacheck: Not installed
   - lua -c: Available (fallback)
3. Validate with fallback: All PASSED ✅
4. Result: ✅ Commit allowed (with warning)

Pre-Commit Guardian: Validation passed (limited)
⚠️ luacheck not installed - using basic validation

✅ Syntax check: All files valid
⚠️ Style check: Skipped (install luacheck for full validation)

💡 Recommendation: brew install luacheck

✅ Commit allowed
```

### Example 5: Multiple File Types

**User**: "Commit all my dotfiles changes"

**Skill Actions**:
```
1. Detect staged files:
   - 3 shell scripts
   - 2 Lua files
   - 1 JSON file
   - 1 yabai config
   - 1 TOML file
2. Run 4 different validators
3. Results:
   - Shell: 3/3 passed ✅
   - Lua: 2/2 passed ✅
   - JSON: 1/1 passed ✅
   - Yabai: 1/1 passed ✅
   - TOML: 1/1 passed ⚠️ (validator missing, skipped)
4. Result: ✅ Commit allowed

Pre-Commit Guardian: Multi-file validation complete
✅ 7/8 files fully validated
⚠️ 1 file skipped (TOML validator not installed)

📊 Results by type:
- Shell scripts (3): ✅ All valid
- Lua scripts (2): ✅ All valid
- JSON (1): ✅ Valid
- Yabai config (1): ✅ Valid
- TOML (1): ⚠️ Skipped

⏱️ Total time: 1.8 seconds
✅ Commit allowed
```

## Guidelines

### DO:
✅ Validate all critical config files before commits
✅ Use appropriate validators for each file type
✅ Block commits on syntax errors and security issues
✅ Provide specific error messages with line numbers
✅ Offer auto-fix for simple issues
✅ Show clear fix suggestions for complex issues
✅ Allow override with --no-verify (document why)
✅ Track validation metrics over time
✅ Install as git pre-commit hook for automation
✅ Warn about missing validators but don't block
✅ Provide fallback validators when possible
✅ Test validators are working before relying on them

### DON'T:
❌ Block commits for style warnings only
❌ Run validators that aren't installed (check first)
❌ Modify user's git configuration without permission
❌ Validate files that aren't staged (respect git workflow)
❌ Use overly strict rules that block legitimate code
❌ Hide validator output (show full errors for debugging)
❌ Auto-fix without user confirmation
❌ Proceed if critical validators fail to run
❌ Ignore validator exit codes
❌ Skip validation on "minor" changes (syntax errors can be anywhere)
❌ Make commits slower than necessary (optimize validator calls)
❌ Validate binary files or non-config files

## Advanced Features

### Intelligent Caching

Cache validation results for unchanged files:

```bash
# Hash file content
FILE_HASH=$(shasum -a 256 "$file" | cut -d' ' -f1)

# Check cache
if [ -f "$CACHE_DIR/$FILE_HASH.valid" ]; then
  echo "✅ Using cached validation result for $file"
  continue
fi

# Run validation and cache result
if validate_file "$file"; then
  touch "$CACHE_DIR/$FILE_HASH.valid"
fi
```

**Benefits**:
- Faster validations on re-commits
- Reduced validator overhead
- Better performance for large repos

### Parallel Validation

Run validators in parallel for speed:

```bash
# Validate multiple files concurrently
for file in "${staged_files[@]}"; do
  validate_file "$file" &
  pids+=($!)
done

# Wait for all validators to finish
for pid in "${pids[@]}"; do
  wait "$pid" || VALIDATION_FAILED=true
done
```

**Use Case**: Large commits with many files

### Custom Validator Configuration

Allow users to define custom validators:

```yaml
# .pre-commit-guardian.yml
validators:
  yabai:
    command: "yabai --check-config"
    files: ["*yabairc*", "*.yabai.yml"]
    blocking: true

  custom_lua:
    command: "luacheck --globals vim --std max"
    files: ["*.lua"]
    blocking: false
```

### Fix Suggestions Database

Build database of common errors and fixes:

```yaml
errors:
  - pattern: "SC2086"
    description: "Double quote to prevent globbing"
    fix_template: 'Change $VAR to "$VAR"'
    auto_fixable: true

  - pattern: "yabai.*unknown command"
    description: "Invalid yabai command"
    fix_template: "Check: yabai --help"
    documentation: "https://github.com/koekeishiya/yabai/wiki"
```

### Integration with CI/CD

Export validation results for CI systems:

```bash
# Generate JUnit XML report
generate_junit_xml "$VALIDATION_RESULTS" > validation-report.xml

# Or JSON for GitHub Actions
jq -n \
  --arg status "$OVERALL_STATUS" \
  --arg errors "$ERROR_COUNT" \
  '{"status": $status, "errors": ($errors|tonumber)}' \
  > validation-report.json
```

## Dependencies

### Required
- **git** - Version control (built-in on macOS)
  - Used to detect staged files
  - Pre-commit hook integration

### Highly Recommended
- **shellcheck** - `brew install shellcheck`
  - Validates shell scripts (bash, zsh)
  - Catches common shell script errors

- **yabai** - `brew install yabai`
  - Validates yabai configs
  - Required if using yabai window manager

### Optional
- **luacheck** - `brew install luacheck`
  - Advanced Lua validation
  - Falls back to `lua -c` if not available

- **jq** - `brew install jq`
  - JSON validation and formatting
  - Widely used for JSON handling

- **taplo** - `brew install taplo`
  - TOML validation and formatting
  - Optional but recommended for TOML configs

- **shfmt** - `brew install shfmt`
  - Shell script formatting
  - Enables auto-fix features

## Configuration

### Install as Git Pre-Commit Hook

**Automatic Installation**:

```bash
# Let the skill install itself as a hook
claude-code "install pre-commit guardian as git hook"
```

**Manual Installation**:

```bash
# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
claude-code "run pre-commit validation"
exit $?
EOF

# Make executable
chmod +x .git/hooks/pre-commit
```

### Configure Validation Behavior

Set via environment variables or config file:

```bash
# Environment variables (in .zshrc or .bashrc)
export PRE_COMMIT_GUARDIAN_STRICT=true      # Block on warnings
export PRE_COMMIT_GUARDIAN_AUTO_FIX=true    # Auto-fix when possible
export PRE_COMMIT_GUARDIAN_CACHE=true       # Enable caching
export PRE_COMMIT_GUARDIAN_PARALLEL=true    # Parallel validation

# Or create .pre-commit-guardian.toml
cat > .pre-commit-guardian.toml << 'EOF'
strict_mode = false
auto_fix = true
enable_cache = true
parallel_validation = true

[validators]
shellcheck_severity = "warning"  # error, warning, info, style
luacheck_std = "max"            # lua51, lua52, max
EOF
```

### Bypass Validation

Sometimes you need to commit without validation:

```bash
# Skip pre-commit hook (use with caution)
git commit --no-verify -m "Emergency fix - validation skipped"

# Temporary disable
export SKIP_PRE_COMMIT_GUARDIAN=true
git commit -m "Message"
unset SKIP_PRE_COMMIT_GUARDIAN
```

## Troubleshooting

### Common Issues

**Issue**: "Validator not found: shellcheck"
**Solution**:
```bash
# Install missing validator
brew install shellcheck

# Or disable that validator
export PRE_COMMIT_GUARDIAN_SKIP_SHELLCHECK=true
```

**Issue**: "Validation is too slow"
**Solution**:
```bash
# Enable caching
export PRE_COMMIT_GUARDIAN_CACHE=true

# Enable parallel validation
export PRE_COMMIT_GUARDIAN_PARALLEL=true

# Or skip non-critical validators
export PRE_COMMIT_GUARDIAN_SKIP_STYLE_CHECKS=true
```

**Issue**: "False positives blocking commits"
**Solution**:
```bash
# Disable strict mode
export PRE_COMMIT_GUARDIAN_STRICT=false

# Or add exceptions to config
echo "ignore_pattern = 'SC2034'" >> .pre-commit-guardian.toml
```

**Issue**: "Auto-fix made unwanted changes"
**Solution**:
```bash
# Disable auto-fix
export PRE_COMMIT_GUARDIAN_AUTO_FIX=false

# Revert changes
git restore --staged .
git restore .

# Restore from backup
git reflog
git reset --hard <commit-before-auto-fix>
```

**Issue**: "Hook doesn't run"
**Solution**:
```bash
# Check hook exists and is executable
ls -la .git/hooks/pre-commit
cat .git/hooks/pre-commit

# Make executable if needed
chmod +x .git/hooks/pre-commit

# Test manually
.git/hooks/pre-commit
```

## Success Metrics

A successful Pre-Commit Guardian execution includes:
- ✅ All staged files detected correctly
- ✅ Appropriate validators selected for each file type
- ✅ All available validators executed successfully
- ✅ Clear error messages with line numbers for failures
- ✅ Actionable fix suggestions provided
- ✅ Correct commit gate decision (block/allow)
- ✅ Validation completed in < 5 seconds for typical commits
- ✅ Zero false negatives (missed errors that should have been caught)
- ✅ Minimal false positives (< 5% blocking valid code)

## Integration

Works seamlessly with:
- **[Stow Health Manager](../stow-health-manager/)** - Validates symlinks before commit
- **[Service Orchestrator](../service-orchestrator/)** - Test services after config changes
- **[Theme Switcher](../theme-switcher/)** - Validate theme configs before commit

### Workflow Example

```bash
# 1. Make config changes
nvim ~/.config/yabai/yabairc

# 2. Test changes
brew services restart yabai

# 3. Stage changes
git add .

# 4. Commit (Pre-Commit Guardian runs automatically)
git commit -m "Update yabai config"
# → Validates yabairc
# → Checks for syntax errors
# → Allows/blocks commit
# → Shows detailed results

# 5. If blocked, fix and retry
nvim +23 ~/.config/yabai/yabairc  # Fix error at line 23
git add .
git commit -m "Update yabai config"
# → Validates again
# → Passes
# → Commit succeeds
```

## Version History

- v1.0.0 (2025-10-30): Initial production release
  - Full validation workflow
  - 6 validator types supported
  - Auto-fix capabilities
  - Git hook integration
  - Caching and parallel execution
  - Comprehensive error reporting
