# Phase 1 Implementation Tasks

## Phase 1: Concern Skills (19 total)

### Security Concern Skills (10)
- [x] **1.1** `security-injection.md` — SQL, XSS, DOM XSS, command, LDAP, NoSQL injection
- [x] **1.2** `security-auth.md` — Auth bypass, CSRF, authentication, session, credentials, passwords, OAuth
- [x] **1.3** `security-data-protection.md` — Secrets, path traversal, mass assignment, crypto, deserialization, file upload
- [x] **1.4** `security-network.md` — SSRF, TLS, headers, CORS, open redirect
- [x] **1.5** `security-client-side.md` — Cookie security, clickjacking, prototype pollution, third-party code + web/ tasks
- [x] **1.6** `security-api.md` — GraphQL, REST, transaction authorization
- [x] **1.7** `security-ai-llm.md` — Prompt injection, AI agent security, MCP tool poisoning
- [x] **1.8** `security-supply-chain.md` — Dependencies, pinning, XXE
- [x] **1.9** `security-mobile.md` — Android/iOS/mobile security (21 tasks)
- [x] **1.10** `security-infrastructure.md` — Docker, IaC, CI/CD, serverless, multi-tenant

### Other Concern Skills (9)
- [x] **1.11** `concurrency.md` — Race conditions, deadlocks, async, thread-unsafe collections, livelock + platform-specific
- [x] **1.12** `correctness.md` — Null deref, off-by-one, overflow, float comparison, logic inversion + platform-specific
- [x] **1.13** `testing.md` — Coverage, assertions, isolation, mocking, flaky tests + platform-specific
- [x] **1.14** `performance.md` — N+1, complexity, memory leaks, unbounded growth + platform-specific
- [x] **1.15** `reliability.md` — Error handling, cleanup, timeouts, retries, degradation + platform-specific
- [x] **1.16** `api-design.md` — Validation, response shapes, breaking changes, pagination + mobile/microservices
- [x] **1.17** `data-integrity.md` — PII, migrations, serialization, schema validation + platform-specific
- [x] **1.18** `observability.md` — Logging, metrics, tracing, crash reporting + platform-specific
- [x] **1.19** `code-quality.md` — Dead code, naming, DRY, docs + platform-specific

---

## Phase 2: Language Skills (11 total)

- [x] **2.1** `python.md` — Django/Flask security, mutable defaults, GIL, subprocess, pickle, eval
- [x] **2.2** `typescript.md` — Node.js/Express security, type coercion, async/await, prototype pollution
- [x] **2.3** `java.md` — Spring Boot security, null handling, concurrency (synchronized), deserialization
- [x] **2.4** `kotlin.md` — Android security, null safety (!!, ?.), coroutines, lateinit
- [x] **2.5** `swift.md` — iOS security, optionals (!, ?), ARC, actors, @MainActor
- [x] **2.6** `go.md` — goroutines, channels, defer, error handling, SQL injection in database/sql
- [x] **2.7** `rust.md` — Memory safety, ownership, borrowing, unsafe blocks, Send/Sync
- [x] **2.8** `csharp.md` — .NET security, async/await, LINQ injection, deserialization
- [x] **2.9** `cpp.md` — Memory management, buffer overflows, use-after-free, RAII
- [x] **2.10** `ruby.md` — Rails security, mass assignment, SQL injection, YAML deserialization
- [x] **2.11** `php.md` — Laravel/Symfony security, type juggling, SQL injection, file inclusion

---

## Phase 3: Output Skills (5 total)

- [x] **3.1** `review-report.md` — Comprehensive Markdown PR comment with severity grouping
- [x] **3.2** `inline-comments.md` — Individual GitHub/GitLab inline comments per finding
- [x] **3.3** `fix-pr.md` — Auto-generate PR with code fixes
- [x] **3.4** `create-issues.md` — Create GitHub issues for findings
- [x] **3.5** `slack-summary.md` — Brief Slack/Discord notification

---

## Phase 4: Core Skills (2 total)

- [x] **4.1** `review-orchestrator.md` — Main workflow: parse diff, dispatch, aggregate, dedupe, rank
- [x] **4.2** `diff-analysis.md` — Parse PR diffs, extract changed sections, identify languages/platforms

---

## Phase 5: Tuning Skills (3 total)

- [x] **5.1** `skill-optimizer.md` — Autoresearch loop: read eval failures, mutate prompts, re-evaluate
- [x] **5.2** `benchmark-runner.md` — Run skills against eval cases, score precision/recall/F1
- [x] **5.3** `local-calibration.md` — Adapt skills to repo-specific conventions and naming

---

## Phase 6: Eval Infrastructure

