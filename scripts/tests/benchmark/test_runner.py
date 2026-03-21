import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from benchmark.runner import BenchmarkRunner


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


if __name__ == "__main__":
    unittest.main()
