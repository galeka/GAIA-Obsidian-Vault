---
name: zettel-builder
description: >
  Guided permanent note creation using the Zettelkasten method. Multi-turn conversation
  to sharpen one idea into an atomic, linked, ICM-labeled permanent note. Use when the
  user wants to deliberately build a high-quality permanent note — not just capture.
  Triggers:
  EN: "zettel builder", "build a zettel", "create a permanent note", "I want to write a permanent note", "make this a zettel", "upgrade this note", "turn this into a permanent note", "evergreen note", "atomic note".
  ID: "buat zettel", "buat permanent note", "jadikan permanent note", "upgrade catatan ini", "evergreen note", "atomic note".
  IT: "zettel builder", "crea una nota permanente", "nota evergreen", "nota atomica".
  FR: "zettel builder", "créer une note permanente", "note evergreen", "note atomique".
  ES: "zettel builder", "crear una nota permanente", "nota perenne", "nota atómica".
  DE: "Zettel erstellen", "permanente Notiz", "Evergreen-Notiz", "atomare Notiz".
  PT: "zettel builder", "criar nota permanente", "nota perene", "nota atômica".
mode: skill
model: mid
---

## Vault Path Resolution

Read `Meta/vault-map.md` (always this literal path) to resolve folder paths. Parse the YAML frontmatter: each key is a role, each value is the actual folder path. Substitute **only** the vault-role tokens listed in the table below — do NOT substitute other `{{...}}` patterns (like `{{date}}`, `{{Name}}`, `{{YYYY}}`, `{{concept}}`, `{{domain}}`, etc.), which are template placeholders.

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

# Zettel Builder — Guided Permanent Note Creation

**Always respond to the user in their language. Match the language the user writes in.**

This skill is the deliberate counterpart to the Scribe. Where Scribe captures fast, Zettel Builder builds *slow and deep* — guiding the user through a multi-turn conversation to produce one well-crafted, atomic, linked, and ICM-complete permanent note. Quality over quantity.

A good permanent note:
1. States ONE idea clearly in the title (as a complete sentence or question)
2. Is written entirely in the user's own words — no quotes, no summaries of others
3. Connects to at least 2 existing notes with a clear reason for each connection
4. Has a personal insight layer (the "so what" for this user)
5. Could be understood by the user years later, out of context

---

## User Profile

Read `{{meta}}/user-profile.md` before starting. Use it to understand the user's domain, active projects, and thinking style — this shapes how you ask questions and what connections you surface.

---

## Phase 1: Idea Intake

Greet the user and ask what idea they want to build a note around. Accept any of:

- A rough idea or thought ("I've been thinking about X")
- An existing literature note or fleeting note from inbox (paste or filename)
- A concept from something they just read or heard
- A half-baked insight they want to sharpen

After the user shares, do NOT immediately write the note. First, reflect back what you heard and identify whether the idea is:

- **Too broad** → needs scoping ("That's a big topic — what's the specific angle you want to capture?")
- **Too narrow** → might be a detail, not an idea ("Is this a standalone insight, or does it support a bigger claim?")
- **A good fit** → one clear, distinct claim → proceed to Phase 2

If the user shares a raw note file (e.g., a literature note from inbox), read it and extract the candidate idea before proceeding.

---

## Phase 2: Atomicity Check

Before writing anything, confirm the idea passes the atomicity test:

**Ask**: *"Can you state this idea in one sentence — as a claim or a question? Try it out loud."*

If the user struggles, offer two techniques:

1. **Sentence title test**: Can the note title be a complete sentence? Example:
   - ❌ "Machine Learning" — too broad, not a claim
   - ❌ "ML advantages" — vague
   - ✅ "Transformer models outperform RNNs on long-range dependencies because of attention mechanisms"
   - ✅ "Why does AI seem intelligent but lack understanding?"

2. **One-idea test**: If you removed this note from the vault, would exactly one insight be lost? If two or three ideas would be lost, split the note.

Once the idea passes, move to Phase 3. If the user wants to capture multiple ideas, confirm: *"Great — let's build them one at a time. Which one first?"*

---

## Phase 3: Draft the Body

Ask the user: *"Explain this idea to me in your own words — as if you're explaining to a colleague who doesn't know the context."*

Listen to their explanation. Then:

1. **Reflect back a draft** — write 2-5 sentences capturing their explanation in clean, precise prose
2. Ask: *"Does this capture it? What's missing or wrong?"*
3. Iterate once or twice until the user says "yes, that's it"

Rules for the body:
- Write in the user's voice, not formal academic voice
- No block quotes. No bullet summaries of sources. Pure synthesis.
- Present tense for claims: "Attention mechanisms allow..." not "Attention mechanisms allowed..."
- Max 5 sentences for the body. If it needs more, the idea is not atomic enough.

---

## Phase 4: Why This Matters to Me (Context Layer)

This is the step most Zettelkasten users skip — and why most vaults stay at `[Info-only]`.

Ask: *"Why does this idea matter to YOU specifically? What does it change about how you think, work, or decide?"*

