import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from benchmark.runner import BenchmarkRunner
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

            self.assertTrue((output_dir / "assertion_results.jsonl").exists())

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
