# Design: Review Task Taxonomy

## Overview

The review task taxonomy defines 197 atomic, testable code review concerns organized by category and platform, each with structured eval cases and OWASP mappings. This is the foundational layer for all downstream work (skills, evals, benchmarks).

## Architecture

### Components Affected
- `review-tasks/` directory structure (new)
- OWASP CheatSheetSeries integration (reference mapping)
- Eval infrastructure groundwork (structured test cases)

### New Components
- `review-tasks/INDEX.md` — master index with platform coverage matrix and OWASP mapping
- `review-tasks/TEMPLATE.md` — standardized task file template
- 197 task markdown files organized by category and platform
- 10 top-level concern categories with platform subfolders

## Technical Decisions

### Decision: Markdown Files Over Database

**Chosen:** Markdown files in Git
**Alternatives considered:**
- Database schema with task records — rejected because version control, diffability, and human readability are critical for a taxonomy that will evolve over time
- JSON/YAML config files — rejected because markdown provides better readability and supports rich documentation

**Rationale:** Git-tracked markdown enables easy collaboration, PR review of new tasks, and natural integration with skill references.

### Decision: Platform Subfolder Structure

**Chosen:** Strict platform subfolders (android/, ios/, web/, microservices/) with universal tasks at category root
**Alternatives considered:**
- Flat structure with platform tags — rejected because discoverability is poor and it's unclear what's universal vs platform-specific
- Separate category folders per platform — rejected because it fragments related concerns (e.g., all security injection tasks should be navigable together)

**Rationale:** Subfolder structure enforces consistent organization while keeping related concerns grouped. Universal tasks at root make cross-platform patterns immediately visible.

### Decision: OWASP CheatSheetSeries as Single Source of Truth

**Chosen:** Map every security task to specific OWASP cheat sheets
**Alternatives considered:**
- CWE/CVE mapping — rejected because OWASP cheat sheets are more actionable and include fix guidance
- Custom security taxonomy — rejected because reinventing the wheel when OWASP already provides comprehensive, maintained guidance

**Rationale:** OWASP CheatSheetSeries covers 100 cheat sheets with practical detection and remediation advice. Mapping to it ensures tasks are grounded in industry-standard security practices.

### Decision: Mobile MASVS Integration

**Chosen:** Tag mobile security tasks with MASVS control groups (STORAGE, CRYPTO, AUTH, NETWORK, PLATFORM, CODE, RESILIENCE, PRIVACY)
**Alternatives considered:**
- Generic security categories — rejected because mobile platforms have unique concerns (Keychain, Content Providers, ATS) not addressed by web-centric frameworks

**Rationale:** MASVS (Mobile Application Security Verification Standard) is the OWASP standard for mobile app security. Aligning with it ensures comprehensive mobile coverage.

### Decision: Eval Cases as Inline Examples

**Chosen:** Include 2-3 eval cases and 1-2 counter-examples directly in each task file
**Alternatives considered:**
- Separate eval repository — rejected because it creates synchronization burden and makes tasks less self-contained
- No eval cases — rejected because tasks without testable examples are just documentation, not a verification system

**Rationale:** Inline eval cases make tasks independently testable and provide concrete examples for skill authors. Counter-examples prevent false positives.

### Decision: Task Template Format

**Chosen:** Structured markdown with required sections: name, severity, description, heuristics, OWASP mapping, eval cases, counter-examples, fix guidance, platforms
**Alternatives considered:**
- Freeform markdown — rejected because consistency is critical for automated processing
- Strict YAML schema — rejected because it sacrifices human readability

**Rationale:** Template balances structure (for tooling) with readability (for humans). Required sections ensure completeness without rigidity.

## Data Flow

1. **Task Creation:** Developer creates task file from TEMPLATE.md
2. **OWASP Mapping:** Task references relevant OWASP cheat sheets
3. **Eval Cases:** Buggy code examples embedded with expected findings
4. **Index Update:** INDEX.md updated with task entry and platform/category counts
5. **Skill Reference:** Phase 1 skills reference tasks for progressive disclosure

## API Changes

No API changes. This is a content and documentation structure.

## Dependencies

- OWASP CheatSheetSeries (external reference)
- OWASP MASVS (external reference for mobile tasks)
- Review-tasks/ directory structure (new)

## Migration / Backwards Compatibility

Not applicable — this is the initial version.

## Testing Strategy

- **Completeness:** Verify all 197 tasks exist per INDEX.md
- **OWASP Coverage:** Confirm all security tasks have OWASP mappings
- **Platform Distribution:** Validate platform subfolder structure is consistent across all 10 categories
- **Eval Quality:** Spot-check eval cases for clarity and testability

## Edge Cases

- **Overlap Between Categories:** Some tasks span multiple concerns (e.g., unvalidated redirects are both a security issue and an API design flaw). Decision: Primary categorization by most severe impact (security wins), with cross-references in other categories.
- **Language-Specific vs Platform-Specific:** Some tasks are both (e.g., Android Kotlin coroutine misuse). Decision: Platform subfolder is primary, language-specific guidance in language skills.
- **Framework-Specific Security:** OWASP has cheat sheets for Django, Rails, Laravel, etc. Decision: These map to language skills (python.md, ruby.md, php.md) rather than standalone tasks, since frameworks are language-bound.
