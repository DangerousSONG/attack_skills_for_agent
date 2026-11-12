---
name: java-route-tracer
description: "Multi-level route call-chain tracing tool for Java Web source code. Given a route path specified by the user, trace the complete call chain from Controller/Action to the DAO layer, and output the file location, method signature, and injectable parameters of each layer. Applicable to parameter flow tracing for multiple vulnerability types: (1) SQL injection - trace parameters to SQL concatenation points, (2) command injection - trace parameters to Runtime.exec(), (3) SSRF - trace parameters to HTTP requests, (4) XSS - trace parameters to response output, (5) file operations - trace parameters to File operations, (6) XXE/deserialization/LDAP injection/expression injection, etc. Supports Spring MVC, Struts 2, Servlet, JAX-RS and other frameworks. **Supports decompiling .class/.jar files to extract call chains**. Combined with java-route-mapper, it enables full route + call-chain auditing."
zh-signals: "追踪 Java Web 路由从 Controller 到 DAO 的调用链与参数流向。信号:Java路由追踪,调用链,参数可控性,Sink定位,反编译。"
when-to-use: >-
  Use when tracing a Java route's full call chain from Controller/Action to DAO or sink across Spring MVC, Struts 2, Servlet, or JAX-RS, and mapping parameter flow to SQLi, RCE, SSRF, XSS, or file sinks.
---

# Java Route Tracer - Route Call-Chain Tracing

Given a user-specified route, trace the complete call chain from the entry point to the final usage point and output layer-by-layer call information. **Applicable to parameter flow tracing across multiple vulnerability types.**

## Core Features

**Outputs call-chain information only; performs no vulnerability detection or security recommendations.**

Output includes:
- **Complete HTTP request packet** - request template directly usable in Burp Suite
- **Detailed parameter definitions** - name, type, and nested structure of each parameter
- **Layer-by-layer call relationships** - Controller → Service → DAO → parent class
- **Parameter flow tracing** - the complete path from the HTTP entry point to the final usage point
- **Parameter variable-name tracing** - how the same parameter's variable name changes across classes
- **Final usage point annotation** - how the parameter is used at the final layer

## Applicable Vulnerability Types

| Vulnerability type | Traced final usage point |
|:---------|:---------------|
| SQL injection | `sql + param`, `Statement.execute()`, MyBatis `${}`, Hibernate HQL concatenation |
| Command injection | `Runtime.exec(cmd)`, `ProcessBuilder(cmd)` |
| SSRF | `HttpClient.execute(url)`, `URL.openConnection()`, `RestTemplate` |
| XSS | `response.getWriter().write()`, template engine output, `@ResponseBody` |
| File operations | `new File(path)`, `FileInputStream()`, `Files.read()` |
| XXE | `DocumentBuilder.parse()`, `SAXParser`, `XMLReader` |
| Deserialization | `ObjectInputStream.readObject()`, `JSON.parseObject()` |
| LDAP injection | `DirContext.search(filter)`, `LdapTemplate` |
| Expression injection | `SpelExpression.getValue()`, OGNL, MVEL, Freemarker |
| Path traversal | `new File(basePath + userInput)`, `Paths.get()` |

---

## Workflow

### 1. Receive user input

Provided by the user:
- **Route path**: e.g. `/admin/user_login.action` or `/api/faceCapture`
- **Project path**: directory containing source code or decompiled files

### 2. Locate the entry point and identify methods

Locate the route entry class based on the framework type:

| Framework | Entry point location method |
|:-----|:-------------|
| Spring MVC | `@RequestMapping` annotation matching |
| Struts 2 | action configuration in struts.xml |
| Servlet | web.xml or `@WebServlet` |
| JAX-RS | `@Path` annotation matching |

**Important note**: When the entry class contains multiple business methods (e.g., a Web Service with multiple interface methods, or a Controller with multiple endpoint methods), the skill automatically identifies and traces all of them. For the detailed implementation strategy, see: [multi-method-tracing.md](references/multi-method-tracing.md)

### 2.1 Multi-method tracing execution flow (mandatory)

**You must strictly follow the steps below and use the TodoWrite tool to manage tasks:**

#### Step 1: Count all methods

First scan the entry class, identify all methods that need tracing, and output the method list:

```
Scanning entry class: VehicleQueryServiceImpl

Found the following 10 methods to trace:
1. getBasicQuery(searchJson, pageJson, extend)
2. getAdvancedQuery(searchJson, pageJson, extend)
3. getDetailQuery(searchJson, pageJson, extend)
4. getStatisticsQuery(searchJson, pageJson, extend)
5. getExportQuery(searchJson, pageJson, extend)
... (list all methods)
10. getReportQuery(searchJson, pageJson, extend)

Total: 10 methods
```

#### Step 2: Create TodoList tasks

**You must use the TodoWrite tool to add each method as a separate task:**

```python
TodoWrite([
    {"content": "Trace method 1/10: getBasicQuery", "status": "pending", "activeForm": "Trace getBasicQuery"},
    {"content": "Trace method 2/10: getAdvancedQuery", "status": "pending", "activeForm": "Trace getAdvancedQuery"},
    {"content": "Trace method 3/10: getDetailQuery", "status": "pending", "activeForm": "Trace getDetailQuery"},
    {"content": "Trace method 4/10: getStatisticsQuery", "status": "pending", "activeForm": "Trace getStatisticsQuery"},
    # ... all 10 methods
    {"content": "Trace method 10/10: getReportQuery", "status": "pending", "activeForm": "Trace getReportQuery"},
    {"content": "Generate the overall index file", "status": "pending", "activeForm": "Generate overall index"}
])
```

#### Step 3: Execute tasks one by one (optimization strategy)

Execute each task in TodoList order, adopting different tracing strategies based on the interface count:

| Interface index | Tracing strategy | Report content |
|:---------|:---------|:---------|
| 1st interface | Full call chain | Includes all layers, branches, variable tracing, and controllability determination |
| 2nd and later interfaces | Simplified call chain | Must include: request template + parameter definitions for this method + call chain + sink identification + controllability determination |

**Execution flow:**
1. Mark the current task as `in_progress`
2. Choose the tracing strategy based on the interface index
3. Generate the corresponding type of report file
4. Mark the task as `completed`
5. Continue to the next task

