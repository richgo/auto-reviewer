---
name: review-task-testing-weak-assertions
description: >
  Migrated review-task skill for Weak Test Assertions. Use this skill whenever diffs may
  introduce testing issues on all, especially in all. Actively look for: Tests that pass
  but don't actually verify meaningful behavior — assertions that are too broad, check
  only existence... and report findings with medium severity expectations and actionable
  fixes.
---

# Weak Test Assertions

## Source Lineage
- Original review task: `review-tasks/testing/weak-assertions.md`
- Migrated skill artifact: `skills/review-task-testing-weak-assertions/SKILL.md`

## Task Metadata
- Category: `testing`
- Severity: `medium`
- Platforms: `all`
- Languages: `all`

## Purpose
Tests that pass but don't actually verify meaningful behavior — assertions that are too broad, check only existence not correctness, or test implementation details instead of outcomes.

## Detection Heuristics
- Assertions on truthiness only (`assert result`, `expect(x).toBeTruthy()`)
- Tests that check only status code 200 without verifying response body
- Snapshot tests without semantic assertions
- Assertions on array length without checking contents
- Tests that mock everything (testing mocks, not code)

## Eval Cases
### Case 1: Truthy-only assertion
```javascript
test('creates user', async () => {
  const result = await createUser({ name: 'Alice', email: 'a@b.com' });
  expect(result).toBeTruthy(); // passes even if result is `{ error: true }`
});
```
**Expected finding:** Medium — Weak assertion. `toBeTruthy()` passes for any non-falsy value including error objects. Assert specific properties: `expect(result.name).toBe('Alice')`

### Case 2: Status-only API test
```python
def test_create_order(client):
    response = client.post('/api/orders', json={'item': 'widget', 'qty': 5})
    assert response.status_code == 201
    # doesn't verify the order was actually created correctly
```
**Expected finding:** Medium — Weak test. Only checks status code. Add assertions on response body and verify database state.

## Counter-Examples
### Counter 1: Specific assertions
```javascript
test('creates user', async () => {
  const result = await createUser({ name: 'Alice', email: 'a@b.com' });
  expect(result.name).toBe('Alice');
  expect(result.email).toBe('a@b.com');
  expect(result.id).toBeDefined();
});
```
**Why it's correct:** Asserts specific expected values.

## Binary Eval Assertions
- [ ] Detects weak assertion in eval case 1
- [ ] Detects status-only test in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding suggests specific assertion improvements
- [ ] Severity assigned as medium

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
