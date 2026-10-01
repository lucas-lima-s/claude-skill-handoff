# Changelog

## [Unreleased]

- Shorter `description` (under 300 characters) and an explicit scope split with ai-memory's `ai-memory-handoff` routing skill.
- Suggested-skills guidance in the render step and a matching `next_steps` bullet.
- No em dashes in the rendered templates or the closing instruction.

## [1.0.0] - 2026-08-25

- Initial public release.
- Two modes: same-project continuity (ai-memory auto-inject) and portable (self-contained block).
- Sanitization pass redacts secret-shaped strings before any handoff touches disk or the terminal.
