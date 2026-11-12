---
name: php-yii-audit
description: "Yii framework-specific security audit tool. Performs white-box static analysis of Yii (typically Yii2) access control (AccessControl/RBAC), CSRF, input filtering rules, output encoding strategy, and URL/redirect security, and maps the results to the generic vulnerability type taxonomy (AUTH/CSRF/XSS/CFG/LOGIC, etc.)."
zh-signals: "对 Yii2 项目进行白盒安全审计，检查访问控制、CSRF、输入过滤、输出编码与 URL 跳转风险。信号:Yii2,访问控制,CSRF,XSS,白盒审计"
when-to-use: "Use when auditing a Yii or Yii2 codebase for access control, CSRF, mass assignment, output encoding, and redirect security. Requires project source code access."
---

# PHP Yii (Yii2) Framework Security Audit (php-yii-audit)

Analyze the framework mechanisms and configuration pitfalls of Yii2 projects, focusing on:
- Access control: `AccessControl` filter, `roles` rules, use of matchCallback
- RBAC: authorization completeness along the `user->can`/`can()` path
- CSRF: `enableCsrfValidation` and cookie validation
- Output encoding: whether views use `Html::encode` and `HtmlPurifier`, plus dangerous raw output
- URL and redirect: whether redirect/Url generation is controlled by untrusted input
- Input filtering: whether `rules()`, `safeAttributes()`, and scenarios lead to mass assignment

## Input
Provided by the user:
- `source_path`: Yii project root directory
Optional:
- `output_path`: output directory path (default `{source_path}_audit`)

## Output Directory
Output to:
```
{output_path}/framework_audit/
  yii_{timestamp}.md
```

## Framework Identification (Required)
Must present Yii identification evidence (no unsupported assertions):
- Dependency evidence: `composer.json` contains `yiisoft/yii2` or related components
- Entry point evidence: `web/index.php` or the `yii` entry script
- Application directories: `controllers/`, `models/`, `views/`

## Risk Type Mapping (Required)
Every finding must state:
- Generic type code: `AUTH` / `CSRF` / `XSS` / `CFG` / `LOGIC` etc.
- The reason for the mapping

## Mandatory Audit Checklist (Required: check each item and output the result)

### 1) AccessControl Authorization Rule Correctness (AUTH)
Must locate and output:
- `AccessControl` configuration in `behaviors()`: `rules`, `roles`, `matchCallback` and the action coverage scope
- Whether a permissive mode exists that relies only on matchCallback
- Whether custom authentication logic exists without being enforced by a unified filter

Decision rules:
- If any path can bypass AccessControl or the rules are too broad, output an AUTH risk

### 2) RBAC / Permission Check Completeness (AUTH/LOGIC)
Must locate and output:
- `user->can({value})`, `can()` or equivalent permission checks in controllers/service layer
- Object ownership validation: whether owner_id/user_id or the resource ownership relationship is also verified

Decision rules:
- If only "the user has permission type X" is checked without verifying object ownership, output an AUTH or LOGIC risk

### 3) CSRF (CSRF)
Must locate and output:
- `enableCsrfValidation` and cookie validation settings
- The token receiving field and how validation failures are handled (whether it returns early)

### 4) Output Encoding and XSS (XSS)
Must locate and output:
- Whether raw output exists in views: cases where `Html::encode` is bypassed, or `raw`-style mechanisms are used
- Whether user input is concatenated directly into HTML attributes/JS/URLs in templates

### 5) Input Filtering and Mass Assignment (LOGIC)
Must locate and output:
- Model `rules()`, `safeAttributes()`, `scenarios()` configuration
- Whether `load($request->post())` is followed by a direct save while sensitive fields remain unrestricted

## Observable PoC (Required: framework-specific observable verification harness)
Provide at least one of the following two categories and clearly state the observation point:
- AUTH: request a suspected protected action as a low-privilege user, and observe the response difference or business side effect
- CSRF: call a suspected protected state-changing POST request without a CSRF token, and observe the error and whether it still executes successfully

PoC output requirements:
- Must include the controller/action route and parameter fields
- Must state which HTTP status code and business outcome you are observing

## Output Completeness Check (Mandatory)
- [ ] Output includes: AccessControl/RBAC/CSRF/output encoding/input filtering check results
- [ ] Every risk has: a mapped type code + location evidence + an observable verification harness + a remediation recommendation
