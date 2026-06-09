# AChatGPT Adapter

Bridges the GAIA to the [AChatGPT](https://achatgpt.com) OpenAI-compatible API via a Cloudflare Worker proxy.

## Setup

```bash
# 1. Build the dist
bash scripts/build.sh --platform achatgpt

# 2. Configure credentials
cp dist/achatgpt/.achatgpt/.env.example dist/achatgpt/.achatgpt/.env
# Edit .env: set ACHATGPT_API_KEY

# 3. Test connectivity
source dist/achatgpt/.achatgpt/http-client.sh
achatgpt_check_quota && echo "OK"
```

## Model mapping

| Crew tier | AChatGPT model |
|-----------|---------------|
| `low`     | gpt-4o-mini   |
| `mid`     | gpt-4o        |
| `high`    | o3            |

## Known differences from Claude Code

| Feature | Claude Code | AChatGPT |
|---------|-------------|----------|
| Vision | Native | Base64 encode required |
| File uploads | Native | Preprocess required |
| Extended thinking | Native | o3 / o3-mini |
| Web search | Native tool | Custom endpoint |
| Rate limit | Soft | 429 → retry |

## Troubleshooting

| Error | Fix |
|-------|-----|
| `401 Unauthorized` | Check `ACHATGPT_API_KEY` |
| `429 Too Many Requests` | Quota exceeded — check dashboard |
| `502 Bad Gateway` | Proxy overload — client retries automatically |
| Timeout | o3/o3-mini are slow (~30-60s) — increase `ACHATGPT_REQUEST_TIMEOUT` |
