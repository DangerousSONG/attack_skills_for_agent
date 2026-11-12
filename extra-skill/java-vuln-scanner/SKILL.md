---
name: java-vuln-scanner
description: "Java component version vulnerability detection tool. Scans third-party dependencies in pom.xml, build.gradle, or jar files, matches known vulnerability rules (CVEs), and generates a vulnerability detection report. Applicable to: (1) Java project dependency security audits, (2) identifying high-risk component vulnerabilities such as Log4j, Fastjson, Shiro, and Spring, (3) dependency extraction after decompiling jar packages. Supports grouped output by directory hierarchy, and supports extracting dependency information from .class/.jar files via java-decompile-mcp decompilation."
zh-signals: "扫描 Java 项目依赖（pom.xml、build.gradle、jar）匹配已知 CVE，识别 Log4j、Fastjson、Shiro、Spring 等高危组件漏洞。信号:Java漏洞扫描,组件漏洞,CVE,依赖审计,反编译"
when-to-use: >-
  Use when auditing a Java project's third-party dependencies for known CVEs,
  including decompiled jar/class files, across Maven or Gradle projects.
---

# Java Component Vulnerability Scanner

Scans Java project dependencies for known vulnerabilities, supporting 130+ CVE rules, outputting grouped by module, with AI-generated vulnerability trigger-point check results.

## Workflow

### 1. Determine the Scan Target

Supported input types:
- `pom.xml` - Maven project
- `build.gradle` - Gradle project
- `.jar` file - extract dependency information from the file name or META-INF
- Directory - recursively scan all of the above, grouping by module automatically

### 2. Process jar/class Files (when decompilation is needed)

When the target is a `.jar` or `.class` file and dependency information cannot be extracted directly, use the `java-decompile-mcp` tool to decompile:

```
# Decompile a single file
mcp__java-decompile-mcp__decompile_file(file_path="/path/to/file.jar")

# Decompile a directory
mcp__java-decompile-mcp__decompile_directory(directory_path="/path/to/classes")
```

### 3. Execute the Vulnerability Scan

Run the scan script; the report is saved automatically to the `{project-name}_audit/vuln_report/` directory:

```bash
python3 scripts/scan_dependencies.py <target-path> \
  --rules references/java-vulnerability.yaml \
  --no-deps
```

Parameter descriptions:
- `<target-path>`: pom.xml, build.gradle, jar file, or directory
- `--rules/-r`: path to the vulnerability rule file (use the built-in rules)
- `--format/-f`: output format (markdown/json)
- `--output/-o`: specify the output path (auto-generated when not specified)
- `--depth/-d`: module grouping depth (default: 2)
- `--no-deps`: do not show the dependency list (simplified output)
- `--no-save`: output to the terminal only, do not save the file

### 4. Review the Scan Results

The report is grouped by module, and each module is categorized by severity level:
- 🔴 **Critical**: fix immediately (Log4Shell, Fastjson RCE, Shiro deserialization, etc.)
- 🟠 **High**: fix as soon as possible (Spring Boot Actuator, XStream, etc.)
- 🟡 **Medium**: plan a fix (JDBC driver vulnerabilities, Guava, etc.)
- 🔵 **Low**: upgrading is recommended (outdated components)

### 5. AI Vulnerability Trigger-Point Analysis (important)

After the scan completes, you **must** produce a complete report (a **single file**) based on the scan results, following the `references/OUTPUT_TEMPLATE.md` template.

#### Analysis Steps

1. Read the scan results produced by the Python script
2. **Identify the project runtime environment**:
   - Check the framework used by the project: Spring MVC / Spring Boot / Struts2 / Servlet / JAX-RS, etc.
   - Check the container type: Tomcat / Jetty / Undertow / WebLogic / WildFly, etc.
   - Locate configuration files: `web.xml`, `struts.xml`, `application.yml`, `applicationContext.xml`, etc.
3. **Extract routes and entry points**:
   - Scan Controller / Action / Servlet classes and extract the HTTP route mappings
   - Identify key entry points such as file upload, JSON/XML parsing, and user input handling
   - Combine with the java-route-mapper skill (if already loaded) to get complete route information
4. Extract the list of **unique vulnerable components** detected (deduplicated)
5. **Fill in the report according to the template**; each vulnerability's detail block must contain:
   - Trigger conditions
   - Dangerous code patterns (java code block)
   - Attack vectors
   - Affected routes/APIs
   - Code search commands (bash code block)
   - Remediation recommendations
6. Use the Write tool to write the complete report into a **single file**

#### Environment Identification Methods

Identify the project environment based on the following indicators (referencing the identification strategy of the java-route-mapper skill):

**Web framework identification:**

