---
name: soul-forge
description: Interview a user and generate SOUL.md, USER.md, AGENTS.md, TOOLS.md, IDENTITY.md, and MEMORY.md files for OpenClaw, Hermes, or other agent harnesses. Use when onboarding a person or fleet, designing a distinct agent persona, creating a SoulForge profile, or auditing generated identity and context files.
---

# SoulForge

Use the harness model as the interviewer and the deterministic `soul-forge` CLI
as the renderer. SoulForge does not select or call an LLM provider.

## Workflow

1. Confirm `soul-forge` is installed and inspect `soul-forge --help`.
2. Initialize only when `soul-forge.yaml` is absent:
   `soul-forge init --no-animation`.
3. Optionally gather existing context:
   - `soul-forge dotfiles <user/repo>` for environment signals.
   - `soul-forge voice <sample...>` for style candidates.
4. Run `soul-forge schema` and use its output as the exact profile contract.
5. Run `soul-forge questions`, then conduct a natural interview instead of
   reading the questions verbatim.
6. Write `.soul-forge/profile.json`. Omit unknowns rather than guessing.
7. Design each agent's distinct persona in the supported profile or YAML shape.
8. Run `soul-forge import .soul-forge/profile.json`.
9. Preview with `soul-forge generate --all --dry-run`.
10. After approval, run `soul-forge generate --all` and `soul-forge audit --all`.

## Interview guidance

Cover identity, goals, communication style, feedback preferences, work habits,
decision-making, hard boundaries, technical environment, and output preferences.
Ask one focused question at a time and follow useful threads. Treat dotfile and
voice analysis as candidates that the user must confirm.

## Persona quality

- Give each agent a specific voice, opinions, tensions, and boundaries.
- Prefer concrete example exchanges over adjective lists.
- Put personality and stance in `SOUL.md`.
- Put operating rules and procedures in `AGENTS.md`.
- Put human facts and preferences in `USER.md`.
- Keep accumulated experience in `MEMORY.md`.
- Avoid generic traits such as “helpful” or “professional” without observable
  behavioral examples.

Never overwrite an existing `MEMORY.md` without explicit approval. Edit source
profiles and configuration rather than hand-editing generated files.
