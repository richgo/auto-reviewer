# Phase 1: Skills from Tasks

## Status
**In Progress** — Implementing skill composition layer

## Motivation
Phase 0 produced 197 atomic review tasks covering security, concurrency, correctness, testing, performance, reliability, API design, data integrity, observability, and code quality concerns across multiple platforms (Android, iOS, web, microservices).

Phase 1 composes these atomic tasks into **skills** following the Anthropic skill format for use in code review workflows.

## Goals
1. **Concern skills:** Group related review tasks by concern area (injection, auth, data protection, etc.)
2. **Language skills:** Provide language-specific guidance (Python, TypeScript, Java, etc.)
3. **Output skills:** Format review findings for different consumers (PR comments, inline annotations, Slack summaries)
4. **Core skills:** Orchestrate the review process (diff analysis, finding aggregation, deduplication)
5. **Tuning skills:** Enable continuous improvement (benchmark running, skill optimization, local calibration)
6. **Eval infrastructure:** Validate skill effectiveness with test cases
7. **Progressive disclosure:** Keep skills under 500 lines with references/ for detail

## Design

### Skill Structure
Every skill follows this format:
```markdown
---
name: skill-name
description: >
  Pushy, trigger-focused description that mentions specific patterns
  and contexts where this skill should be invoked.
---

# Skill Title

[Markdown content under 500 lines]
```

### Skill Categories

**Concern Skills (`skills/concerns/`):**
- `security-injection.md` — SQL, XSS, DOM XSS, command, LDAP, NoSQL injection
- `security-auth.md` — Auth bypass, CSRF, session management, passwords, OAuth
- `security-data-protection.md` — Secrets, path traversal, mass assignment, crypto, deserialization, file upload
- `security-network.md` — SSRF, TLS, security headers, CORS, open redirect
- `security-client-side.md` — Cookie security, clickjacking, prototype pollution, third-party code
- `security-api.md` — GraphQL, REST, transaction authorization
- `security-ai-llm.md` — Prompt injection, AI agent security, MCP tool poisoning
- `security-supply-chain.md` — Dependencies, pinning bypass, XXE
- `security-mobile.md` — Android/iOS/mobile-specific security tasks
- `security-infrastructure.md` — Docker, IaC, CI/CD, serverless, multi-tenant
- `concurrency.md` — Race conditions, deadlocks, async misuse, thread-unsafe collections
- `correctness.md` — Null deref, off-by-one, overflow, float comparison, logic inversion
- `testing.md` — Coverage gaps, weak assertions, flaky tests, isolation issues
- `performance.md` — N+1 queries, algorithmic complexity, memory leaks, unbounded growth
- `reliability.md` — Error handling, resource cleanup, timeouts, retries, degradation
- `api-design.md` — Input validation, response shapes, breaking changes, pagination
- `data-integrity.md` — PII exposure, migrations, serialization, schema validation
- `observability.md` — Logging gaps, missing metrics/tracing, crash reporting
- `code-quality.md` — Dead code, naming, DRY violations, missing docs

**Language Skills (`skills/languages/`):**
- `python.md`, `typescript.md`, `java.md`, `kotlin.md`, `swift.md`, `go.md`, `rust.md`, `csharp.md`, `cpp.md`, `ruby.md`, `php.md`
- Each includes: framework-specific security, language pitfalls, idioms, anti-patterns

**Output Skills (`skills/outputs/`):**
- `review-report.md` — Comprehensive Markdown PR comment
- `inline-comments.md` — Individual inline comments per finding
- `fix-pr.md` — Generate auto-fix PR
- `create-issues.md` — Create GitHub issues
- `slack-summary.md` — Brief notification

**Core Skills (`skills/core/`):**
- `review-orchestrator.md` — Main workflow: parse diff, dispatch skills, aggregate findings
- `diff-analysis.md` — Parse PR diffs, extract changed sections

**Tuning Skills (`skills/tuning/`):**
- `skill-optimizer.md` — Autoresearch loop for skill improvement
- `benchmark-runner.md` — Run skills against eval cases
- `local-calibration.md` — Adapt skills to repo conventions

### Eval Infrastructure
`evals/evals.json` contains:
- **Eval cases:** Code snippets with expected findings
- **Counter-examples:** Safe code that should not be flagged
- **Assertions:** Binary pass/fail checks
- **Scoring:** Metrics for precision, recall, F1, false positive rate

Example eval case:
```json
{
  "id": "sql-injection-001",
  "skill": "security-injection",
  "language": "python",
  "severity": "critical",
  "prompt": "query = f\"SELECT * FROM users WHERE id = {user_id}\"",
  "expected_findings": [{"type": "sql-injection", "line": 1}],
  "assertions": {
    "must_detect": true,
    "severity": "critical",
    "suggest_parameterized_query": true
  }
}
```

## Implementation Status

### Completed
- ✅ `skills/concerns/security-injection.md`
- ✅ `skills/concerns/security-auth.md`
- ✅ `skills/concerns/security-data-protection.md`
- ✅ `skills/concerns/security-network.md`
- ✅ `skills/concerns/concurrency.md`
- ✅ `skills/concerns/correctness.md`
- ✅ `skills/languages/python.md`
- ✅ `skills/core/review-orchestrator.md`
- ✅ `skills/outputs/review-report.md`
- ✅ `evals/evals.json` (16 test cases + 5 counter-examples)

### In Progress
- ⏳ Remaining concern skills (14 more)
- ⏳ Remaining language skills (10 more)
- ⏳ Remaining output skills (4 more)
- ⏳ diff-analysis.md
- ⏳ Tuning skills (3)

### Future Work
- Eval harness implementation (runner script)
- Integration with GitHub Actions
- Skill performance metrics dashboard
- Continuous skill improvement loop

## Success Criteria
1. All 19 concern skills implemented
2. All 11 language skills implemented
3. All 5 output skills implemented
4. Core orchestration functional
5. Eval cases pass with >90% precision and >80% recall
6. Skills successfully reference review-tasks/ for detail
7. Each skill under 500 lines

## Non-Goals
- Runtime implementation (Phase 2)
- LLM integration (Phase 2)
- GitHub App deployment (Phase 3)
- Real-world testing on live repos (Phase 3)

## Timeline
- **Phase 1 Start:** 2026-03-21
- **Phase 1 Target:** 2026-03-22 (skill composition)
- **Phase 2 Target:** 2026-03-29 (runtime + LLM integration)
- **Phase 3 Target:** 2026-04-15 (deployment + live testing)

## Dependencies
- Phase 0 review tasks (✅ complete)
- OWASP CheatSheetSeries references (✅ mapped)
- Anthropic skill format spec (✅ defined)

## Risk Mitigation
- **Skill bloat:** Use progressive disclosure, move details to references/
- **Eval quality:** Start with known CVE examples, expand iteratively
- **False positives:** Counter-examples mandatory for each eval case
- **Maintenance:** Keep skills modular, avoid cross-dependencies

## Open Questions
1. Should language skills include framework detection heuristics?
2. How to handle skill version evolution (backward compat)?
3. What's the right balance between specificity and generalization?

## References
- Phase 0 deliverable: `review-tasks/INDEX.md`
- OWASP CheatSheetSeries: https://github.com/OWASP/CheatSheetSeries
- Anthropic skill format: (internal spec)
