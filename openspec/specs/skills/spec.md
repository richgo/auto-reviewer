# Skills Specification

## Requirements

### Requirement: Skill Format

The system SHALL define each active skill as a folder whose name is the canonical skill identifier and whose entry file is `SKILL.md`.

#### Scenario: Canonical Skill Folder Contract

- GIVEN a skill is part of the active corpus
- WHEN its on-disk structure is validated
- THEN the skill SHALL exist in a folder named exactly for that skill identifier
- AND the folder SHALL include `SKILL.md` as the canonical entry file
- AND active runtime discovery SHALL resolve through this folder contract.

#### Scenario: Skill File Structure (Legacy Reference)

- GIVEN a skill needs to be created for code review
- WHEN writing the skill file
- THEN it SHALL include YAML frontmatter with: name, description (pushy, trigger-focused mentioning specific patterns and contexts)
- AND it SHALL include markdown content with detection logic, examples, and fix guidance
- AND the total file size SHALL be under 500 lines of markdown

### Requirement: Skill-Owned Review Guidance

The system SHALL keep active review guidance in canonical skill folders and remove active dependence on legacy file-shaped skill representations.

#### Scenario: Guidance Resolution Through Canonical Skills

- GIVEN review execution resolves guidance for a capability
- WHEN active sources are loaded
- THEN guidance SHALL be resolved from canonical skill folders
- AND active resolution SHALL not require legacy file-based skill placement.

### Requirement: Progressive Disclosure

The system SHALL use references/ subdirectories for detailed content exceeding the 500-line skill limit.

#### Scenario: References Structure

- GIVEN a skill has detailed content (OWASP mappings, payload catalogs, extensive examples) that would exceed 500 lines
- WHEN organizing the skill content
- THEN detailed content SHALL be moved to a references/ subdirectory next to the skill
- AND the skill SHALL reference these files explicitly for progressive disclosure
- AND references SHALL be optional — skills under 500 lines do not require them

### Requirement: Concern Skill Organization

The system SHALL group review concerns by concern area into composable skills.

#### Scenario: Concern Categories

- GIVEN the Phase 0 research corpus
- WHEN creating concern skills
- THEN they SHALL be organized into 19 skills: 10 security sub-skills (injection, auth, data-protection, network, client-side, api, ai-llm, supply-chain, mobile, infrastructure), plus concurrency, correctness, testing, performance, reliability, api-design, data-integrity, observability, code-quality
- AND each skill SHALL contain detailed detection logic

### Requirement: Language Skill Organization

The system SHALL provide language-specific guidance including framework security and idioms.

#### Scenario: Language Coverage

- GIVEN developers work in multiple programming languages
- WHEN creating language skills
- THEN they SHALL cover: Python, TypeScript, Java, Kotlin, Swift, Go, Rust, C#, C++, Ruby, PHP
- AND each language skill SHALL incorporate framework-specific security rules from OWASP (e.g., Django for Python, Rails for Ruby)
- AND each skill SHALL include language-specific pitfalls, idioms, and anti-patterns

### Requirement: Output Skill Organization

The system SHALL format review findings for different consumption patterns.

#### Scenario: Output Formats

- GIVEN findings need to be delivered to different consumers
- WHEN creating output skills
- THEN they SHALL include: review-report (comprehensive Markdown PR comment), inline-comments (individual GitHub/GitLab comments), fix-pr (auto-fix PR generation), create-issues (GitHub issue creation), slack-summary (brief notification)
- AND output skills SHALL consume findings from concern/language skills and transform them to the target format

### Requirement: Core Orchestration Skills

The system SHALL coordinate the review workflow via orchestration skills.

#### Scenario: Orchestrator Components

- GIVEN the review process needs coordination
- WHEN creating core skills
- THEN they SHALL include: review-orchestrator (main workflow: parse diff, dispatch skills, aggregate findings, dedupe, rank), diff-analysis (parse PR diffs, extract changed sections, detect languages/platforms)
- AND the orchestrator SHALL route work to appropriate concern/language skills based on diff analysis

### Requirement: Tuning Skills

The system SHALL enable continuous improvement via autoresearch-based tuning.

#### Scenario: Tuning Components

- GIVEN skills need optimization over time
- WHEN creating tuning skills
- THEN they SHALL include: skill-optimizer (autoresearch loop: read eval failures, mutate prompts, re-evaluate), benchmark-runner (run skills against eval cases, score precision/recall/F1), local-calibration (adapt skills to repo-specific conventions)
- AND tuning skills SHALL operate on skill files directly (read, modify, test, commit)


### Requirement: Skill Naming Convention

The system SHALL use flattened, explicit skill identifiers for nested lineage and enforce one canonical identifier per active skill.

