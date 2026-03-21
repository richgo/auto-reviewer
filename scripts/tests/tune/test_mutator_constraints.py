import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tune.mutator import constrain_candidates


class TestMutatorConstraints(unittest.TestCase):
    def test_constrain_candidates_applies_budget_and_diff_limit(self):
        candidates = [
            {"id": "a", "content": "line1\nline2", "cluster": "fn"},
            {"id": "b", "content": "line1\nline2\nline3\nline4", "cluster": "fn"},
            {"id": "c", "content": "line1", "cluster": "fp"},
        ]
        selected = constrain_candidates(
            candidates=candidates,
            baseline_content="line1\nline2",
            mutation_budget=2,
            max_diff_lines=1,
        )

        self.assertEqual([row["id"] for row in selected], ["a", "c"])
        self.assertEqual(selected[0]["diff_lines"], 0)
        self.assertEqual(selected[1]["diff_lines"], 1)


if __name__ == "__main__":
    unittest.main()
