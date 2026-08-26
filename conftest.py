from __future__ import annotations

import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SKIP_DIR_NAMES = {".git", ".venv"}


def pytest_sessionfinish(session, exitstatus):
    for path in REPO_ROOT.rglob("__pycache__"):
        if not path.is_dir():
            continue
        if any(part in SKIP_DIR_NAMES for part in path.relative_to(REPO_ROOT).parts):
            continue
        shutil.rmtree(path, ignore_errors=True)
