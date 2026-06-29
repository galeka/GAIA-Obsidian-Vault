# 📖 GAIA — Installation Guide

[← Back to README](README.md) · 🌐 [Bahasa Indonesia](INSTALL.id.md)

---

## Requirements

Before you start, make sure you have:

- [**Obsidian**](https://obsidian.md) — free note-taking app (your vault lives here)
- **One AI platform** — Claude Code is recommended for beginners
- **Git** — to download and update GAIA

---

## Choose your OS

- [🍎 macOS](#-macos)
- [🪟 Windows](#-windows)

---

## 🍎 macOS

### Step 1 — Install Obsidian

1. Go to [obsidian.md](https://obsidian.md) and download the macOS `.dmg`
2. Open the `.dmg`, drag Obsidian into **Applications**, then launch it
3. Click **Create new vault** → give it a name (e.g. `MyBrain`) → choose a folder
4. Remember the folder path — you'll need it in Step 4

### Step 2 — Install Git

Open **Terminal** (press `Cmd + Space`, type "Terminal", press Enter) and run:

```bash
git --version
```

If Git is not installed, macOS will pop up and offer to install it automatically — click **Install** and wait for it to finish.

### Step 3 — Install an AI platform

Pick one and install it:

| Platform | How to install | Best for |
|----------|---------------|----------|
| **Claude Code** ⭐ | Download from [claude.ai/code](https://claude.ai/code) | Beginners, easiest setup |
| **Gemini CLI** | `npm install -g @google/gemini-cli` | Google users |
| **OpenCode** | `npm install -g opencode-ai` | Multi-model flexibility |
| **Codex CLI** | `npm install -g @openai/codex` | OpenAI users |

> **Using npm?** You need Node.js first. Download from [nodejs.org](https://nodejs.org) (pick the LTS version). After installing, verify with `node --version`.

### Step 4 — Install GAIA

Open Terminal and navigate to your vault folder:

```bash
cd ~/Documents/MyBrain   # replace with your actual vault path
```

Clone GAIA and run the installer:

```bash
git clone https://github.com/galeka/GAIA-Obsidian-Vault.git GAIA
cd GAIA
bash scripts/launchme.sh
```

The installer will ask which AI platform you use — select it. GAIA will copy all agents, skills, and config into the right place.

### Step 5 — Start GAIA

Navigate to your vault and launch your AI platform:

```bash
cd ~/Documents/MyBrain

claude        # if you use Claude Code
gemini        # if you use Gemini CLI
opencode      # if you use OpenCode
codex         # if you use Codex CLI
```

Then say: **"Initialize my vault"**

The `/onboarding` skill will start a guided conversation to set up your folder structure, save your profile, and configure integrations.

### Step 6 — Update GAIA (when needed)

```bash
cd ~/Documents/MyBrain/GAIA
git pull
bash scripts/updateme.sh
```

Your vault notes are **never** touched by updates.

---

## 🪟 Windows

> **Claude Code users:** Claude Code runs natively on Windows — you can skip the WSL steps entirely. Just install Obsidian, download Claude Code from [claude.ai/code](https://claude.ai/code), and jump to [Step 4](#step-4--install-gaia-1).

All other platforms (Gemini CLI, OpenCode, Codex CLI) require **WSL 2** — a lightweight Linux environment built into Windows.

### Step 1 — Install WSL 2

Open **PowerShell as Administrator**:  
Start → search "PowerShell" → right-click → *Run as administrator*

```powershell
wsl --install
```

Restart your computer when prompted. After restart, a terminal will open and finish the Ubuntu installation — create a Linux username and password when asked (you'll need these later).

Verify it worked:
```powershell
wsl --version
```

### Step 2 — Install Obsidian

1. Go to [obsidian.md](https://obsidian.md) and download the Windows installer (`.exe`)
2. Run the installer and open Obsidian
3. Click **Create new vault** → name it (e.g. `MyBrain`) → save it somewhere easy, like `C:\Users\YourName\Documents\MyBrain`
4. Remember this path — you'll need it in Step 4

### Step 3 — Install an AI platform

**Option A — Claude Code (native Windows, no WSL needed)**

Download and install from [claude.ai/code](https://claude.ai/code). Skip to Step 4.

**Option B — Gemini CLI / OpenCode / Codex CLI (via WSL)**

Open the **WSL terminal** (Start → search "Ubuntu" or "WSL") and run:

```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
node --version   # should print v20 or higher

# Install Git
sudo apt update && sudo apt install git -y

# Install your chosen platform
npm install -g @google/gemini-cli   # Gemini CLI
npm install -g opencode-ai           # OpenCode
npm install -g @openai/codex         # Codex CLI
```

### Step 4 — Install GAIA

**Claude Code (native Windows):**

Install [Git for Windows](https://git-scm.com) first. Then open **Git Bash** (right-click in your vault folder → *Git Bash Here*):

```bash
git clone https://github.com/galeka/GAIA-Obsidian-Vault.git GAIA
cd GAIA
bash scripts/launchme.sh
```

**Gemini CLI / OpenCode / Codex CLI (via WSL):**

Windows drives are available in WSL at `/mnt/c/`, `/mnt/d/`, etc.

```bash
# Navigate to your vault — adjust YourName and MyBrain
cd /mnt/c/Users/YourName/Documents/MyBrain

git clone https://github.com/galeka/GAIA-Obsidian-Vault.git GAIA
cd GAIA
bash scripts/launchme.sh
```

Select your platform when prompted.

### Step 5 — Start GAIA

**Claude Code (native Windows):**  
Open the Claude desktop app, or navigate to your vault in Command Prompt / PowerShell and run `claude`.

**WSL platforms:**
```bash
cd /mnt/c/Users/YourName/Documents/MyBrain

gemini        # Gemini CLI
opencode      # OpenCode
codex         # Codex CLI
```

Then say: **"Initialize my vault"**

### Step 6 — Update GAIA (when needed)

**WSL:**
```bash
cd /mnt/c/Users/YourName/Documents/MyBrain/GAIA
git pull
bash scripts/updateme.sh
```

**Claude Code (native):**
```bash
cd C:\Users\YourName\Documents\MyBrain\GAIA
git pull
bash scripts/updateme.sh
```

---

## Optional: GPT-4o / o3 via AChatGPT

To use OpenAI models instead of Claude or Gemini:

```bash
cp adapters/AchatGPT/.env.example adapters/AchatGPT/.env
# Edit the file and set your ACHATGPT_API_KEY

chmod +x adapters/AchatGPT/achat.sh
./achat.sh "Initialize my vault"
```

| Tier | Model used |
|------|-----------|
| `low` | gpt-4o-mini |
| `mid` | gpt-4o |
| `high` | o3 |

---

## Optional: Lark / Feishu integration

```bash
pip install fastmcp httpx pydantic python-dotenv

export LARK_APP_ID="cli_xxxxxxxx"
export LARK_APP_SECRET="xxxxxxxxxxxxxxxx"

claude mcp add lark-mcp python3 mcp/lark-mcp-server.py
```

Then say: *"sync from Lark"* or *"pull my Lark tasks"*

> Feishu users: add `LARK_API_BASE=https://open.feishu.cn` to your env vars.  
> Full guide: `docs/lark-setup-guide.md`

---

## Something not working?

Open an issue at [github.com/galeka/GAIA-Obsidian-Vault/issues](https://github.com/galeka/GAIA-Obsidian-Vault/issues)

[← Back to README](README.md)
