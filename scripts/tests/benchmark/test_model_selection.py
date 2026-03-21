import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from benchmark.scorer import select_best_models


class TestModelSelection(unittest.TestCase):
    def test_select_best_models_prefers_higher_pass_rate_on_f1_tie(self):
        matrix = {
            "model-a": {
                "security-injection": {"f1": 0.72, "pass_rate": 0.74},
                "correctness": {"f1": 0.68, "pass_rate": 0.70},
            },
            "model-b": {
                "security-injection": {"f1": 0.72, "pass_rate": 0.81},
                "correctness": {"f1": 0.66, "pass_rate": 0.80},
            },
        }

        best = select_best_models(matrix)

        self.assertEqual(best["security-injection"]["model"], "model-b")
        self.assertEqual(best["security-injection"]["needs_tuning"], False)
        self.assertEqual(best["correctness"]["model"], "model-a")
        self.assertEqual(best["correctness"]["needs_tuning"], True)


if __name__ == "__main__":
    unittest.main()
