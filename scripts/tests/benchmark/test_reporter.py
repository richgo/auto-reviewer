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

    def test_generate_report_includes_unsolved_trivial_and_pairings(self):
        current = {
            "timestamp": "2026-03-21T00:00:00Z",
            "models": {
                "model-a": {
                    "security-injection": {"f1": 0.96, "pass_rate": 0.96, "mean_latency_ms": 400},
                    "correctness": {"f1": 0.50, "pass_rate": 0.50, "mean_latency_ms": 450},
                },
                "model-b": {
                    "security-injection": {"f1": 0.97, "pass_rate": 0.97, "mean_latency_ms": 380},
                    "correctness": {"f1": 0.62, "pass_rate": 0.62, "mean_latency_ms": 420},
                },
            },
            "skills": ["security-injection", "correctness"],
            "assertion_results": [
                {"skill_name": "correctness", "model_id": "model-a", "eval_case_id": "e1", "assertion_name": "detected_bug", "status": "pass"},
                {"skill_name": "correctness", "model_id": "model-b", "eval_case_id": "e1", "assertion_name": "detected_bug", "status": "fail"},
                {"skill_name": "correctness", "model_id": "model-a", "eval_case_id": "e2", "assertion_name": "detected_bug", "status": "fail"},
                {"skill_name": "correctness", "model_id": "model-b", "eval_case_id": "e2", "assertion_name": "detected_bug", "status": "pass"},
            ],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            current_path = tmp / "current.json"
            current_path.write_text(json.dumps(current), encoding="utf-8")

            reporter = BenchmarkReporter(current_path)
            report = reporter.generate_report()

            self.assertIn("unsolved", report.lower())
            self.assertIn("trivial", report.lower())
            self.assertIn("recommended_pairings", report)

    def test_generate_report_writes_heatmap_csv_rows(self):
        current = {
            "timestamp": "2026-03-21T00:00:00Z",
            "models": {
                "model-a": {"security-injection": {"f1": 0.95, "pass_rate": 0.95}},
                "model-b": {"security-injection": {"f1": 0.65, "pass_rate": 0.65}},
            },
            "skills": ["security-injection"],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            current_path = tmp / "current.json"
            heatmap_path = tmp / "heatmap.csv"
            current_path.write_text(json.dumps(current), encoding="utf-8")

            reporter = BenchmarkReporter(current_path)
            reporter.write_heatmap_csv(heatmap_path)

            content = heatmap_path.read_text(encoding="utf-8")
            self.assertIn("model,security-injection", content)
            self.assertIn("model-a,0.95", content)
            self.assertIn("model-b,0.65", content)

    def test_generate_github_output_sets_summary_outputs_and_exit_code(self):
        current = {
            "timestamp": "2026-03-21T00:00:00Z",
            "models": {
                "gpt-4.1": {"security-injection": {"f1": 0.80, "pass_rate": 0.80, "mean_latency_ms": 1000}}
            },
            "skills": ["security-injection"],
        }
        baseline = {
            "timestamp": "2026-03-20T00:00:00Z",
            "models": {
                "gpt-4.1": {"security-injection": {"f1": 0.90, "pass_rate": 0.90, "mean_latency_ms": 600}}
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
            payload = reporter.generate_github_output()

            self.assertIn("summary_markdown", payload)
            self.assertIn("outputs", payload)
            self.assertEqual(payload["outputs"]["regression_count"], 1)
            self.assertEqual(payload["exit_code"], 1)

    def test_generate_report_includes_regressions_and_emoji_heatmap(self):
        current = {
            "timestamp": "2026-03-21T00:00:00Z",
            "models": {
                "model-a": {
                    "security-injection": {"f1": 0.95, "pass_rate": 0.95, "mean_latency_ms": 900},
                    "correctness": {"f1": 0.65, "pass_rate": 0.65, "mean_latency_ms": 1200},
                }
            },
            "skills": ["security-injection", "correctness"],
        }
        baseline = {
            "timestamp": "2026-03-20T00:00:00Z",
            "models": {
                "model-a": {
                    "security-injection": {"f1": 0.98, "pass_rate": 0.98, "mean_latency_ms": 600},
                    "correctness": {"f1": 0.80, "pass_rate": 0.80, "mean_latency_ms": 700},
                }
            },
            "skills": ["security-injection", "correctness"],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            current_path = tmp / "current.json"
            baseline_path = tmp / "baseline.json"
            current_path.write_text(json.dumps(current), encoding="utf-8")
            baseline_path.write_text(json.dumps(baseline), encoding="utf-8")

            reporter = BenchmarkReporter(current_path, compare_to=baseline_path)
            report = reporter.generate_report()

            self.assertIn("## Regressions", report)
            self.assertIn("🟢", report)
            self.assertIn("🔴", report)


if __name__ == "__main__":
    unittest.main()
