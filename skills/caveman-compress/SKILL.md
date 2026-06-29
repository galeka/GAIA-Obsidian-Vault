---
name: caveman-compress
description: >
  Compress natural language memory/state files into caveman format to save input tokens
  every session. Preserves all technical substance, code, URLs, paths, and structure.
  Compressed version overwrites original. Human-readable backup saved as FILE.original.md.
  Trigger: /caveman-compress FILEPATH or "compress this file", "kompres file ini".
  SAFE for: agent state files (Meta/states/*.md), DISPATCHER.md process sections.
  NEVER use on: vault note content, zettel notes, research notes, meeting notes, daily notes.
mode: skill
model: low
---

# Caveman Compress

## Purpose

Compress natural language operational files (agent state post-its, dispatcher notes, preferences) into caveman-speak to reduce input tokens loaded each session. Compressed version overwrites original. Human-readable backup saved as `<filename>.original.md`.

## GAIA-Specific Scope

### Safe to compress (operational/process files)
- `Meta/states/*.md` — agent post-it state files
- `Meta/hot.md` — hot cache file
- `Meta/agent-log.md` — log entries
- `Meta/user-profile.md` — user profile (prose sections only)
- `Meta/naming-conventions.md` — conventions docs
- `Meta/vault-structure.md` — structure documentation

### NEVER compress (vault content)
- Any note in `{{inbox}}/`, `{{projects}}/`, `{{areas}}/`, `{{resources}}/`, `{{archive}}/`
- Daily notes in `{{daily}}/`
- Meeting notes, research notes, zettel notes — ANY file that is vault content
- MOC files in `{{moc}}/`
- Template files in `{{templates}}/`

If user requests compression on a vault note file, refuse and explain:
> "Vault note content must stay in full prose for readability and long-term usefulness. Caveman compress only works on operational/state files."

## Trigger

`/caveman-compress <filepath>` or when user asks to compress a state/memory file.

## Process

1. Check file is in the safe list above. If it's a vault note, refuse.
2. Read the file.
3. Apply compression rules below.
4. Save backup as `<filename>.original.md`.
5. Overwrite original with compressed version.
6. Report: original token estimate → compressed token estimate → % saved.

## Compression Rules

### Remove
- Articles: a, an, the
- Filler: just, really, basically, actually, simply, essentially, generally
- Pleasantries: "sure", "certainly", "of course", "happy to", "I'd recommend"
- Hedging: "it might be worth", "you could consider", "it would be good to"
- Redundant phrasing: "in order to" → "to", "make sure to" → "ensure", "the reason is because" → "because"
- Connective fluff: "however", "furthermore", "additionally", "in addition"

### Preserve EXACTLY (never modify)
- Code blocks (fenced ``` and indented)
- Inline code (`backtick content`)
- URLs and links (full URLs, markdown links)
- File paths (`00-Inbox/`, `Meta/states/`, `{{inbox}}`)
- Commands and CLI strings
- Technical terms (agent names, vault path tokens, plugin names)
- Proper nouns (project names, people, areas)
- Dates, version numbers, numeric values
- Frontmatter/YAML headers — compress values, not keys
- Markdown headings — keep exact heading text, compress body below

### Compress
- Use short synonyms: "big" not "extensive", "fix" not "implement a solution for"
- Fragments OK: "Run tests before commit" not "You should always run tests before committing"
- Drop "you should", "make sure to", "remember to" — just state the action
- Merge redundant bullets that say the same thing differently

## Pattern

Original:
> You should always make sure to check the vault-map.md file before resolving any path tokens. This is important because it ensures that you are using the correct folder paths as configured by the user.

Compressed:
> Check vault-map.md before resolving path tokens. Ensures correct user-configured paths.

## Boundaries

- ONLY compress natural language operational files (.md, .txt)
- NEVER modify: .py, .js, .ts, .json, .yaml, .yml, .toml, .env, .sh, .hook.yaml
- If file has mixed content (prose + code), compress ONLY the prose sections
- Original file backed up as FILE.original.md before overwriting
- Never compress FILE.original.md
