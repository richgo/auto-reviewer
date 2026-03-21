import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tune.autoresearch import should_accept_candidate


class TestPolicyGate(unittest.TestCase):
    def test_should_accept_candidate_rejects_metric_conflict(self):
        accepted = should_accept_candidate(
            baseline={"f1": 0.70, "fpr": 0.10},
            candidate={"f1": 0.73, "fpr": 0.16},
            min_f1_delta=0.01,
            max_fpr_regression=0.02,
        )
        self.assertFalse(accepted)


if __name__ == "__main__":
    unittest.main()
