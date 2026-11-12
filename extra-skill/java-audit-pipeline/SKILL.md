---
name: java-audit-pipeline
description: "Full-chain automated security audit pipeline for Java Web. Uses an agent team to orchestrate multiple audit skills and automatically completes the complete workflow of route extraction → auth audit → component vulnerabilities → cross filtering → call chain tracing → in-depth vulnerability detection → quality validation. Suitable for: (1) one-click launch of a full security audit of a Java project, (2) automatically identifying high-risk unauthenticated routes and precisely detecting vulnerabilities, (3) precise call-chain-based vulnerability auditing (fewer false positives), (4) automatically validating the output quality of each skill. The user only needs to provide the source path and output path."
zh-signals: "编排多 Agent 的 Java Web 全链路自动化安全审计流水线。信号:Java审计,代码审计,调用链追踪,鉴权审计,组件漏洞"
when-to-use: "Use when launching a full automated Java Web security audit from a source path, tracing routes, auth, component CVEs, and call chains."
---

# Java Full-Chain Audit Pipeline

Uses an agent team to orchestrate multiple agents (including dynamically scaled call-chain tracing workers), completing a full security audit of a Java Web project automatically in 5 phases. It uses an agent-7-x quality-checker pool to validate on demand in parallel, and all phases follow the same "validate each one as it completes" model.

## Terminology Definitions

In this pipeline, "risk" refers only to the following two categories:
1. **Authorization risk**: a route is unauthenticated (❌) or its authentication can be bypassed (🔓)
2. **Component vulnerability risk**: a component version flaw matching a known CVE

The following are not within the "risk" scope of this pipeline:
- Code quality (non-standard naming, high cyclomatic complexity, etc.)
- Architecture design (missing rate limiting, missing logging, etc.)
- Business logic (race conditions, logic errors, etc.)

## Input

Provided by the user:
- **source_path**: source code directory path
- **output_path**: output directory path (default `{source_path}_audit`)

## Process Overview

```
Phase 1: Information gathering (parallel)
  ├─ agent-1-route-mapper: /java-route-mapper   → all routes + parameters  → agent-7-x validation → close after passing
  ├─ agent-2-auth-audit: /java-auth-audit     → route auth mapping    → agent-7-x validation → close after passing
  └─ agent-3-vuln-scanner: /java-vuln-scanner   → component vulnerabilities        → agent-7-x validation → close after passing
        ↓ After all three validations pass
Phase 2: Cross filtering (parallel)
  ├─ agent-4a-risk-classifier: route classification (P0/P1/P2) → agent-7-x validation → close after passing
  └─ agent-4b-vuln-aggregator: vulnerability aggregation (component vulnerabilities + auth bypass) → agent-7-x validation → close after passing
        ↓ After both validations pass
Phase 3: Call chain tracing (parallel in batches)
  ├─ agent-5-route-tracer: reads all P0+P1 high-risk routes (falls back to P2 when P0+P1=0), creates tracing tasks in batches → close after passing
  └─ agent-5-1/5-2/.../5-N: /java-route-tracer traces each batch of routes in parallel (including auth risk pass-through) → each completion is immediately validated by agent-7-x → close after passing
        ↓ After all workers pass validation
Phase 4: In-depth vulnerability detection (parallel on demand)
  ├─ agent-6a-sql-auditor: /java-sql-audit         → SQL injection detection (including exploitability preconditions) → agent-7-x validation → close after passing
  ├─ agent-6b-xxe-auditor: /java-xxe-audit         → XXE injection detection (including exploitability preconditions) → agent-7-x validation → close after passing
  ├─ agent-6c-upload-auditor: /java-file-upload-audit  → file upload vulnerability detection (including exploitability preconditions) → agent-7-x validation → close after passing
  └─ agent-6d-fileread-auditor: /java-file-read-audit   → file read vulnerability detection (including exploitability preconditions) → agent-7-x validation → close after passing
        ↓
Phase 5: Summary report
  └─ agent-7-x: integrate all validation results and generate the final quality_report.md → close after completion
```

**Key design:**
1. **Quality-checker pool scales on demand**: the lead dynamically spawns agent-7-1, agent-7-2, ..., agent-7-N quality checkers according to each phase's concurrent validation needs, ensuring that every completed agent gets validated immediately with zero waiting
2. **Validate each one as it completes**: all phases (including Phase 3 call-chain workers) use the same "validate as soon as the agent completes" model, without waiting for other agents in the same phase
3. Each agent is closed immediately after passing validation to free resources; quality checkers are closed when there are no pending validation tasks in the current phase, and are re-spawned on demand in the next phase

