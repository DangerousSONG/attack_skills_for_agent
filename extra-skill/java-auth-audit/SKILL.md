---
name: java-auth-audit
description: "Java Web source-code authentication mechanism audit tool. Identifies all authentication implementations in the source code and detects authentication bypass vulnerabilities and broken access control flaws. Suitable for: (1) identifying authentication frameworks and implementation approaches, (2) finding authentication bypass vulnerabilities, (3) detecting broken access control flaws, (4) auditing permission-check logic. Supports Shiro, Spring Security, JWT, Filter/Interceptor, custom authentication, and more. **Supports decompiling .class/.jar files to extract authentication logic**. Combined with java-route-mapper, it enables a complete route + authentication audit."
zh-signals: "审计 Java Web 源码鉴权实现，检测鉴权绕过、越权访问与组件版本漏洞。信号:Java鉴权审计,Shiro,Spring Security,鉴权绕过,越权访问。"
when-to-use: >-
  Use when auditing a Java web project's authentication and authorization code, identifying Shiro/Spring Security/JWT/Filter implementations, or reviewing decompiled classes for auth-bypass and privilege-escalation flaws.
---

# Java Authentication Mechanism Audit Tool

Scan Java Web project source code, identify authentication mechanism implementations, and detect authentication bypass vulnerabilities and broken access control flaws.

---

## Vulnerability Severity Rating Standard

**See [SEVERITY_RATING.md](../shared/SEVERITY_RATING.md) for details**

- Vulnerability ID format: `{C/H/M/L}-AUTH-{number}`
- Severity Level = f(Reachability R, Impact Scope I, Exploitation Complexity C)
- Score = R × 0.40 + I × 0.35 + C × 0.25, mapped to CVSS 3.1

---

## Detection Scope Boundaries

**This skill's detection scope covers only the following types:**
- Authentication bypass vulnerabilities (Bypass)
- Broken access control flaws (Privilege Escalation)
- Session management flaws (Session Fixation / Hijacking)
- Known component vulnerabilities (CVE)

**The following are outside this skill's detection scope (even if they are "security issues" in the usual sense):**
- ❌ Code quality issues (non-standard naming, redundant logic, performance problems, etc.)
- ❌ General security vulnerabilities (SQL injection, XSS, CSRF, etc.; use the dedicated skill)
- ❌ Architecture design suggestions (missing rate limiting, audit logging, encryption strength, etc.)
- ❌ Business logic reasonableness (business decisions such as whether an interface should be public)

---

## Core Requirements

**This skill must fully inspect all authentication-related code; omissions are not allowed.**

- ✅ Identify all authentication entry points (Filter/Interceptor/annotations)
- ✅ Analyze the authentication status of every route
- ✅ Detect all potential authentication bypass patterns
- ✅ Provide a verification PoC for each vulnerability point
- ❌ Do not omit any authentication configuration
- ❌ Never skip the decompilation step

---

## Workflow

### 1. Project Analysis Initialization

```
Input: project source path
       Optional: known framework information, paths of interest
```

**Initialization steps:**

1. Identify the project type (source / compiled / mixed)
2. Identify the authentication framework (via configuration files and characteristic classes)
3. Determine whether decompilation is required

### 2. Authentication Framework Identification

| Framework | Identification Features | Configuration Files | Reference |
|------|----------|----------|----------|
| Shiro | `shiro.ini`, `@RequiresAuthentication`, `SecurityUtils` | `shiro.ini`, `shiro-spring.xml` | [SHIRO.md](references/SHIRO.md) |
| Spring Security | `@EnableWebSecurity`, `SecurityFilterChain`, `@PreAuthorize` | `SecurityConfig.java` | [SPRING_SECURITY.md](references/SPRING_SECURITY.md) |
| JWT | `io.jsonwebtoken`, `JwtParser`, `Bearer Token` | - | [JWT.md](references/JWT.md) |
| Filter | `implements Filter`, `doFilter()` | `web.xml` | [FILTER_INTERCEPTOR.md](references/FILTER_INTERCEPTOR.md) |
| Interceptor | `implements HandlerInterceptor`, `preHandle()` | `WebMvcConfig` | [FILTER_INTERCEPTOR.md](references/FILTER_INTERCEPTOR.md) |
| Annotation-based authentication | `@RequiresRoles`, `@PreAuthorize`, custom annotations | - | [ANNOTATION_AUTH.md](references/ANNOTATION_AUTH.md) |

### 2.1 Component Version Detection (CRITICAL)

**You must detect the versions of authentication-related components and identify known vulnerabilities.**

For detailed vulnerable versions, see [VERSION_VULNS.md](references/VERSION_VULNS.md)

