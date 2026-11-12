---
name: java-route-mapper
description: "Java Web source-code route and parameter mapping tool. Extract **all** HTTP routes and request parameters from the source code, generate complete Burp Suite request templates, and automatically save them as MD documents. Applicable to: (1) complete interface inventory for projects without API documentation, (2) generating Burp test requests for all interfaces, (3) complete source-code endpoint analysis. Supports Spring MVC, Servlet, JAX-RS, Struts 2, CXF Web Services and other frameworks. **Must output all interfaces without omitting anything, including the complete SOAP methods of Web Services**."
zh-signals: "从 Java Web 源码提取所有 HTTP 路由与参数，生成 Burp Suite 请求模板并导出 MD 文档。信号:Java,路由提取,源码分析,Burp,Spring MVC"
when-to-use: "Use when you need to extract every HTTP route and parameter from Java Web source and generate Burp Suite request templates, especially when no API docs exist."
---

# Java Source Route & Parameter Mapper

**Extract** all HTTP routes and request parameter structures from Java Web project source code and generate Burp Suite Repeater request templates. **Does not perform security vulnerability assessment, code quality analysis, or any output beyond the scope of route extraction.**

## ⚠️ Core requirement: complete output

**This skill must output all discovered interfaces; omissions are not allowed.**

- ✅ Each interface must have a complete parameter analysis
- ✅ Each interface must have a Burp Suite request template (must be inside an md code block)
- ✅ Output the total number of interfaces and a list for verification
- ❌ Do not abbreviate with "..." or "etc." or "other"
- ❌ Do not output only "key interfaces" or "important interfaces"
- ❌ Do not omit content because the number is large

---

## ⚠️ CRITICAL rules summary (mandatory)

**The following rules are mandatory; violating any one of them makes the output non-compliant.**

---

### CRITICAL 1: Wildcard/dynamic routes must be expanded

#### 1.1 Struts2 wildcard routes

**Applicable scenarios:** When the following wildcard configurations exist in struts.xml, they must be expanded
- `name="*_*"` - double wildcard
- `name="user_*"` - single wildcard
- `name="*"` - match-all

**Mandatory execution steps (cannot be skipped):**

1. **Identify the wildcard configuration**
   ```xml
   <action name="*_*" class="{1}Action" method="{2}">
   ```

2. **Decompile all Action classes under that namespace**
   ```bash
   mcp__java-decompile-mcp__decompile_directory(
       directory_path="{WEB-INF/classes/corresponding package path}",
       recursive=true,
       save_to_file=true
   )
   ```

3. **Extract the business methods of each Action class**
   - All public methods
   - Exclude: getters/setters (get*/set*/is*)
   - Exclude: methods inherited from ActionSupport (except execute)
   - Keep: all other public methods

4. **Generate a route mapping table and a separate request template for each route**

#### 1.2 Spring MVC path variables

**Applicable scenarios:** When path variables exist in `@RequestMapping`
- `@GetMapping("/user/{id}")` - path variable
- `@RequestMapping("/api/{version}/**")` - wildcard path

**Mandatory execution steps:**

1. **Identify the path variable pattern**
   ```java
   @GetMapping("/user/{id}/orders/{orderId}")
   ```

2. **Generate placeholder descriptions for each path variable**
   ```markdown
   Path variables:
   - {id}: user ID (type: Long)
   - {orderId}: order ID (type: String)
   ```

3. **Use the `{{variable-name}}` format in Burp templates**

#### 1.3 JAX-RS path parameters

**Applicable scenarios:** When path parameters exist in the `@Path` annotation
- `@Path("/users/{userId}")` - path parameter
- `@Path("{resource}/{id}")` - multi-level path parameter

**Mandatory execution steps:**

1. **Identify the `@PathParam` annotation**
   ```java
   @GET
   @Path("/{userId}/profile")
   public User getProfile(@PathParam("userId") Long userId)
   ```

2. **Extract the parameter types and generate the complete template**

#### 1.4 Servlet URL Pattern wildcards

