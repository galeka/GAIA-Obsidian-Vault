# 🧠 GAIA — Graph-Augmented Intelligence Agent for Obsidian

<div align="right">

🌐 **Bahasa:** [English](README.md) | Bahasa Indonesia

</div>

> **Bicara ke vault Obsidian kamu seperti ngobrol dengan asisten.**  
> GAIA mendengarkan, berpikir, lalu melakukan — tanpa klik, tanpa dashboard.

[![Agents](https://img.shields.io/badge/Agents-11-d29922?style=flat-square)](https://github.com/galeka/GAIA-Obsidian-Vault)
[![Skills](https://img.shields.io/badge/Skills-19-a371f7?style=flat-square)](https://github.com/galeka/GAIA-Obsidian-Vault)
[![Platforms](https://img.shields.io/badge/Platforms-5-388bfd?style=flat-square)](https://github.com/galeka/GAIA-Obsidian-Vault)
[![License](https://img.shields.io/badge/License-MIT-3fb950?style=flat-square)](LICENSE)

---

## ⚡ Cara Kerjanya

```
Kamu bicara natural  →  GAIA routing  →  Agent bekerja  →  Vault diupdate
"Do my daily review"   pilih skill       proses otomatis   note siap pakai
```

**Filosofi inti:** vault kamu seharusnya *berpikir bersama kamu*, bukan sekadar menyimpan. Setiap agent dirancang berdasarkan prinsip Zettelkasten — pengetahuan tumbuh melalui koneksi, bukan akumulasi.

---

## 🏗️ Arsitektur Sistem

```
                        ┌─────────────────────────────────┐
                        │          🧠 GAIA Core            │
  👤 Kamu  ◄──────────► │     routes & orchestrates        │ ◄──────────► 🗂️ Obsidian Vault
  (natural language)     └────────────┬────────────────────┘              (second brain kamu)
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
        🤖 10 Agents            ⚡ 18 Skills          🔌 Integrasi
        (reaktif, sekali jalan) (workflow multi-turn)  Gmail · Calendar
                                                        Web · Lark · GPT-4o
```

---

## 🤖 11 Agents

Aktif otomatis berdasarkan apa yang kamu katakan — tidak perlu memilih secara manual.

| Agent | Fungsi |
|-------|--------|
| 🏛️ **Architect** | Struktur vault, area, template, Maps of Content |
| ✍️ **Scribe** | Capture cepat → note Obsidian yang bersih |
| 📂 **Sorter** | Sortir massal, triage prioritas, project pulse |
| 🔍 **Seeker** | Pencarian vault dan pengambilan knowledge |
| 🔗 **Connector** | Graf pengetahuan, analisis link, deteksi kontradiksi |
| 📚 **Librarian** | Health check vault, konsistensi, analitik |
| 🎙️ **Transcriber** | Transkripsi audio dan meeting |
| 📬 **Postman** | Email (Gmail) dan Google Calendar |
| 🌐 **Researcher** | Riset web otonom 3-round → note terstruktur dengan sitasi |
| 🪶 **Lark-Sync** | Sync pesan, dokumen, tugas, dan event kalender Lark ke vault |
| 🔧 **Prompt-Optimizer** | Audit dan optimasi trigger description agents/skills |

---

## ⚡ 19 Skills

Skills adalah workflow percakapan multi-giliran. **Tidak perlu ketik nama skill** — ucapkan saja secara natural dan GAIA akan routing sendiri.

| # | Skill | Cukup katakan... |
|---|-------|-----------------|
| 1 | `/onboarding` | *"Initialize my vault"* |
| 2 | `/daily-review` | *"Do my daily review"* |
| 3 | `/weekly-agenda` | *"What's on my plate this week?"* |
| 4 | `/inbox-triage` | *"Triage my inbox"* |
| 5 | `/reading-digest` | *"I just read an article about X"* |
| 6 | `/zettel-builder` | *"Build a zettel about [idea]"* |
| 7 | `/vault-audit` | *"Check my vault health"* |
| 8 | `/deadline-radar` | *"What are my deadlines?"* |
| 9 | `/meeting-prep` | *"Prepare me for my 3pm meeting"* |
| 10 | `/email-triage` | *"Triage my email inbox"* |
| 11 | `/transcribe` | *"Transcribe this recording"* |
| 12 | `/defrag` | *"Run a vault defrag"* |
| 13 | `/deep-clean` | *"Deep clean my vault"* |
| 14 | `/tag-garden` | *"Fix my tags"* |
| 15 | `/batch-ingest` | *"Process all these sources"* |
| 16 | `/create-agent` | *"Create a new agent for X"* |
| 17 | `/manage-agent` | *"Update my X agent"* |
| 18 | `/contact-sync` | *"Sync John to my contacts"* |
| 19 | `/vault-security-audit` | *"Audit keamanan vault saya"* |

---

## 🔗 Zettelkasten Intelligence

Agent **Connector** jauh lebih dari sekadar analisis link biasa:

- **Klasifikasi Hub / Branch / Leaf** — note diberi skor berdasarkan kepadatan link. Hub (5+ link) adalah jangkar pengetahuanmu. Leaf (0–1 link) diflag untuk di-upgrade.
- **ICM completeness audit** — setiap permanent note dicek tiga lapisan: *Information* (fakta), *Context* (relevansi ke kamu), *Meaning* (so what?). Note yang stuck di `[Info-only]` mendapat prompt upgrade spesifik.
- **Evergreen scoring** — note diberi skor 0–5 berdasarkan atomicity, penulisan dengan kata sendiri, kelengkapan ICM, dan jumlah link.
- **Typed link suggestion** — saat note baru dibuat, Connector melabeli setiap koneksi: *Supports, Contradicts, Applies, Extends,* atau *Origin*.
- **Deteksi kontradiksi** — ketika dua note membuat klaim yang bertentangan, callout `[!contradiction]` ditambahkan ke keduanya. Teks asli tidak pernah diubah.
- **Deteksi gap MOC** — ketika 3+ permanent note berbagi topik tanpa Map of Content, Connector minta Architect untuk membuat satu.
- **Session continuity** — di akhir setiap sesi, GAIA menulis snapshot ke `Meta/hot.md` dan membacanya secara diam-diam di sesi berikutnya. Konteks tidak pernah hilang.

---

## 🚀 Instalasi

### Yang Dibutuhkan

- [Obsidian](https://obsidian.md) (gratis)
- Satu platform AI: [Claude Code](https://claude.ai/code) ⭐, [Gemini CLI](https://github.com/google-gemini/gemini-cli), [OpenCode](https://opencode.ai), atau [Codex CLI](https://openai.com/codex)
- Git

---

### 🍎 macOS

<details>
<summary><strong>Langkah 1 — Install Obsidian</strong></summary>

1. Download `.dmg` dari [obsidian.md](https://obsidian.md)
2. Buka `.dmg`, drag Obsidian ke **Applications**, lalu buka
3. Klik **Create new vault** → beri nama (mis. `MyBrain`) → pilih lokasi
4. Catat path lengkapnya — akan dipakai di langkah berikutnya

</details>

<details>
<summary><strong>Langkah 2 — Install Git</strong></summary>

Buka **Terminal** (`Cmd + Space` → ketik "Terminal") dan jalankan:

```bash
git --version
```

Jika belum ada, macOS akan tawari install Xcode Command Line Tools otomatis — klik **Install**.

</details>

<details>
<summary><strong>Langkah 3 — Install platform AI</strong></summary>

| Platform | Cara Install |
|----------|-------------|
| **Claude Code** ⭐ (direkomendasikan) | Download dari [claude.ai/code](https://claude.ai/code) |
| **Gemini CLI** | `npm install -g @google/gemini-cli` |
| **OpenCode** | `npm install -g opencode-ai` |
| **Codex CLI** | `npm install -g @openai/codex` |

> Node.js dibutuhkan untuk platform berbasis npm. Install dari [nodejs.org](https://nodejs.org) (versi LTS).

</details>

<details open>
<summary><strong>Langkah 4 — Install & Jalankan GAIA ✅</strong></summary>

```bash
# Masuk ke folder vault kamu
cd ~/Documents/MyBrain

# Clone dan install
git clone https://github.com/galeka/GAIA-Obsidian-Vault.git GAIA
cd GAIA && bash scripts/launchme.sh

# Buka vault dengan platform pilihanmu
cd ~/Documents/MyBrain
claude        # Claude Code
gemini        # Gemini CLI
opencode      # OpenCode
codex         # Codex CLI
```

Lalu katakan: **"Initialize my vault"** — skill `/onboarding` akan memandu setup lengkap.

</details>

---

### 🪟 Windows

> Windows membutuhkan [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install) untuk semua platform **kecuali Claude Code**, yang berjalan native di Windows.

<details>
<summary><strong>Langkah 1 — Install WSL 2</strong></summary>

Buka **PowerShell sebagai Administrator** (Start → klik kanan PowerShell → *Run as administrator*):

```powershell
wsl --install
```

Restart PC saat diminta. Setelah restart, WSL akan selesai install Ubuntu dan meminta kamu membuat username dan password Linux.

</details>

<details>
<summary><strong>Langkah 2 — Install Obsidian & Git</strong></summary>

- **Obsidian:** Download installer `.exe` dari [obsidian.md](https://obsidian.md), jalankan, buat vault baru
- **Git** (di dalam terminal WSL):

```bash
sudo apt update && sudo apt install git -y
```

</details>

<details>
<summary><strong>Langkah 3 — Install platform AI</strong></summary>

**Claude Code (native Windows — tanpa WSL):**  
Download dari [claude.ai/code](https://claude.ai/code). Kamu bisa skip WSL sepenuhnya.

**Gemini CLI / OpenCode / Codex CLI (via WSL):**

```bash
# Install Node.js dulu
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# Lalu install platform pilihan
npm install -g @google/gemini-cli   # Gemini CLI
npm install -g opencode-ai           # OpenCode
npm install -g @openai/codex         # Codex CLI
```

</details>

<details open>
<summary><strong>Langkah 4 — Install & Jalankan GAIA ✅</strong></summary>

```bash
# Di dalam WSL — sesuaikan path dengan nama usermu
cd /mnt/c/Users/NamaKamu/Documents/MyBrain

git clone https://github.com/galeka/GAIA-Obsidian-Vault.git GAIA
cd GAIA && bash scripts/launchme.sh

# Jalankan
cd /mnt/c/Users/NamaKamu/Documents/MyBrain
gemini   # atau: opencode / codex / claude
```

Lalu katakan: **"Initialize my vault"**

> **Claude Code di Windows (native):** Buka Claude desktop app, atau navigasi ke folder vault di Command Prompt / PowerShell lalu jalankan `claude`.

</details>

---

## 💬 Contoh Penggunaan Sehari-hari

```
Kamu:  "Do my daily review"
GAIA:  [membuka note hari ini, pull kalender, tanya focus items]

Kamu:  "I just read an article about zero-trust security"
GAIA:  [jalankan /reading-digest → buat literature note → link ke zettels terkait]

Kamu:  "What's on my plate this week?"
GAIA:  [jalankan /weekly-agenda → gabungkan kalender + email + tasks vault]

Kamu:  "Check my vault health"
GAIA:  [jalankan /vault-audit → laporan audit 7-fase lengkap]

Kamu:  "Prepare me for my 3pm meeting"
GAIA:  [pull konteks peserta, note lama, dan email terkait]
```

---

## 🖥️ Platform yang Didukung

| Platform | Install | macOS | Windows |
|----------|---------|:-----:|:-------:|
| **Claude Code** ⭐ | [claude.ai/code](https://claude.ai/code) | ✅ Native | ✅ Native |
| **Gemini CLI** | [github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | ✅ Native | ✅ Via WSL |
| **OpenCode** | [opencode.ai](https://opencode.ai) | ✅ Native | ✅ Via WSL |
| **Codex CLI** | `npm i -g @openai/codex` | ✅ Native | ✅ Via WSL |
| **AChatGPT** | Lihat bagian adapter di bawah | ✅ Native | ✅ Via WSL |

---

## 🔌 Integrasi Opsional

### GPT-4o / o3 via AChatGPT

Gunakan GPT-4o atau o3 sebagai backend pengganti Claude / Gemini:

```bash
cp adapters/AchatGPT/.env.example adapters/AchatGPT/.env
# Set ACHATGPT_API_KEY dan opsional VAULT_ROOT

chmod +x adapters/AchatGPT/achat.sh
./achat.sh "Initialize my vault"
```

| Tier | Model |
|------|-------|
| `low` | gpt-4o-mini |
| `mid` | gpt-4o |
| `high` | o3 |

Override model: `ACHATGPT_MODEL=gpt-4o ./achat.sh "..."`

### Lark / Feishu

Agent **Lark-Sync** menarik pesan, dokumen, tugas, dan event kalender dari Lark ke inbox vault kamu:

```bash
pip install fastmcp httpx pydantic python-dotenv

export LARK_APP_ID="cli_xxxxxxxx"
export LARK_APP_SECRET="xxxxxxxxxxxxxxxx"

claude mcp add lark-mcp python3 mcp/lark-mcp-server.py
```

Lalu katakan: *"sync from Lark"*, *"pull my Lark tasks"*, atau *"sync Lark calendar this week"*

> **Pengguna Feishu (edisi China):** tambahkan `LARK_API_BASE=https://open.feishu.cn` ke env vars kamu.  
> **Panduan setup lengkap:** `docs/lark-setup-guide.md`

---

## 📁 Struktur Project

```
GAIA/
├── agents/                   # 11 agents (8 core + Researcher + Lark-Sync + Prompt-Optimizer)
├── skills/                   # 19 skills
├── mcp/
│   ├── servers.yaml          # Definisi MCP server
│   └── lark-mcp-server.py   # Lark FastMCP server
├── adapters/
│   └── AchatGPT/            # Adapter backend GPT-4o/o3
├── scripts/
│   ├── launchme.sh          # Installer pertama kali
│   └── updateme.sh          # Updater
├── docs/
│   └── lark-setup-guide.md  # Panduan setup Lark
└── references/              # Referensi vault & konvensi
```

---

## 🔄 Update GAIA

```bash
cd ~/Documents/MyBrain/GAIA
git pull
bash scripts/updateme.sh
```

> Note-note vault kamu tidak pernah disentuh oleh update.

---

## 🤝 Kontribusi

Pull request dan issues sangat disambut! Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk panduan.

---

<div align="center">

Dibuat dengan ❤️ untuk second brain yang benar-benar berpikir.

**[⭐ Star repo ini](https://github.com/galeka/GAIA-Obsidian-Vault)** jika GAIA membantu workflow kamu!

</div>
