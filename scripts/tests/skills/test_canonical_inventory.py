import tempfile
import unittest
from pathlib import Path

from skills.canonical_inventory import (
    build_canonical_skill_inventory,
    validate_canonical_folder_contract,
)


class TestCanonicalInventory(unittest.TestCase):
    def test_build_inventory_lists_flat_skill_folders(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            (skills_dir / "api-design").mkdir(parents=True)
            (skills_dir / "review-orchestrator").mkdir(parents=True)
            (skills_dir / "api-design" / "SKILL.md").write_text("skill", encoding="utf-8")
            (skills_dir / "review-orchestrator" / "SKILL.md").write_text(
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
                    "source_path": "skills/api-design/SKILL.md",
                },
                {
                    "canonical_skill": "review-orchestrator",
                    "source_kind": "canonical-folder",
                    "source_path": "skills/review-orchestrator/SKILL.md",
                },
            ],
        )

    def test_validate_contract_flags_nested_skill_paths(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            (skills_dir / "core" / "review-orchestrator").mkdir(parents=True)
            (skills_dir / "core" / "review-orchestrator" / "SKILL.md").write_text(
                "skill",
                encoding="utf-8",
            )

            errors = validate_canonical_folder_contract(skills_dir=skills_dir)

        self.assertEqual(
            errors,
            [
                "Skill entry must be skills/<skill>/SKILL.md: skills/core/review-orchestrator/SKILL.md"
            ],
        )

    def test_validate_contract_flags_non_skill_md_filename(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            (skills_dir / "api-design").mkdir(parents=True)
            (skills_dir / "api-design" / "skill.md").write_text("skill", encoding="utf-8")

            errors = validate_canonical_folder_contract(skills_dir=skills_dir)

        self.assertEqual(
            errors,
            ["Skill entry must be named SKILL.md: skills/api-design/skill.md"],
        )

    def test_repository_skills_tree_is_flat_skill_folder_layout(self):
        repo_root = Path(__file__).resolve().parents[3]
        errors = validate_canonical_folder_contract(skills_dir=repo_root / "skills")
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
