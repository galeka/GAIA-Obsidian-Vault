#!/usr/bin/env python3
"""
adapters/achatgpt/vault-chat.py — Chat with your Obsidian vault via AChatGPT.

Usage:
    export ACHATGPT_API_KEY="..."
    export VAULT_ROOT="/path/to/vault"   # defaults to current directory
    python vault-chat.py "What projects do I have?"

Requires: Python 3.8+, no external packages.
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path


# ── Config ─────────────────────────────────────────────────────────────────────

PROXY_URL  = os.environ.get("ACHATGPT_PROXY_URL", "https://your-proxy-url.workers.dev")
API_KEY    = os.environ.get("ACHATGPT_API_KEY", "")
MODEL      = os.environ.get("ACHATGPT_MODEL", "gpt-5.4")
VAULT_ROOT = Path(os.environ.get("VAULT_ROOT", ".")).resolve()
TIMEOUT    = int(os.environ.get("ACHATGPT_REQUEST_TIMEOUT", "60"))
RETRIES    = int(os.environ.get("ACHATGPT_RETRY_ATTEMPTS", "3"))
MAX_ITER   = 10

SYSTEM_PROMPT = f"""You are a personal knowledge assistant with full read/write access \
to the user's Obsidian vault at: {VAULT_ROOT}

Available tools:
- read_file: read any note by path
- list_files: list files in any directory
- search_vault: full-text search across all notes
- write_file: create or update notes

Guidelines:
- Use tools to gather context before answering
- Quote relevant passages from notes when helpful
- When writing new notes, use Obsidian markdown with YAML frontmatter
- Be concise and specific"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the full contents of a file in the Obsidian vault.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path from vault root (e.g. 01-Projects/note.md)"}
                },
                "required": ["path"],
            },
        },
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
                    "pattern":   {"type": "string", "description": "Filename glob pattern (default: *.md)"},
                },
                "required": ["directory"],
            },
        },
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
                    "file_pattern": {"type": "string", "description": "Limit to files matching this glob (default: *.md)"},
                },
                "required": ["query"],
            },
        },
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
                    "content": {"type": "string", "description": "Full file content to write"},
                },
                "required": ["path", "content"],
            },
        },
    },
]


# ── HTTP client ────────────────────────────────────────────────────────────────

def _api_call(endpoint: str, payload: dict) -> dict:
    url  = PROXY_URL.rstrip("/") + endpoint
    data = json.dumps(payload).encode()
    req  = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization":  f"Bearer {API_KEY}",
            "Content-Type":   "application/json",
            "x-api-type":     "openai",
            "User-Agent":     "curl/7.88.1",
        },
        method="POST",
    )
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            if e.code in (429, 502, 503) and attempt < RETRIES - 1:
                wait = 2 ** (attempt + 1)
                print(f"[AChatGPT] HTTP {e.code} — retrying in {wait}s ({attempt+1}/{RETRIES})", file=sys.stderr)
                time.sleep(wait)
                continue
            raise RuntimeError(f"HTTP {e.code}: {body}") from e
    raise RuntimeError("Max retries exceeded")


# ── Tool execution ─────────────────────────────────────────────────────────────

def _execute_tool(name: str, args: dict) -> str:
    if name == "read_file":
        path = VAULT_ROOT / args["path"]
        if path.is_file():
            return path.read_text(encoding="utf-8", errors="replace")
        return f"ERROR: file not found: {args['path']}"

    if name == "list_files":
        directory = VAULT_ROOT / args.get("directory", "")
        pattern   = args.get("pattern", "*.md")
        if not directory.is_dir():
            return f"ERROR: directory not found: {args.get('directory')}"
        files = sorted(directory.rglob(pattern))
        rel   = [str(f.relative_to(VAULT_ROOT)) for f in files]
        return "\n".join(rel) if rel else "(no files found)"

    if name == "search_vault":
        query       = args["query"]
        file_pat    = args.get("file_pattern", "*.md")
        results     = []
        try:
            pattern = re.compile(query, re.IGNORECASE)
        except re.error:
            pattern = re.compile(re.escape(query), re.IGNORECASE)
        for f in sorted(VAULT_ROOT.rglob(file_pat)):
            try:
                for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                    if pattern.search(line):
                        rel = f.relative_to(VAULT_ROOT)
                        results.append(f"{rel}:{i}: {line.strip()}")
                        if len(results) >= 60:
                            break
            except OSError:
                continue
            if len(results) >= 60:
                break
        return "\n".join(results) if results else "(no matches)"

    if name == "write_file":
        path    = VAULT_ROOT / args["path"]
        content = args["content"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Written: {args['path']}"

    return f"ERROR: unknown tool: {name}"


# ── Agentic loop ───────────────────────────────────────────────────────────────

def run_agent(user_message: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": user_message},
    ]

    for iteration in range(MAX_ITER):
        response = _api_call("/chat/completions", {
            "model":       MODEL,
            "messages":    messages,
            "tools":       TOOLS,
            "tool_choice": "auto",
            "stream":      False,
        })

        choice       = response["choices"][0]
        finish       = choice["finish_reason"]
        asst_message = choice["message"]
        messages.append(asst_message)

        if finish == "stop":
            return asst_message.get("content", "")

        if finish == "tool_calls":
            for call in asst_message.get("tool_calls", []):
                tool_name = call["function"]["name"]
                tool_args = json.loads(call["function"]["arguments"])
                print(f"[tool: {tool_name}]", file=sys.stderr)
                result = _execute_tool(tool_name, tool_args)
                messages.append({
                    "role":         "tool",
                    "tool_call_id": call["id"],
                    "content":      result,
                })
        else:
            raise RuntimeError(f"Unexpected finish_reason: {finish}")

    raise RuntimeError(f"Max iterations ({MAX_ITER}) reached")


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} "<your question>"')
        sys.exit(1)

    if not API_KEY:
        print("ERROR: ACHATGPT_API_KEY not set.")
        sys.exit(1)

    print(f"Vault: {VAULT_ROOT}", file=sys.stderr)
    print(f"Model: {MODEL}",      file=sys.stderr)
    print("---",                   file=sys.stderr)

    answer = run_agent(" ".join(sys.argv[1:]))
    print(answer)
