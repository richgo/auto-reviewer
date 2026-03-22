import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from benchmark.runner import BenchmarkRunner, main as benchmark_main
from benchmark.scorer import select_best_models
from tune.llm_client import CopilotLLMClient


class _FakeScore:
    pass_rate = 1.0


class _FakeScorer:
    def __init__(self, model):
        self.model = model

    def score_review(self, review_output, eval_case):
        return _FakeScore()


class TestBenchmarkRunner(unittest.TestCase):
    def test_run_writes_assertion_results_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            skills_dir = tmp / "skills"
            evals_dir = tmp / "evals"
            output_dir = tmp / "out"
            (skills_dir / "concerns").mkdir(parents=True)
            evals_dir.mkdir(parents=True)

            (skills_dir / "concerns" / "security-injection.md").write_text(
                "review skill", encoding="utf-8"
            )
            (evals_dir / "security-injection.json").write_text(
                json.dumps(
                    {
                        "skill": "security-injection",
                        "cases": [
                            {
                                "id": "sql-1",
                                "code_snippet": "query = f'{user}'",
                                "assertions": {"detected_bug": True},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            with patch("benchmark.runner.Scorer", _FakeScorer), patch.object(
                BenchmarkRunner, "run_skill_on_eval", return_value="review text"
            ):
                runner = BenchmarkRunner(
                    skills_dir=skills_dir,
                    evals_dir=evals_dir,
                    models=["gpt-4.1"],
                    output_dir=output_dir,
                )
                runner.run()

            run_dirs = [
                path
                for path in output_dir.iterdir()
                if path.is_dir() and path.name.startswith("run-")
            ]
            self.assertEqual(len(run_dirs), 1)
            run_dir = run_dirs[0]

            self.assertTrue((run_dir / "assertion_results.jsonl").exists())
            self.assertTrue((run_dir / "model_scores.json").exists())
            self.assertTrue((run_dir / "best_models.json").exists())
            self.assertTrue((run_dir / "metadata.json").exists())

            self.assertTrue((output_dir / "latest" / "assertion_results.jsonl").exists())
            self.assertTrue((output_dir / "latest" / "model_scores.json").exists())
            self.assertTrue((output_dir / "latest" / "best_models.json").exists())
            self.assertTrue((output_dir / "latest" / "metadata.json").exists())
            self.assertTrue((output_dir / "assertion_results.jsonl").exists())
            self.assertTrue((output_dir / "model_scores.json").exists())
            self.assertTrue((output_dir / "best_models.json").exists())
            self.assertTrue((output_dir / "metadata.json").exists())

    def test_cli_run_single_skill_api_design_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            skills_dir = tmp / "skills"
            evals_dir = tmp / "evals"
            output_dir = tmp / "out"
            (skills_dir / "concerns").mkdir(parents=True)
            evals_dir.mkdir(parents=True)

            (skills_dir / "concerns" / "api-design.md").write_text(
                "api design skill", encoding="utf-8"
            )
            (evals_dir / "api-design.json").write_text(
                json.dumps(
                    {
                        "skill": "api-design",
                        "cases": [
                            {
                                "id": "api-breaking-change-1",
                                "language": "python",
                                "code_snippet": "return {'id': 1}",
                                "assertions": {"detected_bug": True},
                            },
                            {
                                "id": "api-pagination-1",
                                "language": "python",
                                "code_snippet": "return db.query('SELECT * FROM users')",
                                "assertions": {"actionable_fix": True},
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            argv = [
                "runner.py",
                "--skills-dir",
                str(skills_dir),
                "--evals-dir",
                str(evals_dir),
                "--models",
                "gpt-4.1",
                "--output",
                str(output_dir),
            ]
            with patch("benchmark.runner.Scorer", _FakeScorer), patch.object(
                BenchmarkRunner, "run_skill_on_eval", return_value="review text"
            ), patch.object(sys, "argv", argv):
                benchmark_main()

            model_scores_path = output_dir / "model_scores.json"
            assertion_results_path = output_dir / "assertion_results.jsonl"
            best_models_path = output_dir / "best_models.json"
            metadata_path = output_dir / "metadata.json"
            self.assertTrue(model_scores_path.exists())
            self.assertTrue(assertion_results_path.exists())
            self.assertTrue(best_models_path.exists())
            self.assertTrue(metadata_path.exists())

            model_scores = json.loads(model_scores_path.read_text(encoding="utf-8"))
            self.assertEqual(model_scores["skills"], ["api-design"])
            self.assertEqual(set(model_scores["models"].keys()), {"gpt-4.1"})
            self.assertEqual(
                model_scores["models"]["gpt-4.1"]["api-design"]["total_cases"], 2
            )
            self.assertEqual(
                model_scores["models"]["gpt-4.1"]["api-design"]["pass_rate"], 1.0
            )
            self.assertTrue(str(model_scores["run_id"]).startswith("run-"))

            expected_best = select_best_models(model_scores["models"])
            best_models = json.loads(best_models_path.read_text(encoding="utf-8"))
            self.assertEqual(best_models, expected_best)
            self.assertEqual(best_models["api-design"]["model"], "gpt-4.1")

            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            self.assertEqual(metadata["run_id"], model_scores["run_id"])
            self.assertEqual(metadata["models"], ["gpt-4.1"])
            self.assertEqual(metadata["skills"], ["api-design"])
            self.assertEqual(metadata["total_runs"], 1)

            assertion_rows = [
                json.loads(line)
                for line in assertion_results_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(len(assertion_rows), 1)
            self.assertEqual(assertion_rows[0]["skill_name"], "api-design")
            self.assertEqual(assertion_rows[0]["model_id"], "gpt-4.1")

            run_dirs = [
                path
                for path in output_dir.iterdir()
                if path.is_dir() and path.name.startswith("run-")
            ]
            self.assertEqual(len(run_dirs), 1)
            run_dir = run_dirs[0]
            self.assertTrue((run_dir / "model_scores.json").exists())
            self.assertTrue((run_dir / "assertion_results.jsonl").exists())
            self.assertTrue((run_dir / "best_models.json").exists())
            self.assertTrue((run_dir / "metadata.json").exists())
            self.assertTrue((output_dir / "latest" / "model_scores.json").exists())
            self.assertTrue((output_dir / "latest" / "best_models.json").exists())

    def test_run_uses_copilot_llm_client(self):
        """run_skill_on_eval must instantiate CopilotLLMClient, not LLMClient."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            skills_dir = tmp / "skills"
            evals_dir = tmp / "evals"
            output_dir = tmp / "out"
            (skills_dir / "concerns").mkdir(parents=True)
            evals_dir.mkdir(parents=True)

            (skills_dir / "concerns" / "correctness.md").write_text(
                "review skill", encoding="utf-8"
            )
            (evals_dir / "correctness.json").write_text(
                json.dumps(
                    {
                        "skill": "correctness",
                        "cases": [
                            {
                                "id": "c-1",
                                "code_snippet": "x = 1",
                                "assertions": {"detected_bug": False},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            instantiated_clients = []

            class _TrackedCopilotClient(CopilotLLMClient):
                def __init__(self, model, **kwargs):
                    super().__init__(model, **kwargs)
                    instantiated_clients.append(model)

                def complete(self, *args, **kwargs):
                    return "review output"

            with patch("benchmark.runner.Scorer", _FakeScorer), patch(
                "benchmark.runner.CopilotLLMClient", _TrackedCopilotClient
            ):
                runner = BenchmarkRunner(
                    skills_dir=skills_dir,
                    evals_dir=evals_dir,
                    models=["gpt-4o-mini"],
                    output_dir=output_dir,
                )
                runner.run()

            self.assertEqual(instantiated_clients, ["gpt-4o-mini"])

    def test_find_skill_eval_pairs_ignores_evals_not_mapped_to_existing_skills(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            skills_dir = tmp / "skills"
            evals_dir = tmp / "evals"
            output_dir = tmp / "out"
            (skills_dir / "concerns").mkdir(parents=True)
            evals_dir.mkdir(parents=True)

            (skills_dir / "concerns" / "correctness.md").write_text("review skill", encoding="utf-8")
            (evals_dir / "correctness.json").write_text(
                json.dumps({"skill": "correctness", "cases": []}), encoding="utf-8"
            )
            (evals_dir / "legacy-review-task.json").write_text(
                json.dumps({"review_task": "security/xss", "cases": []}), encoding="utf-8"
            )

            runner = BenchmarkRunner(
                skills_dir=skills_dir,
                evals_dir=evals_dir,
                models=["gpt-4.1"],
                output_dir=output_dir,
            )
            pairs = runner.find_skill_eval_pairs()

        pair_names = [skill_name for _, _, skill_name in pairs]
        self.assertEqual(pair_names, ["correctness"])


class TestCopilotLLMClient(unittest.TestCase):
    def test_complete_calls_copilot_sdk_and_returns_content(self):
        with patch("tune.llm_client.CopilotLLMClient._complete_async") as mock_async:
            mock_async.return_value = "mocked review"
            client = CopilotLLMClient("gpt-4o-mini")
            result = client.complete("test prompt", system="sys")

        self.assertEqual(result, "mocked review")
        mock_async.assert_called_once_with("test prompt", "sys")

    def test_complete_raises_on_empty_sdk_response(self):
        async def _fail(self_inner, prompt, system):
            raise RuntimeError("Copilot SDK returned no response for model 'gpt-4o-mini'")

        with patch.object(CopilotLLMClient, "_complete_async", _fail):
            client = CopilotLLMClient("gpt-4o-mini")
            with self.assertRaises(RuntimeError, msg="no response"):
                client.complete("test prompt")


if __name__ == "__main__":
    unittest.main()
