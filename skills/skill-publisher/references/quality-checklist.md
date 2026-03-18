# Quality Checklist

Run this before publishing any skill.

## Required

- [ ] SKILL.md has valid YAML frontmatter (starts with `---`, has `name` and `description`)
- [ ] `name` field matches directory name exactly (lowercase, hyphens)
- [ ] Description includes WHEN triggers (not just what it does)
- [ ] SKILL.md body is under 500 lines
- [ ] No symlinks anywhere in skill directory
- [ ] Only allowed top-level items: SKILL.md, scripts/, references/, assets/, package.json
- [ ] All scripts tested and working
- [ ] `validate-skill.sh` passes with zero errors

## Recommended

- [ ] Tested in at least one real agent task (Claude Code or OpenClaw)
- [ ] Description is clear and actionable (under 1024 chars)
- [ ] `metadata.author` set to `cyperx`
- [ ] `metadata.version` set and follows semver
- [ ] `metadata.openclaw: true` if OpenClaw-compatible
- [ ] `metadata.categories` set for discoverability
- [ ] `license` field set
- [ ] No placeholder or TBD text

## Before Going Public

- [ ] CI workflow passes on main branch
- [ ] README.md updated with new skill entry
- [ ] PR generated for at least Tier 2 awesome-lists
- [ ] Social posts drafted (Reddit, X, DEV.to)
- [ ] ClawHub publish tested
