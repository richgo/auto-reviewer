import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


class TestSkillMachineNamespaceMigration(unittest.TestCase):
    def test_tuning_modules_resolve_from_skill_machine_package(self):
        import skill_machine.pipeline as pipeline
        import skill_machine.workflow_state as workflow_state

        self.assertTrue(hasattr(pipeline, "run_create_stage"))
        self.assertTrue(hasattr(workflow_state, "resolve_skill_state"))

    def test_legacy_tune_directories_do_not_exist(self):
        repo_root = Path(__file__).resolve().parents[3]
        self.assertFalse((repo_root / "scripts" / "tune").exists())
        self.assertFalse((repo_root / "scripts" / "tests" / "tune").exists())


if __name__ == "__main__":
    unittest.main()