- [x] **6.1** `evals/evals.json` — Initial eval cases (legacy file, now split)
- [x] **6.2** `evals/security-injection.json` — Injection eval cases + counter-examples
- [x] **6.3** `evals/security-auth.json` — Auth eval cases + counter-examples
- [x] **6.4** `evals/security-data-protection.json` — Data protection eval cases + counter-examples
- [x] **6.5** `evals/security-network.json` — Network security eval cases + counter-examples
- [x] **6.6** `evals/concurrency.json` — Concurrency eval cases + counter-examples
- [x] **6.7** `evals/correctness.json` — Correctness eval cases + counter-examples
- [x] **6.8** `evals/performance.json` — Performance eval cases + counter-examples

---

## Phase 7: OpenSpec Documentation

- [x] **7.1** `openspec/changes/phase-1-skills-from-tasks/proposal.md` — Proper OpenSpec proposal format
- [x] **7.2** `openspec/changes/phase-1-skills-from-tasks/tasks.md` — This file (task breakdown)
- [x] **7.3** `openspec/changes/phase-1-skills-from-tasks/.openspec.yaml` — Metadata (status: active)
- [x] **7.4** `openspec/changes/phase-1-skills-from-tasks/specs/skills/spec.md` — Delta spec for skill format
- [x] **7.5** `openspec/changes/phase-1-skills-from-tasks/specs/evals/spec.md` — Delta spec for eval infrastructure
- [x] **7.6** `openspec/changes/phase-1-skills-from-tasks/specs/tuning/spec.md` — Delta spec for tuning approach
- [x] **7.7** `openspec/changes/phase-1-skills-from-tasks/design/design.md` — Technical design decisions

---

## Remaining Work

### Eval Expansion (P1)
- [ ] **8.1** Create eval JSON files for remaining concern skills (11 more files)
  - security-client-side.json, security-api.json, security-ai-llm.json, security-supply-chain.json, security-mobile.json, security-infrastructure.json
  - testing.json, reliability.json, api-design.json, data-integrity.json, observability.json, code-quality.json
- [ ] **8.2** Add language-specific eval cases for each language skill (11 files)
- [ ] **8.3** Add platform-specific eval cases (Android, iOS, web, microservices subsections)

### References Structure (P2)
- [ ] **9.1** Identify skills exceeding 500 lines and refactor to skill + references/
- [ ] **9.2** Move OWASP cheat sheet mappings to references/ for large security skills
- [ ] **9.3** Create payload catalogs in references/ for injection skills

### Integration Testing (P2)
- [ ] **10.1** Test orchestrator end-to-end with sample PR diffs
- [ ] **10.2** Verify skill dispatch logic (language detection, platform routing)
- [ ] **10.3** Test deduplication fingerprinting with overlapping findings
- [ ] **10.4** Validate output skill formatting (review-report, inline-comments)

---

## Acceptance Criteria

**Phase 1 is considered complete when:**
- [x] All 19 concern skills implemented
- [x] All 11 language skills implemented
- [x] All 5 output skills implemented
- [x] All 2 core skills implemented
- [x] All 3 tuning skills implemented
- [x] Initial eval cases exist (8 JSON files with test cases for major concern skills)
- [x] OpenSpec documentation complete (proposal, specs, design, tasks, .openspec.yaml)
- [ ] Eval coverage expanded to all 19 concern skills (11 more files needed)
- [ ] Skills validated under 500 lines or using references/ (audit needed)

**Quality gates met:**
- [x] Skills reference review-tasks/ for detailed detection logic
- [x] Security skills reference OWASP cheat sheets
- [x] Platform-specific subsections present where applicable
- [x] Eval cases include counter-examples for false positive prevention

---

## Summary

**Delivered in Phase 1:**
- ✅ **40 skills** across 5 categories (concerns, languages, outputs, core, tuning)
- ✅ **8 eval JSON files** with test cases and counter-examples
- ✅ **Complete OpenSpec documentation** (proposal, specs, design, tasks, metadata)

**Remaining for Phase 1 completion:**
- 🔲 Expand eval coverage to all 19 concern skills (11 more JSON files)
- 🔲 Add language/platform-specific eval cases
- 🔲 Audit skills for 500-line limit and refactor to references/ where needed

**Estimated effort for remaining work:** 4-6 hours

---

## Timeline

- **Phase 1 Start:** 2026-03-21 11:18
- **Phase 1 Core Complete:** 2026-03-21 12:00 (all 40 skills + initial evals + OpenSpec docs)
- **Phase 1 Full Completion Target:** 2026-03-22 (eval expansion + references refactor)
- **Phase 2 Target:** 2026-03-29 (runtime + LLM integration + GitHub App)
