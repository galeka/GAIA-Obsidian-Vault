#!/usr/bin/env bash
# =============================================================================
# achat.sh — Run vault-chat.py from anywhere on macOS
# =============================================================================
# Setup (run once):
#   chmod +x achat.sh
#   cp achat.sh ~/achat.sh          # or anywhere on your PATH
#
# Usage:
#   ./achat.sh "What projects do I have?"
#   ./achat.sh "Summarize my migration checklist"
#   ./achat.sh "Create a note in 00-Inbox about X"
# =============================================================================

# ── Configuration ─────────────────────────────────────────────────────────────
export ACHATGPT_API_KEY="${ACHATGPT_API_KEY:-}"
export ACHATGPT_MODEL="${ACHATGPT_MODEL:-gpt-5.4}"

# ── Auto-detect vault path (opsi 1+2: env var + OS detection) ─────────────────
if [ -n "$VAULT_ROOT" ]; then
  # Option 2: User set environment variable — use it
  true
elif [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS — try both iCloud and local paths
  if [ -d "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault" ]; then
    export VAULT_ROOT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault"
  elif [ -d "$HOME/Library/Mobile Documents/com~obsidianmd~obsidian/Documents/MyVault" ]; then
    export VAULT_ROOT="$HOME/Library/Mobile Documents/com~obsidianmd~obsidian/Documents/MyVault"
  elif [ -d "$HOME/Obsidian/MyVault" ]; then
    export VAULT_ROOT="$HOME/Obsidian/MyVault"
  else
    export VAULT_ROOT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault"
  fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
  # Linux / Windows WSL
  export VAULT_ROOT="$HOME/Obsidian/MyVault"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
  # Windows native (Git Bash / Cygwin)
  export VAULT_ROOT="$USERPROFILE/Obsidian/MyVault"
else
  # Fallback — user must set VAULT_ROOT
  export VAULT_ROOT="${VAULT_ROOT:-.}"
fi
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="$SCRIPT_DIR/vault-chat.py"

if [[ -z "$1" ]]; then
  echo "Usage: $0 \"<your question>\""
  echo ""
  echo "Examples:"
  echo "  $0 \"What projects do I have?\""
  echo "  $0 \"Summarize my migration checklist\""
  echo "  $0 \"Search for notes about budgets\""
  echo "  $0 \"Create a new note in 00-Inbox/ about topic X\""
  exit 1
fi

exec python3 "$RUNNER" "$@"
