import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from benchmark.reporter import BenchmarkReporter


class TestBenchmarkReporter(unittest.TestCase):
    def test_generate_json_report_includes_regressions_with_baseline(self):
        current = {
            "timestamp": "2026-03-21T00:00:00Z",
            "models": {
                "gpt-4.1": {
                    "security-injection": {"f1": 0.80, "pass_rate": 0.82, "mean_latency_ms": 1000}
                }
            },
            "skills": ["security-injection"],
        }
        baseline = {
            "timestamp": "2026-03-20T00:00:00Z",
            "models": {
                "gpt-4.1": {
                    "security-injection": {"f1": 0.90, "pass_rate": 0.90, "mean_latency_ms": 600}
                }
            },
            "skills": ["security-injection"],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            current_path = tmp / "current.json"
            baseline_path = tmp / "baseline.json"
            current_path.write_text(json.dumps(current), encoding="utf-8")
            baseline_path.write_text(json.dumps(baseline), encoding="utf-8")

            reporter = BenchmarkReporter(current_path, compare_to=baseline_path)
            payload = reporter.generate_json_report()

            self.assertIn("leaderboard", payload)
            self.assertIn("regressions", payload)
            self.assertEqual(len(payload["regressions"]), 1)
            self.assertEqual(payload["regressions"][0]["skill"], "security-injection")


if __name__ == "__main__":
    unittest.main()