```
--- Method 1/10: getBasicQuery ---
Status: in_progress
[Full call chain...]
[Generate report: myproject_trace_getBasicQuery_20260205.md]
Status: completed ✅

--- Method 2/10: getAdvancedQuery ---
Status: in_progress
[Simplified call chain...]
[Generate report: myproject_trace_getAdvancedQuery_20260205.md (simplified)]
Status: completed ✅

--- Method 3/10: getDetailQuery ---
Status: in_progress
[Simplified call chain...]
[Generate report: myproject_trace_getDetailQuery_20260205.md (simplified)]
Status: completed ✅

... Continue until all tasks are complete ...
```

#### Step 4: Completion verification

After all methods have been traced:

1. Generate the overall index file
2. Verify the number of generated files
3. Output the completion report

```bash
# Verification command
ls route_tracer/{route_name}/*.md | wc -l
# Expected result: 11 (10 method reports + 1 overall index)
```

### 2.2 Interruption recovery mechanism

**If execution is interrupted, upon resuming you must:**

1. Check the report files already generated
2. Compare against the method list and identify unfinished methods
3. Create TodoList tasks only for the unfinished methods
4. Continue execution

```python
# Check completed methods
existing_files = ls("/path/to/route_tracer/{route_name}/*.md")
completed_methods = [extract_method_name(f) for f in existing_files]

# Create remaining tasks
remaining_tasks = []
for method in all_methods:
    if method not in completed_methods:
        remaining_tasks.append({
            "content": f"Trace method: {method}",
            "status": "pending",
            "activeForm": f"Trace {method}"
        })

TodoWrite(remaining_tasks)
```

### 2.3 Mandatory rules

| Rule | Description |
|:-----|:-----|
| **Must count** | Before starting, you must count and output the total number of methods |
| **Must use TodoList** | You must use TodoWrite to add each method as a task |
| **Interface optimization strategy** | When the interface count > 3, adopt the following optimization:<br>- 1st interface: generate a full call-chain trace (including all layers, branches, and variable tracing)<br>- 2nd and later interfaces: generate only the complete Burp Suite packet + a simple call chain (without detailed code or branch determination) |
| **Must mark status** | Mark each task as completed immediately after it finishes |
| **No early termination** | Do not finish while pending tasks remain in the TodoList |
| **Must verify count** | Before finishing, you must verify the number of generated files |

### 2.4 File generation rules (mandatory)

**Use the following strategy uniformly for all interface counts; no batching is needed:**

| Interface index | Report type | Content |
|:---------|:---------|:-----|
| 1st | Full version | All layers, branches, variable tracing, controllability determination (approx. 20,000-30,000 characters) |
| 2nd and later | Simplified version | Request template + parameter definitions for this method + call chain + sink identification + controllability determination (approx. 2,000-4,000 characters) |

**File naming convention:**

| Rule | Format |
|:-----|:-----|
| ✅ Correct | `{project_name}_trace_{method_name}_{timestamp}.md` |
| ❌ Incorrect | `{method_name}_{timestamp}.md` (missing project prefix) |

**Variable substitution check (mandatory):**

When generating each simplified report, you must ensure the following are correctly substituted (template variables must not remain):

| Check item | Incorrect example | Correct example |
|:-------|:---------|:---------|
| Method name | `${method}` | `getRegionWanderSearchCount` |
| Route path | `/api/${method}` | `/itc/ws/carQuery` → `getRegionWanderSearchCount` |
| Service implementation class | `${ServiceImpl}` | `CarQueryServiceImpl` |
| SOAP method tag | `<web:${method}>` | `<web:getRegionWanderSearchCount>` |
| Call-chain method | `${ServiceImpl}.${method}()` | `CarQueryServiceImpl.getRegionWanderSearchCount()` |

**File content verification:**

After generating each file, you must check:
1. The **file name** contains the project prefix (e.g. `myproject_trace_`)
2. The **file content** contains no unsubstituted variables in the form `${...}`
3. The **method name** is correctly displayed in the report title, packet, and call chain

### 2.5 Required content of the simplified version (mandatory)

| Must include | Description | Cannot omit |
|:---------|:-----|:---------|
| HTTP/SOAP request template | Placeholder format `{{param}}`, used to show the structure | ✅ |
| **Test packet example** | **Complete packet with actual test values, directly usable for Burp testing** | ✅ |
| **Parameter definition table specific to this method** | Read from the method's code signature; do not assume | ✅ |
| Call-chain layer diagram | [L1] → [L2] → [Sink] format | ✅ |
| **Sink identification** | Identify the final usage point type of this method | ✅ |
| **Controllability conclusion** | Controllability determination for this method's parameters | ✅ |

### 2.5.1 Test packet generation rules (mandatory)

**Test packets must contain actual testable values; placeholders are forbidden:**

| Java type | Placeholder (forbidden) | Actual value generation rule |
|:---------|:---------------|:---------------|
| String (ID type) | `{{userId}}` | Numeric string such as `1001` |
| String (name type) | `{{name}}` | Meaningful test value such as `testUser` |
| String (date type) | `{{date}}` | Standard format such as `2026-01-01` |
| String (path type) | `{{path}}` | Legal path such as `/tmp/test.txt` |
| String (URL type) | `{{url}}` | Full URL such as `http://example.com/api` |
| int/Integer | `{{count}}` | Number such as `10` |
| boolean/Boolean | `{{flag}}` | `true` or `false` |
| JSON string | `{{xxxJson}}` | Full JSON such as `{"id":"1","name":"test"}` |

**How to generate test values:**

1. **Extract from code** - look for values in code comments, unit tests, or sample data
2. **Infer from field semantics** - generate reasonable values from the field name's meaning (e.g. `email` → `test@example.com`)
3. **Infer from type** - use descriptive text for String and reasonable range values for numbers
4. **Use common safe test values** - avoid special characters and ensure the request can be sent normally

### 2.6 Independent method-parameter check rules (mandatory)

**When tracing each method, you must perform the following steps; skipping is forbidden:**

#### Step 1: Read the method's actual code signature

You must read the actual code to obtain the real parameters; assumptions are forbidden:

