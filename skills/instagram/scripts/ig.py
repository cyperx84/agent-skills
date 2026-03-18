#!/usr/bin/env python3
"""
Instagram CLI wrapper for OpenClaw agents.
Provides headless access to Instagram features.

Usage:
  ig.py login <username> <password>
  ig.py dm <username> <message>
  ig.py inbox [--count N]
  ig.py feed [--count N]
  ig.py post <image_path> <caption>
  ig.py story <image_path>
  ig.py followers [username]
  ig.py following [username]
  ig.py search <query>
  ig.py profile <username>
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, ChallengeRequired
except ImportError:
    print("Error: instagrapi not installed. Run: pip install instagrapi")
    sys.exit(1)

SESSION_DIR = Path.home() / ".instagram-cli" / "sessions"
DEFAULT_SESSION = SESSION_DIR / "default" / "session.json"


def get_client(username: str = None) -> Client:
    """Get authenticated client, loading session if available."""
    cl = Client()
    
    if username:
        session_path = SESSION_DIR / username / "session.json"
    else:
        session_path = DEFAULT_SESSION
    
    if session_path.exists():
        cl.load_settings(session_path)
        try:
            cl.get_timeline_feed()  # Test if session is valid
            return cl
        except LoginRequired:
            print(f"Session expired for {username or 'default'}")
    
    return cl


def save_session(cl: Client, username: str):
    """Save session for future use."""
    session_path = SESSION_DIR / username / "session.json"
    session_path.parent.mkdir(parents=True, exist_ok=True)
    cl.dump_settings(session_path)


def cmd_login(args):
    """Login and save session."""
    cl = Client()
    try:
        cl.login(args.username, args.password)
        save_session(cl, args.username)
        print(f"✓ Logged in as {args.username}")
        print(f"  Session saved to: {SESSION_DIR / args.username}")
    except ChallengeRequired:
        print("2FA required. Please use instagram-cli auth login for interactive login.")
        sys.exit(1)
    except Exception as e:
        print(f"Login failed: {e}")
        sys.exit(1)


def cmd_dm(args):
    """Send a direct message."""
    cl = get_client(args.account)
    user_id = cl.user_id_from_username(args.username)
    cl.direct_send(args.message, user_ids=[user_id])
    print(f"✓ Sent DM to @{args.username}")


def cmd_inbox(args):
    """List recent DM threads."""
    cl = get_client(args.account)
    threads = cl.direct_threads(amount=args.count)
    
    for t in threads:
        title = t.thread_title or "Unknown"
        last_msg = t.messages[0].text if t.messages else "(no messages)"
        if len(last_msg) > 50:
            last_msg = last_msg[:50] + "..."
        print(f"• {title}: {last_msg}")


def cmd_feed(args):
    """View recent feed posts."""
    cl = get_client(args.account)
    
    if args.username:
        user_id = cl.user_id_from_username(args.username)
        posts = cl.user_medias(user_id, amount=args.count)
    else:
        posts = cl.get_timeline_feed()["feed_items"][:args.count]
    
    for post in posts:
        if hasattr(post, "caption_text"):
            caption = post.caption_text or ""
        else:
            caption = post.get("media_or_ad", {}).get("caption", {}).get("text", "")
        
        if len(caption) > 100:
            caption = caption[:100] + "..."
        print(f"• {caption}")


def cmd_post(args):
    """Post a photo."""
    cl = get_client(args.account)
    media = cl.photo_upload(args.image_path, args.caption)
    print(f"✓ Posted photo: {media.pk}")


def cmd_story(args):
    """Post a story."""
    cl = get_client(args.account)
    media = cl.photo_upload_to_story(args.image_path)
    print(f"✓ Posted story: {media.pk}")


def cmd_profile(args):
    """Get user profile info."""
    cl = get_client(args.account)
    user = cl.user_info_by_username(args.username)
    
    print(f"@{user.username}")
    print(f"  Name: {user.full_name}")
    print(f"  Bio: {user.biography}")
    print(f"  Followers: {user.follower_count}")
    print(f"  Following: {user.following_count}")
    print(f"  Posts: {user.media_count}")


def cmd_search(args):
    """Search for users."""
    cl = get_client(args.account)
    users = cl.search_users(args.query)
    
    for user in users[:10]:
        print(f"• @{user.username} - {user.full_name}")


def main():
    parser = argparse.ArgumentParser(description="Instagram CLI for OpenClaw agents")
    parser.add_argument("--account", "-a", help="Account to use (default: default)")
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Login
    p_login = subparsers.add_parser("login", help="Login to Instagram")
    p_login.add_argument("username")
    p_login.add_argument("password")
    
    # DM
    p_dm = subparsers.add_parser("dm", help="Send a direct message")
    p_dm.add_argument("username", help="Recipient username")
    p_dm.add_argument("message", help="Message to send")
    
    # Inbox
    p_inbox = subparsers.add_parser("inbox", help="List DM threads")
    p_inbox.add_argument("--count", "-n", type=int, default=10, help="Number of threads")
    
    # Feed
    p_feed = subparsers.add_parser("feed", help="View feed")
    p_feed.add_argument("username", nargs="?", help="User to view (default: your feed)")
    p_feed.add_argument("--count", "-n", type=int, default=10, help="Number of posts")
    
    # Post
    p_post = subparsers.add_parser("post", help="Post a photo")
    p_post.add_argument("image_path", help="Path to image")
    p_post.add_argument("caption", help="Post caption")
    
    # Story
    p_story = subparsers.add_parser("story", help="Post a story")
    p_story.add_argument("image_path", help="Path to image")
    
    # Profile
    p_profile = subparsers.add_parser("profile", help="View user profile")
    p_profile.add_argument("username", help="Username to view")
    
    # Search
    p_search = subparsers.add_parser("search", help="Search users")
    p_search.add_argument("query", help="Search query")
    
    args = parser.parse_args()
    
    commands = {
        "login": cmd_login,
        "dm": cmd_dm,
        "inbox": cmd_inbox,
        "feed": cmd_feed,
        "post": cmd_post,
        "story": cmd_story,
        "profile": cmd_profile,
        "search": cmd_search,
    }
    
    commands[args.command](args)


if __name__ == "__main__":
    main()
