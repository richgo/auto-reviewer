# Review Task Index

## Status Legend
- ✅ Complete (has eval cases + counter-examples + assertions)
- ✅ Planned (needs content)

## Platform Organization Convention
Every category follows a strict platform subfolder structure:
- **android/** — Android-specific tasks
- **ios/** — iOS-specific tasks
- **web/** — Web-specific tasks (browser, frontend frameworks)
- **microservices/** — Microservices/distributed systems tasks

Tasks at the category root level are **truly universal** and apply across all platforms (e.g., null-deref, race-condition, n-plus-one for server APIs).

Platform-specific tasks (even if just web-centric) belong in their respective subfolder for consistency.

## OWASP Coverage
Every task in the Security section is mapped to one or more [OWASP Cheat Sheets](https://github.com/OWASP/CheatSheetSeries). The `[OWASP: ...]` tag shows the mapping.

---

## Security — Injection (6 tasks)
- ✅ [sql-injection](security/sql-injection.md) — critical `[OWASP: SQL_Injection_Prevention, Query_Parameterization]`
- ✅ [xss](security/xss.md) — high `[OWASP: Cross_Site_Scripting_Prevention, DOM_based_XSS_Prevention]`
- ✅ [dom-xss](security/dom-xss.md) — high `[OWASP: DOM_based_XSS_Prevention, DOM_Clobbering_Prevention]`
- ✅ [command-injection](security/command-injection.md) — critical `[OWASP: OS_Command_Injection_Defense, Injection_Prevention]`
- ✅ [ldap-injection](security/ldap-injection.md) — high `[OWASP: LDAP_Injection_Prevention]`
- ✅ [nosql-injection](security/nosql-injection.md) — high `[OWASP: NoSQL_Security, Injection_Prevention]`

## Security — Authentication & Session (8 tasks)
- ✅ [auth-bypass](security/auth-bypass.md) — critical `[OWASP: Access_Control, Authorization, Insecure_Direct_Object_Reference_Prevention]`
- ✅ [csrf](security/csrf.md) — high `[OWASP: Cross-Site_Request_Forgery_Prevention]`
- ✅ [authentication-flaws](security/authentication-flaws.md) — critical `[OWASP: Authentication, Multifactor_Authentication, Choosing_and_Using_Security_Questions]`
- ✅ [session-management](security/session-management.md) — high `[OWASP: Session_Management]`
- ✅ [credential-stuffing](security/credential-stuffing.md) — high `[OWASP: Credential_Stuffing_Prevention]`
- ✅ [password-storage](security/password-storage.md) — critical `[OWASP: Password_Storage]`
- ✅ [password-reset-flaws](security/password-reset-flaws.md) — high `[OWASP: Forgot_Password]`
- ✅ [oauth-misconfiguration](security/oauth-misconfiguration.md) — high `[OWASP: OAuth2, SAML_Security, JSON_Web_Token_for_Java]`

## Security — Data Protection (6 tasks)
- ✅ [secrets-exposure](security/secrets-exposure.md) — critical `[OWASP: Secrets_Management, Key_Management]`
- ✅ [path-traversal](security/path-traversal.md) — critical
- ✅ [mass-assignment](security/mass-assignment.md) — high `[OWASP: Mass_Assignment]`
- ✅ [insecure-crypto](security/insecure-crypto.md) — high `[OWASP: Cryptographic_Storage, Key_Management, TLS_Cipher_String]`
- ✅ [insecure-deserialization](security/insecure-deserialization.md) — critical `[OWASP: Deserialization]`
- ✅ [file-upload](security/file-upload.md) — high `[OWASP: File_Upload]`

## Security — Network & Transport (5 tasks)
- ✅ [ssrf](security/ssrf.md) — critical `[OWASP: Server_Side_Request_Forgery_Prevention]`
- ✅ [insufficient-transport-security](security/insufficient-transport-security.md) — high `[OWASP: Transport_Layer_Security, Transport_Layer_Protection, HTTP_Strict_Transport_Security]`
- ✅ [missing-security-headers](security/missing-security-headers.md) — medium `[OWASP: HTTP_Headers, Content_Security_Policy, Clickjacking_Defense]`
- ✅ [cors-misconfiguration](security/cors-misconfiguration.md) — medium `[OWASP: REST_Security, AJAX_Security, HTML5_Security]`
- ✅ [open-redirect](security/open-redirect.md) — medium `[OWASP: Unvalidated_Redirects_and_Forwards]`

## Security — Cookie & Client-Side (4 tasks)
- ✅ [cookie-security](security/cookie-security.md) — high `[OWASP: Cookie_Theft_Mitigation, Session_Management]`
- ✅ [clickjacking](security/clickjacking.md) — medium `[OWASP: Clickjacking_Defense]`
- ✅ [prototype-pollution](security/prototype-pollution.md) — high `[OWASP: Prototype_Pollution_Prevention]`
- ✅ [third-party-code](security/third-party-code.md) — medium `[OWASP: Third_Party_Javascript_Management, Securing_Cascading_Style_Sheets]`

## Security — API & GraphQL (3 tasks)
- ✅ [graphql-security](security/graphql-security.md) — high `[OWASP: GraphQL]`
- ✅ [rest-security](security/rest-security.md) — medium `[OWASP: REST_Security, REST_Assessment]`
- ✅ [transaction-authorization](security/transaction-authorization.md) — high `[OWASP: Transaction_Authorization, Third_Party_Payment_Gateway_Integration]`

## Security — AI & LLM (3 tasks)
- ✅ [prompt-injection](security/prompt-injection.md) — critical `[OWASP: LLM_Prompt_Injection_Prevention]`
- ✅ [ai-agent-security](security/ai-agent-security.md) — high `[OWASP: AI_Agent_Security, MCP_Security, Secure_AI_Model_Ops]`
- ✅ [mcp-tool-poisoning](security/mcp-tool-poisoning.md) — critical `[OWASP: MCP_Security]`

## Security — Supply Chain & Dependencies (3 tasks)
- ✅ [dependency-vulnerability](security/dependency-vulnerability.md) — high `[OWASP: Software_Supply_Chain_Security, Dependency_Graph_SBOM, NPM_Security]`
- ✅ [pinning-bypass](security/pinning-bypass.md) — high (mobile) `[OWASP: Pinning]`
- ✅ [xml-external-entity](security/xml-external-entity.md) — high

## Security — Denial of Service (2 tasks)
- ✅ [denial-of-service](security/denial-of-service.md) — high `[OWASP: Denial_of_Service]`
- ✅ [regex-dos](security/regex-dos.md) — medium (ReDoS)

## Security — Infrastructure (code-level concerns) (5 tasks)
- ✅ [docker-misconfiguration](security/docker-misconfiguration.md) — high `[OWASP: Docker_Security, NodeJS_Docker]`
- ✅ [iac-security](security/iac-security.md) — high `[OWASP: Infrastructure_as_Code_Security, Kubernetes_Security]`
- ✅ [cicd-security](security/cicd-security.md) — high `[OWASP: CI_CD_Security]`
- ✅ [serverless-security](security/serverless-security.md) — medium `[OWASP: Serverless_FaaS_Security]`
- ✅ [multi-tenant-isolation](security/multi-tenant-isolation.md) — critical `[OWASP: Multi_Tenant_Security]`

## Security — Android (8 tasks) `[OWASP: Mobile_Application_Security, MASVS]`
- ✅ [android-insecure-storage](security/android/insecure-storage.md) — high — SharedPreferences/SQLite with plaintext secrets, world-readable files `[MASVS-STORAGE]`
- ✅ [android-exported-components](security/android/exported-components.md) — critical — exported Activities/Services/Receivers/Providers without permission checks `[MASVS-PLATFORM]`
- ✅ [android-intent-injection](security/android/intent-injection.md) — high — unvalidated Intent extras, implicit intents for sensitive ops `[MASVS-PLATFORM]`
- ✅ [android-webview-security](security/android/webview-security.md) — high — JavaScript enabled, file access, universal XSS in WebView `[MASVS-PLATFORM]`
- ✅ [android-insecure-crypto](security/android/insecure-crypto.md) — high — hardcoded keys, weak algorithms, missing Android Keystore usage `[MASVS-CRYPTO]`
- ✅ [android-network-security](security/android/network-security.md) — high — missing network_security_config, cleartext traffic, cert validation bypass `[MASVS-NETWORK]`
- ✅ [android-logging-sensitive-data](security/android/logging-sensitive-data.md) — medium — Log.d/Log.i with PII/tokens in release builds `[MASVS-STORAGE]`
- ✅ [android-backup-exposure](security/android/backup-exposure.md) — medium — allowBackup=true, unencrypted auto-backup exposing app data `[MASVS-STORAGE]`

## Security — iOS (8 tasks) `[OWASP: Mobile_Application_Security, MASVS]`
- ✅ [ios-insecure-storage](security/ios/insecure-storage.md) — high — UserDefaults/plist with secrets, missing Keychain for sensitive data `[MASVS-STORAGE]`
- ✅ [ios-ats-bypass](security/ios/ats-bypass.md) — high — NSAllowsArbitraryLoads, NSExceptionDomains overrides disabling ATS `[MASVS-NETWORK]`
- ✅ [ios-url-scheme-hijack](security/ios/url-scheme-hijack.md) — high — custom URL schemes without validation, universal link misconfiguration `[MASVS-PLATFORM]`
- ✅ [ios-keychain-misuse](security/ios/keychain-misuse.md) — medium — wrong Keychain accessibility class, missing access control flags `[MASVS-CRYPTO]`
- ✅ [ios-pasteboard-leak](security/ios/pasteboard-leak.md) — medium — sensitive data copied to system pasteboard (UIPasteboard.general) `[MASVS-STORAGE]`
- ✅ [ios-screenshot-exposure](security/ios/screenshot-exposure.md) — low — sensitive screens not hidden during app backgrounding `[MASVS-STORAGE]`
- ✅ [ios-insecure-crypto](security/ios/insecure-crypto.md) — high — deprecated CommonCrypto usage, ECB mode, hardcoded IVs `[MASVS-CRYPTO]`
- ✅ [ios-jailbreak-detection-bypass](security/ios/jailbreak-detection-bypass.md) — medium — trivially bypassable jailbreak checks `[MASVS-RESILIENCE]`

## Security — Mobile Shared (5 tasks) `[OWASP: Mobile_Application_Security, Pinning, MASVS]`
- ✅ [mobile-cert-pinning](security/mobile/cert-pinning.md) — high — missing certificate/public key pinning, bypassable implementations `[MASVS-NETWORK, Pinning]`
- ✅ [mobile-biometric-auth-bypass](security/mobile/biometric-auth-bypass.md) — high — local-only biometric check without backend token validation `[MASVS-AUTH]`
- ✅ [mobile-deep-link-hijack](security/mobile/deep-link-hijack.md) — high — unvalidated deep link parameters, open redirect via deep links `[MASVS-PLATFORM]`
- ✅ [mobile-binary-hardening](security/mobile/binary-hardening.md) — medium — missing obfuscation, debug symbols in release, anti-tamper checks `[MASVS-RESILIENCE]`
- ✅ [mobile-privacy-data-collection](security/mobile/privacy-data-collection.md) — medium — excessive permissions, tracking without consent, clipboard snooping `[MASVS-PRIVACY]`

## Security — Logging & Error Handling (2 tasks)
- ✅ [security-error-info-leak](security/security-error-info-leak.md) — medium `[OWASP: Error_Handling]`
- ✅ [security-logging](security/security-logging.md) — medium `[OWASP: Logging, Logging_Vocabulary]`

## Security — Microservices (7 tasks) `[OWASP: Microservices_Security, Microservices_based_Security_Arch_Doc]`
- ✅ [microservices-auth](security/microservices/auth.md) — high — missing service-to-service auth, shared secrets between services
- ✅ [microservices-broken-trust-boundary](security/microservices/broken-trust-boundary.md) — critical — internal APIs trusting external input, missing gateway validation
- ✅ [microservices-data-exposure](security/microservices/data-exposure.md) — high — over-fetching across service boundaries, PII leaking between services
- ✅ [microservices-insecure-messaging](security/microservices/insecure-messaging.md) — high — unencrypted message queues, unsigned events, replay attacks
- ✅ [microservices-distributed-session](security/microservices/distributed-session.md) — medium — inconsistent session handling across services, JWT validation gaps
- ✅ [microservices-service-mesh-bypass](security/microservices/service-mesh-bypass.md) — high — direct pod-to-pod calls bypassing mesh policies `[OWASP: Network_Segmentation]`
- ✅ [microservices-cascading-failure](security/microservices/cascading-failure.md) — high — missing circuit breakers, unbounded retries causing cascading outages

## Security — Web-Specific (consolidation)
The following tasks are web-platform-specific and already listed in other sections:
- XSS, DOM XSS → Injection
- CSRF, clickjacking, CSP headers, CORS → Network & Client-Side
- Cookie security, prototype pollution, third-party JS → Cookie & Client-Side
- GraphQL, REST security → API & GraphQL
- Session management, OAuth → Auth & Session

Additional web-specific tasks:
- ✅ [web-csp-bypass](security/web/csp-bypass.md) — medium — CSP policies with unsafe-inline/unsafe-eval, nonce misuse
- ✅ [web-subresource-integrity](security/web/subresource-integrity.md) — medium — CDN scripts without SRI hashes
- ✅ [web-postmessage-origin](security/web/postmessage-origin.md) — high — `postMessage` without origin validation, `window.opener` attacks
- ✅ [web-client-side-storage](security/web/client-side-storage.md) — medium — tokens/secrets in localStorage, unencrypted IndexedDB
- ✅ [web-html-injection](security/web/html-injection.md) — medium — user content in meta tags, link injection, form action hijack

## Security — Framework-Specific (language skills reference)
These map to **language skills** rather than standalone tasks. Each language skill should incorporate the relevant framework cheat sheet:
- `[OWASP: Django_Security, Django_REST_Framework]` → `skills/languages/python.md`
- `[OWASP: Ruby_on_Rails]` → `skills/languages/ruby.md`
- `[OWASP: Laravel, Symfony, PHP_Configuration]` → `skills/languages/php.md`
- `[OWASP: DotNet_Security]` → `skills/languages/csharp.md`
- `[OWASP: Java_Security, JAAS, Injection_Prevention_in_Java, Bean_Validation]` → `skills/languages/java.md`
- `[OWASP: Nodejs_Security]` → `skills/languages/typescript.md`
- `[OWASP: C-Based_Toolchain_Hardening]` → `skills/languages/cpp.md`

## Security — Process/Architecture (not code review tasks)
These OWASP cheat sheets inform the review system's design but aren't discrete code-level detection tasks:
- `Abuse_Case` — informs threat modeling, not code patterns
- `Attack_Surface_Analysis` — architecture-level
- `Authorization_Testing_Automation` — testing methodology
- `Automotive_Security` — domain-specific architecture
- `Drone_Security` — domain-specific architecture
- `Legacy_Application_Management` — process guidance
- `Secure_Cloud_Architecture` — architecture-level
- `Secure_Code_Review` — meta (we ARE the code review)
- `Secure_Product_Design` — design-level
- `Threat_Modeling` — process guidance
- `User_Privacy_Protection` — policy-level (PII exposure task covers code detection)
- `Virtual_Patching` — operational response

---

## Concurrency — General (5 tasks)
- ✅ [race-condition](concurrency/race-condition.md) — high — `[all platforms]`
- ✅ [deadlock](concurrency/deadlock.md) — high — `[all platforms]`
- ✅ [async-misuse](concurrency/async-misuse.md) — high — `[web, microservices]`
- ✅ [thread-unsafe-collection](concurrency/thread-unsafe-collection.md) — high — `[all platforms]`
- ✅ [livelock](concurrency/livelock.md) — medium — `[all platforms]`

## Concurrency — Android (3 tasks)
- ✅ [android-main-thread-blocking](concurrency/android/main-thread-blocking.md) — high — network/DB on main thread, StrictMode violations, ANR triggers
- ✅ [android-coroutine-misuse](concurrency/android/coroutine-misuse.md) — high — wrong dispatcher (Dispatchers.Main for I/O), missing structured concurrency, leaked coroutine scopes
- ✅ [android-handler-looper](concurrency/android/handler-looper.md) — medium — posting to dead Handler, missing Looper cleanup, delayed message leaks

## Concurrency — iOS (3 tasks)
- ✅ [ios-main-thread-blocking](concurrency/ios/main-thread-blocking.md) — high — synchronous network/DB on main thread, UI updates from background
- ✅ [ios-gcd-misuse](concurrency/ios/gcd-misuse.md) — high — wrong dispatch queue, sync on main causing deadlock, missing DispatchGroup handling
- ✅ [ios-actor-isolation](concurrency/ios/actor-isolation.md) — medium — Swift concurrency: missing @MainActor, Sendable violations, data races across actors

## Concurrency — Web (2 tasks)
- ✅ [web-worker-misuse](concurrency/web/worker-misuse.md) — medium — SharedArrayBuffer without Atomics, postMessage serialization overhead, missing error handling in workers
- ✅ [web-event-loop-blocking](concurrency/web/event-loop-blocking.md) — high — long synchronous operations blocking UI, missing requestIdleCallback for heavy work

## Concurrency — Microservices (3 tasks)
- ✅ [microservices-distributed-lock](concurrency/microservices/distributed-lock.md) — high — missing TTL on distributed locks, split-brain scenarios, lock not released on failure
- ✅ [microservices-event-ordering](concurrency/microservices/event-ordering.md) — high — assuming ordered delivery from message queues, missing idempotency keys
- ✅ [microservices-thundering-herd](concurrency/microservices/thundering-herd.md) — medium — cache stampede on expiry, missing jittered backoff, synchronized retries

---

## Correctness — General (5 tasks)
- ✅ [null-deref](correctness/null-deref.md) — high — `[all platforms]`
- ✅ [off-by-one](correctness/off-by-one.md) — medium — `[all platforms]`
- ✅ [integer-overflow](correctness/integer-overflow.md) — high — `[all platforms]`
- ✅ [floating-point-comparison](correctness/floating-point-comparison.md) — medium — `[all platforms]`
- ✅ [logic-inversion](correctness/logic-inversion.md) — medium — `[all platforms]`

## Correctness — Android (3 tasks)
- ✅ [android-lifecycle-bugs](correctness/android/lifecycle-bugs.md) — high — accessing views after onDestroyView, Fragment not attached, leaking Activity references
- ✅ [android-config-change-crash](correctness/android/config-change-crash.md) — high — state lost on rotation, ViewModel not used for transient data, non-serializable in Bundle
- ✅ [android-permission-handling](correctness/android/permission-handling.md) — medium — missing runtime permission check, assuming grant, not handling denial gracefully

## Correctness — iOS (3 tasks)
- ✅ [ios-force-unwrap](correctness/ios/force-unwrap.md) — high — force unwrapping optionals (!) without guard, implicitly unwrapped optionals in production
- ✅ [ios-retain-cycle](correctness/ios/retain-cycle.md) — high — strong reference cycles in closures (missing [weak self]), delegate not weak, NotificationCenter leaks
- ✅ [ios-lifecycle-bugs](correctness/ios/lifecycle-bugs.md) — medium — UIKit access before viewDidLoad, state corruption across scene lifecycle, background task expiration

## Correctness — Web (1 task)
- ✅ [web-type-coercion](correctness/web/type-coercion.md) — medium — JavaScript type coercion bugs (==  vs ===, truthiness, NaN comparisons, string concatenation as addition)

## Correctness — Microservices (3 tasks)
- ✅ [microservices-eventual-consistency](correctness/microservices/eventual-consistency.md) — high — reading stale data across services, missing saga compensation, split-brain state
- ✅ [microservices-idempotency](correctness/microservices/idempotency.md) — high — non-idempotent handlers for retried messages, duplicate processing, missing dedup keys
- ✅ [microservices-partial-failure](correctness/microservices/partial-failure.md) — high — incomplete multi-service operations without rollback, orphaned resources

---

## Testing — General (5 tasks)
- ✅ [missing-test-coverage](testing/missing-test-coverage.md) — medium — `[all platforms]`
- ✅ [weak-assertions](testing/weak-assertions.md) — medium — `[all platforms]`
- ✅ [test-isolation](testing/test-isolation.md) — medium — `[all platforms]`
- ✅ [mock-overuse](testing/mock-overuse.md) — low — `[all platforms]`
- ✅ [flaky-test-patterns](testing/flaky-test-patterns.md) — medium — `[all platforms]`

## Testing — Android (2 tasks)
- ✅ [android-ui-test-gaps](testing/android/ui-test-gaps.md) — medium — untested UI flows, missing Espresso/Compose test rules, no screenshot tests for visual regressions
- ✅ [android-instrumentation-gaps](testing/android/instrumentation-gaps.md) — medium — missing Robolectric for unit vs instrumented, no database migration tests

## Testing — iOS (2 tasks)
- ✅ [ios-xctest-gaps](testing/ios/xctest-gaps.md) — medium — missing XCUITest for critical flows, no snapshot tests, untested async expectations
- ✅ [ios-preview-divergence](testing/ios/preview-divergence.md) — low — SwiftUI preview not matching runtime behavior, preview-only data masking bugs

## Testing — Web (2 tasks)
- ✅ [web-e2e-gaps](testing/web/e2e-gaps.md) — medium — critical user flows without E2E tests (Playwright/Cypress), no visual regression tests
- ✅ [web-accessibility-testing](testing/web/accessibility-testing.md) — medium — missing axe/WAVE assertions, no keyboard navigation tests, ARIA label coverage

## Testing — Microservices (2 tasks)
- ✅ [microservices-contract-testing](testing/microservices/contract-testing.md) — high — no Pact/consumer-driven contracts, breaking API changes without cross-service test
- ✅ [microservices-integration-gaps](testing/microservices/integration-gaps.md) — medium — mocking all external services in tests (never testing real integration), no chaos/fault injection

---

## Performance — General (4 tasks)
- ✅ [n-plus-one](performance/n-plus-one.md) — high — `[web, api, microservices]`
- ✅ [algorithmic-complexity](performance/algorithmic-complexity.md) — medium — `[all platforms]`
- ✅ [memory-leak](performance/memory-leak.md) — high — `[all platforms]`
- ✅ [unbounded-growth](performance/unbounded-growth.md) — medium — `[all platforms]`

## Performance — Android (3 tasks)
- ✅ [android-overdraw](performance/android/overdraw.md) — medium — nested backgrounds, redundant draw passes, missing clipRect optimization
- ✅ [android-bitmap-memory](performance/android/bitmap-memory.md) — high — loading full-res bitmaps into ImageView, missing Glide/Coil downsampling, Bitmap not recycled
- ✅ [android-startup-time](performance/android/startup-time.md) — medium — heavy init in Application.onCreate, synchronous disk I/O at launch, missing lazy initialization

## Performance — iOS (3 tasks)
- ✅ [ios-main-thread-work](performance/ios/main-thread-work.md) — high — image decoding/JSON parsing on main, UITableView cell height recalculation, Core Data fetch on main
- ✅ [ios-autolayout-perf](performance/ios/autolayout-perf.md) — medium — deeply nested constraint hierarchies, excessive intrinsicContentSize calls, missing stackview optimization
- ✅ [ios-large-asset-loading](performance/ios/large-asset-loading.md) — medium — loading full-res images without downsampling, missing NSCache, no progressive loading

## Performance — Web (4 tasks)
- ✅ [web-bundle-size](performance/web/bundle-size.md) — low — large bundles without tree-shaking, missing code splitting, unoptimized dependencies
- ✅ [web-unnecessary-rerender](performance/web/unnecessary-rerender.md) — medium — React/Vue re-renders from missing memoization, incorrect dependencies, prop drilling
- ✅ [web-core-web-vitals](performance/web/core-web-vitals.md) — medium — LCP/CLS/INP regressions: large images without lazy loading, layout shifts, long input delays
- ✅ [web-hydration-mismatch](performance/web/hydration-mismatch.md) — medium — SSR/client hydration mismatches causing double renders, missing Suspense boundaries

## Performance — Microservices (3 tasks)
- ✅ [microservices-latency-chain](performance/microservices/latency-chain.md) — high — sequential synchronous calls across services (waterfall), missing parallelization
- ✅ [microservices-connection-pool](performance/microservices/connection-pool.md) — high — unbounded connections, pool exhaustion under load, missing connection reuse
- ✅ [microservices-payload-bloat](performance/microservices/payload-bloat.md) — medium — over-fetching entire entities across service boundaries, missing field selection/projections

---

## Reliability — General (5 tasks)
- ✅ [error-handling](reliability/error-handling.md) — high — `[all platforms]`
- ✅ [resource-cleanup](reliability/resource-cleanup.md) — high — `[all platforms]`
- ✅ [timeout-handling](reliability/timeout-handling.md) — medium — `[all platforms]`
- ✅ [graceful-degradation](reliability/graceful-degradation.md) — medium — `[web, microservices]`
- ✅ [retry-without-backoff](reliability/retry-without-backoff.md) — medium — `[all platforms]`

## Reliability — Android (3 tasks)
- ✅ [android-process-death](reliability/android/process-death.md) — high — state lost when OS kills process, missing SavedStateHandle, non-restorable navigation state
- ✅ [android-crash-handling](reliability/android/crash-handling.md) — medium — uncaught exception handler not set, missing graceful crash recovery, no crash breadcrumbs
- ✅ [android-offline-resilience](reliability/android/offline-resilience.md) — medium — no offline queue, crashing on network unavailability, missing ConnectivityManager check

## Reliability — iOS (3 tasks)
- ✅ [ios-background-task-expiry](reliability/ios/background-task-expiry.md) — high — BGTask not completing before expiry, no expiration handler, data corruption on kill
- ✅ [ios-crash-recovery](reliability/ios/crash-recovery.md) — medium — no scene restoration, corrupted UserDefaults on crash, missing transaction boundaries in Core Data
- ✅ [ios-network-resilience](reliability/ios/network-resilience.md) — medium — no offline handling, URLSession not configured for background downloads, missing NWPathMonitor

## Reliability — Microservices (3 tasks)
- ✅ [microservices-circuit-breaker](reliability/microservices/circuit-breaker.md) — high — missing circuit breaker pattern, cascading failures from single service, no fallback
- ✅ [microservices-health-checks](reliability/microservices/health-checks.md) — medium — liveness/readiness probes missing or misconfigured, health check not testing dependencies
- ✅ [microservices-dead-letter-queue](reliability/microservices/dead-letter-queue.md) — medium — failed messages silently dropped, no DLQ monitoring, no poison pill handling

---

## API Design — General (4 tasks)
- ✅ [input-validation](api-design/input-validation.md) — high `[OWASP: Input_Validation, Bean_Validation]` — `[all platforms]`
- ✅ [inconsistent-response-shape](api-design/inconsistent-response-shape.md) — medium — `[web, api, microservices]`
- ✅ [breaking-api-change](api-design/breaking-api-change.md) — high — `[all platforms]`
- ✅ [missing-pagination](api-design/missing-pagination.md) — medium — `[web, api, microservices]`

## API Design — Mobile (3 tasks)
- ✅ [mobile-offline-sync](api-design/mobile/offline-sync.md) — high — no conflict resolution for offline edits, missing last-write-wins vs CRDT strategy, sync race conditions
- ✅ [mobile-api-versioning](api-design/mobile/api-versioning.md) — high — no backward compat for older app versions in the wild, forced update without grace period
- ✅ [mobile-excessive-data-fetch](api-design/mobile/excessive-data-fetch.md) — medium — downloading full payloads on cellular, missing pagination/field selection for mobile clients

## API Design — Microservices (3 tasks)
- ✅ [microservices-api-contract](api-design/microservices/api-contract.md) — high — no OpenAPI/protobuf schema, breaking changes without version bump, missing deprecation notices
- ✅ [microservices-coupling](api-design/microservices/coupling.md) — medium — shared database between services, point-to-point REST instead of events, tight temporal coupling
- ✅ [microservices-error-propagation](api-design/microservices/error-propagation.md) — medium — raw upstream errors exposed to clients, missing error mapping/wrapping at boundaries

---

## Data — General (4 tasks)
- ✅ [pii-exposure](data/pii-exposure.md) — critical `[OWASP: User_Privacy_Protection]` — `[all platforms]`
- ✅ [migration-safety](data/migration-safety.md) — high `[OWASP: Database_Security]` — `[web, api]`
- ✅ [serialization-mismatch](data/serialization-mismatch.md) — medium — `[all platforms]`
- ✅ [schema-validation](data/schema-validation.md) — medium — `[web, api, microservices]`

## Data — Android (2 tasks)
- ✅ [android-room-migration](data/android/room-migration.md) — high — destructive Room migration, missing Migration objects, schema hash mismatch crashes
- ✅ [android-content-provider-exposure](data/android/content-provider-exposure.md) — high — exported ContentProvider leaking app data, missing URI permission grants

## Data — iOS (2 tasks)
- ✅ [ios-coredata-migration](data/ios/coredata-migration.md) — high — Core Data lightweight migration failure, missing mapping model, model version mismatch crash
- ✅ [ios-coredata-threading](data/ios/coredata-threading.md) — high — NSManagedObject accessed across threads, missing performBlock, context merge conflicts

## Data — Microservices (3 tasks)
- ✅ [microservices-distributed-transaction](data/microservices/distributed-transaction.md) — high — 2PC across services (fragile), missing saga pattern, no compensation on failure
- ✅ [microservices-data-ownership](data/microservices/data-ownership.md) — medium — multiple services writing to same table, unclear source of truth, sync conflicts
- ✅ [microservices-schema-evolution](data/microservices/schema-evolution.md) — medium — breaking schema changes in shared events/topics, no Avro/protobuf evolution rules

---

## Observability — General (3 tasks)
- ✅ [logging-gaps](observability/logging-gaps.md) — medium `[OWASP: Logging, Logging_Vocabulary]` — `[all platforms]`
- ✅ [missing-metrics](observability/missing-metrics.md) — medium — `[web, api, microservices]`
- ✅ [missing-tracing](observability/missing-tracing.md) — medium — `[microservices]`

## Observability — Android (2 tasks)
- ✅ [android-crash-reporting](observability/android/crash-reporting.md) — medium — missing crashlytics/sentry integration, no breadcrumbs, obfuscated stacktraces without ProGuard mapping
- ✅ [android-anr-detection](observability/android/anr-detection.md) — medium — no ANR monitoring, missing StrictMode in debug, no main thread watchdog

## Observability — iOS (2 tasks)
- ✅ [ios-crash-symbolication](observability/ios/crash-symbolication.md) — medium — missing dSYM upload, bitcode symbols not preserved, unsymbolicated crash logs
- ✅ [ios-metrickit-gaps](observability/ios/metrickit-gaps.md) — low — not collecting MetricKit data, missing hang rate/disk write diagnostics, no custom signpost instrumentation

## Observability — Microservices (3 tasks)
- ✅ [microservices-correlation-id](observability/microservices/correlation-id.md) — high — missing trace/correlation ID propagation across service calls, broken distributed trace
- ✅ [microservices-slo-monitoring](observability/microservices/slo-monitoring.md) — medium — no SLI/SLO definitions, missing error budget tracking, no alerting on latency percentiles
- ✅ [microservices-log-aggregation](observability/microservices/log-aggregation.md) — medium — inconsistent log format across services, no structured logging standard, missing request context

---

## Code Quality — General (4 tasks)
- ✅ [dead-code](code-quality/dead-code.md) — low — `[all platforms]`
- ✅ [naming-readability](code-quality/naming-readability.md) — low — `[all platforms]`
- ✅ [dry-violations](code-quality/dry-violations.md) — low — `[all platforms]`
- ✅ [missing-documentation](code-quality/missing-documentation.md) — low — `[all platforms]`

## Code Quality — Android (2 tasks)
- ✅ [android-accessibility](code-quality/android/accessibility.md) — medium — missing contentDescription, insufficient touch targets (<48dp), no TalkBack support
- ✅ [android-deprecated-api](code-quality/android/deprecated-api.md) — low — using deprecated APIs without migration path, missing @SuppressLint justification

## Code Quality — iOS (2 tasks)
- ✅ [ios-accessibility](code-quality/ios/accessibility.md) — medium — missing accessibilityLabel, no VoiceOver support, insufficient Dynamic Type scaling
- ✅ [ios-deprecated-api](code-quality/ios/deprecated-api.md) — low — using deprecated UIKit/Foundation APIs without availability checks, missing #available guards

## Code Quality — Web (1 task)
- ✅ [web-accessibility](code-quality/web/accessibility.md) — medium — missing ARIA labels, insufficient keyboard navigation, color contrast issues, semantic HTML violations

## Code Quality — Microservices (2 tasks)
- ✅ [microservices-api-documentation](code-quality/microservices/api-documentation.md) — medium — no OpenAPI spec, missing endpoint documentation, undocumented error codes
- ✅ [microservices-naming-conventions](code-quality/microservices/naming-conventions.md) — low — inconsistent naming across services (snake_case vs camelCase), mismatched HTTP methods

---

## Summary

| Category | Complete | Planned | Total |
|----------|----------|---------|-------|
| Security — Injection | 2 | 4 | 6 |
| Security — Auth & Session | 2 | 6 | 8 |
| Security — Data Protection | 3 | 3 | 6 |
| Security — Network & Transport | 1 | 4 | 5 |
| Security — Cookie & Client-Side | 0 | 4 | 4 |
| Security — API & GraphQL | 0 | 3 | 3 |
| Security — AI & LLM | 0 | 3 | 3 |
| Security — Supply Chain | 0 | 3 | 3 |
| Security — DoS | 0 | 2 | 2 |
| Security — Infrastructure | 0 | 5 | 5 |
| Security — Android | 0 | 8 | 8 |
| Security — iOS | 0 | 8 | 8 |
| Security — Mobile Shared | 0 | 5 | 5 |
| Security — Web-Specific | 0 | 5 | 5 |
| Security — Logging & Errors | 0 | 2 | 2 |
| Security — Microservices | 0 | 7 | 7 |
| **Security Total** | **8** | **72** | **80** |
| Concurrency — General | 3 | 2 | 5 |
| Concurrency — Android | 0 | 3 | 3 |
| Concurrency — iOS | 0 | 3 | 3 |
| Concurrency — Web | 0 | 2 | 2 |
| Concurrency — Microservices | 0 | 3 | 3 |
| **Concurrency Total** | **3** | **13** | **16** |
| Correctness — General | 2 | 3 | 5 |
| Correctness — Android | 0 | 3 | 3 |
| Correctness — iOS | 0 | 3 | 3 |
| Correctness — Web | 0 | 1 | 1 |
| Correctness — Microservices | 0 | 3 | 3 |
| **Correctness Total** | **2** | **13** | **15** |
| Testing — General | 2 | 3 | 5 |
| Testing — Android | 0 | 2 | 2 |
| Testing — iOS | 0 | 2 | 2 |
| Testing — Web | 0 | 2 | 2 |
| Testing — Microservices | 0 | 2 | 2 |
| **Testing Total** | **2** | **11** | **13** |
| Performance — General | 3 | 1 | 4 |
| Performance — Android | 0 | 3 | 3 |
| Performance — iOS | 0 | 3 | 3 |
| Performance — Web | 0 | 4 | 4 |
| Performance — Microservices | 0 | 3 | 3 |
| **Performance Total** | **3** | **14** | **17** |
| Reliability — General | 2 | 3 | 5 |
| Reliability — Android | 0 | 3 | 3 |
| Reliability — iOS | 0 | 3 | 3 |
| Reliability — Microservices | 0 | 3 | 3 |
| **Reliability Total** | **2** | **12** | **14** |
| API Design — General | 1 | 3 | 4 |
| API Design — Mobile | 0 | 3 | 3 |
| API Design — Microservices | 0 | 3 | 3 |
| **API Design Total** | **1** | **9** | **10** |
| Data — General | 2 | 2 | 4 |
| Data — Android | 0 | 2 | 2 |
| Data — iOS | 0 | 2 | 2 |
| Data — Microservices | 0 | 3 | 3 |
| **Data Total** | **2** | **9** | **11** |
| Observability — General | 1 | 2 | 3 |
| Observability — Android | 0 | 2 | 2 |
| Observability — iOS | 0 | 2 | 2 |
| Observability — Microservices | 0 | 3 | 3 |
| **Observability Total** | **1** | **9** | **10** |
| Code Quality — General | 1 | 3 | 4 |
| Code Quality — Android | 0 | 2 | 2 |
| Code Quality — iOS | 0 | 2 | 2 |
| Code Quality — Web | 0 | 1 | 1 |
| Code Quality — Microservices | 0 | 2 | 2 |
| **Code Quality Total** | **1** | **10** | **11** |
| | | | |
| **Grand Total** | **24** | **173** | **197** |

Plus 7 framework-specific security references mapped to language skills, and 12 process/architecture OWASP sheets informing system design.

---

## Platform Coverage Matrix

All categories now follow strict platform subfolder structure (android/, ios/, web/, microservices/).

| Platform | Security | Concurrency | Correctness | Testing | Performance | Reliability | API Design | Data | Observability | Code Quality | **Total** |
|----------|----------|-------------|-------------|---------|-------------|-------------|------------|------|---------------|--------------|-----------|
| **Web** | 25 | 2 | 1 | 2 | 4 | — | — | — | — | 1 | **35+** |
| **Android** | 8 | 3 | 3 | 2 | 3 | 3 | — | 2 | 2 | 2 | **28** |
| **iOS** | 8 | 3 | 3 | 2 | 3 | 3 | — | 2 | 2 | 2 | **28** |
| **Mobile (shared)** | 5 | — | — | — | — | — | 3 | — | — | — | **8** |
| **Microservices** | 7 | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 2 | **32** |
| **API** | 3 | — | — | — | — | — | — | — | — | — | **3+** |
| **Infrastructure** | 5 | — | — | — | — | — | — | — | — | — | **5** |
| **General (all)** | 19 | 5 | 5 | 5 | 4 | 5 | 4 | 4 | 3 | 4 | **58** |

Counts show platform-dedicated tasks. General tasks apply across all platforms.

**Full OWASP CheatSheetSeries coverage: 100/100 cheat sheets mapped.**
**Full OWASP MASVS coverage: all 8 control groups mapped (STORAGE, CRYPTO, AUTH, NETWORK, PLATFORM, CODE, RESILIENCE, PRIVACY).**
