import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from benchmark.scorer import estimate_costs


class TestCostEstimation(unittest.TestCase):
    def test_estimate_costs_returns_per_skill_model_and_total(self):
        rows = [
            {"skill_name": "security-injection", "model_id": "gpt-4.1", "input_tokens": 1000, "output_tokens": 500},
            {"skill_name": "security-injection", "model_id": "gpt-4.1", "input_tokens": 500, "output_tokens": 500},
            {"skill_name": "correctness", "model_id": "gpt-4.1", "input_tokens": 100, "output_tokens": 100},
        ]
        pricing = {"gpt-4.1": {"input_per_1k": 0.01, "output_per_1k": 0.03}}

        costs = estimate_costs(rows=rows, pricing=pricing)

        self.assertAlmostEqual(costs["by_skill_model"]["gpt-4.1"]["security-injection"], 0.045)
        self.assertAlmostEqual(costs["by_skill_model"]["gpt-4.1"]["correctness"], 0.004)
        self.assertAlmostEqual(costs["total_cost"], 0.049)


if __name__ == "__main__":
    unittest.main()
