# Local Calibration

## Purpose
Adapt general-purpose code review skills to a specific repository's conventions, patterns, and false positive triggers. Use this when a skill works well globally but produces false positives on your codebase.

## When to Calibrate

**Trigger conditions:**
- High false positive rate in production (skill flags safe patterns unique to your repo)
- Repo uses a specific ORM, framework, or library with unusual idioms
- Team has coding conventions that differ from common practice
- Legacy codebase with patterns that look buggy but are intentional

**Don't calibrate if:**
- False positives are from genuinely buggy code (fix the code, not the skill)
- Skill is universally underperforming (tune globally instead)
- Repo conventions are insecure (calibration would hide real bugs)

## Calibration Workflow

### 1. Collect False Positive Cases

**From production logs:**
```bash
# Extract false positive reviews from logs
grep "FALSE_POSITIVE" production-logs/*.json \
  | jq -r '.code_snippet' > false-positives.txt
```

**From manual review:**
- Tag legitimate code flagged as buggy
- Note the pattern (e.g., "CustomORM uses raw SQL but escapes internally")
- Extract minimal reproduction case

**Target: 5-10 false positive cases**

### 2. Create Local Eval Set

Create a repo-specific eval JSON in your repo:

```json
{
  "description": "Local calibration evals for MyRepo",
  "skill": "security-injection",
  "cases": [
    {
      "id": "local-orm-safe-001",
      "name": "CustomORM raw SQL (safe)",
      "description": "CustomORM.raw() escapes internally, should not be flagged",
      "code_snippet": "results = CustomORM.raw('SELECT * FROM users WHERE id = %s', user_id)",
      "language": "python",
      "expected_findings": [],
      "assertions": {
        "no_false_positive": true
      }
    },
    {
      "id": "local-legacy-pattern-001",
      "name": "Legacy auth pattern (safe)",
      "description": "Legacy @check_permission decorator handles auth, looks like bypass but isn't",
      "code_snippet": "@check_permission('admin')\ndef delete_user(user_id):\n    User.objects.get(id=user_id).delete()",
      "language": "python",
      "expected_findings": [],
      "assertions": {
        "no_false_positive": true
      }
    }
  ]
}
```

### 3. Merge with Global Evals

Combine global evals (from `evals/`) with local evals:

```bash
# Create local eval file
cat > /path/to/repo/.auto-reviewer/local-evals.json <<EOF
{
  "description": "Local calibration evals",
  "cases": [...]
}
EOF

# Merge global + local evals
jq -s '.[0].cases + .[1].cases | {cases: .}' \
  evals/security-injection.json \
  /path/to/repo/.auto-reviewer/local-evals.json \
  > merged-evals.json
```

### 4. Tune with Local Evals

Run autoresearch with merged evals:

```bash
python scripts/tune/autoresearch.py \
  --skill skills/concerns/security-injection.md \
  --evals merged-evals.json \
  --max-iterations 20 \
  --target-pass-rate 0.95 \
  --output /path/to/repo/.auto-reviewer/security-injection-local.md
```

This produces a **locally calibrated skill** that:
- Maintains global detection capability (from original evals)
- Avoids repo-specific false positives (from local evals)

### 5. Use Local Skill in Production

Configure auto-reviewer to use local skill for your repo:

```yaml
# .auto-reviewer/config.yml
skills:
  security-injection:
    path: .auto-reviewer/security-injection-local.md
    override: true  # Use local instead of global
```

## Common Calibration Patterns

### Pattern 1: Framework-Specific Safe APIs

**Problem:** Framework has a "safe by default" API that looks dangerous.

**Example:**
```python
# Django's QuerySet.raw() with %s is actually parameterized
User.objects.raw('SELECT * FROM users WHERE id = %s', [user_id])
```

**Calibration:**
- Add counter-example to local evals
- Tune skill to recognize `QuerySet.raw()` with `%s` as safe
- Skill learns to check for `.raw()` context before flagging

### Pattern 2: Legacy Authorization Pattern

**Problem:** Repo uses a custom auth decorator that global skill doesn't recognize.

**Example:**
```python
@require_role('admin')
def delete_resource(resource_id):
    # Global skill flags this as auth bypass
    Resource.objects.get(id=resource_id).delete()
```

**Calibration:**
- Document the auth pattern in local eval
- Add assertion: `no_false_positive: true` for `@require_role` decorated functions
- Tune skill to recognize custom decorator as valid auth check

### Pattern 3: Intentional Raw SQL

**Problem:** Repo uses raw SQL for performance, but with internal escaping.

**Example:**
```python
# Internal escaping layer
SafeSQL.execute("SELECT * FROM %s WHERE id = %s" % (table, user_id))
```

