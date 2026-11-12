---
name: php-xss-audit
description: "PHP web source code XSS auditing tool. Identifies user input reaching output contexts (HTML/attribute/JS/URL/template), analyzes escaping and protection strategies, and outputs exploitability ratings, PoCs, and remediation recommendations (no omissions allowed)."
zh-signals: "分析 PHP 源码中的 XSS 漏洞，追踪输入到输出上下文并评估转义防护。信号:XSS审计,PHP源码,输出上下文,转义绕过,PoC"
when-to-use: "Use when auditing PHP source code for cross-site scripting, tracing user input into output contexts, and producing exploitability ratings, PoCs, and remediation advice."
---

# PHP XSS Audit (php-xss-audit)

Analyze PHP project source code and identify cross-site scripting (XSS): user input reaching an output context without correct escaping/encoding, or a framework with auto-escaping disabled that leads to expression execution/HTML injection.

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-XSS-{sequence}`

## XSS Sinks (Mandatory)
Identify the following output points:
- Native output: `echo/print/printf/<?= ?>` (outputs a variable into the response)
- String concatenation into the response: `header()` / `setcookie()` (if it contains controllable content)
- Template rendering:
  - Twig: `{{ }}` (escaped) and the `{% autoescape false %}` / `|raw` risk points
  - Smarty: `fetch/display` and unsafe variable output
  - Blade-style: `{!! !!}` (unescaped output)
- Dynamic script/event attributes: output into `on*` attributes, inside `<script>`, or into URL parameters

## Escaping/Protection Check (Mandatory)
For every suspected chain you must analyze:
- Whether `htmlspecialchars/htmlentities` or framework auto-escaping exists
- Whether context-specific encoding exists (HTML, attribute, JS, URL)
- Whether escaping is disabled (raw/raw filter/unescaped output)

## tracer Trigger Conditions (Required)
- User input passes through multiple layers of processing and is concatenated into an HTML fragment
- A branch exists: one branch escapes, another does not
- The output point is in the template layer while the input is in the controller layer

## Report Output
Output to:
```
{output_path}/vuln_audit/xss_{timestamp}.md
```

## Vulnerability Entry Template (Mandatory)
Essentially the same as `php-sql-audit`, but the data flow chain must explicitly state:
- Output context: HTML body/attribute/script/URL parameter/template fragment
- The location and evidence of the specific escaping function or escaping-disabled point
- The PoC must contain an executable XSS payload and distinguish the required encoding

## Evidence Citation (Mandatory: from php-route-tracer)
Every suspected XSS vulnerability must cite, item by item, the corresponding evidence points of the **XSS row** in `## 9) Sink Evidence Type Checklist` of the trace output (the status may be pending verification, but the evidence citation must exist):
1. `EVID_XSS_OUTPUT_POINT`: evidence of the response output point (echo/template output/`<script>` or attribute/URL context)
2. `EVID_XSS_USER_INPUT_INTO_OUTPUT`: evidence of user input reaching the output
3. `EVID_XSS_ESCAPE_OR_RAW_CONTROL`: escaping/disabled-escaping evidence (htmlspecialchars etc. or raw/raw mode evidence)

## Handling Missing tracer Evidence (Mandatory)
- If none of the key evidence points 1-3 above can be located: the vulnerability status may only be marked `⚠️ Unverified`, and must not be directly marked `✅ Confirmed Exploitable`.
