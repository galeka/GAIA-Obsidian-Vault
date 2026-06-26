#!/usr/bin/env bash
# =============================================================================
# .achatgpt/http-client.sh — AChatGPT HTTP API client
# =============================================================================
# Source this file to make API calls against the AChatGPT proxy.
# Requires: ACHATGPT_API_KEY env var. curl and jq must be on PATH.
# =============================================================================

ACHATGPT_API_KEY="${ACHATGPT_API_KEY:?ERROR: ACHATGPT_API_KEY not set}"
ACHATGPT_PROXY_URL="${ACHATGPT_PROXY_URL:?ERROR: ACHATGPT_PROXY_URL is not set}"
ACHATGPT_TIMEOUT="${ACHATGPT_REQUEST_TIMEOUT:-60}"
ACHATGPT_RETRIES="${ACHATGPT_RETRY_ATTEMPTS:-3}"

# achatgpt_chat <model> <system_prompt> <user_message> [temperature]
# Sends a single-turn chat completion. Echoes the raw JSON response.
achatgpt_chat() {
  local model="${1:?model required}"
  local system_prompt="$2"
  local user_message="$3"
  local temperature="${4:-0.7}"

  local payload; payload=$(jq -n \
    --arg model   "$model" \
    --arg system  "$system_prompt" \
    --arg user    "$user_message" \
    --argjson temp "$temperature" \
    '{
      model: $model,
      messages: [
        {role: "system", content: $system},
        {role: "user",   content: $user}
      ],
      temperature: $temp,
      stream: false
    }')

  _achatgpt_request "/chat/completions" "POST" "$payload"
}

# _achatgpt_request <endpoint> <method> <payload>
# One curl call captures both body and HTTP status — no double-request waste.
# Retries on 429/502/503 with exponential backoff.
_achatgpt_request() {
  local endpoint="$1" method="$2" payload="$3"
  local attempt=0

  while (( attempt < ACHATGPT_RETRIES )); do
    local tmp; tmp="$(mktemp)"
    local http_code
    http_code=$(curl -s \
      -X "$method" \
      "${ACHATGPT_PROXY_URL}${endpoint}" \
      -H "Authorization: Bearer ${ACHATGPT_API_KEY}" \
      -H "Content-Type: application/json" \
      -H "x-api-type: openai" \
      --max-time "${ACHATGPT_TIMEOUT}" \
      -d "$payload" \
      -o "$tmp" \
      -w "%{http_code}")
    local response; response=$(cat "$tmp"); rm -f "$tmp"

    if [[ "$http_code" == "200" ]]; then
      echo "$response"
      return 0
    fi

    if [[ "$http_code" =~ ^(429|502|503)$ ]]; then
      (( attempt++ ))
      if (( attempt < ACHATGPT_RETRIES )); then
        local backoff=$(( 2 ** attempt ))
        echo "[AChatGPT] HTTP $http_code — retrying in ${backoff}s (${attempt}/${ACHATGPT_RETRIES})" >&2
        sleep "$backoff"
        continue
      fi
    fi

    echo "[AChatGPT ERROR] HTTP $http_code: $response" >&2
    return 1
  done

  return 1
}

# achatgpt_extract_content <response_json>
# Extracts the assistant message text from a chat completion response.
achatgpt_extract_content() {
  echo "$1" | jq -r '.choices[0].message.content // empty'
}

# achatgpt_extract_error <response_json>
achatgpt_extract_error() {
  echo "$1" | jq -r '.error.message // "Unknown error"'
}

# achatgpt_check_quota
# Lightweight probe — returns 0 if API is reachable and key is valid.
achatgpt_check_quota() {
  local payload='{"model":"gpt-4o-mini","messages":[{"role":"user","content":"ping"}],"max_tokens":1}'
  _achatgpt_request "/chat/completions" "POST" "$payload" > /dev/null 2>&1
}
