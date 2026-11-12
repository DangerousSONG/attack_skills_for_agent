---
name: php-audit-pipeline
description: Full-chain white-box code security audit pipeline for PHP web applications (multi-file orchestration). Serves as the overall orchestration reference, invoking sub-audit skills by sink type (`php-route-mapper/php-auth-audit/php-route-tracer/php-*-audit`) and reusing a unified output format and severity rating standard.
zh-signals: "编排 PHP 全链路白盒代码审计流水线并汇总子审计结果。信号:PHP代码审计,白盒审计,数据流追踪,漏洞分级,审计编排。"
when-to-use: >-
  Use when performing a full white-box security audit of a multi-file PHP project and needing to orchestrate route mapping, auth review, sink tracing, and per-vulnerability audits into one report.
---

## Runtime Dependency Notes (avoid confusion)
In its current installation form this skill is a "documentation orchestration / methodology" release and typically does not ship executable scripts (such as `scripts/*.py`) in the local repository.
When no matching executor exists in the environment, use the staged workflow described in this document (route-mapper / auth-audit / vuln-scanner / route-tracer, etc.) directly for source analysis and report generation. If you see a "searching for executor script" prompt, treat it as "no executor found, falling back to the staged degraded workflow" rather than a path error.

## Manual Equivalent Workflow Without an Executor (Recommended)
When the environment lacks an executable pipeline script or `trace` evidence is insufficient, complete the same goal manually following this "equivalent methodology": produce actionable vulnerability audit conclusions while ensuring that "exploitability and execution point" are not over-inferred.

1. Start with keyword/function anchor localization (Source/Sink)
   - Recursively traverse from the `source_path` root (not limited to specific business directories; by default still exclude `vendor/` and cache directories, adjustable as needed) to search for Source/Sink candidates.
   - For each matched sink, record: file path, function/method signature, surrounding controller/middleware/service class context, and the sink parameter variable name.

2. Then verify parameter controllability (controllability matrix)
   - Trace where the sink parameter variable comes from: e.g. `get_params()`, `request()->post()`, `$_GET/$_POST/$_REQUEST`, body (`php://input`), header/cookie.
   - Determine whether the parameter is covered by hardening before entering dangerous concatenation/execution: allowlist/enum validation, type casting, escaping/filtering, length/charset constraints, etc.
   - Output the controllability status: `✅ fully controllable / ⚠️ conditionally controllable / ❌ not controllable`, and record the code evidence location of the interception/hardening point.

3. Finally confirm the execution point (actual sink landing)
   - Confirm whether the sink parameter actually executes in a dangerous context, rather than merely being passed in and then safely handled or never actually triggered.
   - If "execution at the actual sink" cannot be proven, always mark it `⚠️ Unverified` / `🔍 Environment-Dependent`; never write `✅ Confirmed Exploitable`.

4. Output recommendations (to reduce false positives)
   - Whenever the "execution point/branch" cannot be fully proven, downgrade the conclusion to Unverified and clearly state the missing evidence points (e.g. branch condition not covered, input filtered upstream, trace-gate not satisfied, etc.).

(Optional) Example verification anchors (consistent with this audit; for reference only, not the sole criterion):
- `Db::query($sql)` / dynamic query calls: verify whether `$sql` is concatenated from user input or insufficiently validated.
- `unlink()` / `rmdir()` / `fopen()` / `opendir()`: verify the path parameter source and path traversal / relative path normalization.
- `Filesystem::putFileAs(...)`: verify whether the destination directory is controllable, web-accessible, and executable.
- `unserialize($data)`: verify whether `$data` comes directly/indirectly from user input and whether a triggerable magic method chain exists.
- `curl_exec` / `curl_setopt(CURLOPT_URL, $url)`: verify whether the URL is controllable and whether protocol/internal-network filtering exists.

# Full-Chain PHP Code Audit Pipeline (White-Box)

You are a senior white-box security auditor. Your goal is not to "find one or two dangerous spots" but to produce a security audit report actionable for remediation, using **data flow analysis + business logic validation**.

## Orchestration Notes
This pipeline follows a "split first, merge later" two-phase output strategy:

1. **Staged execution**: when each sub-skill runs independently, its output follows that skill's own output format (paths such as `routes_{timestamp}.md` and `vuln_audit/sql_{timestamp}.md` appearing in sub-skill descriptions denote logical output units, not standalone files on disk).
2. **Final merge**: in Stage 5 the pipeline orchestrator (you) merges the body content produced by all sub-skills, in stage order, into a single final summary MD file (do not create multiple category files/subdirectories).

Prefer invoking the sub-skills in this directory to audit specific vulnerability categories, assign a corresponding section heading in the final document to each sub-skill's output, and finish with "integration and quality validation".

## Sub-Audit Coverage Matrix (Mandatory)

The "Quality Report Section" in Stage 4 and Stage 5 must include a **sub-skill / audit-surface coverage matrix** (preferably near the top). **Every row** of the matrix must map one-to-one to the capabilities in the "Sub-Skill Reference Table" below (routing, authentication, trace, supply chain, and each specialized `php-*-audit`). Columns must include at least:

