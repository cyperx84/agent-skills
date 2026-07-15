# CyperX Toolbox Inventory

The toolbox contains durable workflows and thin adapters to maintained tools.
Experiments stay out, even when they happen to contain a skill file.

## Keep and improve

| Project | Decision |
| --- | --- |
| `talk-once` | Core publishing workflow. Fold in the useful transcription and site-adapter ideas from VoicePipe. |
| `voice-forge` | Core voice corpus and portable style-profile provider. Expand its toolbox skill beyond TTS. |
| `soul-forge` | Keep standalone; its portable onboarding skill is now in the toolbox. |
| `ascii-animations` | Keep standalone; its portable terminal-animation skill is now in the toolbox. |
| `clwatch` + `changelogs-info` | Keep both. Rebuild the CLI, skill, and website as one coherent changelog product; use a safe toolbox stub during reconstruction. |
| `clawrus` | Keep the distributed fleet-orchestration idea, then rename and simplify it around a Chorus concept. |
| `claude-skills-mental-models` + `lattice` | Preserve the starred repository, rename it, simplify it, and reconcile Lattice into one canonical mental-model product. |

## Remove from toolbox

- `nvim-buffers`: experiment.
- `ai-compat`: abandoned experiment; repository deletion requested.
- `remotion-claw`: abandoned experiment; repository deletion requested.
- `gen-podcast`: abandoned experiment; repository deletion requested.
- `fleet-status`: abandoned experiment; repository deletion requested.
- `tts-toolkit`: experiment, but currently a VoiceForge backend dependency; remove that dependency before deletion.
- `vault-hub-neovim`: unidentified experiment; hold for a quick code audit before deletion.

## Consolidate

- Mine `voicepipe-cli` for capture, transcription, correction, and site-export behavior. Move only generally useful behavior into Talk Once, then retire VoicePipe.
- Use the starred mental-model repository as the canonical public project. Lattice should contribute its useful implementation and models rather than compete with it.
- Keep `deep-research-v2` represented by the existing toolbox skill; do not add duplicate copies.

## Audit separately

- Audit the ten `dotfiles-skills` individually. Expect to discard most of them.
- Keep private fleet copies private; compare them only when repairing a public canonical skill.
- Exclude tutorial content in `claude-code-plugin-examples` and project-local skills such as `gym-cli`.

## Execution order

1. Remove retired experiments and their distribution references.
2. Remove VoiceForge's TTS Toolkit dependency, then retire TTS Toolkit.
3. Import SoulForge and ASCII Animations.
4. Expand the VoiceForge skill and fold VoicePipe behavior into Talk Once.
5. Rename and refactor Clawrus.
6. Rename and simplify the mental-model repository while preserving its GitHub history.
7. Rebuild CLWatch and changelogs.info behind their existing public names.
8. Audit the old dotfiles skills.
