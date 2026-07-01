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

## Real-world scenarios / Skenario nyata

**📖 Remembering what you read, without extra effort**

You read an interesting article, finish a book chapter, or save a recipe — and normally it just disappears into a pile you never look at again. Instead, say *"I just read an article about [whatever it was]"* and GAIA turns it into a short, findable note connected to other things you've written — so weeks later you can actually find it again, instead of vaguely remembering "I read something about this once."

> 🇮🇩 Kamu baca artikel menarik, selesai baca satu bab buku, atau simpan resep masakan — biasanya semua itu cuma numpuk di tempat yang gak pernah kamu buka lagi. Cukup bilang *"I just read an article about [apa pun itu]"* dan GAIA mengubahnya jadi note singkat yang gampang dicari, terhubung ke hal lain yang pernah kamu tulis — jadi beberapa minggu kemudian kamu beneran bisa nemuin lagi, bukan cuma samar-samar inget "kayaknya dulu pernah baca soal ini."

**🗓️ Walking into any meeting already prepared**

Job interview, client call, or catch-up with an old colleague — say *"Prepare me for my 3pm meeting"* and GAIA pulls your calendar, digs up past notes and emails about that person, and hands you a short brief. No more scrambling five minutes before, trying to remember what you talked about last time.

> 🇮🇩 Wawancara kerja, telepon klien, atau ngobrol lagi sama kolega lama — bilang *"Prepare me for my 3pm meeting"* dan GAIA menarik kalender kamu, cari note dan email lama soal orang itu, lalu kasih ringkasan singkat. Gak perlu lagi buru-buru lima menit sebelumnya coba inget-inget obrolan terakhir kalian.

**📥 Clearing a messy pile of notes in minutes**

Your notes app is a graveyard of half-finished thoughts, quick voice memos, and links you saved "to read later" and never did. Say *"Triage my inbox"* and GAIA sorts through all of it — filing each one where it belongs — instead of you losing a Sunday afternoon to it.

> 🇮🇩 Aplikasi catatan kamu jadi kuburan pikiran setengah jadi, memo suara buru-buru, dan link yang kamu simpan "buat dibaca nanti" tapi gak pernah dibaca. Bilang *"Triage my inbox"* dan GAIA yang sortir semuanya — nyimpen tiap catatan ke tempat yang tepat — daripada kamu ngabisin satu sore hari Minggu buat beresin itu semua.

**🩺 Catching a mess before it takes over**

After months of using any note-taking system, things get messy — duplicate notes, broken links, an organization scheme that stopped matching how you actually work. Say *"Check my vault health"* and get a clear, prioritized list of what to fix — instead of discovering a year from now that it's too messy to deal with.

> 🇮🇩 Setelah berbulan-bulan pakai sistem catatan apa pun, semuanya jadi berantakan — note dobel, link putus, cara pengaturan yang udah gak sesuai lagi sama cara kerja kamu sekarang. Bilang *"Check my vault health"* dan dapatkan daftar perbaikan yang jelas dan berprioritas — daripada setahun lagi baru sadar semuanya udah terlalu berantakan buat dibereskan.

**🌐 Getting one clear answer instead of ten open tabs**

Instead of googling something and drowning in ten browser tabs trying to piece it together, ask *"Research [any topic]"* — GAIA reads around, pulls the key facts together, and saves them as one clear, organized note you can actually go back to.

> 🇮🇩 Daripada googling sesuatu dan tenggelam di sepuluh tab browser buat nyusun infonya sendiri, tanya *"Research [topik apa pun]"* — GAIA baca-baca, kumpulin fakta pentingnya, dan simpan jadi satu note yang rapi dan jelas, yang beneran bisa kamu buka lagi nanti.

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
