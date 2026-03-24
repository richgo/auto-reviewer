import sys
import json
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from skill_machine.pipeline import run_tune_stage


class TestPipelineTuneStage(unittest.TestCase):
    def test_tune_stage_resolves_canonical_skill_and_eval_paths(self):
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

            result = run_tune_stage(
                skill_name="security-injection",
                skills_dir=skills_dir,
                evals_dir=evals_dir,
                state_dir=state_dir,
            )

        self.assertEqual("security-injection", result["skill"])
        self.assertEqual(str(skills_dir / "security-injection" / "SKILL.md"), result["skill_path"])
        self.assertEqual(str(evals_dir / "security-injection.json"), result["eval_path"])
        self.assertEqual(str(state_dir / "security-injection.json"), result["state_path"])

    def test_tune_stage_fails_when_eval_file_is_missing(self):
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

            with self.assertRaisesRegex(
                FileNotFoundError,
                "Eval file not found",
            ):
                run_tune_stage(
                    skill_name="security-injection",
                    skills_dir=skills_dir,
                    evals_dir=evals_dir,
                    state_dir=state_dir,
                )

    def test_tune_stage_reads_model_sequence_from_workflow_state(self):
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
            state_dir.mkdir(parents=True, exist_ok=True)
            (state_dir / "security-injection.json").write_text(
                json.dumps(
                    {
                        "skill": "security-injection",
                        "tune_models": ["gpt-5-mini", "claude-haiku-4.5"],
                    }
                ),
                encoding="utf-8",
            )

            result = run_tune_stage(
                skill_name="security-injection",
                skills_dir=skills_dir,
                evals_dir=evals_dir,
                state_dir=state_dir,
            )

        self.assertEqual(["gpt-5-mini", "claude-haiku-4.5"], result["tune_models"])


if __name__ == "__main__":
    unittest.main()
