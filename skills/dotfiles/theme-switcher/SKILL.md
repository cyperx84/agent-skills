---
name: theme-switcher
description: >
  Safely switches themes across all dotfiles components (Starship, Ghostty, Neovim, SketchyBar, Tmux) with automatic validation, backup, and rollback. Coordinates theme changes to ensure visual consistency across terminal, editor, and window management. Use when user wants to change their dotfiles theme. Triggers: switch theme, change theme, apply theme, set theme to, use [theme-name] theme
license: MIT
metadata:
  author: cyperx
  version: "1.0.0"
  openclaw: true
  categories: [dev, dotfiles]
---


# Theme Switcher Skill

## Purpose

The Theme Switcher manages coordinated theme changes across your entire dotfiles setup. Changing themes manually is tedious and error-prone - you need to update 6+ config files, restart services, verify visual consistency, and handle failures. This skill automates the entire process, ensuring your terminal (Ghostty), prompt (Starship), editor (Neovim), menu bar (SketchyBar), and multiplexer (Tmux) all use matching themes without manual file editing.

## When to Use This Skill

Activate when the user:
- Wants to switch their overall dotfiles theme
- Mentions changing from one theme to another (e.g., "switch to gruvbox")
- Asks to "apply a theme" or "set theme to [name]"
- Wants to preview different themes
- Needs to sync theme across all components
- Is troubleshooting theme inconsistencies
- Mentions keywords like: "switch theme", "change colorscheme", "dark mode", "light mode", "gruvbox", "catppuccin", "nord"

## Workflow

### Phase 1: Theme Discovery & Validation

**Detect Available Themes**:

```bash
# Scan for available theme configurations
THEMES_DIR="$HOME/dotfiles"

# Starship themes
STARSHIP_THEMES=$(ls ~/.config/starship/starship-*.toml 2>/dev/null | sed 's/.*starship-//;s/.toml//')

# Ghostty themes
GHOSTTY_THEMES=$(ls ~/.config/ghostty/themes/*.conf 2>/dev/null | xargs -n1 basename | sed 's/.conf//')

# Neovim themes (check installed colorschemes)
NVIM_THEMES=$(nvim --headless -c 'echo join(getcompletion("", "color"), "\n")' -c 'quit' 2>/dev/null)

# SketchyBar themes (from plugins or config)
SKETCHYBAR_THEMES=$(grep -r "theme" ~/.config/sketchybar/ 2>/dev/null | grep -o '".*"' | tr -d '"' | sort -u)

# Tmux themes (from conf files)
TMUX_THEMES=$(ls ~/.config/tmux/themes/*.conf 2>/dev/null | xargs -n1 basename | sed 's/.conf//')
```

**What to check**:
- Which themes are installed for each component
- Whether requested theme exists for all components
- If theme files are valid (no syntax errors)
- Current active theme for each component
- Theme compatibility matrix

**Determine Theme Availability**:

Map requested theme to component support:

```bash
# Example: "catppuccin" theme
THEME_SUPPORT=(
  [starship]="catppuccin-mocha"
  [ghostty]="catppuccin-mocha"
  [nvim]="catppuccin"
  [sketchybar]="catppuccin"
  [tmux]="catppuccin"
)

# Check each component
for component in "${!THEME_SUPPORT[@]}"; do
  if ! theme_exists "$component" "${THEME_SUPPORT[$component]}"; then
    MISSING_THEMES+=("$component")
  fi
done
```

### Phase 2: Pre-Switch Backup

**Create Safety Backup**:

