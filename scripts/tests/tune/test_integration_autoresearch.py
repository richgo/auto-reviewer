import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tune.history import append_history, read_history
from tune.orchestrator import build_trajectory_summary, update_model_scores_snapshot


class TestIntegrationAutoResearch(unittest.TestCase):
    def test_append_then_summarize_history_flow(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            history_file = Path(tmp_dir) / "tune-history" / "security-injection" / "gpt-4.1.jsonl"
            append_history(
                history_file=history_file,
                row={
                    "run_id": "run-1",
                    "skill": "security-injection",
                    "model": "gpt-4.1",
                    "baseline": {"f1": 0.70, "fpr": 0.10},
                    "candidate": {"f1": 0.74, "fpr": 0.09},
                    "accepted": True,
                },
            )
            append_history(
                history_file=history_file,
                row={
                    "run_id": "run-2",
                    "skill": "security-injection",
                    "model": "gpt-4.1",
                    "baseline": {"f1": 0.74, "fpr": 0.09},
                    "candidate": {"f1": 0.74, "fpr": 0.09},
                    "accepted": False,
                },
            )
            rows = read_history(history_file=history_file)
            summary = build_trajectory_summary(history_rows=rows)

        self.assertEqual(summary["runs"], 2)
        self.assertEqual(summary["accepted"], 1)
        self.assertAlmostEqual(summary["accept_rate"], 0.5)

    def test_update_model_scores_snapshot_is_idempotent_for_same_metrics(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            scores_file = Path(tmp_dir) / "model-scores.yml"
            scores_file.write_text(
                "last_updated: null\nmodels:\n  gpt-4.1:\n    security-injection: {pass_rate: null, f1: null, last_run: null}\n",
                encoding="utf-8",
            )
            metrics = {"pass_rate": 0.82, "f1": 0.80, "last_run": "2026-03-21T00:00:00Z"}
            changed_first = update_model_scores_snapshot(
                scores_path=scores_file,
                model="gpt-4.1",
                skill="security-injection",
                metrics=metrics,
                accepted=True,
            )
            snapshot_first = scores_file.read_text(encoding="utf-8")
            changed_second = update_model_scores_snapshot(
                scores_path=scores_file,
                model="gpt-4.1",
                skill="security-injection",
                metrics=metrics,
                accepted=True,
            )
            snapshot_second = scores_file.read_text(encoding="utf-8")

        self.assertTrue(changed_first)
        self.assertTrue(changed_second)
        self.assertEqual(snapshot_first, snapshot_second)


if __name__ == "__main__":
    unittest.main()
