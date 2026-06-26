# AChatGPT Vault Chat — Mac Quickstart

## 1. Open Terminal

## 2. Go to the adapter folder

```bash
cd ~/path/to/your-vault/GAIA/adapters/AchatGPT
```

## 3. Install Python dependencies (once)

```bash
pip install -r requirements.txt
```

> Only needed if you're running the Lark bot (`gaia-lark-bot.py`).
> The CLI tool (`achat.sh` / `vault-chat.py`) uses Python stdlib only — no install required.

## 4. Make the script executable (once)

```bash
chmod +x achat.sh
```

## 5. Set your vault path in achat.sh

Open `achat.sh` and edit this line:

```bash
export VAULT_ROOT="${VAULT_ROOT:-/path/to/your/vault}"
```

## 6. Run it

```bash
./achat.sh "What projects do I have?"
./achat.sh "Summarize my migration checklist"
./achat.sh "Search for notes about budgets"
./achat.sh "Create a note in 00-Inbox/ about topic X"
```

---

## Use from anywhere (optional)

```bash
cp achat.sh /usr/local/bin/achat
achat "your question"
```
