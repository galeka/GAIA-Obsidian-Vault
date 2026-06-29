---
name: batch-ingest
description: >
  Process multiple source documents in a single session: articles, PDFs, notes, URLs,
  or raw text. Each source becomes a structured vault note; the batch ends with a
  cross-linking pass that connects all newly created notes to each other and to the
  existing vault.
  Triggers:
  EN: "batch ingest", "ingest all of these", "process these sources", "multiple sources",
      "add all these", "ingest batch", "I have several articles", "process all of these",
      "add these to the vault", "ingest these files".
  ID: "ingest semua ini", "proses semua sumber", "tambahkan semua ke vault".
  IT: "ingest multiplo", "processa queste fonti", "aggiungi tutto al vault".
  FR: "ingestion multiple", "traite ces sources", "ajoute tout au vault".
  ES: "ingestión múltiple", "procesa estas fuentes", "añade todo al vault".
  DE: "Stapelverarbeitung", "verarbeite diese Quellen", "alles zum Vault hinzufügen".
  PT: "ingestão em lote", "processa essas fontes", "adiciona tudo ao vault".
mode: skill
model: mid
---

## Vault Path Resolution

Read `Meta/vault-map.md` (always this literal path) to resolve folder paths. Substitute only vault-role tokens — do NOT substitute other `{{...}}` patterns.

If vault-map.md is absent, use these defaults:

| Token | Default |
|-------|---------|
| `{{inbox}}` | `00-Inbox` |
| `{{resources}}` | `03-Resources` |
| `{{meta}}` | `Meta` |
| `{{moc}}` | `MOC` |

---

# Batch Ingest — Multi-Source Processing Skill

**Always respond to the user in their language. Match the language the user writes in.**

Process a list of sources (articles, PDFs, URLs, raw text, file paths) into structured vault notes, then run a cross-linking pass across all newly created notes.

---

## User Profile

Read `{{meta}}/user-profile.md` before starting to understand the user's domain and how to classify incoming material.

---

## Hot Cache Check

Read `{{meta}}/hot.md` if it exists. Use it to understand recent vault context so new notes connect to active threads.

---

## Phase 1 — Source Inventory

Ask the user to list all sources if they have not already. Accept any mix of:
- URLs (fetch and extract)
- File paths (read directly)
- Pasted text / raw content
- Note titles already in the vault (re-process with deeper ICM)

Present the confirmed list back to the user:

```
Batch confirmed — N sources to process:
1. [type] "title or URL"
2. [type] "title or URL"
...

Processing order: longest/most complex first.
Estimated: N notes will be created.
Proceed? (yes / reorder / remove any)
```

Wait for confirmation before proceeding.

---

## Phase 2 — Per-Source Processing

Process each source sequentially. For each source:

### 2a. Read & Extract

- Fetch the full content (URL → web fetch, file → read, pasted → use directly)
- Extract: title, author, date, key claims, entities (people, orgs, concepts), key quotes

### 2b. ICM Assessment

Score the source on three layers:
- **Information** — what facts/data does it contain?
- **Context** — why does this exist? What problem does it address?
- **Meaning** — what does this mean for the user's work?

### 2c. Create Vault Note

File at `{{resources}}/Sources/[YYYY-MM-DD] [Title].md`:

```markdown
---
type: source-note
title: "{{title}}"
author: "{{author}}"
date: "{{date}}"
source: "{{url or file path}}"
ingested: "{{ISO date}}"
tags: [source, {{topic-tag}}]
icm: "{{info-only | info+context | full-icm}}"
---

# {{Title}}

## Summary
{{2–3 sentence summary}}

## Key Points
- {{point 1}}
- {{point 2}}
- {{point 3}}

## Notable Quotes
> "{{quote}}" — {{author}}, {{context}}

## Information
{{Core facts, data, definitions}}

## Context
{{Why this exists, what prompted it, relevant actors}}

## Meaning
{{What this implies for the user's work or active projects}}

## Entities
- People: [[Person A]], [[Person B]]
- Organizations: [[Org X]]
- Concepts: [[Concept Y]]

## Source
- Original: {{url or path}}
- Archived: {{date}}
```

### 2d. Progress Report

After each source, print a one-line status:
```
✓ [2/5] "Article Title" → Resources/Sources/2026-06-26 Article Title.md
```

---

## Phase 3 — Cross-Linking Pass

After all notes are created, run a cross-linking analysis across the entire batch:

1. **Intra-batch links** — which of the newly created notes share concepts, people, or arguments? Add wikilinks between them where contextually meaningful.

2. **Vault links** — for each new note, search existing vault notes for overlap. Suggest (but do not auto-apply) links to existing permanent notes, MOCs, or people notes.

3. **Contradiction detection** — if two sources in the batch make conflicting claims, flag with `[!contradiction]` in both notes and list the conflict.

4. **MOC update** — if 3+ new notes share a topic not covered by an existing MOC, flag for the Architect.

Present the cross-linking report:

```
Cross-linking report — N new notes

Intra-batch links created:
- "Note A" ↔ "Note B" — both cover {{shared concept}}
- "Note C" ↔ "Note D" — Note C's claim is challenged by Note D [!contradiction]

Suggested vault links (not auto-applied):
- "Note A" → [[Existing Permanent Note]] — related topic
- "Note B" → [[Person X]] — author mentioned

MOC gaps detected:
- 4 notes on {{topic}} — no existing MOC. Suggest Architect creates MOC/{{topic}}.md
```

Ask: *"Apply intra-batch links? (yes / review each / skip)"*

---

## Phase 4 — Batch Summary

Print a final summary:

```
Batch complete — N/N sources processed

Notes created:
- Resources/Sources/2026-06-26 Article A.md [full-icm]
- Resources/Sources/2026-06-26 Article B.md [info+context]
- ...

Contradictions flagged: N
MOC gaps: N
Vault link suggestions: N

Next steps:
- Say "connect the notes" to run a full vault cross-link pass
- Say "vault audit" if you want a health check after this batch
```

---

## Operational Rules

1. **Never silently skip** — if a source fails to fetch or parse, report it and continue with the rest
2. **ICM minimum** — every note must reach at least `info+context` before being filed
3. **Ask before bulk-linking** — always confirm before writing links to existing vault notes
4. **Log the batch** — append a summary line to `{{meta}}/agent-log.md`
5. **Respect rate limits** — add a 2-second pause between URL fetches to avoid hammering servers