#### Version Identification Methods

**Method 1: JAR filename identification**

```bash
# Scan the WEB-INF/lib directory
ls WEB-INF/lib/ | grep -E "shiro|spring-security|jwt|pac4j"

# Common naming formats
shiro-core-1.4.0.jar          → Shiro 1.4.0
spring-security-core-5.7.3.jar → Spring Security 5.7.3
jjwt-0.9.1.jar                → JJWT 0.9.1
pac4j-core-4.0.0.jar          → PAC4J 4.0.0
```

**Method 2: pom.xml parsing**

```xml
<dependency>
    <groupId>org.apache.shiro</groupId>
    <artifactId>shiro-spring</artifactId>
    <version>1.4.0</version>  <!-- extract the version number -->
</dependency>
```

**Method 3: MANIFEST.MF parsing**

```bash
# Extract the JAR and inspect MANIFEST.MF
unzip -p shiro-core-1.4.0.jar META-INF/MANIFEST.MF

# Key fields
Implementation-Version: 1.4.0
Bundle-Version: 1.4.0
```

**Method 4: pom.properties inside the JAR**

```bash
# View the Maven properties file inside the JAR
unzip -p shiro-core.jar META-INF/maven/org.apache.shiro/shiro-core/pom.properties

# Example content
version=1.4.0
groupId=org.apache.shiro
artifactId=shiro-core
```

#### High-risk Component Version Quick Reference

| Component | Vulnerable Version | CVE | Risk | Notes |
|------|----------|-----|------|------|
| Shiro | < 1.5.2 | CVE-2020-1957 | Path bypass | Requires Spring |
| Shiro | < 1.5.3 | CVE-2020-11989 | Authentication bypass | Requires Spring |
| Shiro | < 1.6.0 | CVE-2020-13933 | Authentication bypass | - |
| Shiro | < 1.7.1 | CVE-2020-17523 | Authentication bypass | Requires Spring integration |
| Shiro | < 1.8.0 | CVE-2021-41303 | Path bypass | - |
| Shiro | < 1.9.1 | CVE-2022-32532 | RegEx bypass | When regex matching is used |
| Shiro | < 1.11.0 | CVE-2023-22602 | Path bypass | Spring Boot 2.6+ |
| Spring Security | < 5.7.5 | CVE-2022-31692 | Authorization bypass | - |
| Spring Security | < 5.4.11 / < 5.5.7 / < 5.6.4 | CVE-2022-22978 | RegEx bypass | Newline bypass |
| PAC4J | < 4.0.0 | CVE-2021-44878 | Authentication bypass | - |
| JJWT | < 0.10.0 | - | Weak key risk | - |

#### Version Detection Output Format

```markdown
## Component Version Analysis

### Detected Authentication Components

| Component | Current Version | Latest Version | Risk Status |
|------|----------|----------|----------|
| shiro-core | 1.4.0 | 1.13.0 | ❌ Known vulnerabilities present |
| spring-security-core | 5.7.3 | 6.2.0 | ⚠️ Upgrade required |
| jjwt | 0.11.2 | 0.12.3 | ✅ Secure |

### Known Vulnerability Details

=== [CVE-2020-11989] Shiro Path Bypass ===
Affected versions: < 1.5.3
Current version: 1.4.0
Risk level: High

Vulnerability description:
- Shiro path matching under the Spring framework can be bypassed
- An attacker can bypass authentication through a specially crafted path

Verification PoC:
\```http
GET /admin/page%2f HTTP/1.1
Host: {{host}}
\```

Remediation:
- Upgrade Shiro to 1.5.3 or later
```

### 3. Decompilation Stage (CRITICAL)

**When source code is unavailable, you must use the MCP Java Decompiler to decompile authentication-related classes.**

See [DECOMPILE_STRATEGY.md](references/DECOMPILE_STRATEGY.md) for the detailed strategy

#### 3.1 Decompiler Tool Invocation

```python
# Decompile a single authentication class
mcp__java-decompile-mcp__decompile_file(
    file_path="/path/to/AuthFilter.class",
    output_dir="/path/to/decompiled",
    save_to_file=True
)

# Decompile an authentication-related directory
mcp__java-decompile-mcp__decompile_directory(
    directory_path="/path/to/WEB-INF/classes/com/example/security",
    output_dir="/path/to/decompiled",
    recursive=True,
    save_to_file=True,
    max_workers=4
)

# Decompile multiple specified files
mcp__java-decompile-mcp__decompile_files(
    file_paths=[
        "/path/to/AuthFilter.class",
        "/path/to/SecurityConfig.class",
        "/path/to/PermissionInterceptor.class"
    ],
    output_dir="/path/to/decompiled",
    save_to_file=True
)
```

