import csv
import tempfile
import unittest
from pathlib import Path

from skills.migration_map import build_review_task_skill_rows, write_migration_inventory


class TestMigrationCoverage(unittest.TestCase):
    def test_generated_inventory_preserves_all_review_tasks_and_valid_skill_targets(self):
        repo_root = Path(__file__).resolve().parents[3]
        rows = build_review_task_skill_rows(
            review_tasks_dir=repo_root / "review-tasks",
            skills_dir=repo_root / "skills",
        )

        review_task_files = sorted(
            path
            for path in (repo_root / "review-tasks").rglob("*.md")
            if path.name not in {"INDEX.md", "TEMPLATE.md"}
        )
        self.assertEqual(len(rows), len(review_task_files))

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "migration-map.csv"
            write_migration_inventory(rows=rows, output_path=output_path)
            with output_path.open("r", encoding="utf-8", newline="") as handle:
                written_rows = list(csv.DictReader(handle))

        self.assertEqual(len(written_rows), len(review_task_files))
        mapped_tasks = {row["review_task"] for row in written_rows}
        expected_tasks = {
            path.relative_to(repo_root / "review-tasks").with_suffix("").as_posix()
            for path in review_task_files
        }
        self.assertSetEqual(mapped_tasks, expected_tasks)

        available_skills = {
            path.stem for path in (repo_root / "skills" / "concerns").glob("*.md")
        }
        mapped_skills = {row["skill"] for row in written_rows}
        self.assertSetEqual(mapped_skills - available_skills, set())

    def test_migration_rows_preserve_platform_and_owasp_lineage_for_security_tasks(self):
        repo_root = Path(__file__).resolve().parents[3]
        rows = build_review_task_skill_rows(
            review_tasks_dir=repo_root / "review-tasks",
            skills_dir=repo_root / "skills",
        )

        security_rows = [row for row in rows if row["category"] == "security"]
        self.assertGreater(len(security_rows), 0)
        self.assertTrue(all(row["platform"] for row in security_rows))
        security_skill_paths = sorted((repo_root / "skills" / "concerns").glob("security-*.md"))
        self.assertGreater(len(security_skill_paths), 0)
        for skill_path in security_skill_paths:
            with self.subTest(skill=skill_path.name):
                content = skill_path.read_text(encoding="utf-8").lower()
                self.assertIn("owasp", content)


if __name__ == "__main__":
    unittest.main()
