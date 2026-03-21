import unittest
from pathlib import Path


class TestAdversarialOutputContracts(unittest.TestCase):
    def test_review_report_mentions_confidence_consensus_and_debate_summary(self):
        repo_root = Path(__file__).resolve().parents[3]
        report_path = repo_root / "skills" / "outputs" / "review-report.md"
        content = report_path.read_text(encoding="utf-8").lower()

        self.assertIn("confidence", content)
        self.assertIn("consensus", content)
        self.assertIn("debate", content)


if __name__ == "__main__":
    unittest.main()
