from pathlib import Path
from typing import Dict, List


def validate_manifest(manifest: Dict, *, repo_root: Path) -> List[str]:
    errors: List[str] = []
    if not manifest.get("name"):
        errors.append("Manifest must include name")
    for dependency in manifest.get("dependencies", {}).get("apm", []):
        dep_path, _, _ref = dependency.partition("#")
        if "#" in dependency and not _ref.strip():
            errors.append(f"Invalid ref format for dependency: {dependency}")
        if dep_path.startswith("richgo/auto-reviewer/skills/"):
            relative = dep_path.replace("richgo/auto-reviewer/", "", 1)
            if not (repo_root / relative).with_suffix(".md").exists():
                errors.append(f"Unknown skill path: {dep_path}")
    return errors
