import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tune.outcomes import OutcomeStatus, build_tuning_outcome, write_outcome


class TestTuningOutcomes(unittest.TestCase):
    def test_build_outcome_marks_promotable_when_target_is_met(self):
        outcome = build_tuning_outcome(
            skill_name="security-injection",
            best_model="gpt-5-mini",
            best_pass_rate=0.96,
            target_pass_rate=0.95,
            benchmark_ran=False,
            benchmark_passed=False,
        )

        self.assertEqual(OutcomeStatus.PROMOTABLE, outcome.status)
        self.assertEqual("security-injection", outcome.skill_name)

    def test_build_outcome_marks_gated_when_target_met_but_benchmark_fails(self):
        outcome = build_tuning_outcome(
            skill_name="security-injection",
            best_model="claude-haiku-4.5",
            best_pass_rate=0.96,
            target_pass_rate=0.95,
            benchmark_ran=True,
            benchmark_passed=False,
        )

        self.assertEqual(OutcomeStatus.GATED, outcome.status)

    def test_build_outcome_marks_needs_review_when_target_not_met(self):
        outcome = build_tuning_outcome(
            skill_name="security-injection",
            best_model="claude-haiku-4.5",
            best_pass_rate=0.88,
            target_pass_rate=0.95,
            benchmark_ran=False,
            benchmark_passed=False,
        )

        self.assertEqual(OutcomeStatus.NEEDS_REVIEW, outcome.status)

    def test_write_outcome_persists_visible_result(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "outcome.json"
            outcome = build_tuning_outcome(
                skill_name="security-injection",
                best_model="claude-haiku-4.5",
                best_pass_rate=0.88,
                target_pass_rate=0.95,
                benchmark_ran=False,
                benchmark_passed=False,
            )
            write_outcome(path=path, outcome=outcome)

            self.assertTrue(path.exists())
            text = path.read_text(encoding="utf-8")
            self.assertIn('"status": "needs_review"', text)
            self.assertIn('"skill_name": "security-injection"', text)


if __name__ == "__main__":
    unittest.main()
