---
name: java-sql-audit
description: "SQL injection audit tool for Java Web source code. Locates all SQL execution entry points in source code and detects injection vulnerabilities. Suitable for: (1) identifying SQL execution frameworks and implementation approaches, (2) discovering SQL injection vulnerabilities, (3) checking parameterized query usage, (4) detecting dynamic SQL concatenation flaws. Supports the three mainstream frameworks JDBC, MyBatis, and Hibernate. **Supports decompiling .class/.jar files to extract SQL logic**. Combined with java-route-mapper, it enables a complete route + SQL injection audit."
zh-signals: "Java Web 源码 SQL 注入漏洞审计，定位 JDBC/MyBatis/Hibernate 的 SQL 执行入口并检测拼接型注入。信号:SQL注入,Java审计,MyBatis,JDBC,Hibernate"
when-to-use: >-
  Use when auditing Java Web source code (including decompiled .class/.jar files) for
  SQL injection and parameterization gaps, typically after java-route-mapper has mapped the routes.
---

# Java SQL Injection Audit Tool

Scans Java Web project source code, locates all SQL execution entry points, and detects SQL injection vulnerabilities.

> **Audit scope (this skill detects only the following, and must not go beyond this scope):**
> - ✅ SQL injection vulnerabilities (parameter concatenation, dynamic SQL, ORDER BY injection, etc.)
> - ✅ Missing parameterized queries
> - ❌ Not included: code quality issues, architecture security issues, other vulnerability types (XSS/SSRF/command injection, etc.)

---

## Vulnerability Severity Rating Standard

**See [SEVERITY_RATING.md](../shared/SEVERITY_RATING.md) for details**

- Vulnerability ID format: `{C/H/M/L}-SQL-{index}`
- Severity Level = f(Reachability R, Impact Scope I, Exploitation Complexity C)
- Score = R × 0.40 + I × 0.35 + C × 0.25, mapped to CVSS 3.1

---

## Core Requirements

**This skill must fully analyze all SQL-related code; omissions are not allowed.**

- ✅ Identify all SQL execution entry points (JDBC/MyBatis/Hibernate)
- ✅ Analyze the parameterization of each SQL operation
- ✅ Detect all potential SQL injection patterns
- ✅ Provide a verification PoC for each risk point
- ❌ Never omit any SQL operation
- ❌ Never skip the decompilation step

### No-Omission Rules (Mandatory)

**All lists and tables in the report must be output in full; any form of omission is forbidden:**

| Forbidden Form | Correct Approach |
|:---------|:---------|
| `{...omitted...}` | List every item in full |
| `... (other N items)` | List every item in full |
| `etc.` | List every item in full |
| `and so on` | List every item in full |
| `see xxx for more` | List everything in full at the current location |

**Example - incorrect form:**
```markdown
| # | Method Name | Description |
|---|--------|------|
| 1 | getCommonQuery | Common query |
| 2 | getCollisionQuery | Collision query |
|{...omitted...}| ... | ... |    ← ❌ Forbidden
```

**Example - correct form:**
```markdown
| # | Method Name | Description |
|---|--------|------|
| 1 | getCommonQuery | Common query |
| 2 | getCollisionQuery | Collision query |
| 3 | getIntervalQuery | Interval query |
| ... | ... | ... |
| 23 | getNewStaypointQuery | New staypoint query |    ← ✅ Listed in full
```

**Content that must be listed in full:**
- List of affected methods
- SQL operation mapping table
- Vulnerability detail list
- Parameter list
- Verification payload list

---

## Skill Collaboration Workflow (CRITICAL)

