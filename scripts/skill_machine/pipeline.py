from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict

from .eval_readiness import validate_eval_readiness as run_eval_readiness
from .workflow_state import resolve_skill_state


def run_create_stage(
    *,
    skill_name: str,
    skills_dir: Path,
    evals_dir: Path,
    state_dir: Path,
    persist_state: bool = False,
    generate_eval_stub: bool = False,
    validate_eval_readiness: bool = False,
    validation_reports_dir: Path | None = None,
) -> Dict[str, str]:
    state = resolve_skill_state(
        skill_name=skill_name,
        skills_dir=skills_dir,
        evals_dir=evals_dir,
        state_dir=state_dir,
    )
    status = "create_started"
    if generate_eval_stub and not state.eval_path.exists():
        state.eval_path.parent.mkdir(parents=True, exist_ok=True)
        state.eval_path.write_text(
            json.dumps(
                {
                    "skill": state.skill_name,
                    "cases": [],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    eval_ready = True
    readiness_reasons = []
    if validate_eval_readiness:
        readiness = run_eval_readiness(eval_path=state.eval_path)
        eval_ready = bool(readiness["ready"])
        readiness_reasons = list(readiness["reasons"])
        if not eval_ready:
            status = "create_eval_not_ready"
    validation_artifact_path = ""
    if validation_reports_dir is not None:
        validation_artifact_path = str(validation_reports_dir / f"{state.skill_name}.json")
        artifact_path = Path(validation_artifact_path)
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        artifact_path.write_text(
            json.dumps(
                {
                    "skill": state.skill_name,
                    "eval_path": str(state.eval_path),
                    "eval_ready": eval_ready,
                    "reasons": readiness_reasons,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    if persist_state:
        timestamp = datetime.utcnow().isoformat() + "Z"
        state.state_path.parent.mkdir(parents=True, exist_ok=True)
        state.state_path.write_text(
            json.dumps(
                {
                    "skill": state.skill_name,
                    "skill_path": str(state.skill_path),
                    "eval_path": str(state.eval_path),
                    "status": status,
                    "updated_at": timestamp,
                    "eval_ready": eval_ready,
                    "eval_readiness_reasons": readiness_reasons,
                    "validation_artifact_path": validation_artifact_path,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    return {
        "skill": state.skill_name,
        "skill_path": str(state.skill_path),
        "eval_path": str(state.eval_path),
        "state_path": str(state.state_path),
        "eval_ready": eval_ready,
        "validation_artifact_path": validation_artifact_path,
    }


def run_tune_stage(
    *,
    skill_name: str,
    skills_dir: Path,
    evals_dir: Path,
    state_dir: Path,
) -> Dict[str, str]:
    state = resolve_skill_state(
        skill_name=skill_name,
        skills_dir=skills_dir,
        evals_dir=evals_dir,
        state_dir=state_dir,
    )
    return {
        "skill": state.skill_name,
        "skill_path": str(state.skill_path),
        "eval_path": str(state.eval_path),
        "state_path": str(state.state_path),
    }
