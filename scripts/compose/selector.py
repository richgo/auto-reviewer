from pathlib import Path
from typing import List, Set

import yaml


def select_dependencies(*, policy_path: Path, detected_signals: Set[str]) -> List[str]:
    policy = yaml.safe_load(policy_path.read_text(encoding="utf-8")) or {}
    selected = set(policy.get("core", []))
    signal_map = policy.get("signals", {})
    for signal in detected_signals:
        selected.update(signal_map.get(signal, {}).get("dependencies", []))
    if not detected_signals:
        selected.update(policy.get("fallback", []))
    return sorted(selected)
