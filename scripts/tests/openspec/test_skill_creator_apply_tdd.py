import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
CHANGE_DIR = REPO_ROOT / "openspec" / "changes" / "skill-creator-copilot-sdk"


def _read(relative_path: str) -> str:
    return (CHANGE_DIR / relative_path).read_text(encoding="utf-8")


def _read_tasks() -> str:
    return _read("tasks.md")


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


def _assert_task_completion(tasks_text: str, task_id: str, context: str) -> None:
    assert _task_is_checked(
        tasks_text, task_id
    ), f"Task {task_id} must be checked after {context}."


def test_1_1_finalize_proposal_scope_and_risk_framing():
    proposal = _read("proposal.md")
    tasks = _read_tasks()

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
    _assert_task_completion(tasks, "1.1", "proposal scope/risk framing is finalized")


def test_1_2_add_skill_authoring_governance_capability_delta():
    spec = _read("specs/skill-authoring-governance/spec.md")
    tasks = _read_tasks()

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
    _assert_task_completion(
        tasks,
        "1.2",
        "skill-authoring governance spec delta is finalized",
    )


def test_1_3_add_copilot_runtime_alignment_capability_delta():
    spec = _read("specs/copilot-sdk-runtime-alignment/spec.md")
    tasks = _read_tasks()

    _assert_delta_requirement(
        spec,
        "Copilot SDK-First Runtime Contract",
        "Normative Runtime Guidance",
    )
    _assert_delta_requirement(
        spec,
        "Runtime Example Consistency",
        "Example Command Review",
    )
    _assert_delta_requirement(
        spec,
        "Historical Reference De-Emphasis",
        "Mixed Historical Documentation",
    )
    _assert_task_completion(
        tasks,
        "1.3",
        "Copilot runtime alignment spec delta is finalized",
    )


def test_2_1_document_technical_decisions_and_alternatives():
    design = _read("design.md")
    tasks = _read_tasks()

    _assert_contains_all(
        design,
        [
            "## Technical Decisions",
            "**Alternatives considered:**",
            "Decision: Baseline-and-Adapt Reuse Model",
            "Decision: Copilot SDK as Normative Default, Provider Examples as Labeled Alternatives",
            "Decision: Non-Normative Labeling for Historical Claude References",
        ],
    )
    _assert_task_completion(
        tasks,
        "2.1",
        "technical decisions and alternatives are documented",
    )
