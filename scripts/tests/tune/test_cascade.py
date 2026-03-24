import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from tune.cascade import CascadeOrchestrator


class TestCascadeOrchestrator(unittest.TestCase):
    """Test cascade orchestrator for multi-model escalation."""

    def test_cascade_runs_stage_1_with_gpt_5_mini_and_5_iterations(self):
        """Given a skill with no tuning history
        When cascade orchestrator starts
        Then it should run Stage 1 with gpt-5-mini for up to 5 iterations."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            history_dir = root / "tune-history" / "test-skill"
            history_dir.mkdir(parents=True, exist_ok=True)

            config = {
                "cascade": {
                    "enabled": True,
                    "stages": [
                        {
                            "model": "gpt-5-mini",
                            "max_iterations": 5,
                            "target_pass_rate": 0.95,
                        },
                        {
                            "model": "claude-haiku-4.5",
                            "max_iterations": 3,
                            "target_pass_rate": 0.95,
                        },
                    ],
                }
            }

            orchestrator = CascadeOrchestrator(
                skill_name="test-skill",
                history_dir=history_dir,
                config=config,
            )

            # Mock the tuning function to return a result
            with patch.object(orchestrator, "_run_single_stage") as mock_run:
                mock_run.return_value = {"pass_rate": 0.85, "model": "gpt-5-mini"}

                result = orchestrator.run()

            # Verify Stage 1 was called with correct parameters (first call)
            mock_run.assert_called()
            first_call_args = mock_run.call_args_list[0]
            self.assertEqual(first_call_args[0][0], "gpt-5-mini")  # model
            self.assertEqual(first_call_args[0][1], 5)  # max_iterations
            self.assertEqual(first_call_args[0][2], 0.95)  # target_pass_rate

    def test_cascade_escalates_to_stage_2_if_stage_1_fails_to_reach_95_percent(self):
        """Given Stage 1 completes with pass_rate < 95%
        When cascade evaluates the result
        Then it should escalate to Stage 2 with claude-haiku-4.5."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            history_dir = root / "tune-history" / "test-skill"
            history_dir.mkdir(parents=True, exist_ok=True)

            config = {
                "cascade": {
                    "enabled": True,
                    "stages": [
                        {
                            "model": "gpt-5-mini",
                            "max_iterations": 5,
                            "target_pass_rate": 0.95,
                        },
                        {
                            "model": "claude-haiku-4.5",
                            "max_iterations": 3,
                            "target_pass_rate": 0.95,
                        },
                    ],
                }
            }

            orchestrator = CascadeOrchestrator(
                skill_name="test-skill",
                history_dir=history_dir,
                config=config,
            )

            call_order = []

            def mock_run_stage(model, max_iter, target):
                call_order.append(model)
                if model == "gpt-5-mini":
                    return {"pass_rate": 0.85, "model": "gpt-5-mini"}
                elif model == "claude-haiku-4.5":
                    return {"pass_rate": 0.96, "model": "claude-haiku-4.5"}

            with patch.object(orchestrator, "_run_single_stage", side_effect=mock_run_stage):
                result = orchestrator.run()

            # Should have called both stages in order
            self.assertEqual(call_order, ["gpt-5-mini", "claude-haiku-4.5"])
            # Should return the successful Stage 2 result
            self.assertEqual(result["pass_rate"], 0.96)
            self.assertEqual(result["stage"], 2)

    def test_cascade_marks_skill_for_review_if_both_stages_fail(self):
        """Given both Stage 1 and Stage 2 complete with pass_rate < 95%
        When cascade evaluates results
        Then it should mark the skill as needing review."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            history_dir = root / "tune-history" / "test-skill"
            history_dir.mkdir(parents=True, exist_ok=True)

            config = {
                "cascade": {
                    "enabled": True,
                    "stages": [
                        {
                            "model": "gpt-5-mini",
                            "max_iterations": 5,
                            "target_pass_rate": 0.95,
                        },
                        {
                            "model": "claude-haiku-4.5",
                            "max_iterations": 3,
                            "target_pass_rate": 0.95,
                        },
                    ],
                }
            }

            orchestrator = CascadeOrchestrator(
                skill_name="test-skill",
                history_dir=history_dir,
                config=config,
            )

            def mock_run_stage(model, max_iter, target):
                # Both stages fail to reach 95%
                return {"pass_rate": 0.88, "model": model}

            with patch.object(orchestrator, "_run_single_stage", side_effect=mock_run_stage):
                result = orchestrator.run()

            # Should mark as needs_review
            self.assertTrue(result["needs_review"])
            self.assertEqual(result["best_model"], "claude-haiku-4.5")
            self.assertEqual(result["best_pass_rate"], 0.88)


if __name__ == "__main__":
    unittest.main()