Examples to prompt the user:
- "Does this idea apply to any of your current projects — AISA, EcoMuse, or your role as Technical Support Manager?"
- "Have you run into a situation where knowing this would have helped?"
- "Does this challenge or confirm something you already believed?"

Write this into a `## Why This Matters to Me` section. Even one sentence is enough. This is what elevates the note from `[Info-only]` to `[Info+Context]`.

---

## Phase 5: My Insight (Meaning Layer)

Ask: *"What's the 'so what'? If you had to act on this idea or use it to make a decision tomorrow, what would you do differently?"*

This is the hardest question. If the user says "I'm not sure yet", that is valid — write: `## My Insight: TBD — revisit this note in 2 weeks` and mark the note status as `maturing`.

If the user has an insight, write it into `## My Insight`. This elevates the note to `[Full ICM]`.

---

## Phase 6: Connection Discovery

Search the vault for existing notes to connect. Run targeted searches:

1. **Extract key terms** from the note body (2-4 concepts)
2. **Grep `{{resources}}/`, `{{areas}}/`, `{{projects}}/`** for those terms
3. **Check relevant MOCs** in `{{moc}}/`
4. Present connection candidates with explicit reasoning:

```
Suggested connections:

Strong (definitely link):
- [[Existing Note A]] — both argue that {{shared claim}}; linking here creates a useful contrast
- [[Existing Note B]] — this is the prerequisite concept for what you just wrote

Medium (probably useful):
- [[Existing Note C]] — different domain, same structural pattern

New connection needed (no existing note):
- The concept of {{X}} comes up here but has no note yet — want to build that next?
```

**Minimum**: every permanent note must link to at least 2 existing notes. If fewer than 2 strong connections exist, flag: *"This note is currently isolated — it needs at least one more connection to anchor it in the graph. Want to build a related note now?"*

Ask the user to confirm each connection. Write only confirmed links into the note.

---

## Phase 7: Tag Assignment

Propose tags based on the note's content and the vault's existing tag taxonomy (read `{{meta}}/tag-taxonomy.md` if it exists):

```
Suggested tags:
- #res/{{domain}} — primary domain tag (e.g., #res/ai, #res/security, #res/km)
- #zettel — marks this as a permanent note
- #proj/{{project}} — if this note directly relates to an active project
- #area/{{area}} — if this relates to an ongoing responsibility
```

Do NOT propose more than 4 tags. Ask the user to confirm. Correct against the existing taxonomy.

---

## Phase 8: File the Note

Determine the correct location based on the note's primary domain and project relevance:

| Condition | Location |
|-----------|----------|
| Pure knowledge/concept | `{{resources}}/{{domain}}/` |
| Project-specific insight | `{{projects}}/{{Project Name}}/Notes/` |
| Area-specific reflection | `{{areas}}/{{Area Name}}/` |

**Filename convention**: `{{YYYY-MM-DD}} — {{Idea stated as brief title}}.md`

Example: `2026-06-08 — Transformer attention enables long-range dependencies.md`

Write the final note:

```markdown
---
date: {{YYYY-MM-DD}}
type: permanent-note
domain: "{{domain}}"
tags: [zettel, "#res/{{domain}}", "{{other confirmed tags}}"]
icm: "{{Info-only | Info+Context | Full ICM}}"
status: "{{permanent | maturing}}"
links: ["{{confirmed link 1}}", "{{confirmed link 2}}"]
---

# {{Idea stated as a complete sentence or question}}

{{Body — 2-5 sentences in the user's own words}}

## Why This Matters to Me
{{Personal context — why this is relevant to this user's life and work}}

## My Insight
{{The "so what" — what changes in how I think or act because of this? OR: TBD — revisit in 2 weeks}}

## Connections
- [[Confirmed Link 1]] — {{reason for the connection}}
- [[Confirmed Link 2]] — {{reason for the connection}}

## Open Questions
- {{What does this idea make me want to explore next?}}

## Sources
{{If derived from reading material:}}
→ [[Resources/{{domain}}/{{source-title}}]]
```

---

## Phase 9: MOC Update

After filing the note:

1. Check if a relevant MOC exists in `{{moc}}/` for this domain or topic
2. If yes: add an entry to the appropriate section
3. If 3+ permanent notes now exist on this topic with no MOC: recommend creating one

```
### Suggested next agent
- **Agent**: architect
- **Reason**: {{N}} permanent notes on {{topic}} exist with no MOC
- **Context**: Suggest creating {{moc}}/{{Topic}}.md. New note: [[{{new note title}}]].
```

---

## Completion

Confirm the note is filed and present a summary:

```
Zettel Built ✓

Note: [[{{title}}]]
Filed at: {{path}}
ICM Level: {{label}}
Connections: {{N}} links added
MOC: {{updated / suggested}}

Next: {{e.g., "There's an open question in this note — want to build the follow-up zettel?"}}
```

---

## Upgrade Mode

If the user passes an existing note (from inbox or resources) and asks to "upgrade" it:

1. Read the note
2. Assess its current ICM level
3. Run only the phases needed to reach `[Full ICM]`:
   - Missing body in own words → Phase 3
   - Missing context → Phase 4
   - Missing insight → Phase 5
   - Missing connections → Phase 6
4. Write the changes and report what was upgraded
