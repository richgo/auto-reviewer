# Proposal: Skills from Tasks

## Intent

Transform the 197 atomic review tasks (Phase 0 deliverable) into composable, deployable **skills** that can be used by LLM-based code review agents. Skills group related tasks by concern area, language, output format, and orchestration needs, enabling modular and maintainable code review automation.

## Scope

### In Scope
- Compose 19 concern-based skills covering all 10 task categories (Security with 10 sub-skills, Concurrency, Correctness, Testing, Performance, Reliability, API Design, Data, Observability, Code Quality)
- Create 11 language-specific skills (Python, TypeScript, Java, Kotlin, Swift, Go, Rust, C#, C++, Ruby, PHP) incorporating framework-specific security and idiom guidance
- Build 5 output format skills (review-report, inline-comments, fix-pr, create-issues, slack-summary) for different consumption patterns
- Implement 2 core orchestration skills (review-orchestrator, diff-analysis) for workflow coordination
- Develop 3 tuning skills (skill-optimizer, benchmark-runner, local-calibration) for continuous improvement
- Create eval infrastructure (evals.json files) with test cases, counter-examples, and assertions for each concern skill
- Follow progressive disclosure pattern: skills under 500 lines with references/ for additional detail

### Out of Scope
- Runtime implementation of skills (Phase 2: execution harness, LLM integration, GitHub API)
- Live deployment to GitHub App or CI/CD pipelines (Phase 3)
- Real-world testing on production repositories (Phase 3)
- Auto-fix implementation (Phase 4: code modification logic)
- Multi-model adversarial review (Phase 5)

## Approach

1. **Group review tasks by concern:** Map the 197 tasks to 19 concern skills based on semantic similarity and detection patterns
2. **Extract language-specific guidance:** Pull framework-specific security rules from OWASP (Django, Rails, Laravel, etc.) into language skills
3. **Define skill format:** Use Anthropic skill format with pushy, trigger-focused descriptions and structured markdown content
4. **Build eval infrastructure:** Extract eval cases from review tasks into structured JSON with assertions and scoring rubric
5. **Create orchestration layer:** Design review-orchestrator to dispatch concern/language skills based on diff analysis
6. **Enable progressive disclosure:** Keep skills concise with references/ subdirectories for detailed OWASP mappings, payload catalogs, and example code
7. **Design tuning loop:** Build autoresearch-style skills that can measure performance, identify weaknesses, and mutate prompts iteratively

## Impact

### Affected Areas
- `skills/` directory structure (new): concerns/, languages/, outputs/, core/, tuning/
- `evals/` directory (new): JSON files with test cases for automated validation
- `review-tasks/` (reference): skills reference task files for detailed detection logic
- Future Phase 2 runtime integration points

### Integration Points
- Skills reference `review-tasks/` files for progressive disclosure
- Evals extract test cases from review task eval sections
- Orchestrator dispatches skills based on diff analysis (language detection, changed files)
- Output skills consume findings from concern/language skills and format for different consumers

## Risks

1. **Skill bloat:** Without progressive disclosure, skills could exceed 500 lines → Mitigation: Strict references/ pattern, move OWASP mappings and payload catalogs out of main skill
2. **Eval quality:** Synthetic test cases may not reflect real-world bugs → Mitigation: Start with known CVE examples, expand with production findings in Phase 3
3. **Skill overlap:** Multiple skills may flag the same issue → Mitigation: Deduplication logic in orchestrator using finding fingerprints
4. **False positives:** Overly aggressive detection heuristics → Mitigation: Counter-examples mandatory for each eval case, tuning loop to optimize precision
5. **Maintenance burden:** 40 skills across 5 categories → Mitigation: Clear ownership model, automated testing via benchmark-runner

## Open Questions

1. Should language skills include framework detection heuristics (e.g., auto-detect Django vs Flask from imports)?
   - **Resolution:** Yes — language skills should detect framework and apply framework-specific rules. Framework detection in diff-analysis skill.

2. How to handle skill version evolution and backward compatibility?
   - **Resolution:** Defer to Phase 2. Initial version is v1, breaking changes trigger new major version. Skills are stateless so no migration concerns.

3. What's the right balance between specificity (narrow detection) and generalization (broader patterns)?
   - **Resolution:** Start specific (mirror review tasks closely), tune for generalization in Phase 3 based on false positive rate.

4. Should skills be language-agnostic where possible, or always language-specific?
   - **Resolution:** Concern skills are language-agnostic with language subsections for platform-specific patterns. Language skills are always language-specific.

5. How to handle platform detection (Android vs iOS vs web)?
   - **Resolution:** diff-analysis skill extracts platform signals (file extensions, framework imports, manifest files). Orchestrator routes to platform-specific subsections in concern skills.
