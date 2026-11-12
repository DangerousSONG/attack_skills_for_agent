---
name: java-file-read-audit
description: "Java web source code auditing tool for arbitrary file read vulnerabilities. Identifies all file read operations in the source code and detects path traversal vulnerabilities. Suitable for (1) identifying file read frameworks and implementation patterns, (2) discovering arbitrary file read vulnerabilities, (3) detecting path traversal vulnerabilities, (4) auditing file path parameter validation logic. Supports BufferedReader, Scanner, Files.lines/readAllLines/readAllBytes and similar methods. **Supports decompiling .class/.jar files to extract file operation logic**. Combined with java-route-mapper it delivers a complete route + file read audit."
zh-signals: "审计 Java Web 源码中的文件读取操作，识别任意文件读取与路径遍历漏洞，并支持反编译 .class/.jar。信号:Java审计,任意文件读取,路径遍历,源码审计,反编译"
when-to-use: >-
  Use when auditing Java Web source or decompiled jars for arbitrary file read
  and path traversal vulnerabilities across all file read entry points.
---

# Java File Read Vulnerability Audit Tool

Inspect Java web project source code, identify file read implementations, and detect arbitrary file read and path traversal vulnerabilities.

## Core Requirements

**This skill must fully analyze all file read related code; no omissions are allowed.**

- ✅ Identify all file read entry points (BufferedReader/Scanner/Files)
- ✅ Analyze the path source of every file operation
- ✅ Detect all potential path traversal patterns
- ✅ Provide a verification PoC for each vulnerability point
- ❌ Never omit any file read operation
- ❌ Never skip the decompilation step

---

## Vulnerability Severity Rating Standard

**See [SEVERITY_RATING.md](../shared/SEVERITY_RATING.md) for details**

- Vulnerability ID format: `{C/H/M/L}-FILE-{sequence}`
- Severity Level = f(Reachability R, Impact Scope I, Exploitation Complexity C)
- Score = R × 0.40 + I × 0.35 + C × 0.25, mapped to CVSS 3.1

| Prefix | CVSS 3.1 | Meaning |
|------|----------|------|
| 🔴 **C** | 9.0-10.0 | Can directly lead to full system compromise |
| 🟠 **H** | 7.0-8.9 | Can cause major damage |
| 🟡 **M** | 4.0-6.9 | Can cause moderate damage |
| 🔵 **L** | 0.1-3.9 | Hardening recommendation |

---

## Skill Collaboration Workflow (CRITICAL)

**java-file-read-audit should run after java-route-mapper and audit based on the mapped route information.**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Complete Audit Flow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Step 1] java-route-mapper                                     │
│     │                                                           │
│     │ Output:                                                   │
│     │ ├─ List of all HTTP routes                                │
│     │ ├─ Parameter definition of each route                     │
│     │ │   ├─ Parameter name, type                                │
│     │ │   └─ Inner JSON fields                                   │
│     │ └─ Burp Suite request templates                           │
│     │                                                           │
│     ↓                                                           │
│  [Step 2] java-file-read-audit (this skill)                     │
│     │                                                           │
│     │ Input: the output of java-route-mapper                    │
│     │                                                           │
│     │ Execution:                                                 │
│     │ ├─ Quick scan of file operations                          │
│     │ ├─ Parameter-to-file-path mapping analysis                │
│     │ ├─ Check whether each String parameter is used as a path  │
│     │ └─ Execution condition analysis                           │
│     │                                                           │
│     ├─── Need deep tracing ───→ java-route-tracer               │
│     │                           │                               │
│     │    ←── Call chain info returned ──┘                       │
│     │                                                           │
│     ↓                                                           │
│  [Step 3] Output the consolidated audit report                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Input Dependencies (from java-route-mapper)

**Before starting the audit, you must first check whether a java-route-mapper output file already exists:**

```
{project_name}_audit/
├── route_mapper/
│   ├── {project_name}_route_mapper_{timestamp}.md    ← main index (read this file first to locate module details)
│   ├── {module_name}/
│   │   └── {project_name}_module_{module_name}_{timestamp}.md  ← module details
│   └── webservice/
│       └── {project_name}_ws_{service_name}_{timestamp}.md
└── file_read_audit/
    └── {project_name}_file_read_audit_{timestamp}.md  ← output of this skill
```

**If the route_mapper output does not exist, you must first run:**
```python
Skill(skill="java-route-mapper", args="--project {project_path}")
```

