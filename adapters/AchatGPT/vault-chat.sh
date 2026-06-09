#!/usr/bin/env bash
# =============================================================================
# adapters/achatgpt/vault-chat.sh — Chat with your Obsidian vault via AChatGPT
# =============================================================================
# Usage:
#   export ACHATGPT_API_KEY="..."
#   export VAULT_ROOT="/path/to/your/vault"   # defaults to current directory
#   bash vault-chat.sh "What projects do I have?"
#   bash vault-chat.sh "Summarise my notes on topic X"
#   bash vault-chat.sh "Create a new note about Y in 00-Inbox/"
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/runner.sh"

# ── Config ────────────────────────────────────────────────────────────────────

VAULT_ROOT="${VAULT_ROOT:-$(pwd)}"
MODEL="${ACHATGPT_MODEL:-gpt-4o}"

SYSTEM_PROMPT="You are a personal knowledge assistant with full read/write access to the user's Obsidian vault at: $VAULT_ROOT

Available tools:
- read_file: read any note by path
- list_files: list files in any directory
- search_vault: full-text search across all notes
- write_file: create or update notes

Guidelines:
- Use tools to gather context before answering
- Quote relevant passages from notes when helpful
- When writing new notes, use Obsidian markdown with YAML frontmatter
- Be concise and specific"

# ── CLI entry ─────────────────────────────────────────────────────────────────

if [[ -z "$1" ]]; then
  echo "Usage: $0 \"<your question>\""
  echo "Example: $0 \"What are my active projects?\""
  exit 1
fi

if [[ -z "$ACHATGPT_API_KEY" ]]; then
  echo "ERROR: ACHATGPT_API_KEY not set."
  echo "Run: export ACHATGPT_API_KEY=\"your-key\""
  exit 1
fi

echo "Vault: $VAULT_ROOT" >&2
echo "Model: $MODEL" >&2
echo "---" >&2

run_agent "$MODEL" "$SYSTEM_PROMPT" "$1"
