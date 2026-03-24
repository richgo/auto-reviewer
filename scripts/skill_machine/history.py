import json
from pathlib import Path
from typing import Any, Dict, List


def append_history(*, history_file: Path, row: Dict[str, Any]) -> None:
    history_file.parent.mkdir(parents=True, exist_ok=True)
    with history_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + "\n")


def read_history(*, history_file: Path) -> List[Dict[str, Any]]:
    if not history_file.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for line in history_file.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
    return rows
