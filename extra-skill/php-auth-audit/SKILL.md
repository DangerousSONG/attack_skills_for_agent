---
name: php-auth-audit
description: PHP web source code authentication and authorization mechanism audit tool. Identify every authentication/authorization implementation in the source code and analyze the risk, then output a route-to-auth mapping and vulnerability analysis (with PoC and remediation recommendations).
zh-signals: "PHP 源码鉴权机制审计技能，识别认证授权链路、路由鉴权状态与越权/IDOR 风险。信号:鉴权审计,认证绕过,越权,IDOR,路由映射"
when-to-use: "Use when auditing PHP web application source code for authentication and authorization flaws, mapping each route's auth status, or detecting bypass, IDOR, and privilege escalation risks."
---

# PHP Authentication and Authorization Mechanism Audit (Auth Audit)

Analyze PHP web project source code, identify the authentication and authorization chains, determine the auth status of every route, and detect auth bypass / privilege bypass / IDOR risks.

## CRITICAL: Complete Analysis (Mandatory)
- Every route that appears in `php-route-mapper` must be processed
- The authentication chains must be identified: session/JWT/middleware/custom validation functions
- The route-to-auth mapping table must be output (no omissions)
- For every suspicious point provide: location evidence + data flow chain + exploitability analysis + verification PoC + remediation recommendation

## Run Modes (Mandatory: aligned with the pipeline stages)
This skill supports two modes, which exist to solve the problem of "referencing EVID_* before the trace has been generated":

1. `STATIC_MAPPING` (recommended for pipeline stage 1)
   - Only generates `auth_mapping_{timestamp}.md` (and optionally `auth_README_{timestamp}.md`)
   - Allows missing `EVID_*` evidence point references from `php-route-tracer`
   - Must provide: the auth status rating (✅/⚠️/❌/❓) and the P0/P1 bucketing rationale (no PoC required)

2. `TRACE_AUDIT` (recommended for pipeline stage 4, when the trace already exists)
   - Generates the complete `auth_audit_report_{timestamp}.md`, and must cite the `EVID_*` evidence points from the trace contract item by item
   - PoC and remediation recommendations must be complete

## Vulnerability Severity Rating
See: `shared/SEVERITY_RATING.md`

## Input Dependencies
Recommended inputs (consistent with `shared/IO_PATH_CONVENTION.md`; when merging into the pipeline, read the equivalent section in the summary report):
- `routes_{timestamp}.md` (when written independently it is usually `route_mapping/routes_{timestamp}.md`)
- `params_{timestamp}.md` (when written independently it is usually `route_mapping/params_{timestamp}.md`)

Optional:
- `source_path`

## Identifying Authentication Implementations (Mandatory)
Identify by framework:
- Laravel:
  - `middleware('auth'|'can'|'role:')`
  - `Auth::check()/Auth::user()`
  - Policies/Gates: `Gate::allows`, `->can({value})`
  - Route protection: `Route::middleware([{value}])->group({value})`
- Symfony:
  - security.yaml / access_control
  - `denyAccessUnlessGranted`, `isGranted`
  - voter/policy
- Native PHP:
  - `session_start` plus a `$_SESSION` check
  - `if (!isset($_SESSION['user']))`/`requireLogin()`
  - Custom functions: `checkAuth/authorize/hasRole/isAdmin`

## Route-to-Auth Mapping (Mandatory)
Output the following status for every route:
- ✅ Public: explicitly allowed, no auth check
- ✅ Protected: a complete authentication/authorization check exists
- ⚠️ Authenticated only: only the login state is verified, with no role/resource-level authorization
- ❌ No auth: no auth chain matches at all
- ❓ Uncertain: dynamic permissions or complex custom logic make it hard to judge (the evidence points must still be written out)

And output the risk type: `AUTH`, including:
- Authentication bypass (the login state check is bypassed)
- Authorization bypass / privilege bypass (the role check is missing or wrong)
- IDOR (object access lacks an ownership/attribution check)

## Suspicious Pattern Detection (Mandatory, provide the evidence chain)
### 1) Path/URI matching leads to auth bypass
Common root causes in PHP:
- The raw `$_SERVER['REQUEST_URI']` or the `parse_url` result is matched against an allowlist, but the path is not normalized
- Differences in encoding/case/duplicate slashes/trailing characters cause the match to fail (the actual route reaches the protected handler)