#### 3.2 Classes That Must Be Decompiled

| Type | Match Pattern | Purpose |
|------|----------|------|
| Filter | `*Filter.class`, `*AuthFilter.class` | Extract doFilter authentication logic |
| Interceptor | `*Interceptor.class` | Extract preHandle permission checks |
| Shiro configuration | `ShiroConfig.class`, `*Realm.class` | Extract filterChainDefinitionMap |
| Spring Security | `*SecurityConfig*.class` | Extract authorizeRequests configuration |
| Custom annotations | `*Permission*.class`, `*Auth*.class` | Extract annotation handling logic |
| Permission utility classes | `*PermissionUtil*.class`, `*SecurityUtil*.class` | Extract permission-check methods |

#### 3.3 Key Points for Analyzing Decompiled Results

```java
// Focus on the following after decompilation:
public class AuthFilter implements Filter {
    
    // 1. Whitelist paths - may be too broad
    private static final String[] EXCLUDE_PATHS = {"/login", "/public"};
    
    // 2. Path matching logic - may be bypassable
    private boolean isExcluded(String path) {
        return path.startsWith("/public");  // startsWith can be bypassed
    }
    
    // 3. Authentication check logic - may be flawed
    if (session.getAttribute("user") == null) {
        // Only checks whether the user is logged in, not the role
    }
}
```

### 4. Authentication Configuration Analysis

#### 4.1 Shiro Configuration Parsing

```ini
# shiro.ini
[urls]
/login = anon
/logout = logout
/admin/** = authc, roles[admin]
/api/** = authc
```

**Extracted content:**
- Public paths: `/login`
- Requires authentication: `/api/**`
- Requires role: `/admin/**` → `admin`

#### 4.2 Spring Security Configuration Parsing

```java
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/public/**").permitAll()
    .requestMatchers("/admin/**").hasRole("ADMIN")
    .anyRequest().authenticated()
);
```

**Extracted content:**
- Public paths: `/public/**`
- Requires role: `/admin/**` → `ADMIN`
- Default policy: requires authentication

#### 4.3 Filter Configuration Parsing

```xml
<!-- web.xml -->
<filter-mapping>
    <filter-name>AuthFilter</filter-name>
    <url-pattern>/api/*</url-pattern>
</filter-mapping>
```

**Analysis points:**
- Filter coverage
- Uncovered paths (potential risk)

### 5. Route-Authentication Mapping

Using route information (the java-route-mapper skill may be used), analyze the authentication status of each interface:

| Status | Meaning | Risk |
|------|------|------|
| ✅ Public | Explicitly configured for public access | None (confirm whether it should be public) |
| ✅ Protected | Complete authentication protection | None |
| ⚠️ Authentication only | Only checks login status, no role check | Medium (possible privilege bypass) |
| ❌ No authentication | No authentication mechanism found | High |
| ❓ Uncertain | Authentication logic is complex and requires manual confirmation | To be determined |

### 6. Vulnerability Detection

For detailed detection patterns, see [BYPASS_PATTERNS.md](references/BYPASS_PATTERNS.md)

#### 6.1 Authentication Bypass Detection

##### 6.1.1 URI Retrieval Method Difference Bypass (CRITICAL)

**This is the most common root cause of authentication bypass and must be detected first!**

For the detailed principle, see [URI_PARSING_BYPASS.md](references/URI_PARSING_BYPASS.md)

**Detection focus:** Identify the URI retrieval method used by the authentication code

| Retrieval Method | Safe? | Bypass Risk |
|----------|----------|----------|
| `request.getRequestURI()` | ❌ Unsafe | Can be bypassed with `;`, encoding, `../` |
| `request.getRequestURL()` | ❌ Unsafe | Same as above |
| `request.getServletPath()` | ✅ Relatively safe | Special characters already handled |
| `UrlPathHelper.getPathWithinApplication()` | ✅ Recommended | Spring standard method |
| `HandlerMapping.BEST_MATCHING_PATTERN_ATTRIBUTE` | ✅ Safest | Strongly tied to the Controller route |

**High-risk code pattern detection:**

```java
// ❌ Dangerous: directly using getRequestURI for authentication decisions
String uri = request.getRequestURI();
if (uri.endsWith(".js") || uri.endsWith(".css")) {
    chain.doFilter(request, response); // can be bypassed with /admin;.js
}

// ❌ Dangerous: using contains/endsWith for whitelist matching
if (uri.contains("/public/") || uri.startsWith("/static/")) {
    return true; // can be bypassed with /public/../admin
}
```

**Bypass principle:**

