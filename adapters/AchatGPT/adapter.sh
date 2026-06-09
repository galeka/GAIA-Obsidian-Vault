#!/usr/bin/env bash
# =============================================================================
# adapters/achatgpt/adapter.sh — AChatGPT framework adapter
# =============================================================================
# Sourced by scripts/build.sh AFTER adapters/lib.sh.
# Translates source files into a dist/achatgpt/ tree.
# =============================================================================

ACHATGPT_PLATFORM="achatgpt"
ACHATGPT_FW_DIR="achatgpt"
ACHATGPT_DISPATCHER="ACHATGPT.md"

# Neutral model tier → AChatGPT model name.
achatgpt_model_to_native() {
  local model="$1"
  case "$model" in
    */*)   echo "$model" ;;
    low)   echo "gpt-4o-mini" ;;
    mid)   echo "gpt-5.4" ;;
    high)  echo "o3" ;;
    *)     echo "$model" ;;
  esac
}

# adapter_translate_dispatcher <source_dispatcher_md> <dest_dir>
adapter_translate_dispatcher() {
  local src="$1" dst="$2"
  [[ -f "$src" ]] || return 0
  mkdir -p "$dst"
  cp "$src" "$dst/ACHATGPT.md"
  rewrite_platform_paths "$dst/ACHATGPT.md" "$ACHATGPT_FW_DIR" "$ACHATGPT_DISPATCHER"
}

# adapter_translate_references <source_refs_dir> <dest_root>
adapter_translate_references() {
  local src="$1" dst="$2"
  [[ -d "$src" ]] || return 0
  local out="$dst/.achatgpt/references"
  mkdir -p "$out"
  for f in "$src"/*.md; do
    [[ -f "$f" ]] || continue
    should_include "$f" "$ACHATGPT_PLATFORM" || continue
    cp "$f" "$out/"
    rewrite_platform_paths "$out/$(basename "$f")" "$ACHATGPT_FW_DIR" "$ACHATGPT_DISPATCHER"
  done
}

# adapter_translate_skills <source_skills_dir> <dest_root>
adapter_translate_skills() {
  local src="$1" dst="$2"
  [[ -d "$src" ]] || return 0
  for skill_dir in "$src"/*/; do
    [[ -f "${skill_dir}SKILL.md" ]] || continue
    should_include "${skill_dir}SKILL.md" "$ACHATGPT_PLATFORM" || continue
    local name; name="$(basename "$skill_dir")"
    local out="$dst/.achatgpt/skills/$name"
    mkdir -p "$out"
    cp "${skill_dir}SKILL.md" "$out/SKILL.md"
    rewrite_platform_paths "$out/SKILL.md" "$ACHATGPT_FW_DIR" "$ACHATGPT_DISPATCHER"
  done
}

# adapter_translate_agents <source_agents_dir> <dest_root>
# Writes each agent to .achatgpt/agents/<name>.md with AChatGPT model names.
adapter_translate_agents() {
  local src="$1" dst="$2"
  [[ -d "$src" ]] || return 0
  local out_dir="$dst/.achatgpt/agents"
  mkdir -p "$out_dir"

  while IFS= read -r agent; do
    [[ -f "$agent" ]] || continue
    should_include "$agent" "$ACHATGPT_PLATFORM" || continue

    local name; name="$(parse_frontmatter "$agent" name)"
    local model_raw; model_raw="$(parse_frontmatter "$agent" model)"
    local model_out; model_out="$(achatgpt_model_to_native "$model_raw")"

    local out_file="$out_dir/$(basename "$agent")"
    {
      echo "---"
      echo "name: $name"
      awk '/^---$/{n++; next} n==1 && /^description:/{print; in_desc=1; next} n==1 && in_desc && /^[[:space:]]/{print; next} n==1 && in_desc && !/^[[:space:]]/{in_desc=0} n>=2{exit}' "$agent"
      echo "model: $model_out"
      echo "---"
      echo ""
      agent_body "$agent"
    } > "$out_file"
    rewrite_platform_paths "$out_file" "$ACHATGPT_FW_DIR" "$ACHATGPT_DISPATCHER"
  done < <(enumerate_agents "$src")
}

# adapter_translate_mcp <source_mcp_dir> <dest_root>
# Copies MCP server definitions — AChatGPT loads these via env or config.
adapter_translate_mcp() {
  local src="$1" dst="$2"
  local yaml="$src/servers.yaml"
  [[ -f "$yaml" ]] || return 0
  mkdir -p "$dst/.achatgpt"
  cp "$yaml" "$dst/.achatgpt/mcp-servers.yaml"
}

# adapter_finalize <source_root> <dest_root>
# Installs the HTTP client, runtime scripts, .env.example, and model mapping.
adapter_finalize() {
  local src="$1" dst="$2"
  local adapter_dir; adapter_dir="$(dirname "${BASH_SOURCE[0]}")"
  local tpl_dir="$adapter_dir/templates"
  local achatgpt_dir="$dst/.achatgpt"
  mkdir -p "$achatgpt_dir"

  if [[ -f "$tpl_dir/achatgpt-http-client.sh" ]]; then
    cp "$tpl_dir/achatgpt-http-client.sh" "$achatgpt_dir/http-client.sh"
    chmod +x "$achatgpt_dir/http-client.sh"
  fi

  if [[ -f "$tpl_dir/achatgpt-env.example" ]]; then
    cp "$tpl_dir/achatgpt-env.example" "$achatgpt_dir/.env.example"
  fi

  if [[ -f "$src/adapters/achatgpt/models-mapping.yaml" ]]; then
    cp "$src/adapters/achatgpt/models-mapping.yaml" "$achatgpt_dir/models-mapping.yaml"
  fi

  # Runtime: tool-use loop engine and CLI entry point
  if [[ -f "$adapter_dir/runner.sh" ]]; then
    cp "$adapter_dir/runner.sh" "$achatgpt_dir/runner.sh"
    chmod +x "$achatgpt_dir/runner.sh"
  fi

  if [[ -f "$adapter_dir/vault-chat.sh" ]]; then
    cp "$adapter_dir/vault-chat.sh" "$achatgpt_dir/vault-chat.sh"
    chmod +x "$achatgpt_dir/vault-chat.sh"
  fi
}

# adapter_build <source_dir> <dest_dir>
# Entry point called by scripts/build.sh.
adapter_build() {
  local src="$1" dst="$2"
  rm -rf "$dst"
  mkdir -p "$dst"
  adapter_translate_dispatcher "$src/DISPATCHER.md" "$dst"
  adapter_translate_references "$src/references"    "$dst"
  adapter_translate_skills     "$src/skills"        "$dst"
  adapter_translate_agents     "$src/agents"        "$dst"
  adapter_translate_mcp        "$src/mcp"           "$dst"
  adapter_finalize             "$src"               "$dst"
}