```bash
# Create timestamped backup directory
BACKUP_DIR="$HOME/.dotfiles-theme-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup current theme configurations
cp ~/.config/starship/starship.toml "$BACKUP_DIR/starship.toml" 2>/dev/null
cp ~/.config/ghostty/config "$BACKUP_DIR/ghostty-config" 2>/dev/null
cp ~/.config/nvim/lua/custom/plugins/colorscheme.lua "$BACKUP_DIR/nvim-colorscheme.lua" 2>/dev/null
cp ~/.config/sketchybar/colors.lua "$BACKUP_DIR/sketchybar-colors.lua" 2>/dev/null
cp ~/.tmux.conf "$BACKUP_DIR/tmux.conf" 2>/dev/null

# Record current theme state
cat > "$BACKUP_DIR/theme-state.json" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "starship": "$(basename $(readlink ~/.config/starship/starship.toml 2>/dev/null || echo 'unknown') .toml)",
  "ghostty": "$(grep -E '^theme =' ~/.config/ghostty/config 2>/dev/null | cut -d'=' -f2 | tr -d ' ')",
  "nvim": "$(grep -E 'vim.cmd.*colorscheme' ~/.config/nvim/init.lua 2>/dev/null | sed 's/.*colorscheme //;s/[\"'\'']//g')",
  "backup_location": "$BACKUP_DIR"
}
EOF
```

