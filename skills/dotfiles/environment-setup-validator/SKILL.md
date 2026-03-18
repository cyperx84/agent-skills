---
name: environment-setup-validator
description: >
  Validates development environment setup by checking tool installations, versions, configurations, environment variables, and permissions. Generates detailed reports and provides fix suggestions. Use when setting up new machines or troubleshooting environment issues. Triggers: validate environment, check setup, verify dev environment, environment health check
license: MIT
metadata:
  author: cyperx
  version: "1.0.0"
  openclaw: true
  categories: [dev, dotfiles]
---


# Environment Setup Validator Skill

## Purpose

The Environment Setup Validator ensures development environments are correctly configured. Setting up a dev environment involves installing dozens of tools, setting environment variables, configuring paths, and ensuring permissions - any mistake can cause hours of debugging. This skill validates everything in minutes, identifies missing or misconfigured components, and provides exact fix commands.

## When to Use This Skill

Activate when the user:
- Sets up a new development machine
- Onboards new team members
- Troubleshoots "works on my machine" issues
- Validates after system updates
- Creates environment documentation
- Mentions keywords like: "check environment", "validate setup", "verify tools installed", "environment health"

## Workflow

### Phase 1: Requirement Detection

**Detect Project Requirements**:

```bash
# Scan project for required tools
detect_requirements() {
  local requirements=()

  # Language runtimes
  [ -f "package.json" ] && requirements+=("node")
  [ -f "requirements.txt" ] && requirements+=("python")
  [ -f "Cargo.toml" ] && requirements+=("rust")
  [ -f "Gemfile" ] && requirements+=("ruby")
  [ -f "go.mod" ] && requirements+=("go")

  # Build tools
  [ -f "Makefile" ] && requirements+=("make")
  [ -f "CMakeLists.txt" ] && requirements+=("cmake")

  # Databases
  grep -q "postgresql" . -r 2>/dev/null && requirements+=("postgresql")
  grep -q "mysql" . -r 2>/dev/null && requirements+=("mysql")
  grep -q "redis" . -r 2>/dev/null && requirements+=("redis")

  # Container tools
  [ -f "Dockerfile" ] && requirements+=("docker")
  [ -f "docker-compose.yml" ] && requirements+=("docker-compose")

  echo "${requirements[@]}"
}
```

### Phase 2: Tool Validation

**Check Tool Installation**:

```bash
check_tool_installed() {
  local tool=$1
  local required_version=$2

  if command -v $tool &>/dev/null; then
    local installed_version=$($tool --version 2>&1 | head -1)
    echo "✅ $tool: $installed_version"

    if [ -n "$required_version" ]; then
      compare_versions "$installed_version" "$required_version"
    fi
  else
    echo "❌ $tool: NOT INSTALLED"
    suggest_install "$tool"
  fi
}
```

**Version Validation**:

```bash
validate_versions() {
  # Node.js
  if [ -f ".nvmrc" ]; then
    local required=$(cat .nvmrc)
    local installed=$(node --version | tr -d 'v')
    compare_semver "$installed" "$required" "node"
  fi

  # Python
  if [ -f ".python-version" ]; then
    local required=$(cat .python-version)
    local installed=$(python --version | cut -d' ' -f2)
    compare_semver "$installed" "$required" "python"
  fi
}
```

### Phase 3: Configuration Validation

**Environment Variables**:

```bash
check_env_vars() {
  local required_vars=(
    "PATH"
    "HOME"
    "SHELL"
  )

  # Project-specific vars from .env.example
  if [ -f ".env.example" ]; then
    while IFS='=' read -r key value; do
      [ -z "${!key}" ] && echo "⚠️ Missing: $key"
    done < .env.example
  fi
}
```

**PATH Validation**:

```bash
validate_path() {
  local required_paths=(
    "/usr/local/bin"
    "$HOME/.local/bin"
  )

  for path in "${required_paths[@]}"; do
    if [[ ":$PATH:" != *":$path:"* ]]; then
      echo "⚠️ Missing from PATH: $path"
    fi
  done
}
```

