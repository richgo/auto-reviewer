import csv
import re
from pathlib import Path
from typing import Dict, List, Set


_CSV_FIELDS = ["review_task", "category", "platform", "skill", "skill_path", "owasp_refs"]
_TASK_HEADER = re.compile(r"^#\s*Task:\s*(.+?)\s*$", re.MULTILINE)
_CATEGORY_HEADER = re.compile(r"^##\s*Category\s*$", re.MULTILINE)
_PLATFORMS_HEADER = re.compile(r"^##\s*Platforms\s*$", re.MULTILINE)
_OWASP_TAG = re.compile(r"\[OWASP:\s*([^\]]+)\]")
_REFERENCE_PATH = re.compile(r"`review-tasks/([^`]+)\.md`")

_CATEGORY_TO_SKILL = {
    "api-design": "api-design",
    "code-quality": "code-quality",
    "concurrency": "concurrency",
    "correctness": "correctness",
    "data": "data-integrity",
    "observability": "observability",
    "performance": "performance",
    "reliability": "reliability",
    "testing": "testing",
}

_SECURITY_SUBCATEGORY_TO_SKILL = {
    "android": "security-mobile-android",
    "ai-agent-security": "security-ai-llm",
    "auth-bypass": "security-auth",
    "authentication-flaws": "security-auth",
    "cicd-security": "security-infrastructure",
    "clickjacking": "security-client-side",
    "cookie-security": "security-client-side",
    "cors-misconfiguration": "security-network",
    "credential-stuffing": "security-auth",
    "csrf": "security-auth",
    "dependency-vulnerability": "security-supply-chain",
    "denial-of-service": "security-network",
    "docker-misconfiguration": "security-infrastructure",
    "dom-xss": "security-injection",
    "file-upload": "security-data-protection",
    "graphql-security": "security-api",
    "infrastructure": "security-infrastructure",
    "insecure-crypto": "security-data-protection",
    "insecure-deserialization": "security-data-protection",
    "insufficient-transport-security": "security-network",
    "ios": "security-mobile-ios",
    "iac-security": "security-infrastructure",
    "ldap-injection": "security-injection",
    "mass-assignment": "security-data-protection",
    "mcp-tool-poisoning": "security-ai-llm",
    "microservices": "security-infrastructure",
    "missing-security-headers": "security-network",
    "mobile": "security-mobile",
    "multi-tenant-isolation": "security-infrastructure",
    "nosql-injection": "security-injection",
    "oauth-misconfiguration": "security-auth",
    "open-redirect": "security-network",
    "path-traversal": "security-data-protection",
    "password-reset-flaws": "security-auth",
    "password-storage": "security-auth",
    "pinning-bypass": "security-supply-chain",
    "prompt-injection": "security-ai-llm",
    "prototype-pollution": "security-client-side",
    "regex-dos": "security-network",
    "rest-security": "security-api",
    "secrets-exposure": "security-data-protection",
    "security-error-info-leak": "security-auth",
    "security-logging": "security-infrastructure",
    "serverless-security": "security-infrastructure",
    "session-management": "security-auth",
    "sql-injection": "security-injection",
    "ssrf": "security-network",
    "third-party-code": "security-client-side",
    "transaction-authorization": "security-api",
    "web": "security-client-side",
    "xml-external-entity": "security-supply-chain",
    "xss": "security-client-side",
}


def _read_section_value(markdown: str, heading_pattern: re.Pattern[str]) -> str:
    match = heading_pattern.search(markdown)
    if not match:
        return ""
    start = match.end()
    lines = markdown[start:].splitlines()
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("## "):
            return ""
        return stripped
    return ""


def _parse_owasp_refs(markdown: str) -> List[str]:
    refs: List[str] = []
    for raw_group in _OWASP_TAG.findall(markdown):
        for token in raw_group.split(","):
            cleaned = token.strip()
            if cleaned and cleaned not in refs:
                refs.append(cleaned)
    return refs


