import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from skill_machine.mutator import constrain_candidates, cluster_failures


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

    def test_cluster_failures_groups_by_assertion(self):
        scores = [
            (
                {"id": "case-1"},
                SimpleNamespace(
                    assertion_results=[
                        SimpleNamespace(name="detected_bug", passed=False, reason="missed"),
                        SimpleNamespace(name="actionable_fix", passed=True, reason="ok"),
                    ]
                ),
            ),
            (
                {"id": "case-2"},
                SimpleNamespace(
                    assertion_results=[
                        SimpleNamespace(name="detected_bug", passed=False, reason="missed again"),
                        SimpleNamespace(name="no_false_positive", passed=False, reason="fp"),
                    ]
                ),
            ),
        ]

        clusters = cluster_failures(scores)
        self.assertEqual(sorted(clusters.keys()), ["detected_bug", "no_false_positive"])
        self.assertEqual([row["case_id"] for row in clusters["detected_bug"]], ["case-1", "case-2"])

    def test_constrain_candidates_respects_mutation_budget(self):
        candidates = [
            {"id": "a", "content": "line1"},
            {"id": "b", "content": "line1"},
            {"id": "c", "content": "line1"},
        ]
        selected = constrain_candidates(
            candidates=candidates,
            baseline_content="line1",
            mutation_budget=2,
            max_diff_lines=0,
        )
        self.assertEqual([row["id"] for row in selected], ["a", "b"])


if __name__ == "__main__":
    unittest.main()
