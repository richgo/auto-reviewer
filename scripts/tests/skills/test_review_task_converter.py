import tempfile
import unittest
from pathlib import Path

from skills.review_task_converter import (
    build_skill_name,
    flatten_review_task_skills,
    convert_all_review_tasks,
    parse_review_task_markdown,
    render_task_skill,
)


class TestReviewTaskConverter(unittest.TestCase):
    def test_parse_review_task_markdown_extracts_sections(self):
        payload = "\n".join(
            [
                "# Task: SQL Injection",
                "",
                "## Category",
                "security",
                "",
                "## Severity",
                "critical",
                "",
                "## Platforms",
                "web, api",
                "",
                "## Languages",
                "all",
                "",
                "## Description",
                "User input flows into SQL queries.",
                "",
                "## Detection Heuristics",
                "- f-strings in SQL",
                "",
                "## Eval Cases",
                "### Case 1",
                "```python",
                "query = f\"SELECT * FROM users WHERE id = {uid}\"",
                "```",
                "",
                "## Counter-Examples",
                "### Counter 1",
                "```python",
                "cursor.execute(\"SELECT * FROM users WHERE id = %s\", (uid,))",
                "```",
                "",
                "## Binary Eval Assertions",
                "- [ ] Detects SQL injection",
            ]
        )

        parsed = parse_review_task_markdown(
            markdown=payload,
            relative_path=Path("security/sql-injection.md"),
        )

        self.assertEqual(parsed.title, "SQL Injection")
        self.assertEqual(parsed.category, "security")
        self.assertEqual(parsed.severity, "critical")
        self.assertEqual(parsed.platforms, "web, api")
        self.assertEqual(parsed.languages, "all")
        self.assertIn("f-strings in SQL", parsed.detection_heuristics)
        self.assertIn("### Case 1", parsed.eval_cases)
        self.assertIn("### Counter 1", parsed.counter_examples)
        self.assertIn("Detects SQL injection", parsed.binary_eval_assertions)

    def test_render_task_skill_uses_skill_frontmatter_and_lineage(self):
        parsed = parse_review_task_markdown(
            markdown="\n".join(
                [
                    "# Task: Open Redirect",
                    "## Category",
                    "security",
                    "## Severity",
                    "medium",
                    "## Platforms",
                    "web, api",
                    "## Languages",
                    "all",
                    "## Description",
                    "Unvalidated redirect targets.",
                    "## Detection Heuristics",
                    "- redirect() from user input",
                    "## Eval Cases",
                    "### Case 1",
                    "```python",
                    "return redirect(request.args['next'])",
                    "```",
                    "## Counter-Examples",
                    "### Counter 1",
                    "```python",
                    "if next_url in ALLOWED: return redirect(next_url)",
                    "```",
                    "## Binary Eval Assertions",
                    "- [ ] Detects issue",
                ]
            ),
            relative_path=Path("security/open-redirect.md"),
        )
        rendered = render_task_skill(
            task=parsed,
            output_label_path="skills/review-tasks/security/open-redirect.md",
        )

        self.assertIn("---\nname: review-task-security-open-redirect", rendered)
        self.assertIn("description: >", rendered)
        self.assertIn("Original review task: `review-tasks/security/open-redirect.md`", rendered)
        self.assertIn("Migrated skill artifact: `skills/review-tasks/security/open-redirect.md`", rendered)
        self.assertIn("## Detection Heuristics", rendered)
        self.assertIn("## Eval Cases", rendered)
        self.assertIn("## Counter-Examples", rendered)
        self.assertIn("## Binary Eval Assertions", rendered)

    def test_convert_all_review_tasks_generates_one_output_per_task(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            review_tasks = root / "review-tasks"
            output_dir = root / "skills" / "review-tasks"
            (review_tasks / "security").mkdir(parents=True)
            (review_tasks / "api-design" / "mobile").mkdir(parents=True)

            (review_tasks / "security" / "sql-injection.md").write_text(
                "\n".join(
                    [
                        "# Task: SQL Injection",
                        "## Category",
                        "security",
                        "## Severity",
                        "critical",
                        "## Platforms",
                        "web, api",
                        "## Languages",
                        "all",
                        "## Description",
                        "SQL injection bug class.",
                        "## Detection Heuristics",
                        "- string interpolation in SQL",
                        "## Eval Cases",
                        "### Case 1",
                        "```python",
                        "query = f\"...\"",
                        "```",
                        "## Counter-Examples",
                        "### Counter 1",
                        "```python",
                        "cursor.execute(\"...\", (...,))",
                        "```",
                        "## Binary Eval Assertions",
                        "- [ ] Detects SQL injection",
                    ]
                ),
                encoding="utf-8",
            )
            (review_tasks / "api-design" / "mobile" / "offline-sync.md").write_text(
                "\n".join(
                    [
                        "# Task: Offline Sync Strategy",
                        "## Category",
                        "api-design",
                        "## Severity",
                        "medium",
                        "## Platforms",
                        "mobile",
                        "## Languages",
                        "all",
                        "## Description",
                        "Offline sync conflict handling gaps.",
                        "## Detection Heuristics",
                        "- missing version vectors",
                        "## Eval Cases",
                        "### Case 1",
                        "```kotlin",
                        "// BUGGY",
                        "```",
                        "## Counter-Examples",
                        "### Counter 1",
                        "```kotlin",
                        "// SAFE",
                        "```",
                        "## Binary Eval Assertions",
                        "- [ ] Detects missing conflict handling",
                    ]
                ),
                encoding="utf-8",
            )

            converted = convert_all_review_tasks(
                review_tasks_dir=review_tasks,
                output_dir=output_dir,
                clean=True,
            )

            self.assertEqual(len(converted), 2)
            self.assertTrue((output_dir / "security" / "sql-injection.md").exists())
            self.assertTrue((output_dir / "api-design" / "mobile" / "offline-sync.md").exists())

            sql_skill = (output_dir / "security" / "sql-injection.md").read_text(encoding="utf-8")
            self.assertIn("name: review-task-security-sql-injection", sql_skill)
            self.assertIn("Original review task: `review-tasks/security/sql-injection.md`", sql_skill)

    def test_build_skill_name_is_deterministic(self):
        self.assertEqual(
            build_skill_name(Path("security/mobile/cert-pinning.md")),
            "review-task-security-mobile-cert-pinning",
        )

    def test_flatten_review_task_skills_merges_collisions_into_single_skill_folder(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            (skills_dir / "concerns").mkdir(parents=True)
            (skills_dir / "review-tasks" / "api-design").mkdir(parents=True)

            (skills_dir / "concerns" / "api-design.md").write_text(
                "---\nname: api-design\ndescription: concern\n---\n\n# Concern\n",
                encoding="utf-8",
            )
            (skills_dir / "review-tasks" / "api-design" / "input-validation.md").write_text(
                "---\nname: review-task-api-design-input-validation\ndescription: task\n---\n\n# Task\n",
                encoding="utf-8",
            )

            created = flatten_review_task_skills(skills_dir=skills_dir)

            canonical_path = skills_dir / "api-design" / "SKILL.md"
            self.assertEqual(created, [canonical_path])
            self.assertTrue(canonical_path.exists())
            content = canonical_path.read_text(encoding="utf-8")
            self.assertIn("name: api-design", content)
            self.assertIn("# Concern", content)
            self.assertIn("# Task", content)

    def test_flatten_review_task_skills_retires_competing_legacy_definitions(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            (skills_dir / "concerns").mkdir(parents=True)
            (skills_dir / "review-tasks" / "api-design").mkdir(parents=True)
            (skills_dir / "concerns" / "api-design.md").write_text(
                "---\nname: api-design\ndescription: concern\n---\n\n# Concern\n",
                encoding="utf-8",
            )
            (
                skills_dir / "review-tasks" / "api-design" / "input-validation.md"
            ).write_text(
                "---\nname: review-task-api-design-input-validation\ndescription: task\n---\n\n# Task\n",
                encoding="utf-8",
            )

            flatten_review_task_skills(skills_dir=skills_dir)

            self.assertFalse((skills_dir / "concerns" / "api-design.md").exists())
            self.assertFalse(
                (skills_dir / "review-tasks" / "api-design" / "input-validation.md").exists()
            )
            self.assertTrue((skills_dir / "api-design" / "SKILL.md").exists())

    def test_flatten_review_task_skills_maps_data_folder_to_data_integrity(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            (skills_dir / "review-tasks" / "data").mkdir(parents=True)
            (skills_dir / "review-tasks" / "data" / "schema-validation.md").write_text(
                "---\nname: review-task-data-schema-validation\ndescription: task\n---\n\n# Task\n",
                encoding="utf-8",
            )

            flatten_review_task_skills(skills_dir=skills_dir)

            self.assertTrue((skills_dir / "data-integrity" / "SKILL.md").exists())
            self.assertFalse((skills_dir / "data" / "SKILL.md").exists())

    def test_flatten_review_task_skills_surfaces_manual_fix_for_non_mergeable_front_matter_name_conflict(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            (skills_dir / "concerns").mkdir(parents=True)
            (skills_dir / "review-tasks" / "api-design").mkdir(parents=True)

            (skills_dir / "concerns" / "api-design.md").write_text(
                "---\nname: api-design\ndescription: concern\n---\n\n# Concern\n",
                encoding="utf-8",
            )
            (skills_dir / "review-tasks" / "api-design" / "input-validation.md").write_text(
                "---\nname: api-design-alt\ndescription: task\n---\n\n# Task\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "manual-fix error.*api-design"):
                flatten_review_task_skills(skills_dir=skills_dir)

    def test_flatten_review_task_skills_surfaces_manual_fix_for_non_mergeable_title_conflict(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            (skills_dir / "concerns").mkdir(parents=True)
            (skills_dir / "review-tasks" / "api-design").mkdir(parents=True)

            (skills_dir / "concerns" / "api-design.md").write_text(
                "---\nname: api-design\ndescription: concern\n---\n\n# Concern\n",
                encoding="utf-8",
            )
            (skills_dir / "review-tasks" / "api-design" / "input-validation.md").write_text(
                "---\nname: api-design\ndescription: task\n---\n\n# Task\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "manual-fix error.*api-design"):
                flatten_review_task_skills(skills_dir=skills_dir)

    def test_flatten_review_task_skills_reports_all_manual_conflicts_before_exiting(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            skills_dir = root / "skills"
            (skills_dir / "concerns").mkdir(parents=True)
            (skills_dir / "review-tasks" / "api-design").mkdir(parents=True)
            (skills_dir / "review-tasks" / "code-quality").mkdir(parents=True)

            (skills_dir / "concerns" / "api-design.md").write_text(
                "---\nname: api-design\ndescription: concern\n---\n\n# Concern\n",
                encoding="utf-8",
            )
            (skills_dir / "review-tasks" / "api-design" / "input-validation.md").write_text(
                "---\nname: api-design-alt\ndescription: task\n---\n\n# Task\n",
                encoding="utf-8",
            )
            (skills_dir / "concerns" / "code-quality.md").write_text(
                "---\nname: code-quality\ndescription: concern\n---\n\n# Quality\n",
                encoding="utf-8",
            )
            (skills_dir / "review-tasks" / "code-quality" / "naming.md").write_text(
                "---\nname: code-quality\ndescription: task\n---\n\n# Naming\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError,
                "(?s)manual-fix error.*api-design.*manual-fix error.*code-quality",
            ):
                flatten_review_task_skills(skills_dir=skills_dir)



if __name__ == "__main__":
    unittest.main()
