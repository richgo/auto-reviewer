from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict

from .workflow_state import resolve_skill_state


def run_create_stage(
    *,
    skill_name: str,
    skills_dir: Path,
    evals_dir: Path,
    state_dir: Path,
    persist_state: bool = False,
    generate_eval_stub: bool = False,
) -> Dict[str, str]:
    state = resolve_skill_state(
        skill_name=skill_name,
        skills_dir=skills_dir,
        evals_dir=evals_dir,
        state_dir=state_dir,
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
                    "status": "create_started",
                    "updated_at": timestamp,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
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
    return {
        "skill": state.skill_name,
        "skill_path": str(state.skill_path),
        "eval_path": str(state.eval_path),
        "state_path": str(state.state_path),
    }
