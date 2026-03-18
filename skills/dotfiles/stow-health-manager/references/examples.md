# Extended Reference

<!-- Moved from SKILL.md to keep it under 500 lines -->

## Examples

### Example 1: Routine Health Check (All Good)

**User**: "Check my stow health"

**Skill Actions**:
```
1. Scanning for dotfiles symlinks...
   Found dotfiles repo: ~/dotfiles
2. Analyzing 47 symlinks...
3. Checking for broken links... ✅ None found
4. Checking for conflicts... ✅ None found
5. Checking for drift... ✅ None found

✨ Perfect Health!
  47/47 symlinks healthy (100%)
  No issues detected

Your dotfiles are in excellent shape! 🎉
```

### Example 2: Broken Links Detected and Fixed

**User**: "Fix my symlinks"

**Skill Actions**:
```
1. Scanning... Found 12 broken symlinks ❌
2. Broken links:
   - ~/.zshrc (target deleted)
   - ~/.tmux.conf (target moved)
   - [10 more...]

3. Auto-repair? [y/n] y

4. Creating backup... ✅
   Backup: ~/.dotfiles-backup-20251030/

5. Removing broken links... ✅

6. Re-stowing components:
   - zsh... ✅
   - tmux... ✅
   - nvim... ✅
   - yabai... ✅

7. Verification:
   All 47 symlinks now healthy! ✅

✨ Repair complete in 4.2 seconds
```

### Example 3: Conflicts Resolved

**User**: "My dotfiles won't stow, there are conflicts"

**Skill Actions**:
```
1. Analyzing conflicts...
   Found 3 conflicts:

   a) ~/.gitconfig (regular file exists)
   b) ~/.config/ghostty/ (directory exists)
   c) ~/.tmux.conf (regular file, modified)

2. Resolving conflicts:

   ~/.gitconfig
   Choice: [A]dopt, [R]eplace, [S]kip? A
   ✅ Adopted existing file into repo

   ~/.config/ghostty/
   Choice: [A]dopt, [R]eplace, [S]kip? A
   ✅ Adopted directory into repo

   ~/.tmux.conf
   Choice: [A]dopt, [R]eplace, [S]kip? A
   ✅ Adopted with local changes

3. Stowing all components... ✅

✨ All conflicts resolved!
   All configs now symlinked and tracked

Next: Review changes in dotfiles repo
   cd ~/dotfiles && git status
```

## Guidelines

### DO:
✅ Always create backup before any destructive operation
✅ Provide clear, actionable options for conflict resolution
✅ Verify repairs with post-check scans
✅ Show detailed reports of what changed
✅ Offer rollback instructions
✅ Detect all types of issues (broken, conflicts, drift)
✅ Support both auto and manual repair modes
✅ Preserve user data (adopt, don't delete)

### DON'T:
❌ Delete files without backing up
❌ Auto-fix without showing what will change
❌ Overwrite modified configs without warning
❌ Skip verification after repair
❌ Leave user in broken state
❌ Assume dotfiles repo location
❌ Force changes without user confirmation for conflicts

## Advanced Features

### Preventive Mode

Run before major operations:
```
Before: "I'm about to upgrade all my dotfiles"
Action: Run health check first
Result: Ensures clean state before changes
```

### Scheduled Health Checks

Add to cron/launchd:
```bash
# Daily health check
0 9 * * * claude-code --skill stow-health-manager "check stow health" > ~/stow-health.log
```

### Integration with Pre-Commit

Works with Pre-Commit Guardian:
```
1. Pre-Commit Guardian validates configs
2. If pass, commits
3. Stow Health Manager verifies links still healthy
4. Report any drift
```

## Dependencies

- **stow**: GNU Stow for symlink management
- **find**: Finding symlinks
- **readlink**: Reading link targets
- **diff**: Comparing files for drift detection
- **git**: For dotfiles repo operations (optional)

## Configuration

No configuration needed - auto-detects dotfiles repo location.

**Optional Environment Variables**:
```bash
# Override dotfiles location
export DOTFILES_DIR=~/my-dotfiles

# Skip backup (not recommended)
export STOW_HEALTH_NO_BACKUP=1

# Auto-accept all repairs (dangerous!)
export STOW_HEALTH_AUTO_YES=1
```

## Troubleshooting

### Issue: Skill can't find dotfiles repo

**Solution**:
```bash
# Specify location
export DOTFILES_DIR=~/path/to/dotfiles

# Or when prompted:
"Where is your dotfiles repository?"
> ~/my-custom-dotfiles
```

### Issue: Too many broken links to fix

**Solution**:
```
1. Start with critical configs only
2. Use manual review mode
3. Fix incrementally
4. Consider fresh stow:
   cd ~/dotfiles && stow -D */ && stow */
```

### Issue: Conflicts won't resolve

**Solution**:
```
1. Backup the conflicting file
2. Remove it manually
3. Run stow again
4. Compare backup with new symlink target
5. Merge any needed changes
```

## Success Metrics

A successful stow health check includes:
- ✅ All symlinks scanned
- ✅ Broken links identified
- ✅ Conflicts detected
- ✅ Drift found
- ✅ Clear repair options offered
- ✅ Backup created before changes
- ✅ All repairs verified
- ✅ Final health score 90%+
- ✅ Detailed report provided
- ✅ Rollback instructions given

## Version History

- v1.0.0 (2025-10-30): Production release
  - Complete health scanning
  - Auto-repair with backup
  - Conflict resolution
  - Drift detection
  - Interactive repair mode
  - Comprehensive reporting
