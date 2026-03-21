import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tune.autoresearch import select_top_candidate


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


if __name__ == "__main__":
    unittest.main()
