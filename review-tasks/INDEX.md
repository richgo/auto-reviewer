# Review Task Index

## Status Legend
- ✅ Complete (has eval cases + counter-examples + assertions)
- 🔲 Planned (needs content)

## OWASP Coverage
Every task in the Security section is mapped to one or more [OWASP Cheat Sheets](https://github.com/OWASP/CheatSheetSeries). The `[OWASP: ...]` tag shows the mapping.

---

## Security — Injection (6 tasks)
- ✅ [sql-injection](security/sql-injection.md) — critical `[OWASP: SQL_Injection_Prevention, Query_Parameterization]`
- ✅ [xss](security/xss.md) — high `[OWASP: Cross_Site_Scripting_Prevention, DOM_based_XSS_Prevention]`
- 🔲 [dom-xss](security/dom-xss.md) — high `[OWASP: DOM_based_XSS_Prevention, DOM_Clobbering_Prevention]`
- 🔲 [command-injection](security/command-injection.md) — critical `[OWASP: OS_Command_Injection_Defense, Injection_Prevention]`
- 🔲 [ldap-injection](security/ldap-injection.md) — high `[OWASP: LDAP_Injection_Prevention]`
- 🔲 [nosql-injection](security/nosql-injection.md) — high `[OWASP: NoSQL_Security, Injection_Prevention]`

## Security — Authentication & Session (8 tasks)
- ✅ [auth-bypass](security/auth-bypass.md) — critical `[OWASP: Access_Control, Authorization, Insecure_Direct_Object_Reference_Prevention]`
- ✅ [csrf](security/csrf.md) — high `[OWASP: Cross-Site_Request_Forgery_Prevention]`
- 🔲 [authentication-flaws](security/authentication-flaws.md) — critical `[OWASP: Authentication, Multifactor_Authentication, Choosing_and_Using_Security_Questions]`
- 🔲 [session-management](security/session-management.md) — high `[OWASP: Session_Management]`
- 🔲 [credential-stuffing](security/credential-stuffing.md) — high `[OWASP: Credential_Stuffing_Prevention]`
- 🔲 [password-storage](security/password-storage.md) — critical `[OWASP: Password_Storage]`
- 🔲 [password-reset-flaws](security/password-reset-flaws.md) — high `[OWASP: Forgot_Password]`
- 🔲 [oauth-misconfiguration](security/oauth-misconfiguration.md) — high `[OWASP: OAuth2, SAML_Security, JSON_Web_Token_for_Java]`

## Security — Data Protection (6 tasks)
- ✅ [secrets-exposure](security/secrets-exposure.md) — critical `[OWASP: Secrets_Management, Key_Management]`
- ✅ [path-traversal](security/path-traversal.md) — critical
- ✅ [mass-assignment](security/mass-assignment.md) — high `[OWASP: Mass_Assignment]`
- 🔲 [insecure-crypto](security/insecure-crypto.md) — high `[OWASP: Cryptographic_Storage, Key_Management, TLS_Cipher_String]`
- 🔲 [insecure-deserialization](security/insecure-deserialization.md) — critical `[OWASP: Deserialization]`
- 🔲 [file-upload](security/file-upload.md) — high `[OWASP: File_Upload]`

## Security — Network & Transport (5 tasks)
- ✅ [ssrf](security/ssrf.md) — critical `[OWASP: Server_Side_Request_Forgery_Prevention]`
- 🔲 [insufficient-transport-security](security/insufficient-transport-security.md) — high `[OWASP: Transport_Layer_Security, Transport_Layer_Protection, HTTP_Strict_Transport_Security]`
- 🔲 [missing-security-headers](security/missing-security-headers.md) — medium `[OWASP: HTTP_Headers, Content_Security_Policy, Clickjacking_Defense]`
- 🔲 [cors-misconfiguration](security/cors-misconfiguration.md) — medium `[OWASP: REST_Security, AJAX_Security, HTML5_Security]`
- 🔲 [open-redirect](security/open-redirect.md) — medium `[OWASP: Unvalidated_Redirects_and_Forwards]`

## Security — Cookie & Client-Side (4 tasks)
- 🔲 [cookie-security](security/cookie-security.md) — high `[OWASP: Cookie_Theft_Mitigation, Session_Management]`
- 🔲 [clickjacking](security/clickjacking.md) — medium `[OWASP: Clickjacking_Defense]`
- 🔲 [prototype-pollution](security/prototype-pollution.md) — high `[OWASP: Prototype_Pollution_Prevention]`
- 🔲 [third-party-code](security/third-party-code.md) — medium `[OWASP: Third_Party_Javascript_Management, Securing_Cascading_Style_Sheets]`

## Security — API & GraphQL (3 tasks)
- 🔲 [graphql-security](security/graphql-security.md) — high `[OWASP: GraphQL]`
- 🔲 [rest-security](security/rest-security.md) — medium `[OWASP: REST_Security, REST_Assessment]`
- 🔲 [transaction-authorization](security/transaction-authorization.md) — high `[OWASP: Transaction_Authorization, Third_Party_Payment_Gateway_Integration]`

## Security — AI & LLM (3 tasks)
- 🔲 [prompt-injection](security/prompt-injection.md) — critical `[OWASP: LLM_Prompt_Injection_Prevention]`
- 🔲 [ai-agent-security](security/ai-agent-security.md) — high `[OWASP: AI_Agent_Security, MCP_Security, Secure_AI_Model_Ops]`
- 🔲 [mcp-tool-poisoning](security/mcp-tool-poisoning.md) — critical `[OWASP: MCP_Security]`

## Security — Supply Chain & Dependencies (3 tasks)
- 🔲 [dependency-vulnerability](security/dependency-vulnerability.md) — high `[OWASP: Software_Supply_Chain_Security, Dependency_Graph_SBOM, NPM_Security]`
- 🔲 [pinning-bypass](security/pinning-bypass.md) — high (mobile) `[OWASP: Pinning]`
- 🔲 [xml-external-entity](security/xml-external-entity.md) — high

## Security — Denial of Service (2 tasks)
- 🔲 [denial-of-service](security/denial-of-service.md) — high `[OWASP: Denial_of_Service]`
- 🔲 [regex-dos](security/regex-dos.md) — medium (ReDoS)

## Security — Infrastructure (code-level concerns) (5 tasks)
- 🔲 [docker-misconfiguration](security/docker-misconfiguration.md) — high `[OWASP: Docker_Security, NodeJS_Docker]`
- 🔲 [iac-security](security/iac-security.md) — high `[OWASP: Infrastructure_as_Code_Security, Kubernetes_Security]`
- 🔲 [cicd-security](security/cicd-security.md) — high `[OWASP: CI_CD_Security]`
- 🔲 [serverless-security](security/serverless-security.md) — medium `[OWASP: Serverless_FaaS_Security]`
- 🔲 [multi-tenant-isolation](security/multi-tenant-isolation.md) — critical `[OWASP: Multi_Tenant_Security]`

## Security — Android (8 tasks) `[OWASP: Mobile_Application_Security, MASVS]`
- 🔲 [android-insecure-storage](security/android/insecure-storage.md) — high — SharedPreferences/SQLite with plaintext secrets, world-readable files `[MASVS-STORAGE]`
- 🔲 [android-exported-components](security/android/exported-components.md) — critical — exported Activities/Services/Receivers/Providers without permission checks `[MASVS-PLATFORM]`
- 🔲 [android-intent-injection](security/android/intent-injection.md) — high — unvalidated Intent extras, implicit intents for sensitive ops `[MASVS-PLATFORM]`
- 🔲 [android-webview-security](security/android/webview-security.md) — high — JavaScript enabled, file access, universal XSS in WebView `[MASVS-PLATFORM]`
- 🔲 [android-insecure-crypto](security/android/insecure-crypto.md) — high — hardcoded keys, weak algorithms, missing Android Keystore usage `[MASVS-CRYPTO]`
- 🔲 [android-network-security](security/android/network-security.md) — high — missing network_security_config, cleartext traffic, cert validation bypass `[MASVS-NETWORK]`
- 🔲 [android-logging-sensitive-data](security/android/logging-sensitive-data.md) — medium — Log.d/Log.i with PII/tokens in release builds `[MASVS-STORAGE]`
- 🔲 [android-backup-exposure](security/android/backup-exposure.md) — medium — allowBackup=true, unencrypted auto-backup exposing app data `[MASVS-STORAGE]`

## Security — iOS (8 tasks) `[OWASP: Mobile_Application_Security, MASVS]`
- 🔲 [ios-insecure-storage](security/ios/insecure-storage.md) — high — UserDefaults/plist with secrets, missing Keychain for sensitive data `[MASVS-STORAGE]`
- 🔲 [ios-ats-bypass](security/ios/ats-bypass.md) — high — NSAllowsArbitraryLoads, NSExceptionDomains overrides disabling ATS `[MASVS-NETWORK]`
- 🔲 [ios-url-scheme-hijack](security/ios/url-scheme-hijack.md) — high — custom URL schemes without validation, universal link misconfiguration `[MASVS-PLATFORM]`
- 🔲 [ios-keychain-misuse](security/ios/keychain-misuse.md) — medium — wrong Keychain accessibility class, missing access control flags `[MASVS-CRYPTO]`
- 🔲 [ios-pasteboard-leak](security/ios/pasteboard-leak.md) — medium — sensitive data copied to system pasteboard (UIPasteboard.general) `[MASVS-STORAGE]`
- 🔲 [ios-screenshot-exposure](security/ios/screenshot-exposure.md) — low — sensitive screens not hidden during app backgrounding `[MASVS-STORAGE]`
- 🔲 [ios-insecure-crypto](security/ios/insecure-crypto.md) — high — deprecated CommonCrypto usage, ECB mode, hardcoded IVs `[MASVS-CRYPTO]`
- 🔲 [ios-jailbreak-detection-bypass](security/ios/jailbreak-detection-bypass.md) — medium — trivially bypassable jailbreak checks `[MASVS-RESILIENCE]`

## Security — Mobile Shared (5 tasks) `[OWASP: Mobile_Application_Security, Pinning, MASVS]`
- 🔲 [mobile-cert-pinning](security/mobile/cert-pinning.md) — high — missing certificate/public key pinning, bypassable implementations `[MASVS-NETWORK, Pinning]`
- 🔲 [mobile-biometric-auth-bypass](security/mobile/biometric-auth-bypass.md) — high — local-only biometric check without backend token validation `[MASVS-AUTH]`
- 🔲 [mobile-deep-link-hijack](security/mobile/deep-link-hijack.md) — high — unvalidated deep link parameters, open redirect via deep links `[MASVS-PLATFORM]`
- 🔲 [mobile-binary-hardening](security/mobile/binary-hardening.md) — medium — missing obfuscation, debug symbols in release, anti-tamper checks `[MASVS-RESILIENCE]`
- 🔲 [mobile-privacy-data-collection](security/mobile/privacy-data-collection.md) — medium — excessive permissions, tracking without consent, clipboard snooping `[MASVS-PRIVACY]`

## Security — Logging & Error Handling (2 tasks)
- 🔲 [security-error-info-leak](security/security-error-info-leak.md) — medium `[OWASP: Error_Handling]`
- 🔲 [security-logging](security/security-logging.md) — medium `[OWASP: Logging, Logging_Vocabulary]`

## Security — Microservices (7 tasks) `[OWASP: Microservices_Security, Microservices_based_Security_Arch_Doc]`
- 🔲 [microservices-auth](security/microservices/auth.md) — high — missing service-to-service auth, shared secrets between services
- 🔲 [microservices-broken-trust-boundary](security/microservices/broken-trust-boundary.md) — critical — internal APIs trusting external input, missing gateway validation
- 🔲 [microservices-data-exposure](security/microservices/data-exposure.md) — high — over-fetching across service boundaries, PII leaking between services
- 🔲 [microservices-insecure-messaging](security/microservices/insecure-messaging.md) — high — unencrypted message queues, unsigned events, replay attacks
- 🔲 [microservices-distributed-session](security/microservices/distributed-session.md) — medium — inconsistent session handling across services, JWT validation gaps
- 🔲 [microservices-service-mesh-bypass](security/microservices/service-mesh-bypass.md) — high — direct pod-to-pod calls bypassing mesh policies `[OWASP: Network_Segmentation]`
- 🔲 [microservices-cascading-failure](security/microservices/cascading-failure.md) — high — missing circuit breakers, unbounded retries causing cascading outages

## Security — Web-Specific (consolidation)
The following tasks are web-platform-specific and already listed in other sections:
- XSS, DOM XSS → Injection
- CSRF, clickjacking, CSP headers, CORS → Network & Client-Side
- Cookie security, prototype pollution, third-party JS → Cookie & Client-Side
- GraphQL, REST security → API & GraphQL
- Session management, OAuth → Auth & Session

Additional web-specific tasks:
- 🔲 [web-csp-bypass](security/web/csp-bypass.md) — medium — CSP policies with unsafe-inline/unsafe-eval, nonce misuse
- 🔲 [web-subresource-integrity](security/web/subresource-integrity.md) — medium — CDN scripts without SRI hashes
- 🔲 [web-postmessage-origin](security/web/postmessage-origin.md) — high — `postMessage` without origin validation, `window.opener` attacks
- 🔲 [web-client-side-storage](security/web/client-side-storage.md) — medium — tokens/secrets in localStorage, unencrypted IndexedDB
- 🔲 [web-html-injection](security/web/html-injection.md) — medium — user content in meta tags, link injection, form action hijack

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

## Concurrency (5 tasks)
- ✅ [race-condition](concurrency/race-condition.md) — high
- ✅ [deadlock](concurrency/deadlock.md) — high
- ✅ [async-misuse](concurrency/async-misuse.md) — high
- 🔲 [thread-unsafe-collection](concurrency/thread-unsafe-collection.md) — high
- 🔲 [livelock](concurrency/livelock.md) — medium

## Correctness (6 tasks)
- ✅ [null-deref](correctness/null-deref.md) — high
- ✅ [off-by-one](correctness/off-by-one.md) — medium
- 🔲 [type-coercion](correctness/type-coercion.md) — medium
- 🔲 [integer-overflow](correctness/integer-overflow.md) — high
- 🔲 [floating-point-comparison](correctness/floating-point-comparison.md) — medium
- 🔲 [logic-inversion](correctness/logic-inversion.md) — medium

## Testing (5 tasks)
- ✅ [missing-test-coverage](testing/missing-test-coverage.md) — medium
- ✅ [weak-assertions](testing/weak-assertions.md) — medium
- 🔲 [test-isolation](testing/test-isolation.md) — medium
- 🔲 [mock-overuse](testing/mock-overuse.md) — low
- 🔲 [flaky-test-patterns](testing/flaky-test-patterns.md) — medium

## Performance (6 tasks)
- ✅ [n-plus-one](performance/n-plus-one.md) — high
- ✅ [algorithmic-complexity](performance/algorithmic-complexity.md) — medium
- ✅ [memory-leak](performance/memory-leak.md) — high
- 🔲 [unbounded-growth](performance/unbounded-growth.md) — medium
- 🔲 [bundle-size](performance/bundle-size.md) — low
- 🔲 [unnecessary-rerender](performance/unnecessary-rerender.md) — medium

## Reliability (5 tasks)
- ✅ [error-handling](reliability/error-handling.md) — high
- ✅ [resource-cleanup](reliability/resource-cleanup.md) — high
- 🔲 [timeout-handling](reliability/timeout-handling.md) — medium
- 🔲 [graceful-degradation](reliability/graceful-degradation.md) — medium
- 🔲 [retry-without-backoff](reliability/retry-without-backoff.md) — medium

## API Design (4 tasks)
- ✅ [input-validation](api-design/input-validation.md) — high `[OWASP: Input_Validation, Bean_Validation]`
- 🔲 [inconsistent-response-shape](api-design/inconsistent-response-shape.md) — medium
- 🔲 [breaking-api-change](api-design/breaking-api-change.md) — high
- 🔲 [missing-pagination](api-design/missing-pagination.md) — medium

## Data (4 tasks)
- ✅ [pii-exposure](data/pii-exposure.md) — critical `[OWASP: User_Privacy_Protection]`
- ✅ [migration-safety](data/migration-safety.md) — high `[OWASP: Database_Security]`
- 🔲 [serialization-mismatch](data/serialization-mismatch.md) — medium
- 🔲 [schema-validation](data/schema-validation.md) — medium

## Observability (3 tasks)
- ✅ [logging-gaps](observability/logging-gaps.md) — medium `[OWASP: Logging, Logging_Vocabulary]`
- 🔲 [missing-metrics](observability/missing-metrics.md) — medium
- 🔲 [missing-tracing](observability/missing-tracing.md) — medium

## Code Quality (5 tasks)
- ✅ [dead-code](code-quality/dead-code.md) — low
- 🔲 [naming-readability](code-quality/naming-readability.md) — low
- 🔲 [dry-violations](code-quality/dry-violations.md) — low
- 🔲 [missing-documentation](code-quality/missing-documentation.md) — low
- 🔲 [accessibility](code-quality/accessibility.md) — medium

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
| Concurrency | 3 | 2 | 5 |
| Correctness | 2 | 4 | 6 |
| Testing | 2 | 3 | 5 |
| Performance | 3 | 3 | 6 |
| Reliability | 2 | 3 | 5 |
| API Design | 1 | 3 | 4 |
| Data | 2 | 2 | 4 |
| Observability | 1 | 2 | 3 |
| Code Quality | 1 | 4 | 5 |
| **Grand Total** | **24** | **99** | **123** |

Plus 7 framework-specific security references mapped to language skills, and 12 process/architecture OWASP sheets informing system design.

---

## Platform Coverage Matrix

Shows which review tasks apply to each platform. ● = primary, ○ = applicable.

| Platform | Security Tasks | Key Concerns |
|----------|---------------|--------------|
| **Web** | XSS, DOM XSS, CSRF, clickjacking, CSP, CORS, cookies, prototype pollution, third-party JS, postMessage, SRI, client-side storage, HTML injection, session management, OAuth | 20+ dedicated tasks |
| **Android** | exported components, intent injection, WebView, insecure storage (SharedPrefs/SQLite), network_security_config, logging, backup exposure, crypto (Keystore) | 8 dedicated + 5 shared mobile |
| **iOS** | ATS bypass, URL scheme hijack, Keychain misuse, pasteboard leak, screenshot exposure, insecure crypto (CommonCrypto), jailbreak detection, insecure storage (UserDefaults) | 8 dedicated + 5 shared mobile |
| **Mobile (shared)** | cert pinning, biometric auth bypass, deep link hijack, binary hardening, privacy/data collection | 5 cross-platform tasks |
| **Microservices** | service auth, trust boundaries, data exposure, message queue security, distributed sessions, service mesh bypass, cascading failures | 7 dedicated tasks |
| **API** | GraphQL, REST security, transaction authorization, input validation, mass assignment, auth bypass (BOLA/IDOR) | 6+ tasks across sections |
| **Infrastructure** | Docker, IaC/K8s, CI/CD, serverless, multi-tenant | 5 dedicated tasks |

**Full OWASP CheatSheetSeries coverage: 100/100 cheat sheets mapped.**
**Full OWASP MASVS coverage: all 8 control groups mapped (STORAGE, CRYPTO, AUTH, NETWORK, PLATFORM, CODE, RESILIENCE, PRIVACY).**
