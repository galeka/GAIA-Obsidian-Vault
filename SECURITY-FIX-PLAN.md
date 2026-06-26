# GAIA Obsidian Vault — Security Fix Plan

> Generated: 2026-06-26
> Source repo: https://github.com/galeka/GAIA-Obsidian-Vault
> Review scope: All files in `main` branch

---

## Overview

This document tracks all security findings from the repo audit and provides
actionable fix steps for each. Issues are ordered by severity.

---

## 🔴 High Severity

### FIX-01 — Webhook Signature Verification Disabled

| Field | Detail |
|-------|--------|
| **File** | `adapters/AchatGPT/gaia-lark-bot.py` line 95 |
| **Impact** | Anyone on the internet can POST to the webhook and trigger vault writes and shell execution |
| **Effort** | Low (< 1 hour) |

**Root cause:**
The `verify_lark_signature()` function unconditionally returns `True` before
performing any check.

```python
# Current (broken)
return True  # For now, skip verification (can enable later)
```

**Fix steps:**
1. Remove the `return True` early-exit on line 95.
2. Confirm the HMAC logic uses the correct arguments (see FIX-02).
3. In the webhook route, call `verify_lark_signature()` and return HTTP 403 on failure.

```python
# Fixed webhook guard
@app.route("/webhook", methods=["POST"])
def lark_webhook():
    timestamp = request.headers.get("X-Lark-Request-Timestamp", "")
    nonce = request.headers.get("X-Lark-Request-Nonce", "")
    body = request.get_data(as_text=True)
    if not verify_lark_signature(timestamp, nonce, body):
        return jsonify({"error": "Invalid signature"}), 403
    # ... rest of handler
```

> ⚠️ Apply FIX-02 **before** enabling this guard, or every legitimate Lark request will 403.

**Verify:**
```bash
# Should return 403 with a bad/missing signature
curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Lark-Request-Timestamp: 9999999999" \
  -H "X-Lark-Request-Nonce: fake" \
  -H "X-Lark-Signature: invalidsignature" \
  -d '{"type":"event_callback"}'
# Expected output: 403

# A correctly signed request (use your own LARK_APP_SECRET) should return 200
# Use the Lark developer console "Send Test Event" button to generate a valid signed payload
```

---

### FIX-02 — HMAC Constructed with Wrong Key/Message Arguments

| Field | Detail |
|-------|--------|
| **File** | `adapters/AchatGPT/gaia-lark-bot.py` lines 86–94 |
| **Impact** | Even if FIX-01 is applied, the signature check would always fail or be bypassable |
| **Effort** | Low (< 30 min) |

**Root cause:**
The current code passes `message` (timestamp+nonce+secret) as the HMAC *key*
and `body` as the *message*. Lark's spec requires the opposite.

```python
# Current (wrong arguments)
signature = hmac.new(
    message.encode('utf-8'),   # ← this should be the SECRET (key)
    body.encode('utf-8'),      # ← this should be the MESSAGE
    hashlib.sha256
).hexdigest()
```

**Fix steps:**
1. Use `LARK_APP_SECRET` as the HMAC key.
2. Use `timestamp + nonce + body` as the message.
3. Compare result against the `X-Lark-Signature` request header (not a local variable).

```python
# Fixed HMAC
def verify_lark_signature(timestamp: str, nonce: str, body: str, signature: str) -> bool:
    message = (timestamp + nonce + body).encode("utf-8")
    expected = hmac.new(
        LARK_APP_SECRET.encode("utf-8"),
        message,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

> Note: Use `hmac.compare_digest()` to prevent timing attacks.

> ⚠️ This changes the function signature from 3 to 4 parameters. Update **all call sites** to pass `signature` (the value of the `X-Lark-Signature` header) or you will get a `TypeError` at runtime.

**Verify:**
```python
# Unit test — run standalone, no Flask needed
import hmac, hashlib

LARK_APP_SECRET = "test_secret"

