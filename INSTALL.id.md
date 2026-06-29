# 📖 GAIA — Panduan Instalasi

[← Kembali ke README](README.md) · 🌐 [English](INSTALL.md)

---

## Yang Dibutuhkan

Sebelum mulai, pastikan kamu punya:

- [**Obsidian**](https://obsidian.md) — aplikasi catatan gratis (vault kamu ada di sini)
- **Satu platform AI** — Claude Code direkomendasikan untuk pemula
- **Git** — untuk download dan update GAIA

---

## Pilih sistem operasimu

- [🍎 macOS](#-macos)
- [🪟 Windows](#-windows)

---

## 🍎 macOS

### Langkah 1 — Install Obsidian

1. Pergi ke [obsidian.md](https://obsidian.md) dan download file `.dmg` untuk macOS
2. Buka file `.dmg`, drag Obsidian ke folder **Applications**, lalu buka
3. Klik **Create new vault** → beri nama (mis. `MyBrain`) → pilih folder penyimpanan
4. Ingat path folder ini — akan dipakai di Langkah 4

### Langkah 2 — Install Git

Buka **Terminal** (tekan `Cmd + Space`, ketik "Terminal", tekan Enter) lalu jalankan:

```bash
git --version
```

Jika Git belum ada, macOS akan otomatis menawarkan untuk install — klik **Install** dan tunggu selesai.

### Langkah 3 — Install platform AI

Pilih salah satu:

| Platform | Cara install | Cocok untuk |
|----------|-------------|-------------|
| **Claude Code** ⭐ | Download dari [claude.ai/code](https://claude.ai/code) | Pemula, setup paling mudah |
| **Gemini CLI** | `npm install -g @google/gemini-cli` | Pengguna Google |
| **OpenCode** | `npm install -g opencode-ai` | Fleksibilitas multi-model |
| **Codex CLI** | `npm install -g @openai/codex` | Pengguna OpenAI |

> **Pakai npm?** Kamu butuh Node.js terlebih dahulu. Download dari [nodejs.org](https://nodejs.org) (pilih versi LTS). Setelah install, cek dengan `node --version`.

### Langkah 4 — Install GAIA

Buka Terminal dan masuk ke folder vault kamu:

```bash
cd ~/Documents/MyBrain   # ganti dengan path vault kamu yang sebenarnya
```

Clone GAIA dan jalankan installer:

```bash
git clone https://github.com/galeka/GAIA-Obsidian-Vault.git GAIA
cd GAIA
bash scripts/launchme.sh
```

Installer akan menanya platform AI yang kamu pakai — pilih sesuai. GAIA akan menyalin semua agent, skill, dan konfigurasi ke tempat yang tepat.

### Langkah 5 — Mulai GAIA

Masuk ke folder vault dan jalankan platform AI-mu:

```bash
cd ~/Documents/MyBrain

claude        # jika pakai Claude Code
gemini        # jika pakai Gemini CLI
opencode      # jika pakai OpenCode
codex         # jika pakai Codex CLI
```

Lalu katakan: **"Initialize my vault"**

Skill `/onboarding` akan memulai percakapan terpandu untuk membuat struktur folder, menyimpan profilmu, dan mengatur integrasi.

### Langkah 6 — Update GAIA (saat diperlukan)

```bash
cd ~/Documents/MyBrain/GAIA
git pull
bash scripts/updateme.sh
```

Note-note vault kamu **tidak pernah** disentuh oleh proses update.

---

## 🪟 Windows

> **Pengguna Claude Code:** Claude Code berjalan native di Windows — kamu bisa skip langkah WSL sepenuhnya. Cukup install Obsidian, download Claude Code dari [claude.ai/code](https://claude.ai/code), dan langsung ke [Langkah 4](#langkah-4--install-gaia-1).

Platform lain (Gemini CLI, OpenCode, Codex CLI) membutuhkan **WSL 2** — lingkungan Linux ringan yang sudah built-in di Windows.

### Langkah 1 — Install WSL 2

Buka **PowerShell sebagai Administrator**:  
Start → cari "PowerShell" → klik kanan → *Run as administrator*

```powershell
wsl --install
```

Restart komputer saat diminta. Setelah restart, terminal akan terbuka dan menyelesaikan instalasi Ubuntu — buat username dan password Linux saat diminta (catat, akan dibutuhkan nanti).

Cek apakah berhasil:
```powershell
wsl --version
```

### Langkah 2 — Install Obsidian

1. Pergi ke [obsidian.md](https://obsidian.md) dan download installer Windows (`.exe`)
2. Jalankan installer dan buka Obsidian
3. Klik **Create new vault** → beri nama (mis. `MyBrain`) → simpan di lokasi yang mudah diingat, mis. `C:\Users\NamaKamu\Documents\MyBrain`
4. Ingat path ini — akan dipakai di Langkah 4

### Langkah 3 — Install platform AI

**Pilihan A — Claude Code (native Windows, tidak butuh WSL)**

Download dan install dari [claude.ai/code](https://claude.ai/code). Langsung ke Langkah 4.

**Pilihan B — Gemini CLI / OpenCode / Codex CLI (via WSL)**

Buka **terminal WSL** (Start → cari "Ubuntu" atau "WSL") dan jalankan:

```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
node --version   # harus menampilkan v20 atau lebih tinggi

# Install Git
sudo apt update && sudo apt install git -y

# Install platform pilihanmu
npm install -g @google/gemini-cli   # Gemini CLI
npm install -g opencode-ai           # OpenCode
npm install -g @openai/codex         # Codex CLI
```

### Langkah 4 — Install GAIA

**Claude Code (native Windows):**

Install [Git for Windows](https://git-scm.com) terlebih dahulu. Lalu buka **Git Bash** (klik kanan di folder vault → *Git Bash Here*):

```bash
git clone https://github.com/galeka/GAIA-Obsidian-Vault.git GAIA
cd GAIA
bash scripts/launchme.sh
```

**Gemini CLI / OpenCode / Codex CLI (via WSL):**

Di WSL, drive Windows tersedia di `/mnt/c/`, `/mnt/d/`, dll.

```bash
# Masuk ke folder vault — sesuaikan NamaKamu dan MyBrain
cd /mnt/c/Users/NamaKamu/Documents/MyBrain

git clone https://github.com/galeka/GAIA-Obsidian-Vault.git GAIA
cd GAIA
bash scripts/launchme.sh
```

Pilih platformmu saat ditanya.

### Langkah 5 — Mulai GAIA

**Claude Code (native Windows):**  
Buka aplikasi Claude desktop, atau navigasi ke folder vault di Command Prompt / PowerShell lalu jalankan `claude`.

**Platform WSL:**
```bash
cd /mnt/c/Users/NamaKamu/Documents/MyBrain

gemini        # Gemini CLI
opencode      # OpenCode
codex         # Codex CLI
```

Lalu katakan: **"Initialize my vault"**

### Langkah 6 — Update GAIA (saat diperlukan)

**WSL:**
```bash
cd /mnt/c/Users/NamaKamu/Documents/MyBrain/GAIA
git pull
bash scripts/updateme.sh
```

**Claude Code (native):**
```bash
cd C:\Users\NamaKamu\Documents\MyBrain\GAIA
git pull
bash scripts/updateme.sh
```

---

## Opsional: GPT-4o / o3 via AChatGPT

Untuk pakai model OpenAI sebagai pengganti Claude atau Gemini:

```bash
cp adapters/AchatGPT/.env.example adapters/AchatGPT/.env
# Edit file dan isi ACHATGPT_API_KEY dengan API key kamu

chmod +x adapters/AchatGPT/achat.sh
./achat.sh "Initialize my vault"
```

| Tier | Model yang dipakai |
|------|-------------------|
| `low` | gpt-4o-mini |
| `mid` | gpt-4o |
| `high` | o3 |

---

## Opsional: Integrasi Lark / Feishu

```bash
pip install fastmcp httpx pydantic python-dotenv

export LARK_APP_ID="cli_xxxxxxxx"
export LARK_APP_SECRET="xxxxxxxxxxxxxxxx"

claude mcp add lark-mcp python3 mcp/lark-mcp-server.py
```

Lalu katakan: *"sync from Lark"* atau *"pull my Lark tasks"*

> Pengguna Feishu: tambahkan `LARK_API_BASE=https://open.feishu.cn` ke env vars kamu.  
> Panduan lengkap: `docs/lark-setup-guide.md`

---

## Ada masalah?

Buka issue di [github.com/galeka/GAIA-Obsidian-Vault/issues](https://github.com/galeka/GAIA-Obsidian-Vault/issues)

[← Kembali ke README](README.md)