```
Method A: getDictionaryAll(String codeTypes)           → 1 parameter
Method B: getCommonQuery(String searchJson, ...)       → 3 parameters
Method C: executeCommand(String cmd, String args)      → 2 parameters
```

#### Step 2: Independently trace the method's call chain to the sink

Different methods may have different sink types:

| Example method | Call chain | Sink type |
|:---------|:-------|:----------|
| getCommonQuery | → DAO → SQL execution | SQL |
| executeTask | → Runtime.exec() | COMMAND |
| fetchUrl | → HttpClient.get() | HTTP |
| parseXml | → DocumentBuilder.parse() | XML |
| getDictionaryAll | → Map.get() | No sensitive sink |

#### Step 3: Determine the controllability of the method's parameters

Determine based on the sink type actually traced for this method:

| Sink type | Determination criteria |
|:----------|:---------|
| SQL | Whether the parameter is concatenated into SQL |
| COMMAND | Whether the parameter is passed to command execution |
| HTTP | Whether the parameter is used to construct a URL |
| FILE | Whether the parameter is used for a file path |
| XML | Whether the parameter is passed to an XML parser |
| No sensitive sink | Mark as "no sensitive operation" |

#### Step 4: Output the independent determination result for this method

**Forbidden behavior:**
- ❌ Do not write "refer to the parameter definitions of the 1st interface"
- ❌ Do not reuse the controllability conclusions of other methods
- ❌ Do not assume all methods have the same parameters or sink types

### 2.7 Pre-generation checklist for the simplified version (must be executed for each method)

| # | Check item | Mandatory |
|:--|:-------|:---------|
| 1 | Read the method's code signature and obtain the actual parameter list | ☐ |
| 2 | Trace the method's call chain to the final usage point | ☐ |
| 3 | Identify the method's sink type (SQL/COMMAND/HTTP/FILE/XML/none) | ☐ |
| 4 | Determine the controllability of the method's parameters | ☐ |
| 5 | Output the controllability determination table for this method | ☐ |

### 3. Trace the call chain

Starting from the entry method, trace layer by layer:

```
Controller/Action layer
    ↓ calls
Service/Manager layer
    ↓ calls
DAO/Repository layer
    ↓ executes
SQL/database operations
```

**Tracing rules:**

1. **Identify method calls** - check `this.xxx()` calls in the method body or method calls on injected objects
2. **Follow dependency injection** - identify objects injected via `@Autowired`, `@Resource`, or constructor injection
3. **Trace parent-class methods** - if `super.xxx()` or an inherited method is called, trace to the parent class
4. **Record parameter passing** - record how parameters are passed from upper to lower layers

### 4. Decompilation support

When source code is unavailable, decompile with java-decompile-mcp:

```python
# Decompile a single file
mcp__java-decompile-mcp__decompile_file(
    file_path="/path/to/SomeClass.class",
    output_dir="/path/to/output",
    save_to_file=True
)

# Decompile a directory
mcp__java-decompile-mcp__decompile_directory(
    directory_path="/path/to/classes",
    output_dir="/path/to/output",
    recursive=True,
    save_to_file=True,
    max_workers=4
)

# Batch decompile
mcp__java-decompile-mcp__decompile_files(
    file_paths=["/path/to/A.class", "/path/to/B.class"],
    output_dir="/path/to/output",
    save_to_file=True
)
```

---

## Output Format

**Strictly follow the fill-in templates in the references/ directory to generate output files.**

| Scenario | Template | File naming |
|------|------|---------|
| 1st interface (full version) | [OUTPUT_TEMPLATE_FULL.md](references/OUTPUT_TEMPLATE_FULL.md) | `{project_name}_trace_{method_name}_{YYYYMMDD_HHMMSS}.md` |
| 2nd+ interfaces (simplified version) | [OUTPUT_TEMPLATE_SIMPLE.md](references/OUTPUT_TEMPLATE_SIMPLE.md) | `{project_name}_trace_{method_name}_{YYYYMMDD_HHMMSS}.md` |
| Multi-method index | [OUTPUT_TEMPLATE_INDEX.md](references/OUTPUT_TEMPLATE_INDEX.md) | `{project_name}_trace_all_methods_{YYYYMMDD_HHMMSS}.md` |

**Key Rules:**
- All [FILL IN] placeholders must be replaced with actual content
- Each method must be traced independently to the sink; reusing conclusions from other methods is forbidden
- Multi-method routes must generate an index file
- Common specification reference: [shared/OUTPUT_STANDARD.md](../shared/OUTPUT_STANDARD.md)

### Single-method route

**File naming:** `{project-name}_audit/route_tracer/{route-name}/{project-name}_trace_{route-id}_{timestamp}.md`

**Directory structure:**
```
{project_name}_audit/
└── route_tracer/
    └── {route_name}/
        └── {project_name}_trace_{route_id}_20260204.md
```

### Multi-interface method routes (important)

**When the entry class contains multiple business methods (e.g., a Web Service or a Controller with multiple endpoints), you must generate a separate trace report file for each method.**

**File naming rules:**
- Single method report: `{project-name}_trace_{method-name}_{timestamp}.md`
- Overall index report: `{project-name}_trace_all_methods_{timestamp}.md`

**Directory structure:**
```
{project_name}_audit/
└── route_tracer/
    └── {route_name}/
        ├── {project_name}_trace_getBasicQuery_20260204.md        # method 1
        ├── {project_name}_trace_getAdvancedQuery_20260204.md     # method 2
        ├── {project_name}_trace_getDetailQuery_20260204.md       # method 3
        ├── {project_name}_trace_getImageQuery_20260204.md        # method N
        ├── ... (one separate file per method)
        └── {project_name}_trace_all_methods_20260204.md           # overall index
```

**Route Name Notes:**
- Route names are extracted from the route path, stripping leading slashes and special characters
- For example: `/itc/ws/carQuery` → `itc_ws_carQuery`
- For example: `/api/user/login.action` → `api_user_login`

**Execution flow:**
```
Scanning entry class: VehicleQueryServiceImpl

✅ Found 10 entry methods

--- Method 1/10: getBasicQuery ---
[Generate separate report: myproject_trace_getBasicQuery_20260204.md]

--- Method 2/10: getAdvancedQuery ---
[Generate separate report: myproject_trace_getAdvancedQuery_20260204.md]

...

✅ All 10 methods traced
✅ Generated overall index: myproject_trace_all_methods_20260204.md
```

