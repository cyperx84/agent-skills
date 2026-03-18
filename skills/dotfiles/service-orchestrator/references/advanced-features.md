# Extended Reference

<!-- Moved from SKILL.md to keep it under 500 lines -->

## Advanced Features

### Selective Restart

Based on what changed, intelligently restart only necessary services:

**Yabai only changed**:
- Restart: yabai, sketchybar (reads yabai state)
- Skip: skhd (not affected)

**SketchyBar only changed**:
- Restart: sketchybar only
- Skip: yabai, skhd (not affected)

**SKHD only changed**:
- Restart: skhd only
- Skip: yabai, sketchybar (not affected)

### Rollback on Failure

If new config causes service failure:
```
1. Detect failure
2. Restore previous config from git/backup
3. Restart with known-good config
4. Notify user of rollback
5. Show diff of what was reverted
```

### Service Dependency Graph

Maintain awareness of full dependency tree:
```
Yabai
├─ Signals → SketchyBar
├─ Window queries → SKHD
└─ Space management → Both

SketchyBar
├─ Reads Yabai state
├─ Subscribes to Yabai events
└─ Helper binary dependency

SKHD
├─ Controls Yabai operations
└─ Triggers SketchyBar actions
```

## Troubleshooting

### Common Issues

**Issue**: Service won't start after restart
**Solution**:
```
1. Check logs for specific error
2. Validate config syntax
3. Check if port/socket already in use
4. Verify dependencies installed
5. Try manual start: brew services start <service>
```

**Issue**: SketchyBar shows blank bar
**Solution**:
```
1. Check if Yabai started successfully
2. Verify external_bar config in yabairc
3. Check SketchyBar logs for errors
4. Rebuild helper binary if needed
5. Test plugins individually
```

**Issue**: Hotkeys not working
**Solution**:
```
1. Check SKHD is running
2. Verify skhdrc syntax
3. Check logs: tail -f /usr/local/var/log/skhd/skhd.out.log
4. Test with simple hotkey first
5. Check for key conflicts
```

## Success Metrics

A successful service restart includes:
- ✅ All configs validated before restart
- ✅ Services stopped cleanly
- ✅ Services started in correct order
- ✅ All PIDs verified
- ✅ Health checks passed
- ✅ Integration verified
- ✅ No errors in logs
- ✅ User can immediately use window management
- ✅ Completion time under 10 seconds

## Version History

- v1.0.0 (2025-10-30): Initial production release
  - Complete validation pipeline
  - Dependency-aware restart orchestration
  - Comprehensive health checking
  - Detailed error reporting
