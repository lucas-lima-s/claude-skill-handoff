---
name: handoff
description: Generate a next-session continuation prompt (handoff). Two modes — (1) same-project continuity: persist to a durable file and register with ai-memory so the next session on THIS project auto-loads it via the SessionStart hook; (2) portable handoff: when the destination is another repo, another agent/harness, a colleague, or a parallel subtask, produce a self-contained paste-able markdown block instead, with no ai-memory registration. Use when the user triggers /handoff, or asks in pt-BR for "prompt para próxima sessão", "prompt para próxima fase", "gera handoff", "gera o handoff", "salva o contexto pra próxima sessão", "contexto pra continuar depois", "prompt de continuação", or accepts an offered handoff after finishing a phase of a multi-phase plan (mode 1); or "manda esse contexto pra outro repo/agente", "handoff portátil", "passa isso pra um colega", "preciso branchar isso numa sessão paralela" (mode 2).
---

# handoff

Package the current session's working context into a continuation prompt for the next session: render it from the template, save it to a durable file, and register it as an ai-memory handoff so the next session receives it automatically — no copy-paste.

## Constraints

- **This skill cannot execute `/clear`.** It is a CLI built-in outside the model's reach. The user runs `/clear` (or opens a new session) themselves; the ai-memory SessionStart hook consumes the pending handoff and prepends its content to the fresh context.
- **Handoffs are single-use.** The next session on this project consumes it, whatever its topic. The durable file is the source of truth; the handoff opens with an ignore-instruction pointing to it (see template).
- **Language:** the generated handoff content is written in the language of the conversation (it is user-facing). Skill instructions, section labels in this file, and code stay in English.
- **Requires** the ai-memory MCP server and its SessionStart hook (see SETUP.md) for mode 1 only. Mode 2 does not depend on ai-memory at all. If `memory_handoff_begin` is unavailable in mode 1, still produce the file and the paste-able block, and tell the user the auto-inject leg is down.

## Detecting the mode

- **Mode 1 (default)**: the destination is the next session of THIS project — no other repo, agent, or person mentioned.
- **Mode 2 (portable)**: the user names a different repo, a different agent/harness, a colleague, or an explicit parallel/branching subtask.

Mode 1 follows the flow below unchanged. Mode 2 keeps step 1 (gather and verify state), but replaces steps 2, 4, 5, 6 as described in "Mode 2 — portable handoff" at the end of this file (step 3, sanitize, applies to both).

## Flow

### 1. Gather session state — validate, don't assume

Collect from the current conversation, then **verify every volatile fact with a command** before writing it:

| Item | Source | Verify with |
|---|---|---|
| Ticket/epic + task title | conversation / branch name | `git branch --show-current` |
| Plan file path(s) | plan-mode system messages (`~/.claude/plans/*.md`) | file exists (Glob/Read) |
| Phase status (done / current / next) | conversation, master plan | read the master plan's phase section |
| Branches, PRs, commit hashes | conversation | `git log --oneline -5`, `git branch`; never from memory |
| Decisions / invariants ("do not touch X") | conversation | — |
| Unknowns for the next phase | conversation, master plan | — |
| Validation/test commands | conversation, component docs | — |

If the next phase has real unknowns, the handoff must recommend starting in plan mode and list the unknowns explicitly.

### 2. Render from the template

Use [references/template.md](references/template.md). Keep the exemplar's density: state per finished phase (branch, PR, commit, one-line deliverables), invariants as imperatives, next-phase scope as concrete bullets. Omit sections that genuinely don't apply (e.g. no PRs yet) instead of leaving empty headers.

### 3. Sanitize before writing

Scan the rendered content for anything that looks like a secret — API keys, tokens (`sk-`, `ghp_`, `AKIA`, `Bearer …`), passwords, credentials embedded in connection strings. Redact matches as `[REDACTED]` before writing to disk or printing the paste-able block. Applies to both modes.

### 4. Persist to a durable file

Write the rendered handoff to:

```
~/.claude/plans/handoffs/<yyyy-mm-dd>_<ticket>-<slug>.md
```

Use the ticket ID (e.g. `TICKET-123`) when there is one, otherwise a short task slug. This file survives even if the ai-memory handoff is consumed by an unrelated session.

### 5. Register the ai-memory handoff

Call `memory_handoff_begin` with:

- `summary`: 2-3 short sentences — what just finished and what state the work is in.
- `next_steps`: compact bullets; the **first** bullet is always `Contexto completo: <full path of the persisted file>`, followed by the concrete next actions.
- `open_questions`: the unknowns from step 1 (empty if none).
- `files_touched`: main files of the session (hint, not exhaustive).

The rendered content (and therefore the summary the next agent reads) must open with the ignore-instruction line from the template, so an unrelated session knows to skip it and where the full context lives.

### 6. Reply to the user

Confirm with proof, then hand over control:

1. Handoff registered (show the `handoff_id`) + file path written.
2. The full paste-able block in a fenced code block (manual fallback).
3. Closing instruction (pt-BR): "Agora é só dar `/clear` (ou abrir uma sessão nova) — o contexto entra sozinho na próxima sessão."

## Mode 2 — portable handoff

1. Render from [references/template-portable.md](references/template-portable.md) instead of `template.md`. Unlike mode 1, assume the reader has zero context on this project's ticket/branch conventions — the block must be self-sufficient.
2. Sanitize (step 3 above applies here too).
3. Persist the rendered block to `~/.claude/plans/handoffs/portable/<yyyy-mm-dd>_<slug>.md` for your own record, but do **not** call `memory_handoff_begin` — that would inject this content into the next session of THIS project, which is not the intended destination.
4. Reply with the full paste-able block in a fenced code block (this is the actual delivery mechanism here, since the destination is unknown to ai-memory) plus the local file path for your own record.