### Phase 4: Permission & Access Checks

**File Permissions**:

```bash
check_permissions() {
  # Check script executability
  find . -name "*.sh" -type f ! -perm -u+x -print | while read script; do
    echo "⚠️ Not executable: $script"
    echo "   Fix: chmod +x $script"
  done
}
```

**Network Access**:

```bash
check_network_access() {
  local endpoints=(
    "https://registry.npmjs.org"
    "https://pypi.org"
    "https://github.com"
  )

  for endpoint in "${endpoints[@]}"; do
    if curl -sf --max-time 3 "$endpoint" >/dev/null; then
      echo "✅ Accessible: $endpoint"
    else
      echo "❌ Cannot reach: $endpoint"
    fi
  done
}
```

### Phase 5: Integration Testing

**Quick Smoke Tests**:

```bash
run_smoke_tests() {
  # Test Node.js
  if command -v node &>/dev/null; then
    node -e "console.log('Node OK')" && echo "✅ Node.js working"
  fi

  # Test Python
  if command -v python &>/dev/null; then
    python -c "print('Python OK')" && echo "✅ Python working"
  fi

  # Test package managers
  npm --version &>/dev/null && echo "✅ npm working"
  pip --version &>/dev/null && echo "✅ pip working"
}
```

### Phase 6: Reporting

**Validation Report**:

```
🔍 Environment Validation Report

📊 Summary:
✅ 15 checks passed
⚠️ 3 warnings
❌ 2 failures

🛠️ Tools:
✅ node: v18.16.0
✅ python: 3.11.0
✅ git: 2.40.0
❌ docker: NOT INSTALLED
⚠️ rust: 1.68.0 (recommended: 1.70.0+)

📦 Package Managers:
✅ npm: 9.5.1
✅ pip: 23.1.2
✅ brew: 4.0.15

🔐 Permissions:
✅ All scripts executable
✅ ~/.ssh permissions correct

🌐 Network:
✅ npm registry accessible
✅ PyPI accessible
❌ Docker Hub unreachable

💡 Required Actions:
1. Install Docker: brew install --cask docker
2. Update Rust: rustup update
3. Check network/firewall for Docker Hub access

⏱️ Validation time: 12 seconds
```

## Examples

### Example 1: New Machine Setup

**User**: "Validate my dev environment"

**Skill Actions**:
```
1. Detect requirements from project files
2. Check 20 tools/versions
3. Validate env vars
4. Test network access
5. Result: Missing docker, outdated rust
6. Provide install commands
```

### Example 2: Onboarding

**User**: "Check if I have everything for this project"

**Skill Actions**:
```
1. Read .tool-versions, package.json
2. Validate Node 18.16.0 installed
3. Check npm packages installable
4. Verify .env.example vars set
5. Result: All good, ready to develop
```

## Guidelines

### DO:
✅ Check both installation and versions
✅ Provide exact fix commands
✅ Test actual functionality, not just presence
✅ Validate permissions and access
✅ Generate shareable reports
✅ Support common platforms (macOS, Linux, Windows)

### DON'T:
❌ Skip version checks
❌ Provide vague error messages
❌ Assume tools are in PATH
❌ Ignore platform differences
❌ Make destructive changes without permission

## Dependencies

### Required
- **bash/zsh** - Shell for running checks

### Optional
```bash
brew install jq       # JSON parsing
brew install curl     # Network checks
```

## Success Metrics

- ✅ All required tools detected
- ✅ Versions validated
- ✅ Configuration checked
- ✅ Permissions correct
- ✅ Clear action items provided
- ✅ < 30 seconds validation time

## Version History

- v1.0.0 (2025-10-30): Initial release
  - Multi-platform support
  - Version validation
  - Configuration checks
  - Smoke testing
