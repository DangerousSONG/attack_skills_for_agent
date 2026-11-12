---





name: php-file-upload-audit





description: "PHP web source code file upload auditing tool. Identifies upload entry points and save paths, filename handling and validation logic, detects arbitrary file upload / path traversal / executable upload risks, and outputs exploitability ratings, PoCs, and remediation recommendations (must not be omitted)."
zh-signals: "审计 PHP 源码文件上传功能，检测任意上传、路径穿越与可执行上传风险。信号:PHP上传,文件上传审计,路径穿越,可执行文件,源码审计"
when-to-use: "Use when auditing PHP source code for file upload entry points, filename handling, and executable upload or path traversal risks."





---





# PHP File Upload Audit (php-file-upload-audit)





## Unified Execution Policy (Mandatory)





You must follow `shared/PHP_AUDIT_EXECUTION_POLICY.md`.





During execution, always apply the "dual channel + layered evidence" rules:





- High-recall channel: first perform a static `source/sink` pre-filter, covering HTTP routes and non-route entry points (CLI/cron/queue/include)





- High-confidence channel: then use `trace/EVID` for confirmation and noise reduction





Status determination is unified as: `✅ Confirmed / 🟡 High Probability / ⚠️ Unverified / ❌ Not Exploitable / 🔍 Environment-Dependent`





- The minimum evidence set is met (reachable fragment + controllability lead + sink trigger lead) => may be marked `🟡 High Probability`





- The complete trace + EVID are met => mark `✅ Confirmed`





- Insufficient evidence => mark `⚠️ Unverified`





The rigor requirements remain unchanged, but you must not stay silent because the trace is incomplete: still output suspected high-severity issues and missing evidence.





Analyze PHP project source code and identify file upload logic: `$_FILES`, `move_uploaded_file`, etc. Trace how the save directory and file name are handled, and detect:





- Arbitrary file upload (any type / any extension)





- Path traversal (concatenation with the original file name)





- Executable file upload (uploaded to a web-accessible directory without execution restrictions)





- Overwrite / same-name conflict risk






## Unified Audit Standard (Mandatory)
You must follow `shared/PHP_AUDIT_UNIFIED_STANDARD.md`.

The status order must be fixed as: `✅ Confirmed / 🟡 High Probability / ⚠️ Unverified / ❌ Not Exploitable / 🔍 Environment-Dependent`.
Trace evidence determination must be performed in layers:
- The minimum evidence set is met (entry reachable + parameter controllability chain + sink execution lead + basic preconditions) => `🟡 High Probability`
- The complete evidence set is met (trace COMPLETE + EVID aligned + branch coverage) => `✅ Confirmed`
- The minimum evidence set is not met => `⚠️ Unverified`

False positive suppression must check: hardcoded overrides, allowlist in effect, unreachable branches, sandbox/permission boundaries.
False negative suppression must be performed: do not stay silent when the trace is incomplete, fall back to sink-only.
The minimum output fields must include: location, source->sink, preconditions, status, PoC, remediation.
The execution priority must be followed: discovery first, documentation second.

## Evidence Confidence Fields and Review Checklist (Mandatory)
Evidence confidence fields (mandatory): output HIGH/MEDIUM/LOW per `shared/PHP_AUDIT_UNIFIED_STANDARD.md`, and give the determination basis (consistent with the status).
Review checklist (mandatory, at least 5 items):
- Has the high-recall channel (stage 0) been executed or the sink-only fallback been enabled, covering non-route entry points
- Has the same-class extension check been completed (after hitting an upload sink, sweep sibling entry points / save wrappers of the same class)
- Has the 🟡 High Probability / ✅ Confirmed / ⚠️ Unverified status been given per the minimum/complete evidence set rules, with the missing points explained
- Is the source->sink data flow chain explicit down to file name parsing / extension sanitization / destination concatenation / access reachability
- Has false positive suppression been addressed with hardcoded / allowlist / unreachable / permission boundary / invalid-format explanations
- Has an executable PoC and replaceable remediation recommendation been given (including randomization strategy / MIME validation / access surface restriction / search-and-locate key points)

## Severity Rating and Numbering





- See `shared/SEVERITY_RATING.md` for details





- Vulnerability ID: `{C/H/M/L}-UPLOAD-{index}`





## Upload Entry Point Identification (Mandatory)





Identify:





- `$_FILES['{value}']` field





- `move_uploaded_file($_FILES['{value}']['tmp_name'], $dest)`





- Save path concatenation: `$uploadDir.$filename`, `sprintf`, `join`, etc.





- Renaming: `uniqid`/`random_bytes`/timestamp (if the file name is still controllable it remains high severity)





## Validation Logic Audit (Mandatory)





You must check every point and output evidence:





- Extension / allowlist: is only the suffix validated (bypassable)





- Extension parsing safety: are there "double extension / multi-dot extension" bypasses (e.g. `a.php.jpg`, `.pHp` case bypass, trailing whitespace / Unicode separators)





- MIME / magic number: is `finfo_file`/`mime_content_type`/file header identification performed





- MIME / magic number consistency: is it checked whether the "actual server-side content type" matches the "extension/suffix" (avoid trusting only `Content-Type`)





- File name sanitization: are path separators and dangerous characters removed (`../`, `\`, `:`, null bytes, etc.)





- Upload directory: is it inside the web root; is execution permission controlled





- Post-write accessibility chain: is there a static mapping / direct-link access to the upload directory (this needs to be combined with route or webserver configuration evidence)





- Authentication: is the upload endpoint protected





## tracer Trigger Conditions (Required)





- The save path or file name passes through multiple layers of wrapper functions





- The validation logic contains branches, making it hard to confirm that it applies to every upload path





## Report Output





Output to:





```





{output_path}/vuln_audit/upload_{timestamp}.md





```





## Vulnerability Entry Template (Mandatory)





Must include:





- Location evidence (save / validation function location)





- Data flow chain (filename/path source -> validation -> target path -> write)





- Evidence citation (from the `php-route-tracer` output, must cite item by item): it must correspond to and cite the evidence points in the trace's `## 9) Sink Evidence Type Checklist` (UPLOAD row)





  - `EVID_UPLOAD_DESTPATH`: destPath (the final landing point of the save directory)





  - `EVID_UPLOAD_FILENAME_EXTENSION_PARSING_SANITIZE`: file name / extension parsing and sanitization logic





  - `EVID_UPLOAD_ACCESSIBILITY_PROOF`: accessibility surface evidence (whether an accessible surface is created after the write: direct static access evidence / mapping evidence)





  - `EVID_UPLOAD_EXEC_DISABLE_STRATEGY`: execution disable policy evidence (server-side execution disable policy, if any)





- Exploitability preconditions (authentication / directory accessibility / bypass conditions)





- Verification PoC (including the real upload route, with the necessary multipart request structure)





- Remediation recommendation (allowlist + magic number validation + directory isolation + randomized file names + overwrite strategy + webserver execution disable key points)





## Handling Missing tracer Evidence (Mandatory, per the unified standard)
- If any of the above key evidence points is missing from the trace `## 9) Sink Evidence Type Checklist` (UPLOAD row):
  - **The minimum evidence set is met** (reachability + parameter controllability lead + sink execution lead + basic preconditions): it may be marked `🟡 High Probability`, and the report must note the missing EVID points and the completion suggestions.
  - **The minimum evidence set is not met**: it may only be marked `⚠️ Unverified` (it must not be marked `✅ Confirmed Exploitable` directly).
  - **The complete evidence set is met** (all EVID aligned + complete trace + branch coverage): it may be marked `✅ Confirmed Exploitable`.





