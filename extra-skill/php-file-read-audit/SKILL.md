---
name: php-file-read-audit
description: "PHP web source code arbitrary file read / path traversal auditing tool. Identifies file read sinks, traces the path source and validation logic, and outputs exploitability ratings, PoCs, and remediation recommendations (omissions are forbidden)."
zh-signals: "审计 PHP 源码中的任意文件读取与路径穿越风险，识别文件读取 Sink、追踪路径来源并给出分级与 PoC。信号:PHP审计,文件读取,路径穿越,漏洞挖掘,安全审计"
when-to-use: >-
  Use when auditing PHP source code for arbitrary file read, path traversal, or
  include/require execution risks, and you need exploitability grading, PoCs, and
  remediation advice.
---

# PHP Arbitrary File Read Audit (php-file-read-audit)

Analyze PHP project source code and identify file read and include execution risks: path traversal leading to arbitrary file read, and inclusion of arbitrary files (include/require) leading to information disclosure or code execution (when the included content is executable, or affected by stream wrappers).

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-FILE-{sequence-number}`

## FILE Sinks (mandatory)
Identify the following functions/syntax:
- Read: `file_get_contents/readfile/fopen/stream_get_contents/file/Storage::get`
- Include: `include/require/include_once/require_once` (path concatenation is especially high risk)
- Compression/archive: `ZipArchive->open` (when the path is controllable)
- Stream wrappers/filters: `php://filter`, `php://input` (when read/included as file content)
Dangerous when `allow_url_fopen/allow_url_include` or wrappers are permitted, because reading/inclusion can cross protocols
Dangerous patterns:
- The read/include path variable comes directly from user input
- Path concatenation without normalization and basePath validation
- `file://`, `php://`, `data://`, `zip://` and other stream wrappers are allowed without restriction
- In include/require scenarios there is `allow_url_include=On`, or evidence of network/cross-protocol inclusion being indirectly enabled through configuration or wrappers

## Path Traversal Detection (mandatory)
You must analyze and provide evidence for:
- Whether `../`, `..\\`, and mixed separators are filtered
- Whether `realpath/canonicalize` is applied and the basePath prefix is validated
- Whether stream wrapper prefixes are handled (`php://`, `file://`, `phar://`, `zip://`, etc.) — each item must be evidenced
- Possibility of encoding/double-encoding/case/trailing space/`\0` (older PHP) bypasses
- Whether a suffix/extension allowlist exists and is not easily bypassable

## Include Execution Determination (mandatory: raise true-positive rate)
When a controllable path is used in `include/require*`, you must output the following determination evidence (it cannot be skipped):
1. **Type of included content**: whether the include target could be executed as PHP code (e.g. extension/parsing behavior/execution path evidence)
2. **Final resolution of the include path**: whether the wrapper still resolves to a controllable resource
3. **Execution boundary**: whether include/require sits after exception handling or a return/throw branch (it may be readable but never executed)
4. **Configuration evidence**: whether `allow_url_include=On` exists, or `auto_prepend_file/auto_append_file`, or a custom wrapper allowlist point for include

## tracer Trigger Conditions (Required)
- The path passes through multiple function calls / JSON fields
- Branches exist: whether the validation logic only applies on one path

## Report Output
Output to:
```
{output_path}/vuln_audit/file_{timestamp}.md
```

## Vulnerability Entry Template (Mandatory)
Must include:
- Location evidence
- Data flow chain (Source→Sink, including path concatenation and validation branches)
- Evidence citation (from the `php-route-tracer` output, must cite every item): it must correspond to and cite the evidence points of the `## 9) Sink Evidence Type Checklist` (FILE rows) in the trace
  - `EVID_FILE_WRAPPER_PREFIX`: wrapper/stream wrapper prefix (e.g. `php://`/`phar://`/`zip://`)
  - `EVID_FILE_RESOLVED_TARGET`: final/resolved target (the final target after wrapper resolution)
  - `EVID_FILE_INCLUDE_REQUIRE_EXEC_BOUNDARY`: include/require execution boundary (whether PHP code is executed vs. only read/errored; this evidence point may also cover evidence related to allow_url_include/wrapper allowance)
- Exploitability preconditions (authentication / input controllability / trigger condition)
- Executable PoC (HTTP request, with the real route)
- Recommended fix (basePath validation + stream wrapper disabling strategy + safe alternatives for include/require + code search commands)

## Handling Missing tracer Evidence (Mandatory)
- If any key evidence point in the `## 9) Sink Evidence Type Checklist` (FILE rows) of the trace is missing or cannot be matched to this vulnerability: the status of that vulnerability must be `⚠️Unverified` (it must not be marked `✅Confirmed Exploitable`).

