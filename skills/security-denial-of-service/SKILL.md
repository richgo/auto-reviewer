---
name: security denial of service
description: >
  Denial of Service Vulnerabilities. Use this skill
  whenever diffs may introduce security issues on all, especially in all. Actively look
  for: Denial of Service vulnerabilities allow attackers to exhaust system resources
  (CPU, memory, disk, network) through algorithmic complexity attacks,... and report
  findings with high severity expectations and actionable fixes.
---

# Denial of Service Vulnerabilities
## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `all`
- Languages: `all`

## Purpose
Denial of Service vulnerabilities allow attackers to exhaust system resources (CPU, memory, disk, network) through algorithmic complexity attacks, resource amplification, unbounded operations, or application-layer exploits without proper rate limiting or resource quotas.

## Detection Heuristics
- Unbounded loops or recursive operations on user input
- No timeout or size limits on file uploads, request bodies, or query results
- Algorithmic complexity vulnerable to worst-case input (O(n²) or worse)
- Missing rate limiting on resource-intensive endpoints
- Synchronous blocking operations without timeouts
- Large object allocations from user-controlled size parameters

## Eval Cases
### Case 1: Unbounded file upload
```python
# BUGGY CODE — should be detected
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    content = file.read() # No size limit!
    db.save_file(content)
    return 'Uploaded'
```
**Expected finding:** High — Unbounded file upload. Attacker can upload multi-GB file exhausting disk/memory. Add size limit: `app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB`.

### Case 2: Algorithmic complexity attack
```javascript
// BUGGY CODE — should be detected
app.post('/api/find-duplicates', (req, res) => {
  const items = req.body.items; // User-controlled array
  const duplicates = [];
  for (let i = 0; i < items.length; i++) {
    for (let j = i + 1; j < items.length; j++) {
      if (items[i] === items[j]) {
        duplicates.push(items[i]);
      }
    }
  }
  res.json({ duplicates });
});
```
**Expected finding:** High — O(n²) algorithm on user-controlled input. Attacker sends array with 1M elements causing 500 billion comparisons. Use Set for O(n) deduplication or limit input size.

### Case 3: No timeout on external request
```java
// BUGGY CODE — should be detected
@GetMapping("/proxy")
public ResponseEntity proxy(@RequestParam String url) {
    RestTemplate restTemplate = new RestTemplate();
    String response = restTemplate.getForObject(url, String.class);
    return ResponseEntity.ok(response);
}
```
**Expected finding:** High — External HTTP request without timeout. Attacker provides slow/hanging endpoint tying up server threads. Configure timeouts: `RestTemplate` with `HttpComponentsClientHttpRequestFactory` (connectTimeout, readTimeout).

## Counter-Examples
### Counter 1: File upload with size limit
```python
# CORRECT CODE — should NOT be flagged
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file.content_length > app.config['MAX_CONTENT_LENGTH']:
        abort(413, 'File too large')
    content = file.read()
    db.save_file(content)
    return 'Uploaded'
```
**Why it's correct:** File size limited to 16MB, explicit check enforced.

### Counter 2: Linear algorithm with input validation
```javascript
// CORRECT CODE — should NOT be flagged
app.post('/api/find-duplicates', (req, res) => {
  const items = req.body.items;
  if (!Array.isArray(items) || items.length > 10000) {
    return res.status(400).json({ error: 'Invalid input size' });
  }
  const duplicates = items.filter((item, index) => items.indexOf(item) !== index);
  res.json({ duplicates: [...new Set(duplicates)] });
});
```
**Why it's correct:** Input size validated (max 10k items), O(n) algorithm.

## Binary Eval Assertions
- [ ] Detects unbounded upload in eval case 1
- [ ] Detects algorithmic complexity in eval case 2
- [ ] Detects missing timeout in eval case 3
- [ ] Does NOT flag counter-example 1 (size limit)
- [ ] Does NOT flag counter-example 2 (input validation + efficient algorithm)
- [ ] Finding recommends specific limits and timeouts
- [ ] Severity assigned as high
