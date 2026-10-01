# handoff: Setup

## What it needs

Mode 1 (same-project continuity) and mode 2 (portable) have different dependencies.

| Dependency | Why | How to check | Required for |
|---|---|---|---|
| ai-memory MCP server (`ai-memory` in the MCP config) | `memory_handoff_begin` registers the handoff the next session auto-loads | `memory_status` tool responds | Mode 1 only |
| ai-memory SessionStart hook in `~/.claude/settings.json` | Consumes the pending handoff at session start (including after `/clear`) and prepends it to the new context | `hooks.SessionStart` contains a command running `ai-memory.exe hook --event session-start` | Mode 1 only |
| `~/.claude/plans/handoffs/` directory | Durable storage for same-project handoff prompts | Created on first use; safe to create manually | Mode 1 |
| `~/.claude/plans/handoffs/portable/` directory | Durable storage for portable handoff prompts (the paste-able block is the actual delivery mechanism; this is just your own local record) | Created on first use; safe to create manually | Mode 2 |

No environment variables, no Python runtime, no external APIs; the pytest suite in `tests/` only validates repository hygiene and is not needed to run the skill.

## For another user

1. Install ai-memory (server + hooks) per its own docs; this skill only *calls* it.
2. Copy `~/.claude/skills/handoff/` into your `~/.claude/skills/`.
3. Done. Without ai-memory the skill degrades gracefully: it still writes the durable file and prints the paste-able block; only the auto-inject leg is lost.

## Known limitations

- The skill cannot run `/clear` (CLI built-in). Flow is: `/handoff` → user runs `/clear` or opens a new session → SessionStart hook injects the context.
- ai-memory handoffs are **single-use**: the next session on the project consumes it regardless of topic. Mitigation: the durable file always persists and the handoff's first line tells an unrelated session to ignore it and where the full copy lives.
- Handoff scoping follows ai-memory's project resolution: sibling checkouts that ai-memory resolves to the same project share one handoff queue.

## Notes

`pyproject.toml` carries a `[tool.black]` block purely so external formatters and hygiene validators that check for it agree with ruff's line length; ruff remains the actual lint and format tool used in CI.
