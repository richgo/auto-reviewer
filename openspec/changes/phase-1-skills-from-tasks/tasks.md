# Phase 1 Implementation Tasks

## Task Breakdown

### 1. Concern Skills (19 total)
**Status:** 6/19 complete

#### Security Concern Skills (10)
- [x] `security-injection.md` — SQL, XSS, DOM XSS, command, LDAP, NoSQL injection
- [x] `security-auth.md` — Auth bypass, CSRF, authentication, session, credentials, passwords, OAuth
- [x] `security-data-protection.md` — Secrets, path traversal, mass assignment, crypto, deserialization, file upload
- [x] `security-network.md` — SSRF, TLS, headers, CORS, open redirect
- [ ] `security-client-side.md` — Cookie security, clickjacking, prototype pollution, third-party code + web/ tasks
- [ ] `security-api.md` — GraphQL, REST, transaction authorization
- [ ] `security-ai-llm.md` — Prompt injection, AI agent security, MCP tool poisoning
- [ ] `security-supply-chain.md` — Dependencies, pinning, XXE
- [ ] `security-mobile.md` — Android/iOS/mobile security (21 tasks)
- [ ] `security-infrastructure.md` — Docker, IaC, CI/CD, serverless, multi-tenant

#### Other Concern Skills (9)
- [x] `concurrency.md` — Race conditions, deadlocks, async, thread-unsafe collections, livelock + platform-specific
- [x] `correctness.md` — Null deref, off-by-one, overflow, float comparison, logic inversion + platform-specific
- [ ] `testing.md` — Coverage, assertions, isolation, mocking, flaky tests + platform-specific
- [ ] `performance.md` — N+1, complexity, memory leaks, unbounded growth + platform-specific
- [ ] `reliability.md` — Error handling, cleanup, timeouts, retries, degradation + platform-specific
- [ ] `api-design.md` — Validation, response shapes, breaking changes, pagination + mobile/microservices
- [ ] `data-integrity.md` — PII, migrations, serialization, schema validation + platform-specific
- [ ] `observability.md` — Logging, metrics, tracing, crash reporting + platform-specific
- [ ] `code-quality.md` — Dead code, naming, DRY, docs + platform-specific

---

### 2. Language Skills (11 total)
**Status:** 1/11 complete

- [x] `python.md` — Django/Flask security, mutable defaults, GIL, subprocess, pickle, eval
- [ ] `typescript.md` — Node.js/Express security, type coercion, async/await, prototype pollution
- [ ] `java.md` — Spring Boot security, null handling, concurrency (synchronized), deserialization
- [ ] `kotlin.md` — Android security, null safety (!!, ?.), coroutines, lateinit
- [ ] `swift.md` — iOS security, optionals (!, ?), ARC, actors, @MainActor
- [ ] `go.md` — goroutines, channels, defer, error handling, SQL injection in database/sql
- [ ] `rust.md` — Memory safety, ownership, borrowing, unsafe blocks, Send/Sync
- [ ] `csharp.md` — .NET security, async/await, LINQ injection, deserialization
- [ ] `cpp.md` — Memory management, buffer overflows, use-after-free, RAII
- [ ] `ruby.md` — Rails security, mass assignment, SQL injection, YAML deserialization
- [ ] `php.md` — Laravel/Symfony security, type juggling, SQL injection, file inclusion

---

### 3. Output Skills (5 total)
**Status:** 1/5 complete

- [x] `review-report.md` — Comprehensive Markdown PR comment with severity grouping
- [ ] `inline-comments.md` — Individual GitHub/GitLab inline comments per finding
- [ ] `fix-pr.md` — Auto-generate PR with code fixes
- [ ] `create-issues.md` — Create GitHub issues for findings
- [ ] `slack-summary.md` — Brief Slack/Discord notification

---

### 4. Core Skills (2 total)
**Status:** 1/2 complete

- [x] `review-orchestrator.md` — Main workflow: parse diff, dispatch, aggregate, dedupe, rank
- [ ] `diff-analysis.md` — Parse PR diffs, extract changed sections, identify languages/platforms

---

### 5. Tuning Skills (3 total)
**Status:** 0/3 complete

- [ ] `skill-optimizer.md` — Autoresearch loop: read eval failures, mutate prompts, re-evaluate
- [ ] `benchmark-runner.md` — Run skills against eval cases, score precision/recall/F1
- [ ] `local-calibration.md` — Adapt skills to repo-specific conventions and naming

---

### 6. Eval Infrastructure
**Status:** ✅ Complete (initial version)

