---
name: php-route-tracer
description: "Multi-layer data flow tracing tool from PHP web routes to sinks. Given a user-specified route, trace from the handler to the final sensitive operation point and output layered evidence, parameter variable tracing, and controllability analysis (no vulnerability conclusions)."
zh-signals: "追踪 PHP 路由从 handler 到敏感 Sink 的多层数据流与参数可控性。信号:PHP路由追踪,数据流分析,Sink定位,参数可控性,调用链。"
when-to-use: >-
  Use when tracing a specified PHP route or synthetic entry from handler to sink, mapping parameter flow and branches, and producing controllability evidence without issuing a vulnerability conclusion.
---

# PHP Route Tracer (data flow tracing, no vulnerability conclusions)

Based on the routes from `php-route-mapper` (or the synthetic entry points provided by `php-audit-pipeline`), trace from the **handler / CLI entry / specified symbol** to the final Sink (SQL/command/file/SSRF/XSS/template rendering/deserialization, etc.), and output the complete data flow chain, parameter variable name changes, and controllability analysis.

## CRITICAL: Output tracing only, no vulnerability recommendations
- Do not provide "vulnerability conclusions / severity ratings / CVSS / remediation recommendations"
- Output only: data flow chain evidence, branch execution paths, sink locations, and the parameter controllability determination table (controllability is not a vulnerability conclusion)

## Input Dependencies
- `routes_{timestamp}.md`: route definitions (when written to disk independently, usually `route_mapping/routes_{timestamp}.md`; see `shared/IO_PATH_CONVENTION.md`)
- `params_{timestamp}.md`: parameter structure (when written to disk independently, usually `route_mapping/params_{timestamp}.md`)
- `source_path`: source code root directory
- `route_id`: from `cross_analysis/high_risk_routes_{timestamp}.md`; may be an HTTP route index, or the **synthetic ID from `php-audit-pipeline` stage 3** (`ENTRY_CLI:` / `ENTRY_CRON:` / `ENTRY_QUEUE:` / `ENTRY_HOOK:` / `ENTRY_INCLUDE:` / `SINK_ONLY:` etc.)
- **Synthetic entry point (mandatory for non-HTTP tasks)**: `entry_file` (relative to `source_path`), `entry_symbol` (function/method or `global`), `trace_from` (description of where to start tracing toward the sink)

## Tracing Scope (Mandatory)
1. The handler entry point (controller method / closure function / the final processing function of the middleware); for **non-HTTP tasks**, use `entry_file` + `entry_symbol` from the input as the tracing start point (see "Input Dependencies")
2. Where request parameters enter the handler (request retrieval, JSON decoding, extraction of $_GET/$_POST)
3. How parameters are passed between functions/methods (assignment, array field access, object property access)
4. Branch conditions (if/switch/try/catch/return/throw) and early exit points
5. The call site of the final Sink and the argument position (function call argument name/position)

## Output File Structure (Recommended)
```
{output_path}/route_tracer/
└── {route_id}/
    ├── trace_{method}_{timestamp}.md
    └── trace_all_{timestamp}.md
```
Description: **HTTP routes**: `route_id` should match the index `N` of `=== [N] {route_summary} ===` in the `routes_{timestamp}.md` produced by `php-route-mapper`. **CLI / hook / sink-only etc.**: use the pipeline synthetic `route_id`, and the tracing start point is the `entry_file` + `entry_symbol` + `trace_from` from the input, with no requirement to correspond to a URI.