**Overall index report content:**
```markdown
# /api/ws/vehicleQuery Web Service All-Method Tracing Index

Generated: 2026-02-04
Entry class: VehicleQueryServiceImpl
Total methods: 10

## Method list

| # | Method name | Parameter list | Detailed report |
|:--|:-------|:---------|:---------|
| 1 | getBasicQuery | searchJson, pageJson, extend | [View](myproject_trace_getBasicQuery_20260204.md) |
| 2 | getAdvancedQuery | searchJson, pageJson, extend | [View](myproject_trace_getAdvancedQuery_20260204.md) |
| 3 | getDetailQuery | searchJson, pageJson, extend | [View](myproject_trace_getDetailQuery_20260204.md) |
| ... | ... | ... | ... |
```

For the detailed implementation strategy, see: [multi-method-tracing.md](references/multi-method-tracing.md)

### Output templates

#### Full trace chain (for the 1st interface)

A complete call-chain trace report containing all layers, branches, variable tracing, and so on.

````markdown
# Route Call-Chain Trace Report

**Traced route**: `/admin/image/getImageCapture.action`
**Generated**: 2026-02-04
**Project path**: /path/to/project

---

## 1. HTTP request packet

### 1.1 Complete request template

```http
POST /admin/image/getImageCapture.action HTTP/1.1
Host: {{host}}
Content-Type: application/x-www-form-urlencoded
Cookie: JSESSIONID={{session}}

searchJson={{searchJson}}&pageJson={{pageJson}}&extend={{extend}}
```

### 1.2 Detailed parameter definitions

#### Top-level parameters

| Parameter name | Java type | HTTP location | Required | Description |
|:-------|:---------|:---------|:-----|:-----|
| searchJson | String | Body | Yes | JSON format, deserialized into ImageCaptureBean |
| pageJson | String | Body | Yes | JSON format, deserialized into Page<ImageCapture> |
| extend | String | Body | No | Extended parameters |

#### Internal structure of pageJson (Page<ImageCapture>)

| Field name | Java type | Description | Final usage location |
|:-------|:---------|:-----|:-------------|
| orderBy | String | Sort field | **AbstractDao.findSql():234 - SQL concatenation** |
| order | String | Sort direction (asc/desc) | **AbstractDao.findSql():234 - SQL concatenation** |
| pageSize | int | Records per page | Paginated query |
| currentPage | int | Current page number | Paginated query |

#### Internal structure of searchJson (ImageCaptureBean)

| Field name | Java type | Description |
|:-------|:---------|:-----|
| userBean | UserBean | User information object |
| startTime | String | Start time |
| endTime | String | End time |
| deviceIds | List<String> | Device ID list |

### 1.3 Test packet example

```http
POST /admin/image/getImageCapture.action HTTP/1.1
Host: 192.168.1.100:8080
Content-Type: application/x-www-form-urlencoded
Cookie: JSESSIONID=ABC123

searchJson={"userBean":{"loginName":"admin"},"startTime":"2026-01-01","endTime":"2026-02-01"}&pageJson={"orderBy":"id","order":"desc","pageSize":10,"currentPage":1}&extend=
```

---

## 2. Layer-by-layer call-chain tracing

### [Level 1] Action entry layer

**File**: `com/example/web/action/ImageCaptureAction.java:125`
**Class**: `ImageCaptureAction`
**Method signature**:
```java
public String getImageCapture(String searchJson, String pageJson, String extend)
```

**Full code:**
```java
public String getImageCapture(String searchJson, String pageJson, String extend) {
    // Deserialize pageJson into a Page object
    Page<ImageCapture> page = (Page)JsonUtils.fromJson(pageJson, (new TypeToken<Page<ImageCapture>>() {
    }).getType(), (String)null);

    this.defaultImageCaptureSearchOrder(page);

    // Deserialize searchJson into an ImageCaptureBean object
    ImageCaptureBean searchBean = (ImageCaptureBean)JsonUtils.fromJson(searchJson, ImageCaptureBean.class, (String)null);

    if (searchBean.getUserBean() != null && StringUtil.isEmpty(searchBean.getUserBean().getHostLoginIp())) {
        String addressIp = WebServiceUtil.getWebServiceIp();
        if (StringUtil.isEmpty(addressIp)) {
            addressIp = searchBean.getUserBean().getLoginServerName();
        }
        searchBean.getUserBean().setHostLoginIp(addressIp);
    }

    searchBean.setSecordExcute(false);
    String json = WebServiceUtil.valiatePam((new TypeToken<ReturnMsgBean<ImageCapture>>() {
    }).getType(), new Object[]{page, searchBean});

    if (json == null) {
        // Key call: pass searchBean, page, extend to the Manager layer
        json = this.imageCaptureManager.getImageCaptureJson(searchBean, page, extend);
    }

    return json;
}
```

**Parameter conversion:**

| HTTP parameter | Converted type | Converted variable name | Passed to next layer |
|:---------|:-----------|:-------------|:-------------|
| pageJson (String) | Page<ImageCapture> | page | ✅ |
| searchJson (String) | ImageCaptureBean | searchBean | ✅ |
| extend (String) | String | extend | ✅ |

**Key fields of the Page object:**
- `page.orderBy` ← pageJson.orderBy (String type)
- `page.order` ← pageJson.order (String type)

**Next-layer call**: `this.imageCaptureManager.getImageCaptureJson(searchBean, page, extend)`

---

### [Level 2] Manager service layer

**File**: `com/example/service/ImageCaptureManager.java:89`
**Class**: `ImageCaptureManager`
**Method signature**:
```java
public String getImageCaptureJson(ImageCaptureBean searchBean, Page<ImageCapture> page, String extend)
```

**Full code:**
```java
public String getImageCaptureJson(ImageCaptureBean searchBean, Page<ImageCapture> page, String extend) {
    // Key call: pass page to the DAO layer
    Page<ImageCapture> result = this.imageCaptureDao.getImageCapturePage(searchBean, page);
    return JsonUtils.toJson(result);
}
```

**Parameter passing:**

