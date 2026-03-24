import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from skill_machine.orchestrator import build_trajectory_summary, update_model_scores_snapshot


class TestScoreSnapshots(unittest.TestCase):
    def test_update_model_scores_snapshot_only_writes_on_accept(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            scores_file = Path(tmp_dir) / "model-scores.yml"
            scores_file.write_text(
                "last_updated: null\nmodels:\n  gpt-4.1:\n    security-injection: {pass_rate: null, f1: null, last_run: null}\n",
                encoding="utf-8",
            )

            changed = update_model_scores_snapshot(
                scores_path=scores_file,
                model="gpt-4.1",
                skill="security-injection",
                metrics={"pass_rate": 0.82, "f1": 0.8, "last_run": "2026-03-21T00:00:00Z"},
                accepted=False,
            )
            self.assertFalse(changed)
            self.assertIn("pass_rate: null", scores_file.read_text(encoding="utf-8"))

    def test_build_trajectory_summary_reports_accept_rate(self):
        summary = build_trajectory_summary(
            history_rows=[
                {"accepted": True, "candidate": {"f1": 0.8}, "baseline": {"f1": 0.7}},
                {"accepted": False, "candidate": {"f1": 0.71}, "baseline": {"f1": 0.7}},
            ]
        )
        self.assertEqual(summary["runs"], 2)
        self.assertEqual(summary["accepted"], 1)
        self.assertAlmostEqual(summary["accept_rate"], 0.5)


if __name__ == "__main__":
    unittest.main()
