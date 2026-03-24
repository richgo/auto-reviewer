from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SkillWorkflowState:
    skill_name: str
    skill_path: Path
    eval_path: Path
    state_path: Path


def resolve_skill_state(
    *,
    skill_name: str,
    skills_dir: Path,
    evals_dir: Path,
    state_dir: Path,
) -> SkillWorkflowState:
    skill_path = skills_dir / skill_name / "SKILL.md"
    if not skill_path.exists():
        raise FileNotFoundError(f"Skill file not found: {skill_path}")
    eval_path = evals_dir / f"{skill_name}.json"
    if not eval_path.exists():
        raise FileNotFoundError(f"Eval file not found: {eval_path}")

    return SkillWorkflowState(
        skill_name=skill_name,
        skill_path=skill_path,
        eval_path=eval_path,
        state_path=state_dir / f"{skill_name}.json",
    )
