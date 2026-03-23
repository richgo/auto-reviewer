name: api design breaking api change
description: >
  Detect breaking API changes: removal, renaming, or re-typing of fields, parameters, or response shapes without versioning or a documented deprecation period.
category: api-design
severity: high
platforms: [all]
languages: [all]

Purpose:
  - Identify code changes that alter a published API contract in a way that will break existing clients (removed fields, renamed fields, changed types, changed parameter semantics) when not accompanied by versioning, deprecation, or clear migration guidance.

Detection heuristics:
  - Diffs that remove or rename public fields, JSON keys, or endpoint paths.
  - Diffs that change parameter or response types (e.g., int → string, non-nullable → nullable) for public endpoints or published schemas.
  - Diffs that add incompatible changes to request/response shapes (reordering is fine; removing required fields or changing meanings is not).
  - Absence of version bump, route versioning (e.g., /v2/), deprecation comments, or compatibility shims alongside the change.
  - Missing migration guidance or automated compatibility tests when the API surface changes.

Actionable findings:
  - Describe the exact breaking change (file, symbol, JSON key, endpoint).
  - State why it breaks existing clients (example before vs after request/response).
  - Recommend remediation: add versioned route/schema, introduce a deprecation period, provide a compatibility adapter, or document migration with examples.
  - If acceptable (e.g., new endpoint or internal-only change), state rationale and why it is not a breaking change.

Examples:
  - Case: Breaking change (should be detected)
    - Removing or renaming a response field in a published API:
      - Before: GET /v1/items → { "items": [{ "id": int, "name": string }] }
      - After: GET /v1/items → { "items": [{ "identifier": int, "name": string }] }
      - Why it breaks: clients expecting "id" will fail; requires versioning or deprecation.
  - Counter-examples (should NOT be flagged)
    - New endpoint or truly internal change with no published contract.
    - Changes that are additive only (adding optional fields) with no type or name changes for existing fields.
    - Intentional versioned changes (e.g., introducing /v2/ with clear migration) or changes accompanied by documented deprecation and compatibility shims.
    - Local refactors that do not alter public request/response shapes or published schemas.

Eval checklist:
  - [ ] Detects removal/renaming/type changes of public fields or params
  - [ ] Flags missing versioning or deprecation when breaking changes are introduced
  - [ ] Does NOT flag new endpoints, internal-only changes, or additive non-breaking changes
  - [ ] Provides clear, actionable remediation steps

Notes:
  - Focus only on changes that affect published contracts (public routes, published SDKs, API schemas). Do not flag internal private functions or unrelated refactors.
  - Keep guidance concise: what changed, why it breaks, and how to fix it.

Migration:
  - Origin: review-tasks/api-design/breaking-api-change.md
  - Keep synchronized by re-running scripts/skills/review_task_converter_cli.py when source changes.

