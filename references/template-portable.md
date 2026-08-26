# Portable handoff template

Unlike [template.md](template.md), this template assumes the reader has **no
access to this project, this repo, or this ai-memory instance**. Render in
the language of the conversation. Replace `<...>` placeholders; drop sections
that don't apply — never leave empty headers. Every fact must be
self-sufficient: no "see the master plan" pointing at a path the reader
cannot open unless that path is itself something portable (a public repo, a
URL, a doc attached alongside this block).

```
[Portable handoff — generated on <yyyy-mm-dd>. This block is self-contained; it assumes no access to this project, this repository, or the local ai-memory instance.]

TASK: <self-sufficient task description, without depending on prior context>

WHY THIS HANDOFF: <another repository | another agent/harness | a colleague | a parallel subtask>

CURRENT STATE:
- <what was already done, one line per item>

REFERENCES (paths/URLs, not copies — only include what the recipient can actually open):
- <path or URL 1>

DECISIONS / CONSTRAINTS:
- <what must not be redone or reverted, and why>

NEXT STEP:
- <concrete action 1>
- <concrete action 2>

SUGGESTED SKILLS FOR THE RECIPIENT:
- <skill name> — <why it applies here>
[Omit when no specific skill applies.]

VALIDATION:
- <exact test command>
```

## Notes for the renderer

- Never assume the receiving agent shares this project's ticket/branch
  conventions, issue-tracker labels, or internal terminology — spell things
  out that `template.md` can leave implicit.
- "REFERENCES" only lists paths/URLs the destination can actually reach.
  A path under this machine's `~/.claude/plans/` is not portable; a public
  repo URL or a path inside the repo being handed off is.
- Run the sanitization pass (SKILL.md step 3) on this content before
  emitting it — portable handoffs are the ones most likely to leave the
  machine.
