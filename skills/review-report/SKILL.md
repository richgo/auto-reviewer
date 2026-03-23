---
name: review report
description: >
  Format code review findings as a comprehensive Markdown report for PR comments. Groups findings
  by severity, provides summaries, includes code snippets and fix suggestions, and adds OWASP/
  security references. Optimized for GitHub/GitLab PR comment rendering.
---

# Output Formatter: Review Report

## Purpose
Transform aggregated code review findings into a well-formatted, actionable Markdown report suitable for posting as a PR comment.

## Report Structure

```markdown
# 🤖 Automated Code Review

## Summary
- **Critical:** X issues
- **High:** Y issues  
- **Medium:** Z issues
- **Low:** W issues

## Critical Issues 🔴

### [CATEGORY] Issue Title (file.py:42)
**Severity:** Critical  
**Category:** Security - SQL Injection

**Description:**
[Detailed explanation of the issue]

**Code:**
```language
[Affected code snippet with context]
```

**Fix:**
```language
[Suggested fix]
```

**Reference:** [OWASP Link]

---

[Repeat for each critical issue]

## High Issues 🟠
[Same structure]

## Medium Issues 🟡
[Same structure]

## Low Issues ⚪
[Same structure]

## Review Statistics
- **Files reviewed:** X
- **Lines changed:** Y
- **Issues found:** Z
- **Review time:** Ns
```

## Formatting Rules

### Adversarial Metadata
- Include a **confidence** class for each finding (`high-confidence`, `contested`, `debunked`).
- Include a **consensus** score when available from adversarial routing.
- Include a compact **debate summary** describing challenge/defense outcome for contested findings.
- Include skill attribution metadata so each finding remains traceable to contributing skills.

### 1. Emoji Usage
- 🔴 Critical severity
- 🟠 High severity
- 🟡 Medium severity
- ⚪ Low severity
- 🔒 Security issues
- ⚡ Performance issues
- 🐛 Correctness issues
- 🔄 Concurrency issues
- 📊 Code quality issues

### 2. Title Format
```
[Category] Brief Description (file.py:line)
```

Example: `[Security] SQL Injection in user query (app.py:42)`

### 3. Code Blocks
- Always specify language for syntax highlighting
- Include 2-3 lines of context if available
- Highlight the problematic line with a comment

```python
def get_user(user_id):
    # ❌ SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
```

### 4. Fix Suggestions
- Show complete working code (not just the fix)
- Use ✅ emoji to mark corrected code
- Add brief explanation of why the fix works

```python
def get_user(user_id):
    # ✅ Parameterized query prevents SQL injection
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
```

### 5. Grouping
- Group by severity first (Critical → High → Medium → Low)
- Within severity, group by file
- Within file, sort by line number

### 6. Collapsible Sections for Long Reports
If >10 findings, use collapsible details:
```markdown
<details>
<summary><b>Medium Issues (15)</b> 🟡</summary>

[Issue details here]

</details>
```

### 7. Links
- Link to OWASP cheat sheets
- Link to specific lines in the PR using GitHub/GitLab syntax
- Link to CVE databases for known vulnerabilities

## Report Generation Steps

### Step 1: Calculate Summary Stats
```python
stats = {
    'critical': len([f for f in findings if f.severity == 'critical']),
    'high': len([f for f in findings if f.severity == 'high']),
    'medium': len([f for f in findings if f.severity == 'medium']),
    'low': len([f for f in findings if f.severity == 'low']),
    'files_reviewed': len(set(f.file for f in findings)),
    'lines_changed': total_lines_changed,
    'review_time_seconds': review_duration
}
```

### Step 2: Generate Header
```markdown
# 🤖 Automated Code Review

📊 **Summary:** {critical} critical, {high} high, {medium} medium, {low} low issues found

{emoji_summary}
```

Emoji summary for quick scan:
- All green (no critical/high): ✅ Code looks good!
- Critical issues: 🚨 **Critical security issues found**
- Only high/medium: ⚠️  Issues found

### Step 3: Render Critical Issues
For each critical finding:
1. Extract code snippet from diff
2. Format with markdown code block
3. Add fix suggestion
4. Include OWASP reference
5. Add GitHub line link

### Step 4: Render Other Severities
Same process as critical, grouped by severity.

### Step 5: Add Footer
```markdown
---

## 📈 Review Statistics
- **Files reviewed:** {files_reviewed}
- **Lines changed:** {lines_changed}
- **Total issues:** {total_issues}
- **Review time:** {review_time_seconds}s

**Powered by AutoReviewer** | [Report an issue](link) | [Configure](link)
```

