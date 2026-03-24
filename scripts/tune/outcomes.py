from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class OutcomeStatus(str, Enum):
    PROMOTABLE = "promotable"
    GATED = "gated"
    NEEDS_REVIEW = "needs_review"


@dataclass(frozen=True)
class TuningOutcome:
    skill_name: str
    best_model: str
    best_pass_rate: float
    target_pass_rate: float
    status: OutcomeStatus


def build_tuning_outcome(
    *,
    skill_name: str,
    best_model: str,
    best_pass_rate: float,
    target_pass_rate: float,
    benchmark_ran: bool,
    benchmark_passed: bool,
) -> TuningOutcome:
    if best_pass_rate < target_pass_rate:
        status = OutcomeStatus.NEEDS_REVIEW
    elif benchmark_ran and not benchmark_passed:
        status = OutcomeStatus.GATED
    else:
        status = OutcomeStatus.PROMOTABLE
    return TuningOutcome(
        skill_name=skill_name,
        best_model=best_model,
        best_pass_rate=best_pass_rate,
        target_pass_rate=target_pass_rate,
        status=status,
    )


def write_outcome(*, path: Path, outcome: TuningOutcome) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "skill_name": outcome.skill_name,
                "best_model": outcome.best_model,
                "best_pass_rate": outcome.best_pass_rate,
                "target_pass_rate": outcome.target_pass_rate,
                "status": outcome.status.value,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
