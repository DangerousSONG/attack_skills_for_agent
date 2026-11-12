---
name: java-file-upload-audit
description: "Java Web source code file upload vulnerability auditing tool. Used to identify every file upload entry point in the source code and check the upload path, filename handling, and validation logic for vulnerabilities. Applicable to: (1) identifying Servlet/Commons FileUpload and Spring Boot MultipartFile upload implementations, (2) discovering arbitrary file upload, path traversal, and executable file upload vulnerabilities, (3) checking whether filename/directory/type/size validation is missing or bypassable, (4) auditing upload directories and access control. **Supports decompiling .class/.jar files to extract upload logic**. Combined with java-route-mapper it enables a complete route + file upload audit."
zh-signals: "审计 Java Web 源码中的文件上传入口，检查任意上传、路径穿越、类型校验与目录访问控制漏洞。信号:Java,文件上传,源码审计,路径穿越,反编译"
when-to-use: "Use when auditing Java Web source (Servlet/Commons FileUpload or Spring MultipartFile) for file-upload vulnerabilities, including decompiling .class/.jar files when source is unavailable."
---

# Java File Upload Vulnerability Auditing Tool

Inspect Java Web project source code, identify file upload implementations, and detect upload-related vulnerabilities (arbitrary file upload, path traversal, file overwrite, web-root executability, etc.).

## Core Requirements

**This skill must fully analyze all upload-related code; omissions are not allowed.**

- ✅ Identify all upload entry points (ServletFileUpload / MultipartFile / transferTo / FileItem)
- ✅ Annotate the save path, filename origin, and validation strategy of each upload point
- ✅ Detect all potential upload vulnerability patterns (missing type validation, path traversal, web root writes, file overwrite)
- ✅ When source code is unavailable, decompilation is mandatory, and a decompiled file list (file name + location) must be output
- ❌ Never omit any upload entry point
- ❌ Never skip the decompilation step

---

## Vulnerability Severity Rating Standard

**See [SEVERITY_RATING.md](../shared/SEVERITY_RATING.md) for details**

- Vulnerability ID format: `{C/H/M/L}-UPLOAD-{sequence number}`
- Severity Level = f(Reachability R, Impact Scope I, Exploitation Complexity C)
- Score = R × 0.40 + I × 0.35 + C × 0.25, mapped to CVSS 3.1

| Prefix | CVSS 3.1 | Meaning |
|------|----------|------|
| 🔴 **C** | 9.0-10.0 | Can directly lead to full system compromise |
| 🟠 **H** | 7.0-8.9 | Can cause major damage |
| 🟡 **M** | 4.0-6.9 | Can cause moderate damage |
| 🔵 **L** | 0.1-3.9 | Hardening item |

---

## Skill Collaboration Workflow (CRITICAL)

**java-file-upload-audit must run after java-route-mapper and audit based on the already-mapped route information.**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Complete Audit Flow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Step 1] java-route-mapper                                     │
│     │                                                           │
│     │ Output:                                                   │
│     │ ├─ Full list of HTTP routes                               │
│     │ ├─ Parameter definitions for each route                   │
│     │ │   ├─ Parameter name, type                               │
│     │ │   └─ Inner JSON fields                                  │
│     │ └─ Burp Suite request templates                           │
│     │                                                           │
│     ↓                                                           │
│  [Step 2] java-file-upload-audit (this skill)                   │
│     │                                                           │
│     │ Input: output of java-route-mapper                        │
│     │                                                           │
│     │ Actions:                                                  │
│     │ ├─ Quick scan for upload implementations                  │
│     │ ├─ Parameter-to-upload mapping analysis                   │
│     │ ├─ Validation logic and save path analysis                │
│     │ └─ Execution condition analysis                           │
│     │                                                           │
│     ├─── Deep tracing needed ───→ java-route-tracer             │
│     │                           │                               │
│     │    ←── call chain info returned ──┘                       │
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
│   ├── {project_name}_route_mapper_{timestamp}.md    ← main index (read this first to locate module details)
│   ├── {module_name}/
│   │   └── {project_name}_module_{module_name}_{timestamp}.md  ← module details
│   └── webservice/
│       └── {project_name}_ws_{service_name}_{timestamp}.md
└── file_upload_audit/
    └── {project_name}_file_upload_audit_{timestamp}.md  ← output of this skill
