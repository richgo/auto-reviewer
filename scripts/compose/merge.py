from pathlib import Path
from typing import Dict, List

import yaml


def merge_managed_dependencies(*, manifest_path: Path, managed_dependencies: List[str]) -> Dict:
    payload = {}
    if manifest_path.exists():
        payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    payload.setdefault("dependencies", {})
    current_apm = payload["dependencies"].get("apm", [])
    unmanaged = [dep for dep in current_apm if not dep.startswith("richgo/skill-machine/skills/")]
    payload["dependencies"]["apm"] = unmanaged + sorted(managed_dependencies)
    return payload
