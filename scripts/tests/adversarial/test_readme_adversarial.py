import unittest
from pathlib import Path


class TestReadmeAdversarialLifecycle(unittest.TestCase):
    def test_readme_documents_adversarial_run_resume_cleanup_and_sqlite(self):
        repo_root = Path(__file__).resolve().parents[3]
        readme_path = repo_root / "README.md"
        content = readme_path.read_text(encoding="utf-8").lower()

        self.assertIn("adversarial-review", content)
        self.assertIn("adversarial-resume", content)
        self.assertIn("adversarial-cleanup", content)
        self.assertIn("sqlite", content)
        self.assertIn(".skill-machine/adversarial.db", content)
        self.assertIn("quorum", content)
        self.assertIn("fallback", content)


if __name__ == "__main__":
    unittest.main()
