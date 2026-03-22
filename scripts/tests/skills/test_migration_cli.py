import csv
import tempfile
import unittest
from pathlib import Path

from skills.migration_cli import build_parser, main


class TestMigrationCli(unittest.TestCase):
    def test_main_writes_inventory_csv_for_migration_notes(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            review_tasks = root / "review-tasks"
            skills = root / "skills" / "concerns"
            review_tasks.mkdir(parents=True)
            skills.mkdir(parents=True)

            (review_tasks / "api-design").mkdir()
            (review_tasks / "api-design" / "input-validation.md").write_text(
                "\n".join(
                    [
                        "# Task: Input Validation",
                        "## Category",
                        "api-design",
                        "## Platforms",
                        "api, web",
                        "## Description",
                        "Missing validation on request payload.",
                    ]
                ),
                encoding="utf-8",
            )
            (skills / "api-design.md").write_text(
                "\n".join(
                    [
                        "# API Design Review",
                        "## Related Review Tasks",
                        "- `review-tasks/api-design/input-validation.md`",
                    ]
                ),
                encoding="utf-8",
            )

            output_path = root / "openspec" / "changes" / "research-changes" / "artifacts" / "map.csv"

            exit_code = main(
                [
                    "--review-tasks-dir",
                    str(review_tasks),
                    "--skills-dir",
                    str(root / "skills"),
                    "--output",
                    str(output_path),
                ]
            )

            with output_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))

        self.assertEqual(exit_code, 0)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["review_task"], "api-design/input-validation")
        self.assertEqual(rows[0]["skill"], "api-design")
        self.assertEqual(rows[0]["platform"], "api,web")

    def test_parser_defaults_to_repo_paths(self):
        args = build_parser().parse_args([])
        self.assertEqual(str(args.review_tasks_dir), "review-tasks")
        self.assertEqual(str(args.skills_dir), "skills")
        self.assertEqual(
            str(args.output),
            "openspec/changes/research-changes/artifacts/review-task-skill-map.csv",
        )


if __name__ == "__main__":
    unittest.main()

