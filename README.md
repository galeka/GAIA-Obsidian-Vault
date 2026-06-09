# GAIA — Graph-Augmented Intelligence Agent for Obsidian

> An AI crew that manages your Obsidian vault through natural conversation. 9 agents, 17 skills, built on the Zettelkasten method and P.A.R.A. organization — with optional AChatGPT backend (GPT-4o, o3) and Lark integration.

---

## What is GAIA?

GAIA is a multi-agent system that lives inside your Obsidian vault. You talk to it; it delegates to the right agent or skill. No UI, no dashboards — just conversation.

The core philosophy: **your vault should think with you, not just store things for you.** Every agent is designed around the Zettelkasten principle that knowledge grows through connection, not accumulation.

---

## The Crew

### 9 Agents

Agents handle reactive, single-shot operations. They activate automatically based on what you say.

| Agent | Role |
|-------|------|
| **Architect** | Vault structure, areas, templates, MOCs |
| **Scribe** | Fast text capture → clean Obsidian notes |
| **Sorter** | Batch sort, priority triage, project pulse |
| **Seeker** | Vault search and knowledge retrieval |
| **Connector** | Knowledge graph, link analysis, Zettelkasten intelligence |
| **Librarian** | Vault health checks, consistency, analytics |
| **Transcriber** | Audio and meeting transcription |
| **Postman** | Email (Gmail / Hey.com) and Google Calendar |
| **Lark Sync** | Sync Lark messages, tasks, docs, and calendar into vault notes |

### 17 Skills

Skills are multi-turn conversational workflows. Say the trigger phrase and the skill takes over.

| # | Skill | What it does |
|---|-------|-------------|
| 1 | `/onboarding` | First-time vault setup — guided conversation creates your full structure |
| 2 | `/create-agent` | Build a custom agent via 6-phase interview |
| 3 | `/manage-agent` | Edit, update, or remove custom agents |
| 4 | `/defrag` | Weekly structural audit: inbox hygiene, areas, MOCs, tags |
| 5 | `/email-triage` | Scan inbox, score by priority, save actionable emails as notes |
| 6 | `/meeting-prep` | Pull participant context, past notes, and emails before a meeting |
| 7 | `/weekly-agenda` | Day-by-day week view combining calendar + email + vault tasks |
| 8 | `/deadline-radar` | Unified deadline timeline grouped by urgency |
| 9 | `/transcribe` | Process recordings and transcripts into structured notes |
| 10 | `/vault-audit` | Full 7-phase vault health audit |
| 11 | `/deep-clean` | Extended cleanup: stale content, broken refs, template compliance |
| 12 | `/tag-garden` | Tag hygiene: orphans, duplicates, unused, over-used |
| 13 | `/inbox-triage` | Classify, route, update MOCs, and extract actions from all inbox notes |
| 14 | `/contact-sync` | Sync a person to Apple Contacts |
| 15 | `/daily-review` | Morning note + focus items, EOD reflection, action item extraction |
| 16 | `/reading-digest` | Turn articles and papers into atomic Zettelkasten notes with ICM assessment |
| 17 | `/zettel-builder` | Guided permanent note creation: atomic, linked, ICM-complete |

---

## Zettelkasten intelligence

The Connector agent goes beyond basic link analysis. It classifies every note in the vault and surfaces the health of your knowledge graph:

**Hub / Branch / Leaf classification** — notes are scored by link density. Hubs (5+ links) are your knowledge anchors. Leaves (0-1 links) are flagged for upgrade.

**ICM completeness audit** — every permanent note is checked for all three layers: Information (the fact), Context (why it matters to you), and Meaning (the "so what"). Notes stuck at `[Info-only]` get specific upgrade prompts.

**Evergreen scoring** — notes are scored 0-5 on atomicity, own-words writing, ICM completeness, link count, and incoming links. Your true evergreens rise to the top.

**Typed link suggestion** — when a new note is created, the Connector finds related notes and labels each connection: *Supports*, *Contradicts*, *Applies*, *Extends*, or *Origin*.

