import unittest


class TestManualVerificationChecklist(unittest.TestCase):
    def test_manual_verification_steps_defined(self):
        steps = [
            "run adversarial-review on a sample diff and inspect sqlite run rows",
            "run adversarial-resume on same repo/pr/commit_sha and verify no duplicate run row",
            "verify confidence buckets include high-confidence, contested, debunked outputs",
            "simulate merge and run adversarial-cleanup to confirm archive/purge/prune/vacuum actions",
            "force quorum/provider failure path and verify degraded fallback metadata is present",
        ]
        self.assertEqual(len(steps), 5)
        merged = " ".join(steps)
        self.assertIn("adversarial-review", merged)
        self.assertIn("adversarial-resume", merged)
        self.assertIn("adversarial-cleanup", merged)


if __name__ == "__main__":
    unittest.main()
