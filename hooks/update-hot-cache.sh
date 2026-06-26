#!/usr/bin/env bash
# =============================================================================
# Hook: Update Hot Cache (Stop)
# =============================================================================
# Fires when the session ends. Outputs a reminder to Claude to write/update
# Meta/hot.md with a compact context snapshot for next-session continuity.
#
# Claude reads this output before finalizing the session stop.
# =============================================================================

cat <<'EOF'
BEFORE ENDING THIS SESSION — write or overwrite Meta/hot.md with the following structure:

---
updated: "<ISO timestamp>"
session_summary: "<one sentence>"
---

## Recent activity (this session)
- <bullet per meaningful action taken>

## Active threads (incomplete work)
- <anything left unfinished or deferred>

## Vault state snapshot
- Notes: <total if known>
- Last audit: <date if known>
- Flagged items: <orphans, contradictions, broken links if any>

## Carry-forward
- <what to do next session — max 3 items>

Keep it under 40 lines. This file is read silently at the start of every session.
EOF