```

**If the route_mapper output does not exist, it is recommended to run first:**
```python
Skill(skill="java-route-mapper", args="--project {project_path}")
```

### Key Information Obtained from route_mapper

| Information | Purpose |
|:-----|:-----|
| Route path | Locate upload Controller/Servlet entry points |
| Parameter name + type | Identify MultipartFile / FileItem / fileName parameters |
| Inner JSON fields | Identify nested upload parameters |
| Parameter purpose description | Determine whether it is used for the filename or the save path |

---

## Workflow (Three Phases)

### Stage 1: Quick Scan (execute first)

**Goal: quickly locate upload-related code without missing any key point.**

```bash
# 1.1 Servlet/Commons FileUpload
rg -n "ServletFileUpload|DiskFileItemFactory|FileItem|isMultipartContent" --glob="*.java"

# 1.2 Spring Boot MultipartFile
rg -n "MultipartFile|@RequestParam\\(\"file\"\\)|transferTo\\(" --glob="*.java"

# 1.3 Filename/path related
rg -n "getOriginalFilename|getName\\(\\)|getRealPath\\(\"/uploads\"\\)|uploadDir" --glob="*.java"
rg -n "new File\\(|Paths\\.get\\(|Path\\.of\\(|File\\.separator" --glob="*.java"

# 1.4 Upload interface routes
rg -n "@PostMapping\\(|@RequestMapping\\(.*upload|/upload" --glob="*.java"
```

**Output: list of high-risk files (sorted by priority)**

| Priority | File Type | Audit Focus |
|:-------|:---------|:---------|
| P0 | `*Controller.java` / `*Servlet.java` containing upload logic | MultipartFile/FileItem |
| P1 | `*Service.java`, `*ServiceImpl.java` | File save path/renaming |
| P2 | `*Util.java`, `*Storage.java`, `*File*.java` | Generic storage wrappers |
| P3 | `*Config.java`, `application.yml` | File size/directory configuration |

### Stage 2: Parameter-to-Upload Mapping Analysis

**Based on the route_mapper output, check whether each upload parameter influences the filename or the save path.**

#### 2.1 High-Risk Parameter Identification

| Parameter Source | Parameter Name | Type | Vulnerability Level |
|:---------|:-------|:-----|:-----|
| @RequestParam | `file` | MultipartFile | **High** - direct upload |
| FileItem | `item` | FileItem | **High** - fileName controllable |
| @RequestParam | `fileName` | String | **High** - filename concatenation |
| JSON | `upload.path` | String | **High** - directory concatenation |

#### 2.2 Parameter Tracing (example)

```
HTTP parameter: file (MultipartFile)
    ↓
Controller.handleFileUpload(file)
    ↓
file.getOriginalFilename()  ← filename origin
    ↓
Paths.get(uploadDir).resolve(fileName)
    ↓
file.transferTo(filePath)   ← upload write point
```

#### 2.3 Upload Point Checks

For each upload write point, check:

1. **Is the filename source controllable?**
   - `getOriginalFilename()` / `item.getName()` → High
   - Server-generated random name → Low

2. **Is there path normalization and directory restriction?**
   - `getCanonicalPath()` + fixed upload directory → relatively safe
   - Direct path concatenation → High

3. **Is type/content validation performed?**
   - Extension whitelist/Content-Type/magic number validation → safe
   - Only a non-empty check or no validation → High

4. **Is the upload directory inside the web root?**
   - `getRealPath("/uploads")` / `/uploads/` → High
   - Directory not accessible from the web → relatively safe

### Stage 3: Deep Review and Reporting

When the upload logic is complex or parameters are passed through multiple layers, call java-route-tracer to obtain the complete call chain and supplement the validation path analysis.

---

## Upload Implementation Identification (key points from the Notion material)

### 1) Servlet/Commons FileUpload

**Identification features:**
- `ServletFileUpload.isMultipartContent(request)`
- `DiskFileItemFactory` / `ServletFileUpload`
- `upload.parseRequest(request)` → `List<FileItem>`
- `item.getName()` used as the filename
- `item.write(storeFile)` writes the file
- `getServletContext().getRealPath("/uploads")` used as the save directory

**Notion notes:**
- The example does not validate the form field name, so `name="file"` **is not checked**.
- Only a size limit is set (e.g. `upload.setSizeMax(5MB)`); no extension/type/path validation is visible.

### 2) Spring Boot MultipartFile

**Identification features:**
- `@RequestParam("file") MultipartFile file`
- `file.getOriginalFilename()`
- `file.transferTo(filePath)`
- Fixed upload directory `uploadDir = "/uploads/"`

**Notion notes:**
- `@RequestParam("file")` does validate the form field name, so `name="file"` is required.
- The example shows no filename sanitization, type whitelist, or directory isolation.

**See [UPLOAD_RULES.md](references/UPLOAD_RULES.md) for detailed detection rules**

---

## Decompilation Phase (CRITICAL)

**When source code is unavailable, the MCP Java Decompiler must be used to decompile upload-related classes.**

### Decompiler Tool Invocation

```python
# Decompile a single upload-related class
mcp__java-decompile-mcp__decompile_file(
    file_path="/path/to/UploadController.class",
    output_dir="/path/to/decompiled",
    save_to_file=True
)

