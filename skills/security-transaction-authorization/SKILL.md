---
name: security transaction authorization
description: >
  Migrated review-task skill for Transaction Authorization Flaws. Use this skill
  whenever diffs may introduce security issues on web, api, especially in all. Actively
  look for: Transaction authorization flaws occur when sensitive operations (money
  transfers, password changes, privilege escalation) lack step-up authentication,
  confirmation mechanisms,... and report findings with high severity expectations and
  actionable fixes.
---

# Transaction Authorization Flaws

## Source Lineage
- Original review task: `review-tasks/security/transaction-authorization.md`
- Migrated skill artifact: `skills/review-task-security-transaction-authorization/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `web, api`
- Languages: `all`

## Purpose
Transaction authorization flaws occur when sensitive operations (money transfers, password changes, privilege escalation) lack step-up authentication, confirmation mechanisms, or secondary authorization checks beyond initial session authentication.

## Detection Heuristics
- Financial transactions without MFA or re-authentication
- Missing confirmation step for destructive actions (delete account, transfer funds)
- No transaction signing or out-of-band verification
- Privilege changes without additional authorization
- High-value operations using only session cookie auth

## Eval Cases
### Case 1: Money transfer without MFA
```python
# BUGGY CODE — should be detected
@app.route('/transfer', methods=['POST'])
@login_required
def transfer_money():
    amount = request.form['amount']
    to_account = request.form['to_account']
    current_user.transfer(amount, to_account)
    return 'Transfer successful'
```
**Expected finding:** Critical — High-risk financial transaction without step-up authentication. Relies only on session cookie, vulnerable if session is hijacked. Require MFA (TOTP, SMS, biometric) or transaction PIN for amounts > threshold.

### Case 2: Account deletion without confirmation
```javascript
// BUGGY CODE — should be detected
app.delete('/api/account', authenticateToken, async (req, res) => {
  await User.deleteOne({ _id: req.user.id });
  res.json({ message: 'Account deleted' });
});
```
**Expected finding:** High — Destructive action (account deletion) without confirmation mechanism. Single HTTP request can delete account if CSRF token is bypassed. Add confirmation email with time-limited token or require password re-entry.

### Case 3: Privilege escalation without approval
```java
// BUGGY CODE — should be detected
@PostMapping("/users/{id}/promote")
public ResponseEntity promoteToAdmin(@PathVariable Long id, Principal principal) {
    if (hasRole(principal, "ADMIN")) {
        User user = userRepository.findById(id).orElseThrow();
        user.setRole("SUPER_ADMIN");
        userRepository.save(user);
        return ResponseEntity.ok("User promoted");
    }
    return ResponseEntity.status(403).build();
}
```
**Expected finding:** High — Privilege escalation without additional authorization. Single admin can create super-admin without approval workflow. Implement multi-party authorization (require 2+ admins) or out-of-band confirmation.

## Counter-Examples
### Counter 1: Transaction with MFA verification
```python
# CORRECT CODE — should NOT be flagged
from pyotp import TOTP

@app.route('/transfer', methods=['POST'])
@login_required
def transfer_money():
    amount = float(request.form['amount'])
    if amount > 1000:  # High-value threshold
        totp_code = request.form.get('mfa_code')
        if not TOTP(current_user.mfa_secret).verify(totp_code):
            abort(403, 'Invalid MFA code')
    to_account = request.form['to_account']
    current_user.transfer(amount, to_account)
    return 'Transfer successful'
```
**Why it's correct:** MFA required for transfers above $1000 threshold.

### Counter 2: Confirmation email for account deletion
```javascript
// CORRECT CODE — should NOT be flagged
app.post('/api/account/request-deletion', authenticateToken, async (req, res) => {
  const token = crypto.randomBytes(32).toString('hex');
  await DeletionToken.create({
    userId: req.user.id,
    token: token,
    expiresAt: Date.now() + 24 * 60 * 60 * 1000 // 24 hours
  });
  await sendEmail(req.user.email, `Confirm deletion: /confirm-delete/${token}`);
  res.json({ message: 'Confirmation email sent' });
});
```
**Why it's correct:** Two-step deletion with email confirmation, time-limited token.

## Binary Eval Assertions
- [ ] Detects missing MFA for transfer in eval case 1
- [ ] Detects missing confirmation in eval case 2
- [ ] Detects privilege escalation without approval in eval case 3
- [ ] Does NOT flag counter-example 1 (MFA verification)
- [ ] Does NOT flag counter-example 2 (confirmation email)
- [ ] Finding references OWASP Transaction Authorization Cheat Sheet
- [ ] Severity assigned as high or critical for financial ops

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
