import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import yaml

from skill_machine.cascade import CascadeOrchestrator
from skill_machine.needs_review import NeedsReviewTracker


class TestCascadeEndToEnd(unittest.TestCase):
    """End-to-end integration tests for cascade orchestration."""

    def test_cascade_end_to_end_success_on_stage_1(self):
        """Given a skill ready for cascade tuning
        When Stage 1 reaches 95% pass rate
        Then cascade completes successfully and skill doesn't appear in needs-review."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            history_dir = root / "tune-history" / "test-skill"
            history_dir.mkdir(parents=True, exist_ok=True)
            review_file = root / "needs-review.md"

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

            # Stage 1 succeeds
            def mock_run_stage(model, max_iter, target):
                if model == "gpt-5-mini":
                    return {"pass_rate": 0.96, "model": "gpt-5-mini"}

            orchestrator = CascadeOrchestrator(
                skill_name="test-skill",
                history_dir=history_dir,
                config=config,
            )

            with patch.object(orchestrator, "_run_single_stage", side_effect=mock_run_stage):
                result = orchestrator.run()

            # Verify success
            self.assertEqual(result["pass_rate"], 0.96)
            self.assertEqual(result["stage"], 1)
            self.assertFalse(result.get("needs_review", False))

            # Verify skill is NOT added to needs-review
            tracker = NeedsReviewTracker(review_file=review_file)
            self.assertFalse(tracker.is_skill_reviewed("test-skill"))

    def test_cascade_end_to_end_failure_adds_to_needs_review(self):
        """Given cascade fails on both stages
        When cascade completes
        Then skill is added to needs-review.md with history link."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            history_dir = root / "tune-history" / "difficult-skill"
            history_dir.mkdir(parents=True, exist_ok=True)
            review_file = root / "skills-tools" / "needs-review.md"

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

            # Both stages fail to reach 95%
            def mock_run_stage(model, max_iter, target):
                return {"pass_rate": 0.88, "model": model}

            orchestrator = CascadeOrchestrator(
                skill_name="difficult-skill",
                history_dir=history_dir,
                config=config,
            )

            with patch.object(orchestrator, "_run_single_stage", side_effect=mock_run_stage):
                result = orchestrator.run()

            # Verify failure state
            self.assertEqual(result["pass_rate"], 0.88)
            self.assertTrue(result.get("needs_review", False))
            self.assertEqual(result["best_model"], "claude-haiku-4.5")

            # Add to needs-review tracker
            tracker = NeedsReviewTracker(review_file=review_file)
            tracker.add(
                skill_name="difficult-skill",
                best_model=result["best_model"],
                best_pass_rate=result["best_pass_rate"],
                history_link=f"tune-history/difficult-skill/{result['best_model']}.jsonl",
            )

            # Verify skill appears in needs-review
            self.assertTrue(tracker.is_skill_reviewed("difficult-skill"))
            self.assertTrue(review_file.exists())
            content = review_file.read_text(encoding="utf-8")
            self.assertIn("difficult-skill", content)
            self.assertIn("claude-haiku-4.5", content)

    def test_cascade_end_to_end_stage_2_escalation(self):
        """Given Stage 1 fails but Stage 2 succeeds
        When cascade completes
        Then skill is successfully tuned and doesn't need review."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            history_dir = root / "tune-history" / "tricky-skill"
            history_dir.mkdir(parents=True, exist_ok=True)
            review_file = root / "needs-review.md"

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

            def mock_run_stage(model, max_iter, target):
                if model == "gpt-5-mini":
                    return {"pass_rate": 0.91, "model": "gpt-5-mini"}
                elif model == "claude-haiku-4.5":
                    return {"pass_rate": 0.97, "model": "claude-haiku-4.5"}

            orchestrator = CascadeOrchestrator(
                skill_name="tricky-skill",
                history_dir=history_dir,
                config=config,
            )

            with patch.object(orchestrator, "_run_single_stage", side_effect=mock_run_stage):
                result = orchestrator.run()

            # Verify Stage 2 success
            self.assertEqual(result["pass_rate"], 0.97)
            self.assertEqual(result["stage"], 2)
            self.assertFalse(result.get("needs_review", False))

            # Verify skill doesn't appear in needs-review
            tracker = NeedsReviewTracker(review_file=review_file)
            self.assertFalse(tracker.is_skill_reviewed("tricky-skill"))

    def test_cascade_end_to_end_idempotent_needs_review_updates(self):
        """Given needs-review already contains a skill
        When cascade updates metrics for the same skill
        Then needs-review is updated with new metrics (not duplicated)."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            review_file = root / "needs-review.md"

            # First tuning attempt
            tracker = NeedsReviewTracker(review_file=review_file)
            tracker.add(
                skill_name="improving-skill",
                best_model="gpt-5-mini",
                best_pass_rate=0.85,
                history_link="tune-history/improving-skill/gpt-5-mini.jsonl",
            )

            # Verify initial entry
            content = review_file.read_text(encoding="utf-8")
            self.assertIn("85%", content)
            self.assertIn("gpt-5-mini", content)

            # Second tuning attempt with better result
            tracker.add(
                skill_name="improving-skill",
                best_model="claude-haiku-4.5",
                best_pass_rate=0.92,
                history_link="tune-history/improving-skill/claude-haiku-4.5.jsonl",
            )

            # Verify updated entry (not duplicated in checklist section)
            content = review_file.read_text(encoding="utf-8")
            self.assertIn("92%", content)
            self.assertIn("claude-haiku-4.5", content)
            # Count only checklist entries (starting with "- [ ]")
            checklist_lines = [l for l in content.split('\n') if l.startswith("- [ ]")]
            improving_skill_count = sum(1 for l in checklist_lines if "improving-skill" in l)
            self.assertEqual(improving_skill_count, 1)  # Only one entry in checklist


if __name__ == "__main__":
    unittest.main()
