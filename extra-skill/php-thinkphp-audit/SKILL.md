---
name: php-thinkphp-audit
description: "ThinkPHP framework-specific security audit tool. Performs white-box static audits of the common ThinkPHP mechanisms such as authentication/CSRF/template escaping/ORM writes (Mass Assignment)/debug and configuration exposure, and maps the results onto the generic vulnerability type system (AUTH/CSRF/TPL/XSS/LOGIC/CFG/SESS/SQL, etc.)."
zh-signals: "对 ThinkPHP 项目进行白盒安全审计，覆盖鉴权、CSRF、模板转义与 ORM 写入风险。信号:thinkphp,php审计,白盒,mass assignment,csrf,框架安全"
when-to-use: >-
  Use when performing a white-box security audit of a ThinkPHP project, focused on
  authentication, CSRF, template escaping, ORM mass assignment, and debug config exposure.
---

# PHP ThinkPHP Framework Security Audit (php-thinkphp-audit)

Analyze the "framework-specific security mechanisms" and typical pitfall patterns in ThinkPHP project source code, focusing on:
- Authentication and access control (auth module, controller/middleware gates)
- The CSRF token mechanism and skip paths
- Automatic escaping and raw output risks in the ThinkPHP template engine
- Mass Assignment caused by the ORM/Model write path (`allowField`/scenario validation)
- Database native expression / raw SQL injection entry points (mapped to the generic SQL risk class)
- Debug/exception output and security configuration switches (mapped to CFG)

## Input
Provided by the user:
- `source_path`: ThinkPHP project root directory
Optional:
- `output_path`: output directory path (default `{source_path}_audit`)

## Output Directory
Output to:
```
{output_path}/framework_audit/
  thinkphp_{timestamp}.md
```

## Framework Identification (Required)
You must provide evidence points proving the project is ThinkPHP:
- Dependency evidence: `composer.json` contains `topthink/think-*` or `thinkphp/think-*` related dependencies
- Entry point evidence: `public/index.php` or an equivalent front-end entry point
- Configuration evidence: the `config/` directory contains ThinkPHP configuration files (such as `app.php`, `database.php`, `middleware.php`, depending on the project)
- Runtime directory evidence: the `runtime/` directory structure (if present)

## Risk Type Mapping (Required)
Every finding must state:
- Generic type code: `AUTH` / `CSRF` / `XSS` / `TPL` / `LOGIC` / `CFG` / `SESS` / `SQL`, etc. (choose from your unified type codes)
- Mapping rationale: why it falls under that type code (explain the mapping logic in one sentence)

## Mandatory Audit Checklist (Required: check each item and output the result)

### 1) Authentication and Access Control (AUTH)
Must locate and output:
- Authentication entry points: controller middleware/filters, base Controller/Behavior classes, route-level permission middleware
- Use of the auth module: whether ThinkPHP's auth capabilities are used (such as `Auth`/RBAC/role permission check functions or an equivalent wrapper)
- The source of the parameters used for permission checks: where the resource ID / user ID comes from (route parameter / request body / session), and whether ownership is validated

Decision rules:
- If you find "only the login state is checked but resource ownership / role granularity is missing", report an AUTH risk
- If you find "the permission check is missing in some branches / bypassed after an exception", report an AUTH or LOGIC risk

### 2) CSRF Protection (CSRF)
Must locate and output:
- Where the CSRF token is enabled: configuration item / middleware / form generation logic
- The field receiving the token: which field of the body/header it comes from (depending on the project)
- The token validation logic: the validation function/middleware entry point and the failure handling (whether it returns/throws and blocks the state change)
- Skip rules: which routes, which request methods, or which scenarios skip the CSRF validation

Decision rules:
- Skip rules exist but cover state-changing interfaces => CSRF risk
- Token validation fails but the business logic still executes (for example the exception is swallowed) => CSRF risk

### 3) Template Engine Escaping and Raw Output (XSS/TPL)
Must locate and output:
- The template auto-escaping policy: whether the template syntax escapes by default and whether it is globally disabled
- Raw output / escaping-skip syntax: for example `raw`/`|raw` in templates or an equivalent mechanism (depending on the actual template engine version and usage)
- User input reaching template variables: where the variables come from (request/session/db), and whether they are directly concatenated into HTML/JS/attribute contexts

Decision rules:
- If raw output is user-controllable and unescaped => map to XSS or TPL (if it involves expressions/execution chains)

### 4) ORM Write Path (LOGIC: Mass Assignment)
Must locate and output:
- Input retrieval: whether `request->param()` / `request->all()` / `$this->request->post()` or an equivalent structure is passed wholesale into a model write
- Model write points: `Model::create/save/update`, `$model->save($data)`, bulk assignment behavior
- Allowed field policy: whether `allowField`/`field`/scenario or an equivalent whitelist mechanism is configured

Decision rules:
- Input is written wholesale and the model lacks deny/allow constraints on sensitive fields => LOGIC risk
- An allowed-field whitelist exists but still contains high-risk fields => LOGIC risk

### 5) Database Native Expression / Raw SQL Risk (SQL)
Must locate and output:
- Raw SQL entry points: `Db::query($sql)`, `Db::execute($sql)`, `whereRaw`, `orderRaw`, `buildExpression`, etc. (depending on the project)
- Evidence of user input entering native expressions: concatenation, template substitution, string assembly points
- Whether a parameterized/binding strategy exists: `->bind/placeholder/prepare`, etc. (depending on the project)

Decision rules:
- User input reaches a raw SQL expression through string concatenation => SQL risk

### 6) Security Configuration and Debug Exposure (CFG/SESS)
Must locate and output:
- Debug/exception output: `app_debug`, `trace`, error page output policy, log level (depending on the project)
- Cookie/session security parameters: if the project configuration file is visible (HttpOnly/Secure/SameSite, etc.), output the SESS/CFG risk mapping

Decision rules:
- Debug enabled in production / stack trace echo => CFG risk

## Observable PoC (Required: framework-specific observable verification harness)
Provide at least one of the following two categories and clearly state the observation point:
- AUTH: use a low-privilege user to request a suspected protected action and observe whether access succeeds / whether a business side effect occurs
- CSRF: craft a request with a missing or incorrect CSRF token against a state-changing route and observe whether it is blocked and whether the business logic still executes

PoC output requirements:
- Must include a real route/controller action (extracted from your route mapping or code entry point evidence)
- Must include the token field name / the fields required for validation (use the actual field names of the project)
- Must state the observation point (HTTP status code, response content characteristics, whether a business side effect occurred)

## Output Completeness Check (Mandatory)
- [ ] The output contains: ThinkPHP identification evidence + the results of the six major checks (AUTH/CSRF/template output/ORM write/database native entry points/debug configuration)
- [ ] Every risk has: a mapped type code + location evidence + an observable verification harness + a remediation recommendation
