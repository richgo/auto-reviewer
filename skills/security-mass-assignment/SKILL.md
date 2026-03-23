---
name: security mass assignment
description: >
  Migrated review-task skill for Mass Assignment. Use this skill whenever diffs may
  introduce security issues on web, api, especially in all. Actively look for: Accepting
  and applying all user-supplied fields to a model/object without filtering, allowing
  attackers to set privileged fields (role,... and report findings with high severity
  expectations and actionable fixes.
---

# Mass Assignment

## Source Lineage
- Original review task: `review-tasks/security/mass-assignment.md`
- Migrated skill artifact: `skills/review-task-security-mass-assignment/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `web, api`
- Languages: `all`

## Purpose
Accepting and applying all user-supplied fields to a model/object without filtering, allowing attackers to set privileged fields (role, admin, verified) they shouldn't control.

## Detection Heuristics
- `Model.create(req.body)` or `Model.update(req.body)` without field filtering
- Spread operator on request body into model: `new User({ ...req.body })`
- ORM `update_attributes(params)` without strong parameters / allowlist
- Deserialization of request body directly into domain objects

## Eval Cases
### Case 1: Mongoose create from body
```javascript
app.post('/api/users', async (req, res) => {
  const user = await User.create(req.body);
  res.json(user);
});
```
**Expected finding:** High — Mass assignment. `req.body` may include `role`, `isAdmin`, or other privileged fields. Destructure only allowed fields: `const { name, email } = req.body`

### Case 2: Django update without filtering
```python
@api_view(['PUT'])
def update_profile(request, user_id):
    user = User.objects.get(id=user_id)
    for key, value in request.data.items():
        setattr(user, key, value)
    user.save()
    return Response(UserSerializer(user).data)
```
**Expected finding:** High — Mass assignment via setattr loop. Attacker can set `is_superuser=True`. Use serializer with explicit fields.

## Counter-Examples
### Counter 1: Explicit field selection
```javascript
app.post('/api/users', async (req, res) => {
  const { name, email, password } = req.body;
  const user = await User.create({ name, email, password });
  res.json(user);
});
```
**Why it's correct:** Only explicitly allowed fields are used.

## Binary Eval Assertions
- [ ] Detects mass assignment in eval case 1
- [ ] Detects mass assignment in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding identifies privileged fields at risk
- [ ] Severity assigned as high

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
