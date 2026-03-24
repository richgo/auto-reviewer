"""Needs-review tracker for skills that fail cascade tuning.

Maintains a markdown checklist of skills that failed to reach 95% pass rate
during cascade tuning and require manual review.
"""

from pathlib import Path
from typing import Dict, List, Optional


class NeedsReviewTracker:
    """Tracks skills that need manual review after failed cascade."""

    def __init__(self, review_file: Path):
        """Initialize tracker with review file path.

        Args:
            review_file: Path to skills-tools/needs-review.md
        """
        self.review_file = Path(review_file)
        self.skills: Dict[str, dict] = {}
        self._load()

    def _load(self):
        """Load existing needs-review.md if it exists."""
        if self.review_file.exists():
            # Parse existing entries from file
            content = self.review_file.read_text(encoding="utf-8")
            # Extract skills from markdown (e.g., "- [ ] **security-injection** — ...")
            for line in content.split('\n'):
                if line.startswith("- [ ] **"):
                    # Parse: "- [ ] **skill-name** — model @ XX% ([History](link))"
                    parts = line.split(" — ")
                    if len(parts) >= 2:
                        skill_name = line.split("**")[1]
                        # Extract model and pass rate from "model @ XX%"
                        rest = parts[1]
                        model_parts = rest.split(" @ ")
                        if len(model_parts) >= 2:
                            model = model_parts[0]
                            pass_rate_str = model_parts[1].split("%")[0]
                            try:
                                pass_rate = int(pass_rate_str) / 100.0
                                # Extract history link
                                history_link = rest.split("(")[1].split(")")[0] if "(" in rest else ""
                                self.skills[skill_name] = {
                                    "best_model": model,
                                    "best_pass_rate": pass_rate,
                                    "history_link": history_link,
                                }
                            except (ValueError, IndexError):
                                pass
        else:
            self.skills = {}

    def add(
        self,
        skill_name: str,
        best_model: str,
        best_pass_rate: float,
        history_link: str,
    ):
        """Add or update a skill in the needs-review list.

        Args:
            skill_name: Name of the skill (e.g., "security-injection").
            best_model: Model that achieved best result.
            best_pass_rate: Best pass rate achieved (0.0-1.0).
            history_link: Path to tuning history file.
        """
        # Reload to get any changes made by other processes
        self._load()
        
        self.skills[skill_name] = {
            "best_model": best_model,
            "best_pass_rate": best_pass_rate,
            "history_link": history_link,
        }
        self._write()

    def _write(self):
        """Write skills to needs-review.md in markdown checklist format."""
        lines = [
            "# Skills Needing Manual Review\n",
            "> Skills that failed to reach 95% pass rate through automatic tuning cascade.\n",
            "> Sorted alphabetically. Check off items as they are resolved.\n",
            "\n",
        ]

        # Sort skills alphabetically
        for skill_name in sorted(self.skills.keys()):
            entry = self.skills[skill_name]
            lines.append(
                f"- [ ] **{skill_name}** — "
                f"{entry['best_model']} @ {entry['best_pass_rate']:.0%} "
                f"([History]({entry['history_link']}))\n"
            )

        self.review_file.parent.mkdir(parents=True, exist_ok=True)
        self.review_file.write_text("".join(lines), encoding="utf-8")

    def get_all(self) -> List[str]:
        """Return list of all skills needing review.

        Returns:
            Sorted list of skill names.
        """
        return sorted(self.skills.keys())

    def is_skill_reviewed(self, skill_name: str) -> bool:
        """Check if a skill is in the needs-review list.

        Args:
            skill_name: Name of the skill.

        Returns:
            True if skill is in needs-review, False otherwise.
        """
        return skill_name in self.skills
