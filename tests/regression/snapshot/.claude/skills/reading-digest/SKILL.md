---
name: reading-digest
description: >
  Process reading material (articles, papers, threads, book excerpts) into atomic
  Zettelkasten notes with ICM assessment, proper tags, and backlinks to existing vault notes.
  Transforms raw reading into permanent knowledge assets.
  Triggers:
  EN: "reading digest", "I just read", "process this article", "save this reading", "digest this", "take notes from this", "summarize this for my vault", "reading notes", "article to notes", "paper notes", "add to my knowledge base".
  ID: "digest bacaan", "baru saja baca", "proses artikel ini", "simpan bacaan ini", "catat dari ini", "ringkasan untuk vault", "catatan bacaan", "artikel ke notes".
  IT: "digest di lettura", "ho appena letto", "processa questo articolo", "note di lettura", "articolo in note".
  FR: "digest de lecture", "je viens de lire", "traite cet article", "notes de lecture", "article en notes".
  ES: "digest de lectura", "acabo de leer", "procesa este artículo", "notas de lectura", "artículo a notas".
  DE: "Lese-Digest", "gerade gelesen", "verarbeite diesen Artikel", "Lesenotizen", "Artikel zu Notizen".
  PT: "digest de leitura", "acabei de ler", "processa este artigo", "notas de leitura", "artigo em notas".
---

## Vault Path Resolution

Read `Meta/vault-map.md` (always this literal path) to resolve folder paths. Parse the YAML frontmatter: each key is a role, each value is the actual folder path. Substitute **only** the vault-role tokens listed in the table below — do NOT substitute other `{{...}}` patterns (like `{{date}}`, `{{Name}}`, `{{YYYY}}`, `{{author}}`, `{{title}}`, etc.), which are template placeholders.

If vault-map.md is absent: warn the user once — "No vault-map.md found, using default paths" — then use these defaults:

| Token | Default |
|-------|---------|
| `{{inbox}}` | `00-Inbox` |
| `{{resources}}` | `03-Resources` |
| `{{areas}}` | `02-Areas` |
| `{{projects}}` | `01-Projects` |
| `{{meta}}` | `Meta` |
| `{{moc}}` | `MOC` |

If vault-map.md is present but a role is missing: warn the user — "vault-map.md does not define [role]. What folder should I use?" — and wait for their answer before proceeding.

---

# Reading Digest — From Raw Reading to Vault Knowledge

**Always respond to the user in their language. Match the language the user writes in.**

Transform reading material into durable, linked, atomic notes in the vault. This skill bridges the gap between passive reading and active knowledge building. Every article, paper, or thread the user processes here becomes a first-class citizen in their Zettelkasten — not a graveyard of bookmarks.

---

## User Profile

Read `{{meta}}/user-profile.md` before processing. Use it to understand active projects, areas of focus, and the user's knowledge domain — this drives better tagging, linking, and ICM assessment.

---

## Phase 1: Material Intake

Ask the user for the reading material. Accept any of the following:

- Pasted article text or excerpt
- A URL (fetch with WebFetch if available)
- A PDF attachment
- A transcript or thread (Twitter/X, LinkedIn, Hacker News, etc.)
- A book excerpt or chapter summary

If a URL is provided, attempt to fetch the content. If fetching fails, ask the user to paste the text directly.

Confirm receipt: *"Got it — a {{format}} by {{author if known}} about {{topic}}. Let me process this."*

---

## Phase 2: Source Analysis

Extract the following metadata from the material:

```yaml
source-title: "{{Full title of the article/paper/thread}}"
source-author: "{{Author name(s)}}"
source-url: "{{URL if available}}"
source-type: "{{article | paper | thread | book | video-transcript | podcast}}"
source-date: "{{Publication date if available}}"
domain: "{{Primary knowledge domain: AI, Fintech, Security, KM, Management, etc.}}"
read-date: "{{Today's date}}"
```

Identify the **primary thesis** in one sentence: what is the core claim or insight this material makes?

---

## Phase 3: Atomic Note Extraction

### Zettelkasten Atomicity Rule

**One idea per note.** Do not create monolithic summaries. Extract each distinct, standalone insight as its own note. A single 2,000-word article may yield 3-8 atomic notes.

An idea is atomic when:
- It can stand alone and be understood without reading the other notes
- It represents a single concept, argument, claim, or question
- It could appear in multiple contexts (different projects, different areas)

### Extraction Process

1. Read the full material
2. Identify 3-10 distinct ideas worth preserving. Discard filler, examples, and re-statements
3. For each idea, draft a **Literature Note** (raw capture) and flag it for conversion to a **Permanent Note**

---

## Phase 4: Note Types

### Type A — Literature Note (auto-created)

A direct capture from the source, minimal processing. Stored in `{{inbox}}/` temporarily.

