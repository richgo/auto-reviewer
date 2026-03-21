from statistics import mean, pstdev
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

    def aggregate_metrics(self, *, assertion_rows: List[Dict[str, Any]], raw_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_assertions = len(assertion_rows)
        passed = sum(1 for row in assertion_rows if row.get("status") == "pass")
        pass_rate = (passed / total_assertions) if total_assertions else 0.0

        detected_rows = self._rows_for(assertion_rows, "detected_bug")
        detected_pass = self._pass_count(detected_rows)
        detection_rate = (detected_pass / len(detected_rows)) if detected_rows else 0.0

        fp_rows = self._rows_for(assertion_rows, "no_false_positive")
        fp_fails = sum(1 for row in fp_rows if row.get("status") == "fail")
        false_positive_rate = (fp_fails / len(fp_rows)) if fp_rows else 0.0

        actionable_rows = self._rows_for(assertion_rows, "actionable_fix")
        actionable_pass = self._pass_count(actionable_rows)
        actionability_rate = (actionable_pass / len(actionable_rows)) if actionable_rows else 0.0

        true_positives = detected_pass
        false_positives = fp_fails
        false_negatives = len(detected_rows) - detected_pass
        precision = (true_positives / (true_positives + false_positives)) if (true_positives + false_positives) else None
        recall = (true_positives / (true_positives + false_negatives)) if (true_positives + false_negatives) else None
        if precision is None or recall is None or (precision + recall) == 0:
            f1 = None
        else:
            f1 = 2 * (precision * recall) / (precision + recall)

        latencies = [float(row.get("latency_ms", 0.0)) for row in raw_rows]
        tokens = [
            float(row.get("input_tokens", 0.0)) + float(row.get("output_tokens", 0.0))
            for row in raw_rows
        ]
        pass_values = [1.0 if row.get("status") == "pass" else 0.0 for row in assertion_rows]
        eval_case_count = len({row.get("eval_case_id") for row in raw_rows})

        return {
            "pass_rate": pass_rate,
            "detection_rate": detection_rate,
            "false_positive_rate": false_positive_rate,
            "actionability_rate": actionability_rate,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "mean_latency_ms": mean(latencies) if latencies else 0.0,
            "mean_tokens": mean(tokens) if tokens else 0.0,
            "pass_rate_stddev": pstdev(pass_values) if len(pass_values) > 1 else 0.0,
            "latency_stddev_ms": pstdev(latencies) if len(latencies) > 1 else 0.0,
            "tokens_stddev": pstdev(tokens) if len(tokens) > 1 else 0.0,
            "eval_count": eval_case_count,
            "low_confidence": eval_case_count < 5,
        }

    @staticmethod
    def _rows_for(assertion_rows: List[Dict[str, Any]], assertion_name: str) -> List[Dict[str, Any]]:
        return [row for row in assertion_rows if row.get("assertion_name") == assertion_name]

    @staticmethod
    def _pass_count(rows: List[Dict[str, Any]]) -> int:
        return sum(1 for row in rows if row.get("status") == "pass")