**Applicable scenarios:** When wildcards exist in web.xml or `@WebServlet`
- `<url-pattern>/api/*</url-pattern>` - path wildcard
- `<url-pattern>*.do</url-pattern>` - extension wildcard

**Mandatory execution steps:**

1. **Analyze the doGet/doPost methods of the Servlet class**
2. **Extract how `request.getPathInfo()` or `request.getServletPath()` is used**
3. **Infer possible sub-paths from the code logic**

---

### CRITICAL 2: Web Service method complete-output rules

#### 2.1 Configuration-file-first principle

**The URL path of a Web Service must be read from the configuration file; it must never be inferred from the class name or endpoint id!**

**Parsing priority (execute in order):**

1. **Read the configuration file** - applicationContext.xml or other Spring configuration
2. **Extract the address attribute** - this is the only authoritative source of the Web Service path
3. **Verify the Servlet mapping** - obtain /ws/* or /services/* from web.xml
4. **Assemble the complete URL** - context path + Servlet mapping + address
5. **Decompile the implementation class** - only for extracting method signatures, not for inferring the path

**URL composition formula:**
```
Complete URL = context path + Servlet mapping in web.xml + address attribute value

Example: /myapp + /services/ + /UserApi = /myapp/services/UserApi
```

**Incorrect examples (must be avoided):**
- ❌ Infer from the class name: `UserServiceImpl` → `/UserService`
- ❌ Infer from the id: `userWebService` → `/userWebService`
- ✅ Read the configuration: `address="/UserApi"` → `/myapp/services/UserApi`

#### 2.2 CXF/JAX-WS services

**Mandatory execution steps:**

1. **Obtain all endpoints from the configuration file**
   ```xml
   <jaxws:endpoint id="userService"
                   implementor="#userServiceImpl"
                   address="/UserService"/>
   ```

2. **Decompile each Service implementation class**

3. **Extract all public methods** - method name, parameter list, return type

4. **Generate a separate SOAP request template for each method**

5. **Record the configuration source** - configuration file path, line number, address attribute value, implementor class name

#### 2.3 Axis/Axis2 services

**Mandatory execution steps:**

1. **Read server-config.wsdd or services.xml**
   ```xml
   <service name="UserService" provider="java:RPC">
     <parameter name="className" value="com.example.UserService"/>
   </service>
   ```

2. **Extract the service name and implementation class**

3. **Decompile the implementation class to obtain the method list**

4. **URL composition:** `/axis/services/{serviceName}`

#### 2.4 Special handling for executeInterface-type services

For generic execution interfaces routed via the interfaceId parameter:

1. **Decompile the implementation class and find all interfaceId definitions**
2. **Generate a separate request template for each interfaceId**

---

### CRITICAL 3: Forbidden output formats

**The following output formats are strictly forbidden:**

| Forbidden pattern | Incorrect example | Correct approach |
|:---------|:---------|:---------|
| Using "etc." to abbreviate | `LoginAction, UserAction etc.` | List all Actions |
| Using "..." to abbreviate | `method1, method2, ...` | List all methods |
| Using "other" to abbreviate | `and the other 20 methods` | List all 20 methods |
| Using "more" to abbreviate | `see the source code for more interfaces` | List all interfaces directly |
| Using placeholders | `{action}_{method}.action` | Expand to the actual URL |
| Using ranges | `001 ~ 050` | List 001, 002, ..., 050 one by one |
| Describing instead of listing | `Method list: user-management related` | List the specific method names |
| Giving only the WSDL address | `See the WSDL for available methods` | List all SOAP methods |
| Listing only class names without methods | `UserAction supports multiple methods` | List the complete template for each method |

---

### CRITICAL 4: Required output format for each framework

#### 4.1 Struts2 routes

```markdown
=== [1] login_login.action ===
URL: `/admin/login_login.action`
Method: LoginAction.login()
Parameters: loginName (String), password (String)

Burp Suite request template:
\```http
POST /admin/login_login.action HTTP/1.1
Host: {{host}}
Content-Type: application/x-www-form-urlencoded

loginName={{username}}&password={{password}}
\```
```

#### 4.2 Spring MVC routes

```markdown
=== [1] GET /api/users/{id} ===
Location: UserController.getUser (UserController.java:45)
HTTP method: GET
URL path: /api/users/{id}

Parameter structure:
  Path: {id} (Long) - user ID
  Header: Authorization - Bearer Token

Burp Suite request template:
\```http
GET /api/users/{{userId}} HTTP/1.1
Host: {{host}}
Authorization: Bearer {{token}}
\```
```

#### 4.3 JAX-RS routes

```markdown
=== [1] GET /rest/users/{userId} ===
Location: UserResource.getUser (UserResource.java:32)
HTTP method: GET
URL path: /rest/users/{userId}

Parameter structure:
  Path: {userId} (Long)
  Query: includeOrders (boolean, optional)

Burp Suite request template:
\```http
GET /rest/users/{{userId}}?includeOrders=true HTTP/1.1
Host: {{host}}
Accept: application/json
\```
```

#### 4.4 Servlet routes

```markdown
=== [1] POST /api/upload ===
Location: UploadServlet.doPost (UploadServlet.java:28)
HTTP method: POST
URL path: /api/upload

Parameter structure:
  Body: multipart/form-data
    - file (File) - uploaded file
    - description (String) - file description

Burp Suite request template:
\```http
POST /api/upload HTTP/1.1
Host: {{host}}
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="test.txt"
Content-Type: text/plain

{{fileContent}}
------WebKitFormBoundary
Content-Disposition: form-data; name="description"

{{description}}
------WebKitFormBoundary--
\```
```

#### 4.5 Web Service (SOAP) methods

```markdown
### UserService (5 methods in total)

- **Configuration file**: applicationContext.xml:42
- **address attribute**: /UserApi
- **Complete URL**: /myapp/services/UserApi

=== [WS-1] login ===
Method signature: login(String loginName, String password)
Return type: String

Burp Suite request template:
\```http
POST /myapp/services/UserApi HTTP/1.1
Host: {{host}}
Content-Type: text/xml; charset=utf-8
SOAPAction: ""

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:web="http://webservice.example.com">
  <soapenv:Header/>
  <soapenv:Body>
    <web:login>
      <loginName>{{username}}</loginName>
      <password>{{password}}</password>
    </web:login>
  </soapenv:Body>
</soapenv:Envelope>
\```
```

---

### CRITICAL 5: Mandatory pre-output verification

**This verification must pass before writing files; if it fails, you must go back and supplement content.**

#### 5.1 Quantity consistency check

| Check item | Formula | Pass condition |
|:-------|:---------|:---------|
| Struts2 routes | actual template count ÷ Action class count | ≥ 3 |
| Spring MVC interfaces | actual template count ÷ Controller class count | ≥ 2 |
| JAX-RS interfaces | actual template count ÷ Resource class count | ≥ 2 |
| Servlet interfaces | actual template count ÷ Servlet class count | ≥ 1 |
| Web Service methods | actual template count ÷ methods obtained by decompilation | = 100% |

#### 5.2 Omission-word detection

Scan the output content; if any omission marker is detected, replace it with the complete content.

#### 5.3 File integrity check

- [ ] Every module in the main index has a corresponding detail file
- [ ] Every detail file contains the complete request template (not a summary)
- [ ] Every service in the Web Service index has a complete method list
- [ ] No case where "see xxx for details" appears but the xxx file does not exist

#### 5.4 Handling when verification fails

1. Stop the current output
2. Identify the missing content type
3. Decompile to obtain the complete information
4. Supplement the missing request templates
5. Re-run the verification
6. Write the file only after verification passes

---

### CRITICAL 6: Completeness checklist (mandatory)

**Before marking the task complete, you must perform the following checks:**

#### 6.1 Module integrity check

```markdown
□ Every module listed in the main index has a corresponding detail file generated

  Demo example:
  ==========
  Suppose the "module index" table in the main index file is as follows:

  | Module | File | Interface count |
  |:-----|:-------|:-----|
  | admin | [admin/myapp_module_admin.md](admin/myapp_module_admin.md) | 218 |
  | user | [user/myapp_module_user.md](user/myapp_module_user.md) | 85 |
  | api | [api/myapp_module_api.md](api/myapp_module_api.md) | 45 |

  Verification steps:
  1. Check whether admin/myapp_module_admin.md exists
  2. Check whether user/myapp_module_user.md exists
  3. Check whether api/myapp_module_api.md exists
  4. Confirm module count (3) = actual file count (3)

□ Every service in the Web Service index has a corresponding detail file generated

□ No case where "see xxx for details" appears but the xxx file does not exist
```

#### 6.2 Cross-verification checklist

```markdown
□ File count consistency
  Demo example: the main index lists 5 modules → there must be 5 corresponding module subdirectories, each containing a corresponding module_xxx.md file

□ File name consistency
  Demo example: the main index references admin/myapp_module_admin.md → the actual relative path and file name must match exactly

□ Link validity
  Demo example: clicking the [admin/myapp_module_admin.md] link in the main index should open successfully
```

#### 6.3 Content completeness check

```markdown
□ Every detail file contains:
  - Module overview (project name, context path, framework)
  - Framework configuration (configuration file location)
  - Detailed route list (complete information for each interface)
  - Burp Suite request template

□ For empty modules (modules without routes):
  Demo example:
  ==========
  A certain upload module has only static resources and no business routes

  Correct approach: still generate upload/myapp_module_upload.md
  ```markdown
  # MyApp - upload module details

  ## Module overview
  This module is mainly used for static file upload; no business routes were detected.

  ## Check results
  - WEB-INF directory: does not exist
  - Configuration file: none
  - Route interfaces: none
```

  Incorrect approach: skip and do not generate the file
```

#### 6.4 Execute verification commands

**Demo example: after all files are generated, run the following commands to verify**

```bash
# Assume the project name is myapp and the output directory is route_mapper/; the generated files are as follows:
# route_mapper/myapp_route_mapper_20260129.md       (main index)
# route_mapper/admin/myapp_module_admin_20260129.md  (admin module)
# route_mapper/user/myapp_module_user_20260129.md    (user module)
# route_mapper/api/myapp_module_api_20260129.md      (api module)

# Verification command 1: check the generated module subdirectories and files
find route_mapper/ -name "*_module_*.md" -type f
# Expected output: you should see 3 module detail files

# Verification command 2: extract all referenced file paths from the main index
grep -oP '[a-z]+/myapp_module_[^)]*md' route_mapper/myapp_route_mapper_20260129.md | sort -u

# Verification command 3: check whether all referenced files exist
grep -oP '[a-z]+/myapp_[^)]*md' route_mapper/myapp_route_mapper_20260129.md | while read f; do
  if [ ! -f "route_mapper/$f" ]; then
    echo "❌ Missing file: route_mapper/$f"
  else
    echo "✅ Existing file: route_mapper/$f"
  fi
done
```

#### 6.5 Completion confirmation

**Demo example: the complete check flow**

```markdown
Suppose an e-commerce project named myshop was analyzed, containing the following modules:

Step 1: Generate the main index file
  ✅ route_mapper/myshop_route_mapper_20260129.md

Step 2: Check the module list in the main index
  The main index shows: product, order, user, payment (4 modules)

Step 3: Verify whether the module subdirectories and detail files exist
  ✅ route_mapper/product/myshop_module_product_20260129.md
  ✅ route_mapper/order/myshop_module_order_20260129.md
  ✅ route_mapper/user/myshop_module_user_20260129.md
  ✅ route_mapper/payment/myshop_module_payment_20260129.md

Step 4: Generate the README document
  ✅ route_mapper/myshop_README_20260129.md

Step 5: Execute verification commands
  $ find route_mapper/ -name "*_module_*.md" -type f | wc -l
  4 (consistent with the number of modules in the main index)

Step 6: Confirm completion
  All check items pass → the task can be marked complete
```

**Only when all of the following conditions are met can the task be marked complete:**

- [ ] Main index file generated
- [ ] README documentation generated
- [ ] Every module listed in the main index has a corresponding detail file
- [ ] Every detail file contains complete route information (or explicitly states that there are no routes)
- [ ] All file links are accessible
- [ ] Verification commands have been run

**If missing files are found, you must:**
1. Immediately supplement the missing files
2. Update the main index (if links do not match)
3. Re-run the integrity check

---

## Workflow

### 1. Project scan initialization

```
Input: project source path
       Optional: project context path, known framework information
```

**Initialization steps:**

1. Identify the project type and framework (via configuration files and directory structure) - **supports multi-framework mixed projects**
2. Determine the route loading method (annotation-driven / XML configuration / mixed)
3. Extract the context path and base URL

### 2. Framework identification and task planning

**Multi-framework support:** A project may use multiple Web frameworks at the same time; each must be identified separately and an analysis task created.

| Framework | Identification features | Reference |
|------|---------|---------|
| Spring MVC | `@Controller`, `@RequestMapping` | [SPRING_MVC.md](references/SPRING_MVC.md) |
| Spring Boot | `application.properties/yml`, Spring Boot starter | [SPRING_MVC.md](references/SPRING_MVC.md) |
| Servlet | `web.xml`, `@WebServlet` | [SERVLET.md](references/SERVLET.md) |
| JAX-RS | `@Path`, `@GET`, `@POST` | [JAXRS.md](references/JAXRS.md) |
| Struts 2 | `struts.xml` | [STRUTS.md](references/STRUTS.md) |
| CXF Web Services | `/ws/*`, `@WebService`, `applicationContext.xml` | [WEBSERVICE.md](references/WEBSERVICE.md) |

**Task planning rules:**
- Generate a separate analysis task for each detected framework
- Order tasks by execution sequence (framework initialization → route scanning → parameter parsing)
- Mixed configurations (annotations + XML) require analyzing both approaches

### 3. Route enumeration

Scan the project source code and extract all externally accessible HTTP routes.

**Scan scope:**
- `@Controller` / `@RestController` classes
- `@RequestMapping` and its variant annotations
- Servlet configuration (web.xml, @WebServlet)
- JAX-RS annotations (@Path, @GET, @POST, etc.)
- Struts2 Action configuration
- Web Service endpoint configuration

**Output information:**
- HTTP method
- URL path (complete path)
- Corresponding controller class and method

### 4. Parameter structure parsing

Parse the parameter structure of each route.

**Parameter sources:**
- **Path variables**: `@PathVariable`, `@PathParam`
- **Query parameters**: `@RequestParam`, `@QueryParam`
- **Body parameters**: `@RequestBody`, request object, Form form
- **Header parameters**: `@RequestHeader`, `@HeaderParam`
- **Cookie parameters**: `@CookieValue`, `@CookieParam`

**Parameter type parsing:**
- Primitive types (String, int, long, etc.)
- Object types (POJO)
- Collection types (List, Map, Set)
- Enum types

### 5. Decompilation support (when necessary)

When interface definitions or method signatures are in compiled .class files or third-party JARs:

1. Use the MCP Java Decompiler tool to decompile the target files
2. Extract method signatures and parameter type definitions
3. Reconstruct the parameter structure

**Decompilation strategy:**
- Decompile only the classes containing the target interfaces or parameter definitions
- Prefer existing source code
- Record the decompilation source for traceability

### 6. Generate output

**Important: you must output all discovered interfaces; do not omit or summarize.**

Generate a complete HTTP request template for **each** interface, including:
- All routes (even if the number is large)
- The complete parameter structure of each route
- The Burp Suite request template for each route (must be inside an md code block)

**Forbidden operations:**
- ❌ Do not use "..." to omit interfaces
- ❌ Do not use "etc." or "other" to abbreviate
- ❌ Do not output only "key interfaces" or "important interfaces"
- ❌ Do not use a table summary because the number is large
- ❌ Do not say "due to the large number, only some are listed"
- ❌ Do not output only the WSDL address without generating concrete SOAP requests
- ❌ Do not list only Action class names without generating concrete request templates

**Mandatory requirements:**
- ✅ Every Struts2 action route must have a corresponding request template
- ✅ Every REST interface must have a complete request template
- ✅ Every Web Service method must have a separate SOAP request template
- ✅ For executeInterface-type services, a separate request template must be generated for each methodId

**Required output format (per entry):**

````markdown
=== [index] interface identifier ===

Annotation: (copy only the original @ApiOperation or Javadoc text from the source; leave blank if there is none)
Location: ClassName.methodName (source file:line number)

HTTP method: GET/POST/PUT/DELETE etc.
URL path: /complete/path/structure

Parameter structure:
  Path: {pathVar1}, {pathVar2}
  Query: param1, param2 (type: String)
  Body: ContentType (type definition)
  Header: X-Custom-Header
  Cookie: sessionId

Burp Suite request template (must be in a code block):
```http
HTTP_METHOD /path/structure HTTP/1.1
Host: {{host}}
Content-Type: application/json
[other required headers]

[request body]
```
````

### 7. File splitting strategy

**Output must be in MD file format, split by hierarchical directories (one MD file per level).**

When the number of interfaces is large, the output files must be split to ensure every interface has a complete template.

#### 7.1 Split trigger conditions

Splitting is triggered when any of the following conditions is met:
- Interfaces per module > 50
- Interfaces per namespace > 20
- Web Service methods per service > 10
- Estimated output file size > 100KB

#### 7.2 File naming and directory strategy

**Create subdirectories by module and generate file names dynamically.**

| File type | Naming format | Example |
|---------|---------|------|
| Main index | `route_mapper/{project-name}_route_mapper_{timestamp}.md` | `route_mapper/myapp_route_mapper_20260121.md` |
| Module details | `route_mapper/{module-name}/{project-name}_module_{module-name}_{timestamp}.md` | `route_mapper/admin/myapp_module_admin_20260121.md` |
| Web Service | `route_mapper/webservice/{project-name}_ws_{service-name}_{timestamp}.md` | `route_mapper/webservice/myapp_ws_userservice_20260121.md` |
| Namespace split | `route_mapper/{module-name}/{project-name}_{namespace}_{timestamp}.md` | `route_mapper/admin/myapp_admin_user_20260121.md` |
| README | `route_mapper/{project-name}_README_{timestamp}.md` | `route_mapper/myapp_README_20260121.md` |

**Directory creation rules:**
- Place the main index and README in the `route_mapper/` root directory
- Place each module's detail file in the `route_mapper/{module-name}/` subdirectory
- Place all Web Service files in the `route_mapper/webservice/` subdirectory
- Subdirectories are created on demand by the route-mapper agent (`mkdir -p`)

**Dynamic module name examples:**

| Actual module/namespace | Subdirectory | Generated file name |
|------------------|:------|:-------------|
| `admin` | `admin/` | `admin/myapp_module_admin_20260121.md` |
| `user` | `user/` | `user/myapp_module_user_20260121.md` |
| `config` | `config/` | `config/myapp_module_config_20260121.md` |
| `api` | `api/` | `api/myapp_module_api_20260121.md` |
| `product` | `product/` | `product/myapp_module_product_20260121.md` |
| `order` | `order/` | `order/myapp_module_order_20260121.md` |
| `/` (root namespace) | `root/` | `root/myapp_module_root_20260121.md` |

**Module identification sources:**

1. **Directory structure** - subdirectory names under webapps
2. **Context path** - Context Path configuration
3. **Struts2 namespace** - package namespace in struts.xml
4. **Spring @RequestMapping** - class-level path prefix
5. **Web Service path** - e.g. `/services/`, `/ws/`

#### 7.3 Splitting strategy

**Strategy A: Split by module subdirectory (recommended)**

One subdirectory per module, with the main index in the root directory:

```
route_mapper/
├── {project_name}_route_mapper_{timestamp}.md         # main index file (root directory)
├── {project_name}_README_{timestamp}.md               # documentation (root directory)
├── admin/                                             # admin module subdirectory
│   └── {project_name}_module_admin_{timestamp}.md     # interfaces ≤ 50 → single file
├── user/                                              # user module subdirectory
│   ├── {project_name}_module_user_{timestamp}.md      # interfaces > 50 → module overview + namespace split
│   ├── {project_name}_user_manage_{timestamp}.md      # namespace details
│   └── {project_name}_user_auth_{timestamp}.md        # namespace details
└── webservice/                                        # Web Service subdirectory
    └── {project_name}_ws_orderService_{timestamp}.md
```

**Links in the main index file point to subdirectories:**
```markdown
## Module index

| Module | File | Interface count | Framework |
|:-----|:-------|:-----|:-----|
| admin | [admin/myapp_module_admin_20260121.md](admin/myapp_module_admin_20260121.md) | 35 | Struts2 |
| user | [user/myapp_module_user_20260121.md](user/myapp_module_user_20260121.md) | 218 | Struts2+Spring |

## Web Service index

| Service | File | Method count |
|:-----|:----|:--------|
| OrderService | [webservice/myapp_ws_orderService_20260121.md](webservice/myapp_ws_orderService_20260121.md) | 40 |
```

**Split trigger rules:**

| Condition | Behavior |
|:-----|:-----|
| Interfaces per module ≤ 50 | Single file placed in the module subdirectory |
| Interfaces per module > 50 | Module overview + split by namespace, all placed in the module subdirectory |

**Strategy B: Split by namespace (for cases with a very large number of interfaces in a single module)**

When a single module has > 50 interfaces, continue splitting by namespace inside that module subdirectory:

```
route_mapper/admin/
├── {project_name}_module_admin_{timestamp}.md          # module overview (with sub-file index)
├── {project_name}_admin_device_{timestamp}.md          # /device namespace
├── {project_name}_admin_channel_{timestamp}.md         # /channel namespace
└── {project_name}_admin_login_{timestamp}.md           # / namespace (login-related)
```

#### 7.4 Split implementation rules

1. **Analyze first, then split**
   - After completing the route analysis, count the interfaces in each module/namespace
   - Decide the splitting strategy based on the counts

2. **Generate the main index file**
   - Include the project overview, module index, and statistical summary
   - Link to each detail file

3. **Create module subdirectories and generate detail files**
   - For each module, run `mkdir -p {output_path}/route_mapper/{module-name}/`
   - Place all Web Services uniformly under `mkdir -p {output_path}/route_mapper/webservice/`
   - Write each module/namespace independently into a file under the corresponding subdirectory

4. **Ensure traceability**
   - The main index contains the **relative subdirectory path** of each detail file (e.g. `admin/myapp_module_admin_xxx.md`)
   - Note the module and generation time at the top of each detail file

#### 7.5 Web Service method splitting

For Web Services of the `execute` type or similar dynamic invocation:

**Incorrect approach:**
```markdown
#### UserService
Supported method IDs: user_001_001, user_001_002, ... (40 in total)
```

**Correct approach - split into separate files:**

Main file:
```markdown
#### UserService (service path: /services/UserService)
See the detailed method list at: [webservice/myapp_ws_user_20260121.md](webservice/myapp_ws_user_20260121.md)
```

Detail file `webservice/myapp_ws_user_20260121.md`:
````markdown
# UserService Method Details

=== [1] user.create ===
Method ID: user_001_001
Description: create a user
Parameters: {"username": "...", "email": "...", "role": "..."}

Burp Suite request template (must be in a code block):
```http
POST /admin/services/UserService HTTP/1.1
Host: {{host}}
Content-Type: text/xml; charset=utf-8
SOAPAction: ""

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:web="http://webservice.example.com">
  <soapenv:Header/>
  <soapenv:Body>
    <web:executeInterface>
      <interfaceId>user_001_001</interfaceId>
      <jsonParam>{"username":"{{username}}","email":"{{email}}","role":"{{role}}"}</jsonParam>
    </web:executeInterface>
  </soapenv:Body>
</soapenv:Envelope>
```

=== [2] user.update ===
[complete request template]

[all 40 methods have complete templates...]
````

### 8. Output file structure

**Strictly follow the fill-in templates in the references/ directory to generate output files.**

| File type | Template | Naming format | Count |
|---------|------|---------|------|
| Main index | [OUTPUT_TEMPLATE_INDEX.md](references/OUTPUT_TEMPLATE_INDEX.md) | `route_mapper/{project_name}_route_mapper_{YYYYMMDD_HHMMSS}.md` | 1 |
| Module details | [OUTPUT_TEMPLATE_MODULE.md](references/OUTPUT_TEMPLATE_MODULE.md) | `route_mapper/{module_name}/{project_name}_module_{module_name}_{YYYYMMDD_HHMMSS}.md` | N (by module) |
| WS details | [OUTPUT_TEMPLATE_MODULE.md](references/OUTPUT_TEMPLATE_MODULE.md) | `route_mapper/webservice/{project_name}_ws_{service_name}_{YYYYMMDD_HHMMSS}.md` | N (by service) |
| Documentation | [OUTPUT_TEMPLATE_README.md](references/OUTPUT_TEMPLATE_README.md) | `route_mapper/{project_name}_route_README_{YYYYMMDD_HHMMSS}.md` | 1 |

**Key Rules:**
- All [FILL IN] placeholders must be replaced with actual content
- Every interface must have a complete Burp Suite request template
- No interface may be omitted
- File names are generated dynamically based on the module names/namespaces actually found in the project
- Common specification reference: [shared/OUTPUT_STANDARD.md](../shared/OUTPUT_STANDARD.md)

**Saving steps:**
1. Complete all route analysis
2. Count the interfaces in each module/namespace
3. Decide the splitting strategy based on the split trigger conditions
4. Generate the main index file from the template
5. Generate the detail files for each module/namespace from the template
6. Generate the documentation from the template
7. **Execute the self-check checklist at the end of each template**
8. Tell the user where all files are saved in the output

---

## Batch processing strategy for large projects

### Trigger conditions

Enable batch processing when any of the following conditions is met:
- Estimated total interfaces > 100
- Interfaces per namespace > 30
- Web Service methods per service > 20

### Batch processing steps

**Step 1: Group by namespace/module**
**Step 2: Process each namespace one by one** (decompile → extract methods → generate templates → verify → write)
**Step 3: Incremental writes** (write to the file immediately after every 10 interfaces are completed)
**Step 4: Progress checkpoints** (verify the interface count after each namespace is completed)

### File naming rules

For large projects, split files by module subdirectory + namespace:
```
route_mapper/
├── {project}_route_mapper_{date}.md                    # main index
├── {module}/
│   ├── {project}_module_{module}_{date}.md             # module overview
│   └── {project}_{module}_{namespace}_{date}.md        # namespace details
└── webservice/
    └── {project}_ws_{service}_{date}.md                # Web Service details
```

---

## Automatic correction rules

When omitted content is detected, perform corrections automatically:

| Detected problem | Automatic correction action |
|:-------------|:-------------|
| `Action1, Action2 etc.` | Decompile to obtain the complete Action list; replace with all of them |
| `{action}_{method}.action` | Decompile to obtain the actual methods; expand to concrete URLs |
| `Method list: descriptive text` | Decompile to obtain method signatures; replace with concrete methods |
| `N methods in total` but fewer than N are listed | Supplement the missing methods until the count matches |
| `interfaceId: xxx ~ yyy` | Expand into individual interfaceIds |

---

## Troubleshooting

| Problem | Solution |
|:-----|:---------|
| Framework cannot be identified | Check the configuration files in the project root; see [FRAMEWORK_PATTERNS.md](references/FRAMEWORK_PATTERNS.md) |
| Route path is incomplete | Check the class-level `@RequestMapping` and context path configuration |
| Parameter type is unknown | Use the decompilation tool to obtain the complete type definition |
| Generated requests are inaccessible | Confirm that they are not restricted by a security interceptor/filter |
| Module name is not as expected | File names are generated dynamically based on the modules/namespaces actually found |