# Lark Integration Setup Guide

This guide shows how to connect GAIA to Lark so the `lark-sync` agent can pull messages, documents, tasks, and calendar events into your vault.

---

## Security model

Credentials follow this priority chain (highest wins):

```
System environment variables  ←  recommended
        ↓ fallback
   .env file (vault root)     ←  local convenience, gitignored
        ↓ fallback
  LARK_API_TOKEN direct        ←  advanced / short-lived use only
```

**Never hardcode credentials in any file that touches git.** The `.env` file is already in `.gitignore` and safe to use locally, but system env vars are the cleanest option.

---

## Step 1 — Create a Lark app

1. Go to [open.larksuite.com/app](https://open.larksuite.com/app) (or [open.feishu.cn/app](https://open.feishu.cn/app) for China edition)
2. Click **Create App → Custom App**
3. Give it a name (e.g. *GAIA Vault Sync*)
4. Under **Permissions & Scopes**, add the minimum required scopes:

| Scope | Purpose |
|-------|---------|
| `im:message` | Read channel messages |
| `drive:drive:readonly` | Read documents |
| `task:task:readonly` | Read tasks |
| `calendar:calendar:readonly` | Read calendar events |
| `contact:user.base:readonly` | Resolve user names |

5. Publish the app to your workspace (Admin approval may be needed)
6. Copy your **App ID** and **App Secret** from the *Credentials & Basic Info* page

> **Principle of least privilege:** Only add the scopes you actually need. If you don't sync tasks, don't add `task:task:readonly`.

---

## Step 2 — Set credentials

### Option A — System environment variables (recommended)

Credentials never touch the filesystem. Set once, persist across reboots.

**Windows (PowerShell, permanent):**
```powershell
[System.Environment]::SetEnvironmentVariable("LARK_APP_ID", "cli_xxxxxxxx", "User")
[System.Environment]::SetEnvironmentVariable("LARK_APP_SECRET", "xxxxxxxxxxxxxxxx", "User")
```
Restart your terminal after setting. Verify with:
```powershell
echo $env:LARK_APP_ID
```

**macOS / Linux (permanent, add to shell profile):**
```bash
# Add to ~/.zshrc or ~/.bashrc
export LARK_APP_ID="cli_xxxxxxxx"
export LARK_APP_SECRET="xxxxxxxxxxxxxxxx"
```
Then run `source ~/.zshrc` (or open a new terminal).

**WSL (Windows Subsystem for Linux):**
```bash
# Add to ~/.bashrc inside WSL
export LARK_APP_ID="cli_xxxxxxxx"
export LARK_APP_SECRET="xxxxxxxxxxxxxxxx"
```

---

### Option B — .env file (local fallback)

Good for a single machine where you don't want to touch shell config.

```bash
# In your vault root, copy the template:
cp .env.example .env
```

Edit `.env`:
```
LARK_APP_ID=cli_xxxxxxxx
LARK_APP_SECRET=xxxxxxxxxxxxxxxx
```

The `.env` file is already in `.gitignore` — it will never be committed.

> **Note:** System env vars always win over `.env`. If both exist, the system var is used.

---

### Option C — China edition (Feishu)

If your organization uses Feishu (the China version of Lark):
```bash
export LARK_API_BASE="https://open.feishu.cn"
```
Or add to `.env`:
```
LARK_API_BASE=https://open.feishu.cn
```

---

## Step 3 — Install Python dependencies

```bash
pip install fastmcp httpx pydantic python-dotenv
```

Or with the full dependency spec:
```bash
pip install "fastmcp>=0.1" "httpx[http2]>=0.24" "pydantic>=2.0" "python-dotenv>=1.0"
```

---

## Step 4 — Register the MCP server with Claude

Run this once to register the Lark MCP server:

```bash
# From your vault root
claude mcp add lark-mcp python3 mcp/lark-mcp-server.py
```

Verify it registered:
```bash
claude mcp list
```

You should see `lark-mcp` in the list.

---

## Step 5 — Test the connection

Start a Claude Code session in your vault, then say:

> "Sync from Lark — just check the connection, don't import anything yet"

The `lark-sync` agent will verify MCP access and report whether credentials are valid.

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `LARK_APP_ID and LARK_APP_SECRET must be set` | Env vars not found | Check Step 2; restart terminal after setting vars |
| `Lark auth error: code=10003` | App ID or Secret is wrong | Re-copy from Lark developer console |
| `Lark auth error: code=10014` | App not published to workspace | Publish the app in Lark developer console |
| `HTTP 403` on message fetch | Missing `im:message` scope | Add scope in Lark console and republish |
| `HTTP 403` on document fetch | Missing `drive:drive:readonly` | Add scope and republish |
| `ModuleNotFoundError: fastmcp` | Dependencies not installed | Run pip install command from Step 3 |
| `python3: command not found` | Python not in PATH | Use full path: `python` or `python3.11` |

---

## Security checklist

- [ ] `.env` is in `.gitignore` (already done in this repo)
- [ ] `.lark_tokens.json` is in `.gitignore` (already done)
- [ ] App has **only** the scopes it needs (principle of least privilege)
- [ ] App credentials are stored in env vars or `.env`, never in agent files
- [ ] Never paste credentials into a chat session (they would appear in history)
- [ ] Rotate App Secret every 90 days (Lark developer console → Credentials → Reset Secret)
- [ ] If you suspect a leak: rotate immediately in the Lark console, then update your env vars

---

## Rotating credentials

When you need to rotate your App Secret:

1. Go to [open.larksuite.com/app](https://open.larksuite.com/app) → your app → *Credentials & Basic Info*
2. Click **Reset App Secret** → copy the new value
3. Update the env var:

**Windows:**
```powershell
[System.Environment]::SetEnvironmentVariable("LARK_APP_SECRET", "new_secret_here", "User")
```

**macOS/Linux:**
```bash
# Edit ~/.zshrc or ~/.bashrc, update the export line, then:
source ~/.zshrc
```

**`.env` file:**
```bash
# Just edit .env and update the LARK_APP_SECRET line
```

4. Restart Claude Code — the new secret takes effect immediately on next server start.

---

## What lark-sync can fetch

| Feature | Trigger phrase |
|---------|---------------|
| Channel messages | "sync Lark messages from [channel]" |
| Documents | "sync Lark docs from [space]" |
| Open tasks | "sync my Lark tasks" |
| Calendar events | "sync Lark calendar this week" |
| Meeting notes | Fetched automatically with calendar events |
| Keyword search | "search Lark for [topic]" |

All synced items land in `00-Inbox/` for review. Run `/inbox-triage` after a sync to file them properly.