## Execution Instructions

### Team Lead Responsibilities

1. Parse the source_path and output_path entered by the user
2. ⚠️ **Placeholder replacement rules (global)**: when passing a prompt to any agent, you must replace **all** placeholders in the template (`{source_path}`, `{output_path}`, `{project_name}`, `{batch_id}`, `{batch_content}`, etc.) with actual values. **Passing unreplaced `{xxx}` placeholders to a sub-agent is forbidden.**
3. Create the output directory structure (create all subdirectories at once):
   ```bash
   mkdir -p {output_path}/route_mapper {output_path}/auth_audit {output_path}/vuln_report {output_path}/cross_analysis {output_path}/route_tracer {output_path}/sql_audit {output_path}/xxe_audit {output_path}/file_upload_audit {output_path}/file_read_audit {output_path}/decompiled {output_path}/scripts {output_path}/qa_reports
   ```
4. Create the agent team
5. Use TaskCreate to create tasks and set dependencies:

```
task-1:  agent-1-route-mapper route extraction           (pending)
task-2:  agent-2-auth-audit auth check             (pending)
task-3:  agent-3-vuln-scanner component vulnerability scan       (pending)
task-4:  agent-7-x validate agent-1               (blockedBy: [1], assign to an idle checker)
task-5:  agent-7-x validate agent-2               (blockedBy: [2], assign to an idle checker)
task-6:  agent-7-x validate agent-3               (blockedBy: [3], assign to an idle checker)
task-7:  agent-4a-risk-classifier unauthenticated route classification (blockedBy: [4,5,6])
task-8:  agent-4b-vuln-aggregator vulnerability aggregation       (blockedBy: [4,5,6])
task-9:  agent-7-x validate agent-4a              (blockedBy: [7], assign to an idle checker)
task-10: agent-7-x validate agent-4b              (blockedBy: [8], assign to an idle checker)
task-11: agent-5-route-tracer route batching and scheduling     (blockedBy: [9,10])
task-12: agent-5-N parallel call chain tracing + validation one by one    (blockedBy: [11], each worker is immediately validated by agent-7-x after completion and closed after passing)
task-13: Lead summarizes Phase 3 coverage                  (blockedBy: [12], compute tracing coverage after all workers pass validation)
task-14: agent-6a-sql-auditor SQL injection detection        (blockedBy: [13], launch on demand)
task-15: agent-6b-xxe-auditor XXE injection detection        (blockedBy: [13], launch on demand)
task-16: agent-6c-upload-auditor file upload vulnerability detection (blockedBy: [13], launch on demand)
task-17: agent-6d-fileread-auditor file read vulnerability detection (blockedBy: [13], launch on demand)
task-18: agent-7-x validates each agent-6x one by one          (each agent-6x is immediately validated by an idle checker after completion, and closed after passing)
task-19: agent-7-x final summary quality_report.md  (blockedBy: [18], waits only for all actually launched agent-6x to pass validation)
```

5. **Phase 1 scheduling**: assign agent-1/2/3 in parallel; after each agent completes, the lead immediately spawns a new quality checker on demand (creating agent-7-1, agent-7-2, agent-7-3 in sequence), assigns the validation task to that checker, and the checker writes the validation report to `qa_reports/` before notifying the lead of the result. If it fails, the lead notifies the corresponding agent to read the validation report file and supplement the failing items; after all three validations pass, close the quality checkers for this phase and launch agent-4a and agent-4b in parallel
6. **Phase 2 scheduling**: after agent-4a and agent-4b each complete, they are immediately validated by an idle checker; after both pass, launch agent-5-route-tracer (the dispatcher)
7. **Phase 3 scheduling**: after agent-5 finishes batching, the lead dynamically spawns agent-5-1/5-2/.../5-N to trace in parallel; each worker is immediately validated by an idle checker after completion and closed after passing; after all pass, the lead summarizes coverage
8. **Phase 4 scheduling**: the lead reads the call-chain reports and launches agent-6x on demand by sink type; each agent-6x is immediately validated by an idle checker after completion and closed after passing (skip when there is no corresponding sink and mark the task completed directly)
9. **Quality-checker pool scheduling strategy**:
   - **Create on demand**: only after an agent completes is a checker spawned to validate that agent's output; do not pre-create them in batches
   - Checker naming rule: `agent-7-{index}`, with the index starting from 1 and incrementing; indices may be reused across phases
   - When there is a new validation need, assign it first to an existing idle checker; if all are busy, spawn a new checker
   - All checkers have identical capabilities and the same validation standards
   - After all validations in the current phase are complete, close that phase's checkers; re-spawn on demand in the next phase
