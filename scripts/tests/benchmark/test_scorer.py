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


if __name__ == "__main__":
    unittest.main()
