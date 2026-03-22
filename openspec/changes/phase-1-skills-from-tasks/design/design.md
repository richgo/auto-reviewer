# Design: Skills from Tasks

> Historical note: This phase design is retained for audit continuity and is non-normative in the current skill-first architecture.

## Overview

Phase 1 transforms 197 atomic review tasks into 40 composable skills organized by concern (19), language (11), output format (5), orchestration (2), and tuning (3). Skills follow the Anthropic format with progressive disclosure and are validated via structured eval infrastructure.

## Architecture

### Components Affected
- `skills/` directory structure (new) — 5 subdirectories with 40 markdown files
- `evals/` directory (new) — JSON test cases extracted from review tasks
- `review-tasks/` (historical, non-normative) — retained archive context

### New Components
- **Concern skills** (`skills/concerns/`): 19 skills grouping related review tasks
  - 10 security sub-skills covering injection, auth, data protection, network, client-side, API, AI/LLM, supply chain, mobile, infrastructure
  - 9 other concern skills covering concurrency, correctness, testing, performance, reliability, API design, data integrity, observability, code quality
- **Language skills** (`skills/languages/`): 11 skills with language-specific guidance (Python, TypeScript, Java, Kotlin, Swift, Go, Rust, C#, C++, Ruby, PHP)
- **Output skills** (`skills/outputs/`): 5 skills for formatting findings (review-report, inline-comments, fix-pr, create-issues, slack-summary)
- **Core skills** (`skills/core/`): 2 orchestration skills (review-orchestrator, diff-analysis)
- **Tuning skills** (`skills/tuning/`): 3 continuous improvement skills (skill-optimizer, benchmark-runner, local-calibration)
- **Eval infrastructure** (`evals/`): 8+ JSON files with test cases, counter-examples, assertions

## Technical Decisions

### Decision: Concern Grouping Strategy

**Chosen:** Group review tasks by semantic similarity into 19 concern skills, with 10 security sub-skills
**Alternatives considered:**
- Flat list of 197 individual skills — rejected because it's unmanageable and creates massive dispatch overhead
- Merge all security into one skill — rejected because a single security skill would exceed 2000 lines and lose focus
- Group by platform first (Android skill, iOS skill) — rejected because cross-platform concerns (SQL injection) would be duplicated

**Rationale:** Concern-based grouping keeps related detection logic together while staying under 500 lines per skill. Security is subdivided because it represents 80 of 197 tasks.

### Decision: Language Skill Approach

**Chosen:** Dedicated language skills incorporating framework-specific security (OWASP Django/Rails/Laravel cheat sheets)
**Alternatives considered:**
- Framework-specific skills (django.md, rails.md) — rejected because frameworks are bound to languages, creating unnecessary indirection
- Embed all language rules in concern skills — rejected because concern skills would become bloated and language-agnostic patterns would be lost

**Rationale:** Language skills provide a natural place for framework detection, idiom guidance, and language-specific pitfalls. They complement concern skills (which detect WHAT) by providing language context (HOW in this language).

### Decision: Output Skill Separation

**Chosen:** Separate output formatting skills (review-report, inline-comments, etc.) from concern detection skills
**Alternatives considered:**
- Embed formatting in orchestrator — rejected because different consumers need different formats (PR comment vs Slack summary)
- Have concern skills directly output formatted findings — rejected because it couples detection logic to presentation

**Rationale:** Separation of concerns: concern/language skills focus on detection, output skills focus on presentation. This enables reuse (same findings → multiple output formats).

### Decision: Progressive Disclosure via References

**Chosen:** Keep skills under 500 lines, move detailed content (OWASP mappings, payload catalogs) to references/ subdirectories
**Alternatives considered:**
- No size limit — rejected because large skills are hard to navigate and slow to load
- Hard 500-line limit with truncation — rejected because some content (comprehensive OWASP mappings) is valuable but voluminous

**Rationale:** Progressive disclosure balances readability (concise skills) with completeness (references available when needed).

### Decision: Eval Infrastructure Format

**Chosen:** Structured JSON files with test cases and assertions, organized by concern skill
**Alternatives considered:**
- Markdown tables in skill files — rejected because not machine-parsable for automated testing
- Separate Git repository for evals — rejected because synchronization burden and discoverability issues
- No formal evals — rejected because skills without tests are just documentation

**Rationale:** JSON enables automated benchmark-runner execution while remaining human-readable. Organizing by concern skill keeps test cases close to the code they validate.

### Decision: Tuning Loop Architecture

**Chosen:** Autoresearch-style tuning with skill-optimizer mutating prompts, benchmark-runner measuring performance, local-calibration adapting to repos
**Alternatives considered:**
- Manual skill iteration — rejected because it doesn't scale and doesn't capture learnings systematically
- Fine-tuning LLM weights — rejected because skill prompt tuning is faster, more interpretable, and doesn't require model retraining
- Static skills — rejected because real-world usage will reveal gaps that need addressing

**Rationale:** Autoresearch loop enables continuous improvement driven by measured performance. Skill mutations are version-controlled and auditable.

## Data Flow

1. **Review Request:** Developer opens PR → GitHub webhook fires
2. **Diff Analysis:** diff-analysis skill parses PR diff, extracts changed files, detects languages/platforms
3. **Skill Dispatch:** review-orchestrator routes to relevant concern/language skills based on diff analysis
4. **Detection:** Each skill analyzes changed code sections and emits findings
5. **Aggregation:** Orchestrator collects findings, deduplicates (fingerprinting), ranks by severity
6. **Output:** Output skill (review-report, inline-comments, etc.) formats findings for consumption
7. **Delivery:** Findings posted as PR comment, inline comments, or notification

## API Changes

No API changes — this is skill content and infrastructure. Phase 2 will define the runtime API.

## Dependencies

- Phase 0 review tasks (✅ complete, historical/non-normative archive context)
- OWASP CheatSheetSeries (external) — referenced in security skills
- Anthropic skill format spec (external) — defines skill structure

## Migration / Backwards Compatibility

Not applicable — this is the initial version. Future skill updates will follow semantic versioning in skill metadata.

## Testing Strategy

### Eval Case Coverage
- Each of 19 concern skills has 2-3 eval cases in evals/{skill}.json
- Each eval case has 1-2 counter-examples
- Assertions include: must_detect, must_not_detect, severity, additional checks

### Benchmark Execution
- benchmark-runner executes all eval cases against skills
- Reports precision, recall, F1, false positive rate per skill
- Target metrics: precision >90%, recall >80%

### Manual Review
- Spot-check skill content for accuracy
- Verify OWASP references are correct
- Test orchestrator end-to-end with sample PRs

## Edge Cases

### Skill Overlap
**Problem:** Multiple skills may flag the same issue (e.g., SQL injection detected by security-injection AND python language skill)
**Solution:** Orchestrator deduplicates findings using fingerprints (file + line + finding type hash). Prioritize concern skill findings over language skill findings for conflicts.

### Platform Detection Ambiguity
**Problem:** A `.java` file could be Android or backend server
**Solution:** diff-analysis checks for platform signals (AndroidManifest.xml, Spring annotations, etc.). If ambiguous, route to both platform subsections and let concern skills filter.

### Eval Case Realism
**Problem:** Synthetic eval cases may not reflect real bugs
**Solution:** Phase 3 will augment evals with real-world findings. For Phase 1, use known CVE examples and OWASP test cases.

### False Positive Tuning
**Problem:** Aggressive detection heuristics cause false positives
**Solution:** Counter-examples mandatory for each eval case. local-calibration learns repo-specific suppressions. skill-optimizer tunes based on false positive rate.

### Skill Versioning
**Problem:** Skills evolve — how to handle breaking changes?
**Solution:** Skills include version metadata in frontmatter. Major version bumps for breaking changes (change in detection logic). Minor version for additions (new patterns). Patch for fixes.
