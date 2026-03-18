# Extended Reference

<!-- Moved from SKILL.md to keep it under 500 lines -->

test_file_exists() {
  if [ -x "$PLUGIN_FILE" ]; then
    echo "✅ Plugin file exists and is executable"
    return 0
  else
    echo "❌ Plugin file missing or not executable"
    return 1
  fi
}

# Test 2: Plugin can fetch data
test_data_fetch() {
  echo "Testing data fetch..."

  # Source the plugin to access its functions
  source "$PLUGIN_FILE"

  local data=$(fetch_data 2>&1)
  local exit_code=$?

  if [ $exit_code -eq 0 ] && [ -n "$data" ]; then
    echo "✅ Data fetch successful: $data"
    return 0
  else
    echo "❌ Data fetch failed (exit code: $exit_code)"
    return 1
  fi
}

# Test 3: Plugin updates SketchyBar
test_sketchybar_update() {
  echo "Testing SketchyBar update..."

  # Trigger plugin update
  NAME="${PLUGIN_NAME}" SENDER="forced" "$PLUGIN_FILE"

  if [ $? -eq 0 ]; then
    echo "✅ SketchyBar update successful"
    return 0
  else
    echo "❌ SketchyBar update failed"
    return 1
  fi
}

# Test 4: Click handler works
test_click_handler() {
  echo "Testing click handler..."

  NAME="${PLUGIN_NAME}" SENDER="mouse.clicked" "$PLUGIN_FILE"

  if [ $? -eq 0 ]; then
    echo "✅ Click handler successful"
    return 0
  else
    echo "❌ Click handler failed"
    return 1
  fi
}

# Run all tests
TESTS_PASSED=0
TESTS_FAILED=0

run_test() {
  if $1; then
    ((TESTS_PASSED++))
  else
    ((TESTS_FAILED++))
  fi
}

run_test test_file_exists
run_test test_data_fetch
run_test test_sketchybar_update
run_test test_click_handler

# Summary
echo ""
echo "📊 Test Summary:"
echo "✅ Passed: $TESTS_PASSED"
echo "❌ Failed: $TESTS_FAILED"

if [ $TESTS_FAILED -eq 0 ]; then
  echo "🎉 All tests passed!"
  exit 0
else
  echo "⚠️ Some tests failed - review output above"
  exit 1
fi
EOF

chmod +x "$TEST_SCRIPT"

echo "✅ Test script created: $TEST_SCRIPT"
```

**Debug Mode**:

```bash
# Add debug mode to plugin
DEBUG_MODE="${DEBUG_MODE:-false}"

debug_log() {
  if [ "$DEBUG_MODE" = "true" ]; then
    echo "[DEBUG] $1" >> "$HOME/.config/sketchybar/logs/${PLUGIN_NAME}-debug.log"
  fi
}

# Run with debug mode
DEBUG_MODE=true SENDER="forced" NAME="${PLUGIN_NAME}" $PLUGIN_FILE
```

**Interactive Testing**:

```bash
# Create interactive test REPL
test_plugin_interactive() {
  echo "🔧 Interactive Plugin Tester"
  echo "Commands: update, click, event <name>, debug, quit"

  while true; do
    read -p "> " command args

    case "$command" in
      update)
        echo "Triggering update..."
        NAME="${PLUGIN_NAME}" SENDER="forced" "$PLUGIN_FILE"
        ;;
      click)
        echo "Simulating click..."
        NAME="${PLUGIN_NAME}" SENDER="mouse.clicked" "$PLUGIN_FILE"
        ;;
      event)
        echo "Triggering event: $args"
        sketchybar --trigger "$args"
        ;;
      debug)
        echo "Enabling debug mode..."
        DEBUG_MODE=true NAME="${PLUGIN_NAME}" SENDER="forced" "$PLUGIN_FILE"
        ;;
      quit)
        break
        ;;
      *)
        echo "Unknown command: $command"
        ;;
    esac
  done
}
```

### Phase 5: Integration & Deployment

**Validate Integration**:

```bash
# Check that plugin is properly integrated
validate_integration() {
  echo "🔍 Validating plugin integration..."

  # 1. Check plugin in SketchyBar config
  if grep -q "$PLUGIN_NAME" "$SKETCHYBAR_DIR/sketchybarrc"; then
    echo "✅ Plugin found in sketchybarrc"
  else
    echo "❌ Plugin not in sketchybarrc"
    return 1
  fi

  # 2. Check SketchyBar can see the plugin
  if sketchybar --query "$PLUGIN_NAME" >/dev/null 2>&1; then
    echo "✅ SketchyBar recognizes plugin"
  else
    echo "❌ SketchyBar doesn't recognize plugin"
    return 1
  fi

  # 3. Verify plugin is updating
  local before=$(sketchybar --query "$PLUGIN_NAME" | jq -r '.label.value')
  sketchybar --trigger "${PLUGIN_NAME}.update"
  sleep 1
  local after=$(sketchybar --query "$PLUGIN_NAME" | jq -r '.label.value')

  if [ "$before" != "$after" ] || [ -n "$after" ]; then
    echo "✅ Plugin is updating"
  else
    echo "⚠️ Plugin may not be updating properly"
  fi

  return 0
}
```

**Deploy Plugin**:

```bash
# Reload SketchyBar to activate plugin
deploy_plugin() {
  echo "🚀 Deploying plugin..."

  # 1. Validate first
  if ! validate_integration; then
    echo "❌ Validation failed - fix issues before deploying"
    return 1
  fi

  # 2. Reload SketchyBar
  echo "Reloading SketchyBar..."
  sketchybar --reload

  # 3. Wait for SketchyBar to stabilize
  sleep 2

  # 4. Trigger initial update
  sketchybar --trigger "${PLUGIN_NAME}.update"

  # 5. Verify plugin is visible
  if sketchybar --query "$PLUGIN_NAME" >/dev/null 2>&1; then
    echo "✅ Plugin deployed and active!"

    # Show plugin info
    echo ""
    echo "📊 Plugin Status:"
    sketchybar --query "$PLUGIN_NAME" | jq '{
      position,
      icon: .icon.value,
      label: .label.value,
      drawing: .drawing
    }'

    return 0
  else
    echo "❌ Plugin deployment failed"
    return 1
  fi
}
```

### Phase 6: Documentation & Reporting

**Generate Plugin Documentation**:

```bash
cat > "$PLUGIN_DIR/docs/${PLUGIN_NAME}.md" << 'EOF'
# ${PLUGIN_NAME} Plugin

