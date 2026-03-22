import unittest
from pathlib import Path

import yaml


class TestComposePolicy(unittest.TestCase):
    def test_policy_contains_signal_mappings_and_fallback_core(self):
        repo_root = Path(__file__).resolve().parents[3]
        policy_path = repo_root / "scripts" / "compose" / "policy.yaml"
        self.assertTrue(policy_path.exists())

        policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
        self.assertIn("core", policy)
        self.assertIn("fallback", policy)
        self.assertIn("signals", policy)
        self.assertIn("python", policy["signals"])
        self.assertIn("ci_github_actions", policy["signals"])
        self.assertIn("review-orchestrator", " ".join(policy["core"]))

    def test_policy_dependencies_are_skill_paths_only(self):
        repo_root = Path(__file__).resolve().parents[3]
        policy_path = repo_root / "scripts" / "compose" / "policy.yaml"
        policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))

        dependencies = list(policy.get("core", [])) + list(policy.get("fallback", []))
        for signal in policy.get("signals", {}).values():
            dependencies.extend(signal.get("dependencies", []))

        for dependency in dependencies:
            with self.subTest(dependency=dependency):
                self.assertIn("/skills/", dependency)
                self.assertNotIn("review-tasks", dependency)
                self.assertNotIn("review_tasks", dependency)

    def test_policy_declares_skill_only_atomic_primitives(self):
        repo_root = Path(__file__).resolve().parents[3]
        policy_text = (repo_root / "scripts" / "compose" / "policy.yaml").read_text(
            encoding="utf-8"
        ).lower()
        self.assertIn("skills", policy_text)
        self.assertNotIn("review-task", policy_text)
        self.assertNotIn("review tasks", policy_text)

    def test_policy_declares_atomic_primitive_as_skills(self):
        repo_root = Path(__file__).resolve().parents[3]
        policy = yaml.safe_load(
            (repo_root / "scripts" / "compose" / "policy.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(policy.get("atomic_primitive"), "skills")


if __name__ == "__main__":
    unittest.main()
