---
name: vault-security-audit
description: >
  Scan the GAIA vault for security issues: hardcoded API keys/tokens, PII in plaintext,
  .gitignore hygiene, sensitive notes exposed to git, and file permission issues.
  Triggers:
  EN: "vault security audit", "security scan", "check for exposed secrets",
  "are there API keys in my vault", "check .gitignore", "security check",
  "scan for sensitive data", "privacy audit".
  ID: "audit keamanan vault", "scan keamanan", "cek secrets yang terekspos",
  "ada API key di vault", "cek gitignore", "audit privasi".
mode: skill
model: mid
---

## Vault Path Resolution

Read `Meta/vault-map.md` (always this literal path) to resolve folder paths. Substitute only vault-role tokens — do NOT substitute other `{{...}}` patterns.

If vault-map.md is absent, use these defaults:

| Token | Default |
|-------|---------|
| `{{inbox}}` | `00-Inbox` |
| `{{meta}}` | `Meta` |

---

# Vault Security Audit

Always respond to the user in their language. Match the language the user writes in.

Scan the GAIA vault for security vulnerabilities: exposed API keys, PII in plaintext, .gitignore gaps, and sensitive note exposure. Generates a security report saved to `{{inbox}}/`.

---

## Critical Rules

1. READ-ONLY — never modify files during the audit. Only report findings.
2. Do NOT display full API keys or tokens in the report — show only the first 8 characters followed by `****`.
3. Do NOT send scan results outside the vault (no web requests, no clipboard writes).
4. Flag but do NOT resolve — present all findings to the user; let THEM decide what action to take.
5. Treat `.env` files as ALWAYS sensitive — flag any `.env` file not in `.gitignore`.
6. Only scan the vault directory — do NOT traverse parent directories or system paths.

---

## Security Checks

### Check 1: Hardcoded Secrets in Notes

Search vault notes (`.md` files) for patterns that indicate hardcoded secrets:

- API key patterns: `sk-`, `Bearer `, `api_key`, `API_KEY`, `apikey`, `token =`, `secret =`, `password =`
- Common service patterns: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `LARK_APP_SECRET`, `AWS_SECRET`, `GITHUB_TOKEN`
- Base64-looking long strings (40+ chars of alphanumeric) near key-like labels

For each finding:
- File path
- Line number
- Masked value (first 8 chars + `****`)
- Severity: CRITICAL (clearly a live key), HIGH (likely a key), MEDIUM (ambiguous)

**Bash command** (run via Bash tool):
```bash
grep -rn "sk-\|Bearer \|api_key\|API_KEY\|apikey\|token =\|secret =\|password =" \
  --include="*.md" /path/to/vault/ 2>/dev/null | head -50
```

### Check 2: PII in Plaintext

Search for patterns indicating unencrypted personal data:

- Email addresses in unexpected locations (outside `05-People/` folder)
- Phone number patterns (`+62`, `+1`, `08xx`)
- National ID patterns (Indonesian NIK: 16 digits; similar patterns)
- Credit card number patterns (16-digit groups)
- Passwords or PINs explicitly labeled as such

**Severity**:
- CRITICAL: passwords or financial data in plaintext
- HIGH: national IDs or medical information
- MEDIUM: phone numbers or addresses in unexpected locations
- LOW: email addresses (common but worth noting)

### Check 3: .gitignore Hygiene

Check if `.gitignore` at vault root properly excludes:

- `Meta/states/*.md` — agent state files (may contain processed email content)
- `.env` — environment variables
- `*.log` — log files
- `Meta/hey-tracker.jsonl` — Hey email tracker (may contain email metadata)
- `Meta/scripts/` — automation scripts (may contain credentials)
- Any `secrets/` or `private/` folders

For each missing exclusion, rate:
- CRITICAL: `.env` files not excluded
- HIGH: state files or tracker files not excluded
- MEDIUM: log files not excluded

**Bash command**:
```bash
cat /path/to/vault/.gitignore 2>/dev/null || echo "NO .GITIGNORE FOUND"
```

### Check 4: Sensitive Note Exposure

Check for notes that should be excluded from git but aren't:

- Notes with `sensitive: true` in frontmatter
- Notes with `private: true` in frontmatter
- Notes in folders named `private/`, `sensitive/`, `confidential/`
- Notes with `type: medical`, `type: financial`, `type: legal` in frontmatter

If a note is sensitive AND would be included in git, flag as HIGH.

### Check 5: eval() / exec() Patterns in Scripts

Scan `.js`, `.ts`, `.py` files in the vault for dangerous patterns:

- `eval(`, `exec(`, `os.system(`, `subprocess.run(`, `shell=True`
- Especially when variable data (from notes) is passed directly

---

## Report Template

Save the report to `{{inbox}}/YYYY-MM-DD — Security Audit Report.md`:

```markdown
---
type: security-audit
date: {{date}}
tags: [security, audit, vault-health]
status: inbox
severity: {{CRITICAL/HIGH/MEDIUM/LOW — highest found}}
created: {{timestamp}}
---

# Vault Security Audit — {{date}}

## Summary

| Severity | Count |
|----------|-------|
| 🔴 CRITICAL | {{N}} |
| 🟠 HIGH | {{N}} |
| 🟡 MEDIUM | {{N}} |
| 🟢 LOW | {{N}} |

**Files scanned**: {{N}}
**Clean files**: {{N}}
**Files with issues**: {{N}}

---

## 🔴 CRITICAL Issues

{{List each issue with: file path, line, masked value, recommended action}}

## 🟠 HIGH Issues

{{List each issue}}

## 🟡 MEDIUM Issues

{{List each issue}}

## 🟢 LOW / Informational

{{List each issue}}

---

## Recommended Actions

1. {{Most urgent action — e.g., "Rotate the API key in 05-People/OpenAI.md line 12"}}
2. {{Second action}}
...

---

## .gitignore Status

{{Current .gitignore entries}} 

Missing recommended exclusions:
- {{pattern}} — {{reason}}

---

*Generated by vault-security-audit skill on {{date}}*
*Vault-specific checks only. For broader security needs, consult a security professional.*
```

---

## Error Handling

- If no bash access: report that the scan requires Bash tool access and list manual checks the user can do
- If vault path is unknown: ask the user for the vault root path before scanning
- If .gitignore is missing: flag as CRITICAL and provide a starter .gitignore template
- Limit output to first 50 findings per check to prevent report bloat — note if truncated