## Description
${PLUGIN_DESCRIPTION}

## Features
- ${FEATURE_1}
- ${FEATURE_2}
- ${FEATURE_3}

## Configuration

### Environment Variables
```bash
export ${PLUGIN_NAME_UPPER}_UPDATE_FREQ=5
export ${PLUGIN_NAME_UPPER}_ICON=""
```

### SketchyBar Config
Located in `~/.config/sketchybar/sketchybarrc`:
```bash
sketchybar --add item ${PLUGIN_NAME} right \\
           --set ${PLUGIN_NAME} \\
                 update_freq=$UPDATE_FREQ \\
                 script="$PLUGIN_FILE"
```

## Events

### Subscribed Events
- `system_woke` - Updates when system wakes
- `${PLUGIN_NAME}.update` - Manual update trigger
- `${PLUGIN_NAME}.refresh` - Force refresh

### Custom Events
Trigger manually:
```bash
sketchybar --trigger ${PLUGIN_NAME}.update
```

## Testing

Run test suite:
```bash
~/.config/sketchybar/plugins/tests/test_${PLUGIN_NAME}.sh
```

Debug mode:
```bash
DEBUG_MODE=true SENDER="forced" NAME="${PLUGIN_NAME}" ~/.config/sketchybar/plugins/${PLUGIN_NAME}.sh
```

## Troubleshooting

### Plugin Not Updating
```bash
# Check if plugin is loaded
sketchybar --query ${PLUGIN_NAME}

# Manually trigger update
sketchybar --trigger ${PLUGIN_NAME}.update

# Check logs
tail -f ~/.config/sketchybar/logs/${PLUGIN_NAME}.log
```

### Data Fetch Failing
```bash
# Test data source directly
source ~/.config/sketchybar/plugins/${PLUGIN_NAME}.sh
fetch_data
```

## Related Plugins
- Plugin A - Similar functionality
- Plugin B - Complementary feature

## Version History
- v1.0.0 - Initial release
EOF
```

**Success Report**:

```
🎉 SketchyBar Plugin Created Successfully!

📊 Plugin Details:
Name: ${PLUGIN_NAME}
Type: ${PLUGIN_TYPE}
Location: ~/.config/sketchybar/plugins/${PLUGIN_NAME}.sh

✅ Files Created:
- Plugin script: ~/.config/sketchybar/plugins/${PLUGIN_NAME}.sh
- Helper functions: ~/.config/sketchybar/plugins/helpers/${PLUGIN_NAME}_helpers.sh
- Test script: ~/.config/sketchybar/plugins/tests/test_${PLUGIN_NAME}.sh
- Documentation: ~/.config/sketchybar/plugins/docs/${PLUGIN_NAME}.md

📝 Integration:
✅ Added to sketchybarrc
✅ Event subscriptions configured
✅ SketchyBar reloaded