def _split_task_path(task_relative_path: Path) -> Dict[str, str]:
    parts = task_relative_path.parts
    if len(parts) < 2:
        raise ValueError(f"Unexpected review-task path: {task_relative_path}")
    category = parts[0]
    subcategory = parts[1] if len(parts) > 2 else ""
    return {"category": category, "subcategory": subcategory, "slug": task_relative_path.stem}


def _category_fallback_skill(category: str) -> str:
    if category == "security":
        return "security-infrastructure"
    if category not in _CATEGORY_TO_SKILL:
        raise ValueError(f"No skill mapping configured for category '{category}'")
    return _CATEGORY_TO_SKILL[category]


def _select_skill_from_related_links(
    task_relative_path: Path, related_task_to_skill: Dict[str, str]
) -> str | None:
    key = task_relative_path.as_posix()
    return related_task_to_skill.get(key)


def _select_skill_from_security_mapping(task_relative_path: Path) -> str | None:
    split = _split_task_path(task_relative_path)
    if split["category"] != "security":
        return None
    if split["subcategory"] in {"android", "ios", "mobile", "web", "microservices"}:
        return _SECURITY_SUBCATEGORY_TO_SKILL.get(split["subcategory"])
    return _SECURITY_SUBCATEGORY_TO_SKILL.get(split["slug"])


def _resolve_skill_name(
    task_relative_path: Path, related_task_to_skill: Dict[str, str]
) -> str:
    related_match = _select_skill_from_related_links(task_relative_path, related_task_to_skill)
    if related_match:
        return related_match
    security_match = _select_skill_from_security_mapping(task_relative_path)
    if security_match:
        return security_match
    split = _split_task_path(task_relative_path)
    return _category_fallback_skill(split["category"])


def _canonical_skill_path(skill_name: str) -> str:
    return f"skills/{skill_name}/SKILL.md"


def _collect_related_task_mappings(skills_dir: Path) -> Dict[str, str]:
    mappings: Dict[str, str] = {}
    if not skills_dir.exists():
        return mappings

    for skill_path in sorted(skills_dir.glob("*/SKILL.md")):
        skill_name = skill_path.parent.name
        content = skill_path.read_text(encoding="utf-8")
        seen_for_skill: Set[str] = set()
        for relative_path in _REFERENCE_PATH.findall(content):
            rel = f"{relative_path}.md"
            if rel in seen_for_skill:
                continue
            seen_for_skill.add(rel)
            if rel not in mappings:
                mappings[rel] = skill_name
    return mappings


def build_review_task_skill_rows(*, review_tasks_dir: Path, skills_dir: Path) -> List[Dict[str, str]]:
    related_task_to_skill = _collect_related_task_mappings(skills_dir)
    rows: List[Dict[str, str]] = []

    for task_path in sorted(review_tasks_dir.rglob("*.md")):
        if task_path.name in {"INDEX.md", "TEMPLATE.md"}:
            continue
        content = task_path.read_text(encoding="utf-8")
        relative_task = task_path.relative_to(review_tasks_dir)
        split = _split_task_path(relative_task)

        platforms = _read_section_value(content, _PLATFORMS_HEADER).replace(" ", "")
        category_value = _read_section_value(content, _CATEGORY_HEADER) or split["category"]
        if not _TASK_HEADER.search(content):
            raise ValueError(f"Missing task heading in {relative_task}")
        owasp_refs = _parse_owasp_refs(content)

        skill_name = _resolve_skill_name(relative_task, related_task_to_skill)
        rows.append(
            {
                "review_task": relative_task.with_suffix("").as_posix(),
                "category": category_value,
                "platform": platforms,
                "skill": skill_name,
                "skill_path": _canonical_skill_path(skill_name),
                "owasp_refs": "|".join(owasp_refs),
            }
        )

    return rows


def write_migration_inventory(*, rows: List[Dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=_CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