10. **Agent lifecycle management**:
   - After each agent completes its task and passes agent-7-x validation, the lead immediately uses the SendMessage tool to send `type: "shutdown_request"` to that agent
   - The lead waits for the agent to respond with `type: "shutdown_response"` to confirm the agent has closed
   - If no response is received within 30 seconds, log a warning and continue with the subsequent flow (to avoid blocking)
   - agent-7-x checkers are closed after all validations in the current phase are complete and are re-spawned on demand in the next phase
   - **Closing order**: within each phase: close the audited agent immediately after validation passes → close the checkers after all validations in the phase are complete → proceed to the next phase

### General Execution Requirements (passed to every agent)

```
Execution requirements:
1. The output directory has already been created in advance by the lead; creating or modifying directory structures on your own is forbidden; write directly to the specified directory
2. First scan the source code directory structure to identify the project's module composition, tech stack, and code distribution
3. Based on the scan results, use TaskCreate to plan your own detailed todo subtask list
4. Execute your planned task list item by item, marking each as completed with TaskUpdate when done
5. After everything is complete, self-check the completeness and count of the output files, and notify the team lead once you confirm nothing is missing
6. **Lifecycle management**:
   - After completing the task and notifying the lead, wait for the shutdown_request sent by the lead
   - Upon receiving the shutdown_request:
     a. Confirm that all output files have been written to disk
     b. Clean up temporary resources (if any)
     c. Use SendMessage to send type: "shutdown_response" to the lead
     d. Stop running
Plan and execute autonomously throughout; no need to wait for confirmation.
```

---

## Detailed Agent Instructions

### Agent-1-route-mapper: Route Extractor

```
Role: agent-1-route-mapper (route extractor)
Skill: /java-route-mapper
Source code: {source_path}
Output directory: {output_path}/route_mapper/ (already created; write directly)
Decompiled output directory: {output_path}/decompiled/ (already created; write directly; shared by multiple agents to avoid repeated decompilation)
Script directory: {output_path}/scripts/ (all temporary scripts and intermediate files generated at runtime must be written to this directory; writing to /tmp or other temporary directories is forbidden)
Task: Extract all HTTP routes and parameter structures of the project and generate Burp Suite request templates
```

### Agent-2-auth-audit: Auth Checker

```
Role: agent-2-auth-audit (auth checker)
Skill: /java-auth-audit
Source code: {source_path}
Output directory: {output_path}/auth_audit/ (already created; write directly)
Decompiled output directory: {output_path}/decompiled/ (already created; write directly; shared by multiple agents to avoid repeated decompilation)
Script directory: {output_path}/scripts/ (all temporary scripts and intermediate files generated at runtime must be written to this directory; writing to /tmp or other temporary directories is forbidden)
Task: Identify the authentication framework, check the auth status of each route, and detect auth bypass vulnerabilities
```

### Agent-3-vuln-scanner: Component Scanner

```
Role: agent-3-vuln-scanner (component scanner)
Skill: /java-vuln-scanner
Source code: {source_path}
Output directory: {output_path}/vuln_report/ (already created; write directly)
Decompiled output directory: {output_path}/decompiled/ (already created; write directly; shared by multiple agents to avoid repeated decompilation)
Script directory: {output_path}/scripts/ (all temporary scripts and intermediate files generated at runtime must be written to this directory; writing to /tmp or other temporary directories is forbidden)
Task: Scan project dependencies for known vulnerabilities (CVEs) and generate a trigger point detection report
```

### Agent-4a-risk-classifier: High-Risk Route Classifier

When the lead creates agent-4a, read `references/agent_4a_instructions.md` to obtain the complete execution steps and output template, **replace all placeholders such as `{output_path}` and `{source_path}` with actual values**, and use the result as agent-4a's prompt instructions.

---

### Agent-4b-vuln-aggregator: Vulnerability Aggregator

