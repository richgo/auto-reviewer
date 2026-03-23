import unittest
from pathlib import Path


class TestAdversarialOrchestratorHandoff(unittest.TestCase):
    def test_review_orchestrator_documents_adversarial_handoff_and_degraded_status(self):
        repo_root = Path(__file__).resolve().parents[3]
        orchestrator_path = repo_root / "skills" / "review-orchestrator" / "SKILL.md"
        content = orchestrator_path.read_text(encoding="utf-8").lower()

        self.assertIn("adversarial-review", content)
        self.assertIn("adversarial-resume", content)
        self.assertIn("repo", content)
        self.assertIn("pr", content)
        self.assertIn("commit", content)
        self.assertIn("degraded", content)


if __name__ == "__main__":
    unittest.main()
