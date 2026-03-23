---
name: slack summary
description: >
  Format code review findings as a Slack message using Blocks API. Severity-grouped, collapsible
  sections, action buttons, and links to code. Used for notifying teams of code review results
  without requiring them to visit GitHub/GitLab.
---

# Output Formatter: Slack Summary

## Purpose
Format code review findings as an engaging, actionable Slack message with collapsible sections and quick action buttons.

## Message Structure

```
[HEADER]
🤖 Code Review Complete: PR #123
Status: ⚠️ 2 critical, 3 high, 5 medium issues found

[CRITICAL SECTION - Always Expanded]
🔴 Critical Issues (2)
• SQL Injection in auth.py:42
• Hardcoded API Key in config.py:15

[HIGH SECTION - Collapsed]
🟠 High Issues (3)
• XSS in api.py:105
• Missing CSRF in views.py:78
• Race condition in payment.py:220

[MEDIUM SECTION - Collapsed]
🟡 Medium Issues (5)
...

[ACTIONS]
[View Full Report] [View PR] [Create Fix PR]
```

## Slack Blocks API Format

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🤖 Code Review Complete: PR #123"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "Status: ⚠️ 2 critical, 3 high, 5 medium issues found"
      }
    },
    {
      "type": "divider"
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*🔴 Critical Issues (2)*\n• SQL Injection in `auth.py:42` <https://github.com/repo/blob/main/auth.py#L42|View>\n• Hardcoded API Key in `config.py:15` <https://github.com/repo/blob/main/config.py#L15|View>"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {"type": "plain_text", "text": "View Full Report"},
          "url": "https://github.com/repo/pull/123",
          "style": "primary"
        },
        {
          "type": "button",
          "text": {"type": "plain_text", "text": "Create Fix PR"},
          "url": "https://github.com/repo/pulls?q=is%3Aopen+is%3Apr+label%3Aauto-fix"
        }
      ]
    }
  ]
}
```

## Generation Logic

```python
def create_slack_summary(findings, pr_url):
    critical = [f for f in findings if f.severity == 'critical']
    high = [f for f in findings if f.severity == 'high']
    medium = [f for f in findings if f.severity == 'medium']
    low = [f for f in findings if f.severity == 'low']
    
    blocks = [
        # Header
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"🤖 Code Review Complete: {pr_title}"
            }
        },
        # Status summary
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": format_status_line(critical, high, medium, low)
            }
        },
        {"type": "divider"}
    ]
    
    # Critical findings (always shown)
    if critical:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": format_findings_section("🔴 Critical", critical)
            }
        })
    
    # High findings (collapsible in Slack via details/summary pattern - not native)
    if high:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": format_findings_section("🟠 High", high)
            }
        })
    
    # Actions
    blocks.append({
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "View Full Report"},
                "url": pr_url,
                "style": "primary"
            }
        ]
    })
    
    return {"blocks": blocks}

def format_findings_section(title, findings):
    lines = [f"*{title} Issues ({len(findings)})*"]
    for f in findings[:5]:  # Limit to 5 per section
        lines.append(f"• {f.title} in `{f.file}:{f.line}` <{f.url}|View>")
    if len(findings) > 5:
        lines.append(f"_...and {len(findings) - 5} more_")
    return "\n".join(lines)
```

## Status Line Formatting

```python
def format_status_line(critical, high, medium, low):
    parts = []
    if critical:
        parts.append(f"🔴 {len(critical)} critical")
    if high:
        parts.append(f"🟠 {len(high)} high")
    if medium:
        parts.append(f"🟡 {len(medium)} medium")
    if low:
        parts.append(f"⚪ {len(low)} low")
    
    if not parts:
        return "Status: ✅ No issues found!"
    
    return "Status: ⚠️ " + ", ".join(parts) + " issues found"
```

## Notification Strategy

### When to Send
- **Always:** Critical/high findings
- **Configurable:** Medium/low findings
- **Never:** If no critical/high and medium/low disabled

### Channel Routing
- **Critical:** #security-alerts
- **High:** #code-review
- **Medium/Low:** #code-quality (optional)

## Threading
```python
# First message
response = slack_client.chat_postMessage(channel='#code-review', **message)
thread_ts = response['ts']

# Follow-up details in thread
slack_client.chat_postMessage(
    channel='#code-review',
    thread_ts=thread_ts,
    text="Detailed findings: ..."
)
```

## Related Skills
- **review-orchestrator** — invokes this for team notifications
- **review-report** — full detailed report
- **inline-comments** — PR-specific comments

## Quick Checklist
- [ ] Status line with severity counts
- [ ] Critical findings always visible
- [ ] File links to GitHub/GitLab
- [ ] Action buttons included
- [ ] Threaded for details
- [ ] Channel routing by severity