🧪 Next Steps:
1. Test the plugin: ~/.config/sketchybar/plugins/tests/test_${PLUGIN_NAME}.sh
2. Customize the logic in fetch_data()
3. Add click handler in handle_click()
4. Adjust update frequency as needed

📚 Documentation: ~/.config/sketchybar/plugins/docs/${PLUGIN_NAME}.md

💡 Trigger manual update: sketchybar --trigger ${PLUGIN_NAME}.update
💡 Debug mode: DEBUG_MODE=true SENDER="forced" NAME="${PLUGIN_NAME}" ...

⏱️ Total time: ${ELAPSED_TIME} seconds
```

## Examples

### Example 1: Create Simple Data Display Plugin

**User**: "Create a SketchyBar plugin to show current Spotify track"

**Skill Actions**:
```
1. Gather requirements:
   - Name: spotify
   - Type: data display
   - Update: on track change
   - Source: AppleScript (Spotify API)

2. Scaffold plugin:
   ✅ Created spotify.sh
   ✅ Added helper functions
   ✅ Created test script

3. Implement data fetch:
   - osascript to get Spotify track name
   - Timeout handling (2s)
   - Error fallback ("Not Playing")

4. Add to sketchybarrc:
   - Item position: right
   - Update freq: event-based
   - Subscribe to: spotify_change (custom event)

5. Test plugin:
   ✅ File exists and executable
   ✅ Data fetch works
   ✅ SketchyBar update works
   ✅ All tests pass

6. Deploy:
   ✅ SketchyBar reloaded
   ✅ Plugin visible and updating

Result: Working Spotify plugin in 30 seconds
```

### Example 2: Debug Existing Plugin

**User**: "My weather plugin isn't updating"

**Skill Actions**:
```
1. Analyze plugin:
   - Read weather.sh
   - Check event subscriptions
   - Review error logs

2. Identify issues:
   ❌ API key missing
   ❌ curl timeout too short (1s)
   ⚠️ No error handling

3. Fix issues:
   ✅ Added API key check with helpful error
   ✅ Increased timeout to 5s
   ✅ Added error logging
   ✅ Added cached data fallback

4. Test fixes:
   ✅ Data fetch now works
   ✅ Error handling prevents crashes
   ✅ Fallback shows cached data during API outage

5. Result:
   ✅ Plugin working reliably
   📊 Added monitoring for API failures
```

### Example 3: Create Combined Plugin (Data + Action)

**User**: "Create plugin showing Docker container count with click to open Docker Desktop"

**Skill Actions**:
```
1. Requirements:
   - Name: docker-status
   - Type: combined (data + action)
   - Update: every 10 seconds
   - Source: docker ps command
   - Action: open Docker Desktop

2. Scaffold with combined template:
   ✅ Data display function
   ✅ Click handler function
   ✅ Both integrated in single script

3. Implement features:
   Data: docker ps -q | wc -l (count containers)
   Icon: 🐳 (changes color based on count)
   Click: open -a "Docker Desktop"

4. Add intelligence:
   - Green icon: containers running
   - Gray icon: no containers
   - Red icon: Docker daemon not running

5. Test:
   ✅ Shows correct container count
   ✅ Click opens Docker Desktop
   ✅ Icon color changes appropriately

6. Deploy:
   ✅ Active in menu bar
   ✅ Updates every 10s
   ✅ Click action works