def verify_lark_signature(timestamp, nonce, body, signature):
    message = (timestamp + nonce + body).encode("utf-8")
    expected = hmac.new(LARK_APP_SECRET.encode("utf-8"), message, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)

ts, nonce, body = "1700000000", "abc123", '{"type":"test"}'
correct_sig = hmac.new(LARK_APP_SECRET.encode(), (ts + nonce + body).encode(), hashlib.sha256).hexdigest()

assert verify_lark_signature(ts, nonce, body, correct_sig) is True,  "Valid sig rejected"
assert verify_lark_signature(ts, nonce, body, "deadbeef") is False,  "Invalid sig accepted"
print("FIX-02 OK")
```

---

### FIX-03 — Proxy URL Defaults to Placeholder Hostname

| Field | Detail |
|-------|--------|
| **Files** | `adapters/AchatGPT/vault-chat.py` line 22, `adapters/AchatGPT/templates/achatgpt-http-client.sh` line 8 |
| **Impact** | If the env var is unset, all API traffic (including vault content and API keys) goes to the placeholder domain |
| **Effort** | Low (< 30 min) |

**Root cause:**
Both files default the proxy URL to `"https://your-proxy-url.workers.dev"` instead of failing when unconfigured.

**Fix steps — Python (`vault-chat.py`):**

```python
# Replace
PROXY_URL = os.environ.get("ACHATGPT_PROXY_URL", "https://your-proxy-url.workers.dev")

# With
PROXY_URL = os.environ.get("ACHATGPT_PROXY_URL")
if not PROXY_URL:
    sys.exit("ERROR: ACHATGPT_PROXY_URL environment variable is not set.")
```

**Fix steps — Bash (`achatgpt-http-client.sh`):**

```bash
# Replace
ACHATGPT_PROXY_URL="${ACHATGPT_PROXY_URL:-https://your-proxy-url.workers.dev}"

# With
ACHATGPT_PROXY_URL="${ACHATGPT_PROXY_URL:?ERROR: ACHATGPT_PROXY_URL is not set}"
```

**Verify:**
```bash
# Python — should exit non-zero with a clear error message
unset ACHATGPT_PROXY_URL
python adapters/AchatGPT/vault-chat.py
# Expected: "ERROR: ACHATGPT_PROXY_URL environment variable is not set." + exit code 1

# Bash — should abort immediately
unset ACHATGPT_PROXY_URL
bash adapters/AchatGPT/achatgpt-http-client.sh
# Expected: bash: ACHATGPT_PROXY_URL: ERROR: ACHATGPT_PROXY_URL is not set

# Confirm normal operation still works when var is set
ACHATGPT_PROXY_URL="https://real.workers.dev" python adapters/AchatGPT/vault-chat.py --dry-run
```

---

## 🟠 Medium Severity

### FIX-04 — Unsanitized Input in Shell grep/find

| Field | Detail |
|-------|--------|
| **File** | `adapters/AchatGPT/runner.sh` — `search_vault` tool |
| **Impact** | Malicious query strings (e.g. starting with `-`) can inject grep options or cause unexpected behavior |
| **Effort** | Low (< 1 hour) |

**Fix steps:**
1. Prefix the query with `--` to stop grep from interpreting it as flags.
2. Always double-quote the variable.

```bash
# Replace
grep -r --include="$pat" -n "$query" "$VAULT_ROOT" 2>/dev/null

# With
grep -r --include="$pat" -n -- "$query" "$VAULT_ROOT" 2>/dev/null
```

3. Alternatively, use `grep -F` (fixed string) when regex is not required.

**Verify:**
```bash
# Should NOT inject grep flags — "-l" would normally list files, not search
query="-l"
grep -r --include="*.md" -n -- "$query" "$VAULT_ROOT" 2>/dev/null
# Expected: lines containing the literal string "-l", not a file listing

