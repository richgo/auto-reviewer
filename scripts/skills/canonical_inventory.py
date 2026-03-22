from pathlib import Path
from typing import Dict, List


def _flatten_review_task_folder(path: Path) -> str:
    parts = list(path.parts)
    return "-".join(parts[1:])


def build_canonical_skill_inventory(*, skills_dir: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    concerns_dir = skills_dir / "concerns"
    for skill_file in sorted(concerns_dir.glob("*.md")):
        rows.append(
            {
                "canonical_skill": skill_file.stem,
                "source_kind": "legacy-file",
                "source_path": f"skills/concerns/{skill_file.name}",
            }
        )

    review_tasks_dir = skills_dir / "review-tasks"
    for folder in sorted(path for path in review_tasks_dir.rglob("*") if path.is_dir()):
        if any(child.is_file() and child.suffix == ".md" for child in folder.iterdir()):
            rows.append(
                {
                    "canonical_skill": _flatten_review_task_folder(
                        folder.relative_to(skills_dir)
                    ),
                    "source_kind": "review-task-folder",
                    "source_path": f"skills/{folder.relative_to(skills_dir).as_posix()}",
                }
            )

    return rows
