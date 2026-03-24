import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from skill_machine.needs_review import NeedsReviewTracker


class TestNeedsReviewTracker(unittest.TestCase):
    """Test needs-review tracking for skills that fail cascade."""

    def test_needs_review_tracker_adds_skill_to_checklist(self):
        """Given a skill that failed cascade
        When NeedsReviewTracker.add() is called
        Then the skill should be added to needs-review.md with metadata."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            review_file = root / "needs-review.md"

            tracker = NeedsReviewTracker(review_file=review_file)

            # Add a skill that failed cascade
            tracker.add(
                skill_name="security-injection",
                best_model="claude-haiku-4.5",
                best_pass_rate=0.88,
                history_link="tune-history/security-injection/claude-haiku-4.5.jsonl",
            )

            # Verify file was created with the skill
            self.assertTrue(review_file.exists())
            content = review_file.read_text(encoding="utf-8")
            self.assertIn("security-injection", content)
            self.assertIn("claude-haiku-4.5", content)
            self.assertIn("88%", content)  # Format is XX%
            self.assertIn("tune-history/security-injection/claude-haiku-4.5.jsonl", content)

    def test_needs_review_tracker_maintains_checklist_format(self):
        """Given multiple skills added to needs-review
        When NeedsReviewTracker maintains the file
        Then it should format as a sortable markdown checklist."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            review_file = root / "needs-review.md"

            tracker = NeedsReviewTracker(review_file=review_file)

            # Add multiple skills
            tracker.add(
                skill_name="correctness",
                best_model="claude-haiku-4.5",
                best_pass_rate=0.91,
                history_link="tune-history/correctness/claude-haiku-4.5.jsonl",
            )
            tracker.add(
                skill_name="api-design",
                best_model="gpt-5-mini",
                best_pass_rate=0.89,
                history_link="tune-history/api-design/gpt-5-mini.jsonl",
            )

            content = review_file.read_text(encoding="utf-8")

            # Should have header
            self.assertIn("# Skills Needing Manual Review", content)

            # Should have checklist items with unchecked boxes
            self.assertIn("- [ ]", content)

            # Should list both skills
            self.assertIn("correctness", content)
            self.assertIn("api-design", content)

    def test_needs_review_tracker_deduplicates_skills(self):
        """Given a skill already in needs-review
        When NeedsReviewTracker.add() is called with updated metrics
        Then it should update the entry rather than duplicate."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            review_file = root / "needs-review.md"

            tracker = NeedsReviewTracker(review_file=review_file)

            # Add a skill
            tracker.add(
                skill_name="testing",
                best_model="gpt-5-mini",
                best_pass_rate=0.87,
                history_link="tune-history/testing/gpt-5-mini.jsonl",
            )

            # Add the same skill with improved metrics
            tracker.add(
                skill_name="testing",
                best_model="claude-haiku-4.5",
                best_pass_rate=0.92,
                history_link="tune-history/testing/claude-haiku-4.5.jsonl",
            )

            content = review_file.read_text(encoding="utf-8")

            # Should only appear once in the list
            count = content.count("- [ ] **testing**")
            self.assertEqual(count, 1)

            # Should have the updated metrics
            self.assertIn("92%", content)
            self.assertIn("claude-haiku-4.5", content)

    def test_needs_review_tracker_generates_with_links_to_history(self):
        """Given skills in needs-review
        When NeedsReviewTracker generates the file
        Then each entry should link to its tuning history."""

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            review_file = root / "needs-review.md"

            tracker = NeedsReviewTracker(review_file=review_file)

            tracker.add(
                skill_name="performance",
                best_model="claude-haiku-4.5",
                best_pass_rate=0.90,
                history_link="tune-history/performance/claude-haiku-4.5.jsonl",
            )

            content = review_file.read_text(encoding="utf-8")

            # Should have markdown link to history
            self.assertIn("[History]", content)
            self.assertIn("tune-history/performance/claude-haiku-4.5.jsonl", content)


if __name__ == "__main__":
    unittest.main()