**java-sql-audit should run after java-route-mapper, auditing based on the already-mapped route information.**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Complete Audit Workflow                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Step 1] java-route-mapper                                     │
│     │                                                           │
│     │ Output:                                                   │
│     │ ├─ List of all HTTP routes                                │
│     │ ├─ Parameter definition for each route                    │
│     │ │   ├─ Parameter name, type                               │
│     │ │   └─ JSON internal fields (e.g. pageJson.orderBy)       │
│     │ └─ Burp Suite request templates                           │
│     │                                                           │
│     ↓                                                           │
│  [Step 2] java-sql-audit (this skill)                           │
│     │                                                           │
│     │ Input: output of java-route-mapper                        │
│     │                                                           │
│     │ Execution:                                                │
│     │ ├─ Quick scan of high-risk files                          │
│     │ ├─ Parameter-SQL mapping analysis                         │
│     │ ├─ Check whether each String parameter reaches SQL        │
│     │ └─ Execution condition analysis                           │
│     │                                                           │
│     ├─── Deep tracing needed ───→ java-route-tracer             │
│     │                           │                               │
│     │    ←── returns call chain info ────┘                      │
│     │                                                           │
│     ↓                                                           │
│  [Step 3] Output the comprehensive audit report                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Input Dependencies (from java-route-mapper)

**Before starting the audit, check whether java-route-mapper output files already exist:**

```
{project_name}_audit/
├── route_mapper/
│   ├── {project_name}_route_mapper_{timestamp}.md    ← Main index (read this file first to locate module details)
│   ├── {module_name}/
│   │   └── {project_name}_module_{module_name}_{timestamp}.md  ← Module details
│   └── webservice/
│       └── {project_name}_ws_{service_name}_{timestamp}.md
└── sql_audit/
    └── {project_name}_sql_audit_{timestamp}.md  ← Output of this skill
```

**If route_mapper output does not exist, it must be run first (if not run, stop the audit and return an error message):**
```python
Skill(skill="java-route-mapper", args="--project {project_path}")
```

### Key Information Obtained from route_mapper

| Information | Purpose |
|:-----|:-----|
| Route path | Locate the Controller/Action entry point |
| Parameter name + type | Identify high-risk String parameters |
| JSON internal fields | Identify nested parameters (e.g. `pageJson.orderBy`) |
| Parameter purpose description | Determine whether it is used in SQL (sorting, grouping, etc.) |

---

## Workflow (Three Phases)

### Stage 1: Quick Scan (execute first)

**Goal: quickly locate high-risk files and patterns without missing key points.**

```bash
# 1.1 Search for pagination/sorting helper classes (most easily missed)
find . -name "*Pagination*.java" -o -name "*PageHelper*.java" -o -name "*Pager*.java"
find . -name "*JdbcSupport*.java" -o -name "*JdbcTemplate*.java"

# 1.2 Search for DAO base classes
find . -name "Abstract*Dao*.java" -o -name "Base*Dao*.java" -o -name "*Support.java"

# 1.3 Search for ORDER BY concatenation patterns
grep -ri "order by" --include="*.java" | grep -v "ORDER BY \?"
grep -ri "getOrderBy\|getSortField\|getOrder\|getSortOrder" --include="*.java"
grep -ri "append.*order" --include="*.java"

# 1.4 Search for SQL execution points
grep -ri "executeQuery\|executeUpdate\|prepareStatement" --include="*.java"
grep -ri "createQuery\|createNativeQuery\|createSQLQuery" --include="*.java"
```

**Output: list of high-risk files (sorted by priority)**

| Priority | File Type | Audit Focus |
|:-------|:---------|:---------|
| P0 | `*Pagination*.java`, `*PageHelper*.java` | orderBy, order, sort parameters |
| P1 | `Abstract*Dao.java`, `Base*Dao.java` | Generic SQL construction methods |
| P2 | `*Mapper.java`, `*Dao.java`, `*Repository.java` | Business SQL operations |
| P3 | `*Mapper.xml` | MyBatis ${} usage |

### Stage 2: Parameter-SQL Mapping Analysis

**Based on java-route-mapper output, analyze whether each parameter reaches SQL.**

#### 2.1 High-Risk Parameter Identification

Extract all String-type parameters from the route_mapper output:

