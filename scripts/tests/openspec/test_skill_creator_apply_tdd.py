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


def _assert_design_covers_task(task_id: str, required_fragments: list[str], context: str) -> None:
    design = _read("design.md")
    tasks = _read_tasks()
    _assert_contains_all(design, required_fragments)
    _assert_task_completion(tasks, task_id, context)


def _assert_tasks_covers_task(task_id: str, required_fragments: list[str], context: str) -> None:
    tasks = _read_tasks()
    _assert_contains_all(tasks, required_fragments)
    _assert_task_completion(tasks, task_id, context)


def _task_header(task_id: str) -> str:
    return f"**{task_id}**"


def _task_fragments(task_id: str, *fragments: str) -> list[str]:
    return [_task_header(task_id), *fragments]


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
    _assert_design_covers_task(
        "2.1",
        [
            "## Technical Decisions",
            "**Alternatives considered:**",
            "Decision: Baseline-and-Adapt Reuse Model",
            "Decision: Copilot SDK as Normative Default, Provider Examples as Labeled Alternatives",
            "Decision: Non-Normative Labeling for Historical Claude References",
        ],
        "technical decisions and alternatives are documented",
    )


def test_2_2_map_data_flow_and_component_impact():
    _assert_design_covers_task(
        "2.2",
        [
            "## Architecture",
            "### Components Affected",
            "README.md",
            "skills/tuning/skill-optimizer.md",
            "skills/tuning/benchmark-runner.md",
            "skills/tuning/local-calibration.md",
            "agents/*/agent.md",
            "## Data Flow",
            "upstream `skill-creator` change",
            "Copilot SDK defaults and examples are normalized",
        ],
        "data flow and component impact are mapped",
    )


def test_2_3_map_tests_to_spec_scenarios():
    _assert_design_covers_task(
        "2.3",
        [
            "## Testing Strategy",
            "Skill-Authoring Governance / Traceable Upstream Baseline",
            "Skill-Authoring Governance / Upstream Refresh Workflow",
            "Skill-Authoring Governance / Reuse Boundary Across Surfaces",
            "Copilot Runtime / Normative Runtime Guidance",
            "Copilot Runtime / Example Command Review",
            "Copilot Runtime / Historical Reference De-Emphasis",
        ],
        "testing strategy maps to all spec scenarios",
    )


def test_3_1_plan_provenance_labeling_updates_in_tuning_docs():
    _assert_tasks_covers_task(
        "3.1",
        _task_fragments(
            "3.1",
            "skills/tuning/skill-optimizer.md",
            "skills/tuning/benchmark-runner.md",
            "skills/tuning/local-calibration.md",
            "provenance/default-runtime edits",
        ),
        "provenance labeling updates are planned in tuning docs",
    )


def test_3_2_plan_runtime_default_normalization_in_top_level_docs():
    _assert_tasks_covers_task(
        "3.2",
        _task_fragments(
            "3.2",
            "README.md",
            "relevant agent docs",
            "Copilot SDK-first defaults",
            "labeled provider alternatives",
        ),
        "runtime-default normalization is planned for top-level docs",
    )


def test_3_3_plan_historical_reference_de_emphasis_pass():
    _assert_tasks_covers_task(
        "3.3",
        _task_fragments(
            "3.3",
            "unlabeled Claude CLI references",
            "historical/non-default",
            "detection criteria and pass/fail conditions",
        ),
        "historical-reference de-emphasis audit is planned",
    )


def test_4_1_verify_proposal_to_spec_coverage():
    tasks = _read_tasks()
    proposal = _read("proposal.md")
    governance_spec = _read("specs/skill-authoring-governance/spec.md")
    runtime_spec = _read("specs/copilot-sdk-runtime-alignment/spec.md")

    _assert_contains_all(
        proposal,
        [
            "Define repository requirements for importing and reusing upstream `skill-creator` guidance",
            "Define Copilot SDK-first runtime expectations",
        ],
    )
    _assert_contains_all(
        governance_spec,
        [
            "### Requirement: Upstream Skill-Creator Provenance Contract",
            "### Requirement: Controlled Upstream Refresh Workflow",
        ],
    )
    _assert_contains_all(
        runtime_spec,
        [
            "### Requirement: Copilot SDK-First Runtime Contract",
            "### Requirement: Runtime Example Consistency",
        ],
    )
    _assert_task_completion(
        tasks,
        "4.1",
        "proposal-to-spec coverage is verified",
    )


def _assert_requirement_present(spec_text: str, requirement_name: str) -> None:
    assert f"### Requirement: {requirement_name}" in spec_text
