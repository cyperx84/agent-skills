# Extended Reference

<!-- Moved from SKILL.md to keep it under 500 lines -->

## Examples

### Example 1: Complete Theme Switch

**User**: "Switch to gruvbox dark theme"

**Skill Actions**:
```
1. Detect theme: gruvbox-dark
2. Check availability:
   ✅ Starship: gruvbox-dark.toml found
   ✅ Ghostty: gruvbox-dark.conf found
   ✅ Neovim: gruvbox installed
   ✅ SketchyBar: gruvbox colors found
   ✅ Tmux: gruvbox.conf found

3. Create backup: ~/.dotfiles-theme-backup-20251030-143022/

4. Apply theme:
   ✅ Updated Starship config
   ✅ Updated Ghostty config
   ✅ Updated Neovim colorscheme
   ✅ Updated SketchyBar colors, reloaded
   ✅ Updated Tmux config, reloaded

5. Verify: All components confirmed ✅

6. Result: ✨ Gruvbox Dark theme applied successfully!

Next steps: exec zsh to reload shell
```

### Example 2: Partial Success (Missing Component)

**User**: "Apply catppuccin mocha theme"

**Skill Actions**:
```
1. Detect theme: catppuccin-mocha
2. Check availability:
   ✅ Starship: found
   ✅ Ghostty: found
   ❌ Neovim: catppuccin not installed
   ✅ SketchyBar: found
   ✅ Tmux: found

3. User prompt: "Neovim theme missing. Continue with other components? [y/n]"
   User: y

4. Create backup

5. Apply theme (skip Neovim):
   ✅ Starship updated
   ✅ Ghostty updated
   ⏭️ Neovim skipped
   ✅ SketchyBar updated
   ✅ Tmux updated

6. Result: ⚠️ Partial success - 4/5 components updated

💡 Suggestion: Install catppuccin for Neovim
   Command: :Lazy install catppuccin
   Then rerun theme switch
```

### Example 3: Rollback Due to Failure

**User**: "Switch to nord theme"

**Skill Actions**:
```
1. Detect theme: nord
2. Check availability: All found ✅
3. Create backup: $BACKUP_DIR
4. Apply theme:
   ✅ Starship updated
   ✅ Ghostty updated
   ❌ Neovim failed (syntax error in theme file)

5. Validation error detected!

6. Automatic rollback initiated:
   ✅ Restored Starship config
   ✅ Restored Ghostty config
   ✅ Restored Neovim config
   ✅ Reloaded SketchyBar

7. Result: ❌ Theme switch failed, rolled back to previous theme

Error: Neovim colorscheme contains syntax error
💡 Fix: Update Neovim theme plugin, then retry

Backup preserved: $BACKUP_DIR
```

### Example 4: Preview Mode

**User**: "Preview available themes"

**Skill Actions**:
```
1. Scan all theme directories
2. Generate theme matrix:

📊 Available Themes:

Theme Name        Starship  Ghostty  Neovim  SketchyBar  Tmux  Complete?
─────────────────────────────────────────────────────────────────────────
gruvbox-dark         ✅       ✅       ✅        ✅        ✅      ✅
catppuccin-mocha     ✅       ✅       ✅        ✅        ✅      ✅
nord                 ✅       ✅       ✅        ❌        ✅      ⚠️
tokyonight-night     ✅       ✅       ✅        ✅        ✅      ✅
dracula              ✅       ❌       ✅        ✅        ✅      ⚠️

Current theme: gruvbox-dark

💡 Complete themes (✅) can be switched to immediately
💡 Partial themes (⚠️) will skip missing components

Which theme would you like to switch to?
```

## Guidelines

### DO:
✅ Always create backup before theme switch
✅ Validate theme files exist before applying
✅ Test each component after theme change
✅ Provide rollback on any failure
✅ Give clear status for each component
✅ Reload services automatically when safe
✅ Preserve backups until user confirms success
✅ Show visual verification prompts
✅ Support partial theme switches (some components only)
✅ Document current and previous themes
✅ Track theme history for easy reversion

### DON'T:
❌ Apply themes without backup
❌ Skip validation steps
❌ Leave user with broken config on failure
❌ Modify configs without confirming syntax
❌ Force full theme switch when components missing
❌ Delete backups immediately after switch
❌ Assume visual appearance is correct without verification
❌ Apply incompatible theme combinations
❌ Restart critical services without user confirmation
❌ Override user customizations within themes

## Advanced Features

### Theme Preview

Generate visual preview before switching:

```bash
# Create temporary preview environment
PREVIEW_DIR=$(mktemp -d)

# Extract color palette from theme
extract_colors "$THEME_NAME" > "$PREVIEW_DIR/palette.txt"

# Show color swatches in terminal
show_color_preview "$PREVIEW_DIR/palette.txt"

# Offer temporary switch (revert after 30 seconds)
preview_theme_temporarily "$THEME_NAME" 30
```

### Theme Sync Across Machines

Export theme config for syncing:

```bash
# Export current theme setup
export_theme_config() {
  cat > ~/.dotfiles-theme-current.json << EOF
{
  "theme": "$CURRENT_THEME",
  "components": {
    "starship": "$STARSHIP_THEME",
    "ghostty": "$GHOSTTY_THEME",
    "nvim": "$NVIM_THEME",
    "sketchybar": "$SKETCHYBAR_THEME",
    "tmux": "$TMUX_THEME"
  },
  "timestamp": "$(date -Iseconds)"
}
EOF
}

# Import on another machine
import_theme_config "$HOME/.dotfiles-theme-current.json"
```