| Parameter Source | Parameter Name | Type | SQL Injection Level |
|:---------|:-------|:-----|:---------|
| pageJson | `orderBy` | String | **High** - sort field concatenated directly |
| pageJson | `order` | String | **High** - sort direction concatenated directly |
| searchJson | `keyword` | String | **High** - search keyword concatenated directly |
| searchJson | `status` | String | Medium - status filter concatenation |
| pageJson | `pageSize` | int | Low - numeric type hard to inject |

#### 2.2 Parameter Tracing

For each high-risk parameter, trace its use in the code:

```
HTTP parameter: pageJson.orderBy (String)
    ↓ deserialization
Page.orderBy
    ↓ pass
Service.method(page)
    ↓ pass
Dao.query(page)
    ↓ call
AbstractDao.findSql(page)
    ↓ use
sql.append(" order by ").append(page.getOrderBy())  ← SQL concatenation point
```

#### 2.3 SQL Execution Point Check

For each SQL execution point found in Stage 1, check:

1. **Is a parameterized query used?**
   - `PreparedStatement` + `?` placeholder → safe
   - String concatenation → dangerous

2. **What is the source of the concatenated parameter?**
   - String parameter from an HTTP request → high risk
   - From system configuration/constants → safe
   - From database query results → requires further analysis

3. **Is there input validation?**
   - Whitelist validation → safe
   - No validation, direct concatenation → high risk

### Stage 3: Deep Analysis and Reporting

#### 3.1 Triggering java-route-tracer

When any of the following is found, call java-route-tracer to obtain the complete call chain:

| Trigger Condition | Invocation Method |
|:---------|:---------|
| Parameter passes through multiple layers | `Skill(skill="java-route-tracer", args="--route {route}")` |
| Branch condition is unclear | `Skill(skill="java-route-tracer", args="--route {route}")` |
| SQL execution in a parent class | `Skill(skill="java-route-tracer", args="--route {route}")` |

#### 3.2 Execution Condition Analysis

After discovering SQL concatenation, you must analyze the execution conditions (see later sections for details).

#### 3.3 Generate Report

Integrate all analysis results and generate a comprehensive audit report.

---

## SQL Framework Identification

| Framework | Identification Features | Configuration Files | References |
|------|----------|----------|----------|
| JDBC | `java.sql.*`, `Statement`, `PreparedStatement`, `DriverManager` | - | [JDBC.md](references/JDBC.md) |
| MyBatis | `@Mapper`, `@Select`, `SqlSession`, `#{}`/`${}` | `mybatis-config.xml`, `*Mapper.xml` | [MYBATIS.md](references/MYBATIS.md) |
| Hibernate | `@Entity`, `Session.createQuery()`, `HQL`, `Criteria` | `hibernate.cfg.xml`, `persistence.xml` | [HIBERNATE.md](references/HIBERNATE.md) |

### 3. Decompilation Stage (CRITICAL)

**When source code is unavailable, you must use the MCP Java Decompiler to decompile SQL-related classes.**

See [DECOMPILE_STRATEGY.md](references/DECOMPILE_STRATEGY.md) for the detailed strategy

#### 3.1 Decompiler Invocation

```python
# Decompile a single DAO/Mapper class
mcp__java-decompile-mcp__decompile_file(
    file_path="/path/to/UserMapper.class",
    output_dir="/path/to/decompiled",
    save_to_file=True
)

# Decompile a DAO-related directory
mcp__java-decompile-mcp__decompile_directory(
    directory_path="/path/to/WEB-INF/classes/com/example/dao",
    output_dir="/path/to/decompiled",
    recursive=True,
    save_to_file=True,
    max_workers=4
)

# Decompile multiple specified files
mcp__java-decompile-mcp__decompile_files(
    file_paths=[
        "/path/to/UserDao.class",
        "/path/to/OrderService.class",
        "/path/to/BaseMapper.class"
    ],
    output_dir="/path/to/decompiled",
    save_to_file=True
)
```

#### 3.2 Classes That Must Be Decompiled

