---
name: skill-eval
description: "Score and grade OpenClaw skills against the AgentSkills spec, apply fixes, and explain why each change is better. Use this skill whenever someone asks to score, grade, rate, or benchmark a skill's quality — even if they just say 'is this good enough to ship' or 'how does this skill look'. Use when: (1) scoring a skill before shipping, (2) grading skill quality against the spec, (3) checking if a skill is production-ready, (4) evaluating trigger description accuracy, (5) benchmarking a CLI wrapper skill for completeness, (6) running the evaluate→fix→explain loop on any skill. Triggers on: 'skill eval', 'score this skill', 'grade this skill', 'rate this skill', 'is this skill good enough', 'is this skill production quality', 'evaluate this skill', 'how good is this skill', 'benchmark skill quality'. NOT for: creating or structurally editing skills (use skill-creator), running behavioral test cases in Docker/subagents (use Claude Code's eval framework or Skill Eval), editing agent workspace files directly."
---

# Skill Eval — Score → Fix → Explain

## Workflow

### 1. Read the Skill

Read the target SKILL.md and any bundled resources (scripts/, references/, assets/).

### 2. Evaluate

Score the skill against each criterion in `references/rubric.md` (in *this* skill's directory, not the target's). Read the rubric before scoring. Output the structured evaluation with scores, evidence, and fixes per criterion.

### 3. Apply Fixes

Apply the top fixes directly to the SKILL.md (and restructure files if needed). Use the patterns in `references/fix-patterns.md` as a guide for common issues.

**Non-destructive by default:** Write the improved version to `<skill-dir>/.eval/SKILL.md` — do not overwrite the original until the user approves. If restructuring adds/moves files, stage them in `.eval/` too.

### 4. Explain Changes

For each fix applied, output:
```
**Change:** [What changed]
**Why:** [Why the new version is better — reference the rubric criterion]
**Before:** [Relevant snippet]
**After:** [New snippet]
```

### 5. Score Delta

Show before/after scores:
```
Criterion           Before  After
─────────────────────────────────
Description Quality    6      8
Conciseness            7      8
...
─────────────────────────────────
Overall               6.4    8.1
```

### 6. Apply (on approval)

When the user approves, overwrite the original SKILL.md with the improved version from `.eval/`. Delete the `.eval/` directory after applying. If `.eval/` already exists from a prior run, overwrite it.

## CLI Skill Evaluation

When evaluating a skill that wraps a CLI tool, add these checks:

- Run `<tool> --help` and each subcommand's `--help` — verify all commands and important flags are documented
- Check that the skill includes partial workflows (not just the full flow)
- Verify error guidance exists for common failure modes
- Confirm the install method is documented

## Quick Mode

If the user says "quick eval" or wants a fast pass, skip the `.eval/` staging and apply fixes in-place. Still output the score delta and change explanations.

## Batch Mode

To evaluate multiple skills: iterate over each skill directory, run the full workflow, and output a summary table:

```
Skill            Before  After  Top Fix
───────────────────────────────────────
soul-forge        7.3    8.5   Added config schema
clawrus           6.8    8.2   Tightened triggers
```

## Contention Eval (CLI)

Prose scoring above judges a skill alone in an empty room, where it always fires.
The `skilleval` CLI judges it against the real installed roster — does it steal
triggers from skills already installed, or lose its own to them.

Install: `brew install cyperx84/tap/skilleval`
Source: <https://github.com/cyperx84/skilleval> (single stdlib-only file, MIT)

Deterministic, no LLM calls inside the CLI. Roster = merged `~/.agents/skills` +
`~/.openclaw/skills` + `~/.claude/skills`, symlink-deduped, `SKILLEVAL_ROSTER` to override.

```
skilleval lint <skill>      structural checks (frontmatter, name/dir match, length)
skilleval scan <skill>      injection / overbroad-trigger pattern scan, exit-gates
skilleval contend <skill>   shadow rate (loses its own queries) + hijack rate (steals
                            others') + worst-victim rate (destroys one specific skill)
skilleval roster            roster-wide shadow-rate matrix — catches collisions on install
skilleval judge <skill>     prints delegation instructions for the LLM rubric pass above
skilleval all <skill>       lint -> scan -> contend -> judge, gates on fail
```

Query sets are generated from each skill's own description ("Use when" / "Triggers on"
clauses, sentence fallback), scored via TF-IDF cosine over the roster corpus — no live
router needed. `--queries file.json` supplies hand-written sets instead.

Run `skilleval roster` after installing a new skill to catch regressions it causes in
skills you already trusted. It also reports skills with no parsable frontmatter (the
router can never trigger them) and name collisions (one file wins, the other is invisible).

**Reading the numbers:** each skill has home-field advantage on queries generated from its
own description, so `shadow_rate` is biased low. A hit is strong evidence of a real
collision; a zero is weak evidence of safety. TF-IDF catches vocabulary overlap, not
semantic overlap. Use `--queries` with held-out sets for the stronger claim.

The lexical proxy cuts both ways: cosine weights term frequency, so a skill that merely
repeats a shared noun more often can look like it steals a neighbour's triggers with no
semantic overlap at all. Confirm a hit reads as a real collision before acting on it.

Gate on `worst_victim_rate` (> 0.3), not `hijack_rate` (> 0.15), when vetting one
candidate: `hijack_rate` divides by the whole roster's queries, so it fades as the roster
grows. `worst_victim_rate` is the worst single victim's loss and names the victim.
Exit codes: 0 clean, 1 a gate failed, 2 unscorable (never read 2 as a pass).

**Thin query sets report but don't gate.** A rate needs 5+ routable queries behind it to
decide the exit code — at 3 queries the smallest non-zero rate is already over the gate,
so one stolen query would fail on quantisation noise. Suppressed rates are still reported,
with the reason in `advisory`; that is not a clean bill. If a skill is too terse to score,
widen its description or pass `--queries` (hand-written sets gate at any size) rather than
reading the pass as safety.