| Received parameter | Type | Passed to next layer |
|:---------|:-----|:-------------|
| searchBean | ImageCaptureBean | ✅ |
| page | Page<ImageCapture> | ✅ (includes orderBy, order) |
| extend | String | ❌ (not passed) |

**Next-layer call**: `this.imageCaptureDao.getImageCapturePage(searchBean, page)`

---

### [Level 3] DAO data-access layer

**File**: `com/example/dao/ImageCaptureDao.java:56`
**Class**: `ImageCaptureDao`
**Parent class**: `AbstractDao<ImageCapture>`
**Method signature**:
```java
public Page<ImageCapture> getImageCapturePage(ImageCaptureBean searchBean, Page<ImageCapture> page)
```

**Full code:**
```java
public Page<ImageCapture> getImageCapturePage(ImageCaptureBean searchBean, Page<ImageCapture> page) {
    String sql = buildQuerySql(searchBean);
    // Key call: call the parent class AbstractDao.findSql(), passing the page object
    return super.findSql(sql, page);
}
```

**Parameter passing:**

| Received parameter | Type | Passed to next layer |
|:---------|:-----|:-------------|
| searchBean | ImageCaptureBean | ❌ (used to build SQL) |
| page | Page<ImageCapture> | ✅ (passed to parent class) |

**Next-layer call**: `super.findSql(sql, page)` → parent class `AbstractDao.findSql()`

---

### [Level 4] Parent base layer (final usage point)

**File**: `com/example/dao/base/AbstractDao.java:234`
**Class**: `AbstractDao<T>`
**Method signature**:
```java
protected Page<T> findSql(String sql, Page<T> page)
```

**Full code:**
```java
protected Page<T> findSql(String sql, Page<T> page) {
    if (page.getOrderBy() != null) {
        // ⚠️ Final usage point: orderBy and order are concatenated directly into the SQL statement
        sql = sql + " ORDER BY " + page.getOrderBy() + " " + page.getOrder();
    }
    // Execute the SQL query
    return executeQuery(sql, page);
}
```

**Final parameter usage:**

| Parameter | Type | Usage | Code location |
|:-----|:-----|:---------|:---------|
| page.getOrderBy() | String | **Concatenated directly into SQL** | AbstractDao.java:235 |
| page.getOrder() | String | **Concatenated directly into SQL** | AbstractDao.java:235 |

---

## 3. Call-chain summary diagram

```
HTTP Request
│
├─ searchJson (String) ──→ ImageCaptureBean searchBean
│                              └─ userBean: UserBean
│                              └─ startTime: String
│                              └─ endTime: String
│
├─ pageJson (String) ────→ Page<ImageCapture> page
│                              ├─ orderBy: String ─────────────────────┐
│                              ├─ order: String ───────────────────────┤
│                              ├─ pageSize: int                        │
│                              └─ currentPage: int                     │
│                                                                      │
└─ extend (String) ──────→ (not passed downward)                       │
                                                                       │
┌──────────────────────────────────────────────────────────────────────┘
│
▼ Parameter flow tracing

[L1] ImageCaptureAction.getImageCapture()
      │
      │  page (includes orderBy, order), searchBean
      ▼
[L2] ImageCaptureManager.getImageCaptureJson()
      │
      │  page (includes orderBy, order), searchBean
      ▼
[L3] ImageCaptureDao.getImageCapturePage()
      │
      │  page (includes orderBy, order)
      ▼
[L4] AbstractDao.findSql()
      │
      └──→ sql = sql + " ORDER BY " + page.getOrderBy() + " " + page.getOrder()
           ▲                              ▲
           │                              │
           └── orderBy concatenated directly ───┴── order concatenated directly
```

---

## 4. Parameter variable-name tracing table (core)

**Trace how the same parameter's variable name changes across classes:**

### 4.1 pageJson.orderBy parameter tracing

| Layer | Class | Variable name | Type | Code location | Notes |
|:-----|:-----|:-------|:-----|:---------|:-----|
| HTTP | - | `pageJson` | String | Request body | Original JSON string |
| L1 | ImageCaptureAction | `pageJson` → `page.orderBy` | Page.orderBy: String | :125 | JsonUtils.fromJson() deserialization |
| L2 | ImageCaptureManager | `page.orderBy` | Page.orderBy: String | :89 | Name unchanged, passed directly |
| L3 | ImageCaptureDao | `page.orderBy` | Page.orderBy: String | :56 | Name unchanged, passed to parent class |
| L4 | AbstractDao | `page.getOrderBy()` | String | :235 | **Final usage: SQL concatenation** |

### 4.2 pageJson.order parameter tracing

| Layer | Class | Variable name | Type | Code location | Notes |
|:-----|:-----|:-------|:-----|:---------|:-----|
| HTTP | - | `pageJson` | String | Request body | Original JSON string |
| L1 | ImageCaptureAction | `pageJson` → `page.order` | Page.order: String | :125 | JsonUtils.fromJson() deserialization |
| L2 | ImageCaptureManager | `page.order` | Page.order: String | :89 | Name unchanged |
| L3 | ImageCaptureDao | `page.order` | Page.order: String | :56 | Name unchanged |
| L4 | AbstractDao | `page.getOrder()` | String | :235 | **Final usage: SQL concatenation** |

### 4.3 searchJson parameter tracing

| Layer | Class | Variable name | Type | Code location | Notes |
|:-----|:-----|:-------|:-----|:---------|:-----|
| HTTP | - | `searchJson` | String | Request body | Original JSON string |
| L1 | ImageCaptureAction | `searchJson` → `searchBean` | ImageCaptureBean | :128 | JsonUtils.fromJson() deserialization |
| L2 | ImageCaptureManager | `searchBean` | ImageCaptureBean | :89 | Name unchanged |
| L3 | ImageCaptureDao | `searchBean` | ImageCaptureBean | :56 | **Final usage: buildQuerySql()** |

### 4.4 Variable-name change example (when the parameter name changes across layers)

```
HTTP: pageJson (String)
       ↓ JsonUtils.fromJson()
L1 ImageCaptureAction: page (Page<ImageCapture>)
       ↓ method parameter passing
L2 ImageCaptureManager: page (Page<ImageCapture>)  ← same name
       ↓ method parameter passing
L3 ImageCaptureDao: page (Page<ImageCapture>)  ← same name
       ↓ super.findSql(sql, page)
L4 AbstractDao: page (Page<T>)  ← generic type change
       ↓ page.getOrderBy()
Final usage: sql = sql + " ORDER BY " + page.getOrderBy()
```