### Key Information Obtained from route_mapper

| Information | Purpose |
|:-----|:-----|
| Route path | Locate Controller/Action entry points |
| Parameter name + type | Identify high-risk String parameters |
| Inner JSON fields | Identify nested parameters (e.g. `fileInfo.path`) |
| Parameter purpose description | Determine whether it is used as a file path |

---

## Workflow (Three Phases)

### Stage 1: Quick Scan (execute first)

**Goal: quickly locate file read related code without missing any key point.**

```bash
# 1.1 Search for file read methods
grep -ri "BufferedReader\|FileReader\|FileInputStream" --include="*.java"
grep -ri "Scanner.*File\|Scanner.*Path" --include="*.java"
grep -ri "Files.lines\|Files.readAllLines\|Files.readAllBytes" --include="*.java"

# 1.2 Search for file download/read interfaces
grep -ri "download\|readFile\|getFile\|viewFile" --include="*.java"
grep -ri "@RequestMapping.*download\|@GetMapping.*download" --include="*.java"

# 1.3 Search for path concatenation patterns
grep -ri "new File.*\+" --include="*.java"
grep -ri "Paths.get.*\+" --include="*.java"
grep -ri "File.separator" --include="*.java"

# 1.4 Search for path parameters
grep -ri "filePath\|fileName\|file\|path" --include="*.java" | grep "@RequestParam\|@PathVariable"
```

**Output: list of high-risk files (sorted by priority)**

| Priority | File Type | Audit Focus |
|:-------|:---------|:---------|
| P0 | Methods containing download/readFile in `*Controller.java` | filePath, fileName parameters |
| P1 | `*Service.java`, `*ServiceImpl.java` | File path handling logic |
| P2 | `*Util.java`, `*Helper.java` | Generic file read methods |
| P3 | `*Dao.java`, `*Repository.java` | Configuration file reads |

### Stage 2: Parameter-to-File-Path Mapping Check

**Based on the java-route-mapper output, check whether each parameter is used as a file path.**

#### 2.1 High-Risk Parameter Identification

Extract all String type parameters from the route_mapper output:

| Parameter Source | Parameter Name | Type | File Read Vulnerability Likelihood |
|:---------|:-------|:-----|:-------------|
| @RequestParam | `filePath` | String | **High risk** - used directly as a path |
| @RequestParam | `fileName` | String | **High risk** - concatenated into a file name |
| @RequestParam | `file` | String | **High risk** - file path |
| @PathVariable | `path` | String | **High risk** - URL path parameter |
| JSON | `fileInfo.path` | String | **High risk** - inner JSON field |

#### 2.2 Parameter Tracing

For each high-risk parameter, trace its usage in the code:

```
HTTP parameter: filePath (String)
    ↓ passed to
Controller.download(filePath)
    ↓ passed to
Service.readFile(filePath)
    ↓ concatenated
basePath + File.separator + filePath
    ↓ used in
new FileInputStream(fullPath)  ← file read point
```

#### 2.3 File Read Point Check

For every file read point found in Stage 1, check:

1. **Is the file path controllable?**
   - Comes entirely from user input → high risk
   - Fixed base path + user supplied file name → medium risk
   - Fully hardcoded → safe

2. **Is there path validation?**
   - Whitelisted directory restriction → safe
   - File extension validation → may be bypassable
   - No validation → high risk

3. **Are path traversal characters filtered?**
   - Filters `../`, `..\\` → may be safe (bypasses must be tested)
   - No filtering → high risk

### Stage 3: In-Depth Check and Report

#### 3.1 Triggering java-route-tracer

When any of the following is found, call java-route-tracer to obtain the complete call chain:

| Trigger Condition | Invocation Method |
|:---------|:---------|
| The parameter passes through multiple layers | `Skill(skill="java-route-tracer", args="--route {route}")` |
| The path concatenation logic is complex | `Skill(skill="java-route-tracer", args="--route {route}")` |
| The validation logic is unclear | `Skill(skill="java-route-tracer", args="--route {route}")` |

#### 3.2 Execution Condition Check

After a file read is found, the execution conditions must be checked (see the following sections for details).

#### 3.3 Generate the Report

Consolidate all analysis results and generate a comprehensive audit report.

---

## File Read Method Identification

See [FILE_READ_METHODS.md](references/FILE_READ_METHODS.md) for detailed rules

