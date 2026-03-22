from pathlib import Path
from typing import Dict, List


_LEGACY_GROUPS = ("concerns", "core", "languages", "outputs", "tuning")


def _flatten_review_task_folder(path: Path) -> str:
    parts = list(path.parts)
    return "-".join(parts[1:])


def _iter_canonical_folder_entries(*, group_dir: Path):
    return sorted(group_dir.glob("*/SKILL.md"))


def _iter_legacy_skill_files(*, group_dir: Path):
    return sorted(group_dir.glob("*.md"))


def build_canonical_skill_inventory(*, skills_dir: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    for group in _LEGACY_GROUPS:
        group_dir = skills_dir / group
        for skill_file in _iter_canonical_folder_entries(group_dir=group_dir):
            rows.append(
                {
                    "canonical_skill": skill_file.parent.name,
                    "source_kind": "canonical-folder",
                    "source_path": f"skills/{group}/{skill_file.parent.name}/SKILL.md",
                }
            )
        for skill_file in _iter_legacy_skill_files(group_dir=group_dir):
            rows.append(
                {
                    "canonical_skill": skill_file.stem,
                    "source_kind": "legacy-file",
                    "source_path": f"skills/{group}/{skill_file.name}",
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


def validate_canonical_folder_contract(*, skills_dir: Path) -> List[str]:
    errors: List[str] = []
    for group in _LEGACY_GROUPS:
        group_dir = skills_dir / group
        for skill_file in _iter_legacy_skill_files(group_dir=group_dir):
            errors.append(
                f"Legacy skill file requires canonical folder: skills/{group}/{skill_file.name}"
            )
    return errors