Result: Professional Docker status widget
```

## Guidelines

### DO:
✅ Start from templates for consistency
✅ Add comprehensive error handling
✅ Implement data caching to reduce load
✅ Use timeouts for all external calls
✅ Test plugins before deploying
✅ Document configuration options
✅ Provide debug logging mode
✅ Handle missing dependencies gracefully
✅ Subscribe to relevant events only
✅ Make plugins configurable via environment variables
✅ Include uninstall instructions

### DON'T:
❌ Skip error handling (will crash SketchyBar)
❌ Make blocking calls without timeout
❌ Update too frequently (causes performance issues)
❌ Hardcode configuration values
❌ Ignore exit codes from external commands
❌ Deploy without testing first
❌ Create plugins with security vulnerabilities (API keys in code)
❌ Assume external tools are installed
❌ Use excessive CPU/memory
❌ Leave debug logging on in production

## Advanced Features

### Dynamic Icon/Color Based on State

```bash
update_with_state_colors() {
  local value=$1
  local icon=""
  local icon_color=""

  if [ $value -gt 80 ]; then
    icon="🔴"
    icon_color="0xffff0000"  # Red
  elif [ $value -gt 50 ]; then
    icon="🟡"
    icon_color="0xffffff00"  # Yellow
  else
    icon="🟢"
    icon_color="0xff00ff00"  # Green
  fi

  sketchybar --set "$NAME" icon="$icon" icon.color="$icon_color"
}
```

### Popup Menus on Click

```bash
handle_click_with_menu() {
  # Create temporary popup script
  POPUP_SCRIPT="/tmp/${PLUGIN_NAME}_popup.sh"

  cat > "$POPUP_SCRIPT" << 'EOF'
#!/usr/bin/env bash
sketchybar --add item popup.title popup \\
           --set popup.title label="Options:" \\
           --add item popup.option1 popup \\
           --set popup.option1 label="Refresh" click_script="sketchybar --trigger ${PLUGIN_NAME}.refresh" \\
           --add item popup.option2 popup \\
           --set popup.option2 label="Settings" click_script="open ~/.config/sketchybar/plugins/${PLUGIN_NAME}.sh"
EOF

  chmod +x "$POPUP_SCRIPT"
  "$POPUP_SCRIPT"
}
```

### Multi-Source Data Aggregation

```bash
fetch_aggregated_data() {
  local source1=$(fetch_primary_source)
  local source2=$(fetch_secondary_source)

  # Combine data
  local combined="${source1} | ${source2}"

  echo "$combined"
}
```

## Dependencies

### Required
- **SketchyBar** - `brew install sketchybar`
  - Menu bar application

- **jq** - `brew install jq`
  - JSON parsing for plugin queries

### Highly Recommended
- **shellcheck** - `brew install shellcheck`
  - Validate plugin scripts

- **bash 4+** - `brew install bash`
  - Modern bash features

### Optional (Plugin-Specific)
Depends on what the plugin does:

```bash
# For weather plugins
brew install curl jq

# For Spotify plugins
# (Spotify app must be installed)

# For system stats plugins
brew install htop iostat

# For Docker plugins
brew install --cask docker
```

## Configuration

### Plugin Directory Structure

```
~/.config/sketchybar/
├── sketchybarrc              # Main config
├── plugins/
│   ├── plugin1.sh            # Plugin scripts
│   ├── plugin2.sh
│   ├── helpers/              # Shared helpers
│   │   ├── plugin_utils.sh
│   │   └── plugin1_helpers.sh
│   ├── tests/                # Test scripts
│   │   ├── test_plugin1.sh
│   │   └── test_plugin2.sh
│   └── docs/                 # Documentation
│       ├── plugin1.md
│       └── plugin2.md
└── logs/                     # Plugin logs
    ├── plugin1.log
    └── plugin1-debug.log
```

## Troubleshooting

### "Plugin not showing up"
```bash
# Check if SketchyBar sees it
sketchybar --query ${PLUGIN_NAME}

# Check sketchybarrc syntax
cat ~/.config/sketchybar/sketchybarrc | grep ${PLUGIN_NAME}

# Reload SketchyBar
sketchybar --reload
```

### "Plugin crashes SketchyBar"
```bash
# Check plugin errors
bash -n ~/.config/sketchybar/plugins/${PLUGIN_NAME}.sh

# Run shellcheck
shellcheck ~/.config/sketchybar/plugins/${PLUGIN_NAME}.sh

# Test in isolation
DEBUG_MODE=true SENDER="forced" NAME="${PLUGIN_NAME}" ~/.config/sketchybar/plugins/${PLUGIN_NAME}.sh
```

### "Data not updating"
```bash
# Check update frequency
sketchybar --query ${PLUGIN_NAME} | jq '.update_freq'

# Manually trigger
sketchybar --trigger ${PLUGIN_NAME}.update

# Check if data source works
source ~/.config/sketchybar/plugins/${PLUGIN_NAME}.sh
fetch_data
```

## Success Metrics

A successful plugin development includes:
- ✅ Plugin file created and executable
- ✅ Integrated into sketchybarrc
- ✅ All tests passing
- ✅ Error handling implemented
- ✅ Data fetching working
- ✅ SketchyBar recognizes plugin
- ✅ Plugin visible in menu bar
- ✅ Updates at correct frequency
- ✅ Click actions working (if applicable)
- ✅ Documentation generated

## Integration

Works seamlessly with:
- **[Service Orchestrator](../service-orchestrator/)** - Reloads SketchyBar after plugin changes
- **[Pre-Commit Guardian](../pre-commit-guardian/)** - Validates plugin scripts before commit
- **[Theme Switcher](../theme-switcher/)** - Updates plugin colors with theme changes

## Version History

- v1.0.0 (2025-10-30): Initial production release
  - Plugin scaffolding from templates
  - Event subscription setup
  - Data fetching patterns
  - Error handling and logging
  - Test suite generation
  - Integration automation
  - Documentation generation
