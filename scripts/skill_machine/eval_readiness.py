from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def validate_eval_readiness(*, eval_path: Path) -> Dict[str, Any]:
    payload = json.loads(eval_path.read_text(encoding="utf-8"))
    cases = payload.get("cases", [])
    reasons: List[str] = []
    if not cases:
        reasons.append("Eval dataset must include at least one case.")
    has_positive = False
    has_negative = False
    for case in cases:
        assertions = case.get("assertions", {}) if isinstance(case, dict) else {}
        if assertions.get("must_detect") is True:
            has_positive = True
        if assertions.get("must_not_detect") is True:
            has_negative = True
    if cases and not has_positive:
        reasons.append("Eval dataset must include at least one positive case (must_detect).")
    if cases and not has_negative:
        reasons.append("Eval dataset must include at least one negative case (must_not_detect).")
    return {"ready": len(reasons) == 0, "reasons": reasons}
