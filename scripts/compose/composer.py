from pathlib import Path
from typing import Dict, Iterable, Set

import yaml

from compose.detector import detect_signals
from compose.merge import merge_managed_dependencies
from compose.selector import select_dependencies
from compose.validator import validate_manifest
from compose.versioning import apply_refs

_DEFAULT_STABLE_TAG = "v1.0.0"
_RUNTIME_SIGNALS = {
    "python",
    "typescript",
    "java",
    "go",
    "rust",
    "ruby",
    "php",
    "csharp",
    "kotlin",
    "swift",
}


def _build_compilation_defaults(detected_signals: Set[str]) -> Dict[str, str]:
    compilation = {"target": "all"}
    if len(detected_signals & _RUNTIME_SIGNALS) > 1:
        compilation["strategy"] = "distributed"
    return compilation


def _build_manifest_base(*, repo_root: Path, dependencies: Iterable[str]) -> Dict:
    return {
        "name": f"{repo_root.name}-review",
        "version": "1.0.0",
        "description": f"Auto-reviewer skills tailored for {repo_root.name}",
        "dependencies": {"apm": list(dependencies)},
    }


def compose_manifest(
    *,
    repo_root: Path,
    policy_path: Path,
    output_path: Path,
    ref_strategy: str = "tag",
    ref_value: str | None = None,
    update: bool = False,
) -> Dict:
    detected_signals = detect_signals(repo_root)
    selected_dependencies = select_dependencies(
        policy_path=policy_path,
        detected_signals=detected_signals,
    )
    effective_ref_value = ref_value
    if ref_strategy == "tag" and not effective_ref_value:
        effective_ref_value = _DEFAULT_STABLE_TAG
    pinned_dependencies = apply_refs(
        selected_dependencies,
        strategy=ref_strategy,
        ref_value=effective_ref_value,
    )

    if update:
        manifest = merge_managed_dependencies(
            manifest_path=output_path,
            managed_dependencies=pinned_dependencies,
        )
    else:
        manifest = _build_manifest_base(
            repo_root=repo_root,
            dependencies=pinned_dependencies,
        )

    manifest.setdefault("name", f"{repo_root.name}-review")
    manifest["compilation"] = _build_compilation_defaults(detected_signals)
    manifest["composer"] = {
        "detected_signals": sorted(detected_signals),
        "detection_confidence": "low" if not detected_signals else "high",
        "mode": "update" if update else "generate",
    }

    errors = validate_manifest(manifest, repo_root=repo_root)
    if errors:
        raise ValueError("\n".join(errors))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        yaml.safe_dump(manifest, sort_keys=False),
        encoding="utf-8",
    )
    return manifest