# Decompile an upload-related directory
mcp__java-decompile-mcp__decompile_directory(
    directory_path="/path/to/WEB-INF/classes/com/example/upload",
    output_dir="/path/to/decompiled",
    recursive=True,
    save_to_file=True,
    max_workers=4
)

# Decompile multiple specified files
mcp__java-decompile-mcp__decompile_files(
    file_paths=[
        "/path/to/UploadController.class",
        "/path/to/FileStorageService.class",
        "/path/to/UploadUtil.class"
    ],
    output_dir="/path/to/decompiled",
    save_to_file=True
)
```

### Classes That Must Be Decompiled

| Type | Match Pattern | Purpose |
|------|----------|------|
| Controller/Servlet | `*Upload*Controller.class`, `*Servlet.class` | Extract upload entry points |
| Service/Storage | `*Storage*.class`, `*FileService*.class` | Trace save paths |
| Utility classes | `*UploadUtil*.class`, `*FileUtil*.class` | Find generic validation |
| Configuration classes | `*Config*.class` | Obtain upload directory/size limits |

**Decompilation output requirements:**
- Output a "decompiled file list" containing the original file names and the decompiled output paths
- Decompiled file paths must be locatable to a specific directory

---

## Execution Condition Analysis (CRITICAL - avoid false positives)

**After finding upload logic, you must check whether that logic will actually be executed!**

| Check Item | Description | Impact |
|--------|------|------|
| Permission check | Only administrators can access | Affects exploitability |
| Parameter validation | Field name/type/size validation | Reduces vulnerability exploitability |
| Directory restriction | Fixed upload directory | Reduces path traversal |
| Accessibility | Whether the upload directory is web accessible | Determines whether the file is executable |

Conclusion ratings must be labeled: ✅ confirmed exploitable / ⚠️ pending verification / ❌ not exploitable / 🔍 environment dependent

---

## Report Generation

**Output a single comprehensive audit report file:**

```
{project_name}_audit/file_upload_audit/
└── {route_name}/
    └── {project_name}_file_upload_audit_{timestamp}.md
```

**Route Name Notes:**
- Route names are extracted from the route path, stripping leading slashes and special characters
- Example: `/api/file/upload` → `api_file_upload`

---

## Output Format

**Generate the output file strictly following the fill-in template in [references/OUTPUT_TEMPLATE.md](references/OUTPUT_TEMPLATE.md).**

- File name format: `{project_name}_file_upload_audit_{YYYYMMDD_HHMMSS}.md`
- Do not modify the template structure, add or remove sections, or change their order
- All [FILL IN] placeholders must be replaced with actual content
- Common specification reference: [shared/OUTPUT_STANDARD.md](../shared/OUTPUT_STANDARD.md)

---

## Audit Checklist (to prevent omissions)

### Code Analysis Check
- [ ] All upload entry points have been analyzed (Servlet/MultipartFile)
- [ ] Filename origin and save path are annotated for every upload point
- [ ] Directory and access control have been analyzed

### Decompilation Check
- [ ] Decompilation has been performed when the source code is unavailable
- [ ] The decompiled file list has been output (file name + location)

### Report Completeness Check
- [ ] **The comprehensive audit report has been generated and passes the self-check checklist at the end of OUTPUT_TEMPLATE.md**

---

## References

- [OUTPUT_TEMPLATE.md](references/OUTPUT_TEMPLATE.md) - Fill-in template for the output report
- [UPLOAD_RULES.md](references/UPLOAD_RULES.md) - Upload implementation identification and risk rules
