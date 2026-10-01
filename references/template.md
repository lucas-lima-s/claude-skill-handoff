# Handoff prompt template

Skeleton for a same-project continuation prompt. Render it in the language of the conversation; translate the section labels if needed, but keep their order and density. Replace every `<...>` placeholder; drop sections that do not apply instead of leaving an empty header. The next session must be able to start working without re-deriving anything.

```
[If this session is NOT the continuation of <TICKET-123>, ignore this handoff; the full content is persisted at <path under ~/.claude/plans/handoffs/>.]

<TICKET-123 | epic name>: "<task title>". Continue with <Phase N | next step>.

APPROVED PLAN (source of truth, read it in full first): <path to the master plan under ~/.claude/plans/> (see section "<Phase N>")
Previous phase plan (pattern reference): <path, if any>

SUGGEST STARTING IN PLAN MODE: <real unknowns of the next phase: what must be investigated or validated in the code BEFORE implementing>.
[Omit this block when there are no unknowns.]

CURRENT STATE (<finished phases, e.g. "Phases 1, 2 and 3 done and pushed">):
- Phase 1 <branch> (<deliverables in one line>). PR <#NNN | URL>. Commit <hash>.
- Phase 2 <branch> ← <base-branch> (<deliverables>). PR <#NNN>. Commit <hash>.
- ...

DECISIONS / INVARIANTS (do not touch):
- <decision made and why, in 1 line>
- <invariant: "X is already correct, do not change it">
- ...

NEXT STEP (<scope of the next phase>):
- <concrete action 1>
- <concrete action 2>
- ...

SUGGESTED SKILLS FOR THE NEXT PHASE:
- <skill name>: <why it applies here>
[Omit this block when no specific skill applies.]

VALIDATION:
- <exact test command, e.g. `pytest -q tests/`>
- <lint, build, E2E when applicable>
```

## Notes for the renderer

- Branch/PR/commit lines come from `git log` / `git branch` output captured in step 1 of the flow, never from conversational memory.
- "DECISIONS / INVARIANTS" carries anything a fresh session would plausibly redo wrong: rejected approaches, review findings already honored, gates that must stay.
- The first bracketed line doubles as the single-use mitigation: an unrelated session that consumes the handoff knows to ignore it and where the durable copy lives.
