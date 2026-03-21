from pathlib import Path
from typing import Dict, List


def validate_manifest(manifest: Dict, *, repo_root: Path) -> List[str]:
    errors: List[str] = []
    if not manifest.get("name"):
        errors.append("Manifest must include name")
    dependencies = manifest.get("dependencies", {})
    if not isinstance(dependencies, dict):
        errors.append("Manifest dependencies must be a mapping")
        return errors
    apm_dependencies = dependencies.get("apm", [])
    if not isinstance(apm_dependencies, list):
        errors.append("Manifest dependencies.apm must be a list")
        return errors
    for dependency in apm_dependencies:
        if not isinstance(dependency, str):
            errors.append(f"Dependency entries must be a string: {dependency!r}")
            continue
        dep_path, _, _ref = dependency.partition("#")
        if "#" in dependency and not _ref.strip():
            errors.append(f"Invalid ref format for dependency: {dependency}")
        if dep_path.startswith("richgo/auto-reviewer/skills/"):
            relative = dep_path.replace("richgo/auto-reviewer/", "", 1)
            if not (repo_root / relative).with_suffix(".md").exists():
                errors.append(f"Unknown skill path: {dep_path}")
    return errors