### 4.5 Complete parameter tracing summary

| Original HTTP parameter | L1 variable name | L2 variable name | L3 variable name | L4 variable name | Final usage |
|:-------------|:---------|:---------|:---------|:---------|:---------|
| pageJson | page | page | page | page | page.getOrderBy() → SQL concatenation |
| pageJson.orderBy | page.orderBy | page.orderBy | page.orderBy | page.getOrderBy() | SQL ORDER BY clause |
| pageJson.order | page.order | page.order | page.order | page.getOrder() | SQL ORDER BY clause |
| searchJson | searchBean | searchBean | searchBean | - | buildQuerySql() |
| extend | extend | - | - | - | Not passed downward |
````

---

## 5. Actual parameter usage check (CRITICAL - prevent false positives)

**Trace each parameter from the HTTP entry point to the final usage point, and determine whether the parameter truly participates in a sensitive operation.**

**This check is essential for accurate vulnerability determination and prevents "parameter passed but unused" cases from being misjudged as vulnerabilities.**

### 5.1 Check description

| Status | Meaning | Effect on vulnerability determination |
|:-----|:-----|:-----------------|
| ✅ Used | The parameter value directly or indirectly participates in a sensitive operation | Must further check whether a vulnerability exists |
| ❌ Not used | The parameter is passed but does not participate in a sensitive operation (overwritten by hardcoding / ignored) | **Rule out the vulnerability** |
| ⚠️ Partially used | Some fields of the parameter are used, others are not | Check only the used fields |

### 5.2 "Hardcoded override" scenarios for each vulnerability type

| Vulnerability type | Parameter | Hardcoded override scenario | Conclusion |
|:---------|:-----|:---------------|:-----|
| **SQL injection** | `page.orderBy` | SQL already hardcodes `order by createTime desc` | Parameter not used |
| **Command injection** | `cmd` | Code hardcodes `Runtime.exec("ls -la")` | Parameter not used |
| **SSRF** | `url` | Code hardcodes `httpClient.get("http://internal/api")` | Parameter not used |
| **File operations** | `path` | Code hardcodes `new File("/tmp/fixed.txt")` | Parameter not used |
| **XXE** | `xml` | Code uses a fixed XML template | Parameter not used |
| **Expression injection** | `expr` | Code hardcodes the expression `SpEL.parse("#{fixed}")` | Parameter not used |

### 5.3 Parameter usage checklist (output template)

```markdown
## Actual Parameter Usage Check

| Parameter | Sink type | Override type | Override condition | Controllability conclusion | Controllable scenario |
|:-----|:---------|:---------|:---------|:-----------|:---------|
| page.orderBy | SQL ORDER BY | Conditional override | `isEmpty(orderBy)` | ⚠️ Conditionally controllable | Controllable when non-empty |
| page.order | SQL ORDER BY | No override | - | ✅ Fully controllable | Any value |
| cmd | Runtime.exec | No override | - | ✅ Fully controllable | Any value |
| url | HTTP request | Security-check override | `!isInternalUrl(url)` | ⚠️ Conditionally controllable | Controllable for external URLs |
| path | File operation | Whitelist override | `!allowedPaths.contains()` | ⚠️ Controllable within the whitelist | e.g. /tmp, /data |
| searchBean.keyword | SQL WHERE | Unconditional override | Always overridden | ❌ Not controllable | None |
```

**Controllability conclusion description:**

| Conclusion | Meaning | Audit requirement |
|:-----|:-----|:---------|
| ✅ Fully controllable | The parameter has no override and user input reaches the sink directly | Must audit the security of the sink |
| ⚠️ Conditionally controllable | The parameter is controllable under specific conditions | Verify the bypass conditions before auditing |
| ❌ Not controllable | The parameter is unconditionally overridden or safely handled | The vulnerability for this parameter can be ruled out |

### 5.4 General override-condition identification rules (applicable to all vulnerability types)

**After tracing a parameter assignment operation, you must check the override condition; this rule applies to any type of parameter:**

| Override type | Code pattern | Controllability determination | Applicable scenario |
|:---------|:---------|:-----------|:---------|
| **Unconditional override** | `x = "hardcoded";` (not inside an if) | ❌ Not controllable | All vulnerability types |
| **Empty-value guard override** | `if (isEmpty(x)) { x = default; }` | ⚠️ Controllable when non-empty | All vulnerability types |
| **Null guard override** | `if (x == null) { x = default; }` | ⚠️ Controllable when non-null | All vulnerability types |
| **Whitelist override** | `if (!list.contains(x)) { x = default; }` | ⚠️ Controllable within the whitelist | All vulnerability types |
| **Security-check override** | `if (!isAllowed(x)) { x = safe; }` | ⚠️ Controllable when the check is bypassed | SSRF/file/command |
| **Format-validation override** | `if (!isValid(x)) { x = default; }` | ⚠️ Controllable when the format is met | All vulnerability types |
| **Conditional-branch override** | `if (cond) { x = default; }` | ⚠️ Controllable when the condition is not met | All vulnerability types |

**Common override-condition identification (general):**

| Condition type | Identification pattern | Controllable scenario |
|:---------|:---------|:---------|
| **Empty-value check** | `isEmpty()`, `isBlank()`, `== null`, `length() == 0` | Controllable when non-empty |
| **Whitelist check** | `contains()`, `Arrays.asList()`, `allowedList.contains()` | Controllable within the whitelist |
| **Blacklist check** | `!contains()`, `blacklist.contains()` → reject | Controllable when not in the blacklist |
| **Format validation** | `matches()`, `Pattern.compile()`, `isValid()` | Controllable when the format is met |
| **Security check** | `isAllowed()`, `isSafe()`, `checkSecurity()` | Controllable when the check is bypassed |
| **Range check** | `x > min && x < max`, `inRange()` | Controllable within the range |

**Existing hardcoded-override detection rules (still applicable):**