```
Request: GET /api/admin;.js

Authentication Filter uses: request.getRequestURI() → returns /api/admin;.js → matches the .js suffix → allows through
Route matching uses: request.getServletPath() → returns /api/admin → routes to the Controller

Result: the authentication check treats it as a static resource and allows it, but it is actually routed to the /api/admin endpoint
```

##### 6.1.2 Semicolon Path Parameter Bypass (;.js Family)

| Bypass Pattern | Payload Example | Principle |
|----------|-------------|------|
| Semicolon + static suffix | `/admin;.js`, `/admin;.css`, `/admin;.png` | Tomcat strips the content after the semicolon; the whitelist matches the suffix |
| Semicolon + path traversal | `/public;/../admin` | Combination of semicolon truncation + directory traversal |
| Semicolon + URL encoding | `/admin%3b.js` | URL-encoded semicolon |
| Semicolon + parameter | `/admin;bypass=true` | Path matrix parameter |
| Leading semicolon | `/;/admin` | Special handling by some parsers |

**Verification PoC:**

```http
# Semicolon suffix bypass (most common)
GET /center/api/users;.js HTTP/1.1
Host: {{host}}

# Semicolon + multiple suffixes
GET /center/api/users;.css HTTP/1.1
GET /center/api/users;.png HTTP/1.1
GET /center/api/users;.html HTTP/1.1

# Semicolon + URL encoding combination
GET /center/api/users%3b.js HTTP/1.1
Host: {{host}}

# Semicolon + path traversal
GET /public;/../admin/users HTTP/1.1
Host: {{host}}
```

##### 6.1.3 Path Normalization Difference Bypass

| Bypass Pattern | Detection Method | Risk |
|----------|----------|------|
| Path traversal | `/admin/../public`, `/public/../admin` | High |
| Double slash | `//admin`, `/api//users` | High |
| Dot slash | `/./admin`, `/api/./users` | High |
| URL-encoded slash | `/admin%2fusers`, `%2fadmin` | High |
| Double encoding | `/admin%252fusers` | High |
| Case bypass | `/ADMIN` vs `/admin` | Medium |
| Suffix bypass | `/admin.action` has no authentication but `/admin` does | High |
| Trailing slash | `/admin/` vs `/admin` | Medium |
| Parameter pollution | `?role=admin` overrides the user's role | High |
| Null byte | `/admin%00.jpg` | High |

##### 6.1.4 Data Flow Analysis (CRITICAL - Avoid False Positives)

**After finding a suspicious code pattern, you must perform data flow analysis to avoid false positives!**

**Background:** Reporting a vulnerability based solely on pattern matching (e.g. finding a `contains()` match) is not enough. You must trace the complete usage chain of the variable to determine whether the bypass is actually effective.

**Data flow analysis steps:**

```
Step 1: Identify the suspicious pattern
  └── Found isIgnoreUrl() using contains() matching

Step 2: Trace the variable usage chain
  └── How is the uri variable used after whitelist matching?
      ├── Only used for whitelist checks → continue analyzing the subsequent logic
      └── Also used for permission checks → analyze how the permission check handles uri

Step 3: Analyze the subsequent code logic
  └── For example, getActionPrefix(uri) takes the last segment
      → Path traversal does not affect the final permission decision
      → The bypass is ineffective!

Step 4: Draw a conclusion
  └── The whitelist can be bypassed, but the permission check is still effective
      → Lower the risk level or mark as "needs verification"
```

**Questions that must be answered:**

| Question | Analysis Focus |
|------|----------|
| How is the variable used afterward? | Trace all use points of uri after matching |
| What logic is executed after the bypass? | Analyze the complete code of each if/else branch |
| Is there a second check? | Check whether other security checks follow |
| Does path traversal affect the final result? | Analyze the path handling function (e.g. taking the last segment) |

**Example: incorrect vs correct analysis**

```java
// Code under audit
if (this.isIgnoreUrl(uri)) {
    chain.doFilter(request, response);  // whitelist pass-through
} else {
    if (privileges.contains(getActionPrefix(uri))) {  // permission check
        chain.doFilter(request, response);
    }
}

// getActionPrefix() implementation
public static String getActionPrefix(String uri) {
    String[] components = uri.split("/");
    return components[components.length - 1];  // takes the last segment!
}
```

| Analysis Approach | Conclusion | Correct? |
|----------|------|--------|
| ❌ Pattern matching | `contains()` can be bypassed via path traversal → report a high-risk vulnerability | Incorrect |
| ✅ Data flow analysis | After path traversal, `getActionPrefix()` still takes the last segment, so the permission check is unaffected → the bypass is ineffective | Correct |