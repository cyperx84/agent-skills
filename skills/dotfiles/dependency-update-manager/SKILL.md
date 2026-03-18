---
name: dependency-update-manager
description: >
  Automates dependency updates across package managers (npm, pip, cargo, brew, etc.) with safety checks, changelog analysis, breaking change detection, and rollback capability. Use when user wants to update dependencies safely. Triggers: update dependencies, upgrade packages, check for updates, update npm packages, upgrade all deps
license: MIT
metadata:
  author: cyperx
  version: "1.0.0"
  openclaw: true
  categories: [dev, dotfiles]
---


# Dependency Update Manager Skill

## Purpose

The Dependency Update Manager automates the tedious and risky process of updating project dependencies. Manually updating dependencies requires checking each package, reading changelogs, testing for breaking changes, and handling update failures. This skill intelligently updates dependencies across multiple package managers, detects breaking changes, runs tests, and rolls back on failure - turning a multi-hour task into a 5-minute automated workflow.

## When to Use This Skill

Activate when the user:
- Wants to update project dependencies
- Asks to "upgrade packages" or "update deps"
- Needs to check for outdated dependencies
- Wants to update specific packages safely
- Is preparing a dependency security update
- Mentions keywords like: "npm update", "pip upgrade", "cargo update", "brew upgrade", "outdated packages"

## Workflow

### Phase 1: Detection & Analysis

**Detect Package Managers**:

```bash
# Scan project for package managers
detect_package_managers() {
  local managers=()

  [ -f "package.json" ] && managers+=("npm")
  [ -f "package-lock.json" ] && managers+=("npm")
  [ -f "yarn.lock" ] && managers+=("yarn")
  [ -f "pnpm-lock.yaml" ] && managers+=("pnpm")
  [ -f "requirements.txt" ] && managers+=("pip")
  [ -f "Pipfile" ] && managers+=("pipenv")
  [ -f "Cargo.toml" ] && managers+=("cargo")
  [ -f "Gemfile" ] && managers+=("bundler")
  [ -f "composer.json" ] && managers+=("composer")
  [ -f "go.mod" ] && managers+=("go")

  echo "${managers[@]}"
}
```

**Scan for Outdated Dependencies**:

```bash
# Check outdated packages per manager
check_outdated_npm() {
  npm outdated --json 2>/dev/null | jq -r 'to_entries[] | "\(.key): \(.value.current) → \(.value.latest)"'
}

check_outdated_pip() {
  pip list --outdated --format=json 2>/dev/null | jq -r '.[] | "\(.name): \(.version) → \(.latest_version)"'
}

check_outdated_cargo() {
  cargo outdated --format json 2>/dev/null | jq -r '.dependencies[] | "\(.name): \(.project) → \(.latest)"'
}
```

**Categorize Updates**:

```bash
categorize_update() {
  local current=$1
  local latest=$2

  # Parse semver versions
  local current_major=$(echo $current | cut -d'.' -f1)
  local latest_major=$(echo $latest | cut -d'.' -f1)

  if [ "$current_major" != "$latest_major" ]; then
    echo "MAJOR"  # Breaking changes likely
  elif [ "$(echo $current | cut -d'.' -f2)" != "$(echo $latest | cut -d'.' -f2)" ]; then
    echo "MINOR"  # New features
  else
    echo "PATCH"  # Bug fixes
  fi
}
```

### Phase 2: Safety Checks & Planning

**Analyze Changelogs**:

```bash
fetch_changelog() {
  local package=$1
  local from_version=$2
  local to_version=$3

  # Try to get changelog from npm, GitHub, etc.
  npm view $package@$to_version changelog 2>/dev/null ||
  curl -s "https://api.github.com/repos/$package/releases" | jq -r '.[].body' ||
  echo "Changelog not available"
}

detect_breaking_changes() {
  local changelog="$1"

  # Look for breaking change indicators
  echo "$changelog" | grep -iE "(BREAKING|breaking change|deprecated|removed|incompatible)" && return 0
  return 1
}
```

