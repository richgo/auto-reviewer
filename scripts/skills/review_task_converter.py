import re
import shutil
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

_TASK_HEADING = re.compile(r"^#\s*Task:\s*(.+?)\s*$")
_SECTION_HEADING = re.compile(r"^##\s+(.+?)\s*$")
_SKIP_FILENAMES = {"INDEX.md", "TEMPLATE.md"}
_DEFAULT_OUTPUT_LABEL = "skills/review-tasks"
_CANONICAL_RENAMES = {"data": "data-integrity"}


@dataclass(frozen=True)
class ReviewTask:
    relative_path: Path
    title: str
    category: str
    severity: str
    platforms: str
    languages: str
    description: str
    detection_heuristics: str
    eval_cases: str
    counter_examples: str
    binary_eval_assertions: str


def iter_review_task_files(review_tasks_dir: Path) -> List[Path]:
    return sorted(
        path
        for path in review_tasks_dir.rglob("*.md")
        if path.name not in _SKIP_FILENAMES
    )


def _split_sections(markdown: str) -> tuple[str, Dict[str, str]]:
    title = ""
    section_buffers: Dict[str, List[str]] = {}
    current_section = ""

    for line in markdown.splitlines():
        title_match = _TASK_HEADING.match(line)
        if title_match:
            title = title_match.group(1).strip()
            continue

        section_match = _SECTION_HEADING.match(line)
        if section_match:
            current_section = section_match.group(1).strip()
            section_buffers.setdefault(current_section, [])
            continue

        if current_section:
            section_buffers[current_section].append(line)

    sections = {
        key: "\n".join(value).strip()
        for key, value in section_buffers.items()
    }
    return title, sections


def parse_review_task_markdown(*, markdown: str, relative_path: Path) -> ReviewTask:
    title, sections = _split_sections(markdown)
    if not title:
        raise ValueError(f"Missing '# Task:' heading in {relative_path}")

    return ReviewTask(
        relative_path=relative_path,
        title=title,
        category=sections.get("Category", "").strip(),
        severity=sections.get("Severity", "").strip(),
        platforms=sections.get("Platforms", "").strip(),
        languages=sections.get("Languages", "").strip(),
        description=sections.get("Description", "").strip(),
        detection_heuristics=sections.get("Detection Heuristics", "").strip(),
        eval_cases=sections.get("Eval Cases", "").strip(),
        counter_examples=sections.get("Counter-Examples", "").strip(),
        binary_eval_assertions=sections.get("Binary Eval Assertions", "").strip(),
    )


def _sanitize_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def build_skill_name(relative_path: Path) -> str:
    slug_parts = [_sanitize_slug(part) for part in relative_path.with_suffix("").parts]
    return "review-task-" + "-".join(part for part in slug_parts if part)


def _truncate_words(text: str, *, limit: int) -> str:
    tokens = [token for token in text.split() if token]
    if len(tokens) <= limit:
        return " ".join(tokens)
    return " ".join(tokens[:limit]) + "..."


def build_skill_description(task: ReviewTask) -> str:
    category = task.category or "code review"
    platforms = task.platforms or "all platforms"
    languages = task.languages or "all languages"
    severity = task.severity or "appropriate"
    focus = _truncate_words(task.description or task.title, limit=18)
    return (
        f"Migrated review-task skill for {task.title}. Use this skill whenever diffs may introduce "
        f"{category} issues on {platforms}, especially in {languages}. Actively look for: {focus} "
        f"and report findings with {severity} severity expectations and actionable fixes."
    )


def _section_or_default(content: str, default_value: str) -> str:
    stripped = content.strip()
    return stripped if stripped else default_value