**Key Decisions**:
- If theme doesn't exist for all components → Offer partial switch or download missing
- If backup fails → STOP and warn user (don't risk losing config)
- If current theme unknown → Proceed with caution, extra validation
- If requested theme same as current → Ask if user wants to re-apply (useful for fixing corruption)
- Otherwise → Proceed with theme switch

### Phase 3: Theme Application

**Apply Theme to Each Component**:

Apply themes in a specific order to minimize visual disruption:

**1. Starship (Terminal Prompt)**:

```bash
# Switch Starship theme via symlink or config update
TARGET_THEME="starship-${THEME_NAME}.toml"

if [ -f "$HOME/.config/starship/$TARGET_THEME" ]; then
  # Method 1: Update STARSHIP_CONFIG in .zshrc
  sed -i '' "s|export STARSHIP_CONFIG=.*|export STARSHIP_CONFIG=~/.config/starship/$TARGET_THEME|" ~/.zshrc

  # Reload for current session
  export STARSHIP_CONFIG="$HOME/.config/starship/$TARGET_THEME"

  echo "✅ Starship theme updated: $THEME_NAME"
else
  echo "⚠️ Starship theme not found: $TARGET_THEME"
  PARTIAL_SUCCESS=true
fi
```

**2. Ghostty (Terminal Emulator)**:

```bash
# Update Ghostty theme
GHOSTTY_CONFIG="$HOME/.config/ghostty/config"

if [ -f "$HOME/.config/ghostty/themes/${THEME_NAME}.conf" ]; then
  # Update theme= line in config
  sed -i '' "s|^theme = .*|theme = ${THEME_NAME}|" "$GHOSTTY_CONFIG"

  # Ghostty auto-reloads config
  echo "✅ Ghostty theme updated: $THEME_NAME"
else
  echo "⚠️ Ghostty theme not found: ${THEME_NAME}.conf"
  PARTIAL_SUCCESS=true
fi
```

**3. Neovim (Editor)**:

```bash
# Update Neovim colorscheme
NVIM_CONFIG="$HOME/.config/nvim/lua/custom/plugins/colorscheme.lua"

if nvim --headless -c "colorscheme $THEME_NAME" -c 'quit' 2>/dev/null; then
  # Update colorscheme file
  cat > "$NVIM_CONFIG" << EOF
-- Auto-generated by Theme Switcher
return {
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "$THEME_NAME",
    },
  },
}
EOF

  echo "✅ Neovim theme updated: $THEME_NAME"
  echo "💡 Run :colorscheme $THEME_NAME in open Neovim sessions"
else
  echo "❌ Neovim theme not available: $THEME_NAME"
  THEME_FAILED=true
fi
```

**4. SketchyBar (Menu Bar)**:

```bash
# Update SketchyBar colors
SKETCHYBAR_COLORS="$HOME/.config/sketchybar/colors.lua"

if [ -f "$HOME/.config/sketchybar/themes/${THEME_NAME}/colors.lua" ]; then
  # Copy or symlink theme colors
  cp "$HOME/.config/sketchybar/themes/${THEME_NAME}/colors.lua" "$SKETCHYBAR_COLORS"

  # Reload SketchyBar
  sketchybar --reload

  echo "✅ SketchyBar theme updated: $THEME_NAME"
else
  echo "⚠️ SketchyBar theme not found: $THEME_NAME"
  echo "💡 Using default colors"
  PARTIAL_SUCCESS=true
fi
```

**5. Tmux (Terminal Multiplexer)**:

```bash
# Update Tmux theme
TMUX_CONF="$HOME/.tmux.conf"

if [ -f "$HOME/.config/tmux/themes/${THEME_NAME}.conf" ]; then
  # Update source line in .tmux.conf
  sed -i '' "s|source.*themes/.*\.conf|source ~/.config/tmux/themes/${THEME_NAME}.conf|" "$TMUX_CONF"

  # Reload tmux if running
  if tmux info &>/dev/null; then
    tmux source-file "$TMUX_CONF"
    echo "✅ Tmux theme updated and reloaded: $THEME_NAME"
  else
    echo "✅ Tmux theme updated: $THEME_NAME (will apply on next tmux start)"
  fi
else
  echo "⚠️ Tmux theme not found: ${THEME_NAME}.conf"
  PARTIAL_SUCCESS=true
fi
```

**Error Handling**:

For each component switch:
- Validate config file syntax after modification
- Test that service can reload with new theme
- If validation fails → Restore from backup immediately
- Track which components succeeded/failed
- Continue with other components even if one fails

### Phase 4: Service Reload & Verification

**Reload Services to Apply Changes**:

```bash
# Reload shell to apply Starship changes
echo "🔄 Reload shell with: exec zsh"

# Ghostty auto-reloads (no action needed)
echo "✅ Ghostty: Auto-reloaded"

# SketchyBar already reloaded in Phase 3
echo "✅ SketchyBar: Reloaded"

# Tmux already reloaded in Phase 3 (if running)
if tmux info &>/dev/null; then
  echo "✅ Tmux: Reloaded"
else
  echo "💡 Tmux: Start tmux to see new theme"
fi

# Neovim: Inform about manual reload
if pgrep -x nvim >/dev/null; then
  echo "💡 Neovim: Run :colorscheme $THEME_NAME in open sessions"
else
  echo "✅ Neovim: Will apply on next start"
fi
```

**Verify Theme Applied Correctly**:

```bash
# Check each component's current theme
verify_starship_theme() {
  local current=$(grep "STARSHIP_CONFIG" ~/.zshrc | sed 's/.*starship-//;s/.toml.*//')
  [ "$current" = "$EXPECTED_THEME" ] && echo "✅" || echo "❌"
}

verify_ghostty_theme() {
  local current=$(grep "^theme =" ~/.config/ghostty/config | cut -d'=' -f2 | tr -d ' ')
  [ "$current" = "$EXPECTED_THEME" ] && echo "✅" || echo "❌"
}

verify_nvim_theme() {
  local current=$(grep 'colorscheme = ' ~/.config/nvim/lua/custom/plugins/colorscheme.lua | sed 's/.*= "//;s/".*//')
  [ "$current" = "$EXPECTED_THEME" ] && echo "✅" || echo "❌"
}

# Run verification
STARSHIP_OK=$(verify_starship_theme)
GHOSTTY_OK=$(verify_ghostty_theme)
NVIM_OK=$(verify_nvim_theme)
```

**Visual Verification Prompt**:

```
🎨 Theme Applied - Visual Verification Needed

Please verify visually:
1. Terminal background color changed?
2. Prompt colors match new theme?
3. Syntax highlighting looks correct?
4. Menu bar colors updated?

Does everything look correct? [y/n]
```

### Phase 5: Rollback on Failure

**Detect Failures**:

```bash
if [ "$THEME_FAILED" = true ] || [ "$VISUAL_CHECK_FAILED" = true ]; then
  echo "❌ Theme switch failed - Rolling back..."

  # Restore all backed up configs
  cp "$BACKUP_DIR/starship.toml" ~/.config/starship/starship.toml
  cp "$BACKUP_DIR/ghostty-config" ~/.config/ghostty/config
  cp "$BACKUP_DIR/nvim-colorscheme.lua" ~/.config/nvim/lua/custom/plugins/colorscheme.lua
  cp "$BACKUP_DIR/sketchybar-colors.lua" ~/.config/sketchybar/colors.lua
  cp "$BACKUP_DIR/tmux.conf" ~/.tmux.conf

  # Reload services with original themes
  sketchybar --reload
  [ -n "$TMUX" ] && tmux source-file ~/.tmux.conf

  echo "✅ Rolled back to previous theme"
  echo "📁 Backup preserved at: $BACKUP_DIR"

  exit 1
fi
```

**Cleanup on Success**:

```bash
if [ "$THEME_SWITCH_SUCCESS" = true ]; then
  # Keep backup for 24 hours, then auto-delete
  echo "$BACKUP_DIR" >> ~/.dotfiles-theme-backups-to-delete

  # Or immediately delete if user confirms
  read -p "Delete backup? Theme switch successful [y/n]: " DELETE_BACKUP
  if [ "$DELETE_BACKUP" = "y" ]; then
    rm -rf "$BACKUP_DIR"
    echo "🗑️ Backup deleted"
  else
    echo "💾 Backup kept at: $BACKUP_DIR"
  fi
fi
```

### Phase 6: Reporting & Documentation

**Success Report**:

```
✨ Theme Switch Complete - $THEME_NAME Applied

📊 Components Updated:
✅ Starship (terminal prompt)
✅ Ghostty (terminal emulator)
✅ Neovim (editor)
✅ SketchyBar (menu bar)
✅ Tmux (multiplexer)

🎨 Theme Details:
Name: $THEME_NAME
Style: $THEME_STYLE (dark/light)
Color palette: $THEME_PALETTE

📝 Next Steps:
1. Reload shell: exec zsh
2. Restart Neovim sessions (or run :colorscheme $THEME_NAME)
3. Visual check complete ✅

💾 Backup: $BACKUP_DIR (preserved for rollback)

⏱️ Total time: $ELAPSED_TIME seconds

🎯 Enjoy your new theme!
```

**Partial Success Report**:

```
⚠️ Theme Switch - Partially Applied

✅ Successfully Updated:
✅ Starship
✅ Ghostty
✅ Tmux

❌ Failed or Skipped:
❌ Neovim (theme not installed)
⚠️ SketchyBar (theme not available, using default)

💡 To complete the theme switch:

For Neovim:
1. Install theme: :Lazy install $THEME_NAME
2. Run this skill again

For SketchyBar:
1. Create theme: ~/.config/sketchybar/themes/$THEME_NAME/colors.lua
2. Or download from: [theme repo URL]

💾 Backup: $BACKUP_DIR

Would you like help installing the missing themes?
```

**Failure Report**:

```
❌ Theme Switch Failed - Rolled Back

🛑 Error: $ERROR_MESSAGE

📋 What went wrong:
- Component: $FAILED_COMPONENT
- Issue: $FAILURE_REASON
- Error output: $ERROR_DETAILS

✅ Rollback successful - Previous theme restored

💡 Troubleshooting:
1. Check theme exists: ls ~/.config/$COMPONENT/themes/
2. Validate syntax: $VALIDATION_COMMAND
3. Check logs: $LOG_LOCATION

📁 Original backup preserved: $BACKUP_DIR

Try again after fixing the issue, or switch to a different theme.
```


---

*Extended details: [references/examples.md](references/examples.md)*