## Example Output

```markdown
# 🤖 Automated Code Review

📊 **Summary:** 2 critical, 1 high, 3 medium, 2 low issues found

🚨 **Critical security issues require immediate attention**

## Critical Issues 🔴

### [Security] SQL Injection in user query (app.py:42)
**Severity:** Critical 🔴  
**Category:** Security - SQL Injection

**Description:**
User input `user_id` is directly interpolated into SQL query using f-string, allowing SQL injection attacks. An attacker could inject `1 OR 1=1` to bypass authentication or `1; DROP TABLE users` to cause data loss.

**Vulnerable Code:**
```python
@app.route('/user/<user_id>')
def get_user(user_id):
    # ❌ SQL injection via f-string
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return jsonify(cursor.fetchone())
```

**Fix:**
```python
@app.route('/user/<user_id>')
def get_user(user_id):
    # ✅ Parameterized query prevents SQL injection
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    return jsonify(cursor.fetchone())
```

**Reference:** [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

---

### [Security] Hardcoded API Key (config.py:15)
**Severity:** Critical 🔴  
**Category:** Security - Secrets Exposure

**Description:**
API key hardcoded in source code. This will be committed to git history and exposed to anyone with repository access.

**Vulnerable Code:**
```python
# ❌ Secret in code
API_KEY = "sk-abc123456789"
```

**Fix:**
```python
# ✅ Load from environment
import os
API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

**Reference:** [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---

## High Issues 🟠

### [Security] Missing Authentication (app.py:38)
[Same format...]

---

## Medium Issues 🟡
[Collapsed if >5 issues]

---

## Low Issues ⚪
[Collapsed if >5 issues]

---

## 📈 Review Statistics
- **Files reviewed:** 3
- **Lines changed:** 150
- **Total issues:** 8
- **Review time:** 12s

**Powered by AutoReviewer** | [Report false positive](link) | [Configure rules](link)
```

## Special Cases

### No Issues Found
```markdown
# 🤖 Automated Code Review

✅ **No issues found!**

Your code passed all automated checks:
- ✅ No injection vulnerabilities
- ✅ No authentication/authorization issues
- ✅ No concurrency bugs detected
- ✅ No common correctness issues

📊 **Statistics:**
- Files reviewed: {count}
- Lines changed: {count}
- Review time: {seconds}s

**Note:** Automated review focuses on common security and correctness issues. Manual review is still recommended for logic and design validation.
```

### Partial Review
```markdown
# 🤖 Automated Code Review ⚠️

**Partial review:** Some analysis modules failed. Results may be incomplete.

[Standard report format]

---

**Failed modules:** concurrency-analyzer, ios-lifecycle-checks  
**Reason:** Timeout exceeded  
**Action:** Manual review recommended for concurrency and iOS lifecycle code
```

### Too Large to Review
```markdown
# 🤖 Automated Code Review

⚠️ **PR too large for automated review**

This PR contains {file_count} files and {line_count} lines of changes, which exceeds automated review limits.

**Recommendation:**
- Split into smaller PRs
- Request manual security review
- Focus automated review on high-risk files only

**High-risk files detected:**
- `auth/login.py` (authentication logic)
- `api/transactions.py` (financial operations)
- `crypto/encryption.py` (cryptographic operations)

[Show sampled findings from high-risk files]
```

## Configuration Options

Allow customization via config:
```yaml
output:
  format: review-report
  options:
    max_findings_per_severity: 10  # Collapse if exceeded
    include_code_snippets: true
    include_fix_suggestions: true
    include_references: true
    emoji_style: full  # full | minimal | none
    group_by: severity  # severity | file | category
    show_stats: true
    show_no_issues_message: true
```

## Related Skills
- **review-orchestrator** — Calls this skill to format output
- **inline-comments** — Alternative output format
- **slack-summary** — Condensed format for notifications
- **fix-pr** — Generate auto-fix PR instead of report

## Quick Checklist
- [ ] Summary with issue counts
- [ ] Critical issues highlighted
- [ ] Code snippets with syntax highlighting
- [ ] Fix suggestions provided
- [ ] OWASP references included
- [ ] GitHub line links added
- [ ] Collapsible sections for long reports
- [ ] Statistics footer
- [ ] Emoji for quick scanning
- [ ] Proper markdown rendering (tested on target platform)
