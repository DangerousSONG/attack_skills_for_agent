---
name: php-file-write-audit
description: "PHP web source code arbitrary file write auditing tool. Identifies chains where user-controllable data reaches a write sink, traces arbitrary destination writes / path traversal to write, and assesses post-write executability (must not be omitted)."
zh-signals: "审计 PHP 源码中的任意文件写入漏洞，追踪用户可控数据到写入 Sink、路径穿越落点及写入后可执行性。信号:文件写入,路径穿越,写入Sink,代码审计,RCE"
when-to-use: >-
  Use when auditing PHP source code for arbitrary file write vulnerabilities, tracing
  user-controlled data to write sinks, or assessing post-write executability.
---

# PHP Arbitrary File Write Audit (php-file-write-audit)

Analyze the implementation logic that "writes data to files on disk" in PHP project source code, focusing on:

- Arbitrary destination writes: the write target path can be controlled by the attacker (including path traversal to the destination)
- Controllable write content: the written file content originates from user input (creating the conditions for subsequent RCE / overwrite)
- Overwrite/truncate mode: whether the write uses an overwrite mode such as `w/x`, or whether an exploitable same-name conflict overwrite can occur

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-WRITE-{index}`

## WRITE Sinks (Mandatory)
Identify and trace the following write/destination-changing functions/statements (select according to what actually appears in the project):

- Direct writes:
  - `file_put_contents({path}, {data})`
  - `fwrite($handle, {data})` (usually combined with `fopen($path, 'w'|'ab'|'x'|...)`)
  - `stream_write($stream, {data})` / `fputs($handle, {data})`
- Open and write (overwrite/truncate):
  - `fopen($path, 'w'|'x'|'a'|'ab'|'wb'|...)`
  - `ftruncate($handle, {size})` (if the path is user-controlled or related to a path concatenation chain)
- Destination changes caused by rename/copy (can form a "write destination"):
  - `rename($src, $dest)`
  - `copy($src, $dest)`
  - `move_uploaded_file($tmp, $dest)` (if it is not a pure UPLOAD scenario and the core risk is a controllable destination/path)
- Log destination writes (optional, but enable them according to your project's risk):
  - `error_log($message, 3, $destination)` (with message_type=3 the destination is a file)

## Path Traversal to Write Destination Detection (Mandatory)
You must analyze and give an evidence-based determination (you cannot simply write "possibly"):

1. Path concatenation and normalization chain
- How the base directory (e.g. `$baseDir` / `$uploadDir` / `$dataDir`) is joined with user input (`$base.$user` / `sprintf` / `join` / array path field concatenation)
- Whether there is directory sanitization / rejection of traversal fragments (`../`, `..\\`, mixed separators, Windows drive letters, absolute paths, trailing whitespace, etc.)
- Whether `realpath/canonicalize` is used together with a prefix check that "the final resolved path is still under the base prefix"

2. Final resolved write destination
- Whether the target path string before the write changes the final destination through wrapper/symlink/realpath resolution
- Whether the final `resolved target` escapes the base constraint (an escape suggests a controllable destination)

## Write Content Controllability and Overwrite Strategy (Mandatory)
You must trace and output the following (write the chain step by step):

1. Source of the write content
- Whether the `{data}/{content}` argument comes from user-controllable input (GET/POST/JSON/COOKIE/upload fields, etc.)
- Whether it remains controllable after decode/concatenation/templating/encoding steps

2. Overwrite/truncate mode
- Whether the write mode is an overwrite (`fopen(...,'w'|'x')`, etc.) or explicitly allows overwriting a file with the same name
- Whether there are mode-based conditional branches (some branches overwrite, some only append, etc.)

## Post-Write Executability/Reachability Assessment (Mandatory)
Because file writes often directly lead to RCE, this skill must output an evidence-based determination of "can the file be executed/accessed after being written" (must not be omitted):

- If a PHP/executable script is written: check the extension/parsing path (e.g. the final destination ends with `.php`, or the written content gets included/parsed)
- If the destination lies in the web root or an application-includable directory: output static mapping evidence (e.g. dest points to `public/`, `www/`, or a framework template/configuration directory)
- If an "execution disable policy" exists (e.g. the directory does not execute PHP, or the server configuration forbids execution): output the corresponding evidence and note what is missing

## tracer Evidence Citation (Mandatory: from php-route-tracer)
Every suspected WRITE vulnerability must cite item by item the corresponding evidence points of the **WRITE row** in the `## 9) Sink Evidence Type Checklist` of the trace output (a pending-verification status is allowed, but the evidence citation must exist):