| Column | Meaning |
|----|------|
| Sub-skill or audit surface | Matches the name in the reference table |
| Status | **Executed** / **Not Applicable** / **Deferred** (pick one; never leave blank) |
| Trigger basis | Executed: the basis (trace-gate, static sink, config evidence, etc.); Not Applicable: **negative evidence** (e.g. no relevant API found via repository-wide search; specify the scope and ripgrep pattern); Deferred: **residual risk** and conditions for follow-up |
| Output anchor | Section heading or first sentence of the paragraph in the master report, for easy review |

**Rule**: you are not required to execute every sub-skill within a single session, but **100% of the matrix rows must have a conclusion**. "Not Applicable" and "Deferred" must meet the evidence requirements above; blank rows without justification are prohibited.

## Role and Method
### Three-Layer Analysis Method (Mandatory)
- **Surface**: pattern/keyword scanning to quickly locate high-risk areas
- **Line**: line-by-line audit tracing variable flow (Source → Sink)
- **Point**: logic validation to confirm whether the bypass/exploitation truly holds

### 10 Security Dimensions
- D1 Injection: SQL/command/LDAP/SSRF/template injection/SSTI/expression injection
- D2 Authentication: Token/Session/JWT/framework authentication chain
- D3 Authorization: privilege-bypass consistency, IDOR, RBAC/ABAC checks
- D4 Deserialization: unserialize/object injection gadget
- D5 File operations: upload/download/path traversal/arbitrary file inclusion
- D6 SSRF: URL injection, protocol restrictions, internal network access restrictions
- D7 Cryptography: key management, cipher mode, signature/validation weaknesses
- D8 Configuration: CORS/error exposure/debug switches/security headers
- D9 Business logic: race conditions, Mass Assignment, state machine flaws
- D10 Supply chain: known vulnerabilities in Composer dependencies

## Vulnerability Severity Rating (Mandatory)
### Severity Score Formula
```
Severity = f(Reachability, Impact Scope, Exploitation Complexity)
Score = R × 0.40 + I × 0.35 + C × 0.25
CVSS mapping = Score / 3.0 × 10.0
```

### Three-Dimensional Scoring Criteria (Mandatory)
- **Reachability R**
  - 3: no authentication required, directly reachable over HTTP
  - 2: requires regular user authentication
  - 1: requires admin privileges or internal network access
  - 0: code unreachable/dead code
- **Impact Scope I**
  - 3: RCE/arbitrary file write/full data exfiltration/system compromise
  - 2: sensitive data disclosure/privilege bypass/partial file read
  - 1: limited information disclosure/low-impact configuration read
  - 0: no real security impact
- **Exploitation Complexity C**
  - 3: low complexity (exploitable with a single request)
  - 2: medium complexity (requires crafting a payload or multiple steps)
  - 1: high complexity (requires a specific environment/race condition/chained exploitation)
  - 0: not exploitable (effective protection, cannot bypass)

### Severity Mapping (Mandatory)
- 🔴 C (Critical): CVSS 9.0-10.0
- 🟠 H (High): CVSS 7.0-8.9
- 🟡 M (Medium): CVSS 4.0-6.9
- 🔵 L (Low): CVSS 0.1-3.9

### Vulnerability ID Convention (Mandatory)
Format: `{severity prefix}-{type code}-{sequence number}`

Type codes (PHP edition extensions):
- `SQL`: SQL injection
- `NOSQL`: NoSQL injection
- `CMD`: command injection
- `SSRF`: SSRF
- `XSS`: cross-site scripting
- `FILE`: arbitrary file read/path traversal
- `UPLOAD`: arbitrary file upload/executable upload
- `WRITE`: arbitrary file write (path traversal to a write sink)
- `REDIR`: open redirect
- `CRLF`: CRLF/response splitting
- `XXE`: XXE
- `DESER`: deserialization/object injection
- `TPL`: template injection/SSTI
- `LDAP`: LDAP injection/query filter injection/DN injection
- `EXPR`: expression injection (non-template expression evaluation; includes eval/assert, etc.)
- `AUTH`: authentication/authorization bypass/privilege bypass (including IDOR)
- `CSRF`: CSRF
- `SESS`: session fixation/Cookie flags/JWT validation flaws/incomplete logout
- `CFG`: security configuration/CORS/error exposure/security headers/dangerous switches
- `CRYPTO`: encryption and key security flaws
- `LOGIC`: business logic flaws (Mass Assignment/race condition/state machine/flow bypass, etc.)
- `FS`: filesystem operation risks (permissions/links/deletion/TOCTOU, etc. used in chained exploitation)
- `LOG`: security logging and monitoring flaws (missing auditing/sensitive information logged/log injection, etc.)

