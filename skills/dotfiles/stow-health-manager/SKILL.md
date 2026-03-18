---
name: stow-health-manager
description: >
  Scans for broken symlinks, identifies stow conflicts, detects config drift, and repairs dotfiles automatically. Use when user has stow issues, wants to verify dotfiles health, or suspects symlink problems. Triggers: check stow, fix symlinks, verify dotfiles, repair stow, stow health.
license: MIT
metadata:
  author: cyperx
  version: "1.0.0"
  openclaw: true
  categories: [dev, dotfiles]
---


# Stow Health Manager Skill

## Purpose

Prevents and fixes the most catastrophic dotfiles failure mode: broken symlinks. Automatically detects broken links, identifies conflicts, finds configuration drift, and safely repairs issues with backup and rollback capabilities. Essential for maintaining healthy stow-managed dotfiles.

## When to Use This Skill

Activate when the user:
- Asks to "check stow health" or "verify dotfiles"
- Says "fix symlinks" or "repair stow"
- Reports configuration issues or missing files
- Wants to validate dotfiles setup
- Before major changes (as safety check)
- After manual file operations in home directory
- Suspects config drift or stow conflicts

## Workflow

### Phase 1: Discovery & Detection

**Locate Stow-Managed Directories**:

```bash
# Find dotfiles repository
# Common locations:
DOTFILES_DIRS=(
    ~/dotfiles
    ~/.dotfiles
    ~/dev/dotfiles
    ~/.config/dotfiles
)

# Or ask user
echo "Where is your dotfiles repository?"

# Detect stow structure (directories with .config/ subdirs)
find "$DOTFILES_DIR" -maxdepth 2 -type d -name ".config" -o -name "bin"
```

**Identify Stow Targets**:

```bash
# Typically stow creates links in:
STOW_TARGETS=(
    ~/ # Home directory
    ~/.config/ # Config directory
    ~/.local/bin/ # Local binaries
)

# Detect by finding existing stow symlinks
find ~ -maxdepth 2 -type l -exec readlink {} \; | grep -o "dotfiles/[^/]*" | sort -u
```

### Phase 2: Health Analysis

**Scan for Broken Symlinks**:

```bash
# Find all symlinks pointing to dotfiles
find ~ -type l -lname "*dotfiles*" 2>/dev/null | while read link; do
    target=$(readlink "$link")

    # Check if target exists
    if [ ! -e "$target" ]; then
        echo "BROKEN: $link -> $target"
    fi
done

# Detailed broken link analysis
broken_links=()
for link in $(find ~ -type l -lname "*dotfiles*" 2>/dev/null); do
    if [ ! -e "$link" ]; then
        target=$(readlink "$link")
        broken_links+=("$link|$target")
    fi
done
```

**Identify Stow Conflicts**:

```bash
# Conflicts = files/dirs that would be created by stow but already exist

# Get list of what stow WOULD create
cd "$DOTFILES_DIR"
stow -n -v component-name 2>&1 | grep "existing target is neither"

# For each component, check for conflicts
for component in */; do
    component_name=${component%/}

    # Simulate stow to find conflicts
    conflicts=$(stow -n "$component_name" 2>&1 | grep -E "existing|conflict")

    if [ -n "$conflicts" ]; then
        echo "CONFLICT in $component_name: $conflicts"
    fi
done
```

**Detect Configuration Drift**:

```bash
# Drift = symlinked files that were modified/replaced with regular files

# This shouldn't happen, but users sometimes:
# 1. Delete symlink
# 2. Create regular file in same location
# 3. Edit it, forgetting it's no longer tracked

# Detect files that SHOULD be symlinks but aren't
expected_links=(
    ~/.zshrc
    ~/.tmux.conf
    ~/.config/yabai/yabairc
    ~/.config/skhd/skhdrc
    # ... detect from dotfiles repo
)

for file in "${expected_links[@]}"; do
    if [ -f "$file" ] && [ ! -L "$file" ]; then
        echo "DRIFT: $file is regular file, should be symlink"

        # Check if content differs from repo
        repo_file="$DOTFILES_DIR/component/.../$(basename $file)"
        if ! diff -q "$file" "$repo_file" >/dev/null 2>&1; then
            echo "  AND HAS UNCOMMITTED CHANGES!"
        fi
    fi
done
```

**Find Orphaned Symlinks**:

