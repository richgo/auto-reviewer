import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tune.history import append_history, read_history


class TestHistory(unittest.TestCase):
    def test_append_history_writes_jsonl_and_read_history_replays_rows(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            history_file = Path(tmp_dir) / "tune-history" / "security-injection" / "gpt-4.1.jsonl"
            append_history(
                history_file=history_file,
                row={
                    "run_id": "run-1",
                    "skill": "security-injection",
                    "model": "gpt-4.1",
                    "baseline": {"f1": 0.71, "fpr": 0.11},
                    "candidate": {"f1": 0.74, "fpr": 0.09},
                    "accepted": True,
                },
            )
            rows = read_history(history_file=history_file)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["run_id"], "run-1")
        self.assertTrue(rows[0]["accepted"])

    def test_read_history_returns_empty_for_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            history_file = Path(tmp_dir) / "missing.jsonl"
            rows = read_history(history_file=history_file)
        self.assertEqual(rows, [])


if __name__ == "__main__":
    unittest.main()
