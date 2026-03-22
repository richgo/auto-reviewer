import tempfile
import unittest
from pathlib import Path

from skills.canonical_inventory import (
    build_canonical_skill_inventory,
    validate_canonical_folder_contract,
)


class TestCanonicalInventory(unittest.TestCase):
    def test_build_inventory_flattens_review_task_folders(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            (skills_dir / "concerns").mkdir(parents=True)
            (skills_dir / "review-tasks" / "api-design" / "mobile").mkdir(parents=True)

            (skills_dir / "concerns" / "api-design.md").write_text("skill", encoding="utf-8")
            (skills_dir / "review-tasks" / "api-design" / "input-validation.md").write_text(
                "skill",
                encoding="utf-8",
            )
            (
                skills_dir
                / "review-tasks"
                / "api-design"
                / "mobile"
                / "api-versioning.md"
            ).write_text("skill", encoding="utf-8")

            rows = build_canonical_skill_inventory(skills_dir=skills_dir)

        self.assertEqual(
            rows,
            [
                {
                    "canonical_skill": "api-design",
                    "source_kind": "legacy-file",
                    "source_path": "skills/concerns/api-design.md",
                },
                {
                    "canonical_skill": "api-design",
                    "source_kind": "review-task-folder",
                    "source_path": "skills/review-tasks/api-design",
                },
                {
                    "canonical_skill": "api-design-mobile",
                    "source_kind": "review-task-folder",
                    "source_path": "skills/review-tasks/api-design/mobile",
                },
            ],
        )

    def test_build_inventory_includes_all_active_skill_groups(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            (skills_dir / "concerns").mkdir(parents=True)
            (skills_dir / "core").mkdir(parents=True)
            (skills_dir / "languages").mkdir(parents=True)
            (skills_dir / "outputs").mkdir(parents=True)
            (skills_dir / "tuning").mkdir(parents=True)

            (skills_dir / "concerns" / "api-design.md").write_text("skill", encoding="utf-8")
            (skills_dir / "core" / "review-orchestrator.md").write_text("skill", encoding="utf-8")
            (skills_dir / "languages" / "python.md").write_text("skill", encoding="utf-8")
            (skills_dir / "outputs" / "inline-comments.md").write_text("skill", encoding="utf-8")
            (skills_dir / "tuning" / "skill-optimizer.md").write_text("skill", encoding="utf-8")

            rows = build_canonical_skill_inventory(skills_dir=skills_dir)

        canonical_names = {row["canonical_skill"] for row in rows}
        self.assertEqual(
            canonical_names,
            {
                "api-design",
                "review-orchestrator",
                "python",
                "inline-comments",
                "skill-optimizer",
            },
        )

    def test_build_inventory_includes_folder_based_active_skills(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            (skills_dir / "concerns").mkdir(parents=True)
            (skills_dir / "concerns" / "api-design").mkdir(parents=True)

            (skills_dir / "concerns" / "api-design" / "SKILL.md").write_text(
                "skill",
                encoding="utf-8",
            )

            rows = build_canonical_skill_inventory(skills_dir=skills_dir)

        self.assertEqual(
            rows,
            [
                {
                    "canonical_skill": "api-design",
                    "source_kind": "canonical-folder",
                    "source_path": "skills/concerns/api-design/SKILL.md",
                }
            ],
        )

    def test_validate_canonical_folder_contract_requires_skill_md_files_to_move(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            (skills_dir / "concerns").mkdir(parents=True)
            (skills_dir / "concerns" / "api-design.md").write_text("skill", encoding="utf-8")

            errors = validate_canonical_folder_contract(skills_dir=skills_dir)

        self.assertEqual(
            errors,
            [
                "Legacy skill file requires canonical folder: skills/concerns/api-design.md"
            ],
        )


if __name__ == "__main__":
    unittest.main()