- [x] `evals/evals.json` — 16 eval cases covering major security concerns
- [x] Counter-examples for false positive testing
- [x] Assertions and scoring rubric defined

**Future expansion:**
- [ ] Add eval cases for all concern skills (currently only security + concurrency + correctness)
- [ ] Add language-specific eval cases
- [ ] Add platform-specific eval cases (Android, iOS, microservices)

---

### 7. References Structure
**Status:** Not started

Each skill with >500 lines of content should use `references/` subdirectory:

Example structure:
```
skills/concerns/security-injection/
  SKILL.md          # Main skill (under 500 lines)
  references/
    sql-injection-examples.md
    xss-payloads.md
    owasp-guidance.md
```

**Task:** Identify skills needing references/ and refactor.

---

### 8. OpenSpec Documentation
**Status:** ✅ Complete

- [x] `openspec/changes/phase-1-skills-from-tasks/proposal.md`
- [x] `openspec/changes/phase-1-skills-from-tasks/tasks.md`

---

## Priority Order

### P0 (Critical Path)
1. Complete remaining security concern skills (client-side, API, AI/LLM, supply-chain, mobile, infrastructure)
2. Complete `diff-analysis.md` (required for orchestrator to function)
3. Expand eval cases to cover all security concerns

### P1 (High Value)
4. Complete language skills (TypeScript, Java, Kotlin, Swift prioritized for common usage)
5. Complete `inline-comments.md` output skill (more actionable than full reports)
6. Implement benchmark-runner.md for continuous validation

### P2 (Nice to Have)
7. Complete remaining concern skills (testing, performance, reliability, api-design, data-integrity, observability, code-quality)
8. Complete remaining language skills (Go, Rust, C#, C++, Ruby, PHP)
9. Complete tuning skills (optimizer, calibration)
10. Refactor large skills into skill + references/ structure

---

## Acceptance Criteria

**Phase 1 is complete when:**
- [ ] All 19 concern skills implemented
- [ ] All 11 language skills implemented
- [ ] All 5 output skills implemented
- [ ] All 2 core skills implemented
- [ ] All 3 tuning skills implemented
- [ ] Eval cases cover all concern skills
- [ ] All skills under 500 lines (or using references/)
- [ ] Skills reference review-tasks/ appropriately
- [ ] OpenSpec documentation complete
- [ ] Git committed and pushed

**Quality gates:**
- Each skill has at least 2 eval cases
- Each eval case has at least 1 counter-example
- All examples include fix suggestions
- All security skills reference OWASP cheat sheets
- Platform-specific subsections present where applicable

---

## Estimated Effort

| Category | Tasks | Lines/Task | Total Lines | Estimated Time |
|----------|-------|------------|-------------|----------------|
| Concern skills (remaining) | 13 | 400 | 5,200 | 6h |
| Language skills (remaining) | 10 | 350 | 3,500 | 5h |
| Output skills (remaining) | 4 | 300 | 1,200 | 2h |
| Core skills (remaining) | 1 | 400 | 400 | 1h |
| Tuning skills | 3 | 400 | 1,200 | 2h |
| Eval expansion | - | - | - | 2h |
| Testing & polish | - | - | - | 2h |
| **Total** | **31** | **-** | **11,500** | **20h** |

---

## Dependencies & Blockers

**Dependencies:**
- Phase 0 review tasks (✅ complete)
- OWASP CheatSheetSeries mapping (✅ complete)
- Skill format spec (✅ defined)

**Blockers:**
- None currently

**Risks:**
- Scope creep (19 concern skills is already large)
- Eval quality (need diverse, realistic test cases)
- Skill overlap (deduplication logic in orchestrator critical)

---

## Next Steps

1. **Complete P0 security concern skills** (client-side, API, AI/LLM, supply-chain, mobile, infrastructure)
2. **Implement diff-analysis.md** for orchestrator integration
3. **Expand evals** to cover new concern skills
4. **Begin P1 language skills** (TypeScript, Java, Kotlin, Swift)
5. **Implement inline-comments.md** output skill
6. **Test orchestrator** end-to-end with sample PR
7. **Document findings** and iterate

---

## Timeline

- **Day 1 (Today):** Complete 6 concern skills, 1 language skill, 1 core skill, 1 output skill, evals, OpenSpec
- **Day 2:** Complete remaining P0 security concerns, diff-analysis, expand evals
- **Day 3-4:** Complete P1 language skills, inline-comments output
- **Day 5-6:** Complete remaining concern skills
- **Day 7:** Complete tuning skills, testing, polish, commit

**Target completion:** 2026-03-27 (7 days)