# Should NOT treat leading dash as option
query="--include=*.sh"
grep -r --include="*.md" -n -- "$query" "$VAULT_ROOT" 2>/dev/null
# Expected: lines containing the literal string "--include=*.sh"
```

---

### FIX-05 — Path Traversal in File Read/Write Tools

| Field | Detail |
|-------|--------|
| **Files** | `adapters/AchatGPT/runner.sh`, `adapters/AchatGPT/vault-chat.py` |
| **Impact** | An AI-generated path like `../../.ssh/authorized_keys` could read or overwrite files outside the vault |
| **Effort** | Medium (1–2 hours) |

**Fix steps — Python (`vault-chat.py`):**

```python
def _safe_path(base: Path, relative: str) -> Path:
    resolved = (base / relative).resolve()
    if not str(resolved).startswith(str(base.resolve())):
        raise ValueError(f"Path traversal detected: {relative}")
    return resolved
```

Apply `_safe_path(VAULT_ROOT, args["path"])` in both `read_file` and `write_file`.

> ⚠️ Do **not** use `str(resolved).startswith(str(base))` — this passes for `/vault-escape/file` when base is `/vault`. Use `resolved.is_relative_to(base.resolve())` (Python 3.9+) or `base.resolve() in resolved.parents`.

**Fix steps — Bash (`runner.sh`):**

```bash
# Add this helper
safe_path() {
    local base="$1" rel="$2"
    local full; full="$(realpath --no-symlinks "$base/$rel" 2>/dev/null)"
    # Use trailing slash to avoid prefix-match bypass (e.g. /vault-escape matching /vault*)
    if [[ "$full/" != "$base/"* ]]; then
        echo "ERROR: path traversal attempt: $rel" >&2
        return 1
    fi
    echo "$full"
}
```

Use `safe_path "$VAULT_ROOT" "$path"` instead of direct concatenation.

**Verify:**
```python
# Python unit test
from pathlib import Path

VAULT_ROOT = Path("/vault")

def _safe_path(base: Path, relative: str) -> Path:
    resolved = (base / relative).resolve()
    if not resolved.is_relative_to(base.resolve()):
        raise ValueError(f"Path traversal detected: {relative}")
    return resolved

# Should raise
try:
    _safe_path(VAULT_ROOT, "../../etc/passwd")
    assert False, "Traversal not caught"
except ValueError:
    pass

# Prefix-match bypass — /vault-escape should also raise
try:
    _safe_path(VAULT_ROOT, "../vault-escape/secret")
    assert False, "Prefix bypass not caught"
except ValueError:
    pass

# Legitimate path should work
result = _safe_path(VAULT_ROOT, "notes/daily.md")
assert str(result).startswith("/vault/")
print("FIX-05 Python OK")
```

```bash
# Bash — traversal attempt should print error and return non-zero
safe_path "/vault" "../../etc/passwd"
# Expected: ERROR: path traversal attempt: ../../etc/passwd (exit 1)

# Prefix-match bypass
safe_path "/vault" "../vault-escape/secret"
# Expected: ERROR: path traversal attempt (exit 1)

# Legitimate path should succeed
safe_path "/vault" "notes/daily.md"
# Expected: /vault/notes/daily.md (exit 0)
```

---

### FIX-06 — No Rate Limiting on Flask Webhook

| Field | Detail |
|-------|--------|
| **File** | `adapters/AchatGPT/gaia-lark-bot.py` |
| **Impact** | Attacker can spam the webhook with requests, triggering repeated vault writes and shell subprocesses |
| **Effort** | Low (< 1 hour) |

**Fix steps:**

Option A — Use `Flask-Limiter` (recommended):

```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address, app=app, default_limits=["30 per minute"])
```

Option B — Lightweight manual counter using a dict with a TTL check (no extra dependency).

> Note: FIX-01 (enabling signature verification) also mitigates this significantly.

> ⚠️ If Flask sits behind nginx/Caddy (as recommended in FIX-10), `get_remote_address` reads the proxy's IP, not the client's. Add `ProxyFix` middleware and configure `x_for=1` so Flask-Limiter sees the real client IP. Without this, all clients share a single rate-limit bucket.

**Verify:**
```bash
# Send 31 rapid requests — the 31st should return 429
for i in $(seq 1 31); do
  CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:5000/webhook \
    -H "Content-Type: application/json" -d '{}')
  echo "Request $i: $CODE"