**Calibration:**
- Add eval case showing `SafeSQL` class
- Assert it's safe (if true!)
- Skill learns to recognize `SafeSQL` wrapper as escaping layer

### Pattern 4: Monorepo with Multiple Stacks

**Problem:** Repo has microservices in different languages with different conventions.

**Solution:**
- Create separate local eval sets per service
- Tune separate skill variants
- Configure auto-reviewer to use service-specific skills

```yaml
# .auto-reviewer/config.yml
skills:
  security-injection:
    path_mapping:
      services/api-python/: .auto-reviewer/skills/security-injection-python.md
      services/api-node/: .auto-reviewer/skills/security-injection-node.md
```

## Validation

### Before Deploying Calibrated Skill

1. **Sanity check:** Run global evals to ensure no regression
   ```bash
   # Original skill should still pass global evals
   python scripts/benchmark/runner.py \
     --skills-dir .auto-reviewer/ \
     --evals-dir evals/
   ```

2. **False positive test:** Run on known false positive cases
   ```bash
   # Check that calibration fixed false positives
   python scripts/tune/autoresearch.py \
     --skill .auto-reviewer/security-injection-local.md \
     --evals local-evals.json \
     --max-iterations 1
   # Should show 100% pass rate on no_false_positive assertions
   ```

3. **A/B test in production:**
   - Deploy calibrated skill to 10% of reviews
   - Monitor false positive rate vs. global skill
    - Full rollout if FP rate drops without missing real bugs

### Workflow Permission Behavior

If GitHub Actions lacks `contents: write` or `pull-requests: write`, tuning runs should still produce benchmark and history artifacts but skip promotion with explicit failed status. This keeps local calibration evidence available without silent promotion failures.

## Maintenance

### When to Re-calibrate

- New false positive pattern emerges in production
- Framework/library upgraded with new safe APIs
- Repo conventions change (team adopts new patterns)

### Keeping Global Skills Updated

**Important:** Don't let calibration diverge too much from global skills.

- Periodically merge global skill updates into local skill
- Re-run calibration tuning after global skill changes
- Contribute generalizable patterns back to global evals

```bash
# Update local skill with global changes
git diff upstream/main skills/concerns/security-injection.md \
  | patch .auto-reviewer/security-injection-local.md

# Re-tune
python scripts/tune/autoresearch.py \
  --skill .auto-reviewer/security-injection-local.md \
  --evals merged-evals.json \
  --max-iterations 10
```

## Best Practices

### Documentation
- Document why each local eval case exists (link to PR, incident, or design doc)
- Explain the repo-specific pattern being whitelisted
- Ensure it's actually safe (get security review if unsure)

### Team Alignment
- Share calibrated skills across team (commit to repo)
- Review local evals like you review code (PR process)
- Don't silently whitelist patterns without explanation

### Security Hygiene
- Never calibrate to suppress real bugs
- If a pattern is unsafe, fix the code, don't tune the skill
- Escalate if unsure whether pattern is safe

## Example: Full Calibration Session

**Scenario:** Django repo with custom ORM wrapper causing false positives.

```bash
# 1. Collect false positives
grep "SQL injection" production-reviews.json \
  | jq -r '.code_snippet' > fps.txt

# 2. Create local eval
cat > .auto-reviewer/local-evals.json <<EOF
{
  "cases": [
    {
      "id": "safe-orm-001",
      "description": "CustomORM.query() escapes internally",
      "code_snippet": "CustomORM.query('SELECT * FROM users WHERE id = %s', user_id)",
      "language": "python",
      "expected_findings": [],
      "assertions": {"no_false_positive": true}
    }
  ]
}
EOF

# 3. Merge evals
jq -s '.[0].cases + .[1].cases | {cases: .}' \
  evals/security-injection.json \
  .auto-reviewer/local-evals.json \
  > merged.json

# 4. Tune
python scripts/tune/autoresearch.py \
  --skill skills/concerns/security-injection.md \
  --evals merged.json \
  --max-iterations 20 \
  --output .auto-reviewer/security-injection-local.md

# 5. Validate
python scripts/benchmark/runner.py \
  --skills-dir .auto-reviewer/ \
  --evals-dir .auto-reviewer/ \
  --models claude-sonnet-4-20250514
# Check: no_false_positive assertions pass

# 6. Deploy
# Configure auto-reviewer to use .auto-reviewer/security-injection-local.md

# 7. Monitor
# Track FP rate over next week
# Ensure no regressions in bug detection
```

## Related
- `skill-optimizer.md` — Tune skills globally
- `benchmark-runner.md` — Compare skill performance