```bash
# Orphaned = symlinks to dotfiles repo for components no longer stowed

# Get currently stowed components (have active symlinks)
active_components=$(find ~ -type l -lname "*dotfiles*" | \
    grep -o "dotfiles/[^/]*" | sort -u)

# Get all components in repo
repo_components=$(ls -d "$DOTFILES_DIR"/*/ | xargs -n1 basename)

# Find components in repo but not linked
for comp in $repo_components; do
    if ! echo "$active_components" | grep -q "$comp"; then
        echo "UNSTOWED: $comp (exists in repo but not linked)"
    fi
done
```

### Phase 3: Health Report Generation

**Categorize Issues**:

```
CRITICAL (Immediate Action Required):
❌ Broken symlinks (12 found)
  - ~/.config/nvim/init.lua -> ~/dotfiles/nvim/.config/nvim/init.lua (target missing)
  - ~/.zshrc -> ~/dotfiles/zsh/.zshrc (target missing)

HIGH PRIORITY (Should Fix Soon):
⚠️ Stow conflicts (3 found)
  - ~/.gitconfig exists, blocking git component
  - ~/.config/ghostty/ directory exists, blocking ghostty component

MEDIUM PRIORITY (Review and Decide):
📝 Configuration drift (2 found)
  - ~/.tmux.conf is regular file (should be symlink)
    Content differs from repo - has uncommitted changes!

INFORMATIONAL:
ℹ️ Unstowed components (1 found)
  - karabiner (in repo but not stowed)

SUMMARY:
  Total symlinks: 47
  Healthy links: 35 ✅
  Broken links: 12 ❌
  Conflicts: 3 ⚠️
  Drift detected: 2 📝
  Overall health: 74% (needs attention)
```

### Phase 4: Interactive Repair

**Offer Repair Options**:

```
Found 12 broken symlinks. How to proceed?

1. [AUTO REPAIR] Automatically fix (recommended)
   - Backs up current state
   - Removes broken links
   - Re-stows affected components
   - Verifies all links healthy

2. [MANUAL REVIEW] Show each issue, let me decide
   - Review each broken link
   - Choose action per issue
   - More control, takes longer

3. [REPORT ONLY] Just show me the issues
   - No changes made
   - I'll fix manually

Choice:
```

**Auto-Repair Workflow**:

```bash
# 1. Create backup
backup_dir="$HOME/.dotfiles-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"

echo "Creating backup at $backup_dir..."

# Backup broken links and their targets
for link in "${broken_links[@]}"; do
    link_path=${link%|*}
    target=${link#*|}

    # Save link info
    echo "$link_path -> $target" >> "$backup_dir/broken-links.txt"

    # If file exists, backup it
    if [ -e "$link_path" ]; then
        cp -a "$link_path" "$backup_dir/"
    fi
done

# 2. Remove broken links
echo "Removing broken symlinks..."
for link in "${broken_links[@]}"; do
    link_path=${link%|*}
    rm "$link_path"
    echo "  Removed: $link_path"
done

# 3. Identify affected components
affected_components=()
for link in "${broken_links[@]}"; do
    target=${link#*|}
    # Extract component name from path
    component=$(echo "$target" | grep -o "dotfiles/[^/]*" | cut -d/ -f2)
    affected_components+=("$component")
done

# Remove duplicates
affected_components=($(echo "${affected_components[@]}" | tr ' ' '\n' | sort -u))

# 4. Re-stow affected components
echo "Re-stowing components: ${affected_components[@]}"
cd "$DOTFILES_DIR"

for component in "${affected_components[@]}"; do
    echo "  Restowing $component..."
    stow -R "$component"

    if [ $? -eq 0 ]; then
        echo "    ✅ Success"
    else
        echo "    ❌ Failed"
        echo "    Rolling back..."
        # Restore from backup
        stow -D "$component"
        # Show error
        stow -R "$component" 2>&1
    fi
done

# 5. Verify repair
echo "Verifying repair..."
remaining_broken=$(find ~ -type l -lname "*dotfiles*" ! -e 2>/dev/null | wc -l)

if [ "$remaining_broken" -eq 0 ]; then
    echo "✅ All symlinks repaired successfully!"
else
    echo "⚠️ Still have $remaining_broken broken links"
    echo "   Manual intervention may be needed"
fi
```

**Conflict Resolution**:

```bash
# For each conflict, offer options:

Conflict: ~/.gitconfig already exists (regular file)
  Blocking: git component from being stowed

Options:
1. [ADOPT] Move existing file into dotfiles repo
   - Moves ~/.gitconfig to ~/dotfiles/git/.gitconfig
   - Stows git component (creates symlink)
   - Preserves your config, now tracked

2. [BACKUP & REPLACE] Backup existing, use dotfiles version
   - Backs up ~/.gitconfig to $backup_dir
   - Stows git component (replaces with symlink)
   - Old config saved for reference

3. [SKIP] Leave as-is
   - Keep regular file
   - Don't stow git component
   - No changes

Choice:
```