When the lead creates agent-4b, read `references/agent_4b_instructions.md` to obtain the complete execution steps and output template, **replace all placeholders such as `{output_path}` and `{source_path}` with actual values**, and use the result as agent-4b's prompt instructions.

---

### Agent-5-route-tracer: Call Chain Tracing Dispatcher

When the lead creates agent-5, read `references/agent_5_instructions.md` to obtain the complete execution steps, intelligent selection strategy, and output template, **replace all placeholders such as `{output_path}` and `{source_path}` with actual values**, and use the result as agent-5's prompt instructions.

After the lead receives `trace_batch_plan.md`: close agent-5 → spawn agent-5-1~5-N in parallel (using the Worker template below) → each worker is validated by agent-7-x after completion → after all pass, summarize coverage (>= 90%) → enter Phase 4.

---

### Agent-5-N-worker: Call Chain Tracing Executor (Worker Template)

For each worker, the lead generates a prompt using the following template, replacing all of `{source_path}`, `{output_path}`, `{project_name}`, `{batch_id}`, and `{batch_content}` with actual values (⚠️ you must replace all placeholders in the template; none may be missed):

```
Role: agent-5-{batch_id} (call chain tracing executor)
Skill: /java-route-tracer
Source code: {source_path}
Output root directory: {output_path}/route_tracer/ (already created)
Decompiled output directory: {output_path}/decompiled/ (already created; write directly; shared by multiple agents to avoid repeated decompilation)
Script directory: {output_path}/scripts/ (all temporary scripts and intermediate files generated at runtime must be written to this directory; writing to /tmp or other temporary directories is forbidden)
Input: the route batch you are responsible for tracing, from {output_path}/cross_analysis/trace_batch_plan.md

{batch_content}

Task: Perform call chain tracing on each of the above routes, and pass through the auth risk information in each report

⚠️ Mandatory output file naming rules (must be strictly followed; inventing your own names is forbidden):
- For each route, first create a subdirectory, then write the report file inside that subdirectory
- Directory structure: {output_path}/route_tracer/{route_name}/
- Single-method route file name: {project_name}_trace_{route_id}_{YYYYMMDD}.md
- Multi-method route file name: {project_name}_trace_{method_name}_{YYYYMMDD}.md + index file {project_name}_trace_all_methods_{YYYYMMDD}.md
- route_name is the route path with underscores (stripping leading slashes), e.g. /api/upload → api_upload
- Forbidden: flattening files directly under the route_tracer/ root, using numeric prefixes (e.g. 01_xxx.md), or omitting subdirectories
```

**Key requirement: auth risk pass-through**

When each worker generates a call chain report, it must add an auth risk section at the top of the report:

```markdown
## Auth Status Determination

- **Auth status**: ❌ Unauthenticated
- **Auth bypass vulnerabilities**:
  - Shiro permission bypass present (H-AUTH-001): path traversal `/admin/;/user`
  - Component vulnerability bypass present (CVE-2020-1938): Tomcat AJP protocol injection
- **Risk level**: 🔴 Extremely high (unauthenticated + bypass methods present)
```

**Pass-through logic**:
1. Obtain the auth bypass vulnerabilities relevant to this batch from the "Auth Risk Information" section in the batching plan
2. For P0 routes: mark ❌ Unauthenticated; if a global auth bypass vulnerability exists, also mark it
3. For P1 routes: mark 🔓 Auth bypassable and attach the specific bypass method
4. For P2 routes (P2 fallback mode only): mark ✅ Authenticated, with no bypass information passed through, and vulnerability detection focuses on code-layer vulnerabilities after authentication
5. This information will be read by the agent-6 series to determine the exploitability of vulnerabilities

---

### Agent-6a-sql-auditor: SQL Injection Auditor

```
Role: agent-6a-sql-auditor (SQL injection auditor)
Wait for: all agent-5-N call chain tracing to complete, and SQL-related sinks to exist in the call chains
Skill: /java-sql-audit
Source code: {source_path}
Output directory: {output_path}/sql_audit/ (already created; write directly)
Decompiled output directory: {output_path}/decompiled/ (already created; write directly; shared by multiple agents to avoid repeated decompilation)
Script directory: {output_path}/scripts/ (all temporary scripts and intermediate files generated at runtime must be written to this directory; writing to /tmp or other temporary directories is forbidden)
Input: call chain reports containing SQL sinks under {output_path}/route_tracer/ (including auth risk information)
Task: Perform precise SQL injection detection based on call chains (not a full scan), reduce false positives, and reflect exploitability preconditions in the vulnerability report
```