| Type | Match Pattern | Purpose |
|------|----------|------|
| DAO/Mapper | `*Dao.class`, `*Mapper.class`, `*Repository.class` | Extract SQL execution logic |
| Service | `*Service.class`, `*ServiceImpl.class` | Trace the SQL call chain |
| Utility classes | `*SqlUtil*.class`, `*DbHelper*.class` | Extract generic SQL methods |
| Entity classes | `*Entity.class`, `*Model.class` | Hibernate annotation analysis |

---

## Execution Condition Analysis (CRITICAL - Avoid False Positives)

**After discovering SQL concatenation code, you must analyze whether that code will actually be executed!**

### 1. Database Type Branch Check

After discovering SQL concatenation, you must check whether a database type check exists:

| Check Pattern | Code Features | Handling |
|----------|----------|----------|
| Oracle branch | `isOracle()`, `getDbType().equals("oracle")` | Mark as Oracle-only |
| MySQL branch | `isMySQL()`, `isMySql()`, `getDbType().equals("mysql")` | Mark as MySQL-only |
| Common code | No database type check | Mark as common |

**Example analysis:**
```java
public String getSql(QueryBean bean, List<Object> params) {
    if (this.isOracle()) {
        return this.getOracleSql(bean, params);  // Oracle branch - SQL concatenation happens here
    }
    return "";  // ⚠️ MySQL branch - returns an empty string directly!
}
```

### 2. Code Path Reachability Analysis

Trace the complete path from entry point to SQL execution, and check:

| Check Item | Description | Impact |
|--------|------|------|
| Early return | `return ""`, `return null` | Code does not execute |
| Exception thrown | `throw new Exception()` | Code does not execute |
| Condition unmet | Dead code such as `if (false)` | Code does not execute |
| Environment-restricted | Executes only with a specific database/configuration | Environment must be confirmed |

### 3. Conclusion Grading (Must Be Annotated)

| Status | Meaning | Follow-up Action |
|------|------|----------|
| ⚠️ **To Be Verified** | SQL concatenation exists, but execution conditions are unconfirmed | Target environment must be confirmed |
| ✅ **Confirmed Exploitable** | Code path verified to execute in the target environment | Perform exploitation testing |
| ❌ **Not Exploitable** | Code exists but does not execute in the target environment | Annotate the reason and lower the priority |
| 🔍 **Environment-Dependent** | Vulnerability exists but is exploitable only in a specific environment | Annotate the environment condition |

### 4. Audit Process Correction

```
SQL concatenation code discovered
       ↓
Check whether a database type branch exists (isOracle/isMySQL)
       ↓
  ┌────┴────┐
 Present    Absent
  ↓         ↓
Analyze each   Continue with
branch         routine analysis
  ↓
Confirm the target environment's database type
  ↓
Determine whether the vulnerable code will execute
  ↓
  ┌────┴────┐
Executes   Does not execute
  ↓         ↓
Mark ✅     Mark ❌
Confirmed  Not exploitable
```

### 5. Report Output Requirements

**When SQL concatenation is found, the report must include:**

```markdown
### Execution Condition Analysis

| Item | Value |
|------|-----|
| Code location | AnalyseDaoImpl.java:187 |
| Branch condition | `if (this.isOracle())` |
| Oracle branch | Calls getOracleSql() → SQL concatenation |
| MySQL branch | `return ""` → does not execute |
| Target environment | MySQL |
| **Exploitability** | ❌ Not exploitable (code path does not execute in the MySQL environment) |
```

---

## SQL Injection Detection Rules Quick Reference

### Core Detection Principles

**Identify by behavior, not fixed naming patterns. Developers may use arbitrary names, and fixed patterns will cause missed detections!**

| Principle | Description |
|:-----|:-----|
| Behavior first | Search for SQL keyword concatenation behavior, not method/class names |
| Data flow tracing | Trace whether any String parameter flows into SQL |
| Multi-database coverage | Detection must cover Oracle, MySQL, PostgreSQL, SQL Server, etc. |