| Method Category | Identification Feature | Risk Point |
|---------|----------|--------|
| BufferedReader | `new BufferedReader(new FileReader(path))` | Source of the path parameter |
| Scanner | `new Scanner(new FileReader(path))` | Source of the path parameter |
| Files.lines | `Files.lines(Path.of(path))` | Source of the path parameter |
| Files.readAllLines | `Files.readAllLines(Path.of(path))` | Source of the path parameter |
| Files.readAllBytes | `Files.readAllBytes(Path.of(path))` | Source of the path parameter |
| FileInputStream | `new FileInputStream(path)` | Source of the path parameter |

### Decompilation Phase (CRITICAL)

**When source code is unavailable, the MCP Java Decompiler must be used to decompile the file operation related classes.**

See [DECOMPILE_STRATEGY.md](references/DECOMPILE_STRATEGY.md) for the detailed strategy

#### Decompiler Tool Invocation

```python
# Decompile a single Controller/Service class
mcp__java-decompile-mcp__decompile_file(
    file_path="/path/to/FileController.class",
    output_dir="/path/to/decompiled",
    save_to_file=True
)

# Decompile a directory containing file operations
mcp__java-decompile-mcp__decompile_directory(
    directory_path="/path/to/WEB-INF/classes/com/example/controller",
    output_dir="/path/to/decompiled",
    recursive=True,
    save_to_file=True,
    max_workers=4
)

# Decompile multiple specified files
mcp__java-decompile-mcp__decompile_files(
    file_paths=[
        "/path/to/FileController.class",
        "/path/to/FileService.class",
        "/path/to/FileUtil.class"
    ],
    output_dir="/path/to/decompiled",
    save_to_file=True
)
```

**Output file naming convention:**
- Decompiled files are saved in the `{output_dir}` directory
- File name format: `{ClassName}.java`
- Preserve the original package structure: `com/example/controller/FileController.java`

#### Classes That Must Be Decompiled

| Type | Match Pattern | Purpose |
|------|----------|------|
| Controller | `*Controller.class` | Extract route and parameter definitions |
| Service | `*Service.class`, `*ServiceImpl.class` | Trace the file operation call chain |
| Utility class | `*FileUtil*.class`, `*FileHelper*.class` | Extract generic file read methods |
| DAO | `*Dao.class`, `*Repository.class` | Configuration file read logic |

---

## Execution Condition Check (CRITICAL - Avoiding False Positives)

**After finding file read code, you must check whether that code will actually be executed!**

### 1. Path Validation Check

After finding a file read, you must check whether path validation exists:

| Check Pattern | Code Feature | Handling |
|----------|----------|----------|
| Whitelisted directory | `path.startsWith("/upload/")` | Mark as a restricted path |
| Extension validation | `fileName.endsWith(".txt")` | Check whether it can be bypassed |
| Path canonicalization | `new File(path).getCanonicalPath()` | Check whether it is complete |
| No validation | Direct use of user input | Mark as high risk |

### 2. Code Path Reachability Analysis

Trace the complete path from the entry point to the file read and check:

| Check Item | Description | Impact |
|--------|------|------|
| Early return | `if (!validate()) return;` | May prevent execution |
| Exception thrown | `throw new SecurityException()` | Code does not execute |
| Unsatisfied condition | Dead code such as `if (false)` | Code does not execute |
| Permission restriction | Administrator-only access | Permissions must be confirmed |

### 3. Conclusion Rating (must be annotated)

| Status | Meaning | Follow-up Action |
|------|------|----------|
| ⚠️ **To be verified** | File read code exists but execution conditions are unconfirmed | Confirm the target environment |
| ✅ **Confirmed exploitable** | The code path was verified to execute with no effective validation | Proceed with exploitation testing |
| ❌ **Not exploitable** | Effective security validation is present | Annotate the reason and lower the priority |
| 🔍 **Environment dependent** | The vulnerability exists but is only exploitable under specific conditions | Annotate the environment conditions |

---

## Path Traversal Detection Rules Quick Reference

### ⚠️ High-Risk Pattern Detection (CRITICAL)

