# Phase 0: Review Task Taxonomy

## Intent

Define every code review concern as a discrete, testable **review task** — the atomic unit of the entire system. Everything else (skills, evals, model scoring, tuning, composition) builds on this foundation.

## Scope

- Create a comprehensive taxonomy of review tasks across 10 concern categories
- Each task is a standalone markdown file with: description, detection heuristics, eval cases (buggy code + expected finding), and counter-examples (correct code that looks similar)
- Tasks are language-agnostic where possible, with language-specific variants noted
- Cover security (OWASP web/api/mobile), correctness, concurrency, testing, performance, reliability, API design, data, observability, and code quality

## Approach

1. Define the task file format (template)
2. Build out all tasks per category
3. Tag each task with: severity, applicable languages, applicable platforms
4. Include 2-3 eval cases and 1-2 counter-examples per task
5. These become the ground truth for Phase 1 (skills) and Phase 2 (benchmarks)

## Success Criteria

- Every known class of code bug/concern has a corresponding task file
- Each task has enough eval material to be independently testable
- Tasks are granular enough that a single skill prompt can target them
