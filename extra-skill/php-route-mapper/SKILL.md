---
name: php-route-mapper
description: "PHP web source code route and parameter mapping analysis tool. Extracts every entry route and parameter structure from the source code and outputs complete request templates with a parameter inventory (omissions are not allowed)."
zh-signals: "从 PHP 源码提取完整路由与参数结构，生成请求模板与参数清单。信号:php路由,参数映射,源码分析,请求模板,路由提取,burp"
when-to-use: >-
  Use when you need to map all HTTP routes and request parameters from PHP source code into
  complete request templates for security testing.
---

# PHP Source Code Route & Param Mapper

Analyze PHP web project source code, extract **complete** HTTP route entries and request parameter structures, generate request templates usable for security testing (Burp/Repeater style), and save them automatically as Markdown.

## CRITICAL: Complete Output (Mandatory)
This skill must output every discovered route and endpoint; omissions are not allowed:
- No elision placeholders are allowed; the full route and parameter content must be output
- Do not output only "key routes / important routes"
- Every route must include: HTTP method, path rule, handler location, complete parameter structure, and a complete request template (inside a code block)

## Core Input
Provided by the user:
- `source_path`: root directory of the PHP project source code
Optional:
- `context_path`: if a reverse proxy / gateway prefix exists, it can be used to build the full path (must have an evidence source)

## Output Directory Structure (Recommended)
```
{output_path}/
├── route_mapping/
│   ├── routes_{timestamp}.md
│   └── params_{timestamp}.md
└── quality/
    └── route_mapper_validation_{timestamp}.md
```

The mapping between paths and the pipeline merge mode is described in **`shared/IO_PATH_CONVENTION.md`** (`route_mapping/*.md` is equivalent to the "Routes / Parameters" section of the report).

## Detection Scope (Mandatory)
1. Route configuration / definitions (identified per framework)
   - Laravel: `routes/web.php`, `routes/api.php`, `Route::get/post/{subpath}`, `Route::resource`, Route group prefixes and middleware
   - Symfony: `config/routes/*`, PHP8 attribute `#[Route({route_options})]`, Annotation `@Route({route_options})`
   - Slim: `$app->get/post/any({handler})`, custom middleware
   - WordPress: `admin-post.php`/`admin-ajax.php`, `add_action('admin_post_*')`, `add_action('wp_ajax_*')`
   - Plain PHP: front controller (e.g. `public/index.php`) dispatch logic, route matching based on `$_SERVER['REQUEST_URI']`
2. Dynamic / parameterized routes (mandatory)
   - `{id}` / `(?P<id>{id_pattern})` / regex routes: controllable parameters must be listed explicitly
   - Route constraints (where / regex limit): the constraint rules and controllability boundaries must be output

## Parameter Structure Analysis (Mandatory)
For each route, output the following parameter sources and type information:
- Path parameters: placeholders taken from the route rule (output like `{id}`)
- Query parameters: `$_GET` / `request()->query({query})` / framework query parsing result
- Body parameters: `php://input`, `$_POST`, JSON `json_decode({json})`
- Header parameters: `getallheaders()`, `$_SERVER[{value}]`, framework request header API
- Cookie parameters: `$_COOKIE`
- File parameters: `$_FILES` (output the field name and the filename source)

## Handler Location (Mandatory)
Every route must provide evidence of its handler source:
- File path (relative or absolute are both fine, but must be consistent)
- Function / class / method signature (names that can be located in the source code)
- Key dispatch point: how the route match enters the handler (e.g. switch case / include file chain)

## Output Format (Mandatory)
### `routes_{timestamp}.md`: main index (listed one by one)
Description: this skill uses the `N` in `=== [N] {route_summary} ===` inside `routes_{timestamp}.md` as the `route_id` of the **HTTP route** (the pipeline later uses it to bucket files into `route_tracer/{route_id}/trace_{timestamp}.md`). Synthetic `route_id` values such as **CLI / hook / sink-only** are written by `php-audit-pipeline` stage 3 into `high_risk_routes_{timestamp}.md` and **do not** consume the `[N]` sequence number in this file.
```markdown
# {project_name} - Route and Endpoint Index (PHP)
Generated at: {timestamp}
Analysis path: {source_path}

## Route Inventory (All)
=== [1] GET /path/to/{id} ===
HTTP method: GET
Route path rule: /path/to/{id}
Handler: ControllerClass@method / functionName
Location: path/to/file.php:line (if the line number cannot be obtained, mark "to be located: manual file review required" but still give the file path)
Parameter overview:
  Path: id (type inference / constraint)
  Query: {query_params}

=== [2] POST /path/to/{id}/action ===
HTTP method: POST
Route path rule: /path/to/{id}/action
Handler: ControllerClass@action / functionName
Location: path/to/file.php:line (if the line number cannot be obtained, mark "to be located: manual file review required" but still give the file path)
Parameter overview:
  Path: id (type inference / constraint)
  Query: {query_params}
```

### `params_{timestamp}.md`: parameter details (listed one by one)
```markdown
# {project_name} - Route Parameter Structure (One by One)
Generated at: {timestamp}

=== Route: GET /path/to/{id} ===
1) Path parameters
| Parameter | Type / Constraint | Location | Required |
|------|------------|------|------|
| id   | int/regex{id_pattern} | Router rule | Yes / No / Uncertain |

2) Query parameters
| Parameter | Type | Source | Required | Description |

3) Body parameters (e.g. JSON)
| Field | Type | JSON path | Required |

4) Header / Cookie / File (if any)
| Field | Type | Source | Required |

5) Complete request template (must be inside a code block)
```http
GET /path/to/{id}?a={a}&b={b} HTTP/1.1
Host: {host}
Cookie: {cookie}
Authorization: Bearer {token}
Content-Type: application/json

{"k":"{v}"}
```
```

## Self-Check Before Output (Mandatory)
- [ ] The "index / route identifier" of every route is consistent between routes and params
- [ ] No elision placeholders appear
- [ ] Every route has a "complete request template" code block
