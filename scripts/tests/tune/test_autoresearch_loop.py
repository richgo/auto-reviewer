import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tune.autoresearch import reached_convergence, select_top_candidate


class TestAutoResearchLoop(unittest.TestCase):
    def test_select_top_candidate_prefers_higher_screen_score_then_stable_id(self):
        candidates = [
            {"id": "b", "screen_score": 0.8},
            {"id": "a", "screen_score": 0.8},
            {"id": "c", "screen_score": 0.6},
        ]
        top = select_top_candidate(candidates)
        self.assertEqual(top["id"], "a")
        self.assertEqual(top["screen_score"], 0.8)

    def test_reached_convergence_after_configured_non_improving_rounds(self):
        history = [0.62, 0.63, 0.63, 0.63]
        self.assertTrue(reached_convergence(history, convergence_rounds=2, min_delta=0.01))


if __name__ == "__main__":
    unittest.main()