**Key requirement: exploitability preconditions**

When generating each SQL injection vulnerability report, you must add an exploitability preconditions section:

```markdown
## Exploitability Preconditions

- **Auth requirement**: ❌ No auth required
- **Or auth bypass**:
  - Shiro permission bypass present (H-AUTH-001)
  - Component vulnerability bypass present (CVE-2020-1938)
- **Other conditions**: parameters controllable
- **Overall determination**: 🔴 Directly exploitable (no auth barrier)
```

---

### Agent-6b-xxe-auditor: XXE Injection Auditor

```
Role: agent-6b-xxe-auditor (XXE injection auditor)
Wait for: all agent-5-N call chain tracing to complete, and XML parsing sinks to exist in the call chains
Skill: /java-xxe-audit
Source code: {source_path}
Output directory: {output_path}/xxe_audit/ (already created; write directly)
Decompiled output directory: {output_path}/decompiled/ (already created; write directly; shared by multiple agents to avoid repeated decompilation)
Script directory: {output_path}/scripts/ (all temporary scripts and intermediate files generated at runtime must be written to this directory; writing to /tmp or other temporary directories is forbidden)
Input: call chain reports containing XML parsing sinks under {output_path}/route_tracer/ (including auth risk information)
Task: Perform precise XXE injection detection based on call chains (not a full scan), reduce false positives, and reflect exploitability preconditions in the vulnerability report
```

**Key requirement: exploitability preconditions** (same as agent-6a)

---

### Agent-6c-upload-auditor: File Upload Auditor

```
Role: agent-6c-upload-auditor (file upload auditor)
Wait for: all agent-5-N call chain tracing to complete, and file upload sinks to exist in the call chains
Skill: /java-file-upload-audit
Source code: {source_path}
Output directory: {output_path}/file_upload_audit/ (already created; write directly)
Decompiled output directory: {output_path}/decompiled/ (already created; write directly; shared by multiple agents to avoid repeated decompilation)
Script directory: {output_path}/scripts/ (all temporary scripts and intermediate files generated at runtime must be written to this directory; writing to /tmp or other temporary directories is forbidden)
Input: call chain reports containing file upload sinks under {output_path}/route_tracer/ (including auth risk information)
Task: Perform precise file upload vulnerability detection based on call chains (not a full scan), reduce false positives, and reflect exploitability preconditions in the vulnerability report
```

**Key requirement: exploitability preconditions** (same as agent-6a)

---

### Agent-6d-fileread-auditor: File Read Auditor

```
Role: agent-6d-fileread-auditor (file read auditor)
Wait for: all agent-5-N call chain tracing to complete, and file read sinks to exist in the call chains
Skill: /java-file-read-audit
Source code: {source_path}
Output directory: {output_path}/file_read_audit/ (already created; write directly)
Decompiled output directory: {output_path}/decompiled/ (already created; write directly; shared by multiple agents to avoid repeated decompilation)
Script directory: {output_path}/scripts/ (all temporary scripts and intermediate files generated at runtime must be written to this directory; writing to /tmp or other temporary directories is forbidden)
Input: call chain reports containing file read sinks under {output_path}/route_tracer/ (including auth risk information)
Task: Perform precise file read vulnerability detection based on call chains (not a full scan), reduce false positives, and reflect exploitability preconditions in the vulnerability report
```

**Key requirement: exploitability preconditions** (same as agent-6a)

---

**Sink type to agent mapping:**

| Sink Type | Characteristic Keywords | Agent |
|:----------|:----------|:------|
| SQL concatenation | `Statement.execute`, `executeQuery`, `executeUpdate`, `sql.*\+`, `StringBuilder.*append.*sql`, `StringBuffer.*append.*sql`, `String.format.*sql`, `concat.*sql`, `MyBatis.*\$\{`, `createQuery.*\+`, `HQL.*\+` | agent-6a-sql-auditor |
| XML parsing | `DocumentBuilder.parse`, `SAXParser`, `XMLReader`, `XMLReaderFactory`, `SAXBuilder`, `SAXReader`, `TransformerFactory`, `SchemaFactory`, `XMLInputFactory`, `Unmarshaller`, `JAXBContext` | agent-6b-xxe-auditor |
| File upload | `MultipartFile`, `transferTo`, `ServletFileUpload`, `DiskFileItemFactory`, `FileItem`, `getOriginalFilename`, `new File.*fileName`, `Paths.get.*fileName` | agent-6c-upload-auditor |
| File read | `BufferedReader`, `FileReader`, `FileInputStream`, `Scanner.*File`, `Scanner.*Path`, `Files.readAllLines`, `Files.readAllBytes`, `Files.lines`, `new File.*\+`, `Paths.get.*\+` | agent-6d-fileread-auditor |