**For detailed detection strategies, see: [SQL_DETECTION_RULES.md](references/SQL_DETECTION_RULES.md)**

### Detection Rules Reference

| Detection Type | Description | Reference Document |
|:---------|:-----|:---------|
| Generic behavior detection | SQL keyword concatenation, data flow tracing, pagination/sorting | [SQL_DETECTION_RULES.md](references/SQL_DETECTION_RULES.md) |
| JDBC framework | Statement, PreparedStatement, parameterization | [JDBC.md](references/JDBC.md) |
| MyBatis framework | `#{}` vs `${}`, dynamic SQL | [MYBATIS.md](references/MYBATIS.md) |
| Hibernate framework | HQL, Criteria, Native Query | [HIBERNATE.md](references/HIBERNATE.md) |

### Quick Detection Commands

```bash
# Search for SQL keyword concatenation (generic, not name-dependent)
grep -ri "order by\|group by" --include="*.java" | grep -E "\+|\.append"
grep -ri "limit\s|offset\s|rownum|row_number" --include="*.java"
```

---

### ⚠️ Parameter Types and Injection Risk

**SQL injection vulnerabilities occur mainly on String-type parameters!**

| Parameter Type | Injection Risk | Reason |
|----------|----------|------|
| `String` | **High** | Can inject arbitrary SQL fragments |
| `Integer`/`int` | Low | Invalid input throws NumberFormatException |
| `Long`/`long` | Low | Invalid input throws NumberFormatException |
| `Boolean`/`boolean` | Low | Can only be true/false |

**Audit points:**
- Focus on SQL concatenation of `String`-type parameters
- **Pay special attention to sorting/grouping parameters such as orderBy, order, groupBy**
- Numeric-type parameters are hard to inject even when concatenated (but precompilation is still recommended)
- Check whether there is intermediate handling that converts String to numeric

---

### JDBC Dangerous vs Safe → [Detailed Rules](references/JDBC.md)

| Type | Dangerous Pattern | Safe Pattern |
|------|----------|----------|
| Query | `stmt.executeQuery("..."+var)` | `pstmt.setXxx(1, var)` |
| Concatenation | `+`, `StringBuilder`, `String.format` | `?` placeholder |
| **ORDER BY** | `" order by " + orderBy` | **Whitelist validation** |

### MyBatis Dangerous vs Safe → [Detailed Rules](references/MYBATIS.md)

| Type | Dangerous Pattern | Safe Pattern |
|------|----------|----------|
| Parameter | `${param}` | `#{param}` |
| like | `'%${keyword}%'` | `CONCAT('%', #{keyword}, '%')` |
| **order by** | `ORDER BY ${col}` | **Use after whitelist validation** |
| in | `IN (${ids})` | `<foreach>` tag |

### Hibernate Dangerous vs Safe → [Detailed Rules](references/HIBERNATE.md)

| Type | Dangerous Pattern | Safe Pattern |
|------|----------|----------|
| HQL | `"FROM User WHERE name='"+n+"'"` | `query.setParameter("name", n)` |
| Native | `createNativeQuery(sql+var)` | Parameter binding |
| Criteria | `Restrictions.sqlRestriction(str)` | `CriteriaBuilder` API |
| **Sorting** | `" order by " + sortField` | **Whitelist validation** |

**When detailed detection rules are needed, click the corresponding framework link to load the full document.**

---

## Audit Checklist (to prevent omissions)

### Dangerous Patterns That Must Be Searched

**At the start of the audit, the following searches must be performed:**

```bash
# ORDER BY injection detection
grep -r "order by" --include="*.java" | grep -v "ORDER BY \?"
grep -r "getOrderBy\|getSortField\|getOrder\|getSortOrder" --include="*.java"
grep -r "append.*order" --include="*.java"

# GROUP BY injection detection
grep -r "group by" --include="*.java" | grep -v "GROUP BY \?"
grep -r "getGroupBy" --include="*.java"

# Pagination helper class detection
find . -name "*Pagination*.java" -o -name "*PageHelper*.java" -o -name "*JdbcSupport*.java"

# Base class detection
find . -name "Abstract*Dao*.java" -o -name "Base*Support*.java"
```

