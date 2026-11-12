---
name: php-filesystem-audit
description: "PHP filesystem operation audit tool. Focuses on the security risks of operations such as mkdir/chmod/chown/unlink/rmdir/link/symlink/readlink/touch, permissions, and TOCTOU, providing exploitability-enhancing evidence for path validation bypass and write-chain exploitation (does not replace FILE/UPLOAD/WRITE sink sub-audits)."
zh-signals: "PHP 文件系统操作安全审计。信号:PHP,文件系统,TOCTOU,权限,符号链接,路径绕过"
when-to-use: "Use when auditing PHP filesystem operations such as mkdir, chmod, symlink, or unlink for path validation bypass and TOCTOU write-chain risks."
---

# PHP Filesystem Operation Audit (php-filesystem-audit)

Analyze critical filesystem operations in PHP projects, paying particular attention to how these operations interact with:

- Path validation / normalization failures (directory traversal, missing basePath)
- Write / read / inclusion chains to the drop location
- Post-write triggers (executability, includability)
- Race conditions (TOCTOU)

When they occur together, thereby increasing the likelihood of real exploitation.

## Coverage Scope (Mandatory)
Must cover and output the "evidence point + risk explanation + exploitability assessment" for:

### 1) Creation / directory operations
- `mkdir($path, $mode, $recursive)`
- `rmdir($path)`
- `touch($path)`
- `tmpfile()` / `tempnam()`
- Framework-wrapped directory creation (e.g. the underlying wrapper of `Storage::put`/`ensureDirectory`, if identifiable)

### 2) Permission / ownership changes (commonly used in privilege escalation chains or execution policy bypasses)
- `chmod/chown/chgrp`
- `umask`

### 3) Links and redirection drop locations (common symlink/hardlink bypasses)
- `symlink($target, $link)`
- `link($target, $link)`
- `readlink($path)`

### 4) Deletion and cleanup (combined with TOCTOU or overwrite chains)
- `unlink($path)`
- `unlink/rename` variant deletions
- `rename($src, $dest)` (requires special attention to TOCTOU when the drop location changes)
- `copy/move` variants (when they appear as a "drop location preparation step")

### 5) Path races and TOCTOU (must be audited separately)
Give a verdict on "check-then-use" code patterns:
- Whether there is an `if (realpath/canonicalize + prefix validation)` followed by a repeated join/open/write in some branch or exception handler (the path may change)
- Whether there is a writability check followed by a write, or a check followed by the file operation
- Whether there is inconsistent symlink resolution (the resolved path at check time differs from the path actually opened)

## Key Output Requirements (Mandatory)
Every finding must include:

1. Location evidence: file path and function / call site (include the line number where possible; mark it as pending location if the line number cannot be found)
2. Operation type: creation / permission / link / deletion / rename / copy, etc.
3. Path control source: whether the path parameter comes from GET/POST/SESSION/configuration or is hardcoded
4. Relationship to the chain (at least one must be explained):
   - Related to the executability or includability of a `WRITE`/`UPLOAD` drop location
   - Related to `FILE` (read/inclusion) or `ARCHIVE` (extraction drop location)
   - Related to authorization / resource ownership (e.g. only admin directories are writable but the check is bypassed)
   - Related to a TOCTOU race (the path may be swapped between the check point and the use point)
5. Exploitability assessment:
   - ✅ Confirmed: the key precondition of the exploit chain can be proven to be provided by this filesystem operation (or the evidence forms a closed loop with WRITE/UPLOAD/FILE)
   - ⚠️ Unverified: a risk exists, but a key precondition or trace / resolution evidence is missing
   - ❌ Not Exploitable: strong constraints apply (the baseDir allowlist is in effect, resolved path consistency protection exists, permissions are fixed and cannot be changed, the race window is eliminated)
   - 🔍 Environment-Dependent: it depends on a specific file system, permissions, concurrency timing, or server-side directory structure

6. Triggerability constraints (mandatory):
   - Only generate a vulnerability entry for a filesystem operation that can be triggered by a concrete HTTP route / entry point, and you must be able to provide the real route with complete parameters for the PoC.
   - If the concrete route entry point cannot be located (e.g. a pure background job / scheduled task / CLI tool with an untraceable entry point), that FS risk may only be noted in the report as "entry point not located, entry generation skipped (trigger path to be completed manually)", and must not be output as a vulnerability entry with a non-executable PoC.

## Report Output
Output to:
```
{output_path}/vuln_audit/fs_{timestamp}.md
```

