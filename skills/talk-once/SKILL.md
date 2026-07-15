---
name: talk-once
description: Turn a conversation, voice note, transcript, or guided interview into one source-grounded canonical article and reviewed channel-specific drafts. Use when someone wants to be interviewed about an idea, create long-form content from speech, repurpose one piece across channels, build a content package, or run the Talk Once workflow with an optional VoiceForge profile.
---

# Talk Once

Turn one substantive conversation into reusable content while keeping the user
in control of truth, voice, and publishing.

## Operating rules

- Keep Markdown and JSON files as the source of truth.
- Work with any model or agent harness available to the user.
- Separate the user's claims from sourced facts and agent inference.
- Use a voice profile as style guidance only; never invent beliefs or claims.
- Establish one canonical article before producing derivatives.
- Ask for approval at the brief, article, and distribution boundaries.
- Never publish or post without explicit approval.
- Keep recordings, raw transcripts, credentials, and unpublished personal data
  outside public repositories.

## Workflow

1. Create a content package from the Talk Once template or schema.
2. If the package references a voice profile, read it before interviewing.
3. Interview for the idea, audience, evidence, personal experience, useful
   examples, disagreements, and desired outcome. Ask one focused question at a
   time when the interface supports conversation.
4. Attach supplied sources. Research only when requested or when factual
   verification is necessary. Preserve links and distinguish evidence from
   interpretation.
5. Produce a brief containing the thesis, audience, promise, outline, claims,
   sources, unknowns, and tone notes. Stop for approval.
6. Draft one canonical long-form article from the approved brief. Preserve the
   speaker's meaning while tightening structure and prose. Stop for approval.
7. Produce only the requested derivatives from the approved canonical article.
   Adapt format and length without changing the underlying position.
8. Present the distribution set for approval. Do not publish automatically.

## Interoperability

Prefer stable contracts over harness-specific state:

- Voice providers export a versioned JSON profile. VoiceForge supports
  `forge profile --output <path>`.
- Talk Once packages conform to `content-package.schema.json` and may reference
  a voice profile by provider, path, and version.
- Harness integrations should orchestrate this workflow without changing the
  contracts.

Read [references/contracts.md](references/contracts.md) when creating or
validating package files.

## Completion

Return the created artifact paths, current package status, outstanding approval,
and any unresolved factual questions. A draft is not published content.