| Framework | Identification Indicators | Configuration Files | Key Dependencies |
|------|---------|---------|---------|
| Spring MVC | `@Controller`, `@RequestMapping`, `@RestController` | `dispatcher-servlet.xml`, `spring-mvc.xml` | `spring-webmvc.jar` |
| Spring Boot | `@SpringBootApplication`, Spring Boot starter | `application.properties`, `application.yml` | `spring-boot-starter-*.jar` |
| Struts 2 | `ActionSupport`, `\<action\>` configuration | `struts.xml`, `struts-plugin.xml` | `struts2-core.jar` |
| Servlet | `HttpServlet`, `@WebServlet`, `\<servlet\>` configuration | `web.xml` | `javax.servlet-api.jar` |
| JAX-RS | `@Path`, `@GET`, `@POST`, `@PathParam` | `web.xml` (REST servlet mapping) | `jersey-*.jar`, `cxf-rt-*.jar` |
| CXF Web Services | `@WebService`, `\<jaxws:endpoint\>` | `applicationContext.xml`, `cxf-servlet.xml` | `cxf-*.jar` |

**Container identification:**

| Container | Identification Indicators | Configuration Files |
|------|---------|---------|
| Tomcat | `catalina.jar`, `org.apache.catalina` | `server.xml`, `context.xml` |
| Jetty | `jetty-*.jar`, `org.eclipse.jetty` | `jetty.xml`, `webdefault.xml` |
| Undertow | `undertow-*.jar`, `io.undertow` | `undertow-handlers.conf` |
| WebLogic | `weblogic.jar`, `weblogic.xml` | `weblogic.xml`, `weblogic-application.xml` |
| WildFly/JBoss | `jboss-*.jar`, `org.jboss` | `jboss-web.xml`, `standalone.xml` |

**Framework combination identification:**

Projects mixing multiple frameworks require separate identification and checks:
- Struts2 + Spring: check `struts-spring-plugin.jar` and the Spring configuration
- Spring MVC + CXF: check whether `\<jaxws:endpoint\>` and `@Controller` coexist
- Servlet + Filter chain: check the filter-mapping order in `web.xml`

## Vulnerability Rule Coverage

The rule file `references/java-vulnerability.yaml` contains 130+ rules covering:

| Component Category | Main Vulnerabilities |
|---------|---------|
| Log4j | CVE-2021-44228 (Log4Shell), CVE-2021-45046 |
| Fastjson | CVE-2022-25845, CVE-2017-18349 |
| Spring | CVE-2022-22965 (Spring4Shell), CVE-2022-22963 |
| Struts2 | S2-045, S2-046, S2-057, S2-061 |
| Shiro | CVE-2016-4437, CVE-2020-11989, CVE-2020-17510 |
| Jackson | CVE-2020-36518, CVE-2019-12384 |
| XStream | CVE-2021-39144 and 15 other CVEs |
| ActiveMQ | CVE-2023-46604 |
| JDBC drivers | MySQL, PostgreSQL, H2, Derby, etc. |

## Examples

### Complete Scan Workflow

```bash
# 1. Execute the scan
python3 scripts/scan_dependencies.py /path/to/webapp \
  --rules references/java-vulnerability.yaml \
  --no-deps

# 2. Example output:
# [INFO] Created output directory: webapp_audit/vuln_report
# [INFO] Report saved to: webapp_audit/vuln_report/webapp_vuln_report_20260204_101747.md
# 📊 Scan summary:
#    Module count: 4
#    Total dependencies: 262
#    Total vulnerabilities: 80
#    🔴 Critical: 24

# 3. AI automatically reads the report and appends the trigger-point check results
```

### Output Report Structure

> **Output constraints (must not be violated):**
> 1. **Output as a single file** — must not be split into multiple files
> 2. File naming format: `{project_name}_vuln_report_{YYYYMMDD_HHMMSS}.md`
> 3. Must strictly follow the `references/OUTPUT_TEMPLATE.md` template
> 4. Sections must not be added or removed, and the section order must not be changed

**Output template**: [references/OUTPUT_TEMPLATE.md](references/OUTPUT_TEMPLATE.md)

```
{project_name}_audit/vuln_report/
└── {project_name}_vuln_report_{YYYYMMDD_HHMMSS}.md   ← this single file only
    ├── 1. Scan Overview
    ├── 2. Risk Statistics
    ├── 3. Component Vulnerability Mapping Table
    ├── 4. Vulnerability Details (trigger conditions, dangerous code, attack vectors, search commands)
    └── 5. Audit Conclusion
```

Refer to the general output standard: [shared/OUTPUT_STANDARD.md](../shared/OUTPUT_STANDARD.md)
