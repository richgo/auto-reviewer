from pathlib import Path
from typing import Set


def detect_signals(repo_root: Path) -> Set[str]:
    detected: Set[str] = set()
    if (repo_root / "requirements.txt").exists() or list(repo_root.rglob("*.py")):
        detected.add("python")
    if (repo_root / "package.json").exists() or list(repo_root.rglob("package.json")):
        if list(repo_root.rglob("*.ts")) or list(repo_root.rglob("*.tsx")):
            detected.add("typescript")
    if (repo_root / ".github" / "workflows").exists():
        detected.add("ci_github_actions")
    return detected
