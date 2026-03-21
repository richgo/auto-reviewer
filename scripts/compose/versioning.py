from typing import Iterable, List


def apply_refs(dependencies: Iterable[str], *, strategy: str, ref_value: str | None) -> List[str]:
    if strategy not in {"tag", "sha", "branch", "none"}:
        raise ValueError(f"Unsupported ref strategy: {strategy}")
    if strategy == "none":
        return list(dependencies)
    if not ref_value:
        raise ValueError("ref_value is required unless strategy is 'none'")
    return [f"{dependency}#{ref_value}" for dependency in dependencies]
