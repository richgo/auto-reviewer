import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from llm.transport import CompletionResponse
from skill_machine.autoresearch import AutoResearcher, reached_convergence, select_top_candidate


class TestAutoResearchLoop(unittest.TestCase):
    def test_select_top_candidate_prefers_higher_screen_score_then_stable_id(self):
        candidates = [
            {"id": "b", "screen_score": 0.8},
            {"id": "a", "screen_score": 0.8},
            {"id": "c", "screen_score": 0.6},
        ]
        top = select_top_candidate(candidates)
        self.assertEqual(top["id"], "a")
        self.assertEqual(top["screen_score"], 0.8)

    def test_reached_convergence_after_configured_non_improving_rounds(self):
        history = [0.62, 0.63, 0.63, 0.63]
        self.assertTrue(reached_convergence(history, convergence_rounds=2, min_delta=0.01))

    def test_autoresearcher_uses_injected_transport_for_model_calls(self):
        class FakeTransport:
            def __init__(self):
                self.last_request = None

            def complete(self, request):
                self.last_request = request
                return CompletionResponse(
                    text="ok",
                    model=request.model,
                    provider="fake",
                    usage={},
                    raw=None,
                )

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skill = root / "SKILL.md"
            evals = root / "evals.json"
            out = root / "out.md"
            log = root / "run.jsonl"
            skill.write_text("skill content", encoding="utf-8")
            evals.write_text('{"cases":[{"prompt":"x","assertions":{"must_detect":true}}]}', encoding="utf-8")
            transport = FakeTransport()

            researcher = AutoResearcher(
                skill_path=skill,
                evals_path=evals,
                model="gpt-5-mini",
                max_iterations=1,
                target_pass_rate=0.95,
                output_path=out,
                log_path=log,
                transport=transport,
            )
            researcher._run_skill_on_case(researcher.current_skill, {"prompt": "test"})

        self.assertIsNotNone(transport.last_request)
        self.assertEqual("gpt-5-mini", transport.last_request.model)


if __name__ == "__main__":
    unittest.main()
