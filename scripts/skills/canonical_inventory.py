from pathlib import Path
from typing import Dict, List


def build_canonical_skill_inventory(*, skills_dir: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for skill_file in sorted(skills_dir.glob("*/SKILL.md")):
        rows.append(
            {
                "canonical_skill": skill_file.parent.name,
                "source_kind": "canonical-folder",
                "source_path": f"skills/{skill_file.parent.name}/SKILL.md",
            }
        )
    return rows


def validate_canonical_folder_contract(*, skills_dir: Path) -> List[str]:
    errors: List[str] = []
    for markdown_path in sorted(skills_dir.rglob("*.md")):
        relative = markdown_path.relative_to(skills_dir)
        if len(relative.parts) != 2:
            errors.append(
                f"Skill entry must be skills/<skill>/SKILL.md: skills/{relative.as_posix()}"
            )
            continue
        if relative.name != "SKILL.md":
            errors.append(
                f"Skill entry must be named SKILL.md: skills/{relative.as_posix()}"
            )
    return errors