### Smart Theme Recommendations

Suggest themes based on time of day or ambient light:

```bash
# Auto-switch based on time
auto_theme_by_time() {
  local hour=$(date +%H)

  if [ $hour -ge 6 ] && [ $hour -lt 18 ]; then
    suggest_theme "light"
  else
    suggest_theme "dark"
  fi
}

# Integration with macOS dark mode
match_macos_appearance() {
  if defaults read -g AppleInterfaceStyle 2>/dev/null | grep -q "Dark"; then
    switch_theme "dark-variant"
  else
    switch_theme "light-variant"
  fi
}
```

### Custom Theme Builder

Create custom themes from color palettes:

```bash
# Generate theme files from hex colors
create_custom_theme() {
  local theme_name=$1
  local bg_color=$2
  local fg_color=$3
  local accent_color=$4

  # Generate Starship theme
  generate_starship_theme "$theme_name" "$bg_color" "$fg_color" "$accent_color"

  # Generate Ghostty theme
  generate_ghostty_theme "$theme_name" "$bg_color" "$fg_color" "$accent_color"

  # ... generate for other components
}
```

## Dependencies

### Required
- **GNU Stow** or config management system
  - Manages symlinks for theme files

### Highly Recommended
- **Starship** - `brew install starship`
  - Terminal prompt

- **Ghostty** - `brew install --cask ghostty`
  - Terminal emulator with theme support

- **Neovim** - `brew install neovim`
  - Editor with colorscheme support

### Optional
- **SketchyBar** - `brew install sketchybar`
  - Menu bar with theming

- **Tmux** - `brew install tmux`
  - Terminal multiplexer with theme plugins

- **jq** - `brew install jq`
  - For theme config parsing

## Configuration

### Theme Directory Structure

Organize themes for easy management:

```bash
~/.config/
├── starship/
│   ├── starship-gruvbox-dark.toml
│   ├── starship-catppuccin-mocha.toml
│   └── starship-nord.toml
├── ghostty/
│   └── themes/
│       ├── gruvbox-dark.conf
│       ├── catppuccin-mocha.conf
│       └── nord.conf
├── nvim/
│   └── lua/custom/plugins/
│       └── colorscheme.lua
├── sketchybar/
│   └── themes/
│       ├── gruvbox-dark/
│       │   └── colors.lua
│       └── catppuccin-mocha/
│           └── colors.lua
└── tmux/
    └── themes/
        ├── gruvbox.conf
        ├── catppuccin.conf
        └── nord.conf
```

### Theme Mapping Configuration

Define theme relationships:

```yaml
# ~/.dotfiles-theme-map.yml
themes:
  gruvbox-dark:
    starship: "starship-gruvbox-dark.toml"
    ghostty: "gruvbox-dark"
    nvim: "gruvbox"
    sketchybar: "gruvbox-dark"
    tmux: "gruvbox"

  catppuccin-mocha:
    starship: "starship-catppuccin-mocha.toml"
    ghostty: "catppuccin-mocha"
    nvim: "catppuccin"
    sketchybar: "catppuccin-mocha"
    tmux: "catppuccin"
```

## Troubleshooting

### "Theme not found for component"
**Solution**:
```bash
# List available themes
ls ~/.config/starship/starship-*.toml
ls ~/.config/ghostty/themes/*.conf

# Download missing theme
# (example for Neovim)
nvim -c ":Lazy install catppuccin" -c ":quit"
```

### "Theme applied but looks wrong"
**Solution**:
```bash
# Verify true color support
echo $COLORTERM  # Should show: truecolor

# Test terminal colors
curl -s https://gist.githubusercontent.com/lifepillar/09a44b8cf0f9397465614e622979107f/raw/24-bit-color.sh | bash

# Reload services
sketchybar --reload
tmux source-file ~/.tmux.conf
```

### "Rollback didn't work"
**Solution**:
```bash
# Manual rollback
BACKUP=$(ls -td ~/.dotfiles-theme-backup-* | head -1)
cp -r $BACKUP/* ~/.config/

# Restart services
brew services restart sketchybar
exec zsh
```

### "Services won't reload with new theme"
**Solution**:
```bash
# Force restart instead of reload
brew services restart yabai
brew services restart sketchybar
pkill -USR1 tmux

# Check service logs
tail -f /usr/local/var/log/sketchybar/sketchybar.out.log
```

## Success Metrics

A successful theme switch includes:
- ✅ All component configs updated
- ✅ No syntax errors in any config file
- ✅ All services reloaded successfully
- ✅ Visual consistency across all components
- ✅ Backup created and preserved
- ✅ Switch completed in < 10 seconds
- ✅ Zero manual config edits required
- ✅ Rollback available if needed

## Integration

Works seamlessly with:
- **[Service Orchestrator](../service-orchestrator/)** - Restarts services after theme change
- **[Pre-Commit Guardian](../pre-commit-guardian/)** - Validates theme configs before commit
- **[Stow Health Manager](../stow-health-manager/)** - Ensures theme symlinks are valid

## Version History

- v1.0.0 (2025-10-30): Initial production release
  - Multi-component theme switching
  - Automatic backup and rollback
  - Visual verification
  - Partial success handling
  - Theme preview and recommendations
  - Custom theme builder