Must output:
- The allowlist check location and the code snippet
- The bypass request (PoC) and the evidence of the handler it reaches

### 2) Only the login state is verified, with no role/resource authorization
Must output:
- The location of the route's "authentication check"
- The location of the "missing authorization check" (for example, only `user!=null` is tested before a sensitive operation runs)

### 3) IDOR / privilege bypass
Must output:
- Where the sensitive object id comes from (GET/POST/URL)
- Whether an "ownership check" for the query/update exists (whether the WHERE clause includes user_id/owner_id)
- The reason it is not verified and its reachability

## Report Output (by run mode)
Output to:
```
{output_path}/auth_audit/
├── auth_audit_report_{timestamp}.md
├── auth_mapping_{timestamp}.md
└── auth_README_{timestamp}.md
```
Mandatory rules:
- `STATIC_MAPPING`: must generate `auth_mapping_{timestamp}.md`; `auth_audit_report_{timestamp}.md` may be omitted or generated as an empty shell (and annotated: bucketing mapping only, contains no trace evidence)
- `TRACE_AUDIT`: must generate all three files, and the trace evidence points must be complete

### File 1: Main Report `auth_audit_report_{timestamp}.md`
Contains:
- Authentication framework identification (with version/implementation evidence)
- Authentication architecture overview (middleware/functions/handlers)
- Risk statistics
- The complete vulnerability structure for each risk (number/severity/data flow/PoC/remediation)

### File 2: Mapping Table `auth_mapping_{timestamp}.md`
Lists only the routes with their auth status and the required role/conditions (do not put detailed vulnerability analysis here).
However, it must add the bucketing fields (used for route selection in pipeline stage 3):
- `p_bucket`: `P0` or `P1`
  - `P0`: ❌ No auth
  - `P1`: ⚠️ Authenticated only, or an authorization bypass / privilege bypass / IDOR risk is detected (even when the auth status shows "authenticated only", explain in `p1_reason` why it lands in P1)
- `p1_reason`: a short static rationale (e.g. "login state only, missing hasRole/authorize or missing owner_id check")

### File 3: Documentation `auth_README_{timestamp}.md`
Describes only the methodology, tools, and verification guide, with no specific vulnerability details.

## PoC Verification Template (Mandatory)
At least the following scenarios must be distinguished:
- Access without logging in (no cookie/session/JWT)
- Access as a regular user (regular account cookie/JWT)
- Administrator / high-privilege control case (where applicable)

The PoC must be an executable HTTP request code block, and the route path must use the real route rules.

## Evidence Citation (Mandatory per run mode)
- `STATIC_MAPPING`: citing the trace's `EVID_*` evidence points is not mandatory (only the auth rating and the P0/P1 bucketing rationale need to be output).
- `TRACE_AUDIT`: every suspected auth risk must cite the evidence from the trace output item by item (a status may be marked as pending verification, but the evidence citation must exist):
1. `EVID_AUTH_PATH_PROTECTED_MATCH`: path matching evidence that the route reaches the protected handler (corresponds to the branch path evidence in the trace)
2. `EVID_AUTH_TOKEN_DECODE_JUDGMENT`: evidence of how the login state / token decoding result is judged (corresponds to the session/JWT read and conditional branch in the trace)
3. `EVID_AUTH_PERMISSION_CHECK_EXEC`: execution evidence of the permission decision function or condition (such as `hasRole/authorize`) (trace sink location or branch evidence)
4. `EVID_AUTH_IDOR_OWNERSHIP_CONDITION`: evidence of whether the IDOR ownership check (WHERE/condition) includes owner_id/user_id (the final query condition or state update statement in the trace)

## Handling Missing tracer Evidence (Mandatory)
- `STATIC_MAPPING`: not applicable (the bucketing rationale is based on static code evidence).
- `TRACE_AUDIT`: if the trace contract validation fails or any of the key evidence points 1~4 cannot be located: the risk can only be marked as `⚠️pending verification`, and must not be given a `✅confirmed exploitable` or "definitely bypassable" conclusion.

