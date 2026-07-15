---
name: clwatch
description: Work with the CLWatch changelog-tracking CLI when the user asks to inspect AI coding-tool releases, compare changelog versions, or check what changed. CLWatch and changelogs.info are currently being rebuilt, so discover the installed command surface before use and do not assume legacy commands or APIs still exist.
---

# CLWatch

Treat CLWatch as an active product under reconstruction. Preserve the skill name
while the CLI and changelogs.info website are redesigned together.

## Safe workflow

1. Check whether `clwatch` is installed.
2. Run `clwatch --help` and, when relevant, the selected subcommand's `--help`.
3. Use only commands and flags shown by the installed binary.
4. Prefer structured output when the current CLI advertises it.
5. Report the installed version and the exact command used with any result.

If the binary is unavailable or the requested capability is absent, say that
CLWatch is being rebuilt. Do not install an old release, call an undocumented
changelogs.info endpoint, or reconstruct the legacy interface from memory.

For release facts that must be answered now, consult the tools' official
changelogs directly and label that result as outside CLWatch.
