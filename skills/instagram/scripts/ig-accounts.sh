#!/bin/bash
# Instagram multi-account helper
# Usage: ig-accounts.sh [list|switch|current|login]

set -e

CMD=${1:-list}

case "$CMD" in
  list)
    echo "Saved Instagram accounts:"
    ls -1 ~/.instagram-cli/sessions/ 2>/dev/null || echo "No accounts saved yet"
    ;;
  
  current|whoami)
    instagram-cli auth whoami
    ;;
  
  switch)
    if [ -z "$2" ]; then
      echo "Usage: ig-accounts.sh switch <username>"
      exit 1
    fi
    instagram-cli auth switch "$2"
    echo "Switched to: $2"
    ;;
  
  login)
    if [ -z "$2" ]; then
      echo "Usage: ig-accounts.sh login <username>"
      exit 1
    fi
    instagram-cli auth login --username "$2"
    ;;
  
  logout)
    instagram-cli auth logout
    ;;
  
  *)
    echo "Instagram Account Manager"
    echo ""
    echo "Usage: ig-accounts.sh <command> [args]"
    echo ""
    echo "Commands:"
    echo "  list              List saved accounts"
    echo "  current, whoami   Show current account"
    echo "  switch <user>     Switch to account"
    echo "  login <user>      Login to new account"
    echo "  logout            Logout current account"
    ;;
esac
