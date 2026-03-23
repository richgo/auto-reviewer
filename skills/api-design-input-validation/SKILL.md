---
name: api design input validation
description: >
  Migrated review-task skill for Missing Input Validation. Use this skill whenever diffs
  may introduce api-design issues on web, api, mobile, especially in all. Actively look
  for: API endpoints or functions that accept user input without validating type,
  format, range, or required fields — leading... and report findings with high severity
  expectations and actionable fixes.
---

# Missing Input Validation

## Source Lineage
- Original review task: `review-tasks/api-design/input-validation.md`
- Migrated skill artifact: `skills/review-task-api-design-input-validation/SKILL.md`

## Task Metadata
- Category: `api-design`
- Severity: `high`
- Platforms: `web, api, mobile`
- Languages: `all`

## Purpose
API endpoints or functions that accept user input without validating type, format, range, or required fields — leading to crashes, data corruption, or security vulnerabilities.

## Detection Heuristics
- Request body fields used directly without schema validation
- Missing type checks on dynamic inputs
- No range/length validation on numeric/string fields
- Enum values not validated against allowed set
- File uploads without type/size validation

## Eval Cases
### Case 1: No validation on API input
```javascript
app.post('/api/orders', async (req, res) => {
  const order = await Order.create({
    userId: req.body.userId,
    quantity: req.body.quantity, // could be negative, string, or missing
    productId: req.body.productId,
  });
  res.json(order);
});
```
**Expected finding:** High — No input validation. `quantity` could be negative, zero, non-numeric, or missing. Validate with schema (Zod, Joi) before processing.

### Case 2: Unvalidated file upload
```python
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['document']
    file.save(f'/uploads/{file.filename}')
    return jsonify({"status": "uploaded"})
```
**Expected finding:** High — No file validation. Missing checks for file type, size limit, and filename sanitization. Also path traversal risk via `file.filename`.

## Counter-Examples
### Counter 1: Schema-validated input
```javascript
const schema = z.object({
  userId: z.string().uuid(),
  quantity: z.number().int().positive().max(1000),
  productId: z.string().uuid(),
});

app.post('/api/orders', async (req, res) => {
  const data = schema.parse(req.body);
  const order = await Order.create(data);
  res.json(order);
});
```
**Why it's correct:** Zod schema validates types, ranges, and formats before processing.

## Binary Eval Assertions
- [ ] Detects missing validation in eval case 1
- [ ] Detects unvalidated upload in eval case 2
- [ ] Does NOT flag counter-example 1
- [ ] Finding suggests schema validation approach
- [ ] Severity assigned as high

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