**MOC gap detection** — when 3+ permanent notes share a topic with no Map of Content, the Connector flags it and asks the Architect to create one.

The three Zettelkasten skills complete the loop:

- `/reading-digest` — raw article → Literature Note → Permanent Note → ICM label → vault links
- `/zettel-builder` — one rough idea → 9-phase guided conversation → full ICM permanent note
- `/daily-review` — morning note → focus items → EOD reflection → action items to inbox

---

## Installation

### Requirements

- [Obsidian](https://obsidian.md) (free)
- One supported agent platform: [Claude Code](https://claude.ai/code), [Gemini CLI](https://github.com/google-gemini/gemini-cli), [OpenCode](https://opencode.ai), or [Codex CLI](https://openai.com/codex)
- Git

---

### macOS

#### Step 1 — Install Obsidian

1. Go to [obsidian.md](https://obsidian.md) and download the macOS `.dmg`
2. Open the `.dmg`, drag Obsidian into **Applications**, then open it
3. Click **Create new vault**, give it a name (e.g. `MyBrain`), and pick a location
4. Note the full path — you'll need it in the next steps

#### Step 2 — Install Git

Open **Terminal** (`Command + Space` → type "Terminal" → Enter) and run:

```bash
git --version
```

If Git is not installed, macOS will offer to install Xcode Command Line Tools automatically — click **Install** and wait. Verify with `git --version` again.

#### Step 3 — Install an agent platform

Pick one and install it:

| Platform | How to install |
|----------|---------------|
| **Claude Code** (recommended) | Download from [claude.ai/code](https://claude.ai/code) |
| **Gemini CLI** | `npm install -g @google/gemini-cli` |
| **OpenCode** | `npm install -g opencode-ai` |
| **Codex CLI** | `npm install -g @openai/codex` |

> **Node.js required for npm-based platforms.** Install it from [nodejs.org](https://nodejs.org) (LTS version). Verify with `node --version`.

#### Step 4 — Install GAIA

In Terminal, navigate to your vault folder:

```bash
# Replace the path with your actual vault location
cd ~/Documents/MyBrain
```

Clone the repo and run the installer:

```bash
git clone https://github.com/galeka/gaia-obsidian.git GAIA
cd GAIA
bash scripts/launchme.sh
```

The installer will ask which platform you use. Select it and it copies all agents, skills, hooks, and references into the correct directory (`.claude/`, `.gemini/`, etc.).

#### Step 5 — Initialize your vault

Open your agent platform **from inside your vault folder**:

```bash
# Navigate to your vault first — this is important
cd ~/Documents/MyBrain

# Then launch your platform:
claude        # Claude Code
gemini        # Gemini CLI
opencode      # OpenCode
codex         # Codex CLI
```

Then say:

> **"Initialize my vault"**

The `/onboarding` skill starts a guided conversation to build your folder structure, save your profile, and configure integrations.

#### Step 6 — Daily usage example

```
You:  "Do my daily review"
GAIA: [opens today's note, pulls calendar, asks for focus items]

You:  "I just read an article about zero-trust security"
GAIA: [runs /reading-digest → creates literature note → links to related zettels]

You:  "Triage my inbox"
GAIA: [classifies all notes in 00-Inbox/, routes them, updates MOCs]
```

#### Step 7 — Update GAIA

```bash
cd ~/Documents/MyBrain/GAIA
git pull
bash scripts/updateme.sh
```

Your vault notes are never touched by updates.

---

### Windows

> Windows support requires [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install) (Windows Subsystem for Linux) for all platforms except Claude Code, which runs natively. All terminal commands below run inside WSL unless noted otherwise.

#### Step 1 — Install WSL 2

Open **PowerShell as Administrator** (Start → search "PowerShell" → right-click → *Run as administrator*):

```powershell
wsl --install
```

Restart your computer when prompted. After restart, WSL will finish installing Ubuntu and ask you to create a Linux username and password. Remember these.

Verify:

```powershell
wsl --version
```

#### Step 2 — Install Obsidian

1. Go to [obsidian.md](https://obsidian.md) and download the Windows installer (`.exe`)
2. Run the installer and open Obsidian
3. Click **Create new vault**, name it (e.g. `MyBrain`), and save it somewhere easy to find — e.g. `C:\Users\YourName\Documents\MyBrain`
4. Note the full path — you'll need it

#### Step 3 — Install Git (inside WSL)

Open the **WSL terminal** (Start → search "Ubuntu" or "WSL") and run:

```bash
sudo apt update && sudo apt install git -y
git --version
```

#### Step 4 — Install an agent platform

**Option A: Claude Code — native Windows (no WSL needed)**

Download and install from [claude.ai/code](https://claude.ai/code). Claude Code runs natively on Windows and includes a desktop app (Cowork mode). You can skip WSL entirely if you only use Claude Code.

**Option B: Gemini CLI / OpenCode / Codex CLI — via WSL**

Inside WSL, install Node.js:

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
node --version   # should print v20.x or higher
```

Then install your chosen platform:

```bash
# Gemini CLI
npm install -g @google/gemini-cli

# OpenCode
npm install -g opencode-ai

# Codex CLI
npm install -g @openai/codex
```

#### Step 5 — Install GAIA

Inside WSL, navigate to your vault. Windows drives are mounted at `/mnt/c/`, `/mnt/d/`, etc.:

```bash
# Replace YourName and MyBrain with your actual values
cd /mnt/c/Users/YourName/Documents/MyBrain
```

Clone and install:

```bash
git clone https://github.com/galeka/gaia-obsidian.git GAIA
cd GAIA
bash scripts/launchme.sh
```

Select your platform when prompted.

> **Claude Code on Windows (native, no WSL):**
> Install [Git for Windows](https://git-scm.com) first, then open **Git Bash** (right-click in your vault folder → *Git Bash Here*):
> ```bash
> git clone https://github.com/galeka/gaia-obsidian.git GAIA
> cd GAIA
> bash scripts/launchme.sh
> ```

#### Step 6 — Initialize your vault

**WSL (Gemini CLI / OpenCode / Codex CLI):**

```bash
# Navigate to your vault first — this is important
cd /mnt/c/Users/YourName/Documents/MyBrain

# Then launch your platform:
gemini        # Gemini CLI
opencode      # OpenCode
codex         # Codex CLI
```

**Claude Code (native Windows):**

Open the Claude desktop app, or navigate to your vault in Command Prompt / PowerShell and run `claude`.

Then say:

> **"Initialize my vault"**

#### Step 7 — Daily usage example

```
You:  "What's on my plate this week?"
GAIA: [runs /weekly-agenda → pulls calendar + email + vault tasks]

You:  "Build a zettel about the concept I just read"
GAIA: [runs /zettel-builder → 9-phase guided note creation]

You:  "Check my vault health"
GAIA: [runs /vault-audit → full 7-phase structural report]
```

#### Step 8 — Update GAIA

```bash
# In WSL
cd /mnt/c/Users/YourName/Documents/MyBrain/GAIA
git pull
bash scripts/updateme.sh
```

---

## First conversation — quick reference

After initialization, try these phrases to explore what GAIA can do:

| Say this... | GAIA does this |
|-------------|---------------|
| "Initialize my vault" | `/onboarding` — full vault setup |
| "Do my daily review" | `/daily-review` — morning note + focus items |
| "What's on my plate this week?" | `/weekly-agenda` — week overview |
| "Triage my inbox" | `/inbox-triage` — route and classify inbox notes |
| "I just read an article about X" | `/reading-digest` — article → atomic Zettel |
| "Build a zettel about [idea]" | `/zettel-builder` — guided permanent note |
| "Check my vault health" | `/vault-audit` — structural audit |
| "What are my deadlines?" | `/deadline-radar` — unified deadline view |
| "Prepare me for my 3pm meeting" | `/meeting-prep` — participant context + notes |
| "Create a new agent for X" | `/create-agent` — custom agent builder |

You don't need to type the skill name — just speak naturally and GAIA routes to the right agent or skill automatically.

---

## AChatGPT backend (optional)

Use GPT-4o or o3 instead of Claude / Gemini to run the crew.

```bash
cp adapters/AchatGPT/.env.example adapters/AchatGPT/.env
# Set ACHATGPT_API_KEY and optionally VAULT_ROOT

chmod +x adapters/AchatGPT/achat.sh
cd adapters/AchatGPT
./achat.sh "Initialize my vault"
```

| Tier | Model |
|------|-------|
| `low` | gpt-4o-mini |
| `mid` | gpt-4o |
| `high` | o3 |

Override: `ACHATGPT_MODEL=gpt-4o ./achat.sh "..."`

---

## Lark integration (optional)

The `lark-sync` agent pulls Lark messages, documents, tasks, and calendar events into your vault. The `gaia-lark-bot.py` bot lets your Lark workspace trigger vault operations directly.

```bash
pip install flask python-dotenv requests
python adapters/AchatGPT/gaia-lark-bot.py
```

Set `LARK_APP_ID`, `LARK_APP_SECRET`, and `LARK_BOT_ID` in `.env`. Configure the webhook in your Lark console.

Trigger: *"sync from Lark"*, *"Lark calendar"*, *"save Lark meeting notes"*

---

## Supported platforms

| Platform | Install | macOS | Windows |
|----------|---------|-------|---------|
| Claude Code | [claude.ai/code](https://claude.ai/code) | ✅ Native | ✅ Native |
| Gemini CLI | [github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | ✅ Native | ✅ Via WSL |
| OpenCode | [opencode.ai](https://opencode.ai) | ✅ Native | ✅ Via WSL |
| Codex CLI | `npm i -g @openai/codex` | ✅ Native | ✅ Via WSL |
| AChatGPT | See adapter above | ✅ Native | ✅ Via WSL |

---

## Project structure

```
GAIA/
├── agents/                   9 agents
├── skills/                   17 skills
├── adapters/
│   ├── AchatGPT/             AChatGPT backend + Lark bot
│   ├── claude-code/
│   ├── gemini-cli/
│   ├── opencode/
│   └── codex-cli/
├── references/               Shared docs read by agents at runtime
├── hooks/                    Vault protection and validation hooks
├── docs/                     User-facing documentation
├── scripts/
│   ├── launchme.sh           First-time installer
│   └── updateme.sh           Post-pull updater
├── mcp/servers.yaml          MCP server definitions
└── DISPATCHER.md             Routing rules (platform-neutral source)
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Agent doesn't activate | Open the platform **inside the vault folder** — not a different directory |
| `bash: command not found` on Windows | Use Git Bash or WSL — don't run bash scripts in vanilla PowerShell/CMD |
| `Permission denied` on launchme.sh | Run `chmod +x scripts/launchme.sh` first |
| WSL can't find vault path | Windows drives are at `/mnt/c/`, `/mnt/d/` etc. in WSL |
| Node not found in WSL | Run `sudo apt install nodejs npm -y` or use the nodesource script above |
| Email / Calendar not working | See `docs/gws-setup-guide.md` for GWS setup |
| `401 Unauthorized` (AChatGPT) | Check `ACHATGPT_API_KEY` in `.env` |
| `429 Too Many Requests` | Quota exceeded — check your API dashboard |
| Timeout on o3 | Set `ACHATGPT_REQUEST_TIMEOUT=90` in `.env` |
| Vault structure looks unexpected | Say "show my vault structure" — the Architect will explain it |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The short version: open an issue, improve an agent or skill, add usage examples. All agents auto-respond in the user's language — write instructions in English.

---

## License

MIT. Credentials (`.env`) are gitignored and must never be committed.
