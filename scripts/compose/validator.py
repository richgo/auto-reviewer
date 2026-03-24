from pathlib import Path
from typing import Dict, List


_AUTO_REVIEWER_SKILLS_PREFIX = "richgo/skill-machine/skills/"


def _resolve_skill_dependency_error(*, dep_path: str, repo_root: Path) -> str | None:
    if dep_path.endswith(".md"):
        return f"Legacy skill path alias not allowed: {dep_path}"
    relative = dep_path.replace("richgo/skill-machine/", "", 1)
    canonical_entry = repo_root / relative / "SKILL.md"
    if not canonical_entry.exists():
        return f"Unknown skill path: {dep_path}"
    return None


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
        if dep_path.startswith(_AUTO_REVIEWER_SKILLS_PREFIX):
            dep_error = _resolve_skill_dependency_error(dep_path=dep_path, repo_root=repo_root)
            if dep_error:
                errors.append(dep_error)
    return errors