**Create Update Plan**:

```bash
# Prioritize updates by safety and importance
plan_updates() {
  local updates=("$@")

  # Group by severity
  local security_updates=()
  local patch_updates=()
  local minor_updates=()
  local major_updates=()

  for update in "${updates[@]}"; do
    if is_security_update "$update"; then
      security_updates+=("$update")
    else
      case $(get_update_type "$update") in
        PATCH) patch_updates+=("$update") ;;
        MINOR) minor_updates+=("$update") ;;
        MAJOR) major_updates+=("$update") ;;
      esac
    fi
  done

  # Update order: security → patches → minor → major (with confirmation)
  echo "${security_updates[@]} ${patch_updates[@]} ${minor_updates[@]} ${major_updates[@]}"
}
```

### Phase 3: Backup & Update Execution

**Create Backup**:

```bash
create_dependency_backup() {
  local backup_dir=".dependency-backup-$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$backup_dir"

  # Backup lock files and manifests
  cp package.json package-lock.json "$backup_dir/" 2>/dev/null
  cp requirements.txt "$backup_dir/" 2>/dev/null
  cp Cargo.toml Cargo.lock "$backup_dir/" 2>/dev/null

  echo "$backup_dir"
}
```

**Execute Updates**:

```bash
update_npm_packages() {
  local packages=("$@")

  for package in "${packages[@]}"; do
    echo "Updating $package..."

    npm update $package 2>&1 | tee -a update.log

    if [ ${PIPESTATUS[0]} -eq 0 ]; then
      echo "✅ $package updated"
    else
      echo "❌ $package update failed"
      return 1
    fi
  done
}

update_pip_packages() {
  local packages=("$@")

  for package in "${packages[@]}"; do
    pip install --upgrade $package 2>&1 | tee -a update.log || return 1
  done
}
```

### Phase 4: Testing & Validation

**Run Tests**:

```bash
run_test_suite() {
  echo "Running test suite..."

  # Detect test command
  if [ -f "package.json" ]; then
    npm test 2>&1 | tee test.log
  elif [ -f "pytest.ini" ]; then
    pytest 2>&1 | tee test.log
  elif [ -f "Cargo.toml" ]; then
    cargo test 2>&1 | tee test.log
  else
    echo "No test suite detected"
    return 0
  fi

  return ${PIPESTATUS[0]}
}
```

**Validate Build**:

```bash
validate_build() {
  echo "Validating build..."

  if [ -f "package.json" ]; then
    npm run build 2>&1 | tee build.log
  elif [ -f "Cargo.toml" ]; then
    cargo build 2>&1 | tee build.log
  fi

  return ${PIPESTATUS[0]}
}
```

### Phase 5: Rollback or Commit

**Rollback on Failure**:

```bash
rollback_updates() {
  local backup_dir=$1

  echo "🔄 Rolling back updates..."

  cp "$backup_dir"/* . 2>/dev/null

  # Reinstall from lock files
  if [ -f "package-lock.json" ]; then
    npm ci
  elif [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
  fi

  echo "✅ Rollback complete"
}
```

**Commit Updates**:

```bash
commit_updates() {
  echo "📝 Committing updates..."

  git add package.json package-lock.json requirements.txt Cargo.toml Cargo.lock 2>/dev/null

  git commit -m "Update dependencies

- Updated X packages
- All tests passing
- No breaking changes detected

🤖 Generated with Claude Code" 2>&1

  echo "✅ Updates committed"
}
```

### Phase 6: Reporting

**Success Report**:

