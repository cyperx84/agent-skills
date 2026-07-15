# CyperX Toolbox Inventory

Inventory of reusable skills and skill-shaped projects across `cyperx84`.
Applications remain in their own repositories; this toolbox carries thin,
harness-neutral operating skills and references their stable interfaces.

## Selection rules

A toolbox skill should:

- solve a repeatable job rather than describe one project session;
- work from public, documented commands or file contracts;
- avoid personal paths, credentials, and private fleet state;
- keep provider and harness assumptions optional where possible;
- have one canonical implementation and a clear owner repository.

## Import next

| Candidate | Source | Action |
| --- | --- | --- |
| `nvim-buffers` | `cyperx84/nvim-buffers` | Fix missing `name` frontmatter and import the existing read-only skill. |
| `soul-forge` | `cyperx84/soul-forge` | Import its mature onboarding skill as a thin CLI adapter. |
| `ascii-animations` | `cyperx84/ascii-animations` | Import the existing cross-language terminal-animation skill. |
| `ai-compat` | `cyperx84/ai-compat` | Import the existing skill backed by its shared compatibility dataset. |
| `remotion` | `cyperx84/remotion-claw` | Import the canonical public skill, removing OpenClaw-only metadata where unnecessary. |
| `voice-forge` | `cyperx84/voice-forge` | Expand the current TTS-only skill to cover corpus, style profile, and portable profile export. |

## Build adapters

These are useful applications with agent-friendly interfaces but need a focused
toolbox skill.

| Candidate | Source | Proposed skill boundary |
| --- | --- | --- |
| `gen-podcast` | `cyperx84/gen-podcast` | Generate, inspect, and resume podcast jobs from reviewed source material. |
| `fleet-status` | `cyperx84/fleet-status` | Read-only OpenClaw fleet health and error inspection. |
| `clawrus` | `cyperx84/clawrus` | Run and gather work across explicit agent groups with safe confirmation boundaries. |
| `tts-toolkit` | `cyperx84/tts-toolkit` | Consolidate six legacy skills into a small audio collection: speech, dialogue/podcast, audiobook, and voiceover. |
| `voicepipe` | `cyperx84/voicepipe-cli` | Mine transcription and site-adapter behavior for Talk Once; avoid a second publishing workflow. |
| `vault-hub` | `cyperx84/vault-hub-neovim` | Add a knowledge-vault skill only after its MCP/CLI interface is verified current. |

## Audit before importing

| Candidate | Reason |
| --- | --- |
| `dotfiles-skills` | Ten older skills claim production readiness but are Claude-oriented and need command and safety verification. Import only the strongest individual workflows. |
| `image-gen-skills` | Useful educational provider architecture, but overlaps native image-generation capabilities and contains template providers. |
| `faceless-pipeline` skills | Script, footage, thumbnail, composition, and upload skills are promising but currently reference a private local repo and unfinished backends. |
| `cloudflare-pages` | Contains personal Keychain conventions and direct deployment steps; replace with a portable deployment skill rather than publishing it unchanged. |

## Consolidate or exclude

| Source | Disposition |
| --- | --- |
| `claude-skills-mental-models` | Reconcile with the existing `lattice` skill; keep one canonical mental-model system. |
| `clwatch-skill`, `deep-research-v2` | Already represented in the toolbox; treat standalone repositories as upstream implementations or archives. |
| `claude-code-plugin-examples` | Educational examples, not curated production toolbox entries. |
| project-local `gym-cli` | Keep scoped to its application unless the workflow becomes generally reusable. |
| private fleet copies | Do not import directly. Compare only to find fixes for their public canonical counterparts. |

## Suggested order

1. Import `nvim-buffers`, `soul-forge`, and `ascii-animations`.
2. Import `ai-compat` and `remotion` after cross-harness cleanup.
3. Upgrade the `voice-forge` skill around the new portable profile contract.
4. Create adapters for `gen-podcast`, `fleet-status`, and `clawrus`.
5. Consolidate the TTS skills and decide the future of `voicepipe`.
6. Audit the older dotfiles and faceless-content collections one skill at a time.