1. `EVID_WRITE_WRITE_CALLSITE`: call site evidence for the write/destination change (file_put_contents/fwrite/fopen('w')/rename/copy, etc.)
2. `EVID_WRITE_DESTPATH_JOIN_AND_NORMALIZATION`: destination path concatenation and normalization evidence (base join, sanitization/traversal rejection fragments, realpath prefix validation, etc.)
3. `EVID_WRITE_DESTPATH_RESOLVED_TARGET`: evidence of the final resolved destination (resolved target) (whether it escapes the base)
4. `EVID_WRITE_CONTENT_SOURCE_INTO_WRITE`: mapping evidence between the write content argument and user-controllable input
5. `EVID_WRITE_TRUNCATE_OR_OVERWRITE_MODE`: overwrite/truncate/append mode evidence (write mode or overwrite strategy)
6. `EVID_WRITE_EXECUTION_ACCESSIBILITY_PROOF`: post-write executability/reachability evidence (web root / includable directory / execution disable policy, etc.)

## Handling Missing tracer Evidence (Mandatory)
- If any key evidence point in the `## 9) Sink Evidence Type Checklist` (WRITE row) of the trace is missing or cannot be mapped to this vulnerability: the status of that vulnerability may only be marked `⚠️ Unverified` (it must not be marked `✅ Confirmed Exploitable` directly).

## tracer Trigger Conditions (Required)
At least one of the following must hold, and the sink must be verified through the trace:

- The write target path reaches the write function after passing through multiple layers of functions/object properties/JSON fields
- The write content (data/content) remains controllable after decode/concatenation
- Branching logic exists such that an overwrite/truncate/landing in a writable controllable directory only happens in some cases

## Report Output
Output to:
```
{output_path}/vuln_audit/write_{timestamp}.md
```

## Vulnerability Entry Template (Mandatory)
Every vulnerability must follow the following structure (must not be omitted):

```markdown
### [{severity prefix}-WRITE-{index}] Arbitrary File Write (path traversal to destination / write chain) risk

| Item | Information |
|------|------|
| Severity Level | {🔴/🟠/🟡/🔵} (CVSS {score}) |
| Reachability (R) | {0-3} - {rationale} |
| Impact Scope (I) | {0-3} - {rationale} |
| Exploitation Complexity (C) | {0-3} - {rationale} |
| Exploitability | ✅ Confirmed / ⚠️ Unverified / ❌ Not Exploitable / 🔍 Environment-Dependent |
| Location | {file}:{line} ({Function/Class}) |

#### Data Flow Chain (Source -> Path Transform -> Content Transform -> Sink)
(Write it line by line: the chain by which user input enters destination/path, the normalization/sanitization/realpath constraint check -> the final resolved target -> the chain by which user input enters the write content data -> the argument position inside the write function -> whether it overwrites/truncates -> the write call site)

#### Exploitability Preconditions
- Authentication Requirement: {none / login required / specific privilege required}
- Input Controllability: {fully controllable / conditionally controllable / not controllable}
- Trigger conditions: {branch / exceptional path / specific server file permissions required / must land in an executable directory}

#### Evidence Citation (Mandatory: from php-route-tracer)
You must cite item by item:
- `EVID_WRITE_WRITE_CALLSITE`: {brief evidence description (including file:line)}
- `EVID_WRITE_DESTPATH_JOIN_AND_NORMALIZATION`: {brief evidence description}
- `EVID_WRITE_DESTPATH_RESOLVED_TARGET`: {brief evidence description}
- `EVID_WRITE_CONTENT_SOURCE_INTO_WRITE`: {brief evidence description}
- `EVID_WRITE_TRUNCATE_OR_OVERWRITE_MODE`: {brief evidence description}
- `EVID_WRITE_EXECUTION_ACCESSIBILITY_PROOF`: {brief evidence description}

#### Verification PoC (Mandatory: executable or observable verification framework)
```http
{HTTP Method} {real route with full parameters} HTTP/1.1
Host: {host}
{required Header/Session/JWT/Cookie}

{Payload}
```

PoC output/observation points (must be spelled out):
- Whether the written target file appears in a web-accessible location (or whether it can be included/read by subsequent business logic)
- If a PHP file was written: observe whether code execution can be triggered (or at least observe the file content echo / successful download)

#### Recommended Fix
- Use "whether the final resolved target is inside the allowed base directory" as the criterion, and enforce `realpath + prefix validation`
- Strictly restrict writable directories (allowlist) and avoid concatenating user input directly into file paths
- Apply type constraints to the written content: forbid writing executable scripts into executable directories; make the content non-executable (e.g. only allow serialized data formats)
- Avoid directly overwriting sensitive files with `'w'/'x'` as an overwrite strategy; safely reject same-name conflicts
- Provide code search commands (`rg`): locate all write APIs and path join points
```

## PoC/Remediation Search Commands (Mandatory Reference)
- Write APIs:
  - `rg -n "file_put_contents\\(|fwrite\\(|fopen\\(|stream_write\\(|rename\\(|copy\\(|ftruncate\\(|error_log\\(" .`
- Path concatenation/normalization (common variable names are only hints; the project is authoritative):
  - `rg -n "realpath\\(|canonicalize\\(|\\.\\.\\/|\\.\\.\\\\|allowlist|baseDir|dest(path)?|target(path)?|mkdir\\(" .`

