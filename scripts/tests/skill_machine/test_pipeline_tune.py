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

    def test_tune_stage_runs_benchmark_gate_and_marks_gated_on_failed_validation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            state_dir = root / ".skill-machine" / "workflow"
            reports_dir = root / "benchmark-results"
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
                        "tune_models": ["gpt-5-mini"],
                        "best_model": "gpt-5-mini",
                        "best_pass_rate": 0.96,
                        "target_pass_rate": 0.95,
                    }
                ),
                encoding="utf-8",
            )

            def fake_benchmark_runner(*, skill_name, skill_path, eval_path):
                artifact = reports_dir / f"{skill_name}.json"
                artifact.parent.mkdir(parents=True, exist_ok=True)
                artifact.write_text('{"benchmark_passed": false}', encoding="utf-8")
                return {"passed": False, "artifact_path": str(artifact)}

            result = run_tune_stage(
                skill_name="security-injection",
                skills_dir=skills_dir,
                evals_dir=evals_dir,
                state_dir=state_dir,
                benchmark_runner=fake_benchmark_runner,
            )

            self.assertEqual("gated", result["outcome_status"])
            self.assertTrue(Path(result["benchmark_artifact_path"]).exists())

    def test_tune_stage_persists_benchmark_artifact_path_to_workflow_state(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            state_dir = root / ".skill-machine" / "workflow"
            reports_dir = root / "benchmark-results"
            (skills_dir / "security-injection").mkdir(parents=True)
            (skills_dir / "security-injection" / "SKILL.md").write_text(
                "skill",
                encoding="utf-8",
            )
            evals_dir.mkdir(parents=True)
            (evals_dir / "security-injection.json").write_text("{}", encoding="utf-8")
            state_dir.mkdir(parents=True, exist_ok=True)
            state_path = state_dir / "security-injection.json"
            state_path.write_text(
                json.dumps(
                    {
                        "skill": "security-injection",
                        "tune_models": ["gpt-5-mini"],
                        "best_model": "gpt-5-mini",
                        "best_pass_rate": 0.96,
                        "target_pass_rate": 0.95,
                    }
                ),
                encoding="utf-8",
            )

            def fake_benchmark_runner(*, skill_name, skill_path, eval_path):
                artifact = reports_dir / f"{skill_name}.json"
                artifact.parent.mkdir(parents=True, exist_ok=True)
                artifact.write_text('{"benchmark_passed": true}', encoding="utf-8")
                return {"passed": True, "artifact_path": str(artifact)}

            run_tune_stage(
                skill_name="security-injection",
                skills_dir=skills_dir,
                evals_dir=evals_dir,
                state_dir=state_dir,
                benchmark_runner=fake_benchmark_runner,
            )

            state_payload = state_path.read_text(encoding="utf-8")
            self.assertIn('"benchmark_artifact_path"', state_payload)

    def test_tune_stage_keeps_local_calibration_state_separate_from_canonical_state(self):
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
            canonical_state_path = state_dir / "security-injection.json"
            canonical_state_path.write_text(
                json.dumps(
                    {
                        "skill": "security-injection",
                        "status": "canonical",
                    }
                ),
                encoding="utf-8",
            )

            result = run_tune_stage(
                skill_name="security-injection",
                skills_dir=skills_dir,
                evals_dir=evals_dir,
                state_dir=state_dir,
                local_calibration=True,
            )

            local_state = Path(result["state_path"])
            self.assertTrue(local_state.exists())
            self.assertIn("local-calibration", str(local_state))
            canonical_state = canonical_state_path.read_text(encoding="utf-8")
            self.assertIn('"status": "canonical"', canonical_state)


if __name__ == "__main__":
    unittest.main()