done
# Expected: requests 1–30 return 403 (no valid sig) or 200; request 31 returns 429

# Confirm the rate-limit resets after 60 seconds (or restart Flask for testing)
```

---

## 🟡 Low / Informational

### FIX-07 — Enable GitHub Security Scanners

| Field | Detail |
|-------|--------|
| **Location** | GitHub repo Settings → Security |
| **Impact** | Missed dependency CVEs, accidental secret commits go undetected |
| **Effort** | < 15 min |

**Fix steps:**
1. Go to **Settings → Security & analysis**.
2. Enable **Dependabot alerts** and **Dependabot security updates**.
3. Enable **Secret scanning** — this will retroactively scan commit history for leaked keys.
4. Enable **Code scanning** using the default CodeQL workflow.

> ⚠️ If secret scanning finds any leaked keys in commit history, **rotate those credentials immediately** before marking this fix done. Removing the key from code does not invalidate already-leaked secrets.

**Verify:**
- Navigate to **Security → Dependabot alerts** — page should exist and show "No alerts" or a list of CVEs (not a 404).
- Navigate to **Security → Secret scanning alerts** — confirm it shows "Enabled" in Settings.
- Push a commit that intentionally includes a fake secret in a comment (e.g., `# fake_key = "AKIA0000TEST0000"`), confirm an alert fires within minutes, then revert the commit.
- Check **Actions** tab for a CodeQL workflow run after the next push.

---

### FIX-08 — Add a Security Disclosure Policy

| Field | Detail |
|-------|--------|
| **Location** | Create `SECURITY.md` at repo root |
| **Effort** | < 15 min |

**Fix steps:**
Create `SECURITY.md` with at minimum:
- Supported versions
- How to privately report a vulnerability (GitHub private advisory link recommended)
- Response SLA expectation

GitHub will automatically surface this file on the Security tab and issue creation pages.

**Verify:**
- Visit `https://github.com/galeka/GAIA-Obsidian-Vault/security/policy` — should render `SECURITY.md` content, not a 404.
- Open a new issue on the repo — GitHub should display a link to the security policy above the issue form.

---

### FIX-09 — Fix Hardcoded Non-Existent Model Name

| Field | Detail |
|-------|--------|
| **File** | `adapters/AchatGPT/achat.sh` line 17 |
| **Impact** | Default model `gpt-5.4` does not exist; all calls fail silently without `ACHATGPT_MODEL` set |
| **Effort** | < 5 min |

**Fix steps:**

```bash
# Replace
export ACHATGPT_MODEL="${ACHATGPT_MODEL:-gpt-5.4}"

# With a valid model (align with models-mapping.yaml)
export ACHATGPT_MODEL="${ACHATGPT_MODEL:-gpt-4o}"
```

**Verify:**
```bash
# Run without override — should use gpt-4o, not gpt-5.4
unset ACHATGPT_MODEL
source adapters/AchatGPT/achat.sh
echo "Model: $ACHATGPT_MODEL"
# Expected: Model: gpt-4o

# Override should still be respected
ACHATGPT_MODEL="gpt-4-turbo" source adapters/AchatGPT/achat.sh
echo "Model: $ACHATGPT_MODEL"
# Expected: Model: gpt-4-turbo

# Make a real API call and confirm it does not return a model-not-found error
```

---

### FIX-10 — Replace localtunnel with a Secure Webhook Endpoint

| Field | Detail |
|-------|--------|
| **File** | `adapters/AchatGPT/gaia-lark-bot.py` docstring |
| **Impact** | `localtunnel` exposes the Flask server on a public, unauthenticated, ephemeral URL |
| **Effort** | Medium (setup time varies) |

