---
name: php-config-audit
description: "PHP web configuration security audit tool. Identifies overly permissive CORS, error exposure, debug switches, missing security headers, dangerous runtime switches, and more, and outputs severity ratings, exploitability analysis, PoCs, and remediation recommendations (must not be omitted)."
zh-signals: "审计 PHP 项目配置与运行时设置中的 CORS、错误暴露、安全头缺失与危险开关缺陷并输出证据、PoC 与修复建议。信号:PHP配置,CORS,安全头,错误暴露,配置审计"
when-to-use: >-
  Use when auditing a PHP project's configuration files and runtime settings for security
  misconfigurations, and you need graded evidence, exploitability analysis, and PoC.
---

# PHP Configuration Security Audit (php-config-audit)

Analyze PHP project configuration and runtime settings to detect security-relevant configuration flaws:
- Overly permissive CORS (allowing all origins, improper credentials combination)
- Error and debug information exposure (display_errors, debug mode, unhidden stack traces)
- Missing security response headers (CSP, X-Frame-Options/Frame-Options, Referrer-Policy, HSTS, etc.)
- Dangerous PHP/runtime switches (e.g. `allow_url_include`, `file_uploads`, and other risky combinations tied to business logic)
- Accessible/executable properties of upload/download directories (if inferable from configuration, output the evidence)

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-CFG-{sequence}`

## Mandatory Evidence (Mandatory)
An evidence path MUST be given for every issue:
- Configuration file/environment variable location (e.g. `.env`, `config/*.php/yaml`, `php.ini`, Dockerfile/entrypoint)
- Runtime setting code location (`ini_set`, `set_exception_handler`, response header middleware)
- Impact point: which routes/responses are affected by this configuration (must link to at least one entry point/response chain)

## Exploitability and Preconditions (Mandatory)
- Error exposure: whether it leaks sensitive information that an attacker can exploit (e.g. combined with arbitrary file read/SQLi for escalation)
- CORS: whether a victim browser scenario with a credentials combination exists
- Missing security headers: whether it can be chained with XSS/clickjacking

## PoC (Mandatory)
An observable PoC (e.g. `curl -i`) or request steps MUST be given:
- Trigger the response through a real route
- Show evidence of the missing/incorrect response headers or stack trace output

## Evidence Citation (Mandatory: static evidence first, trace as optional enhancement)

> **CFG belongs to the non-trace-gate category**: configuration security auditing relies primarily on static configuration file/code evidence, and does NOT use the `php-route-tracer` trace-gate or `## 9) Sink Evidence Type Checklist` as a hard prerequisite. If CFG row evidence exists in the trace output, it can be cited as an enhancement.

Every suspected configuration security risk MUST provide the following evidence (sourced from static code/configuration files; trace output may serve as an enhancement):
1. `EVID_CFG_CONFIG_LOCATION`: configuration file/environment variable location evidence (e.g. `.env`, `config/*.php/yaml`, `php.ini`, Dockerfile/entrypoint)
2. `EVID_CFG_RUNTIME_SETTING_CODE`: runtime setting code location evidence (ini_set/set_exception_handler/response header middleware, etc.)
3. `EVID_CFG_IMPACT_ASSOCIATION`: impact point association evidence (which routes/responses are affected by this configuration)
4. `EVID_CFG_SECURITY_SWITCH_EVIDENCE`: key configuration evidence for security headers/error exposure/CORS/dangerous switches

## Handling Missing Evidence (Mandatory, follows the unified standard)
- Configuration items can be evidenced directly from static files and do not depend on trace completeness.
- If the static evidence for 1~4 above is complete and the impact path is clear: you may directly give `✅Confirmed Exploitable` or `🟡High Probability`.
- If the key impact point association (3) is missing (it cannot be confirmed which entry points/responses are affected): downgrade to `⚠️Pending Verification`.

## Report Output
```
{output_path}/vuln_audit/cfg_{timestamp}.md
```

