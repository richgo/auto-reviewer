import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from benchmark.scorer import BenchmarkScorer


class _FakeJudge:
    def __init__(self):
        self.calls = []

    def evaluate(self, **kwargs):
        self.calls.append(kwargs)
        return {"status": "pass", "justification": "ok", "model": "judge-x"}


class TestBenchmarkScorer(unittest.TestCase):
    def test_score_case_skips_non_false_positive_assertions_for_counter_examples(self):
        judge = _FakeJudge()
        scorer = BenchmarkScorer(judge=judge)
        eval_case = {
            "id": "safe-1",
            "counter_example": True,
            "assertions": {
                "detected_bug": True,
                "actionable_fix": True,
                "no_false_positive": True,
            },
            "code_snippet": "safe_query(param)",
        }

        rows = scorer.score_case(
            model_id="gpt-4.1",
            skill_name="security-injection",
            eval_case=eval_case,
            review_output="No issues detected",
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["assertion_name"], "no_false_positive")
        self.assertEqual(len(judge.calls), 1)

    def test_aggregate_metrics_includes_precision_recall_and_confidence(self):
        scorer = BenchmarkScorer(judge=_FakeJudge())
        assertion_rows = []
        statuses = [
            ("pass", "pass"),
            ("pass", "fail"),
            ("fail", "pass"),
            ("pass", "pass"),
            ("pass", "pass"),
        ]
        for idx, (detected_status, fp_status) in enumerate(statuses, start=1):
            eval_case_id = f"case-{idx}"
            assertion_rows.extend(
                [
                    {"eval_case_id": eval_case_id, "assertion_name": "detected_bug", "status": detected_status},
                    {"eval_case_id": eval_case_id, "assertion_name": "no_false_positive", "status": fp_status},
                    {"eval_case_id": eval_case_id, "assertion_name": "actionable_fix", "status": "pass"},
                ]
            )
        raw_rows = [
            {"eval_case_id": "case-1", "latency_ms": 100, "input_tokens": 20, "output_tokens": 10},
            {"eval_case_id": "case-2", "latency_ms": 150, "input_tokens": 22, "output_tokens": 12},
            {"eval_case_id": "case-3", "latency_ms": 200, "input_tokens": 24, "output_tokens": 14},
            {"eval_case_id": "case-4", "latency_ms": 250, "input_tokens": 26, "output_tokens": 16},
            {"eval_case_id": "case-5", "latency_ms": 300, "input_tokens": 28, "output_tokens": 18},
        ]

        metrics = scorer.aggregate_metrics(assertion_rows=assertion_rows, raw_rows=raw_rows)

        self.assertAlmostEqual(metrics["precision"], 0.8)
        self.assertAlmostEqual(metrics["recall"], 0.8)
        self.assertAlmostEqual(metrics["f1"], 0.8)
        self.assertAlmostEqual(metrics["false_positive_rate"], 0.2)
        self.assertAlmostEqual(metrics["mean_latency_ms"], 200.0)
        self.assertAlmostEqual(metrics["mean_tokens"], 38.0)
        self.assertFalse(metrics["low_confidence"])
        self.assertIn("pass_rate_stddev", metrics)
        self.assertIn("latency_stddev_ms", metrics)
        self.assertIn("tokens_stddev", metrics)


if __name__ == "__main__":
    unittest.main()
