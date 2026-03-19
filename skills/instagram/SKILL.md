---
name: instagram
description: "Control Instagram via instagram-cli — browse feed, send/read DMs, view and post stories, upload content, manage multiple accounts. Use when the user mentions Instagram, asks to check/post DMs, view stories, upload a photo/reel, or manage Instagram accounts."
metadata:
  { "openclaw": { "emoji": "📸", "os": ["darwin", "linux"], "requires": { "bins": ["instagram-cli"] } } }
---

# Instagram Skill (OpenClaw)

Full Instagram control via `instagram-cli` — DMs, feed, stories, posts, multi-account support.

## Installation

```bash
brew tap supreme-gg-gg/tap
brew install instagram-cli
```

Or via npm:
```bash
npm install -g @i7m/instagram-cli
```

## Authentication

### Login (first time)
```bash
instagram-cli auth login --username <username>
# Follow prompts for password and 2FA if enabled
```

### Multi-Account Setup
```bash
# Login to multiple accounts
instagram-cli auth login --username account1
instagram-cli auth login --username account2

# Check current account
instagram-cli auth whoami

# Switch accounts
instagram-cli auth switch <username>

# List saved accounts
instagram-cli auth list
```

Sessions are saved locally at `~/.instagram-cli/`

## Core Commands

### Feed
```bash
# View your feed
instagram-cli feed

# View specific user's posts
instagram-cli feed <username>
```

### Stories
```bash
# View stories from people you follow
instagram-cli stories
```

### Notifications
```bash
# View notifications (inbox, followers, mentions)
instagram-cli notify
```

### Chat/DMs (TUI)
```bash
# Open chat interface
instagram-cli chat

# Open chat with specific user
instagram-cli chat -u <username>

# Chat with custom title
instagram-cli chat -t "Work DMs"
```

#### Chat Commands (inside TUI)
```
:select              # Select message for actions
:react <emoji>       # React to selected message
:reply <text>        # Reply to selected message
:unsend              # Unsend selected message
:upload <path>       # Upload image/video
:download <path>     # Download selected media
:k / :j              # Navigate up/down
:K / :J              # Jump to top/bottom
```

## Headless Operations

For automation, use the Python client which has more scripting capabilities:

```bash
pip install instagram-cli
```

The Python client uses the `instagram` command (not `instagram-cli`).

## Multi-Account Automation Pattern

For running multiple bots/accounts:

```bash
# Script to post to multiple accounts
for account in account1 account2 account3; do
  instagram-cli auth switch $account
  # perform actions
done
```

Or use `--username` flag:
```bash
instagram-cli feed --username account1
instagram-cli feed --username account2
```

## Configuration

```bash
# View all config
instagram-cli config

# Set config value
instagram-cli config <key> <value>

# Edit config file directly
instagram-cli config edit

# Config location: ~/.instagram-cli/config.ts.yaml
```

### Common Config Options
| Key | Default | Description |
|-----|---------|-------------|
| `image.protocol` | `halfBlock` | Image rendering: ascii, halfBlock, braille, kitty, iterm2, sixel |
| `feed.feedType` | `list` | Feed layout: timeline, list |

## Agent Integration

### Reading DMs
```bash
# For agents, use the Python client for non-interactive access
pip install instagrapi

# Then use Python scripting for automation
python3 -c "
from instagrapi import Client
cl = Client()
cl.load_settings('~/.instagram-cli/session.json')  # or login
threads = cl.direct_threads()
for t in threads[:5]:
    print(t.thread_title, t.messages[0].text if t.messages else '')
"
```

### Sending DMs Programmatically
```bash
python3 -c "
from instagrapi import Client
cl = Client()
cl.login('username', 'password')
cl.direct_send('Hello!', user_ids=[cl.user_id_from_username('target_user')])
"
```

### Posting Content
```bash
python3 -c "
from instagrapi import Client
cl = Client()
cl.login('username', 'password')
cl.photo_upload('path/to/photo.jpg', 'Caption here')
"
```

## Multi-Bot Architecture

For running multiple Instagram bots:

```
~/.instagram-cli/
├── sessions/
│   ├── bot1/
│   │   └── session.json
│   ├── bot2/
│   │   └── session.json
│   └── bot3/
│       └── session.json
```

Each bot can have its own session directory. Use environment variables or config to point to different sessions.

## Limitations & Warnings

⚠️ **Account Risk**: Using unofficial APIs may violate Instagram ToS. Use responsibly.

- Don't spam or automate aggressively
- Add delays between actions
- Use for personal productivity, not mass automation
- Instagram may require re-authentication periodically

## Troubleshooting

### Login Issues
```bash
# Clear session and re-login
instagram-cli auth logout
instagram-cli auth login --username <username>
```

### 2FA Required
The CLI supports 2FA — you'll be prompted to enter the code during login.

### Rate Limiting
If you hit rate limits, wait a few hours before trying again. Don't retry aggressively.

## See Also

- [instagram-cli GitHub](https://github.com/supreme-gg-gg/instagram-cli)
- [instagrapi Python library](https://github.com/subzeroid/instagrapi) (for deeper automation)
