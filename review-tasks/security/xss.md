# Task: Cross-Site Scripting (XSS)

## Category
security

## Severity
high

## Platforms
web

## Languages
javascript, typescript, python, java, ruby, php

## Description
User-controlled input rendered in HTML without proper encoding/escaping, allowing attackers to inject malicious scripts that execute in other users' browsers.

## Detection Heuristics
- `innerHTML`, `outerHTML`, `document.write()` with user input
- `dangerouslySetInnerHTML` in React without sanitization
- Template engines with unescaped output (`{{{ }}}` in Handlebars, `| safe` in Jinja2, `<%- %>` in EJS)
- URL parameters reflected in page without encoding
- `v-html` in Vue with user data

## Eval Cases

### Case 1: React dangerouslySetInnerHTML
```jsx
function Comment({ comment }) {
  return <div dangerouslySetInnerHTML={{ __html: comment.body }} />;
}
```
**Expected finding:** High — XSS via dangerouslySetInnerHTML. User-provided `comment.body` rendered as raw HTML. Sanitize with DOMPurify: `DOMPurify.sanitize(comment.body)`

### Case 2: Express template without escaping
```javascript
app.get('/search', (req, res) => {
  res.send(`<h1>Results for: ${req.query.q}</h1>`);
});
```
**Expected finding:** High — Reflected XSS. Search query rendered directly in HTML response without encoding.

### Case 3: Jinja2 safe filter
```html
<div class="bio">{{ user.bio | safe }}</div>
```
**Expected finding:** High — XSS via Jinja2 `safe` filter bypassing auto-escaping on user-controlled content.

## Counter-Examples

### Counter 1: React text content
```jsx
function Comment({ comment }) {
  return <div>{comment.body}</div>;
}
```
**Why it's correct:** React auto-escapes text content in JSX expressions.

### Counter 2: Sanitized HTML
```jsx
import DOMPurify from 'dompurify';
function Comment({ comment }) {
  return <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(comment.body) }} />;
}
```
**Why it's correct:** DOMPurify sanitizes HTML before rendering.

## Binary Eval Assertions
- [ ] Detects XSS in eval case 1 (dangerouslySetInnerHTML)
- [ ] Detects XSS in eval case 2 (reflected XSS)
- [ ] Detects XSS in eval case 3 (Jinja2 safe filter)
- [ ] Does NOT flag counter-example 1 (React auto-escape)
- [ ] Does NOT flag counter-example 2 (DOMPurify)
- [ ] Finding includes sanitization fix suggestion
- [ ] Severity assigned as high
