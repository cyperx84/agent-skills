---
name: ascii-animations
description: Design or implement polished ASCII and ANSI animations for command-line and terminal applications. Use when adding spinners, loading states, splash screens, animated banners, terminal effects, or CLI/TUI motion in Go, JavaScript, TypeScript, Rust, or Python.
---

# ASCII Animations

Add motion that improves feedback and personality without breaking terminal
compatibility, accessibility, or non-interactive use.

## Choose the smallest useful effect

- Use a spinner for indeterminate work.
- Use progress text or a bar when progress is measurable.
- Use a short splash animation only at intentional product moments.
- Use full-screen effects only when the animation is the experience.
- Keep logs and piped output static.

## Common libraries

| Language | Lightweight feedback | Full TUI/effects |
| --- | --- | --- |
| Go | `briandowns/spinner` | Bubble Tea, Lip Gloss |
| JavaScript/TypeScript | `ora`, `cli-spinners` | Ink |
| Rust | `indicatif` | Ratatui, TachyonFX |
| Python | `yaspin` | Textual, asciimatics |

Prefer an existing project dependency or native framework facility before
adding another animation library.

## Implementation rules

1. Detect whether stdout is an interactive terminal.
2. Disable motion for `NO_COLOR`, `TERM=dumb`, CI, redirected output, and an
   explicit `--no-animation` option.
3. Never make animation the only signal that work succeeded or failed.
4. Hide the cursor only while animating and restore it with cleanup handlers on
   success, error, cancellation, and interrupts.
5. Render frames into memory and write each frame in one operation.
6. Update only changed lines instead of repeatedly clearing the whole screen.
7. Use elapsed-time frame selection so slow frames do not permanently drift.
8. Cap refresh rates; spinners rarely need more than 10–15 frames per second.
9. Test narrow terminals, Unicode-disabled environments, and interrupted runs.

## Portable frame format

For custom reusable animations, prefer plain JSON:

```json
{
  "interval_ms": 100,
  "frames": ["⠋", "⠙", "⠹", "⠸"]
}
```

Keep a basic ASCII fallback such as `| / - \\` for environments without Unicode.

## Verification

Run the relevant tests and manually verify interactive, redirected, disabled,
and interrupted behavior. Report any terminal-specific assumptions introduced.
