# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| latest (`main`) | ✅ |

Only the latest commit on `main` receives security fixes.

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Report vulnerabilities privately via [GitHub Security Advisories](https://github.com/galeka/GAIA-Obsidian-Vault/security/advisories/new).

Include:
- A description of the vulnerability and its impact
- Steps to reproduce or a proof-of-concept
- Any suggested fix (optional)

## Response SLA

| Stage | Target |
|-------|--------|
| Initial acknowledgement | 48 hours |
| Severity assessment | 5 business days |
| Fix or mitigation | 30 days for High/Critical; 90 days for Medium/Low |

## Scope

In scope: code under `adapters/`, Python and shell scripts, Flask webhook, Claude API integration.

Out of scope: third-party services (Lark, AChatGPT proxy, Cloudflare), the Obsidian app itself, vault note content.