def render_task_skill(*, task: ReviewTask, output_label_path: str) -> str:
    skill_name = build_skill_name(task.relative_path)
    description = build_skill_description(task)
    wrapped_description = textwrap.fill(
        description,
        width=88,
        initial_indent="  ",
        subsequent_indent="  ",
    )

    source_path = f"review-tasks/{task.relative_path.as_posix()}"
    lines = [
        "---",
        f"name: {skill_name}",
        "description: >",
        wrapped_description,
        "---",
        "",
        f"# {task.title}",
        "",
        "## Source Lineage",
        f"- Original review task: `{source_path}`",
        f"- Migrated skill artifact: `{output_label_path}`",
        "",
        "## Task Metadata",
        f"- Category: `{task.category or 'unspecified'}`",
        f"- Severity: `{task.severity or 'unspecified'}`",
        f"- Platforms: `{task.platforms or 'unspecified'}`",
        f"- Languages: `{task.languages or 'unspecified'}`",
        "",
        "## Purpose",
        _section_or_default(task.description, "No task description provided."),
        "",
        "## Detection Heuristics",
        _section_or_default(
            task.detection_heuristics,
            "- No detection heuristics provided in source task.",
        ),
        "",
        "## Eval Cases",
        _section_or_default(
            task.eval_cases,
            "_No eval cases provided in source task._",
        ),
        "",
        "## Counter-Examples",
        _section_or_default(
            task.counter_examples,
            "_No counter-examples provided in source task._",
        ),
        "",
        "## Binary Eval Assertions",
        _section_or_default(
            task.binary_eval_assertions,
            "_No binary assertions provided in source task._",
        ),
        "",
        "## Migration Notes",
        "- This skill is generated from the legacy review-task corpus for one-to-one lineage.",
        "- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`",
        "  whenever review-task source files change.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def convert_all_review_tasks(
    *,
    review_tasks_dir: Path,
    output_dir: Path,
    output_label: str = _DEFAULT_OUTPUT_LABEL,
    clean: bool = False,
) -> List[Path]:
    task_files = iter_review_task_files(review_tasks_dir)
    if clean and output_dir.exists():
        shutil.rmtree(output_dir)

    converted_paths: List[Path] = []
    output_label_root = output_label.rstrip("/")

    for task_path in task_files:
        relative_path = task_path.relative_to(review_tasks_dir)
        task = parse_review_task_markdown(
            markdown=task_path.read_text(encoding="utf-8"),
            relative_path=relative_path,
        )
        output_path = output_dir / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_label_path = f"{output_label_root}/{relative_path.as_posix()}"
        rendered = render_task_skill(task=task, output_label_path=output_label_path)
        output_path.write_text(rendered, encoding="utf-8")
        converted_paths.append(output_path)

    return converted_paths


def _flatten_path_to_skill_name(path: Path) -> str:
    flat = "-".join(path.parts)
    return _canonical_skill_name(flat)


def _canonical_skill_name(flat_name: str) -> str:
    return _CANONICAL_RENAMES.get(flat_name, flat_name)


def _extract_front_matter_name(markdown: str) -> Optional[str]:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip()
    return None


def _rewrite_front_matter_name(markdown: str, *, canonical_name: str) -> str:
    lines = markdown.splitlines()
    if lines and lines[0].strip() == "---":
        for idx in range(1, len(lines)):
            if lines[idx].startswith("name:"):
                lines[idx] = f"name: {canonical_name}"
                return "\n".join(lines).rstrip() + "\n"
            if lines[idx].strip() == "---":
                break
    return f"---\nname: {canonical_name}\n---\n\n{markdown.rstrip()}\n"


def _strip_front_matter(markdown: str) -> str:
    if _extract_front_matter_name(markdown) is None:
        return markdown.strip()
    return re.sub(r"^---\n.*?\n---\n?", "", markdown, flags=re.DOTALL).strip()


def flatten_review_task_skills(*, skills_dir: Path) -> List[Path]:
    grouped_sources: Dict[str, List[Path]] = {}
    created_paths: List[Path] = []
    all_sources: List[Path] = []

    for concern_file in sorted((skills_dir / "concerns").glob("*.md")):
        grouped_sources.setdefault(concern_file.stem, []).append(concern_file)
        all_sources.append(concern_file)

    review_tasks_root = skills_dir / "review-tasks"
    for folder in sorted(path for path in review_tasks_root.rglob("*") if path.is_dir()):
        if any(child.is_file() and child.suffix == ".md" for child in folder.iterdir()):
            canonical_name = _flatten_path_to_skill_name(folder.relative_to(review_tasks_root))
            for markdown_file in sorted(folder.glob("*.md")):
                grouped_sources.setdefault(canonical_name, []).append(markdown_file)
                all_sources.append(markdown_file)

    for canonical_name, source_paths in sorted(grouped_sources.items()):
        target_dir = skills_dir / canonical_name
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / "SKILL.md"

        merged_bodies: List[str] = []
        first_source = source_paths[0]
        first_content = first_source.read_text(encoding="utf-8")
        merged_bodies.append(_rewrite_front_matter_name(first_content, canonical_name=canonical_name))

        for extra_source in source_paths[1:]:
            content = extra_source.read_text(encoding="utf-8")
            merged_bodies.append(_strip_front_matter(content))

        target_path.write_text("\n\n".join(part.rstrip() for part in merged_bodies).rstrip() + "\n", encoding="utf-8")
        created_paths.append(target_path)

    for source in _unique_paths(sorted(all_sources)):
        if source.exists():
            source.unlink()

    return created_paths


def _unique_paths(paths: List[Path]) -> List[Path]:
    unique: List[Path] = []
    seen = set()
    for path in paths:
        key = path.as_posix()
        if key in seen:
            continue
        seen.add(key)
        unique.append(path)
    return unique
