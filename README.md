# 🧠 GAIA — Graph-Augmented Intelligence Agent for Obsidian

[![Agents](https://img.shields.io/badge/Agents-11-d29922?style=flat-square)](https://github.com/galeka/GAIA-Obsidian-Vault)
[![Skills](https://img.shields.io/badge/Skills-19-a371f7?style=flat-square)](https://github.com/galeka/GAIA-Obsidian-Vault)
[![Platforms](https://img.shields.io/badge/Platforms-5-388bfd?style=flat-square)](https://github.com/galeka/GAIA-Obsidian-Vault)
[![License](https://img.shields.io/badge/License-MIT-3fb950?style=flat-square)](LICENSE)

> Talk to your Obsidian vault like you're talking to an assistant.  
> GAIA listens, thinks, then acts — no clicking, no dashboards.

> Bicara ke vault Obsidian kamu seperti ngobrol dengan asisten.  
> GAIA mendengarkan, berpikir, lalu melakukan — tanpa klik, tanpa dashboard.

---

## How it works / Cara kerjanya

```
You speak  →  GAIA routes  →  Agent runs  →  Vault updated
Kamu bicara   GAIA routing   Agent bekerja   Vault diupdate
```

**11 agents** that activate automatically + **19 skills** triggered by natural conversation — powered by Claude, Gemini, GPT-4o, or any supported AI platform.

---

## What can it do? / Apa yang bisa dilakukan?

| Just say... / Cukup katakan... | What happens / Yang terjadi |
|-------------------------------|----------------------------|
| *"Do my daily review"* | Opens today's note, pulls calendar, asks for focus items |
| *"I just read an article about X"* | Turns it into a linked Zettelkasten note |
| *"What's on my plate this week?"* | Combines calendar + email + vault tasks into one view |
| *"Triage my inbox"* | Classifies and routes all inbox notes automatically |
| *"Check my vault health"* | Full structural audit with recommendations |
| *"Prepare me for my 3pm meeting"* | Pulls participant context, past notes, related emails |
| *"What are my deadlines?"* | Unified timeline grouped by urgency |
| *"Create a new agent for X"* | Builds a custom agent via guided conversation |

---

## The crew / Anggota tim

### 🤖 11 Agents — reactive, one-shot

| | Agent | Role |
|-|-------|------|
| 🏛️ | **Architect** | Vault structure, areas, templates, MOCs |
| ✍️ | **Scribe** | Fast capture → clean Obsidian notes |
| 📂 | **Sorter** | Batch sorting and priority triage |
| 🔍 | **Seeker** | Search and knowledge retrieval |
| 🔗 | **Connector** | Knowledge graph, link analysis, contradiction detection |
| 📚 | **Librarian** | Vault health checks and analytics |
| 🎙️ | **Transcriber** | Audio and meeting transcription |
| 📬 | **Postman** | Gmail and Google Calendar |
| 🌐 | **Researcher** | 3-round web research → structured vault note |
| 🪶 | **Lark-Sync** | Sync Lark messages, tasks, and calendar |
| 🔧 | **Prompt-Optimizer** | Audit and optimize agent/skill trigger descriptions |

### ⚡ 19 Skills — multi-turn workflows

`/onboarding` · `/daily-review` · `/weekly-agenda` · `/inbox-triage` · `/reading-digest` · `/zettel-builder` · `/vault-audit` · `/deadline-radar` · `/meeting-prep` · `/email-triage` · `/transcribe` · `/defrag` · `/deep-clean` · `/tag-garden` · `/batch-ingest` · `/create-agent` · `/manage-agent` · `/contact-sync` · `/vault-security-audit`

You don't need to type the skill name — just speak naturally and GAIA routes automatically.  
*(Tidak perlu ketik nama skill — bicara natural, GAIA routing otomatis.)*

---

## Supported platforms / Platform yang didukung

| Platform | macOS | Windows |
|----------|:-----:|:-------:|
| **Claude Code** ⭐ | ✅ | ✅ |
| **Gemini CLI** | ✅ | ✅ via WSL |
| **OpenCode** | ✅ | ✅ via WSL |
| **Codex CLI** | ✅ | ✅ via WSL |
| **AChatGPT** (GPT-4o/o3) | ✅ | ✅ via WSL |

---

## Installation / Instalasi

Choose your language for the full installation guide:

> 📖 **[Installation Guide — English](INSTALL.md)**

> 📖 **[Panduan Instalasi — Bahasa Indonesia](INSTALL.id.md)**

**Quick start (4 steps):**
```bash
# 1. Install Obsidian → obsidian.md
# 2. Install Claude Code → claude.ai/code  (or another platform)
# 3. Clone GAIA into your vault folder
git clone https://github.com/galeka/GAIA-Obsidian-Vault.git GAIA
cd GAIA && bash scripts/launchme.sh
# 4. Open your vault and say: "Initialize my vault"
```

---

## Optional integrations / Integrasi opsional

- **GPT-4o / o3** — use OpenAI models via the AChatGPT adapter (`adapters/AchatGPT/`)
- **Lark / Feishu** — sync messages, tasks, and calendar via FastMCP (`mcp/lark-mcp-server.py`)

---

## Update

```bash
cd your-vault/GAIA
git pull && bash scripts/updateme.sh
```

Your notes are never touched by updates. / Note vault kamu tidak pernah disentuh oleh update.

---

<div align="center">

Built with ❤️ for a second brain that actually thinks.  
*Dibuat dengan ❤️ untuk second brain yang benar-benar berpikir.*

**[⭐ Star this repo](https://github.com/galeka/GAIA-Obsidian-Vault)**

</div>