| Dangerous Pattern | Code Example | Risk Description |
|:---------|:---------|:---------|
| Direct concatenation | `basePath + fileName` | `../` is not filtered |
| File.separator concatenation | `basePath + File.separator + fileName` | Path traversal is possible |
| String formatting | `String.format("%s/%s", base, file)` | `../` is not filtered |
| Path.of concatenation | `Path.of(basePath, fileName)` | Path traversal is possible |
| Paths.get concatenation | `Paths.get(basePath).resolve(fileName)` | Canonicalization must be checked |

### ⚠️ Safe vs Dangerous Patterns

| Type | Dangerous Pattern | Safe Pattern |
|------|----------|----------|
| Path concatenation | `basePath + fileName` | Whitelist validation + canonicalization |
| File read | `new FileInputStream(userInput)` | `getCanonicalPath()` validation |
| Path traversal | No filtering of `../` | `path.contains("..")` interception |
| Extension | Not validated | Whitelisted extensions |

**Example of a safe pattern:**
```java
// Safe: path canonicalization + whitelisted directory validation
String basePath = "/var/uploads";
File file = new File(basePath, fileName);
String canonicalPath = file.getCanonicalPath();
if (!canonicalPath.startsWith(basePath)) {
    throw new SecurityException("Path traversal detected");
}
```

---

## Audit Checklist (to prevent omissions)

### Dangerous Patterns That Must Be Searched

**The following searches must be executed at the start of the audit:**

```bash
# File read method detection
grep -r "FileInputStream\|FileReader\|BufferedReader" --include="*.java"
grep -r "Files.readAllBytes\|Files.readAllLines\|Files.lines" --include="*.java"

# Path concatenation detection
grep -r "new File.*\+" --include="*.java"
grep -r "File.separator" --include="*.java"

# Download interface detection
grep -r "download\|readFile\|getFile" --include="*.java"
```

---

## Data Flow Tracing (load java-route-tracer when needed)

### When Parameter Tracing Is Needed

When any of the following is found, **the java-route-tracer skill must be loaded for deep tracing**:

| Scenario | Description | Operation |
|------|------|------|
| The parameter passes through multiple layers | An HTTP parameter passes through Controller → Service → Util layers and is then used as a file path | Load java-route-tracer |
| Path concatenation is complex | Multiple path concatenations and transformations | Load java-route-tracer |
| Validation logic is scattered | Validation logic is spread across different classes/methods | Load java-route-tracer |

---

## Report Generation

**Output a single comprehensive audit report file:**

```
{project_name}_audit/file_read_audit/
└── {route_name}/
    └── {project_name}_file_read_audit_{timestamp}.md      # comprehensive audit report
```

**Route Name Notes:**
- Route names are extracted from the route path, stripping leading slashes and special characters
- Example: `/api/file/download` → `api_file_download`
- Example: `/download.action` → `download`

---

## Output Format

**Generate the output file strictly following the fill-in template in [references/OUTPUT_TEMPLATE.md](references/OUTPUT_TEMPLATE.md).**

- File name format: `{project_name}_file_read_audit_{YYYYMMDD_HHMMSS}.md`
- Do not modify the template structure, add or remove sections, or change their order
- All [FILL IN] placeholders must be replaced with actual content
- Common specification reference: [shared/OUTPUT_STANDARD.md](../shared/OUTPUT_STANDARD.md)

---

## Verification Checklist

**Before marking the audit as complete, the following checks must be performed:**

### Code Analysis Check
- [ ] All Controller classes analyzed
- [ ] All Service/Util classes analyzed
- [ ] Every file operation annotated with its path source

### Execution Condition Check (CRITICAL)
- [ ] Path validation logic checked
- [ ] Code path reachability checked
- [ ] Exploitability status annotated for each vulnerability

### Vulnerability Detection Check
- [ ] All file read methods detected
- [ ] All path concatenation patterns detected
- [ ] All parameter sources traced

### Report Completeness Check
- [ ] **The comprehensive audit report has been generated and passes the self-check checklist at the end of OUTPUT_TEMPLATE.md**
- [ ] **Decompiled output file paths annotated**

---

## References

- [OUTPUT_TEMPLATE.md](references/OUTPUT_TEMPLATE.md) - Fill-in template for the output report
- [FILE_READ_METHODS.md](references/FILE_READ_METHODS.md) - Detailed guide to Java file read methods
- [PATH_TRAVERSAL.md](references/PATH_TRAVERSAL.md) - Detailed guide to path traversal attacks
- [DECOMPILE_STRATEGY.md](references/DECOMPILE_STRATEGY.md) - Decompilation strategy guide
