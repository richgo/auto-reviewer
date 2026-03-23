# Proposal: Skill Creator Copilot SDK Reuse

## Intent

The repository does not currently define a canonical process for reusing upstream skill-authoring guidance such as Anthropic's `skills/skill-creator`. Without that contract, contributors duplicate guidance, upstream improvements are hard to adopt consistently, and provenance becomes unclear. At the same time, several repository surfaces still encode Claude CLI-specific assumptions, which conflicts with the current Copilot SDK-first runtime direction and creates uncertainty about supported commands, auth, and model naming.

## Scope

### In Scope
- Define repository requirements for importing and reusing upstream `skill-creator` guidance with clear provenance and ownership boundaries.
- Define refresh expectations for adopting upstream changes (what gets synced, what can diverge locally, and what must be reviewed).
- Define Copilot SDK-first runtime expectations for tuning/benchmarking documentation and related workflow guidance.
- Identify and align affected repository surfaces (`skills/`, `scripts/`, `README`, and agent contract docs) so runtime language is consistent.
- Preserve provider-agnostic skill intent while making transport/auth defaults explicitly Copilot-centric.

### Out of Scope
- Implementing importer/sync automation or runtime orchestration changes in this change set.
- Reworking benchmark or tuning algorithms unrelated to skill-creator reuse and runtime-contract alignment.
- Introducing provider-specific behavior changes in review semantics.
- Publishing or distributing external packages beyond repository-internal documentation and contract alignment.

## Approach

Adopt a reuse-first governance model with explicit provenance: keep a traceable upstream baseline, define local adaptation boundaries, and require explicit review of upstream refresh decisions. In parallel, define a Copilot SDK-first operational contract for examples and defaults, while keeping skill content provider-neutral where possible. This establishes one coherent skill-authoring pathway that can absorb upstream improvements without reintroducing Claude-specific operational drift.

## Impact

This change affects contract and documentation surfaces that define how skills are authored and operated:
- `skills/tuning/` guidance (notably `skill-optimizer.md`, `benchmark-runner.md`, `local-calibration.md`)
- Runtime contract defaults and examples in `scripts/tune/` and `scripts/benchmark/` docs/config surfaces
- `README.md` runtime descriptions and model/example language
- `agents/` instructions where provider assumptions are implicit
- OpenSpec capability deltas for reuse governance and Copilot SDK alignment

## Risks

- Upstream dependency drift if external `skill-creator` guidance changes faster than local synchronization decisions.
- Confusion between “reused reference content” and “locally authoritative behavior” if provenance boundaries are unclear.
- Terminology mismatches if Copilot SDK runtime assumptions are updated in some surfaces but not all.
- Over-constraining skill authoring guidance to one provider style and accidentally reducing multi-model portability.

## Open Questions

- Should upstream `skill-creator` be preserved as a verbatim baseline plus local overlay, or fully rewritten with only conceptual alignment?
- How strict should refresh cadence be (event-driven on upstream changes versus scheduled periodic sync)?
- Which historical Claude references must remain for compatibility context, and which must be actively removed?
- What acceptance criteria should gate Copilot SDK alignment across docs/config (for example, no unlabeled Claude CLI references in normative sections)?
