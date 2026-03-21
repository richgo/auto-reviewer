# Proposal: Composer Agent

## Intent

Build an intelligent composer agent that analyzes a repository's codebase, tech stack, and conventions, then generates a bespoke APM (Agent Programming Model) package tailored to that specific repo. This shifts from generic review skills to hyper-personalized, repo-aware code review.

## Scope

### In Scope
- Implement composer agent that scans repo for: languages, frameworks, libraries, architecture patterns, coding conventions, common anti-patterns
- Generate custom APM package with: repo-specific skills (e.g., "detect violations of our logger abstraction"), tuned detection thresholds, suppression rules for known false positives, repo-specific eval cases
- Package structure: `{repo-name}-apm/skills/`, `{repo-name}-apm/evals/`, `{repo-name}-apm/config.yaml`
- Auto-detect framework-specific rules (e.g., "this repo uses Django, enable Django-specific security checks")
- Learn from historical PR review comments (extract patterns like "always use X instead of Y")

### Out of Scope
- Deploying APM packages (manual install for Phase 4)
- Real-time regeneration of APM (one-time generation, manual refresh)
- Cross-repo learning (each repo analyzed independently)

## Approach

1. **Repo Analysis:** Composer scans: file extensions, import statements, package.json/requirements.txt/build.gradle, .eslintrc/.pylintrc/etc., git history of PR comments
2. **Pattern Extraction:** Identify: primary languages (Python 60%, TypeScript 30%, Go 10%), frameworks (Django, React, Docker), architectural style (microservices, monorepo, etc.), coding conventions (snake_case, logger usage patterns, test structure)
3. **Skill Customization:** Clone base skills from Phase 1, inject repo-specific heuristics (e.g., "flag usage of print() in this repo, suggest logger.info"), tune severity thresholds based on repo priorities, add suppression rules for known safe patterns
4. **Eval Generation:** Create repo-specific eval cases from: historical bugs (extract from closed PRs with "bug" label), framework-specific examples (Django CSRF examples for Django repos)
5. **Packaging:** Bundle as standalone APM package, include README with detected stack and customization notes

## Impact

### Affected Areas
- New `composer/` directory with composer agent skill and templates
- APM packages stored per-repo (e.g., `apm-packages/mycompany-backend/`)
- May affect orchestrator to load repo-specific APM instead of generic skills

## Risks

1. **Analysis Accuracy:** Composer may misdetect framework or conventions → Mitigation: Conservative defaults, human review of generated APM
2. **APM Bloat:** Repo-specific skills may duplicate generic skills → Mitigation: Extend generic skills, don't replace
3. **Maintenance:** APM packages may drift from upstream skill improvements → Mitigation: Versioned dependencies on base skills
4. **Privacy:** Scanning repo history may expose sensitive patterns → Mitigation: Local execution only, no telemetry

## Open Questions

1. How often should APM packages be regenerated (weekly, monthly, manual)?
2. Should composer learn from other repos in the same org?
3. How to handle monorepos with multiple languages/frameworks?
4. Should APM packages be versioned and distributed like npm packages?
