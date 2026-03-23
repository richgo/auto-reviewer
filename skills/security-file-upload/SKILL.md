---
name: review-task-security-file-upload
description: >
  Migrated review-task skill for Insecure File Upload. Use this skill whenever diffs may
  introduce security issues on web, api, especially in all. Actively look for: Insecure
  file upload vulnerabilities allow attackers to upload malicious files (web shells,
  malware) leading to remote code execution,... and report findings with high severity
  expectations and actionable fixes.
---

# Insecure File Upload

## Source Lineage
- Original review task: `review-tasks/security/file-upload.md`
- Migrated skill artifact: `skills/review-task-security-file-upload/SKILL.md`

## Task Metadata
- Category: `security`
- Severity: `high`
- Platforms: `web, api`
- Languages: `all`

## Purpose
Insecure file upload vulnerabilities allow attackers to upload malicious files (web shells, malware) leading to remote code execution, stored XSS, or denial of service through missing validation on file type, content, size, and storage location.

## Detection Heuristics
- Missing file extension or MIME type validation
- Trusting client-provided Content-Type header without content inspection
- Storing uploaded files in web-accessible directory without renaming
- No file size limits (DoS via disk exhaustion)
- Missing virus/malware scanning on uploads
- Executable files (.php, .jsp, .exe) not blocked
- Image uploads not re-encoded to strip metadata/embedded scripts

## Eval Cases
### Case 1: No file type validation
```python
# BUGGY CODE — should be detected
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file.save(f'/var/www/uploads/{filename}')
    return f'File {filename} uploaded successfully'
```
**Expected finding:** Critical — No file type or extension validation. Attacker can upload shell.php to web-accessible directory and execute it. Validate extensions against allowlist, use secure_filename(), store outside webroot or serve with X-Content-Type-Options: nosniff.

### Case 2: Trusting client MIME type
```javascript
// BUGGY CODE — should be detected
app.post('/upload', upload.single('file'), (req, res) => {
  if (req.file.mimetype !== 'image/jpeg') {
    return res.status(400).send('Only JPEG allowed');
  }
  fs.writeFileSync(`./uploads/${req.file.originalname}`, req.file.buffer);
  res.send('Uploaded');
});
```
**Expected finding:** High — Trusting client-provided MIME type. Attacker can bypass check by setting Content-Type: image/jpeg while uploading PHP shell. Validate actual file content (magic bytes) using file-type library, re-encode images.

### Case 3: Uploads in webroot without renaming
```java
// BUGGY CODE — should be detected
@PostMapping("/upload")
public ResponseEntity upload(@RequestParam("file") MultipartFile file) throws IOException {
    String filename = file.getOriginalFilename();
    File dest = new File("/var/www/html/uploads/" + filename);
    file.transferTo(dest);
    return ResponseEntity.ok("Uploaded: " + filename);
}
```
**Expected finding:** Critical — Files saved in webroot with original filename. Attacker can upload malicious.jsp and execute it via direct URL access. Use randomized filenames (UUID), store outside webroot, serve via separate download controller with proper headers.

## Counter-Examples
### Counter 1: Extension allowlist with secure storage
```python
# CORRECT CODE — should NOT be flagged
import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = '/var/uploads' # Outside webroot

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
        return 'Invalid file type', 400
    filename = f"{uuid.uuid4()}.{secure_filename(file.filename).rsplit('.', 1)[1]}"
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return f'File uploaded: {filename}'
```
**Why it's correct:** Extension allowlist, UUID filename, stored outside webroot, secure_filename() used.

### Counter 2: Content validation with file-type
```javascript
// CORRECT CODE — should NOT be flagged
const fileType = require('file-type');
const sharp = require('sharp');

app.post('/upload', upload.single('file'), async (req, res) => {
  const type = await fileType.fromBuffer(req.file.buffer);
  if (!type || !['image/jpeg', 'image/png'].includes(type.mime)) {
    return res.status(400).send('Invalid image');
  }
  // Re-encode to strip EXIF/metadata
  const processed = await sharp(req.file.buffer).jpeg().toBuffer();
  const filename = `${uuidv4()}.jpg`;
  fs.writeFileSync(`/secure/uploads/${filename}`, processed);
  res.send('Uploaded');
});
```
**Why it's correct:** Magic bytes validation, image re-encoding strips metadata, UUID filename, secure directory.

## Binary Eval Assertions
- [ ] Detects missing file validation in eval case 1
- [ ] Detects MIME type trust in eval case 2
- [ ] Detects webroot storage in eval case 3
- [ ] Does NOT flag counter-example 1 (extension allowlist + UUID)
- [ ] Does NOT flag counter-example 2 (content validation + re-encoding)
- [ ] Finding references OWASP File Upload Cheat Sheet
- [ ] Severity assigned as high or critical

## Migration Notes
- This skill is generated from the legacy review-task corpus for one-to-one lineage.
- Keep this artifact synchronized by re-running `scripts/skills/review_task_converter_cli.py`
  whenever review-task source files change.