```markdown
---
date: {{read-date}}
type: literature-note
source: "[[Resources/{{domain}}/{{source-title}}]]"
author: "{{source-author}}"
tags: [lit-note, "#res/{{domain}}"]
status: to-process
icm: Info-only
---

# LIT — {{Idea Title}}

> {{Direct quote or close paraphrase from source}}

**Source**: [[{{source-title}}]] by {{source-author}} ({{source-date}})

## My Initial Reaction
{{One sentence: what strikes me about this? Do I agree, doubt, or find it useful?}}
```

### Type B — Permanent Note (user-confirmed)

A permanent note is the user's own formulation of the idea — in their own words, connected to their existing knowledge. Stored in `{{resources}}/{{domain}}/`.

```markdown
---
date: {{read-date}}
type: permanent-note
tags: [zettel, "#res/{{domain}}", "{{additional tags}}"]
links: []
icm: "{{Info-only | Info+Context | Full ICM}}"
status: permanent
---

# {{Idea stated as a complete sentence or provocative question}}

{{The idea in the user's own words — 2-5 sentences. No quotes. Pure synthesis.}}

## Why This Matters to Me
{{Personal relevance: how does this connect to my work, projects, or thinking?}}

## Connections
- [[Related Note 1]] — {{why they're connected}}
- [[Related Note 2]] — {{why they're connected}}

## Open Questions
- {{What does this make me wonder about?}}

## Source
→ [[Resources/{{domain}}/{{source-title}}]]
```

---

## Phase 5: ICM Assessment

Evaluate each extracted note against the three ICM stages and label it:

| Label | Criteria |
|-------|----------|
| `[Info-only]` | Raw data or fact — accurate but no personal context or insight yet |
| `[Info+Context]` | Fact + why it matters to THIS user in THIS vault (their projects, domain, role) |
| `[Full ICM]` | Fact + context + personal insight or action — translates into wisdom or a decision |

**Target**: push every note to at least `[Info+Context]`. Flag `[Info-only]` notes with: *"⚠️ This note needs a 'Why This Matters to Me' section to reach Info+Context level."*

For `[Full ICM]` notes, add a `## My Insight` section:
```markdown
## My Insight
{{The "so what" — what does this mean for how I think, work, or decide?}}
```

---

## Phase 6: Link Discovery

After drafting each permanent note, search the vault for existing notes to connect:

1. **Grep by concept** — search `{{resources}}/`, `{{areas}}/`, `{{projects}}/` for key terms from the note
2. **Check relevant MOCs** — does a MOC for this topic exist in `{{moc}}/`? If yes, add this note to it
3. **Surface connection candidates**:

```
Suggested connections for "{{Note Title}}":

Strong match:
- [[Existing Note A]] — both discuss {{shared concept}}
- [[Existing Note B]] — this note challenges/confirms what you wrote there

Medium match:
- [[Existing Note C]] — different domain, same underlying principle

New MOC needed?
- You now have {{N}} notes on {{topic}} — consider creating {{moc}}/{{Topic}}.md
```

Ask the user to confirm connections before writing links. Apply confirmed links bidirectionally where meaningful.

---

## Phase 7: Filing & Output

### Source Note

Create a master source note in `{{resources}}/{{domain}}/{{source-title}}.md`:

```markdown
---
date: {{read-date}}
type: source
source-type: "{{article | paper | thread | book}}"
author: "{{source-author}}"
url: "{{source-url}}"
tags: [source, "#res/{{domain}}"]
---

# {{source-title}}
**By**: {{source-author}} | **Published**: {{source-date}} | **Read**: {{read-date}}

## Primary Thesis
{{One sentence: the core claim of this work}}

## Atomic Notes Extracted
{{List of wikilinks to all permanent notes derived from this source}}
- [[{{Permanent Note 1}}]]
- [[{{Permanent Note 2}}]]

## My Overall Take
{{2-3 sentences: overall reaction, usefulness rating, would I cite this?}}
```

### Final Output Summary

Present a digest report:

```
Reading Digest Complete

Source: "{{title}}" by {{author}}
Domain: {{domain}}

Notes Created:
- {{N}} Literature notes → {{inbox}}/
- {{N}} Permanent notes → {{resources}}/{{domain}}/
- 1 Source note → {{resources}}/{{domain}}/

ICM Assessment:
- Full ICM: {{N}} notes
- Info+Context: {{N}} notes
- Info-only (needs upgrade): {{N}} notes

Links Added: {{N}} connections to existing notes
MOCs Updated: {{list of MOCs touched}}

Suggested next step: {{e.g., "Run /zettel-builder on the Info-only notes to upgrade them"}}
```

---

## Suggested Next Agent

If the reading contains people worth adding to `{{people}}/`:
```markdown
### Suggested next agent
- **Agent**: scribe
- **Reason**: Author {{name}} or mentioned expert {{name}} should have a People note
- **Context**: Create [[People/{{name}}]] with their background and this source as reference
```

If 3+ notes on the same topic are now in the vault with no MOC:
```markdown
### Suggested next agent
- **Agent**: architect
- **Reason**: {{N}} notes on {{topic}} now exist with no MOC
- **Context**: Suggest creating {{moc}}/{{Topic}}.md linking all new permanent notes
```
