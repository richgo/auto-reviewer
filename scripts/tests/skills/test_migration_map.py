import csv
import tempfile
import unittest
from pathlib import Path

from skills.migration_map import build_review_task_skill_rows, write_migration_inventory


class TestMigrationMap(unittest.TestCase):
    def test_build_review_task_skill_rows_deterministically_maps_review_tasks_to_skill_and_preserves_owasp_lineage(
        self,
    ):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            review_tasks_dir = root / "review-tasks"
            concerns_dir = root / "skills" / "concerns"
            review_tasks_dir.mkdir(parents=True)
            concerns_dir.mkdir(parents=True)

            (review_tasks_dir / "security").mkdir()
            (review_tasks_dir / "security" / "xss.md").write_text(
                "\n".join(
                    [
                        "# Task: XSS",
                        "## Category",
                        "security",
                        "## Severity",
                        "high",
                        "## Platforms",
                        "web",
                        "## Description",
                        "Cross-site scripting in rendered content.",
                        "[OWASP: Cross_Site_Scripting_Prevention, DOM_based_XSS_Prevention]",
                    ]
                ),
                encoding="utf-8",
            )
            (review_tasks_dir / "data").mkdir()
            (review_tasks_dir / "data" / "schema-validation.md").write_text(
                "\n".join(
                    [
                        "# Task: Schema Validation",
                        "## Category",
                        "data",
                        "## Severity",
                        "medium",
                        "## Platforms",
                        "api, microservices",
                        "## Description",
                        "Missing schema validation on payloads.",
                        "[OWASP: Input_Validation]",
                    ]
                ),
                encoding="utf-8",
            )
            (review_tasks_dir / "testing").mkdir()
            (review_tasks_dir / "testing" / "mock-overuse.md").write_text(
                "\n".join(
                    [
                        "# Task: Mock Overuse",
                        "## Category",
                        "testing",
                        "## Severity",
                        "low",
                        "## Platforms",
                        "all",
                        "## Description",
                        "Tests that only use mocks and no integration coverage.",
                    ]
                ),
                encoding="utf-8",
            )

            (concerns_dir / "security-client-side").mkdir()
            (concerns_dir / "data-integrity").mkdir()
            (concerns_dir / "testing").mkdir()
            (concerns_dir / "security-client-side" / "SKILL.md").write_text("skill", encoding="utf-8")
            (concerns_dir / "data-integrity" / "SKILL.md").write_text("skill", encoding="utf-8")
            (concerns_dir / "testing" / "SKILL.md").write_text("skill", encoding="utf-8")

            rows = build_review_task_skill_rows(
                review_tasks_dir=review_tasks_dir, skills_dir=concerns_dir.parent
            )
            csv_path = root / "migration-map.csv"
            write_migration_inventory(rows=rows, output_path=csv_path)

            with csv_path.open("r", encoding="utf-8", newline="") as handle:
                written_rows = list(csv.DictReader(handle))

        self.assertEqual(
            rows,
            [
                {
                    "review_task": "data/schema-validation",
                    "category": "data",
                    "platform": "api,microservices",
                    "skill": "data-integrity",
                    "skill_path": "skills/data-integrity/SKILL.md",
                    "owasp_refs": "Input_Validation",
                },
                {
                    "review_task": "security/xss",
                    "category": "security",
                    "platform": "web",
                    "skill": "security-client-side",
                    "skill_path": "skills/security-client-side/SKILL.md",
                    "owasp_refs": "Cross_Site_Scripting_Prevention|DOM_based_XSS_Prevention",
                },
                {
                    "review_task": "testing/mock-overuse",
                    "category": "testing",
                    "platform": "all",
                    "skill": "testing",
                    "skill_path": "skills/testing/SKILL.md",
                    "owasp_refs": "",
                },
            ],
        )
        self.assertEqual(written_rows, rows)

    def test_concern_skills_do_not_reference_review_task_files_after_migration(self):
        repo_root = Path(__file__).resolve().parents[3]
        offending = []
        for skill_path in sorted((repo_root / "skills" / "concerns").glob("*.md")):
            content = skill_path.read_text(encoding="utf-8")
            if "review-tasks/" in content:
                offending.append(skill_path.name)

        self.assertEqual(offending, [])

    def test_migration_map_emits_canonical_skill_folder_paths(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            review_tasks_dir = root / "review-tasks"
            concerns_dir = root / "skills" / "concerns"
            review_tasks_dir.mkdir(parents=True)
            concerns_dir.mkdir(parents=True)

            (review_tasks_dir / "testing").mkdir()
            (review_tasks_dir / "testing" / "mock-overuse.md").write_text(
                "\n".join(
                    [
                        "# Task: Mock Overuse",
                        "## Category",
                        "testing",
                        "## Severity",
                        "low",
                        "## Platforms",
                        "all",
                        "## Description",
                        "Tests rely only on mocks.",
                    ]
                ),
                encoding="utf-8",
            )
            (concerns_dir / "testing").mkdir()
            (concerns_dir / "testing" / "SKILL.md").write_text("skill", encoding="utf-8")

            rows = build_review_task_skill_rows(
                review_tasks_dir=review_tasks_dir,
                skills_dir=concerns_dir.parent,
            )

        self.assertEqual(rows[0]["skill_path"], "skills/testing/SKILL.md")


if __name__ == "__main__":
    unittest.main()
