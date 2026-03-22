import argparse
from pathlib import Path
from typing import Sequence

from skills.migration_map import build_review_task_skill_rows, write_migration_inventory


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build deterministic review-task to skill migration inventory."
    )
    parser.add_argument(
        "--review-tasks-dir",
        type=Path,
        default=Path("review-tasks"),
        help="Source review-tasks directory",
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=Path("skills"),
        help="Skills root directory",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("openspec/changes/research-changes/artifacts/review-task-skill-map.csv"),
        help="Destination CSV path",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = build_review_task_skill_rows(
        review_tasks_dir=args.review_tasks_dir, skills_dir=args.skills_dir
    )
    write_migration_inventory(rows=rows, output_path=args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