**Fix steps:**
- For production use, deploy behind a proper reverse proxy (nginx/Caddy) with TLS.
- Alternatively, use **Cloudflare Tunnel** (`cloudflared`) which authenticates the tunnel and does not expose an open port.
- Update documentation to discourage `localtunnel` for anything beyond local development.

**Verify:**
```bash
# Confirm Flask is no longer reachable on the public localtunnel URL
# After switching to Cloudflare Tunnel or nginx:

# 1. The old localtunnel subdomain should return an error or timeout
curl -s -o /dev/null -w "%{http_code}" https://<old-lt-subdomain>.loca.lt/webhook
# Expected: connection error or 404 (tunnel no longer active)

# 2. The new endpoint should respond
curl -s -o /dev/null -w "%{http_code}" https://<your-domain>/webhook
# Expected: 403 (request blocked by sig check, which confirms the endpoint is live)

# 3. Confirm TLS is valid
curl -v https://<your-domain>/webhook 2>&1 | grep "SSL certificate verify ok"
# Expected: SSL certificate verify ok
```

---

### FIX-11 — Explicitly Disable Flask Debug Mode

| Field | Detail |
|-------|--------|
| **File** | `adapters/AchatGPT/gaia-lark-bot.py` |
| **Impact** | If debug mode is accidentally enabled, Flask exposes an interactive Python shell on error pages |
| **Effort** | < 5 min |

**Fix steps:**

```python
# Replace
app.run(...)

# With
app.run(debug=False, host="127.0.0.1", port=5000)
```

Binding to `127.0.0.1` (localhost only) instead of `0.0.0.0` also reduces exposure.

> ⚠️ Binding to `127.0.0.1` will block localtunnel from routing to Flask. If still using localtunnel during development, keep `host="0.0.0.0"` but ensure `debug=False` explicitly. Switch to `127.0.0.1` only once a proper reverse proxy (FIX-10) is in place.

**Verify:**
```bash
# Trigger a deliberate 500 error (e.g., send malformed JSON)
curl -s -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d 'not-valid-json'
# Expected: a plain JSON error response — NOT an interactive debugger page (no HTML with "Traceback" or "Console" in the body)

# Confirm debug mode is off via Flask logs at startup
# Expected log line: WARNING: Do not use the development server in a production environment.
# (This warning only appears when debug=False; debug=True shows a different message.)

# Confirm port is not listening on 0.0.0.0
ss -tlnp | grep 5000
# Expected: 127.0.0.1:5000 (not 0.0.0.0:5000)
```

---

## Fix Priority Checklist

```
[x] FIX-01  Enable Lark webhook signature verification      🔴 High   ✅ 2026-06-26
[x] FIX-02  Correct HMAC key/message arguments              🔴 High   ✅ 2026-06-26
[x] FIX-03  Fail on unconfigured proxy URL                  🔴 High   ✅ 2026-06-26
[x] FIX-04  Sanitize grep input in runner.sh                🟠 Medium ✅ 2026-06-26
[x] FIX-05  Add path traversal guard to file tools          🟠 Medium ✅ 2026-06-26
[x] FIX-06  Add rate limiting to Flask webhook              🟠 Medium ✅ 2026-06-26
[x] FIX-07  Enable GitHub Dependabot + secret scanning      🟡 Low    ✅ 2026-06-26
[x] FIX-08  Add SECURITY.md disclosure policy               🟡 Low    ✅ 2026-06-26
[x] FIX-09  Fix default model name in achat.sh              🟡 Low    ✅ 2026-06-26
[x] FIX-10  Replace localtunnel with secure tunnel          🟡 Low    ✅ 2026-06-26 (docstring updated)
[x] FIX-11  Explicitly set Flask debug=False                🟡 Low    ✅ already correct
```

---

*This plan was generated from a manual code review of commit `744ad80` (initial) through `f4dee96` (latest as of 2026-06-11).*
