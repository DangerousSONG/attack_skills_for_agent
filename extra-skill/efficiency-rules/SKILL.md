---
name: efficiency-rules
description: "Penetration testing efficiency rules. Prevent inefficient behavior such as blind enumeration and blocking tools, so that the number of vulnerabilities found is maximized within limited time. Use when starting a penetration test, when a scanning tool takes too long to run, when you fall into a blind brute-force loop, or when you need to decide the next attack direction. Recommended reading before each pentest round"
zh-signals: "渗透测试效率规则，避免盲目枚举与工具阻塞，在有限时间内最大化漏洞发现。信号:效率,枚举,超时,优化,渗透测试"
when-to-use: "Use at the start of a penetration test or when enumeration loops, long-running tools, or unclear next steps threaten to waste engagement time."
metadata:
  tags: "efficiency,enumeration,timeout,optimization,pentest efficiency,enumeration,timeout"
  category: "general"
---

# Penetration Testing Efficiency Rules

## ⛔ Rule 1: No Blind Manual Enumeration

**Trigger scenario**: testing paths one by one with curl (e.g. /upload, /admin/upload, /bank/upload ...)

**Rule**:
- For paths of the same type (e.g. file upload endpoints), try at most the **3 most likely paths manually with curl**
- After 3 x 404 responses, **stop manual enumeration immediately** and switch to a tool:
  ```bash
  # ✅ Sweep them all at once with gobuster/dirsearch
  gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt -q -t 20 --timeout 10s 2>&1 | head -50
  ```
- ⛔ **Never** issue 20+ HEAD requests one by one for guessed paths — that wastes time

## ⛔ Rule 2: Long-Running Tools Must Have a Timeout

**Trigger scenario**: running scanners such as sqlmap, nikto, dirsearch

**Rule**:
- All scanning tools must be wrapped in `timeout`, at most **8 minutes**
- Always keep the output with `tee` so partial results can be inspected after a timeout
  ```bash
  # ✅ Correct
  timeout 480 sqlmap -u 'http://target/page?id=1' --batch --level 2 --risk 2 2>&1 | tee /tmp/sqlmap.log
  # After the timeout
  tail -80 /tmp/sqlmap.log
  ```
- ⛔ **Forbidden**: `sleep N && tail` polling waits — they waste round-trip time

## ⛔ Rule 3: Switch Direction Quickly When There Are No Results

**Trigger scenario**: multiple consecutive attempts at the same vulnerability class yield nothing

**Rule**:
- Same endpoint + same vulnerability type: **switch direction after 5 different payloads yield nothing**
- Before switching, record what has been tested with `evidence_save` (to avoid repeating it next round)
- Prefer switching to an untested vulnerability type over trying more variants of the same type

## Efficiency Priorities

| Behavior | Efficiency | Description |
|------|------|------|
| Batch scanning with tools | ⭐⭐⭐ | gobuster/sqlmap/nikto cover many paths in one run |
| Targeted manual testing | ⭐⭐ | Precisely test 3-5 high-probability points based on analysis results |
| Blind manual enumeration | ⛔ | Guessing paths with curl one by one, extremely inefficient |
