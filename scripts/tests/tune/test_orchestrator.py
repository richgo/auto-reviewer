import tempfile
import unittest
from pathlib import Path

import yaml

from tune.orchestrator import build_plan, build_run_plan, compose_run_plan


PRIMARY_MODEL = "gpt-4.1"
SECONDARY_MODEL = "gemini-2.5-pro"
TERTIARY_MODEL = "gpt-4o"


class TestOrchestrator(unittest.TestCase):
    def test_build_plan_generates_skill_model_pairs_from_config(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            skills_dir.mkdir(parents=True)
            evals_dir.mkdir(parents=True)
            (skills_dir / "security-injection").mkdir()
            (skills_dir / "correctness").mkdir()
            (skills_dir / "security-injection" / "SKILL.md").write_text("skill", encoding="utf-8")
            (skills_dir / "correctness" / "SKILL.md").write_text("skill", encoding="utf-8")
            (evals_dir / "security-injection.json").write_text("{}", encoding="utf-8")
            (evals_dir / "correctness.json").write_text("{}", encoding="utf-8")

            config = root / "config.yaml"
            config.write_text(
                yaml.safe_dump({"models": [PRIMARY_MODEL, SECONDARY_MODEL]}),
                encoding="utf-8",
            )

            pairs = build_plan(
                skills_dir=root / "skills",
                evals_dir=evals_dir,
                config_path=config,
                skills_filter=None,
                models_filter=None,
            )

        self.assertEqual(
            pairs,
            [
                ("correctness", SECONDARY_MODEL),
                ("correctness", PRIMARY_MODEL),
                ("security-injection", SECONDARY_MODEL),
                ("security-injection", PRIMARY_MODEL),
            ],
        )

    def test_build_run_plan_applies_filters_trigger_and_run_id(self):
        pairs = [
            ("correctness", SECONDARY_MODEL),
            ("correctness", PRIMARY_MODEL),
            ("security-injection", SECONDARY_MODEL),
            ("security-injection", PRIMARY_MODEL),
        ]
        run_plan = build_run_plan(
            pairs=pairs,
            skills_filter=["security-injection"],
            models_filter=[PRIMARY_MODEL],
            trigger="schedule",
            run_id="run-123",
        )
        self.assertEqual(
            run_plan,
            [
                {
                    "run_id": "run-123",
                    "trigger": "schedule",
                    "skill": "security-injection",
                    "model": PRIMARY_MODEL,
                }
            ],
        )

    def test_build_plan_is_deterministic_for_repeated_calls(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            skills_dir.mkdir(parents=True)
            evals_dir.mkdir(parents=True)
            for name in ["security-injection", "correctness", "concurrency"]:
                (skills_dir / name).mkdir()
                (skills_dir / name / "SKILL.md").write_text("skill", encoding="utf-8")
                (evals_dir / f"{name}.json").write_text("{}", encoding="utf-8")
            config = root / "config.yaml"
            config.write_text(yaml.safe_dump({"models": ["z-model", "a-model"]}), encoding="utf-8")

            first = build_plan(
                skills_dir=root / "skills",
                evals_dir=evals_dir,
                config_path=config,
                skills_filter=None,
                models_filter=None,
            )
            second = build_plan(
                skills_dir=root / "skills",
                evals_dir=evals_dir,
                config_path=config,
                skills_filter=None,
                models_filter=None,
            )

        self.assertEqual(first, second)

    def test_compose_run_plan_uses_cli_model_filter_when_config_has_no_models(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            skills_dir.mkdir(parents=True)
            evals_dir.mkdir(parents=True)
            (skills_dir / "security-injection").mkdir()
            (skills_dir / "security-injection" / "SKILL.md").write_text("skill", encoding="utf-8")
            (evals_dir / "security-injection.json").write_text("{}", encoding="utf-8")
            config = root / "config.yaml"
            config.write_text(yaml.safe_dump({}), encoding="utf-8")

            run_plan = compose_run_plan(
                skills_dir=root / "skills",
                evals_dir=evals_dir,
                config_path=config,
                skills_filter=["security-injection"],
                models_filter=["gpt-4.1"],
                trigger="manual",
                run_id="manual-check",
            )

        self.assertEqual(
            run_plan,
            [
                {
                    "run_id": "manual-check",
                    "trigger": "manual",
                    "skill": "security-injection",
                    "model": "gpt-4.1",
                }
            ],
        )

    def test_build_plan_filters_by_skills_prefix(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            skills_dir.mkdir(parents=True)
            evals_dir.mkdir(parents=True)
            for name in ["security-injection", "security-auth", "correctness", "concurrency"]:
                (skills_dir / name).mkdir()
                (skills_dir / name / "SKILL.md").write_text("skill", encoding="utf-8")
                (evals_dir / f"{name}.json").write_text("{}", encoding="utf-8")
            config = root / "config.yaml"
            config.write_text(yaml.safe_dump({"models": ["gpt-4.1"]}), encoding="utf-8")

            pairs = build_plan(
                skills_dir=root / "skills",
                evals_dir=evals_dir,
                config_path=config,
                skills_filter=None,
                models_filter=None,
                skills_prefix="security-",
            )

        self.assertEqual(
            pairs,
            [
                ("security-auth", "gpt-4.1"),
                ("security-injection", "gpt-4.1"),
            ],
        )

    def test_build_plan_skills_prefix_excludes_non_matching_skills(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            skills_dir.mkdir(parents=True)
            evals_dir.mkdir(parents=True)
            for name in ["security-injection", "correctness"]:
                (skills_dir / name).mkdir()
                (skills_dir / name / "SKILL.md").write_text("skill", encoding="utf-8")
                (evals_dir / f"{name}.json").write_text("{}", encoding="utf-8")
            config = root / "config.yaml"
            config.write_text(yaml.safe_dump({"models": ["gpt-4.1"]}), encoding="utf-8")

            pairs_with_prefix = build_plan(
                skills_dir=root / "skills",
                evals_dir=evals_dir,
                config_path=config,
                skills_filter=None,
                models_filter=None,
                skills_prefix="security-",
            )
            pairs_no_prefix = build_plan(
                skills_dir=root / "skills",
                evals_dir=evals_dir,
                config_path=config,
                skills_filter=None,
                models_filter=None,
                skills_prefix=None,
            )

        self.assertEqual(pairs_with_prefix, [("security-injection", "gpt-4.1")])
        self.assertEqual(
            pairs_no_prefix,
            [("correctness", "gpt-4.1"), ("security-injection", "gpt-4.1")],
        )

    def test_compose_run_plan_skills_prefix_scopes_to_security_on_schedule(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            skills_dir.mkdir(parents=True)
            evals_dir.mkdir(parents=True)
            for name in ["security-injection", "security-auth", "correctness"]:
                (skills_dir / name).mkdir()
                (skills_dir / name / "SKILL.md").write_text("skill", encoding="utf-8")
                (evals_dir / f"{name}.json").write_text("{}", encoding="utf-8")
            config = root / "config.yaml"
            config.write_text(
                yaml.safe_dump(
                    {"models": [SECONDARY_MODEL, TERTIARY_MODEL, PRIMARY_MODEL]}
                ),
                encoding="utf-8",
            )

            run_plan = compose_run_plan(
                skills_dir=root / "skills",
                evals_dir=evals_dir,
                config_path=config,
                skills_filter=None,
                models_filter=None,
                skills_prefix="security-",
                trigger="schedule",
                run_id="nightly-42",
            )

        skill_names = sorted({row["skill"] for row in run_plan})
        self.assertEqual(skill_names, ["security-auth", "security-injection"])
        self.assertNotIn("correctness", {row["skill"] for row in run_plan})
        model_names = sorted({row["model"] for row in run_plan})
        self.assertEqual(model_names, ["gemini-2.5-pro", "gpt-4.1", "gpt-4o"])

    def test_build_plan_rejects_eval_payloads_with_review_task_identifier(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            evals_dir = root / "evals"
            skills_dir.mkdir(parents=True)
            evals_dir.mkdir(parents=True)
            (skills_dir / "security-auth").mkdir()
            (skills_dir / "security-auth" / "SKILL.md").write_text("skill", encoding="utf-8")
            (evals_dir / "security-auth.json").write_text(
                '{"skill":"security-auth","review_task":"security/auth-bypass","cases":[]}',
                encoding="utf-8",
            )
            config = root / "config.yaml"
            config.write_text(yaml.safe_dump({"models": ["gpt-4.1"]}), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "review_task"):
                build_plan(
                    skills_dir=root / "skills",
                    evals_dir=evals_dir,
                    config_path=config,
                    skills_filter=None,
                    models_filter=None,
                )

    def test_build_plan_discovers_canonical_folder_skills(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            concerns_dir = root / "skills" / "security-injection"
            evals_dir = root / "evals"
            concerns_dir.mkdir(parents=True)
            evals_dir.mkdir(parents=True)
            (concerns_dir / "SKILL.md").write_text("skill", encoding="utf-8")
            (evals_dir / "security-injection.json").write_text("{}", encoding="utf-8")
            config = root / "config.yaml"
            config.write_text(yaml.safe_dump({"models": ["gpt-4.1"]}), encoding="utf-8")

            pairs = build_plan(
                skills_dir=root / "skills",
                evals_dir=evals_dir,
                config_path=config,
                skills_filter=None,
                models_filter=None,
            )

        self.assertEqual(pairs, [("security-injection", "gpt-4.1")])

    def test_build_plan_ignores_legacy_md_skill_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            concerns_dir = root / "skills"
            evals_dir = root / "evals"
            concerns_dir.mkdir(parents=True)
            evals_dir.mkdir(parents=True)
            (concerns_dir / "security-injection.md").write_text("skill", encoding="utf-8")
            (evals_dir / "security-injection.json").write_text("{}", encoding="utf-8")
            config = root / "config.yaml"
            config.write_text(yaml.safe_dump({"models": ["gpt-4.1"]}), encoding="utf-8")

            pairs = build_plan(
                skills_dir=root / "skills",
                evals_dir=evals_dir,
                config_path=config,
                skills_filter=None,
                models_filter=None,
            )

        self.assertEqual(pairs, [])

    def test_build_plan_discovers_flat_root_skill_folders(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills" / "security-injection"
            evals_dir = root / "evals"
            skills_dir.mkdir(parents=True)
            evals_dir.mkdir(parents=True)
            (skills_dir / "SKILL.md").write_text("skill", encoding="utf-8")
            (evals_dir / "security-injection.json").write_text("{}", encoding="utf-8")
            config = root / "config.yaml"
            config.write_text(yaml.safe_dump({"models": ["gpt-4.1"]}), encoding="utf-8")

            pairs = build_plan(
                skills_dir=root / "skills",
                evals_dir=evals_dir,
                config_path=config,
                skills_filter=None,
                models_filter=None,
            )

        self.assertEqual(pairs, [("security-injection", "gpt-4.1")])


if __name__ == "__main__":
    unittest.main()