**Decision logic:**
1. The lead reads all call chain reports under `{output_path}/route_tracer/`
2. Searches the reports for the characteristic keywords above (regex matching supported)
3. Launches only the agents that have corresponding sinks; skips an agent if there is no corresponding sink and marks its task as completed directly
4. Preferred approach: directly read the **Sink Identification section** in the java-route-tracer output report, which already contains a complete Sink classification

### Agent-7-x-quality-checker: Quality Checker Pool (dynamically spawned on demand throughout the flow)

```
Role: agent-7-x-quality-checker (quality checker pool, spawned on demand)
Naming: agent-7-1, agent-7-2, ..., agent-7-N, with increasing indices
Validation basis: Use the Skill tool to load the corresponding skill (e.g. /java-route-mapper) and extract the output specification from the loaded skill context as the validation standard
Validation report directory: {output_path}/qa_reports/ (write qa_report_{audited agent name}.md for each validation)
Final summary: {output_path}/quality_report.md (generated as a summary by the last quality checker)
Working mode: validate each agent immediately after it completes (validate each one as it completes); the lead assigns validation tasks to idle checkers
```

**Core principle: only after an agent's output passes validation is that agent allowed to be closed and the flow advanced. This prevents erroneous data from propagating downstream.**

**Quality-checker pool scheduling strategy:**
- **Create on demand**: after an agent completes its task, the lead immediately spawns a checker to validate its output; do not pre-create them in batches
  - Phase 1: after agent-1/2/3 each complete, spawn agent-7-1, agent-7-2, agent-7-3 in sequence on demand
  - Phase 2: after agent-4a/4b each complete, spawn checkers in sequence on demand
  - Phase 3: after each agent-5-N worker completes, spawn a checker on demand (concurrency capped at min(N,5))
  - Phase 4: after each agent-6x completes, spawn a checker on demand
- When there is a new validation need, assign it first to an existing idle checker; if all are busy, spawn a new checker
- All checkers have identical capabilities and the same validation standards
- After each checker finishes validating, write the complete validation report to `{output_path}/qa_reports/qa_report_{audited agent name}.md`, then notify the lead of the result (pass/fail + report file path); **sending the report body in the message is forbidden**
- After all validations in the current phase are complete, close all checkers for that phase; re-spawn on demand in the next phase

#### Validation Trigger Timing (uniform across all phases: validate each one as it completes)

| Trigger Point | Validation Target | Assigned To | Action After Passing | Handling on Failure |
|:-------|:---------|:------|:--------------|:-----------|
| After agent-1 completes | java-route-mapper output | Idle checker | Close agent-1 | Lead notifies agent-1 to read `qa_reports/qa_report_agent-1.md` and supplement |
| After agent-2 completes | java-auth-audit output | Idle checker | Close agent-2 | Lead notifies agent-2 to read `qa_reports/qa_report_agent-2.md` and supplement |
| After agent-3 completes | java-vuln-scanner output | Idle checker | Close agent-3 | Lead notifies agent-3 to read `qa_reports/qa_report_agent-3.md` and supplement |
| After agent-4a completes | `high_risk_routes.md` | Idle checker | Close agent-4a | Lead notifies agent-4a to read `qa_reports/qa_report_agent-4a.md` and supplement |
| After agent-4b completes | `component_vulnerabilities.md` + `auth_bypass_vulnerabilities.md` | Idle checker | Close agent-4b | Lead notifies agent-4b to read `qa_reports/qa_report_agent-4b.md` and supplement |
| After agent-5 finishes batching | `trace_batch_plan.md` batching plan | Lead checks personally | Close agent-5, spawn workers | Notify agent-5 to re-batch |
| After each agent-5-N completes | That worker's route_tracer output (including the auth risk section) | Idle checker | Close that worker | Lead notifies that worker to read `qa_reports/qa_report_agent-5-{N}.md` and supplement |
| After each agent-6x completes | The corresponding audit output (including exploitability preconditions) | Idle checker | Close that agent-6x | Lead notifies that agent-6x to read `qa_reports/qa_report_{agent-6x name}.md` and supplement |
| After all agent-6x pass validation | Cross-skill data consistency | Any checker | Generate quality_report.md → close agent-7-x | — |