## Single-Route Report Template (Mandatory)
```markdown
# Route Call Trace

Traced route: {HTTP_METHOD} {route_rule}
Generated at: {timestamp}
Project path: {source_path}

---
## 1) Complete Request Template (from route-mapper)
```http
{complete request template}
```

---
## 2) Parameter Entry Points
| Parameter | HTTP Source | Variable/Field Entering the Handler | Location |
|------|----------|-----------------------------|------|
|      |          |                             |      |

---
## 3) Call Chain Layered Evidence (level by level, nothing omitted)
Level-1: {file}:{line} {Function/Class}.{method}({args})
Key code:
```php
// Show the key fragment that passes the parameter to the next level
```

Level-2: {file}:{line} {Function/Class}.{method}({args})

---
## 4) Branch Path Tracing (Branch Execution Proof, mandatory output)
path A:
Condition: {summary of the if/switch/try/catch/return/throw condition}
Execution: {summary of how the parameter continues to flow to the Sink under this branch}
Sink: executed = Yes/No

path B:
Condition: {summary of the other branch condition}
Execution: {summary of parameter handling / early exit under the other branch}

---
## 5) Parameter Controllability Matrix (Controllability Matrix, mandatory field names and columns must match)
| Parameter | HTTP/Body Field | Preprocessing/Normalization | Sink Type | Coverage Type | Coverage Condition | BlockReason (if any) | Controllability Conclusion (✅/⚠️/❌) | Actually Used (Yes/No) | Controllable Scenario |
|------|------------------|------------------|-----------|-----------|-----------|--------------------|----------------------|------------------|----------|

---
## 6) Sink Location (Sink Parameter Mapping, mandatory field names and columns must match)
| Sink Type | Function/Method | Call Site (file:line) | Sink Argument Name/Position | Parameter Mapping (sink argument <- controllable parameter) | Evidence (key code fragment) |
|----------|-----------|-------------------|-------------------|----------------------------------------------|----------------------|
```

## 7) Sink Summary (mandatory: used for the pipeline hard-gate validation)
Must output a summary table (must not be omitted):
| route_id | Sink Type | Sink Function/Statement | Executed (Yes/No) | Triggered Branch (condition summary) | Related Parameters (from the controllability matrix) | Evidence (code fragment) |
|----------|---------|---------------|----------------|--------------------|------------------------------|----------------------|

---
## 8) Trace Completeness Statement (mandatory)
| trace_status | Meaning |
|-------------|------|
| COMPLETE | Call chain and sink evidence are complete and parameter controllability can be determined |
| PARTIAL | Only partial chain evidence or incomplete branch evidence, but the sink exists or part of the parameter flow can be proven |
| UNRESOLVED | No explicit sink can be located or there is insufficient controllability evidence |

And provide:
- List of missing items (missing items must be enumerated one by one: call chain levels / branches / mapping / evidence)
- Fallback recommendation (allowed fallbacks: re-run the tracer or enter the ⚠️ pending-verification mode of the corresponding sub-skill)

## Mandatory Prohibitions
- Do not omit call chain levels with ellipses
- Do not leave template variables unreplaced (e.g. `${route}` not replaced with the real route_id)
- Do not conflate "not controllable" with "no risk": this skill only outputs controllability, never vulnerability conclusions

## 9) Sink Evidence Type Checklist (mandatory: used for the pipeline hard gate)
This checklist must be output in every trace report (content may be empty, but the heading and table header must exist; and for each sink actually hit, write out the evidence source and evidence fragment).

