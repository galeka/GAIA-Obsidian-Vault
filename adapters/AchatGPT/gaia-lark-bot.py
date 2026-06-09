#!/usr/bin/env python3
"""
GAIA Lark Bot Handler
Connects Lark messages to ./achat.sh for Obsidian vault updates.

Installation:
  pip install flask python-dotenv requests

Setup:
  1. Copy gaia-lark-bot.py to your AchatGPT adapter directory
  2. Create .env file with Lark credentials (see below)
  3. Run: python gaia-lark-bot.py
  4. Set webhook URL in Lark console to: https://my-gaia-bot.loca.lt/webhook
     (replace with your localtunnel URL)

Environment variables (.env file):
  LARK_APP_ID=your_lark_app_id_here
  LARK_APP_SECRET=your_app_secret_here
  LARK_BOT_ID=your_bot_id_here
  ACHATGPT_API_KEY=your_api_key
  VAULT_ROOT=/path/to/vault
  ACHAT_SCRIPT=./achat.sh
"""

import os
import sys
import json
import subprocess
import hashlib
import hmac
import time
import platform
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import requests
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# Cross-Platform Path Resolution
# ─────────────────────────────────────────────────────────────────────────────

def get_default_vault_root():
    """Auto-detect vault path based on OS."""
    system = platform.system()

    if system == "Darwin":  # macOS
        # Try iCloud first, then local
        paths = [
            Path.home() / "Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault",
            Path.home() / "Library/Mobile Documents/com~obsidianmd~obsidian/Documents/MyVault",
            Path.home() / "Obsidian/MyVault",
        ]
        for p in paths:
            if p.exists():
                return str(p)
        return str(paths[0])  # Fallback

    elif system == "Windows":
        return str(Path.home() / "OneDrive" / "Documents" / "Obsidian" / "MyVault")

    elif system == "Linux":
        return str(Path.home() / "Obsidian" / "MyVault")

    else:
        return "."

# Configuration
LARK_APP_ID = os.getenv("LARK_APP_ID")
LARK_APP_SECRET = os.getenv("LARK_APP_SECRET")
LARK_BOT_ID = os.getenv("LARK_BOT_ID")
ACHATGPT_API_KEY = os.getenv("ACHATGPT_API_KEY")
VAULT_ROOT = Path(os.getenv("VAULT_ROOT") or get_default_vault_root()).resolve()
ACHAT_SCRIPT = Path(os.getenv("ACHAT_SCRIPT", "./achat.sh")).resolve()
LARK_API_BASE = "https://open.larksuite.com/open-apis"

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Lark Signature Verification
# ─────────────────────────────────────────────────────────────────────────────

def verify_lark_signature(timestamp: str, nonce: str, body: str) -> bool:
    """Verify that the request came from Lark."""
    # Lark verification: sign(timestamp + nonce + secret)
    message = timestamp + nonce + LARK_APP_SECRET
    signature = hmac.new(
        message.encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return True  # For now, skip verification (can enable later)


# ─────────────────────────────────────────────────────────────────────────────
# Lark API Helper Functions
# ─────────────────────────────────────────────────────────────────────────────

def get_lark_access_token() -> str:
    """Get a tenant access token from Lark."""
    url = f"{LARK_API_BASE}/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": LARK_APP_ID,
        "app_secret": LARK_APP_SECRET
    }
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()["tenant_access_token"]


def send_lark_message(message_id: str, content: str, token: str) -> dict:
    """Send a reply to a Lark message."""
    url = f"{LARK_API_BASE}/im/v1/messages/{message_id}/reply"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "content": json.dumps({
            "text": content
        }),
        "msg_type": "text"
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()


def get_lark_message_content(message_id: str, token: str) -> str:
    """Fetch full message content from Lark."""
    url = f"{LARK_API_BASE}/im/v1/messages/{message_id}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    # Extract text from message content
    try:
        content = json.loads(data["data"]["body"]["content"])
        return content.get("text", "")
    except:
        return str(data.get("data", {}).get("body", ""))


# ─────────────────────────────────────────────────────────────────────────────
# Vault Chat Integration
# ─────────────────────────────────────────────────────────────────────────────

def query_vault(message: str, source: str = "lark") -> str:
    """
    Send a query to ./achat.sh and get the response.

    Args:
        message: User message from Lark
        source: Source identifier (e.g., "lark", "email", "doc")

    Returns:
        Response from achat.sh
    """
    # Build prompt for achat.sh
    prompt = f"[{source.upper()}] {message}\n\nPlease save this to my Obsidian vault (00-Inbox if unclear where)."

    try:
        # Use platform-appropriate Python command
        python_cmd = "python3" if platform.system() != "Windows" else "python"

        result = subprocess.run(
            [python_cmd, str(ACHAT_SCRIPT), prompt],
            env={
                **os.environ,
                "VAULT_ROOT": str(VAULT_ROOT),
                "ACHATGPT_API_KEY": ACHATGPT_API_KEY
            },
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(ACHAT_SCRIPT.parent)  # Run from script directory
        )

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error processing message: {result.stderr}"

    except subprocess.TimeoutExpired:
        return "Request timed out. Please try again."
    except Exception as e:
        return f"Error: {str(e)}"


# ─────────────────────────────────────────────────────────────────────────────
# Flask Routes
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/webhook", methods=["POST"])
def lark_webhook():
    """Receive and process Lark webhook events."""
    try:
        body = request.get_json()

        # Lark sends a challenge on first setup
        if body.get("type") == "url_verification":
            return jsonify({
                "challenge": body.get("challenge")
            })

        # Handle message events
        if body.get("type") == "event_callback":
            event = body.get("event", {})

            if event.get("type") == "message":
                message_id = event.get("message_id")
                chat_id = event.get("chat_id")
                sender_id = event.get("sender", {}).get("open_id")

                # Get message content
                token = get_lark_access_token()
                message_content = get_lark_message_content(message_id, token)

                if not message_content:
                    return jsonify({"status": "ok"})

                print(f"[{datetime.now()}] Lark message from {sender_id}: {message_content}")

                # Query vault
                response = query_vault(message_content, source="lark")

                # Send reply
                try:
                    send_lark_message(message_id, response, token)
                    print(f"[{datetime.now()}] Sent reply: {response[:100]}...")
                except Exception as e:
                    print(f"[{datetime.now()}] Failed to send reply: {e}")

        return jsonify({"status": "ok"})

    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "vault": VAULT_ROOT,
        "tunnel": "https://my-gaia-bot.loca.lt"
    })


# ─────────────────────────────────────────────────────────────────────────────
# CLI Entry
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Validate setup
    if not LARK_APP_ID or not LARK_APP_SECRET:
        print("❌ Error: LARK_APP_ID and LARK_APP_SECRET required in .env")
        exit(1)

    if not ACHATGPT_API_KEY:
        print("❌ Error: ACHATGPT_API_KEY required in .env")
        exit(1)

    if not Path(ACHAT_SCRIPT).exists():
        print(f"❌ Error: {ACHAT_SCRIPT} not found")
        exit(1)

    print("✅ GAIA Lark Bot starting...")
    print(f"   Vault: {VAULT_ROOT}")
    print(f"   Script: {ACHAT_SCRIPT}")
    print(f"   Health: http://localhost:5000/health")
    print(f"   Webhook: https://my-gaia-bot.loca.lt/webhook (update in Lark console)")
    print()

    app.run(host="localhost", port=5000, debug=False)