---

## Data Flow Tracing (load java-route-tracer when needed)

### When Parameter Tracing Is Needed

When the following situations are found, **you must invoke the java-route-tracer skill for deep tracing**:

| Scenario | Description | Operation |
|------|------|------|
| Parameter passes through multiple layers | HTTP parameter passes through Controller → Service → DAO multiple layers before being concatenated into SQL | Load java-route-tracer |
| Parameter type conversion | After a String JSON is deserialized into an object, one field is used in SQL | Load java-route-tracer |
| Parent/base class SQL execution | SQL execution happens in a base class such as AbstractDao | Load java-route-tracer |
| Variable name changes multiple times | The same parameter uses different variable names at different layers | Load java-route-tracer |

### Auto-trigger java-route-tracer (Claude Code Convention)

When the following scenarios are found, **you must automatically invoke the java-route-tracer skill**:

```python
# When parameter flow needs to be traced, automatically invoke java-route-tracer
mcp__cclsp__find_references  # First analyze method references
# Then trigger automatically
Skill(
    skill="java-route-tracer",
    args="--route {controller_route} --project {project_path}"
)
```

### Vulnerability Determination Based on tracer Output (CRITICAL - Prevent Misjudgment)

**java-sql-audit must determine vulnerabilities based on the "actual parameter usage analysis" output of java-route-tracer.**

#### Determination Flow

```
1. Invoke java-route-tracer to obtain the tracing report
       ↓
2. Read the "Actual Parameter Usage Analysis" section
       ↓
3. Filter parameters
   ├─ "✅ Used" → perform SQL injection detection
   ├─ "❌ Not used" → skip, do not mark as a vulnerability
   └─ "⚠️ Partially used" → detect only the fields that are used
       ↓
4. Perform detailed analysis on the "used" parameters
       ↓
5. Output the audit conclusion
```

#### tracer Output Example and audit Determination

| Parameter | tracer Output (Actual Usage Status) | sql-audit Determination |
|:-----|:---------------------------|:---------------|
| page.orderBy | ❌ Not used (overridden by hardcoding) | ⏭️ **Skip**, do not detect |
| page.order | ❌ Not used (overridden by hardcoding) | ⏭️ **Skip**, do not detect |
| searchBean.keyword | ✅ Used (`#{keyword}` parameterized) | 🔍 Detect → safe (parameterized) |
| searchBean.status | ✅ Used (`${status}` concatenation) | 🔍 Detect → **vulnerability found** |

#### Representation in the Audit Report

```markdown
### [SQL-001] ORDER BY Injection Analysis

| Check Item | Result |
|:-------|:-----|
| Concatenation code location | PaginationJdbcSupport.java:115 |
| Calling method | UserBulletinDaoImpl.getUserBulletinReplayList() |
| **tracer parameter analysis** | page.orderBy → ❌ Not used (overridden by hardcoding) |
| Hardcoding details | `sql + " order by replayDateStr desc"` |
| **Conclusion** | ❌ **Not a vulnerability** - parameter is not actually used |

---

### [SQL-002] WHERE Condition SQL Injection

| Check Item | Result |
|:-------|:-----|
| Concatenation code location | UserDaoImpl.java:89 |
| Calling method | UserDaoImpl.searchUsers() |
| **tracer parameter analysis** | searchBean.status → ✅ Used (`${status}` concatenation) |
| Parameter source | HTTP request searchJson.status |
| **Conclusion** | ✅ **Vulnerability confirmed** - parameter is concatenated directly into SQL |
```

#### tracer Output Fields That Must Be Checked

| tracer Output Field | Purpose |
|:----------------|:-----|
| `Actual usage status` | Determine whether the parameter needs to be detected |
| `Overridden by hardcoding` | Rule out false positives in hardcoded scenarios |
| `Sensitive operation type` | Determine the detection rule (SQL/command/SSRF, etc.) |
| `Hardcoding override details` | Output to the audit report as evidence |