**Drift Resolution**:

```bash
# Configuration drift handling

Drift detected: ~/.tmux.conf
  Current: Regular file with local modifications
  Expected: Symlink to ~/dotfiles/tmux/.tmux.conf
  Diff: 47 lines changed

Options:
1. [COMMIT CHANGES] Save changes to dotfiles repo
   - Copy current file to dotfiles repo
   - Commit changes
   - Convert to symlink
   - Preserves all modifications

2. [DISCARD CHANGES] Revert to dotfiles version
   - Backs up current file
   - Removes regular file
   - Re-stows tmux component
   - Uses repo version

3. [SHOW DIFF] See what changed
   - Display detailed diff
   - Then choose option

4. [SKIP] Leave as-is
   - Keep regular file
   - Manual resolution needed

Choice:
```

### Phase 5: Verification

**Post-Repair Checks**:

```bash
# 1. Count symlinks
total_links=$(find ~ -type l -lname "*dotfiles*" 2>/dev/null | wc -l)
broken_links=$(find ~ -type l -lname "*dotfiles*" ! -e 2>/dev/null | wc -l)
healthy_links=$((total_links - broken_links))

# 2. Verify critical configs
critical_configs=(
    ~/.zshrc
    ~/.tmux.conf
    ~/.config/nvim/init.lua
    ~/.config/yabai/yabairc
    ~/.config/skhd/skhdrc
)

all_healthy=true
for config in "${critical_configs[@]}"; do
    if [ -L "$config" ] && [ -e "$config" ]; then
        echo "✅ $config"
    else
        echo "❌ $config (PROBLEM)"
        all_healthy=false
    fi
done

# 3. Test stow status
cd "$DOTFILES_DIR"
for component in */; do
    component_name=${component%/}

    # Dry-run stow to check for issues
    if stow -n "$component_name" 2>&1 | grep -q "conflict"; then
        echo "⚠️ $component_name still has conflicts"
    else
        echo "✅ $component_name"
    fi
done

# 4. Final health score
health_percentage=$((healthy_links * 100 / total_links))
echo "Overall Health: $health_percentage%"

if [ "$health_percentage" -eq 100 ]; then
    echo "🎉 Perfect health!"
elif [ "$health_percentage" -ge 90 ]; then
    echo "✅ Good health"
elif [ "$health_percentage" -ge 75 ]; then
    echo "⚠️ Needs attention"
else
    echo "❌ Poor health - manual review recommended"
fi
```

### Phase 6: Reporting

**Success Report**:
```
✨ Stow Health Manager Complete

📊 Initial State:
  Total symlinks: 47
  Broken: 12 ❌
  Conflicts: 3 ⚠️
  Drift: 2 📝
  Health: 74%

🔧 Actions Taken:
  ✅ Removed 12 broken symlinks
  ✅ Re-stowed 4 affected components (zsh, tmux, nvim, yabai)
  ✅ Resolved 3 conflicts (adopted existing configs)
  ✅ Fixed 2 drift issues (committed local changes)

📊 Final State:
  Total symlinks: 47
  Broken: 0 ✅
  Conflicts: 0 ✅
  Drift: 0 ✅
  Health: 100% 🎉

💾 Backup Location:
  ~/.dotfiles-backup-20251030-143022/
  (Restore if needed: stow -D component && restore from backup)

⏱️ Total time: 4.7 seconds

Next steps:
  - Test critical configs (open terminal, tmux, neovim)
  - Verify window management works
  - Consider running: git status (in dotfiles repo)
```

**Partial Success Report**:
```
⚠️ Stow Health Manager - Partial Success

📊 Summary:
  ✅ Fixed 10/12 broken symlinks
  ❌ 2 symlinks still broken (manual intervention needed)

🔍 Remaining Issues:

1. ~/.config/nvim/lua/custom/deleted.lua
   Problem: Target file doesn't exist in repo
   Likely: File was deleted from repo but link remains
   Fix: rm ~/.config/nvim/lua/custom/deleted.lua

2. ~/.local/bin/old-script
   Problem: Points to ~/old-dotfiles (moved repo?)
   Fix: Update link or remove

💡 To fix manually:
   rm ~/.config/nvim/lua/custom/deleted.lua
   rm ~/.local/bin/old-script

Then run: "check stow health" to verify
```


---

*Extended details: [references/examples.md](references/examples.md)*
