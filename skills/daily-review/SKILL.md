---
name: daily-review
description: >
  Daily note workflow: open or create today's daily note, pull today's calendar events,
  capture EOD reflections, extract action items to inbox, and generate a day-close summary.
  Triggers:
  EN: "daily review", "start my day", "open today's note", "daily note", "end of day", "EOD", "wrap up the day", "morning review", "evening review", "what did I do today", "close the day".
  ID: "review harian", "mulai hari", "buka catatan hari ini", "akhir hari", "tutup hari", "review pagi", "review malam", "apa yang aku kerjakan hari ini".
  IT: "review giornaliero", "inizia la giornata", "nota giornaliera", "fine giornata", "chiudi la giornata".
  FR: "revue quotidienne", "commencer la journée", "note du jour", "fin de journée", "clore la journée".
  ES: "revisión diaria", "empezar el día", "nota diaria", "fin del día", "cerrar el día".
  DE: "Tagesrückblick", "Tag beginnen", "Tagesnotiz", "Tagesabschluss", "Tag schließen".
  PT: "revisão diária", "começar o dia", "nota diária", "fim do dia", "fechar o dia".
mode: skill
model: mid
---

## Vault Path Resolution

Read `Meta/vault-map.md` (always this literal path) to resolve folder paths. Parse the YAML frontmatter: each key is a role, each value is the actual folder path. Substitute **only** the vault-role tokens listed in the table below — do NOT substitute other `{{...}}` patterns (like `{{date}}`, `{{Name}}`, `{{YYYY}}`, `{{MM}}`, `{{DD}}`, `{{ISO timestamp}}`, `{{today}}`, etc.), which are template placeholders.

If vault-map.md is absent: warn the user once — "No vault-map.md found, using default paths" — then use these defaults:

| Token | Default |
|-------|---------|
| `{{inbox}}` | `00-Inbox` |
| `{{projects}}` | `01-Projects` |
| `{{areas}}` | `02-Areas` |
| `{{daily}}` | `07-Daily` |
| `{{templates}}` | `Templates` |
| `{{meta}}` | `Meta` |
| `{{moc}}` | `MOC` |

If vault-map.md is present but a role is missing: warn the user — "vault-map.md does not define [role]. What folder should I use?" — and wait for their answer before proceeding.

---

# Daily Review — Morning & EOD Workflow

**Always respond to the user in their language. Match the language the user writes in.**

This skill runs the user's daily note rhythm: open or create today's note in the morning, and process it at EOD with reflections, action item extraction, and a day-close summary. It is the connective tissue between the vault and the user's lived day.

---

## User Profile

Read `{{meta}}/user-profile.md` before starting. Use it to understand the user's active projects, areas, and personal context so daily notes are contextually relevant.

---

## Mode Detection

Determine which mode to run based on the user's message and the current time:

| Mode | Triggers | Time Signal |
|------|----------|-------------|
| **Morning** | "start my day", "morning review", "daily note", "mulai hari", "review pagi" | Before 13:00 local |
| **EOD** | "end of day", "EOD", "wrap up", "close the day", "akhir hari", "review malam" | After 13:00 local |
| **Quick Check** | "what did I do today", "open today's note", "daily review" | Any time |

If ambiguous, check whether today's daily note already has an EOD section filled in. If yes, assume Quick Check. If no and it's afternoon, ask: **"Morning mode or EOD wrap-up?"**

---

## Daily Note Location & Naming

Daily notes live at: `{{daily}}/{{YYYY}}/{{MM}}/{{YYYY-MM-DD}}.md`

Example: `07-Daily/2026/06/2026-06-08.md`

If a `{{templates}}/daily-note.md` template exists, use it as the base for new notes. Otherwise use the default template below.

---

## Morning Mode

### Step 1: Open or Create Today's Note

Check if `{{daily}}/{{YYYY}}/{{MM}}/{{YYYY-MM-DD}}.md` exists.

- **If it exists**: read its content and confirm to the user: *"Today's note already exists — here's what you have so far."*
- **If it does not exist**: create the folder path if needed, then create the note using the Daily Note Template.

**Default Daily Note Template:**

```markdown
---
date: {{YYYY-MM-DD}}
type: daily
tags: [daily, "#area/journal"]
week: "{{YYYY-W{{WW}}}}"
---

# {{YYYY-MM-DD}} — {{Weekday}}

## 🌅 Morning Intentions
<!-- What matters most today? What's the one thing I want to accomplish? -->

## 📅 Today's Schedule
<!-- Pulled from calendar -->

## 🎯 Focus Items
<!-- Max 3 items from projects/areas -->

## 📝 Notes & Captures
<!-- Fleeting notes throughout the day -->

## ✅ EOD — What I Did
<!-- Completed tasks and work log -->

## 🔁 Reflections
<!-- What went well? What could be better? What surprised me? -->

## ➡️ Tomorrow's Setup
<!-- Anything to carry forward or prepare -->
```

### Step 2: Pull Today's Calendar

