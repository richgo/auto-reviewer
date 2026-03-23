import argparse
from pathlib import Path
from typing import Sequence

from skills.review_task_converter import convert_all_review_tasks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert review-tasks corpus into per-task migrated skill artifacts."
    )
    parser.add_argument(
        "--review-tasks-dir",
        type=Path,
        default=Path("review-tasks"),
        help="Source review-tasks directory",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("skills/review-tasks"),
        help="Destination directory for generated per-task skills",
    )
    parser.add_argument(
        "--output-label",
        default="skills/review-tasks",
        help="Path label stored inside generated SKILL markdown lineage",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove output directory before generating new files",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    convert_all_review_tasks(
        review_tasks_dir=args.review_tasks_dir,
        output_dir=args.output_dir,
        output_label=args.output_label,
        clean=args.clean,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

