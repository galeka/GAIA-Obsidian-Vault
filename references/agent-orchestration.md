# Agent Orchestration Protocol

This document defines how agents coordinate through the **dispatcher** (`DISPATCHER.md`). Agents do NOT communicate directly with each other — the dispatcher handles all routing and chaining.

---

## Overview

The dispatcher is a **reactive multi-router** with skill-first routing:

1. **User sends a message** → dispatcher checks the **skill routing table** first
2. **Skill match found?** → invoke the skill via the **Skill tool** and respond to user
3. **No skill match?** → dispatcher picks the best **agent** by priority
4. **Agent executes** → returns output to the dispatcher
5. **Dispatcher reads the output** → decides if another agent should be chained
6. **Repeat** until done or max depth reached

Agents help the dispatcher by including **suggestions** in their output when they detect work for other agents.

---

## Skill-First Routing

Skills are checked **before** agents. They handle complex, multi-step workflows that were extracted from agents for better performance.

### How it works

- The dispatcher maintains a **skill routing table** (defined in `DISPATCHER.md`) with trigger phrases in multiple languages.
- If a user message matches a skill trigger, the skill is invoked via the **Skill tool** (not the Agent tool). The dispatcher does NOT also invoke the source agent.
- Skills run in the **main conversation context**, preserving multi-turn state. This is different from agents, which run as subprocesses.
- If no skill matches, the dispatcher falls through to the **agent routing table**.

### Skill-to-agent chaining

Skills can still produce output that triggers agent chaining:
- A skill may include `### Suggested next agent` in its output (e.g., `/onboarding` may suggest Connector to link newly created notes).
- The dispatcher reads this output and applies the same chaining rules as for agents (check registry, check call chain, max depth 3).
- Skills count as step 1 in the call chain when they produce agent suggestions.

### List of skills

See `.platform/references/agents.md` (Skills section) for the full table of skills, their source agents, and purposes.

---

## How Agents Signal the Dispatcher

When an agent detects work that another agent should handle, it includes a section at the end of its output:

```markdown
### Suggested next agent
- **Agent**: {name from agents-registry.md}
- **Reason**: {what needs to be done and why}
- **Context**: {relevant details the next agent would need — note titles, folder paths, specific issues}
```

Multiple suggestions are allowed — list them all. The dispatcher prioritizes and decides which (if any) to invoke.

### Examples

```markdown
### Suggested next agent
- **Agent**: architect
- **Reason**: No area exists for "Personal Finance" — 3 notes were placed in Inbox as fallback
- **Context**: Notes: "Monthly Budget March.md", "Savings Goals.md", "Expense Tracking.md". Suggest creating 02-Areas/Personal Finance/ with sub-folders and MOC.
```

```markdown
### Suggested next agent
- **Agent**: connector
- **Reason**: 5 recently filed notes about "Machine Learning" have no cross-links
- **Context**: Notes in 03-Resources/Technology/ML/. They reference shared concepts (gradient descent, neural networks) but have zero wikilinks between them.

### Suggested next agent
- **Agent**: architect
- **Reason**: MOC for Machine Learning is missing
- **Context**: There are now 8 notes under this topic but no MOC in MOC/ folder.
```

### Suggesting a New Agent

When an agent detects that the user needs functionality that no existing agent provides, it can suggest creating a new custom agent:

```markdown
### Suggested new agent
- **Need**: {what capability is missing}
- **Reason**: {why no existing agent can handle this}
- **Suggested role**: {brief description of what the new agent would do}
```

The dispatcher reads this and may invoke the **Architect** to start the custom agent creation flow. This is NOT automatic. The dispatcher should confirm with the user first:

> "The [agent] noticed you might benefit from a custom agent for [need]. Would you like me to create one?"

---

## Dispatcher Decision Logic

After each agent returns, the dispatcher:

1. **Reads the output** — looks for `### Suggested next agent` sections
2. **Consults `agents-registry.md`** — validates the suggested agent exists and is `active`
3. **Checks the call chain** — is this agent already in the chain? Is max depth reached?
4. **Checks for `### Suggested new agent`** -- if present, asks the user if they want the Architect to create a custom agent
5. **Decides**: invoke next agent OR return results to user

The dispatcher can also chain agents **without an explicit suggestion** if the output clearly matches another agent's capabilities (e.g., notes created → Sorter might be needed).

---

## Call Chain Tracking

Every user request has a **call chain** — the ordered list of agents invoked so far.

### Rules

1. **Start**: chain is empty `[]`
2. **After each agent returns**: append its name to the chain (the chain always lists agents already invoked, in order)
3. **Pass the chain**: when invoking the next agent, tell it the chain and its position — `"Call chain so far: [scribe, architect]. You are step 3 of max 3."`
4. **No duplicates**: never invoke the same agent twice in one chain
5. **No circular patterns**: if Agent A suggests Agent B and B is already in the chain, skip
6. **Max depth: 3**: no more than 3 agents per user request
7. **On overflow**: return results to user with a note about what was deferred

### What Happens at Max Depth

If the dispatcher would need a 4th agent, it:
- Returns the current results to the user
- Includes a summary of what was deferred: _"The Connector also detected 5 orphan notes that need linking — you can say 'connect the notes' to handle that."_

---

## Custom Agent Lifecycle

Custom agents are created by the Architect and stored in `.platform/agents/`. They participate fully in the orchestration system:

1. **Creation**: the Architect creates the agent file, adds a row to `agents-registry.md`, and updates `agents.md`
2. **Discovery**: the platform auto-discovers the agent from its frontmatter in `.platform/agents/`
3. **Routing**: the dispatcher checks `agents-registry.md` for custom agents when no core agent matches
4. **Chaining**: custom agents can suggest (and be suggested by) any other agent, following the same protocol
5. **Maintenance**: the Librarian audits custom agents during vault health checks. For every row in agents-registry.md with status=active, the corresponding file must exist in `.platform/agents/`
6. **Deletion**: only the Architect can remove a custom agent (with user confirmation). The agent file is deleted, and the registry row is set to `disabled`

---

## Validation Gate

After an agent completes a task, the dispatcher performs a lightweight output validation before returning the result to the user or chaining the next agent.

### When to validate

Validate whenever the agent was asked to produce a specific output format (e.g., a meeting note with 4 required sections, a security report, a structured triage digest). Validation is NOT needed for conversational responses.

### Validation criteria

The dispatcher checks that:
1. Output contains the expected structure (required sections present)
2. Output does not contain placeholder text like `{{...}}` where real values were expected
3. Output does not contradict the user's original request

### Retry protocol

If validation fails:
1. **Retry once** — re-invoke the same agent with specific feedback: "Your output was missing [X]. Please regenerate with [X] included."
2. **Retry twice** — if the second attempt also fails, escalate to the user with: "The agent was unable to produce the expected output after 2 attempts. Here is what it generated: [output]. Would you like to try again or accept this result?"
3. **Max 2 retries** — never retry more than twice automatically. Always involve the user after 2 failures.

### What counts as a validation failure

- Required section is completely absent (e.g., `## Action Items` missing from meeting notes)
- Output is less than 20% of the expected length for the task type
- Output explicitly says "I cannot" or "I don't have access" when the task was within the agent's defined capabilities

---

## Parallel Dispatch

Some user requests involve independent sub-tasks that can be executed by multiple agents simultaneously rather than sequentially. The dispatcher should recognize these patterns and invoke agents in parallel.

### When to use parallel dispatch

- User asks for a **combined report** from multiple sources (e.g., "summarize my emails AND calendar for this week" → Postman + Calendar scan run in parallel)
- Multiple **independent cleanup tasks** exist (e.g., after inbox triage: Connector links notes while Sorter files the rest — independent operations)
- A **research task** requires multiple search threads that don't depend on each other

### How to signal parallel dispatch

Agents can signal that their suggested next steps are **parallel-eligible** by using the `parallel: true` flag in their suggestion:

```markdown
### Suggested next agent
- **Agent**: connector
- **Reason**: 5 ML notes need cross-linking
- **Context**: Notes filed to 03-Resources/Technology/ML/
- **parallel**: true

### Suggested next agent
- **Agent**: architect
- **Reason**: MOC missing for ML cluster
- **Context**: No MOC in MOC/ folder for this topic
- **parallel**: true
```

When both suggestions are marked `parallel: true`, the dispatcher may invoke both agents simultaneously if the platform supports concurrent subagent execution.

### Parallel dispatch constraints

- Maximum **2 agents** in parallel (to avoid context overload)
- Never run agents with **write conflicts** in parallel (e.g., two agents writing to the same file)
- If one parallel agent fails, the other continues independently — do not block

---

## What Agents Should NOT Do

- ❌ **Do NOT reference `Meta/agent-messages.md`** — the shared message board is deprecated
- ❌ **Do NOT edit other agents' prompt/config files** (e.g., `.platform/agents/*.md`) — normal vault notes/MOC edits are still allowed per your responsibilities; all coordination goes through the dispatcher
- ❌ **Do NOT block waiting for another agent** — finish your task and suggest next steps in your output
- ❌ **Do NOT call other agents** — only the dispatcher invokes agents

---

## Migration from Legacy System

If a vault still has the old `Meta/agent-messages.md` file:
- The **Librarian** will rename it to `Meta/agent-messages-DEPRECATED.md` during maintenance
- Agents should ignore this file entirely — all coordination now flows through the dispatcher

---

## Agent State (Post-it Protocol)

Every agent has a personal post-it file at `Meta/states/{agent-name}.md`. This provides continuity between executions.

### Rules

- **One file per agent** — named after the agent (e.g., `Meta/states/scribe.md`)
- **Always written** — every agent writes its post-it at the end of every execution, no exceptions
- **Overwrites previous** — each execution replaces the previous post-it (it is not a log)
- **Max 30 lines** — agents must keep the body under 30 lines to prevent bloat
- **Read at start** — agents read their post-it at the start of execution for context
- **Private** — the dispatcher does not read or write agent post-its. Only the owning agent touches its own file
- **Multi-step flows** — agents that run multi-step conversations (e.g., Architect onboarding) use the post-it to track their current phase and collected answers, so they can resume on re-invocation

### Format

```markdown
---
agent: {agent-name}
last-run: "YYYY-MM-DDTHH:MM:SS"
---

## Post-it

[Agent's notes — max 30 lines]
```

---

## Reference Files

- **Agent registry**: `.platform/references/agents-registry.md` — the single source of truth for all agents
- **Agent directory**: `.platform/references/agents.md` — detailed descriptions of each agent's responsibilities
