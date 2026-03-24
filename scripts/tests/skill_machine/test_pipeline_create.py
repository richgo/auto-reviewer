import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from skill_machine.pipeline import run_create_stage


class TestPipelineCreateStage(unittest.TestCase):
    def test_create_stage_resolves_canonical_skill_and_returns_artifact_paths(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            state_dir = root / ".skill-machine" / "workflow"
            (skills_dir / "security-injection").mkdir(parents=True)
            (skills_dir / "security-injection" / "SKILL.md").write_text(
                "skill",
                encoding="utf-8",
            )
            evals_dir.mkdir(parents=True)
            (evals_dir / "security-injection.json").write_text("{}", encoding="utf-8")

            result = run_create_stage(
                skill_name="security-injection",
                skills_dir=skills_dir,
                evals_dir=evals_dir,
                state_dir=state_dir,
            )

        self.assertEqual("security-injection", result["skill"])
        self.assertEqual(str(skills_dir / "security-injection" / "SKILL.md"), result["skill_path"])
        self.assertEqual(str(evals_dir / "security-injection.json"), result["eval_path"])
        self.assertEqual(str(state_dir / "security-injection.json"), result["state_path"])

    def test_create_stage_can_persist_create_started_state(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            state_dir = root / ".skill-machine" / "workflow"
            (skills_dir / "security-injection").mkdir(parents=True)
            (skills_dir / "security-injection" / "SKILL.md").write_text(
                "skill",
                encoding="utf-8",
            )
            evals_dir.mkdir(parents=True)
            (evals_dir / "security-injection.json").write_text("{}", encoding="utf-8")

            result = run_create_stage(
                skill_name="security-injection",
                skills_dir=skills_dir,
                evals_dir=evals_dir,
                state_dir=state_dir,
                persist_state=True,
            )

            state_path = Path(result["state_path"])
            self.assertTrue(state_path.exists())
            content = state_path.read_text(encoding="utf-8")
            self.assertIn('"status": "create_started"', content)

    def test_create_stage_records_timestamps_when_state_is_persisted(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            state_dir = root / ".skill-machine" / "workflow"
            (skills_dir / "security-injection").mkdir(parents=True)
            (skills_dir / "security-injection" / "SKILL.md").write_text(
                "skill",
                encoding="utf-8",
            )
            evals_dir.mkdir(parents=True)
            (evals_dir / "security-injection.json").write_text("{}", encoding="utf-8")

            result = run_create_stage(
                skill_name="security-injection",
                skills_dir=skills_dir,
                evals_dir=evals_dir,
                state_dir=state_dir,
                persist_state=True,
            )

            payload = Path(result["state_path"]).read_text(encoding="utf-8")
            self.assertIn('"updated_at"', payload)

    def test_create_stage_generates_eval_stub_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            state_dir = root / ".skill-machine" / "workflow"
            (skills_dir / "security-injection").mkdir(parents=True)
            (skills_dir / "security-injection" / "SKILL.md").write_text(
                "skill",
                encoding="utf-8",
            )
            evals_dir.mkdir(parents=True)

            result = run_create_stage(
                skill_name="security-injection",
                skills_dir=skills_dir,
                evals_dir=evals_dir,
                state_dir=state_dir,
                generate_eval_stub=True,
            )

            eval_path = Path(result["eval_path"])
            self.assertTrue(eval_path.exists())
            content = eval_path.read_text(encoding="utf-8")
            self.assertIn('"skill": "security-injection"', content)
            self.assertIn('"cases": []', content)

    def test_create_stage_persists_not_ready_status_when_eval_stub_fails_readiness(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            state_dir = root / ".skill-machine" / "workflow"
            (skills_dir / "security-injection").mkdir(parents=True)
            (skills_dir / "security-injection" / "SKILL.md").write_text(
                "skill",
                encoding="utf-8",
            )
            evals_dir.mkdir(parents=True)

            result = run_create_stage(
                skill_name="security-injection",
                skills_dir=skills_dir,
                evals_dir=evals_dir,
                state_dir=state_dir,
                persist_state=True,
                generate_eval_stub=True,
                validate_eval_readiness=True,
            )

            self.assertFalse(result["eval_ready"])
            state_payload = Path(result["state_path"]).read_text(encoding="utf-8")
            self.assertIn('"status": "create_eval_not_ready"', state_payload)


if __name__ == "__main__":
    unittest.main()