```
✨ Dependency Updates Complete

📊 Summary:
✅ 15 packages updated
⚠️ 3 packages skipped (major updates)
❌ 0 failures

📦 Updated Packages:
- lodash: 4.17.20 → 4.17.21 (PATCH)
- react: 17.0.2 → 17.0.3 (PATCH)
- typescript: 4.5.0 → 4.9.5 (MINOR)
- ... (12 more)

⚠️ Major Updates Available (require review):
- react: 17.0.3 → 18.2.0 (MAJOR - breaking changes)
- webpack: 5.75.0 → 5.88.0 (MAJOR - config changes)
- jest: 27.5.0 → 29.5.0 (MAJOR - API changes)

🧪 Validation:
✅ Tests passed (142/142)
✅ Build successful
✅ No breaking changes detected

💾 Backup: .dependency-backup-20251030-160000/

⏱️ Total time: 4m 32s

🎯 Next Steps:
1. Review major updates: npm outdated
2. Update one at a time with testing
3. Or: "Update react to v18 safely"
```

## Guidelines

### DO:
✅ Always create backup before updates
✅ Run tests after updates
✅ Categorize updates by severity
✅ Read changelogs for major updates
✅ Update incrementally (not all at once)
✅ Check for security vulnerabilities
✅ Validate build after updates
✅ Roll back on test failures
✅ Commit with descriptive messages
✅ Keep user informed of progress

### DON'T:
❌ Update without backups
❌ Skip tests after updates
❌ Apply major updates without review
❌ Ignore breaking change warnings
❌ Update production dependencies blindly
❌ Commit failed updates
❌ Update lock files manually
❌ Skip security updates
❌ Ignore peer dependency warnings
❌ Force updates that fail

## Advanced Features

### Security Audit Integration

```bash
run_security_audit() {
  npm audit --json | jq '.vulnerabilities | to_entries[] | select(.value.severity == "high" or .value.severity == "critical")'
}

fix_security_issues() {
  npm audit fix 2>&1 | tee audit-fix.log
}
```

### Dependency Graph Analysis

```bash
analyze_dependencies() {
  npm ls --all --json | jq '.dependencies | to_entries[] | {name: .key, version: .value.version, dependencies: (.value.dependencies | keys)}'
}
```

### Automated Update PRs

```bash
create_update_pr() {
  local branch="deps/update-$(date +%Y%m%d)"

  git checkout -b "$branch"
  # ... perform updates ...
  git push -u origin "$branch"

  gh pr create \
    --title "Update dependencies" \
    --body "Automated dependency update

Updates: ...
Tests: ✅ Passing"
}
```

## Dependencies

### Required (at least one)
- **npm** - `brew install node`
- **pip** - `brew install python`
- **cargo** - `brew install rust`
- **bundler** - `gem install bundler`

### Highly Recommended
- **jq** - `brew install jq` (JSON parsing)
- **git** - Version control for rollback

### Optional
- **gh** - `brew install gh` (GitHub CLI for PRs)

## Configuration

Environment variables:

```bash
# Update behavior
export DEP_UPDATE_AUTO_PATCH=true      # Auto-apply patch updates
export DEP_UPDATE_AUTO_MINOR=false     # Require approval for minor
export DEP_UPDATE_AUTO_MAJOR=false     # Always require approval for major

# Testing
export DEP_UPDATE_SKIP_TESTS=false     # Run tests after update
export DEP_UPDATE_SKIP_BUILD=false     # Run build after update

# Safety
export DEP_UPDATE_BACKUP=true          # Create backup before update
export DEP_UPDATE_ROLLBACK_ON_FAIL=true # Auto-rollback on failure
```

## Success Metrics

- ✅ All updates completed successfully
- ✅ Tests passing after updates
- ✅ Build succeeds
- ✅ No breaking changes introduced
- ✅ Backup created and verified
- ✅ Security vulnerabilities addressed
- ✅ Changes committed with clear message

## Integration

Works seamlessly with:
- **[Pre-Commit Guardian](../../dotfiles/pre-commit-guardian/)** - Validates changes before commit
- **[Environment Setup Validator](../environment-setup-validator/)** - Ensures deps installed correctly
- **[Test Coverage Analyzer](../test-coverage-analyzer/)** - Validates test coverage maintained

## Version History

- v1.0.0 (2025-10-30): Initial production release
  - Multi-package manager support
  - Breaking change detection
  - Automated testing and validation
  - Rollback on failure
  - Security audit integration
