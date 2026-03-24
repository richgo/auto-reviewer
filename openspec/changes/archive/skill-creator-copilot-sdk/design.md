# Design: Skill Creator Copilot SDK Reuse

## Overview

This change defines a coherent planning-level contract for reusing Anthropic `skill-creator` guidance in this repository and aligning runtime guidance to a Copilot SDK-first default. The design is documentation and contract focused: it introduces explicit provenance rules, controlled refresh behavior, and runtime-language normalization without changing benchmark/tuning runtime logic in this phase.

## Architecture

### Components Affected

- `openspec/changes/skill-creator-copilot-sdk/proposal.md` — scope and intent authority for this change.
- `openspec/changes/skill-creator-copilot-sdk/specs/skill-authoring-governance/spec.md` — provenance and refresh requirements.
- `openspec/changes/skill-creator-copilot-sdk/specs/copilot-sdk-runtime-alignment/spec.md` — runtime contract requirements.
- `skills/tuning/skill-optimizer.md` — tuning-facing normative runtime and authoring guidance.
- `skills/tuning/benchmark-runner.md` — benchmark-facing normative runtime and model examples.
- `skills/tuning/local-calibration.md` — calibration guidance that may contain provider-specific wording.
- `README.md` — top-level runtime expectations and compatibility narrative.
- `agents/*/agent.md` — agent contract text where runtime assumptions may be implicit.

### New Components

- `openspec/changes/skill-creator-copilot-sdk/specs/skill-authoring-governance/spec.md`
- `openspec/changes/skill-creator-copilot-sdk/specs/copilot-sdk-runtime-alignment/spec.md`

## Technical Decisions

### Decision: Use OpenSpec Capability Deltas for Governance Contracts

**Chosen:** Introduce two explicit capability deltas (`skill-authoring-governance`, `copilot-sdk-runtime-alignment`) to encode requirements.
**Alternatives considered:**
- Keep requirements only in proposal text — rejected because they are not testable as capability contracts.
- Fold all requirements into one broad spec — rejected because provenance governance and runtime alignment evolve independently.

**Rationale:** Separate capability deltas provide clearer ownership, easier review, and direct task traceability.

### Decision: Baseline-and-Adapt Reuse Model

**Chosen:** Treat upstream `skill-creator` as a baseline reference with explicit local adaptation boundaries.
**Alternatives considered:**
- Verbatim mirror only — rejected because local repo conventions and Copilot-first runtime context require adaptation.
- Fully independent rewrite — rejected because it loses upstream alignment and increases long-term drift.

**Rationale:** Baseline-and-adapt keeps upstream value while preserving local contract clarity.

### Decision: Copilot SDK as Normative Default, Provider Examples as Labeled Alternatives

**Chosen:** Make Copilot SDK defaults normative across active docs; keep other-provider examples only when explicitly labeled.
**Alternatives considered:**
- Multi-default guidance (Copilot + Claude equal defaults) — rejected because it preserves ambiguity in operational expectations.
- Remove all non-Copilot references — rejected because historical context and optional interoperability may still be useful.

**Rationale:** A single default prevents ambiguity while preserving clearly marked compatibility context.

### Decision: Non-Normative Labeling for Historical Claude References

**Chosen:** Retain historical references only if clearly marked non-default/non-normative.
**Alternatives considered:**
- Immediate hard deletion of all references — rejected because some historical traces may still aid migration understanding.
- No labeling requirement — rejected because it causes user confusion on active runtime expectations.

**Rationale:** Labeling balances migration clarity and historical continuity.

## Data Flow

1. Maintainer identifies upstream `skill-creator` change or internal drift in skill-authoring guidance.
2. Change proposal/spec context is reviewed against the `skill-authoring-governance` requirements.
3. Documentation surfaces are updated with explicit provenance markers and adaptation boundaries.
4. Runtime-facing docs are reviewed against `copilot-sdk-runtime-alignment` requirements.
5. Copilot SDK defaults and examples are normalized; alternative provider references are labeled.
6. Coherence check verifies no contradictory normative language across README, tuning docs, and agent contracts.
7. OpenSpec artifacts remain the normative source for future follow-on implementation or automation work.

## API Changes

No external API changes.

No runtime code interface changes are required for this planning change.

## Dependencies

- External reference dependency: Anthropic `skills/skill-creator` documentation source.
- Internal contract dependencies: existing tuning/benchmark docs and OpenSpec artifact conventions.
- No new runtime libraries or service dependencies.

## Migration / Backwards Compatibility

- Existing runtime code paths remain unchanged.
- Historical Claude CLI references may remain where needed, but must be labeled non-normative after alignment.
- Documentation consumers receive a clearer default runtime contract (Copilot SDK-first) without losing optional interoperability context.

## Testing Strategy

- **Skill-Authoring Governance / Traceable Upstream Baseline:** review checklist test ensuring provenance and adaptation boundaries appear in all normative skill-authoring docs.
- **Skill-Authoring Governance / Upstream Refresh Workflow:** process test ensuring upstream refresh decisions are captured in repository change artifacts.
- **Skill-Authoring Governance / Reuse Boundary Across Surfaces:** consistency test across README, tuning docs, and agent contracts for a single skill-creator contract.
- **Copilot Runtime / Normative Runtime Guidance:** documentation test verifying active sections use Copilot SDK defaults and do not rely on unlabeled Claude CLI assumptions.
- **Copilot Runtime / Example Command Review:** command/example audit test verifying model identifiers and auth steps are Copilot-compatible.
- **Copilot Runtime / Historical Reference De-Emphasis:** label test verifying remaining Claude references are explicitly marked historical/non-default.

## Edge Cases

- Upstream source changes structure significantly; provenance references must still remain unambiguous.
- A doc requires provider-specific nuance; alternative examples must remain clearly labeled to avoid default ambiguity.
- Partial updates create split guidance; coherence checks must block completion until all normative surfaces align.
- Historical artifacts are cited by active docs; references must distinguish archival context from active contract language.