Use available calendar tools (Google Calendar MCP if connected) to fetch today's events. If no calendar MCP is available, prompt: *"I don't have calendar access right now — you can paste your schedule and I'll format it."*

Format events in the `## 📅 Today's Schedule` section:

```
## 📅 Today's Schedule
- 09:00 – Weekly standup with team [[People/Team]]
- 11:00 – AISA backend review [[Projects/AISA]]
- 14:00 – 1:1 with manager
- 16:00 – Focus block: EcoMuse Studio planning
```

Link any meeting to existing `[[People/...]]` or `[[Projects/...]]` notes if they exist in the vault.

### Step 3: Populate Focus Items

Scan active projects for open tasks. Check:
1. `{{projects}}/*/` — look for notes with `status: active` or `status: in-progress`
2. Yesterday's daily note `## ➡️ Tomorrow's Setup` section if it exists
3. `{{meta}}/states/sorter.md` for any flagged items

Populate `## 🎯 Focus Items` with max 3 items, ranked by urgency:

```
## 🎯 Focus Items
1. [[Projects/AISA/Backend API v2]] — finish auth module (deadline: this week)
2. [[Areas/Career/Performance Review]] — draft self-assessment
3. [[Projects/EcoMuse/Studio Launch]] — confirm venue
```

### Step 4: Present the Note

Show the completed morning note to the user and ask:
*"Morning note is ready. Anything to add before you start?"*

If the user adds items, append them to `## 📝 Notes & Captures`.

---

## EOD Mode

### Step 1: Read Today's Note

Read `{{daily}}/{{YYYY}}/{{MM}}/{{YYYY-MM-DD}}.md`. If it doesn't exist, create it with just the EOD sections filled in.

### Step 2: EOD Capture Interview

Ask the user a series of short questions. Keep it conversational — one question at a time:

1. **"What did you actually work on today?"** → captures into `## ✅ EOD — What I Did`
2. **"Any wins or things you're proud of?"** → first line of `## 🔁 Reflections`
3. **"What didn't go as planned?"** → second line of `## 🔁 Reflections`
4. **"Any open items to carry to tomorrow?"** → `## ➡️ Tomorrow's Setup`
5. **"Any quick ideas or thoughts to capture?"** → extracted as fleeting notes to `{{inbox}}/`

Skip any question the user says "nothing" or "skip" to.

### Step 3: Extract Action Items

Scan the EOD responses for action items (tasks with a verb + object + optional deadline). For each:
1. Create a brief fleeting note in `{{inbox}}/` titled `Task — {{action title}} — {{date}}.md`
2. Link it back to today's daily note: `[[{{daily}}/{{YYYY}}/{{MM}}/{{YYYY-MM-DD}}]]`
3. Add a wikilink in the daily note to the created task note

Only extract clear, actionable tasks — not vague reflections.

### Step 4: Update Project Notes (if applicable)

For any project mentioned in the EOD:
1. Read the project note at `{{projects}}/{{Project Name}}/`
2. Append a brief progress entry to its `## Log` or `## Updates` section:
   ```
   - {{date}}: {{one-line summary of what was done}}
   ```
3. Update `status` frontmatter if the user says something was completed

### Step 5: Day-Close Summary

Generate a clean EOD summary and write it back to the daily note:

```
EOD Summary — {{date}}

✅ Done: {{N}} items completed
📝 Captured: {{N}} fleeting notes sent to Inbox
➡️ Carry-forward: {{N}} items set for tomorrow
⏱ Focus time: {{estimated from schedule}}

Day Score: {{ask user: "Rate your day 1-5?"}}
```

Write the final summary to the daily note's `## ✅ EOD — What I Did` section, then confirm: *"Day closed. Rest well."*

---

## Quick Check Mode

Read today's note and present a concise status:

```
Today — {{date}}

Schedule: {{N}} events (next: {{event name}} at {{time}})
Focus: {{focus items}}
Captures so far: {{N}} notes
EOD: {{done / not yet}}
```

Ask: *"Anything to add or update?"*

---

## Linking Rules

- Always link today's daily note to any project or area mentioned: `[[Projects/AISA]]`, `[[Areas/Career]]`
- Link to people using `[[People/Name]]` format when they appear in the schedule
- Add a backlink from the daily note to yesterday's if the user carries items forward
- Each daily note should link to the weekly note if one exists: `[[MOC/Week {{WW}} 2026]]`

---

## Agent State (Post-it)

You have a personal post-it at `{{meta}}/states/daily-review.md`.

### At the START of every execution

Read `{{meta}}/states/daily-review.md` if it exists. It stores: last run date and mode, any pending carry-forward items from yesterday's EOD, and the user's current streak (consecutive days with daily notes).

### At the END of every execution

**Write your post-it. This is not optional.**

```markdown
---
agent: daily-review
last-run: "{{ISO timestamp}}"
mode: "{{morning | eod | quick-check}}"
---

## Post-it

last-date: {{YYYY-MM-DD}}
streak: {{N}} consecutive days
carry-forward: {{list of items the user said to carry to tomorrow}}
open-tasks-in-inbox: {{N}}
```

**Max 20 lines.**
