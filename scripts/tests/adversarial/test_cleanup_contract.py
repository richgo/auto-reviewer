import unittest
from pathlib import Path


class TestAdversarialCleanupContract(unittest.TestCase):
    def test_cleanup_contract_defines_merge_trigger_purge_prune_and_vacuum(self):
        repo_root = Path(__file__).resolve().parents[3]
        cleanup_path = repo_root / "agents" / "adversarial" / "cleanup.md"

        self.assertTrue(cleanup_path.exists())
        content = cleanup_path.read_text(encoding="utf-8").lower()

        self.assertIn("merge", content)
        self.assertIn("archive", content)
        self.assertIn("purge", content)
        self.assertIn("prune", content)
        self.assertIn("vacuum", content)
        self.assertIn("idempotent", content)


if __name__ == "__main__":
    unittest.main()