### Trigger Conditions (Auto-invocation)

| Scenario | Operation |
|------|------|
| Parameter passes through multiple layers | Invoke java-route-tracer to trace the complete call chain |
| Parameter type conversion | Invoke java-route-tracer to trace the parameter conversion process |
| Parent/base class SQL execution | Invoke java-route-tracer to trace the inheritance chain |
| Variable name changes multiple times | Invoke java-route-tracer to trace variable name changes |
| Execution condition unclear | Invoke java-route-tracer to analyze branch conditions |

### java-route-tracer Collaboration Content

**Parameters passed on invocation:**
- `--route`: the corresponding HTTP route (e.g. `/api/users/getUserById`)
- `--project`: project path (used for decompilation and code analysis)

**java-route-tracer returns:**
- Complete call chain information (L1 → L2 → L3 → L4)
- Parameter variable name changes at each layer
- Branch condition analysis of the execution path
- Final SQL usage point location
- HTTP request template (usable in Burp Suite)

**Collaboration flow:**
```
java-sql-audit                    java-route-tracer
     │                                   │
     │  SQL injection point discovered   │
     │  Scenario requiring deep trace    │
     │  detected                         │
     │                                   │
     └───────── Skill tool invocation ───→│
                                         │
                                         │  Trace the complete call chain
                                         │  Analyze branch conditions
                                         │  Output parameter flow
                                         │
     ←───────── Automatically returns ─────┘
     │
     │  Annotate exploitability using tracing results
     ▼
```

---

## Report Generation

**Output a single comprehensive audit report file:**

```
{project_name}_audit/sql_audit/
└── {route_name}/
    └── {project_name}_sql_audit_{timestamp}.md      # Comprehensive audit report
```

**Route Name Notes:**
- Route names are extracted from the route path, stripping leading slashes and special characters
- For example: `/itc/ws/carQuery` → `itc_ws_carQuery`
- For example: `/api/user/login.action` → `api_user_login`

---

## Output Format

**Generate the output file strictly following the fill-in template in [references/OUTPUT_TEMPLATE.md](references/OUTPUT_TEMPLATE.md).**

- File name format: `{project_name}_sql_audit_{YYYYMMDD_HHMMSS}.md`
- Do not modify the template structure, add or remove sections, or change their order
- All [FILL IN] placeholders must be replaced with actual content
- Common specification reference: [shared/OUTPUT_STANDARD.md](../shared/OUTPUT_STANDARD.md)

---

## Verification Checklist

**Before marking the audit as complete, the following checks must be performed:**

### Code Analysis Check
- [ ] All DAO/Mapper classes have been analyzed
- [ ] All SQL configuration files (*Mapper.xml) have been parsed
- [ ] Every SQL operation has a parameterization status annotation

### Execution Condition Check (CRITICAL)
- [ ] Database type branches checked (isOracle/isMySQL)
- [ ] Code path reachability analyzed
- [ ] Exploitability status annotated for each vulnerability

### Vulnerability Detection Check
- [ ] All JDBC concatenation patterns detected
- [ ] All MyBatis ${} usages detected
- [ ] All Hibernate HQL concatenations detected

### Report Completeness Check
- [ ] **The comprehensive audit report has been generated and passes the self-check checklist at the end of OUTPUT_TEMPLATE.md**

---

## References

- [OUTPUT_TEMPLATE.md](references/OUTPUT_TEMPLATE.md) - Fill-in template for the output report
- [JDBC.md](references/JDBC.md) - Detailed JDBC SQL injection audit guide
- [MYBATIS.md](references/MYBATIS.md) - Detailed MyBatis SQL injection audit guide
- [HIBERNATE.md](references/HIBERNATE.md) - Detailed Hibernate SQL injection audit guide
- [DECOMPILE_STRATEGY.md](references/DECOMPILE_STRATEGY.md) - Decompilation strategy guide