## Vulnerability ID Convention (recommended: FS)
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-FS-{sequence}`

## Vulnerability Entry Template (Mandatory)
Every finding must follow the structure below (no omissions):

```markdown
### [{severity-prefix}-FS-{sequence}] Filesystem Operation Chain Risk (permission / link / deletion / TOCTOU / path control)

| Item | Information |
|------|------|
| Severity Level | {🔴/🟠/🟡/🔵} (CVSS {score}) |
| Reachability (R) | {0-3} - {rationale} |
| Impact Scope (I) | {0-3} - {rationale} |
| Exploitation Complexity (C) | {0-3} - {rationale} |
| Exploitability | ✅ Confirmed / ⚠️ Unverified / ❌ Not Exploitable / 🔍 Environment-Dependent |
| Location | {file}:{line} ({Function/Class}) |

#### Data Flow Chain (Source → Path Control → FS Operation → Chain Influence)
(write line by line: how user/context input enters the path control variable, whether it passes through realpath/canonicalize and prefix validation, how it finally reaches the parameters of filesystem operations such as mkdir/chown/symlink/unlink/rename, and how that filesystem operation affects the capability of subsequent chains: WRITE/UPLOAD/FILE/ARCHIVE/CMD/TPL/EXPR/DESER, etc.)

#### Exploitability Preconditions
- Authentication Requirement: {none / login required / specific privilege required}
- Input Controllability: {fully controllable / conditionally controllable / not controllable}
- Trigger conditions: {branch / exception path / specific file system permissions required / race window required / specific directory structure required}
- Chain continuation: {how it provides "exploitability-enhancing" explanation for other sink categories (write drop location / includability / privilege escalation / execution policy bypass / race trigger)}

#### Verification PoC (mandatory: observable verification framework)
```http
{HTTP Method} {real route with full parameters} HTTP/1.1
Host: {host}
{required Header/Session/JWT/Cookie}

{Payload}
```

PoC output / observation points (must be spelled out):
1. Whether the file system state change caused by this FS operation is observable (e.g. file created under the target path / permission change / link target change / deletion result / final drop location existence).
2. If it is TOCTOU: demonstrate the observable phenomenon of "the resolved path at the check point differs from the resolved path at the use point / the window can be exploited" (e.g. concurrent triggering causes the final drop location to change).

#### Evidence References (mandatory: from source snippets)
Must include at least three evidence snippets matching the location (key lines may be restated directly in the text):
1. FS operation call site (mkdir/chmod/chown/symlink/unlink/rename, etc.) and parameter positions (file:line)
2. Path validation / normalization logic (realpath/canonicalize/baseDir prefix validation) and its relationship to the FS operation (within the same function or across functions)
3. Path control source (GET/POST/SESSION/hardcoded configuration, etc.) and its propagation chain

#### Recommended Fix
- Path validation and actual use must be bound to the same resolved target: after `realpath`/canonicalize, use the same value for open/rename/write (avoid TOCTOU)
- Splitting "validate first, use later" is forbidden for paths that an attacker can influence; if the split is unavoidable, complete it within the same system call / same file descriptor context
- For symlink/hardlink: enable a no-link policy at the target drop location (disable symlink following when the platform supports it, or verify consistency based on inode / file descriptor)
- Permission changes must be minimized and must not be influenceable by the user; avoid paths where an attacker can control `chmod/chown`

#### Code Search Queries (mandatory)
```text
rg -n "(mkdir\\(|rmdir\\(|touch\\(|tmpfile\\(|tempnam\\(|chmod\\(|chown\\(|chgrp\\(|symlink\\(|readlink\\(|link\\(|unlink\\(|rename\\(|copy\\(|symlink\\()" .
rg -n "(realpath\\(|canonicalize\\(|dirname\\(|basename\\(|baseDir|dest(path)?|target(path)?)" .
```

## Remediation Recommendations (Mandatory Points)
- Path validation and actual use must be bound to the same resolved target: after `realpath`/canonicalize, use the same value for open/rename/write (avoid TOCTOU)
- Splitting "validate first, use later" is forbidden for paths that an attacker can influence; if the split is unavoidable, complete it within the same system call / same file descriptor context
- For symlink/hardlink: enable a no-link policy at the target drop location (disable symlink following when the platform supports it, or verify consistency based on inode / file descriptor)
- Permission changes must be minimized and must not be influenceable by the user; avoid paths where an attacker can control `chmod/chown`
