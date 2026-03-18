---
name: clwatch
description: Track AI coding agent changelog updates (Claude Code, Codex, Gemini CLI, OpenCode) using the clwatch CLI. Use when the user asks to check for updates to coding tools, view changelogs, see what changed between versions, or monitor AI coding tool releases. NOT for managing OpenClaw itself (use gateway tools for that).
metadata: { "openclaw": { "emoji": "👁️", "requires": { "bins": ["clwatch"] } } }
---

# clwatch — AI Coding Tool Changelog Tracker

Track updates across Claude Code, Codex, Gemini CLI, and OpenCode via changelogs.info.

**Binary:** `clwatch` (`/opt/homebrew/bin/clwatch`)
**Install:** `brew install cyperx84/tap/clwatch`

## Quick Reference

```bash
# See what's changed since last check
clwatch diff

# List all tracked tools
clwatch list

# Refresh a specific tool's changelog
clwatch refresh claude-code

# Watch for updates on an interval
clwatch watch --interval 6h

# Get status of all tools
clwatch status

# See diff between two versions
clwatch diff-tool claude-code v1.0.0 v1.1.0

# Acknowledge (mark as seen) a version
clwatch ack claude-code v1.1.0

# Init tracking in a directory
clwatch init

# JSON output for any command
clwatch diff --json
clwatch status --json
```

## How to Use

When the user asks about updates to coding tools, AI agent releases, or changelogs:

1. Run `clwatch diff` to see unacknowledged changes
2. Run `clwatch status` for a full overview
3. Use `clwatch refresh <tool>` to force-fetch latest
4. Use `clwatch diff-tool <tool> <from> <to>` for specific version diffs

## Tracked Tools

- Claude Code
- Codex (OpenAI)
- Gemini CLI
- OpenCode

Data sourced from changelogs.info API.
