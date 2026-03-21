import copy
from typing import Any, Dict


def _migrate_assertions(assertions: Dict[str, Any], is_counter_example: bool) -> Dict[str, bool]:
    if is_counter_example:
        return {"no_false_positive": True}

    if "detected_bug" in assertions:
        migrated = dict(assertions)
        migrated.setdefault("evidence_cited", True)
        return migrated

    migrated = {}
    if assertions.get("must_detect"):
        migrated["detected_bug"] = True
    if "severity" in assertions:
        migrated["correct_severity"] = True
    if any(key.startswith("suggest_") for key in assertions):
        migrated["actionable_fix"] = True
    migrated.setdefault("evidence_cited", True)
    return migrated


def migrate_eval_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    migrated = copy.deepcopy(payload)
    cases = migrated.get("cases") or migrated.get("evals") or []
    for case in cases:
        assertions = case.get("assertions", {})
        is_counter_example = bool(case.get("counter_example"))
        case["assertions"] = _migrate_assertions(assertions, is_counter_example)
        case.setdefault("counter_example", is_counter_example)
    if "evals" in migrated and "cases" not in migrated:
        migrated["cases"] = migrated.pop("evals")
    return migrated