| Sensitive operation type | Hardcoded-override detection method | Example |
|:-------------|:-------------------|:-----|
| SQL ORDER BY | Check whether the SQL string already contains `order by` | `sql + " order by id desc"` |
| SQL WHERE | Check whether the condition uses parameterized `#{}` or a hardcoded value | `WHERE status = 1` |
| Command execution | Check whether the command string uses a hardcoded command | `exec("ls -la")` |
| HTTP request | Check whether the URL uses a hardcoded address | `get("http://fixed.com")` |
| File operations | Check whether the path uses a hardcoded path | `new File("/tmp/log.txt")` |
| XML parsing | Check whether the XML comes from a fixed template | `parse(FIXED_XML)` |

### 5.5 Output format for hardcoded override details

**When a parameter is found to be hardcoded-overridden, you must output the details:**

```
### Hardcoded Override Details

#### {param-name} - hardcoded override

**Code location**: `{ClassName}.java:{line}`

**Override code**: {code snippet showing the hardcoded override}

**Determination**:
- {param} is passed to {method}
- but {sensitive operation} already contains a hardcoded value
- **Conclusion**: ❌ The parameter is unused; no vulnerability exists
```

### 5.6 Actual parameter usage checklist

**Before outputting the trace report, you must complete the following checks:**

| # | Check item | Status |
|:--|:-------|:-----|
| 1 | Identify all parameters passed to the final layer | ☐ |
| 2 | Determine the sensitive operation type for each parameter | ☐ |
| 3 | Check whether a hardcoded override exists | ☐ |
| 4 | Annotate the actual usage status of each parameter | ☐ |
| 5 | Output details for parameters that are "hardcoded-overridden" | ☐ |
| 6 | **Check the semantics of override conditions and output the controllability conclusion** | ☐ |

---

## 6. Parameter controllability determination (CRITICAL - general basis for vulnerability determination)

**Applicable to all vulnerability types: SQL injection, command injection, SSRF, file operations, XXE, expression injection, etc.**

**For detailed determination principles, see: [CONTROLLABILITY_ANALYSIS.md](references/CONTROLLABILITY_ANALYSIS.md)**

### 6.1 Core determination flow

```
1. Trace the parameter's complete path from the HTTP entry point to the sink
2. Identify all assignment/override operations on the parameter along the path
3. Check the condition semantics of the override operations (identify code intent, not pattern matching)
4. Output the controllability conclusion
```

### 6.2 Override types and controllability

| Override type | Determination criteria | Controllability conclusion |
|:---------|:---------|:-----------|
| **No override** | The parameter is passed directly to the sink | ✅ Fully controllable |
| **Unconditional override** | The assignment is not inside any condition | ❌ Not controllable |
| **Conditional override** | The assignment is inside a condition; semantics must be determined | ⚠️ Conditionally controllable |

### 6.3 Condition semantics determination (key)

**Identify from code semantics, not by matching fixed method names:**

| Semantic type | Determination method | Controllable scenario |
|:---------|:---------|:---------|
| Empty-value guard | The condition checks whether the parameter is empty and sets a default when it is | Controllable when non-empty |
| Whitelist validation | The condition checks whether the parameter is in the allowlist | Controllable within the whitelist |
| Security check | The condition checks whether the parameter is safe | Controllable when the check is bypassed |

### 6.4 Output format

**You must output the controllability determination table:**

```markdown
| Parameter | Sink type | Override type | Override condition | Controllability conclusion | Controllable scenario |
|:-----|:---------|:---------|:---------|:-----------|:---------|
| {name} | {sink} | {type} | {condition} | {✅/⚠️/❌} | {scenario} |
```

**You must output the controllability summary:**

```markdown
| Controllability type | Parameter list | Audit requirement |
|:-----------|:---------|:---------|
| ✅ Fully controllable | {list} | Must audit sink security |
| ⚠️ Conditionally controllable | {list} | Must verify the bypass conditions |
| ❌ Not controllable | {list} | The possibility of a vulnerability can be ruled out |
```

### 6.5 Sink types

| Sink | Description |
|:-----|:-----|
| SQL | SQL concatenation/execution |
| COMMAND | System command execution |
| HTTP | HTTP request initiation |
| FILE | File read/write operations |
| XML | XML parsing |
| LDAP | LDAP query |
| EXPRESSION | Expression parsing |
| DESERIALIZE | Deserialization |
| RESPONSE | Response output |
| PATH | Path concatenation |

---

## 7. Branch-condition tracing (CRITICAL - avoid false positives)

**When tracing the call chain, you must record all conditional branches to ensure you identify whether the code will actually execute!**

**For detailed determination principles, see: [BRANCH_TRACING.md](references/BRANCH_TRACING.md)**

### 7.1 Core determination flow

```
1. Identify conditional branches in the code (if/else/switch)
2. Check the execution content of each branch
3. Determine in which branches the sensitive operation executes
4. Output the execution-path conclusion
```

### 7.2 Branch types that must be identified

**Identify from code semantics, not by matching fixed method names:**

| Branch type | Semantic feature | Tracing focus |
|:---------|:---------|:---------|
| Environment/platform branch | Selects different paths based on the runtime environment | Annotate what executes in each environment |
| Security-check branch | Performs security validation on input | Annotate the blocking conditions |
| Feature-flag branch | Decides whether to execute based on configuration | Annotate the effect of the flag state |
| Empty-value/exception branch | Checks parameter validity | Annotate the early-exit conditions |
| Permission-check branch | Checks user permissions | Annotate the permission requirements |

### 7.3 Early-exit point identification

| Exit type | Semantics | Must annotate |
|:---------|:-----|:---------|
| Security-block exit | Security check fails; refuse to continue | ⚠️ Security block |
| Empty-value guard exit | Parameter invalid; return early | ⚠️ Early exit |
| Exception-throw exit | Condition not met; throw an exception | ⚠️ Exception exit |

### 7.4 Output format

**You must output the branch structure:**

```markdown
methodName(param)
    ├─ [if condition A] → content executed in branch A
    │      └─→ sensitive operation ⚠️
    └─ [else] → default branch / return / throw
```

**You must output the execution-path conclusion:**

```markdown
| Path | Condition | Sensitive operation | Exploitability |
|:-----|:-----|:---------|:---------|
| Path A | {condition} | ✅ Executes | Exploitable |
| Path B | {condition} | ❌ Does not execute | Not exploitable |
```

