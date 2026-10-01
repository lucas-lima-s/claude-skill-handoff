from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REFERENCES_DIR = REPO_ROOT / "references"


def test_both_templates_exist_and_are_fenced():
    for filename in ("template.md", "template-portable.md"):
        text = (REFERENCES_DIR / filename).read_text(encoding="utf-8")
        assert "```" in text, filename


def test_template_sections():
    text = (REFERENCES_DIR / "template.md").read_text(encoding="utf-8")
    labels = ["APPROVED PLAN", "CURRENT STATE", "DECISIONS / INVARIANTS", "NEXT STEP", "VALIDATION"]
    positions = [text.index(label) for label in labels]
    assert positions == sorted(positions)


def test_portable_template_sections():
    text = (REFERENCES_DIR / "template-portable.md").read_text(encoding="utf-8")
    labels = [
        "TASK:",
        "WHY THIS HANDOFF:",
        "CURRENT STATE:",
        "REFERENCES",
        "DECISIONS / CONSTRAINTS:",
        "NEXT STEP:",
        "VALIDATION:",
    ]
    positions = [text.index(label) for label in labels]
    assert positions == sorted(positions)


def test_generic_ticket_placeholder():
    skill_md = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
    template = (REFERENCES_DIR / "template.md").read_text(encoding="utf-8")
    assert "TICKET-123" in skill_md
    assert "TICKET-123" in template


def test_rendered_text_has_no_em_dash():
    for path in (REFERENCES_DIR / "template.md", REFERENCES_DIR / "template-portable.md", REPO_ROOT / "SKILL.md"):
        assert "\u2014" not in path.read_text(encoding="utf-8"), path.name


def test_description_fits_listing_budget():
    text = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
    description = re.search(r"^description:\s*(.+)$", text, re.MULTILINE).group(1).strip().strip("'\"")
    assert len(description) <= 300, len(description)
    assert "ai-memory-handoff" in description
