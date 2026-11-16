---
name: ctf-flag-verification
description: "Mandatory CTF/lab flag verification workflow. When a suspected flag string (including flag{, FLAG{, ctf{ and similar formats) is found **by any means**, this skill **must be used immediately** to verify it — do not submit it directly. This prevents submitting a wrong flag due to character truncation, encoding errors, HTML entities, incomplete base64 decoding, hex truncation, and similar causes. Even if the flag looks complete, hidden characters or encoding problems may remain. Covers all flag extraction scenarios including SQL injection chunked extraction, command execution output truncation, file read encoding, and web page parsing. Trigger this skill whenever you see the string flag{"
zh-signals: "在提交前强制用程序验证 CTF flag 的长度、格式与编码，避免截断或解码错误。信号:ctf,flag验证,编码解码,截断,靶场,提交"
when-to-use: >-
  Use whenever you find a suspected flag string (flag{, FLAG{, ctf{) in a CTF or lab,
  especially after SQL injection, RCE, file read, or web page extraction, and before submitting it.
metadata:
  tags: "ctf,flag,verification,capture the flag,lab,flag verification,sqli,rce,lfi,file-read,submit,flag{,suspected flag,flag format,flag truncation,encoding restoration,hex,base64 decoding,character truncation,HTML entities,extraction verification"
  category: "ctf"
---

# CTF Flag Verification Methodology

## Core Principles

**LLMs cannot reliably count hex characters or concatenate long strings.** All flag extraction, concatenation, and verification must be done with a program (Python) — never concatenate by hand.

## Mandatory Verification Workflow

### 1.1 Prefer programmatic methods when extracting flags

**SQL injection (EXTRACTVALUE/UPDATEXML chunked extraction):**
- ❌ Do not copy each chunk manually and concatenate it in your head
- ✅ Write a Python script that sends the requests, splits the chunks, and concatenates them automatically (see the Python template in sql-injection-methodology)
- ✅ Prefer UNION SELECT (no truncation limit, gets the complete flag in one shot)

**Command execution (RCE / command injection):**
- ⚠️ `cat /flag.txt` output may contain a trailing newline → strip it with `flag.strip()`
- ⚠️ Command output may be HTML-encoded (`&lt;` → `<`) → decode it with Python `html.unescape()`
- ⚠️ If the output is truncated, use `base64 /flag.txt` and decode it

**File read (LFI / arbitrary file read):**
- ⚠️ PHP `file_get_contents` may return base64 → decode it first
- ⚠️ When reading via php://filter: `php://filter/convert.base64-encode/resource=flag` → a base64 decode is required
- ⚠️ Path case sensitivity: `/flag.txt` ≠ `/Flag.txt` ≠ `/FLAG.txt`

**Web page parsing:**
- The flag may be in an HTML comment `<!-- flag{...} -->`
- The flag may be in an HTML attribute `data-flag="flag{...}"`
- The flag may be in a JavaScript variable `var flag = "flag{...}"`
- Extract it with Python `re.search(r'flag\{[a-fA-F0-9_-]+\}', html_text)`

### 1.2 Length verification

If you learned the expected length of the flag through SQL `LENGTH()` or another means, verify it with Python:
```python
flag = "flag{...extracted...}"
expected_length = 70  # obtained from LENGTH()
assert len(flag) == expected_length, f"MISMATCH! {len(flag)} != {expected_length}"
```

### 1.3 Format verification

```python
import re
flag = "flag{...}"
assert re.match(r'^flag\{[a-fA-F0-9_-]+\}$', flag), f"Invalid format: {flag}"
assert flag.endswith('}'), "Missing } — flag may be truncated"
```

### 1.4 Handling verification failure

1. **Length mismatch** → re-extract. Switch EXTRACTVALUE to a Python automated script or UNION SELECT
2. **Wrong format** → check HTML encoding, base64 encoding, trailing whitespace
3. **Repeated failures** → switch extraction method (EXTRACTVALUE → UNION → blind injection → sqlmap --dump)

### 1.5 Common error patterns

| Error | Cause | Solution |
|------|------|------|
| Flag is 1-2 characters short | EXTRACTVALUE 32-character truncation + manual concatenation | Python automated extraction script |
| Flag is 1-2 characters long | Overlapping SUBSTRING start positions | Check the SUBSTRING parameters |
| Wrong character in the middle of the flag | LLM misread hex characters | Extract with Python re.search |
| Flag contains HTML entities | `&amp;` not decoded | `html.unescape()` |
| Flag contains newlines/spaces | Command output contains whitespace | `.strip()` |
| Flag format is wrong | Wrong data extracted | Re-confirm the table name / file path |

### 1.6 Character-level verification issues
- If characters are missing in the middle of the flag, check the position 29-32 region — an offset error may have dropped characters
- HTML entity restoration: `&lt;` becomes `<`, `&amp;` becomes `&`; what the page renders differs from the source, so it must be decoded and restored
- Example: `flag{a3b<c5d&e7f}` — the rendered form differs from the source; only the decoded form is the correct flag
