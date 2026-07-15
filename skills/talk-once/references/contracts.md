# Talk Once contracts

Canonical schemas:

- Content package: `https://github.com/cyperx84/talk-once/blob/main/schemas/content-package.schema.json`
- VoiceForge profile: `https://github.com/cyperx84/voice-forge/blob/main/schemas/voice-profile.schema.json`

Minimal content package:

```json
{
  "version": "1.0",
  "id": "my-idea",
  "title": "My idea",
  "status": "idea",
  "canonicalPath": null,
  "voiceProfile": {
    "provider": "voiceforge",
    "path": "./private/voice-profile.json",
    "version": "1.0"
  },
  "sources": [],
  "outputs": { "website": "pending" },
  "approvals": {
    "brief": false,
    "article": false,
    "distribution": false
  }
}
```

Resolve relative paths from the package file's directory. Do not embed raw
corpus entries in a content package. If a profile cannot be loaded, continue
without it and report that clearly rather than blocking capture.
