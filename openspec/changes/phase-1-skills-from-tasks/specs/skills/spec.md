# Skills Specification Delta

## ADDED Requirements

### Requirement: Skill Format

The system SHALL define skills following the Anthropic skill format with YAML frontmatter and markdown content.

#### Scenario: Skill File Structure

- GIVEN a skill needs to be created for code review
- WHEN writing the skill file
- THEN it SHALL include YAML frontmatter with: name, description (pushy, trigger-focused mentioning specific patterns and contexts)
- AND it SHALL include markdown content with detection logic, examples, and fix guidance
- AND the total file size SHALL be under 500 lines of markdown

### Requirement: Progressive Disclosure

The system SHALL use references/ subdirectories for detailed content exceeding the 500-line skill limit.

#### Scenario: References Structure

- GIVEN a skill has detailed content (OWASP mappings, payload catalogs, extensive examples) that would exceed 500 lines
- WHEN organizing the skill content
- THEN detailed content SHALL be moved to a references/ subdirectory next to the skill
- AND the skill SHALL reference these files explicitly for progressive disclosure
- AND references SHALL be optional — skills under 500 lines do not require them

### Requirement: Concern Skill Organization

The system SHALL group review tasks by concern area into composable skills.

#### Scenario: Concern Categories

- GIVEN the 197 review tasks from Phase 0
- WHEN creating concern skills
- THEN they SHALL be organized into 19 skills: 10 security sub-skills (injection, auth, data-protection, network, client-side, api, ai-llm, supply-chain, mobile, infrastructure), plus concurrency, correctness, testing, performance, reliability, api-design, data-integrity, observability, code-quality
- AND each skill SHALL reference the underlying review tasks for detailed detection logic

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

The system SHALL follow consistent naming for skill files.

#### Scenario: Naming Pattern

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
- AND platform subsections SHALL reference platform-specific review tasks from Phase 0
