from typing import Any, Dict, List


ASSERTION_CRITERIA = {
    "detected_bug": "The review identifies the target bug.",
    "no_false_positive": "The review does not flag safe code as vulnerable.",
    "actionable_fix": "The review suggests a concrete fix.",
    "correct_severity": "The review assigns the right severity.",
    "evidence_cited": "The review cites concrete code evidence.",
}


class BenchmarkScorer:
    def __init__(self, judge):
        self.judge = judge

    def score_case(
        self,
        *,
        model_id: str,
        skill_name: str,
        eval_case: Dict[str, Any],
        review_output: str,
    ) -> List[Dict[str, Any]]:
        assertions = eval_case.get("assertions", {})
        assertion_names = self._assertion_names(assertions, bool(eval_case.get("counter_example")))

        rows: List[Dict[str, Any]] = []
        for assertion_name in assertion_names:
            result = self.judge.evaluate(
                code_snippet=eval_case.get("code_snippet", eval_case.get("prompt", "")),
                review_output=review_output,
                assertion_name=assertion_name,
                criteria=ASSERTION_CRITERIA.get(assertion_name, assertion_name),
            )
            rows.append(
                {
                    "model_id": model_id,
                    "skill_name": skill_name,
                    "eval_case_id": eval_case.get("id", ""),
                    "assertion_name": assertion_name,
                    "status": result["status"],
                    "justification": result["justification"],
                    "judge_model": result["model"],
                }
            )
        return rows

    @staticmethod
    def _assertion_names(assertions: Dict[str, Any], counter_example: bool) -> List[str]:
        assertion_names = list(assertions.keys())
        if counter_example:
            return [name for name in assertion_names if name == "no_false_positive"]
        return assertion_names