---

## Tracing strategies

### Strategy 1: Dependency injection tracing

Identify Spring/Struts dependency injection:

```java
// Spring
@Autowired
private ImageCaptureManager imageCaptureManager;

// Struts
private ImageCaptureService faceCaptureService;
public void setImageCaptureService(ImageCaptureService service) {
    this.faceCaptureService = service;
}
```

When tracing the `imageCaptureManager.xxx()` call, locate the `ImageCaptureManager` class.

### Strategy 2: Inheritance-chain tracing

When `super.xxx()` or a parent-class method is called:

```java
public class ImageCaptureDao extends AbstractDao<ImageCapture> {
    public Page<ImageCapture> query(Page<ImageCapture> page) {
        return super.findSql(sql, page);  // trace to AbstractDao
    }
}
```

Tracing steps:
1. Identify `extends AbstractDao`
2. Find the `findSql` method in the parent class
3. Continue tracing the parent's parent (if any)

### Strategy 3: Interface implementation tracing

When an interface method is called:

```java
@Autowired
private UserService userService;  // interface type

userService.getUser(id);  // need to find the implementation class
```

Tracing steps:
1. Identify that `UserService` is an interface
2. Find the class that `implements UserService`
3. Locate the method in the implementation class

### Strategy 4: MyBatis/Hibernate tracing

For ORM frameworks:

**MyBatis:**
```java
@Mapper
public interface UserMapper {
    List<User> selectByPage(@Param("page") Page page);
}
```
Trace to the SQL definition in the corresponding XML file.

**Hibernate:**
```java
session.createQuery("FROM User WHERE id = " + id);
```
Identify the HQL/SQL directly in the code.

---

## Decompilation tool usage

### When to decompile

| Scenario | Action |
|:-----|:-----|
| .java source exists | Read and inspect directly |
| Only .class files exist | Use decompile_file |
| The whole project has only .class files | Use decompile_directory |
| Parent class is inside a JAR | Extract the JAR first, then use decompile_file |

### Decompilation command reference

```python
# Check CFR status
mcp__java-decompile-mcp__check_cfr_status()

# Check the Java version
mcp__java-decompile-mcp__get_java_version()

# If CFR is missing, download it
mcp__java-decompile-mcp__download_cfr_tool(target_dir="/path/to/tools")

# Decompile a single class
mcp__java-decompile-mcp__decompile_file(
    file_path="/path/to/AbstractDao.class",
    save_to_file=True
)

# Decompile the entire DAO package
mcp__java-decompile-mcp__decompile_directory(
    directory_path="/path/to/com/example/dao",
    recursive=True,
    save_to_file=True
)
```

---

## Output specification

### Required information

Each layer must include:

1. **File location** - full package path + file name + line number
2. **Class name** - including parent-class information (if any)
3. **Method signature** - method name + parameter list + return type
4. **Key code** - the code snippet that calls the next layer
5. **Parameter passing** - explain how parameters are passed to the next layer

### Forbidden operations

- ❌ Do not perform vulnerability detection or vulnerability determination
- ❌ Do not provide remediation plans
- ❌ Do not infer call relationships that do not exist
- ❌ Do not omit any layer

### Output file naming

```
{project_name}_audit/route_tracer/{route_name}/{project_name}_trace_{route_id}_{timestamp}.md

Example:
myproject_audit/route_tracer/itc_ws_carQuery/myproject_trace_getImageCapture_20260204.md
```

#### Simple trace chain (for the 2nd and later interfaces)

**Must include the following: request template + parameter definitions for this method + call chain + sink identification + controllability determination**

```markdown
# Route Call-Chain Trace Report (Simplified)

**Traced route**: `{route}`
**Method**: `{method}`
**Generated**: {date}

---

## 1. HTTP request packet

### 1.1 Complete request template
```http
{complete request template for this method}
```

### 1.2 Parameter definitions for this method

**Parameter source**: read from the `{ClassName}.{method}()` method signature

#### Top-level parameters
| Parameter name | Java type | Description |
|:-------|:---------|:-----|
| {param} | {type} | {desc} |

#### Internal parameter structure (if any)
| Field name | Java type | Description |
|:-------|:---------|:-----|
| {field} | {type} | {desc} |

### 1.3 Test packet example
```http
{test packet}
```

---

## 2. Call-chain tracing

### Call-chain layers
```
[L1] {Class}.{method}()
    ↓
[L2] {Class}.{method}()
    ↓
[Sink] {sink type}: {specific location}
```

### Sink identification

| Sink type | Location | Description |
|:----------|:-----|:-----|
| {SQL/COMMAND/HTTP/FILE/XML/no sensitive sink} | {Class.java:line} | {specific operation} |

### Parameter passing relationships
| Parameter | L1 | L2 | ... | Final usage |
|:-----|:---|:---|:----|:---------|
| {param} | {var} | {var} | ... | {usage} |

---

## 3. Controllability determination

| Parameter | Sink type | Override type | Override condition | Controllability conclusion | Controllable scenario |
|:-----|:---------|:---------|:---------|:-----------|:---------|
| {param} | {sink} | {type} | {condition} | {✅/⚠️/❌/-} | {scenario} |

**Controllability summary**:
| Type | Parameter | Audit requirement |
|:-----|:-----|:---------|
| ✅ Fully controllable | {list} | Must audit sink security |
| ⚠️ Conditionally controllable | {list} | Must verify the bypass conditions |
| ❌ Not controllable | {list} | The possibility of a vulnerability can be ruled out |
| - No sensitive sink | {list} | Low risk |
```

**Notes for generating the simplified version:**
- Read parameters from the method's actual code; assumptions are forbidden
- Independently trace the method's call chain to the sink
- Identify the method's sink type (it may differ from the 1st interface)
- Output the controllability determination for this method (reusing conclusions from other methods is forbidden)
- If the method has no sensitive sink, mark it as "no sensitive sink, low risk" in the controllability determination

---

## Limits and boundaries

**Only the following operations are performed:**
- Trace the call chain of the specified route
- Output the file location and method signature of each layer
- Record parameter passing relationships
- Generate HTTP request templates

**The following operations are not performed:**
- No security vulnerability detection
- No remediation plans provided
- No vulnerability severity determination
- No business-logic correctness checks