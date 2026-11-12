---
name: php-codeigniter-audit
description: "CodeIgniter framework-specific security audit tool. Performs white-box static analysis of CodeIgniter's CSRF, XSS output filtering, database query construction, router and validator configuration, session cookie security, and other mechanisms, and maps the results to the generic vulnerability type taxonomy (CSRF/AUTH/XSS/SQL/CFG/SESS, etc.)."
zh-signals: "CodeIgniter 框架白盒安全审计。信号:CodeIgniter,白盒审计,CSRF,XSS,SQL注入,会话安全"
when-to-use: "Use when auditing a CodeIgniter project's framework configuration for CSRF, XSS output filtering, SQL construction, router and validator, and session cookie issues."
---

# PHP CodeIgniter Framework Security Audit (php-codeigniter-audit)

Analyze the framework mechanisms and configuration pitfalls of CodeIgniter projects, focusing on:
- Whether CSRF protection is enabled and whether the token name/validation logic is correct
- Output filtering and XSS protection (whether CI's built-in filters are disabled or misused)
- Database query construction: whether user input is concatenated into `$this->db->query` or raw SQL
- Whether form validators are overridden or bypassed
- Session cookie flag security (CI session settings)

## Input
Provided by the user:
- `source_path`: CodeIgniter project root directory
Optional:
- `output_path`: output directory path (default `{source_path}_audit`)

## Output Directory
Output to:
```
{output_path}/framework_audit/
  codeigniter_{timestamp}.md
```

## Framework Identification (Required)
Must present identification evidence (no unsupported assertions):
- Typical directories: `application/`, `system/`
- Configuration files: `application/config/config.php` or session/security configuration files
- Version clues: `composer.json` or the `system/core/` structure

## Risk Type Mapping (Required)
Every finding must state:
- Generic type code: `CSRF` / `XSS` / `SQL` / `AUTH` / `CFG` / `SESS` / `LOGIC` etc.
- The reason for the mapping

## Mandatory Audit Checklist (Required: check each item and output the result)

### 1) CSRF Protection (CSRF)
Must locate and output:
- Whether CSRF is enabled (CI 3: csrf settings in `config.php`; CI 4: Security class configuration)
- Token name, validation entry point, and skip rules (whether some controllers/methods do not enable validation)

Decision rules:
- If a state-changing route exists without CSRF enabled, output a CSRF risk

### 2) XSS Output Protection (XSS/CFG)
Must locate and output:
- Whether CI's XSS filters are enabled (such as `global_xss_filtering`, `Security::xss_clean`)
- Whether the view layer applies proper `html_escape` or equivalent escaping to user input

Decision rules:
- If filtering is disabled or output is unescaped and user input can reach the view output, output an XSS risk

### 3) Database Query Concatenation (SQL)
Must locate and output:
- Raw queries: concatenation evidence in `$this->db->query($sql)` or `->query($userInput)`
- The correct path: Query Builder with bound parameters

Decision rules:
- If user input enters an SQL string concatenation, output an SQL risk

### 4) Session and Cookie (SESS/CFG)
Must locate and output:
- Cookie flags: HttpOnly/Secure/SameSite (as configured in the project)
- Session configuration: session timeout, fixation protection (if present)

### 5) Authentication and Access Control (AUTH)
Must locate and output:
- Access protection patterns in controllers: custom `auth` helper, base controller checks, filters
- Router-level filters or middleware (CI 4 filters)

Decision rules:
- If sensitive controllers or methods lack unified authentication, output an AUTH risk

## Observable PoC (Required: framework-specific observable verification harness)
Provide at least one of the following two categories and clearly state the observation point:
- CSRF: call a state-changing route without a CSRF token, and observe whether it succeeds and its side effects
- SQL: call a suspected SQL concatenation path with an injection payload, and observe the response difference or error output

## Output Completeness Check (Mandatory)
- [ ] Output includes: CSRF/XSS/SQL/Session/Auth check results
- [ ] Every risk has: a mapped type code + location evidence + an observable verification harness + a remediation recommendation
