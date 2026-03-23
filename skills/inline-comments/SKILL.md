---
name: inline comments
description: >
  Format code review findings as inline PR comments (GitHub, GitLab, Bitbucket). Each comment
  includes file path, line number, severity emoji, finding description, evidence snippet, and
  suggested fix. Optimized for PR review workflows where findings appear directly on changed lines.
---

# Output Formatter: Inline PR Comments

## Purpose
Transform code review findings into inline comments on PR diff lines. Each finding becomes a targeted comment attached to the specific line of code.

## Format Specification

### GitHub PR Comment
```markdown
**🔴 Critical: SQL Injection**

User input flows to SQL query without parameterization.

**Evidence:**
```python
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)
```

**Fix:**
```python
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

**Reference:** [OWASP SQL Injection Prevention](https://owasp.org/...)
```

### GitLab Comment Format
```markdown
🔴 **SQL Injection** (Critical)

User input `user_id` is directly interpolated into SQL query.

```suggestion
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

[OWASP Reference](https://owasp.org/...)
```

### Bitbucket Comment Format
```markdown
**[CRITICAL] SQL Injection**

Direct string interpolation in SQL query allows injection attacks.

Vulnerable code:
```
query = f"SELECT * FROM users WHERE id = {user_id}"
```

Suggested fix:
```
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```
```

## Generation Logic

### Step 1: Map Finding to Line
```python
def create_inline_comment(finding, platform='github'):
    comment = {
        'path': finding.file,
        'line': finding.line,
        'side': 'RIGHT',  # Comment on new code
        'body': format_comment_body(finding, platform)
    }
    return comment
```

### Step 2: Format Comment Body
```python
def format_comment_body(finding, platform):
    severity_emoji = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '⚪'
    }
    
    emoji = severity_emoji[finding.severity]
    
    if platform == 'github':
        return f"""**{emoji} {finding.severity.title()}: {finding.title}**

{finding.description}

**Evidence:**
```{finding.language}
{finding.code_snippet}
```

**Fix:**
```{finding.language}
{finding.fix_suggestion}
```

**Reference:** {finding.reference}"""
    
    elif platform == 'gitlab':
        return f"""{emoji} **{finding.title}** ({finding.severity.title()})

{finding.description}

```suggestion
{finding.fix_suggestion}
```

[Reference]({finding.reference})"""
```

### Step 3: Batch Comments API Call
```python
# GitHub
comments = [create_inline_comment(f, 'github') for f in findings]
github_api.create_review(pr_number, comments=comments, event='COMMENT')

# GitLab
for comment in comments:
    gitlab_api.create_discussion(mr_id, comment)
```

## Severity Formatting

| Severity | Emoji | GitHub | GitLab | Bitbucket |
|----------|-------|--------|--------|-----------|
| Critical | 🔴 | `**🔴 Critical**` | `🔴 **Title** (Critical)` | `[CRITICAL]` |
| High | 🟠 | `**🟠 High**` | `🟠 **Title** (High)` | `[HIGH]` |
| Medium | 🟡 | `**🟡 Medium**` | `🟡 **Title** (Medium)` | `[MEDIUM]` |
| Low | ⚪ | `**⚪ Low**` | `⚪ **Title** (Low)` | `[LOW]` |

## Grouping Strategy

### Option 1: One Comment Per Finding
- Simple, clear
- Can be noisy if many findings on same file

### Option 2: Group by File
- Post summary comment at file level
- List all findings in one comment

### Option 3: Group by Severity
- Post critical/high inline
- Group medium/low in summary comment

## Adversarial Metadata

- include finding confidence in each inline comment body.
- include short debate rationale when a finding is challenged or contested.
- include skill attribution in each inline comment so findings are traceable to the producing skills.

## Special Cases

### Multi-Line Findings
```python
# Span across lines
comment = {
    'path': finding.file,
    'start_line': finding.start_line,
    'line': finding.end_line,
    'side': 'RIGHT'
}
```

### Deleted Lines
```python
# Comment on old code (deletion)
comment = {
    'path': finding.file,
    'line': finding.line,
    'side': 'LEFT'  # Left side of diff
}
```

## Related Skills
- **review-orchestrator** — invokes this skill to format output
- **review-report** — alternative output format (summary)

## Quick Checklist
- [ ] Comments attached to correct line numbers
- [ ] Severity emoji included
- [ ] Code snippets syntax-highlighted
- [ ] Fix suggestions provided
- [ ] OWASP references linked
- [ ] Platform-specific formatting (GitHub/GitLab/Bitbucket)
