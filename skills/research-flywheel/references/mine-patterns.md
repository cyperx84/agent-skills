# Mine Patterns

Patterns used by `research-flywheel mine` to scan conversation history via `lcm_grep`.

## Usage

From an OpenClaw agent session, use these patterns with `lcm_grep`:

```
lcm_grep({ pattern: "<pattern>", mode: "regex", scope: "messages" })
```

## Pattern Categories

### Research Directives
Explicit requests to research something.
```
(?i)(research this|look into|investigate|deep dive on?|find out about) (.+)
```

### How/What Questions
Curiosity-driven questions that signal research interest.
```
(?i)how (does|do|can|to) (.+?)[.?]
(?i)what('?s| is| are) (the )?(best|difference|state of|future of) (.+?)[.?]
```

### Evaluation Language
Comparing options signals a research need.
```
(?i)(compare|versus|vs\\.?|better than|alternative[s]? to) (.+)
```

### Build Context
Building something around a topic = deep research opportunity.
```
(?i)(build|create|make|ship) (a |an )?(.+?)(app|tool|cli|service|platform)
```

### Repeated Mentions
Same topic across multiple conversations = high priority candidate.
- Strategy: run broad topic extraction, count frequency across conversations
- Pattern: extract noun phrases that appear in 3+ conversations

## Scoring

| Signal | Weight | Notes |
|--------|--------|-------|
| Chris-initiated | +3 | Message from sender matching Chris's ID |
| Explicit directive | +3 | "research this", "look into" |
| Multiple mentions | +2 | Same topic in 2+ conversations |
| Recent (last 3 days) | +2 | Recency bonus |
| Build context | +1 | "build X" around the topic |
| Question format | +1 | How/what questions |

## Dedup Rules

- Normalize: lowercase, strip punctuation, collapse whitespace
- Topic = first 5 meaningful words from the match
- Match against `state.completed[].topic` and `state.candidates[].topic`
- If topic already completed in last 30 days, skip