Platform-Specific Guidance:
  Web/API: |
    Detection cues:
      - Changes to OpenAPI/Swagger files, JSON Schema, or RAML diffs that remove/rename properties.
      - Route/path changes in server routing files (e.g., express/router, Flask app.route) that alter public paths.
      - Changes to request/response Content-Type handling or required query/body parameters.
    How to verify:
      - Generate "before" and "after" OpenAPI/JSON Schema and run a schema diff tool (e.g., schemats, openapi-diff) to list removed/renamed fields and incompatible type changes.
      - Run consumer-facing examples (curl/postman) showing the old vs new payloads.
      - Check CI for contract tests and whether they still pass.
    Remediation and rollout:
      - If incompatible, require a major (breaking) version bump in the API or add a new versioned route (/v2/) and keep v1 behavior until deprecation.
      - If rolling out a change without a new route, introduce compatibility shims (server-side adapter returning old keys) and emit deprecation headers (e.g., Warning or custom X-Deprecation-Date).
      - Provide migration docs with exact example requests/responses and add automated compatibility tests to CI.
    Tests and automation:
      - Require consumer-driven contract tests (Pact or contract tests) in PRs that touch API surfaces.
      - Gate merges on openapi/schema-diff checks and automated integration tests that exercise public endpoints.
    Quick mitigations:
      - Accept unknown fields in JSON parsing, add aliases/legacy keys for renamed fields, and feature-flag the new behavior for a staged rollout.

  Android: |
    Detection cues:
      - Changes to model classes used by Retrofit/OkHttp, kotlinx.serialization, Moshi/Gson annotations, or Parcelable/Serializable field names/types.
      - Changes in SDK client libraries published for Android (package public API, method signatures, serialized JSON keys).
      - Modifications to typed responses (e.g., int → String) or nullability annotations that affect Kotlin consumers.
    How to verify:
      - Build and run instrumentation/unit tests that use the current published SDK or client code against the updated API.
      - Deserialize sample responses with the new and old models to confirm failures (missing keys, type errors).
      - Check published SDK artifacts (AAR/Maven) for binary/semantic changes to public APIs (use API compatibility tools like japicmp or Gradle's API compatibility plugin).
    Remediation and rollout:
      - Keep deserialization tolerant: use @Json(name="newKey") with fallback logic, default values, and ignoreUnknownKeys where possible.
      - Publish a new SDK major version for breaking model changes and document migration steps in release notes and Kotlin/Java examples.
      - For field renames, support both keys for a deprecation window and log warnings for clients using legacy keys.
    Tests and automation:
      - Add matrix CI jobs that run Android unit tests against both old and new API shapes.
      - Include end-to-end smoke tests on representative Android clients in PR pipelines.
    Quick mitigations:
      - Use feature flags in server responses or add backward-compatible payloads to avoid immediate client breakage; provide explicit migration snippets for Android (Retrofit + Moshi/Gson examples).

  iOS: |
    Detection cues:
      - Changes to Codable/NSCoding model structs/classes, Objective-C-visible headers, SPM/CocoaPods public interfaces, or changes to JSON keys and nullability.
      - Alterations to library API signatures (public methods, models) that clients import.
    How to verify:
      - Decode representative JSON before/after using Swift Codable and Objective-C bridges to surface decoding errors or missing keys.
      - Run client integration tests and sample app builds against the modified API and check for runtime crashes due to unexpected nils or type mismatches.
      - Inspect published binary/headers (frameworks, module maps) for ABI/API changes.
    Remediation and rollout:
      - Make decoding resilient: implement keyed decoding with fallback keys, provide default values, and use optional properties rather than force-unwrapped values.
      - Release a new major version of any public SDK/framework for breaking changes; for server-side API changes, add transitional responses supporting both old and new keys.
      - Document migration steps with sample Swift/Objective-C code and add deprecation notices to README and SDK docs.
    Tests and automation:
      - Require CI to run unit and UI tests of sample apps against the changed API; include nightly acceptance tests on key iOS versions.
      - Use API contract tests (OpenAPI-based) and verify via a small test app that mimics the most common client usage patterns.
    Quick mitigations:
      - For renamed fields, accept both keys in server responses and update the SDK to log deprecation warnings; prefer non-breaking additive changes where possible.

  Microservices: |
    Detection cues:
      - Changes to inter-service API contracts (REST JSON schemas or gRPC/Protobuf definitions), alterations to message queues/events payloads, or modifications to event types that downstream services consume.
      - Changes to gRPC/proto field numbers, oneof groups, or required semantics that violate protobuf evolution rules.
    How to verify:
      - Diff protobuf files and ensure only additive/non-breaking changes (add new fields with new tag numbers, avoid changing or reusing tag numbers).
      - Run consumer-driven contract tests and integration test suites that include downstream services; validate that event consumers can still parse existing messages.
      - For REST, perform OpenAPI schema diffs and replay production traffic (or a subset) against the updated service in a staging environment.
    Remediation and rollout:
      - Follow schema evolution best practices: for protobuf/gRPC, never change existing tag numbers or field types in an incompatible way; mark fields deprecated rather than removing; add new fields as optional.
      - Coordinate rolling deployments and use backward-compatible changes first; when breaking changes are unavoidable, create new API endpoints or new message types and migrate consumers gradually.
      - Use feature flags, versioned event types, and adapter/translator services to bridge old and new message shapes.
    Tests and automation:
      - Enforce contract tests (Pact, consumer-driven tests) in the CI pipeline and require approval from downstream owners for changes that touch shared contracts.
      - Add CI gates that run a "dry-run" deployment of the new contract in staging and run smoke tests of all consumers.
    Observability and rollout guardrails:
      - Instrument API gateways and service meshes to emit deprecation and compatibility metrics; monitor consumer error rates, deserialization failures, and increased latency immediately after deploy.
      - Prepare rollback plans and automated circuit breakers or request-version routing in gateway to route older clients to older service versions until migration completes.

Platform-Agnostic Remediation Patterns: |
  - Always include: clear migration notes, code examples showing before/after payloads, and an explicit deprecation timeline.
  - Use semantic versioning and make breaking changes only on major releases or new route versions; enforce CI checks for schema diffs and contract tests.
  - Provide automated compatibility shims where possible and require API owners to add consumer-facing tests demonstrating continued compatibility.
  - When acceptable (internal-only or new endpoint), annotate code and docs to justify the decision and list why it is not a breaking change.

Coaching Prompts for Reviewers: |
  - "Point to the public API contract (OpenAPI/protobuf/SDK) changed by this PR and show a minimal before/after payload example."
  - "Is there a version bump, route version, or deprecation header accompanying this change? If not, ask the author to add one or implement a compatibility shim."
  - "Which consumers (internal/external SDKs, mobile apps, third-party clients) will be impacted? Request consumer-driven contract tests or owner sign-off."

Contact and escalation:
  - If multiple downstream consumers are impacted or automated mitigations are not feasible, escalate to the API owner and product manager and require a migration plan before merge.