| Sink Type | Required Evidence Points (evidencible fragments from code/config) | Evidence Location |
|----------|----------------------------------------------------|----------|
| FILE | `EVID_FILE_WRAPPER_PREFIX`: how wrapper/stream wrapper prefixes (e.g. `php://`/`phar://`/`zip://`) are used; `EVID_FILE_RESOLVED_TARGET`: the final resolved result of the included/read file (resolved target); `EVID_FILE_INCLUDE_REQUIRE_EXEC_BOUNDARY`: the execution boundary of include/require (whether PHP code is really executed or only read for an error) | file:line |
| WRITE | `EVID_WRITE_WRITE_CALLSITE`: evidence of the write/destination-change call site (e.g. `file_put_contents`/`fwrite`/`fopen(...,'w')`/`rename`/`copy`); `EVID_WRITE_DESTPATH_JOIN_AND_NORMALIZATION`: evidence of destination path joining and normalization (base join, sanitization/traversal rejection fragments, realpath prefix validation, etc.); `EVID_WRITE_DESTPATH_RESOLVED_TARGET`: the final resolved write target and evidence of base constraint escape determination; `EVID_WRITE_CONTENT_SOURCE_INTO_WRITE`: mapping evidence between the written content argument and user-controllable input; `EVID_WRITE_TRUNCATE_OR_OVERWRITE_MODE`: evidence of overwrite/truncate/append mode (write mode or overwrite strategy); `EVID_WRITE_EXECUTION_ACCESSIBILITY_PROOF`: executability/reachability evidence after the write (web root / includable directory / execution-disabled policy, etc.) | file:line |
| UPLOAD | `EVID_UPLOAD_DESTPATH`: the final save directory destination (destPath); `EVID_UPLOAD_FILENAME_EXTENSION_PARSING_SANITIZE`: file name/extension parsing and sanitization logic; `EVID_UPLOAD_ACCESSIBILITY_PROOF`: whether an accessible surface is created after the write (direct static access evidence / mapping evidence); `EVID_UPLOAD_EXEC_DISABLE_STRATEGY`: server-side execution disable strategy (if any) | file:line |
| ARCHIVE | `EVID_ARCHIVE_EXTRACT_CALLSITE`: the location of the archive extraction call site (e.g. `ZipArchive->extractTo/->extract`, `PharData->extractTo`); `EVID_ARCHIVE_ENTRY_NAME_SOURCE`: evidence of the source of extracted entry names/paths (entry name/path inside the archive or an entry list constructed from user input); `EVID_ARCHIVE_ENTRY_SANITIZATION`: evidence of entry path sanitization/normalization (removing `../`, absolute paths, Windows drive letters, and other path traversal characters); `EVID_ARCHIVE_EXTRACT_BASE_DIR`: evidence of the extraction base directory argument; `EVID_ARCHIVE_FINAL_TARGET`: the final resolved target path (resolved target after base + entry join) and the base directory constraint determination evidence (if present) | file:line |
| SSRF | `EVID_SSRF_URL_NORMALIZATION`: URL normalization steps; `EVID_SSRF_FINAL_URL_HOST_PORT`: the final URL/Host/Port before the request is issued; `EVID_SSRF_FINAL_REDIRECT_URL`: evidence of the final address after redirects (final URL) if redirects are followed; `EVID_SSRF_DNSIP_AND_INNER_BLOCK`: evidence of DNS/IP resolution and internal network blocking determination | file:line |
| SQL | `EVID_SQL_EXEC_POINT`: the location of the SQL execution function/statement (e.g. `$pdo->query/exec/prepare` or `mysqli_query` / ORM execution point); `EVID_SQL_STRING_CONSTRUCTION`: the location of SQL string construction/concatenation; `EVID_SQL_USER_PARAM_TO_SQL_FRAGMENT`: mapping from user-controllable parameters to SQL fragments (corresponds to a field in the controllability matrix) | file:line |
| NOSQL | `EVID_NOSQL_QUERY_CONSTRUCTION`: the NoSQL query construction point (find/update/delete or query builder); `EVID_NOSQL_USER_INPUT_INTO_QUERY_STRUCTURE`: evidence of user input entering the query condition structure (controllable fields entering the filter/where structure); `EVID_NOSQL_OPERATOR_INJECTION_FIELDS`: operator injection field evidence ($ne/$gt/$or/$where/$regex, etc.) | file:line |
| CMD | `EVID_CMD_EXEC_POINT`: the location of the command execution function/statement (e.g. `exec/system/shell_exec/passthru` or `proc_open/popen/pcntl_exec`); `EVID_CMD_COMMAND_STRING_CONSTRUCTION`: the location of command string/key argument construction (concatenation/templating); `EVID_CMD_USER_PARAM_TO_CMD_FRAGMENT`: mapping from user-controllable parameters to command fragments | file:line |
| XSS | `EVID_XSS_OUTPUT_POINT`: the location of the response output point (echo/printf/template rendering output/`<script>`/attribute/URL context); `EVID_XSS_USER_INPUT_INTO_OUTPUT`: evidence of user input entering the output; `EVID_XSS_ESCAPE_OR_RAW_CONTROL`: escaping/escaping-disabled evidence (e.g. correct escape or a raw output disable point) | file:line |
| REDIR | `EVID_REDIR_OUTPUT_POINT`: the location of the redirect output point (`header(Location={location})`/redirect/return_to); `EVID_REDIR_DEST_SOURCE_MAPPING`: mapping evidence for the source variable of the destination; `EVID_REDIR_DEST_VALIDATION_NORMALIZATION`: branch evidence of destination validation/normalization/allowlist/scheme rejection (including encoded bypass handling evidence) | file:line |
| CRLF | `EVID_CRLF_OUTPUT_POINT`: the location of the response header/Cookie output point (header/setcookie); `EVID_CRLF_USER_INPUT_INTO_HEADER_COOKIE`: evidence of user input entering header/cookie values; `EVID_CRLF_CONTROL_CHAR_FILTERING_ENCODING`: evidence of `\r\n` or control character filtering/encoding | file:line |
| XXE | `EVID_XXE_PARSER_CALL`: the location of the XML parser call site (DOMDocument->loadXML/simplexml_load_string/XMLReader->open); `EVID_XXE_INPUT_SOURCE`: evidence of the input stream source (php://input/upload read/parameters); `EVID_XXE_ENTITY_DOCTYPE_SAFETY_AND_ECHO`: evidence of security options related to disabling external entities/DOCTYPE + the location where parsing results are echoed | file:line |
| DESER | `EVID_DESER_CALLSITE`: the location of the deserialization call site (`unserialize` etc.); `EVID_DESER_INPUT_SOURCE`: evidence of the user-controllable source of the input argument; `EVID_DESER_OBJECT_TYPE_MAGIC_TRIGGER_CHAIN`: evidence of the post-deserialization object type/magic method trigger conditions + evidence of the chain to the final sensitive operation point (if locatable) | file:line |
| TPL | `EVID_TPL_ENGINE_RENDER_OR_PARSE_ENTRY`: the location of the template engine rendering/expression parsing point; `EVID_TPL_TEMPLATE_OR_EXPR_CONTROL`: evidence of whether the template name or expression is controllable; `EVID_TPL_EXEC_CHAIN_ENTRY`: evidence of the execution chain entry point (expression evaluation/compilation/execution) and the disabling/sandboxing policy (if any) | file:line |
| LDAP | `EVID_LDAP_EXEC_POINT`: the location of LDAP query/read/enumerate execution functions/statements; `EVID_LDAP_FILTER_STRING_CONSTRUCTION`: the location of LDAP filter/query condition string construction/concatenation; `EVID_LDAP_USER_PARAM_TO_FILTER_FRAGMENT`: mapping evidence from user-controllable parameters to LDAP filter/DN fragments | file:line |
| EXPR | `EVID_EXPR_EVAL_ENTRY`: the entry point of expression parsing/compilation/evaluation; `EVID_EXPR_EXPR_CONTROL`: evidence of whether the expression string is controllable; `EVID_EXPR_EXEC_CHAIN_ENTRY`: evidence of the execution chain entry point (the evaluation result further entering sensitive semantics, or the final evaluation execution point) | file:line |
| AUTH | `EVID_AUTH_PATH_PROTECTED_MATCH`: path matching evidence for the route entering the protected handler; `EVID_AUTH_TOKEN_DECODE_JUDGMENT`: evidence of how the login state/token decode result is judged; `EVID_AUTH_PERMISSION_CHECK_EXEC`: execution evidence of the permission check function or conditional statement (e.g. hasRole/authorize); `EVID_AUTH_IDOR_OWNERSHIP_CONDITION`: evidence of whether the IDOR/ownership check (WHERE/condition) includes owner_id/user_id | file:line |
| CSRF | `EVID_CSRF_STATE_CHANGE_HANDLER_EXEC`: execution evidence of the state-changing handler (branch path evidence from the trace); `EVID_CSRF_TOKEN_SOURCE`: evidence of the CSRF token source and generation (session/cookie/random); `EVID_CSRF_TOKEN_RECEIVE`: evidence of the location where the CSRF token is received from the request / enters validation logic; `EVID_CSRF_TOKEN_VERIFY`: location and early-exit evidence of the backend validation comparison/hash judgment; `EVID_CSRF_BYPASS_BRANCH`: bypass branch evidence (e.g. only validating a specific Content-Type / only validating AJAX / a branch that does not validate) | file:line |
| SESS | `EVID_SESS_SESSION_INIT_REGEN`: evidence of session fixation protections such as `session_regenerate_id` after login; `EVID_SESS_COOKIE_FLAGS`: evidence of Cookie flag settings (HttpOnly/Secure/SameSite); `EVID_SESS_JWT_VERIFY_CLAIMS`: evidence of JWT signature algorithm pinning and exp/nbf/iss/aud claim validation; `EVID_SESS_LOGOUT_CLEAR`: evidence of whether logout truly clears the session and the token | file:line |
| CFG | `EVID_CFG_CONFIG_LOCATION`: evidence of the config file/environment variable location (.env/config/php.ini/Dockerfile etc.); `EVID_CFG_RUNTIME_SETTING_CODE`: evidence of the location of runtime setting code (ini_set/set_exception_handler/security middleware etc.); `EVID_CFG_IMPACT_ASSOCIATION`: impact association evidence (which routes/responses are affected by this configuration); `EVID_CFG_SECURITY_SWITCH_EVIDENCE`: evidence of key configurations such as security headers/error exposure/CORS/dangerous switches | file:line |