#### Scenario: Flattened Name Resolution

- GIVEN a nested skill lineage exists (for example `api-design/mobile`)
- WHEN canonical identifiers are derived
- THEN the active skill identifier SHALL be flattened to an explicit name preserving lineage semantics (for example `api-design-mobile`)
- AND nested folder hierarchy SHALL not be required for active skill identity.

#### Scenario: Canonical Duplicate Merge

- GIVEN multiple source artifacts resolve to the same flattened active skill identifier
- WHEN canonicalization is validated
- THEN those artifacts SHALL be represented by one active skill folder and one canonical `SKILL.md`
- AND active contracts SHALL treat that canonical artifact as the sole source of truth.

#### Scenario: Naming Pattern (Legacy Reference)

- GIVEN a skill file is created
- WHEN naming the file
- THEN concern skills SHALL use hyphenated lowercase (security-injection.md, api-design.md)
- AND language skills SHALL use language name (python.md, typescript.md)
- AND skill subdirectories SHALL mirror this pattern (security-injection/ for references)


### Requirement: Platform-Specific Subsections

The system SHALL include platform-specific guidance within concern skills.

#### Scenario: Platform Subsections

- GIVEN a concern skill covers multiple platforms
- WHEN writing the skill content
- THEN it SHALL include subsections for platform-specific patterns (Android, iOS, web, microservices) where applicable
- AND the diff-analysis skill SHALL detect the platform and the orchestrator SHALL route accordingly
- AND platform subsections SHALL include platform-specific guidance

### Requirement: Canonical Skill Front Matter Ownership

The system SHALL maintain one canonical front matter block per active skill, owned by the canonical `SKILL.md`.

#### Scenario: Front Matter Consolidation

- GIVEN multiple source artifacts contribute to one canonical skill identifier
- WHEN metadata ownership is validated
- THEN the canonical `SKILL.md` SHALL contain the authoritative front matter for that skill
- AND active contracts SHALL not rely on competing front matter definitions outside the canonical folder.

### Requirement: Manual Conflict Error Reporting

The system SHALL make non-mergeable canonicalization conflicts explicit for manual remediation.

#### Scenario: Non-Mergeable Content Conflict

- GIVEN source artifacts targeting one canonical skill cannot be safely unified
- WHEN canonicalization checks are performed
- THEN each conflict SHALL be reported as a manual-fix error with impacted skill identifier context
- AND the conflict SHALL remain visible until manually resolved.

### Requirement: Skill Atomicity for Tuning and Scoring

The system SHALL treat each skill as the smallest independently tuneable and benchmarkable review unit.

#### Scenario: Skill-Scoped Tuning Targets

- GIVEN a tuning run is planned
- WHEN optimization targets are enumerated
- THEN targets SHALL be expressed as skill identifiers
- AND targets SHALL be expressed as skill identifiers only.

#### Scenario: Skill-Scoped Benchmark Reporting

- GIVEN benchmark execution over review capabilities
- WHEN skill/eval pairs are discovered and scored
- THEN each executable pair SHALL be keyed by skill identifier
- AND score outputs SHALL be reported at skill granularity.

### Requirement: Skill-Owned Review Guidance

The system SHALL store bug-class review guidance in skills as the canonical source for active review behavior.

#### Scenario: Migrated Guidance Availability

- GIVEN a bug class in the review coverage surface
- WHEN migration validation is performed
- THEN equivalent guidance SHALL exist in one or more skill artifacts
- AND active review behavior SHALL resolve through skill artifacts.

### Requirement: Skill-Level Coverage Preservation

The system SHALL preserve concern and platform coverage through the skill corpus.

#### Scenario: Concern and Platform Continuity

- GIVEN the set of concerns and platform-specific guidance supported before migration
- WHEN coverage is validated after migration
- THEN each concern SHALL be represented by at least one skill
- AND previously supported platform-specific guidance SHALL remain represented in skills.

### Requirement: Skill-Eval Ownership

The system SHALL associate eval datasets directly with skill identifiers.

#### Scenario: Eval Resolution by Skill

- GIVEN an eval case used by benchmark or tuning workflows
- WHEN the eval case is resolved for execution
- THEN it SHALL map to a skill identifier
- AND execution SHALL depend only on skill artifacts.

### Requirement: Skill-Level Security Reference Mapping

The system SHALL maintain security reference mappings at the skill layer.

#### Scenario: Security Reference Traceability

- GIVEN a security capability is reviewed for reference traceability
- WHEN references are inspected in the canonical review layer
- THEN relevant OWASP or equivalent security references SHALL be available through security skills
- AND reference completeness SHALL be satisfied through security skill artifacts.
