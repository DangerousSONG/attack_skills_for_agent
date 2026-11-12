---
name: php-symfony-audit
description: "Symfony framework-specific security audit tool. Performs white-box static analysis of Symfony framework mechanisms such as security.yaml, CSRF, Twig/Twig raw, expressions, and access control, and maps risks to the generic vulnerability type taxonomy (AUTH/CSRF/CFG/XSS/TPL/LOGIC, etc.)."
zh-signals: "审计 Symfony 框架配置与安全机制，覆盖访问控制、CSRF、Twig raw 与安全表达式。信号:Symfony审计,security.yaml,CSRF防护,Twig转义,访问控制。"
when-to-use: >-
  Use when performing a white-box security audit of a Symfony project, especially security.yaml access_control, CSRF protection, Twig autoescaping or raw output, and ExpressionLanguage usage.
---

# PHP Symfony Framework Security Audit (php-symfony-audit)

Analyze the "framework-specific security mechanisms" and "configuration/usage pitfalls" in Symfony project source code, focusing on:
- Correctness of access_control and firewalls configuration in `config/packages/security*.yaml`
- CSRF protection mechanism (form submission and token validation)
- Risks of Twig rendering autoescaping and raw output
- Symfony access expressions and the security interceptor chain (mapped to AUTH/EXPR/TPL as appropriate)
- HttpClient outbound request policy (SSRF-class risks mapped to the generic SSRF type)

## Input
Provided by the user:
- `source_path`: root directory of the Symfony project source code
Optional:
- `output_path`: output directory path (default `{source_path}_audit`)

## Output Directory
Output to:
```
{output_path}/framework_audit/
  symfony_{timestamp}.md
```

## Framework Identification (Required)
You must present evidence points identifying the target as Symfony (no unsupported assertions):
- Typical directories: `config/`, `src/`, `templates/`
- Dependency evidence: `symfony/framework-bundle` etc. in `composer.json`
- Entry point evidence: `public/index.php` or a similar front controller

## Risk Type Mapping (Required)
Every finding must state:
- The applicable generic type code: `AUTH` / `CSRF` / `CFG` / `XSS` / `TPL` / `LOGIC` / `SESS` / `SSRF` / `EXPR` etc.
- Mapping rationale: why this Symfony risk belongs to that type code (one sentence)

## Mandatory Audit Checklist (Required: check each item and output the result)

### 1) Access Control and Authentication Policy (AUTH)
Must locate and output:
- `access_control` rules in `security.yaml`
- `firewalls` configuration (whether `anonymous: true`, whether `stateless: true` and the authentication method)
- `switch_user`, `role_hierarchy`, or voter/policy-style configuration (if present)

Decision rules:
- If overly permissive rules exist (e.g. an overly generic anonymous rule covering sensitive paths), output an AUTH risk
- If a pattern of "authenticated but missing role/ownership checks" exists, output an AUTH or LOGIC risk

### 2) CSRF Protection (CSRF)
Must locate and output:
- Symfony CSRF-related configuration (`framework: csrf_protection` or component-level configuration)
- How the CSRF token is generated and received in form type usage
- The handling path when token validation fails (early exit, or validated only in some branches)

Decision rules:
- If "some routes/forms have CSRF disabled or the CSRF token receiving field is inconsistent" exists, output a CSRF risk

### 3) Twig Autoescaping and Raw Output (XSS/TPL)
Must locate and output:
- Twig configuration: whether autoescaping is disabled (globally or locally)
- Raw output points in templates: `|raw`, `{% autoescape false %}`, and any "escaping bypass" directives
- Data sources: where the variables used in raw output come from (request/session/database fields)

Decision rules:
- If a raw output variable has a controllable source and is not escaped, map it to XSS or TPL (TPL if expression execution / template engine controllability exists)

### 4) Security Expressions and Evaluation Risk (EXPR/TPL/AUTH)
Must locate and output:
- Where ExpressionLanguage is used for security (voter/policy `is_granted` or expression conditions)
- Whether the expression string source may be user-controlled (e.g. expression concatenation)

Decision rules:
- If the expression string is controllable, output it as an EXPR or TPL risk

### 5) Outbound HTTP and Internal Network Access (SSRF)
Must locate and output (framework correlation checks only):
- Wrapper entry points for outbound calls such as `HttpClient`/`KernelInterface`
- Whether the URL/host originates from user input, and whether an allowlist or internal network blocking exists

## Observable PoC (Required: framework-specific observable verification harness)
Provide at least one of the following two categories and clearly state the observation point:
- Access control error: access a suspected protected route as an unauthenticated/low-privilege user and observe the response difference
- CSRF error: craft a form request with a missing or forged CSRF token and observe the status code/error path

PoC output requirements:
- Must include the real route and the real form action (or route path)
- Must state the expected observation point (e.g. whether a 403 is returned, whether the state change still proceeds)

## Output Completeness Check (Mandatory)
- [ ] Output includes: Symfony identification evidence points
- [ ] All five blocks (AUTH/CSRF/Twig(raw)/security expressions/HttpClient(optional)) have check results
- [ ] Every risk has: a mapped type code + location evidence + an observable verification harness + a remediation recommendation
