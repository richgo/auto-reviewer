# Task: XML External Entity (XXE) Injection

## Category
security

## Severity
high

## Platforms
all

## Languages
Java, Python, PHP, .NET, C++

## Description
XXE vulnerabilities occur when XML parsers process user-controlled XML with external entity definitions enabled, allowing attackers to read local files, perform SSRF, cause denial of service, or execute remote code via malicious DTDs.

## Detection Heuristics
- XML parsers with external entity processing enabled
- DTD processing not disabled
- User-uploaded XML files parsed without sanitization
- SOAP/XML-RPC endpoints accepting XML input
- Missing secure parser configuration (SAXParserFactory, DocumentBuilderFactory)

## Eval Cases

### Case 1: Java DocumentBuilder with XXE
```java
// BUGGY CODE — should be detected
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(new InputSource(new StringReader(userXml)));
```
**Expected finding:** Critical — XML parser vulnerable to XXE. External entities enabled by default. Attacker can read files: `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>`. Disable external entities: `factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)`.

### Case 2: Python lxml with unsafe parsing
```python
# BUGGY CODE — should be detected
from lxml import etree
xml_data = request.data
tree = etree.fromstring(xml_data) # Unsafe default
```
**Expected finding:** High — lxml parses XML with entity expansion enabled. Allows XXE and billion laughs DoS. Use safe parser: `etree.XMLParser(resolve_entities=False, no_network=True)`.

### Case 3: PHP simplexml_load_string
```php
// BUGGY CODE — should be detected
<?php
$xml = simplexml_load_string($_POST['xml']);
echo $xml->user->name;
?>
```
**Expected finding:** Critical — simplexml_load_string with default settings allows XXE. Attacker can exfiltrate files via SSRF to attacker-controlled server. Disable entity loading: `libxml_disable_entity_loader(true)`.

## Counter-Examples

### Counter 1: Secure Java XML parsing
```java
// CORRECT CODE — should NOT be flagged
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
factory.setExpandEntityReferences(false);
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(new InputSource(new StringReader(userXml)));
```
**Why it's correct:** All XXE protections enabled: DTD disabled, external entities disabled.

### Counter 2: Python defusedxml
```python
# CORRECT CODE — should NOT be flagged
from defusedxml.ElementTree import fromstring
xml_data = request.data
tree = fromstring(xml_data) # Safe by default
```
**Why it's correct:** defusedxml library has XXE protections enabled by default.

## Binary Eval Assertions
- [ ] Detects XXE in Java DocumentBuilder in eval case 1
- [ ] Detects XXE in Python lxml in eval case 2
- [ ] Detects XXE in PHP simplexml in eval case 3
- [ ] Does NOT flag counter-example 1 (secure Java config)
- [ ] Does NOT flag counter-example 2 (defusedxml)
- [ ] Finding lists specific features to disable
- [ ] Severity assigned as high or critical
