# Review Task Index

## Status Legend
- ✅ Complete (has eval cases + counter-examples + assertions)
- 🔲 Planned (needs content)

## Security (7 complete, ~8 planned)
- ✅ [sql-injection](security/sql-injection.md) — critical
- ✅ [xss](security/xss.md) — high
- ✅ [auth-bypass](security/auth-bypass.md) — critical (IDOR, broken access control)
- ✅ [secrets-exposure](security/secrets-exposure.md) — critical
- ✅ [ssrf](security/ssrf.md) — critical
- ✅ [path-traversal](security/path-traversal.md) — critical
- ✅ [csrf](security/csrf.md) — high
- ✅ [mass-assignment](security/mass-assignment.md) — high
- 🔲 insecure-deserialization — critical
- 🔲 xml-external-entity — high
- 🔲 open-redirect — medium
- 🔲 insecure-crypto — high
- 🔲 cors-misconfiguration — medium
- 🔲 insecure-direct-object-ref-mobile — high (OWASP Mobile)
- 🔲 insecure-storage-mobile — high (OWASP Mobile)
- 🔲 insufficient-transport-security — high

## Concurrency (3 complete, ~2 planned)
- ✅ [race-condition](concurrency/race-condition.md) — high
- ✅ [deadlock](concurrency/deadlock.md) — high
- ✅ [async-misuse](concurrency/async-misuse.md) — high
- 🔲 thread-unsafe-collection — high
- 🔲 livelock — medium

## Correctness (2 complete, ~4 planned)
- ✅ [null-deref](correctness/null-deref.md) — high
- ✅ [off-by-one](correctness/off-by-one.md) — medium
- 🔲 type-coercion — medium
- 🔲 integer-overflow — high
- 🔲 floating-point-comparison — medium
- 🔲 logic-inversion — medium

## Testing (2 complete, ~3 planned)
- ✅ [missing-test-coverage](testing/missing-test-coverage.md) — medium
- ✅ [weak-assertions](testing/weak-assertions.md) — medium
- 🔲 test-isolation — medium (tests depending on each other)
- 🔲 mock-overuse — low
- 🔲 flaky-test-patterns — medium

## Performance (3 complete, ~3 planned)
- ✅ [n-plus-one](performance/n-plus-one.md) — high
- ✅ [algorithmic-complexity](performance/algorithmic-complexity.md) — medium
- ✅ [memory-leak](performance/memory-leak.md) — high
- 🔲 unbounded-growth — medium (queues, logs, buffers)
- 🔲 bundle-size — low (frontend)
- 🔲 unnecessary-rerender — medium (React/UI)

## Reliability (2 complete, ~3 planned)
- ✅ [error-handling](reliability/error-handling.md) — high
- ✅ [resource-cleanup](reliability/resource-cleanup.md) — high
- 🔲 timeout-handling — medium
- 🔲 graceful-degradation — medium
- 🔲 retry-without-backoff — medium

## API Design (1 complete, ~3 planned)
- ✅ [input-validation](api-design/input-validation.md) — high
- 🔲 inconsistent-response-shape — medium
- 🔲 breaking-api-change — high
- 🔲 missing-pagination — medium

## Data (2 complete, ~2 planned)
- ✅ [pii-exposure](data/pii-exposure.md) — critical
- ✅ [migration-safety](data/migration-safety.md) — high
- 🔲 serialization-mismatch — medium
- 🔲 schema-validation — medium

## Observability (1 complete, ~2 planned)
- ✅ [logging-gaps](observability/logging-gaps.md) — medium
- 🔲 missing-metrics — medium
- 🔲 missing-tracing — medium

## Code Quality (1 complete, ~4 planned)
- ✅ [dead-code](code-quality/dead-code.md) — low
- 🔲 naming-readability — low
- 🔲 dry-violations — low
- 🔲 missing-documentation — low
- 🔲 accessibility — medium (UI)

---

**Total: 24 complete, ~34 planned = ~58 tasks**