## Key Constraints (Mandatory)
### Completeness Constraints
1. **No omissions**: no ellipsis placeholders are allowed; every list must be output item by item in full.
2. **No unreplaced templates**: every request/PoC template must be filled in with real routes and real parameters; `${var}` must not remain. For host and session fields in headers/body, use placeholders such as `{host}`/`{cookie}`/`{token}`; unreplaced `{{...}}` must not appear.
3. **No bare conclusions**: every high-risk vulnerability must include "location evidence + data flow chain + exploitability analysis + verification PoC + remediation recommendation".
4. **Non-vulnerabilities must be explained**: for suspicious patterns, provide the conclusion and evidence, e.g. "overridden by hardcoding/intercepted by validation/bypass ineffective/blind-only and unverifiable".

### Output Completeness Check (Mandatory)
Run the following checklist after completion:
- [ ] The route list and parameter list are "non-empty and equal in count" (if split across files, check each file's completeness separately)
- [ ] The authentication mapping table covers all endpoints (or explicitly marks "this endpoint is a static resource / not an entry point / has no route binding", but it must still be recorded in the table)
- [ ] Every vulnerability in the vulnerability list has: ID, severity, location, data flow chain, exploitability, verification PoC, and remediation recommendation
- [ ] No unreplaced template placeholders remain in the report (e.g. `${var}` or unreplaced `{{...}}`)

## Input
Provided by the user:
- `source_path`: path to the PHP project source (a directory or repository root)
- `output_path`: output directory path (default `{source_path}_audit`)

Derived variables (to keep sub-skill outputs aligned):
- `project_name`: extracted from the `source_path` directory name (basename)
- `timestamp`: generated timestamp, recommended format `YYYY_MM_DD_HH_mm` (example filename value: `2026_03_20_18_00`)

## Output Directory Structure (Recommended as Mandatory)
```
{output_path}/
└── {project_name}_code_audit_{timestamp}.md
```

Description:
- "File paths" such as `routes_{timestamp}.md`, `auth_mapping_{timestamp}.md`, and `vuln_audit/sql_{timestamp}.md` mentioned later only denote the corresponding section content to be written into this master report; they are not written as standalone files.
- Likewise, "read the file" becomes "reference the corresponding section content already generated in this report".
- **Path consistency with sub-skills**: paths such as `route_mapping/routes_*.md` in sub-skills are **logically equivalent** to the table above; see `shared/IO_PATH_CONVENTION.md` for details (pipeline merge vs standalone files).

## Execution Workflow (Staged Pipeline: Higher True Positive Rate)

### False-Negative Suppression (Mandatory, Applies to All Stages)

- **No silent dropping**: when `trace_status = UNRESOLVED`, when an item does not enter the `SINK_SUSPECT` heuristic list, or when the trace contract fails validation, it **must not** disappear from the report. It must be listed item by item in the **"Trace Unclosed / Pending-Evidence Risk Pool"** (or an equivalent heading) of the Stage 5 "Quality Report Section": `route_id` (or `SINK_ONLY:…`), known code location/snippet, missing evidence type, and recommended follow-up action (rerun trace, expand `high_risk_routes`, or run the matching `php-*-audit` static deep audit on that file).
- **Heuristics are not safety**: Stage 3's `SINK_SUSPECT` relies only on parameter-name keywords and **inevitably misses** paths where "the parameter name looks ordinary but still reaches a sink"; use Stage 2 (per-route data flow) + Stage 2.5 (global sink fallback) + sink scans in each sub-skill to compensate.
- **Relationship between Stage 2.5 and Stage 4**: Stage 2.5 output is always treated as **`⚠️ Unverified (static)`** until the trace or a sub-skill closes it with `EVID_*`; entries from 2.5 **must not** be removed from the master report just because they did not pass trace-gate.
- **Balancing false positives and false negatives**: without a complete trace you **must not** mark `✅ Confirmed Exploitable` (to prevent hallucination/false positives), but you must retain **`⚠️ Unverified` or `🔍 Environment-Dependent`** entries (to prevent false negatives).

### Stage 1: Reconnaissance (Recon)
Goal: identify all foundational data for "entry point → route → parameter → authentication chain".

1. **Identify the tech stack/entry-point pattern (required)**
   - Laravel: `routes/web.php`, `routes/api.php`, `app/Http/Controllers/`, middleware
   - Symfony: `config/routes/*`, Controller annotations/attributes
   - Slim: routes are defined in code (`$app->get/post`)
   - WordPress: `wp-admin/admin-post.php`, `admin-ajax.php`, hook callbacks
   - Native PHP: front controller, `index.php`, `include` chain, `$_GET/$_POST` dispatch
2. **Enumerate routes/entry points (required, no omissions)**
   - Extract from route configuration or dispatch logic: HTTP method, path/rule, corresponding handler (file/function/class method)
   - For dynamic routes (e.g. `{id}`, regex routes, WordPress parameter routes) you must document the "parsing rule and list of controllable parameters"
3. **Enumerate parameters (required)**
   - Identify sources: `$_GET/$_POST/$_REQUEST/$_FILES/$_COOKIE`, `php://input`, `getallheaders()`
   - Identify JSON: `json_decode(file_get_contents('php://input'), true)`
   - Identify files: the `$_FILES['{file_field}']` field and the origin of the file name (`name`/`tmp_name`)
4. **Identify the authentication chain and session mechanism (required)**
   - Session: `session_start()`, `$_SESSION['key']`, login-state checks
   - JWT: `JWT::decode`, signature validation logic, `Authorization: Bearer`
   - Middlewares: Laravel middleware, Symfony event listener, Slim middleware
   - Custom authentication: functions like `checkAuth()/requireLogin()/authorize()`

5. **Generate the authentication mapping (static mapping, not yet relying on trace)**
   - Invoke: `php-auth-audit`
   - Mode: `STATIC_MAPPING` (only generate `auth_mapping_{timestamp}.md` for P0/P1 route bucketing)
   - Constraint: when no `route_tracer/` trace exists yet, "missing trace contract evidence points" is allowed, but you must output "authentication status grading + P0/P1 bucketing basis"

6. **Supply chain vulnerability scan (known component CVEs/advisories)**
   - Invoke: `php-vuln-scanner`
   - Output: `vuln_report/{project_name}_composer_vuln_report_{timestamp}.md`

7. **Framework-specific audit (optional: invoke only when the framework is detected)**
   - Detection principle (required): identify Laravel/Symfony/WordPress/CodeIgniter/Yii2 from `composer.json` dependencies and typical directory/entry-file characteristics
   - Laravel: invoke `php-laravel-audit`, output `framework_audit/laravel_{timestamp}.md`
   - Symfony: invoke `php-symfony-audit`, output `framework_audit/symfony_{timestamp}.md`
   - WordPress: invoke `php-wordpress-audit`, output `framework_audit/wordpress_{timestamp}.md`
   - CodeIgniter: invoke `php-codeigniter-audit`, output `framework_audit/codeigniter_{timestamp}.md`
   - Yii2: invoke `php-yii-audit`, output `framework_audit/yii_{timestamp}.md`
   - ThinkPHP: invoke `php-thinkphp-audit`, output `framework_audit/thinkphp_{timestamp}.md`

Stage 1 output:
- `routes_{timestamp}.md`: complete route list (item by item)
- `params_{timestamp}.md`: parameter source and type/structure for each route (item by item)
- `auth_audit/auth_mapping_{timestamp}.md`: route authentication mapping (including P0/P1 bucketing basis)
- `vuln_report/{project_name}_composer_vuln_report_{timestamp}.md`: component vulnerability list (used to infer affected routes)
- `framework_audit/*_{timestamp}.md`: framework-specific audit reports (produced only when the corresponding framework is detected in Stage 1)

### Stage 2: Modeling
Goal: build a "traceable version" of the Source → Sink data flow graph.

For each route, establish at least one "shortest path from entry parameter to sensitive sink" and record:
- Source parameter name/data-structure field path (e.g. the PHP equivalent of `pageJson.orderBy`: array field path)
- Intermediate variable name changes (assignment/concat/transform)
- Branch conditions (if/switch/try/catch) and early returns (return/throw)
- Sink type and call site (file/line number/function name)

Stage 2 output:
- Route-level data flow chain evidence (recommended to embed in `vuln_audit/*` or create a separate `dataflow_tracer/`; to keep it simple, inlining into the vulnerability report is also acceptable)

### Stage 2.5: Sink-Only Global Scan Fallback (improve recall, cover RCE and extended high-risk)
Goal: when route enumeration/trace-gate fails or evidence is insufficient, still find high-risk points via "static sink hits + local controllability backtracking + execution point confirmation", and always downgrade them to `⚠️ Unverified (static evidence)` **until** Stages 3/4 supply further evidence.

> **Difference from Stages 3/4**: Stage 2.5 performs a "broad-spectrum sink pre-screening" over all PHP source files, independent of route completeness and trace completeness, and its output enters a downgraded candidate pool; Stages 3/4, after routes + traces are complete, perform "high-confidence precise auditing" of sinks that pass trace-gate. The two scan scopes may overlap, but their timing, target precision, and output destination differ — Stage 2.5 output never replaces the confirmation results of Stage 4 and serves only as a fallback for missed items.

1. Scan scope (no directory restriction)
   - Recursively traverse from the `source_path` root, covering every PHP source file in the project (e.g. `*.php`).
   - To reduce noise, exclude `vendor/` and cache directories by default (disable the exclusion strategy if maximum recall is needed).

2. **Mandatory sink set (minimum)** (prevent missed RCE/object injection)
   - CMD: `exec/system/shell_exec/passthru/proc_open/popen/pcntl_exec` and backticks `` `cmd` ``
   - EXPR: `eval/assert` and the deprecated but still common risky `preg_replace(..., ..., .../e)`
   - FILE (execution-surface boundary): when `include/require` poses a risk on the "executable content/execution boundary" (read-only is not equivalent to RCE; confirm execution semantics)
   - DESER: `unserialize(...)` has a potential magic method execution chain on a controllable input chain (escalate only when static evidence suffices; otherwise mark Unverified)
3. **Extended scan (strongly recommended; prevents missed SQL/SSRF/arbitrary read, etc.)**: on business code directories, follow `shared/PHP_SINK_REFERENCE.md` for one more pass over the **SQL execution family** (`query/exec/prepare` + concatenation clues), the **SSRF family** (`curl_exec`/`file_get_contents($url)`, etc.), and the **arbitrary read family** (`file_get_contents`/`fopen` + path concatenation). Hits are written to the same `sink_static_index_{timestamp}.md` (or appended to `rce_sinks`), tagged "extended scan"; the conclusion remains `⚠️ Unverified` until closed by a trace or by the corresponding `php-sql-audit`/`php-ssrf-audit`/`php-file-read-audit`.

4. Local analysis of each hit (must be output)
   - Location: `file:line`, function/statement, sink parameter expression (quote the key snippet verbatim)
   - Controllability backtracking: within the same file/adjacent call chain, trace whether the sink parameter comes from request input (`get/post/request()->param()`, `$_GET/$_POST/$_REQUEST`, decoded JSON `php://input`, header/cookie, etc.)
   - Execution point confirmation: if it cannot be proven that the dangerous context actually executes (e.g. branch returns early/exception skipped/filtered out), the conclusion must be downgraded to `⚠️ Unverified`

5. Output and aggregation rules (independent of route_id)
   - Output to `{output_path}/global_sink_fallback/`:
     - `rce_sinks_{timestamp}.md`: static hit list of RCE/high-risk execution points (each entry includes location, controllability backtracking evidence, execution point confirmation, and the reason for downgrade)
     - `sink_static_index_{timestamp}.md`: static hit index (for quality statistics and subsequent manual trace completion)
   - During Stage 5 aggregation: in the "Vulnerability List Overview" of the "Quality Report Section", additionally reference `global_sink_fallback/rce_sinks_{timestamp}.md` and label those items as "static evidence (non-trace-gate)".

### Stage 3: Batched Tracing (Only When Trace Proves)
Goal: use the "actual execution evidence" from `php-route-tracer` to upgrade vulnerability hunting from "keyword scanning" to "controllability and branch evidence driven", maximizing true positives.

Stage 3 must be executed in the following order:
1. **Generate the high-risk route set**:
   - Read `auth_audit/auth_mapping_{timestamp}.md` and extract P0 (❌ no authentication) and P1 (⚠️ authentication only, or 🔓 bypassable/privilege-bypass/IDOR risky routes)
   - Read `vuln_report/{project_name}_composer_vuln_report_{timestamp}.md` and "infer-map" component vulnerability trigger points related to parsing entry points/sensitive features to potentially affected routes, noting the "inference rationale"
   - Supplement `SINK_SUSPECT` routes based on static parameter clues (not relying on trace evidence points; trace-gate is the hard threshold confirmed in Stage 4)
     - LDAP: parameter name/field name contains keywords such as `dn/baseDn/filter/searchFilter/ldap/filterString` (or its JSON field path in route params)
     - EXPR: parameter name/field name contains keywords such as `expr/expression/condition/where/rule/eval` (or its JSON field path in route params)
     - SQL: parameter name/field name contains keywords such as `sql/query/filter/orderBy/sort/limit/search` (or its JSON field path in route params)
     - CMD: parameter name/field name contains keywords such as `cmd/command/exec/shell/run/path/filename` (or its JSON field path in route params)
     - SSRF: parameter name/field name contains keywords such as `url/uri/target/host/port/protocol/path` (or its JSON field path in route params)
     - FILE: parameter name/field name contains keywords such as `file/path/filename/download/view/document/template` (or its JSON field path in route params)
     - UPLOAD: parameter name/field name contains keywords such as `upload/file/tmp_name/filename/multipart` (or its JSON field path in route params)
     - WRITE: parameter name/field name contains keywords such as `write/put_contents/fwrite/fopen/rename/copy/truncate/error_log/dest/path/target/path` (or its JSON field path in route params)
     - XSS: parameter name/field name contains keywords such as `content/body/comment/title/description/html` (or its JSON field path in route params)
     - TPL: parameter name/field name contains keywords such as `template/view/engine/renderer/format/expr` (or its JSON field path in route params)
     - XXE: parameter name/field name contains keywords such as `xml/doctype/dtd/xxe` (or its JSON field path in route params)
     - DESER: parameter name/field name contains keywords such as `serialize/unserialize/payload/object/serialized` (or its JSON field path in route params)
     - NOSQL: parameter name/field name contains keywords such as `filter/query/where/operator/op/regex/whereClause` (or its JSON field path in route params)
     - REDIR: parameter name/field name contains keywords such as `next/return_to/redirect/target/url` (or its JSON field path in route params)
     - CRLF: parameter name/field name contains keywords such as `header/cookie/location/set-cookie` (or its JSON field path in route params)
     - ARCHIVE: parameter name/field name contains keywords such as `zip/tar/phar/archive/entry/extractTo/unzip/untar` (or its JSON field path in route params)
   - **Synthesize `route_id` (mandatory)**: when an entry comes from CLI/cron/queue, a WordPress hook, an `include` chain, a Stage 2.5 static sink, etc. **without an HTTP route**, use a stable ID (never leave it blank) and state on the same line the `entry_file` (relative to `source_path`), `entry_symbol` (function/method or `global`), and `trace_from` (where to start tracing toward the sink). Recommended: `ENTRY_CLI:{script identifier}`, `ENTRY_CRON:{task name}`, `ENTRY_QUEUE:{consumer class or file}`, `ENTRY_HOOK:{hook name}`, `ENTRY_INCLUDE:{file}:{symbol}`, `SINK_ONLY:{sequence}:{basename}:{line number}` (cross-reference with `sink_static_index`).
   - Output: `cross_analysis/high_risk_routes_{timestamp}.md` (contains P0/P1/SINK_SUSPECT; **every entry must have a `route_id`** (including synthetic IDs). `php-route-tracer` identifies tasks by `route_id`, and the tracing start is determined by `entry_file`+`entry_symbol`+`trace_from`; the ID is not required to look like a URI.)
2. **Generate the batched tracing plan**:
   - Read `high_risk_routes_{timestamp}.md`
   - **Batch parametrization (mandatory)**: order **P0 → P1 → SINK_SUSPECT**. `trace_batch_max_size` **defaults to 10** and can be adjusted between **5–30** per project; the plan must state the **selection rationale** (e.g. same module can be merged into a larger batch; deep call chains, many cross-file hops, a wide parameter surface, or a tight context budget call for smaller batches).
   - Every **batch** in `trace_batch_plan_{timestamp}.md` must contain: `batch_id`, the `trace_batch_max_size` used for this batch, the **selection rationale** (1–3 sentences), and an ordered list of `route_id` for the batch.
   - Output: `cross_analysis/trace_batch_plan_{timestamp}.md`
3. **Invoke the tracer in batches** (required):
   - Invoke `php-route-tracer` for each batch of routes
   - Output: `route_tracer/{route_id}/trace_{timestamp}.md`
4. **Trigger condition (hard threshold)**:
   - Only when a given sink type shows a "real sink execution point" in the trace, the trace contract passes validation, and the corresponding parameter is not marked "not controllable/no actual use (overridden by hardcoding)" in the trace's controllability matrix, may Stage 4 be entered to trigger the corresponding `php-*-audit`

5. **Trace contract validation (required)**:
   - Every trace file must contain the following sections/headings (field names must be identical; do not rename):
     - `## 7) Sink Summary`
     - `## 5) Parameter Controllability Matrix`
     - `## 6) Sink Location`
     - `## 8) Trace Completeness Statement`
     - `## 9) Sink Evidence Type Checklist`
   - If trace contract validation fails:
     - The route's trace must be marked `PARTIAL` or `UNRESOLVED`
     - For every vulnerability supported by that trace, the status must be downgraded to `⚠️ Unverified`, and `✅ Confirmed Exploitable` must not be given directly.

For the full text of sink-type anchors, dangerous patterns, and mandatory verification, see **`shared/PHP_SINK_REFERENCE.md`** in this repository (sections 3.1–3.16 plus LDAP/EXPR). When Stages 3/4 decide from the trace whether to trigger the corresponding `php-*-audit`, that file is authoritative.

Stage 3 output:
- `cross_analysis/high_risk_routes_{timestamp}.md`
- `cross_analysis/trace_batch_plan_{timestamp}.md`
- `trace_{timestamp}.md` for each traced route under `route_tracer/` (including the parameter controllability table and branch-path evidence)

### Stage 4: Sink Audit Execution (Only When Trace Proves)
Steps:
1. From the traces in `route_tracer/`, filter the vulnerability categories requiring "trace-gate" and the "actual parameter usage status" (must follow the trace controllability matrix).
   - trace-gate categories: SQL/NOSQL/CMD/SSRF/FILE/UPLOAD/WRITE/ARCHIVE/XSS/REDIR/CRLF/XXE/DESER/TPL/LDAP/EXPR/AUTH/CSRF/SESS
   - Non-trace-gate categories: CFG/CRYPTO/LOGIC/LOG (you may invoke the corresponding skill directly based on static scanning and code configuration evidence, **not** treating trace `## 9) … CFG` as the sole threshold). Note: although the `php-route-tracer` checklist includes a CFG row, it serves only as **supporting evidence**; `php-config-audit` and similar must still be executed **unconditionally as planned** in Stage 4 (unless the coverage matrix has marked them Not Applicable with negative evidence).
2. Invoke the corresponding sub-audit skill only for matched categories, satisfying the following "evidence source" rules (inference from keywords alone is prohibited):
   - If the category is trace-gate: you must reference each corresponding row of `php-route-tracer`'s `## 9) Sink Evidence Type Checklist` (FILE/UPLOAD/WRITE/ARCHIVE/SSRF/SQL/NOSQL/CMD/XSS/REDIR/CRLF/XXE/DESER/TPL/LDAP/EXPR/AUTH/CSRF/SESS) and use its evidence points as the audit basis (evidence point IDs must match verbatim)
   - If the category is `AUTH`: invoke `php-auth-audit` in `TRACE_AUDIT` mode (you must reference trace evidence point IDs)
3. For each suspected vulnerability, you must output the "exploitability preconditions":
- Authentication requirement: ✅ none / ⚠️ login required / ❌ not exploitable threshold
- Input controllability: ✅ fully controllable / ⚠️ conditionally controllable / ❌ not controllable (overridden by hardcoding)
- Trigger condition: branch condition/exception path/environment dependency (database type, network reachability)

4. **Trace completeness fallback rules (required)**:
   - If trace_status = PARTIAL: only `⚠️ Unverified` mode is allowed (do not give `✅ Confirmed Exploitable` directly)
   - If trace_status = UNRESOLVED: **silent false-negative reporting is prohibited** — do not write "no risk" or let it disappear from the report. You must add a separate entry for that `route_id` in the master report's **"Trace Unclosed / Pending-Evidence Risk Pool"**: `known snippet` (from the reachable part of the trace), `missing evidence`, `recommended next step` (complete the trace / include it in `SINK_ONLY` static deep audit / invoke the corresponding `php-*-audit`). If the route can be correlated with a Stage 2.5 static hit, provide a cross-reference.

5. **Filesystem operation audit (non-trace-gate, static-evidence driven)**:
   - Invoke: `php-filesystem-audit`
   - Output: `vuln_audit/fs_{timestamp}.md`
   - Decision rule: you may output `✅/⚠️/❌/🔍` directly based on a source-located "filesystem operation evidence chain + path control source + TOCTOU/link bypass explanation", without treating `php-route-tracer`'s evidence contract fields as a prerequisite hard threshold

And finally provide:
- Status: ✅ Confirmed / ⚠️ Unverified / ❌ Not Exploitable / 🔍 Environment-Dependent
- Severity and CVSS mapping (per the formula above)

### Stage 5: Summary Report (Report)
Generate a "Quality Report Section" in the master report, containing:
- **Sub-skill / audit-surface coverage matrix**: same structure as "Sub-Audit Coverage Matrix (Mandatory)" above, placed near the top of the quality report; it must be consistent with the actual Stage 4 execution and must not contradict it.
- Risk statistics table (🔴/🟠/🟡/🔵 counts and CVSS ranges)
- Vulnerability list overview (reference each corresponding vulnerability detail paragraph in this report item by item)
- **"Trace Unclosed / Pending-Evidence Risk Pool"** (mandatory): aggregate the `route_id`s with `trace_status ∈ {PARTIAL, UNRESOLVED}`, the entries in the Stage 2.5 `sink_static_index` not yet closed by a trace, and the "extended scan" hits; place it alongside the "Vulnerability List Overview"; **deleting records due to insufficient evidence is prohibited** (unclosed ≠ no risk).
- Coverage: route coverage, authentication coverage, sink coverage, key branch coverage (use "completed/to be supplemented" rather than omission; recommended thresholds: route coverage and sink coverage >= 90%)
- Framework-specific audit summary: if `framework_audit/*.md` exists, map its risks to the unified type codes (AUTH/CSRF/TPL/XSS/SQL/LOGIC/CFG/SESS/SSRF/…), count quantities and the highest severity, and note in the summary "which framework_audit report files the framework risks come from"

  > **Framework audit exemption note**: framework-specific audits (Laravel/Symfony/WordPress/CodeIgniter/Yii2/ThinkPHP) are "static configuration/pattern matching" audits; their identified risks do not need trace-gate validation by `php-route-tracer` or evidence validation via `## 9) Sink Evidence Type Checklist`. Framework audit results are rated by their own rules and mapped directly to the unified type codes.
- Evidence Completeness score: for all trace-gate sink types (FILE/UPLOAD/WRITE/ARCHIVE/SSRF/SQL/NOSQL/CMD/XSS/REDIR/CRLF/XXE/DESER/TPL/LDAP/EXPR/AUTH/CSRF/SESS), count against the evidence point ID sets defined in `shared/EVIDENCE_POINT_IDS.md`: `coverage% = satisfied evidence points / total required evidence points for the type × 100%`; also list the missing evidence point IDs (must match verbatim) and the reason for each gap (e.g. trace_status=PARTIAL/UNRESOLVED, evidence point location failed, parameter not controllable, etc.).

Stage 5.1: Exploit Chain Aggregation (Mandatory)
- Invoke: `php-exploit-chain-audit`
- After the "Vulnerability List Overview" in the "Quality Report Section", add an "Exploit Chain Aggregation Section": reference the chain overview table and shortest exploit chain from the exploit chain aggregation report (reference only; do not duplicate content).

## Vulnerability Detail Template (Mandatory)
Every vulnerability must follow this structure (written into the vulnerability detail section of this master report):
```markdown
### [{severity prefix}-{type code}-{sequence number}] {risk title}

| Item | Information |
|------|------|
| Severity Level | {🔴/🟠/🟡/🔵} (CVSS {score}) |
| Reachability (R) | {0-3} - {rationale} |
| Impact Scope (I) | {0-3} - {rationale} |
| Exploitation Complexity (C) | {0-3} - {rationale} |
| Exploitability | ✅ Confirmed / ⚠️ Unverified / ❌ Not Exploitable / 🔍 Environment-Dependent |
| Location | {file path}:{line number} ({function/method}) |

#### Data Flow Chain (Source → Sink)
```
(write out assignment/passing/concatenation/validation/branching line by line for the route; no omissions)

#### Exploitability Preconditions
- Authentication Requirement: {none / login required / specific privilege required}
- Input Controllability: {fully controllable / conditionally controllable / not controllable}
- Trigger Condition: {branch / exception / environment-dependent}

#### Verification PoC (an executable request is mandatory)
```http
{HTTP Method} {full path with query/body} HTTP/1.1
Host: {host}
{required Header/Session/JWT/Cookie}

{Payload}
```

#### Recommended Fix
- Focus on "code replacement recommendations" (give the key points of the secure implementation)
- Provide search statements (bash/rg form) for "how to search the code to check for missed fixes"
```

## Documentation (Audit READMEs)
The following appendix sections must be generated within this master report:
- How to identify PHP routes and parameters
- How to identify sessions/JWT and audit the authentication chain
- How to use `shared/PHP_SINK_REFERENCE.md` for per-type sink hunting and trace-gate alignment

## Self-Check and Quality Assurance (Mandatory)
Before marking complete, answer and self-check:
- [ ] Does the "Sub-skill / audit-surface coverage matrix" give Executed/Not Applicable/Deferred for **every row** of the reference table, with trigger basis or negative evidence attached for Not Applicable and Deferred?
- [ ] Did I cover the common high-risk categories (SQL/NOSQL/CMD/SSRF/XSS/FILE/UPLOAD/WRITE/ARCHIVE/XXE/DESER/TPL/AUTH/CSRF/REDIR/CRLF/SESS/CRYPTO/CFG/LOG/FS) per `shared/PHP_SINK_REFERENCE.md` and the trace results?
- [ ] Did I cover LDAP/EXPR (or has "Not Applicable" in the matrix been backed by negative evidence)?
- [ ] Does every vulnerability have a data flow chain and exploitability preconditions?
- [ ] Is there any abbreviated wording?
- [ ] Are there any unreplaced template placeholders?
- [ ] Does the **"Trace Unclosed / Pending-Evidence Risk Pool"** list all `PARTIAL/UNRESOLVED` entries and unclosed Stage 2.5 static hits, without contradicting the vulnerability list?

## Sub-Skill Reference Table (Capability list + Matrix alignment)
The table below is the **list of rows that must appear in the "sub-skill / audit-surface coverage matrix"**. Stages 3/4 trigger the corresponding skill based on trace-gate and static evidence; rows that are **not executed** must be marked "Not Applicable" or "Deferred" in the matrix and satisfy the matrix column requirements (blank rows and unjustified skips are prohibited).

1. Routing/parameters: `php-route-mapper`
2. Authentication: `php-auth-audit`
3. Deep tracing: `php-route-tracer` (used in any scenario requiring controllability/branch evidence)
4. Component vulnerabilities (supply chain): `php-vuln-scanner`

5. Exploit chain aggregation: `php-exploit-chain-audit` (mandatorily invoked in Stage 5.1)

6. Filesystem operation audit: `php-filesystem-audit` (executed in Stage 4, driven by static evidence)

Invoke by vulnerability category:
- SQL injection: `php-sql-audit`
- NoSQL injection: `php-nosql-audit`
- Command injection: `php-cmd-audit`
- SSRF: `php-ssrf-audit`
- XSS: `php-xss-audit`
- Template injection/SSTI: `php-tpl-audit`
- LDAP injection: `php-ldap-audit`
- Expression injection (non-template): `php-expr-audit`
- Arbitrary file read/path traversal: `php-file-read-audit`
- File upload: `php-file-upload-audit`
- Arbitrary file write: `php-file-write-audit`
- Archive extraction path traversal/Zip Slip: `php-archive-extract-audit`
- XXE: `php-xxe-audit`
- Deserialization/object injection: `php-deser-audit`
- Authentication/authorization bypass/privilege bypass/IDOR: `php-auth-audit` (folded into the summary along with authentication status and resource ownership)
- CSRF: `php-csrf-audit`
- Open redirect: `php-open-redirect-audit`
- CRLF/response splitting: `php-crlf-audit`
- Session and Cookie security: `php-session-cookie-audit`
- Encryption and key security: `php-crypto-audit`
- Security configuration (CORS/error exposure/security headers/dangerous switches): `php-config-audit`
- Business logic flaws (Mass Assignment/race condition/state machine/flow bypass): `php-logic-audit`
- Security logging and monitoring: `php-logging-audit`