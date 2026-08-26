# claude-skill-handoff

Claude Code skill that packages a session's working context into a dense continuation prompt for the next session, either auto-injected into the same project or emitted as a self-contained portable block.

## Why

Context windows end. The next session normally restarts from zero: re-reading the plan, re-deriving what branch it's on, re-discovering which decisions were already made. This skill turns the live session state into a dense, verified prompt so the next session opens already knowing the branch, PRs, commits, decisions, and the next concrete step.

## Two modes

| Mode | What it does |
|---|---|
| **Same-project continuity** | Writes a durable file under `~/.claude/plans/handoffs/` and registers an ai-memory handoff that the SessionStart hook injects into the next session automatically. |
| **Portable** | Produces a self-contained, paste-able block for another repo, another agent/harness, or a colleague. Never registered with ai-memory. |

## What makes it non-trivial

Every volatile fact — branch, commit hash, PR number, plan path — is re-verified with a command before it is written, never taken from conversational memory. A sanitization pass redacts anything matching secret shapes (`sk-`, `ghp_`, `AKIA`, `Bearer …`, credentials embedded in connection strings) before the content touches disk or the terminal.

## Install

```
mkdir -p ~/.claude/skills
cp -r claude-skill-handoff ~/.claude/skills/handoff
```

Restart or start a Claude Code session, then confirm with `/handoff`.

## Usage

Trigger with `/handoff`, or with natural language in either English or Portuguese — the skill's `description:` frontmatter carries trigger phrases in both languages, since it was built for daily bilingual use:

- "prompt para próxima sessão", "gera handoff", "salva o contexto pra próxima sessão" (mode 1)
- "manda esse contexto pra outro repo/agente", "handoff portátil", "passa isso pra um colega" (mode 2)
- Accepting an offered handoff after finishing a phase of a multi-phase plan also triggers mode 1.

## Sample output

A rendered mode-2 portable handoff, with fictional data:

```
[Portable handoff — generated on 2026-08-25. This block is self-contained; it assumes no access to this project, this repository, or the local ai-memory instance.]

TASK: Add a token-bucket rate limiter to the public API gateway, keyed by API key, with a 429 response and a Retry-After header.

WHY THIS HANDOFF: another repository

CURRENT STATE:
- Rate limiter core implemented and unit-tested on branch feature/ticket-123-rate-limiter.
- Wired into the gateway middleware chain; integration test pending.

REFERENCES (paths/URLs, not copies — only include what the recipient can actually open):
- https://github.com/example-org/api-gateway/pull/42
- https://github.com/example-org/api-gateway/blob/a1b2c3d/src/middleware/rate_limit.py

DECISIONS / CONSTRAINTS:
- Bucket state lives in-memory per instance, not in a shared store — deliberate for this phase, do not swap in Redis without a new decision.

NEXT STEP:
- Add the integration test exercising a burst above the bucket size.
- Document the new Retry-After header in the API reference.

SUGGESTED SKILLS FOR THE RECIPIENT:
- (none specific)

VALIDATION:
- pytest -q tests/test_rate_limit.py
```

## Dependencies

| Dependency | Required for |
|---|---|
| `ai-memory` MCP server + its SessionStart hook | Mode 1 only, and optional even there |

Mode 2 has zero coupling to ai-memory. Mode 1 degrades gracefully when the MCP server is absent: the durable file and the paste-able block are still produced, only the auto-inject leg is lost.

## License

MIT — see [LICENSE](LICENSE).
