import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from skill_machine.workflow_state import resolve_skill_state


class TestWorkflowState(unittest.TestCase):
    def test_resolve_skill_state_maps_canonical_skill_to_eval_and_state(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            state_dir = root / "state"
            (skills_dir / "security-injection").mkdir(parents=True)
            (skills_dir / "security-injection" / "SKILL.md").write_text(
                "content",
                encoding="utf-8",
            )
            evals_dir.mkdir(parents=True)
            (evals_dir / "security-injection.json").write_text("{}", encoding="utf-8")

            state = resolve_skill_state(
                skill_name="security-injection",
                skills_dir=skills_dir,
                evals_dir=evals_dir,
                state_dir=state_dir,
            )

        self.assertEqual("security-injection", state.skill_name)
        self.assertEqual(skills_dir / "security-injection" / "SKILL.md", state.skill_path)
        self.assertEqual(evals_dir / "security-injection.json", state.eval_path)
        self.assertEqual(state_dir / "security-injection.json", state.state_path)

    def test_resolve_skill_state_raises_when_skill_file_missing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            state_dir = root / "state"
            skills_dir.mkdir(parents=True)
            evals_dir.mkdir(parents=True)
            (evals_dir / "security-injection.json").write_text("{}", encoding="utf-8")

            with self.assertRaises(FileNotFoundError):
                resolve_skill_state(
                    skill_name="security-injection",
                    skills_dir=skills_dir,
                    evals_dir=evals_dir,
                    state_dir=state_dir,
                )

    def test_resolve_skill_state_raises_when_eval_file_missing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            state_dir = root / "state"
            (skills_dir / "security-injection").mkdir(parents=True)
            (skills_dir / "security-injection" / "SKILL.md").write_text(
                "content",
                encoding="utf-8",
            )
            evals_dir.mkdir(parents=True)

            with self.assertRaises(FileNotFoundError):
                resolve_skill_state(
                    skill_name="security-injection",
                    skills_dir=skills_dir,
                    evals_dir=evals_dir,
                    state_dir=state_dir,
                )


if __name__ == "__main__":
    unittest.main()