#### General Validation Method

For each validation:
1. Read `references/quality_check_templates.md` and find the **mandatory fill-in validation checklist table** for the corresponding phase
2. Use the Skill tool to load the skill corresponding to the audited agent (e.g. `/java-route-mapper`), and extract the output specification from the skill context as the validation standard
3. Read the actual output file
4. **Fill in row by row** the "Actual" and "Status" columns of each checklist item according to the template table; omitting any field is forbidden
5. Fill in the "Final Determination" section: status (pass/fail), proportion of passing items (M/N), specific missing items and remediation requirements for failing items
6. **Write the complete validation report to a file** `{output_path}/qa_reports/qa_report_{audited agent name}.md` (e.g. `qa_report_agent-1.md`, `qa_report_agent-5-2.md`)
7. Notify the lead of the validation result: send only "pass/fail" + the report file path; **including the validation report body in the message is forbidden**
8. After receiving a fail notification, the lead sends to the corresponding agent: "Validation failed. Please read `{output_path}/qa_reports/qa_report_{your name}.md` to obtain the complete validation report, supplement each failing item in the list, and resubmit"

**Output format requirement**: the checker's validation result must be returned strictly by filling in each item according to the table template in `references/quality_check_templates.md`; summarizing in one sentence or omitting the validation process is not allowed.

The specific validation items and output templates for each phase are uniformly collected in `references/quality_check_templates.md`; checkers validate item by item according to its mandatory fill-in tables.

#### Final Summary: Generate `quality_report.md`

After all agent-6x pass validation, the lead assigns the summarization task to any idle checker. The checker reads the "Final Quality Report Template" at the end of `references/quality_check_templates.md`, integrates the validation results of all phases to generate `{output_path}/quality_report.md`, then closes agent-7-x, completing the entire pipeline.

---

## Output Directory Structure

```
{output_path}/
├── route_mapper/              # Phase 1 - agent-1-route-mapper (including subdirectories by module)
├── auth_audit/                # Phase 1 - agent-2-auth-audit
├── vuln_report/               # Phase 1 - agent-3-vuln-scanner
├── cross_analysis/            # Phase 2 - agent-4a & agent-4b
│   ├── high_risk_routes.md              # agent-4a output
│   ├── trace_batch_plan.md              # agent-5 batching plan
│   ├── component_vulnerabilities.md     # agent-4b output
│   └── auth_bypass_vulnerabilities.md   # agent-4b output
├── route_tracer/              # Phase 3 - agent-5-1/5-2/.../5-N parallel output (including auth risk pass-through)
├── sql_audit/                 # Phase 4 - agent-6a-sql-auditor (including exploitability preconditions)
├── xxe_audit/                 # Phase 4 - agent-6b-xxe-auditor (including exploitability preconditions)
├── file_upload_audit/         # Phase 4 - agent-6c-upload-auditor (including exploitability preconditions)
├── file_read_audit/           # Phase 4 - agent-6d-fileread-auditor (including exploitability preconditions)
├── decompiled/                # Decompiled output (shared by multiple agents)
├── scripts/                   # Temporary script directory (shared by multiple agents; all runtime-generated scripts must be written here; writing to temporary directories is forbidden)
├── qa_reports/                # Checker validation reports (qa_report_{agent name}.md, one per validation)
└── quality_report.md          # Phase 5 - agent-7-x-quality-checker
```

## Skill Output Specification Reference

During validation, agent-7-x uses the Skill tool to load the corresponding skill and obtain its output specification:

| Validation Target | Skill To Load |
|:---------|:-----------|
| agent-1-route-mapper output | `/java-route-mapper` |
| agent-2-auth-audit output | `/java-auth-audit` |
| agent-3-vuln-scanner output | `/java-vuln-scanner` |
| agent-5-route-tracer output | `/java-route-tracer` |
| agent-5-N output | `/java-route-tracer` |
| agent-6a-sql-auditor output | `/java-sql-audit` |
| agent-6b-xxe-auditor output | `/java-xxe-audit` |
| agent-6c-upload-auditor output | `/java-file-upload-audit` |
| agent-6d-fileread-auditor output | `/java-file-read-audit` |