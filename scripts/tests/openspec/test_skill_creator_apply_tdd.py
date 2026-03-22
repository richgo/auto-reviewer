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


def _assert_delta_requirement(text: str, requirement: str, scenario: str) -> None:
    _assert_contains_all(
        text,
        [
            "## ADDED Requirements",
            f"### Requirement: {requirement}",
            f"#### Scenario: {scenario}",
            "SHALL",
            "GIVEN",
            "WHEN",
            "THEN",
        ],
    )


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


def test_1_2_add_skill_authoring_governance_capability_delta():
    spec = _read("specs/skill-authoring-governance/spec.md")
    tasks = _read("tasks.md")

    _assert_delta_requirement(
        spec,
        "Upstream Skill-Creator Provenance Contract",
        "Traceable Upstream Baseline",
    )
    _assert_delta_requirement(
        spec,
        "Controlled Upstream Refresh Workflow",
        "Upstream Guidance Changes",
    )
    _assert_delta_requirement(
        spec,
        "Reuse Boundary Across Authoring Surfaces",
        "Skill Authoring Contract Review",
    )
    assert _task_is_checked(
        tasks, "1.2"
    ), "Task 1.2 must be checked after skill-authoring governance spec delta is finalized."
