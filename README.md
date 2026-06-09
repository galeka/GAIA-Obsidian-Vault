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

## Quick start

### Requirements

- [Obsidian](https://obsidian.md) (free)
- One of: [Claude Code](https://claude.ai/code), [Gemini CLI](https://github.com/google-gemini/gemini-cli), [OpenCode](https://opencode.ai), [Codex CLI](https://openai.com/codex), or the AChatGPT adapter (see below)
- Git

### Install

```bash
# Clone inside your Obsidian vault
cd /path/to/your-vault
git clone https://github.com/galeka/gaia-obsidian.git GAIA
cd GAIA

# Install into your vault
bash scripts/launchme.sh
```

Select your platform when prompted. The installer copies agents, skills, hooks, and references into the platform directory (`.claude/`, `.gemini/`, etc.) and creates the dispatcher file at the vault root.

### Initialize

Open your agent platform inside the vault folder, then say:

> **"Initialize my vault"**

The `/onboarding` skill starts a conversation to build your vault structure, save your profile, and configure integrations.

### Update

```bash
cd /path/to/your-vault/GAIA
git pull
bash scripts/updateme.sh
```

Your vault notes are never touched.

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

| Platform | Install |
|----------|---------|
| Claude Code | [claude.ai/code](https://claude.ai/code) |
| Gemini CLI | [github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) |
| OpenCode | [opencode.ai](https://opencode.ai) |
| Codex CLI | `npm i -g @openai/codex` |
| AChatGPT | See adapter above |

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
| Agent doesn't activate | Open the platform inside the vault folder, not a different directory |
| Email / Calendar not working | See `docs/gws-setup-guide.md` for GWS setup |
| `401 Unauthorized` (AChatGPT) | Check `ACHATGPT_API_KEY` in `.env` |
| `429 Too Many Requests` | Quota exceeded — check AChatGPT dashboard |
| Timeout on o3 | Set `ACHATGPT_REQUEST_TIMEOUT=90` in `.env` |
| Vault structure looks unexpected | The Architect customizes structure during onboarding — say "show my vault structure" |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The short version: open an issue, improve an agent or skill, add usage examples. All agents auto-respond in the user's language — write instructions in English.

---

## License

MIT. Credentials (`.env`) are gitignored and must never be committed.
