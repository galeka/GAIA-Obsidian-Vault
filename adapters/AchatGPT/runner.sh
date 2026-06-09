#!/usr/bin/env bash
# =============================================================================
# adapters/achatgpt/runner.sh — Local tool-use loop for vault access
# =============================================================================
# Sources http-client.sh, then runs an agentic loop:
#   1. Send query + tool schemas to AChatGPT
#   2. If response has tool_calls → execute locally → append result → repeat
#   3. If finish_reason == stop → print final answer
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/templates/achatgpt-http-client.sh"

VAULT_ROOT="${VAULT_ROOT:-$(pwd)}"

# ── Tool schemas ─────────────────────────────────────────────────────────────

VAULT_TOOLS=$(jq -n '[
  {
    "type": "function",
    "function": {
      "name": "read_file",
      "description": "Read the full contents of a file in the Obsidian vault.",
      "parameters": {
        "type": "object",
        "properties": {
          "path": {"type": "string", "description": "Relative path from vault root (e.g. 01-Projects/MyProject/note.md)"}
        },
        "required": ["path"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "list_files",
      "description": "List files in a vault directory. Returns relative paths.",
      "parameters": {
        "type": "object",
        "properties": {
          "directory": {"type": "string", "description": "Directory relative to vault root"},
          "pattern":   {"type": "string", "description": "Filename glob pattern (default: *.md)"}
        },
        "required": ["directory"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "search_vault",
      "description": "Search for text or regex across vault notes. Returns matching file paths and lines.",
      "parameters": {
        "type": "object",
        "properties": {
          "query":        {"type": "string", "description": "Text or regex to search for"},
          "file_pattern": {"type": "string", "description": "Limit to files matching this glob (default: *.md)"}
        },
        "required": ["query"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "write_file",
      "description": "Create or overwrite a file in the vault.",
      "parameters": {
        "type": "object",
        "properties": {
          "path":    {"type": "string", "description": "Relative path from vault root"},
          "content": {"type": "string", "description": "Full file content to write"}
        },
        "required": ["path", "content"]
      }
    }
  }
]')

# ── Tool execution ────────────────────────────────────────────────────────────

_execute_tool() {
  local name="$1" args="$2"

  case "$name" in
    read_file)
      local path; path=$(echo "$args" | jq -r '.path')
      local full="$VAULT_ROOT/$path"
      if [[ -f "$full" ]]; then
        cat "$full"
      else
        echo "ERROR: file not found: $path"
      fi
      ;;

    list_files)
      local dir; dir=$(echo "$args" | jq -r '.directory')
      local pat; pat=$(echo "$args" | jq -r '.pattern // "*.md"')
      local full="$VAULT_ROOT/$dir"
      if [[ -d "$full" ]]; then
        find "$full" -name "$pat" 2>/dev/null | sed "s|$VAULT_ROOT/||" | sort
      else
        echo "ERROR: directory not found: $dir"
      fi
      ;;

    search_vault)
      local query; query=$(echo "$args" | jq -r '.query')
      local pat;   pat=$(echo "$args"   | jq -r '.file_pattern // "*.md"')
      grep -r --include="$pat" -n "$query" "$VAULT_ROOT" 2>/dev/null \
        | sed "s|$VAULT_ROOT/||" \
        | head -60
      ;;

    write_file)
      local path;    path=$(echo "$args"    | jq -r '.path')
      local content; content=$(echo "$args" | jq -r '.content')
      local full="$VAULT_ROOT/$path"
      mkdir -p "$(dirname "$full")"
      printf '%s' "$content" > "$full"
      echo "Written: $path"
      ;;

    *)
      echo "ERROR: unknown tool: $name"
      ;;
  esac
}

# ── Agentic loop ──────────────────────────────────────────────────────────────

# run_agent <model> <system_prompt> <user_message>
# Runs the tool-use loop. Prints final answer to stdout; progress to stderr.
run_agent() {
  local model="${1:-gpt-4o}"
  local system_prompt="$2"
  local user_message="$3"

  local messages; messages=$(jq -n \
    --arg sys  "$system_prompt" \
    --arg user "$user_message" \
    '[{"role":"system","content":$sys},{"role":"user","content":$user}]')

  local iteration=0
  local max_iter=10

  while (( iteration < max_iter )); do
    (( iteration++ ))

    local payload; payload=$(jq -n \
      --arg       model    "$model" \
      --argjson   messages "$messages" \
      --argjson   tools    "$VAULT_TOOLS" \
      '{model:$model, messages:$messages, tools:$tools, tool_choice:"auto", stream:false}')

    local response; response=$(_achatgpt_request "/chat/completions" "POST" "$payload")
    [[ $? -ne 0 ]] && return 1

    local finish;   finish=$(echo "$response"   | jq -r '.choices[0].finish_reason')
    local asst_msg; asst_msg=$(echo "$response" | jq    '.choices[0].message')

    messages=$(echo "$messages" | jq --argjson m "$asst_msg" '. += [$m]')

    if [[ "$finish" == "stop" ]]; then
      echo "$response" | jq -r '.choices[0].message.content'
      return 0
    fi

    if [[ "$finish" == "tool_calls" ]]; then
      local calls; calls=$(echo "$asst_msg" | jq '.tool_calls')
      local n;     n=$(echo "$calls" | jq 'length')

      for (( i=0; i<n; i++ )); do
        local call;      call=$(echo "$calls"    | jq ".[$i]")
        local call_id;   call_id=$(echo "$call"  | jq -r '.id')
        local tool_name; tool_name=$(echo "$call"| jq -r '.function.name')
        local tool_args; tool_args=$(echo "$call"| jq -r '.function.arguments')

        echo "[tool: $tool_name]" >&2

        local result; result=$(_execute_tool "$tool_name" "$tool_args")

        local tool_msg; tool_msg=$(jq -n \
          --arg id      "$call_id" \
          --arg content "$result" \
          '{"role":"tool","tool_call_id":$id,"content":$content}')
        messages=$(echo "$messages" | jq --argjson m "$tool_msg" '. += [$m]')
      done
    else
      echo "[AChatGPT] unexpected finish_reason: $finish" >&2
      echo "$response" | jq -r '.choices[0].message.content // empty'
      return 1
    fi
  done

  echo "[AChatGPT] max iterations ($max_iter) reached" >&2
  return 1
}
