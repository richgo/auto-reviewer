import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
CHANGE_DIR = REPO_ROOT / "openspec" / "changes" / "skill-creator-copilot-sdk"


def _read(relative_path: str) -> str:
    return (CHANGE_DIR / relative_path).read_text(encoding="utf-8")


def _task_is_checked(tasks_text: str, task_id: str) -> bool:
    pattern = rf"- \[x\] \*\*{re.escape(task_id)}\*\*"
    return re.search(pattern, tasks_text) is not None


def _assert_contains_all(text: str, fragments: list[str]) -> None:
    for fragment in fragments:
        assert fragment in text


def test_1_1_finalize_proposal_scope_and_risk_framing():
    proposal = _read("proposal.md")
    tasks = _read("tasks.md")

    _assert_contains_all(
        proposal,
        [
            "## Intent",
            "### In Scope",
            "### Out of Scope",
            "## Risks",
            "upstream `skill-creator` guidance",
            "Copilot SDK-first runtime expectations",
            "README.md",
            "skills/tuning/",
        ],
    )
    assert _task_is_checked(
        tasks, "1.1"
    ), "Task 1.1 must be checked after proposal scope/risk framing is finalized."
