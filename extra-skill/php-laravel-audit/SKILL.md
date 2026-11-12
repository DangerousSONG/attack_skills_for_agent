---
name: php-laravel-audit
description: "Laravel framework-specific security audit tool. Performs white-box static audits of common Laravel framework characteristics such as authentication/CSRF/Session/model mass assignment/Blade rendering, and maps the risks onto your existing generic vulnerability type system (AUTH/CSRF/LOGIC/XSS/CFG, etc.)."
zh-signals: "对 Laravel 项目源码进行框架特性相关的白盒安全审计并映射到通用漏洞类型。信号:Laravel,框架审计,鉴权,CSRF,Blade,Eloquent"
when-to-use: "Use when auditing a Laravel codebase for framework-specific security flaws such as auth bypass, CSRF gaps, session issues, mass assignment, or Blade template injection."
---

# PHP Laravel Framework Security Audit (php-laravel-audit)

Analyze the "framework-specific security mechanisms" and "common pitfall patterns" in Laravel project source code, focusing on:
- Authentication and route protection (middleware/auth/Policies/Gates)
- CSRF and token protection (VerifyCsrfToken, except list, API vs. Cookie authentication differences)
- Session and Cookie security (session_regenerate_id, cookie flags, risk points in the remember mechanism)
- Eloquent mass assignment and request-to-model write flaws (Model::create/fill/update and the `$request->all()` chain)
- Raw output and expression execution risks in Blade template rendering (`{!! !!}`, `@php`, and unescaped output)
- Whether Laravel signed URLs and route signature validation form a closed loop (Signed middleware and generation sites)

## Input
Provided by the user:
- `source_path`: Laravel project source root directory
Optional:
- `output_path`: output directory path (default `{source_path}_audit`)

## Output Directory
Output to:
```
{output_path}/framework_audit/
  laravel_{timestamp}.md
```

## Framework Identification (Required)
You must provide evidence points identifying the project as Laravel (bare assertions are not allowed):
- `composer.json` dependencies
- Typical directories: `app/`, `routes/`, `config/`
- Core entry points: `public/index.php`, `bootstrap/app.php`

## Risk Type Mapping (Required)
Every finding must state:
- Applicable generic type code: `AUTH` / `CSRF` / `LOGIC` / `XSS` / `CFG` / `SESS` / `FILE`, etc. (choose from the type codes available in your `shared/SEVERITY_RATING.md`)
- Why this Laravel risk falls under that generic type code (explain the mapping logic in one sentence)

## Mandatory Audit Checklist (Required: check each item and output the result)

### 1) Authentication and Access Control (AUTH)
You must locate and output the following evidence:
- Protected route entry points: `middleware('auth')` / `middleware('can')` / `Route::middleware([{value}])->group({value})` in `routes/web.php` and `routes/api.php`
- Authorization logic: location evidence for `Gate::` / `Policy` / `authorize` / `can` / `->can({value})`
- Risk judgement: whether there is a "logged in but no resource-level ownership validation" pattern (e.g. only checking that the user exists, not that they own the resource)
- Route naming and resource binding: whether Route Model Binding exists without ownership validation

Output requirements:
- If a gap is found: you must provide the "gap location + the request types that could bypass it (GET/POST/API) + a remediation recommendation"
- If none is found: you must still output the "basis for the not-found conclusion" (e.g. except/guard is empty, all sensitive routes have middleware, etc.)

### 2) CSRF and Token Protection (CSRF)
You must locate:
- CSRF middleware: `VerifyCsrfToken` or an equivalent middleware
- except list: which routes are excluded
- API vs. Cookie authentication differences: if the project uses Cookie/session for the API, confirm whether API routes are still protected by CSRF

Output requirements:
- Must cover "bypassable branches": for example only some methods are not validated, only certain Content-Types are not validated, only skipped for AJAX requests, etc.

### 3) Session and Cookie Security (SESS)
You must locate:
- Session fixation protection after login: whether `session_regenerate_id` or the Laravel equivalent exists
- Cookie flags: the configuration location of `HttpOnly`/`Secure`/`SameSite` (`config/session.php` or custom middleware)
- logout: whether the session is cleared on logout

### 4) Eloquent Mass Assignment (LOGIC)
You must locate and output the data-flow chain evidence:
- Request input retrieval: `$request->all()`, `$request->input({value})`, `json_decode({value})`
- Model write points: `Model::create({value})` / `Model::update({value})` / `$model->fill({value})` / `->save()`
- Model fill policy: the configuration location of `$fillable` / `$guarded`

Decision rules:
- If `$request->all()` or equivalent input flows directly into `create/fill/update` and the model lacks a denylist for sensitive fields (or `$fillable` is too broad), report a risk

### 5) Blade Raw Output (XSS)
Must locate and output:
- Raw output: `{!! {value} !!}`, `@php`, and any "skip escaping" directives or callbacks
- User input sources: evidence of values coming from `$request`, `request()`, or database fields written back without escaping

Decision rules:
- If raw output contains a user-controllable field and no `e()` or equivalent escaping is applied, report a risk mapped to `XSS` or a related template injection risk (map to `TPL` if your project uses template expression execution)

### 6) Signed URLs and Signature Validation Closure (AUTH or CFG)
You must locate:
- Signed URL generation: `URL::temporarySignedRoute` / `URL::signedRoute`
- Validation middleware: `middleware('signed')` or an equivalent validation mechanism

Decision rules:
- If only generation exists without signature validation middleware, or the validation logic can be bypassed, report a risk mapped to `AUTH` or `CFG`

## Observable PoC (Required: framework-specific observable verification harness)
Provide at least one of the following two categories and clearly state the observation point:
- Missing authentication / privilege bypass: give the real route and the payload target (for example switching the object id)
- Missing CSRF / CSRF bypass: give the real route and the token scenario (with and without the token) and explain the observation point

PoC output requirements:
- Must include a real route (extracted from an actually reachable location in `routes/*.php`)
- Must include real field names (such as the `csrf` field, or the form action)

## Output Completeness Check (Mandatory)
- [ ] The output contains: Laravel identification evidence points
- [ ] The six major areas (CSRF/Auth/Session/Mass Assignment/Blade raw/Signed URL) all have "check results"
- [ ] Every risk has: a mapped type code + location evidence + an observable verification harness + a remediation recommendation
