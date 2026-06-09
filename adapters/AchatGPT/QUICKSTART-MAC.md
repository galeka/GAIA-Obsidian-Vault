# AChatGPT Vault Chat — Mac Quickstart

## 1. Open Terminal

## 2. Go to the adapter folder

```bash
cd ~/path/to/your-vault/GAIA/adapters/AchatGPT
```

## 3. Make the script executable (once)

```bash
chmod +x achat.sh
```

## 4. Set your vault path in achat.sh

Open `achat.sh` and edit this line:

```bash
export VAULT_ROOT="${VAULT_ROOT:-/path/to/your/vault}"
```

## 5. Run it

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
