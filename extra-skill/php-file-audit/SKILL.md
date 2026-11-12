---
name: php-file-audit
description: |
  Audit of PHP source code for file operation vulnerabilities. Triggered during PHP white-box audits when file-related vulnerabilities need to be detected.
  Covers 5 categories of file risk: arbitrary file upload (type bypass/path traversal/secondary rendering), arbitrary file read (include/fread/path traversal),
  arbitrary file write (log injection/config overwrite), file system race conditions (TOCTOU/symlink), and archive extraction vulnerabilities (Zip Slip).
  Requires data-flow evidence provided by php-audit-pipeline.
zh-signals: "审计 PHP 源码中的文件上传、读取、写入、竞争与归档提取类漏洞。信号:PHP审计,文件上传,任意读取,路径穿越,ZipSlip"
when-to-use: "Use during PHP white-box audits when tracing file-operation sinks such as upload, include, write, TOCTOU, or archive extraction."
metadata:
  tags: file upload, file read, file write, path traversal, zip slip, lfi, rfi, include, arbitrary read, arbitrary write, toctou, symlink
  category: code-audit
---

# PHP File Operation Vulnerability Source Code Audit
This skill focuses on the source code level: determining whether a "file operation vulnerability actually holds". Its core is verifying path controllability, content controllability, and execution reachability. Runtime exploitation techniques such as crafting upload bypass payloads or LFI log poisoning belong to the corresponding black-box exploit skills.

## Further Reading

- Dangerous patterns of the 5 file vulnerability categories / secure vs. insecure code comparison / EVID evidence examples → [references/file-vuln-patterns.md](references/file-vuln-patterns.md)

---

## Sink Classification Decision Tree

Depending on the type of sink function encountered, enter a different audit branch:

| Sink function | Branch | Typical severity |
|-----------|------|-----------|
| `move_uploaded_file`, `copy($_FILES)` | File upload | Critical-High |
| `include`/`require`/`include_once`/`require_once` | File read + execution | Critical |
| `file_get_contents`/`readfile`/`fread`/`highlight_file` | File read | High-Medium |
| `file_put_contents`/`fwrite`/`fopen('w')` | File write | Critical-High |
| `ZipArchive::extractTo`/`PharData::extractTo` | Archive extraction | High |
| `file_exists`/`is_file` + subsequent operation | Race condition | Medium-High |

## File Upload Audit Points

The essence of an upload vulnerability is that three conditions hold simultaneously: an executable extension + a web-reachable storage path + no renaming/content sanitization.

- **Extension validation**: blacklists easily miss `.phtml`/`.pht`/`.php5`/`.phar`/`.shtml`; whitelists are safer but the case-handling logic must be checked
- **MIME vs. magic bytes**: `$_FILES['type']` comes from the client and is fully forgeable; `finfo_file()`/`getimagesize()` validate the file header, but image webshells (GIF89a + PHP code) can bypass them
- **Storage path controllability**: whether the user can control the storage location via `../` in the filename and escape the intended upload directory
- **Web root reachability**: if the file is stored outside the web root, an uploaded PHP file cannot be executed directly even if the upload succeeds
- **Renaming strategy**: predictable naming such as `md5(time())` can be guessed, while `random_bytes()` is safer

## File Read / Include Audit Points

The `include` family both reads and executes, so its impact is far greater than that of pure read functions:

- **Path concatenation pattern**: `include($dir . '/' . $page . '.php')` — check whether `$page` is user-controllable and whether `../` traversal is filtered
- **%00 truncation**: PHP < 5.3.4 allows null byte truncation of the `.php` suffix; fixed in newer versions, but still worth watching when auditing legacy systems
- **Wrapper abuse**: `php://filter/convert.base64-encode/resource=` to read source code, `php://input` to inject code, `data://` to execute payloads
- **RFI conditions**: remote file inclusion holds when `allow_url_include=On`; check the `php.ini` configuration
- **Pure read functions**: `file_get_contents`/`readfile` do not execute, but they can leak sensitive configuration (database passwords, API keys)

## File Write Audit Points

Write vulnerabilities require three conditions: controllable path + controllable content + the written file is executable.

- **Direct shell write**: when both arguments of `file_put_contents($path, $content)` are user-controllable, a webshell is written directly
- **Log injection chain**: user input is logged → the log file is loaded via `include` → indirect code execution. Review whether the log path is predictable and whether the content is filtered
- **Configuration file overwrite**: write `.htaccess` (making `.jpg` be parsed as PHP) or PHP configuration files (injecting code into `<?php return [...];`)
- **Session file abuse**: session file content under `session.save_path` is partially user-controllable, and combined with LFI this yields RCE

## Archive Extraction Audit Points

- **Zip Slip**: `ZipArchive::extractTo()` does not validate `../../` in entry names, so a malicious archive can write files to arbitrary directories
- **PharData**: same as ZipArchive, `extractTo()` is vulnerable to path traversal
- **Safe extraction**: iterate over entry names before extracting and reject paths containing `..`; or extract to a temporary directory and then verify and move each file

## Race Condition Audit Points

- **TOCTOU**: after `is_file($path)` passes the check and before `unlink($path)` executes, the attacker replaces the file with a symlink → arbitrary file deletion
- **Upload race**: the file is saved first and validated/deleted afterwards; within that window, send a large number of concurrent requests to access the uploaded PHP file
- **Symlink following**: `file_get_contents($userPath)` reads the link target if `$userPath` is a symlink, bypassing directory restrictions
- **Atomic operations**: `rename()` is atomic and can be used for safe replacement; writing to a temporary file and then `rename`ing it to the target location avoids the race

## Detection Checklist

- [ ] All file-related EVID_* evidence points have been reviewed one by one
- [ ] The extension validation method of the upload feature has been confirmed (whitelist vs. blacklist vs. no validation)
- [ ] Whether the upload storage path is inside the web root and directly reachable has been verified
- [ ] The source of path parameters and the filtering logic of include/require have been traced
- [ ] The exploitability of wrappers such as php://filter under the current configuration has been assessed
- [ ] The path and content sources of file_put_contents/fwrite have been traced
- [ ] Entry name validation of archive extraction functions has been checked
- [ ] TOCTOU patterns (the interval between check and operation) have been identified
- [ ] Insufficient filtering points have been given a bypass idea or marked "to be verified"
- [ ] Severity scoring used the unified formula, consistent with the pipeline
