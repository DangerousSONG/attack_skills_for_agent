---
name: java-xxe-audit
description: "Java Web source code XXE (XML External Entity) vulnerability auditing tool. Identifies all XML parsing operations in the source code and detects external entity injection vulnerabilities. Applicable to: (1) identifying XML parser types and implementations, (2) discovering XXE injection vulnerabilities, (3) checking external entity protection configuration, (4) auditing XML input sources and echo logic. Supports five mainstream parsers: XMLReader, SAXBuilder, SAXReader, SAXParserFactory, DocumentBuilderFactory. **Supports decompiling .class/.jar files to extract XML parsing logic**. Combined with java-route-mapper, it delivers a complete route + XXE audit."
zh-signals: "审计 Java Web 源码中的 XXE 漏洞，识别 XML 解析器并检查外部实体防护。信号:xxe,java审计,xml解析,外部实体,反编译"
when-to-use: >-
  Use when auditing Java web source code for XML External Entity injection, including
  identifying parser types and checking for external entity protections.
---

# Java XXE Vulnerability Auditing Tool

Inspect Java web project source code, identify XML parsing implementations, and detect XXE (XML External Entity) injection vulnerabilities.

## Core Requirements

**This skill must inspect every XML-parsing-related piece of code; omitting anything is not allowed.**

- ✅ Identify all XML parsing entry points (5 parser families)
- ✅ Check the external entity protection configuration of every parser
- ✅ Trace XML input sources (user controllability)
- ✅ Detect echo points (whether data is returned to the user)
- ✅ Provide a verification PoC for each vulnerability point
- ❌ Omitting any XML parsing operation is forbidden
- ❌ Never skip the decompilation step

---

## Vulnerability Severity Rating Standard

**See [SEVERITY_RATING.md](../shared/SEVERITY_RATING.md) for details**

- Vulnerability ID format: `{C/H/M/L}-XXE-{sequence-number}`
- Severity Level = f(Reachability R, Impact Scope I, Exploitation Complexity C)
- Score = R × 0.40 + I × 0.35 + C × 0.25, mapped to CVSS 3.1

| Prefix | CVSS 3.1 | Meaning |
|------|----------|------|
| 🔴 **C** | 9.0-10.0 | Can directly lead to full system compromise |
| 🟠 **H** | 7.0-8.9 | Can cause major damage |
| 🟡 **M** | 4.0-6.9 | Can cause moderate damage |
| 🔵 **L** | 0.1-3.9 | Security hardening item |

---

## Skill Collaboration Workflow (CRITICAL)

**java-xxe-audit must run after java-route-mapper, auditing based on the route information already mapped.**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Complete audit flow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Step 1] java-route-mapper                                     │
│     │                                                           │
│     │ Output:                                                   │
│     │ ├─ Full HTTP route list                                   │
│     │ ├─ Parameter definition for each route                    │
│     │ └─ Content-Type identification (application/xml, text/xml)│
│     │                                                           │
│     ↓                                                           │
│  [Step 2] java-xxe-audit (this skill)                           │
│     │                                                           │
│     │ Input: the output of java-route-mapper                    │
│     │                                                           │
│     │ Performs:                                                 │
│     │ ├─ Quick scan for XML parsing classes                     │
│     │ ├─ Check parser security configuration                    │
│     │ ├─ Trace XML input sources                                │
│     │ └─ Check echo paths                                        │
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
└── xxe_audit/
    └── {project_name}_xxe_audit_{timestamp}.md  ← output of this skill
```

**If the route_mapper output does not exist, you must first run:**
```python
Skill(skill="java-route-mapper", args="--project {project_path}")
```

### Key Information Obtained from route_mapper

| Information | Purpose |
|:-----|:-----|
| Route path | Locate Controller/Servlet entry points |
| Content-Type | Identify endpoints that accept XML input |
| Parameter source | Identify raw input such as getInputStream() |
| Request method | POST methods are more likely to accept an XML body |

---

## Workflow (Three Phases)

### Stage 1: Quick Scan (execute first)

**Goal: quickly locate all XML parsing points and high-risk files.**

```bash
# 1.1 Search for XML parser instantiation
grep -ri "XMLReaderFactory.createXMLReader" --include="*.java"
grep -ri "new SAXBuilder" --include="*.java"
grep -ri "new SAXReader" --include="*.java"
grep -ri "SAXParserFactory.newInstance" --include="*.java"
grep -ri "DocumentBuilderFactory.newInstance" --include="*.java"

# 1.2 Search for XML parsing execution points
grep -ri "\.parse\s*(" --include="*.java"
grep -ri "\.build\s*(" --include="*.java"
grep -ri "\.read\s*(" --include="*.java"

# 1.3 Search for XML input sources
grep -ri "getInputStream" --include="*.java"
grep -ri "InputSource" --include="*.java"
grep -ri "StringReader" --include="*.java"
grep -ri "StreamSource" --include="*.java"

# 1.4 Search for security configuration (to determine whether protection is already in place)
grep -ri "disallow-doctype-decl" --include="*.java"
grep -ri "external-general-entities" --include="*.java"
grep -ri "external-parameter-entities" --include="*.java"
grep -ri "setFeature" --include="*.java"
grep -ri "setExpandEntityReferences" --include="*.java"

# 1.5 Search for other XML-related classes
grep -ri "TransformerFactory" --include="*.java"
grep -ri "SchemaFactory" --include="*.java"
grep -ri "XMLInputFactory" --include="*.java"
grep -ri "Unmarshaller\|JAXBContext" --include="*.java"
```

**Output: list of high-risk files (sorted by priority)**

| Priority | File Type | Audit Focus |
|:-------|:---------|:---------|
| P0 | Directly uses `getInputStream()` + XML parsing | User-controlled XML parsed directly |
| P1 | XML handling in Servlet/Controller | XML parsing at the HTTP entry point |
| P2 | XML utility classes `*XmlUtil*.java` | Generic XML parsing methods |
| P3 | WebService/SOAP handling classes | SOAP XML parsing |

### Stage 2: Parser Security Configuration Check

**For every XML parsing point found in Stage 1, check the security configuration state one by one.**

#### 2.1 Parser Identification and Configuration Check

For each parser instance, check whether the following protective features are set:

| Protective Feature | Feature URI | Purpose |
|:---------|:------------|:-----|
| Disallow DOCTYPE | `http://apache.org/xml/features/disallow-doctype-decl` | **Strictest, recommended** |
| Disallow external general entities | `http://xml.org/sax/features/external-general-entities` | Disable external entity references |
| Disallow external parameter entities | `http://xml.org/sax/features/external-parameter-entities` | Disable parameter entities |
| Disallow external DTD loading | `http://apache.org/xml/features/nonvalidating/load-external-dtd` | Prohibit loading external DTDs |

For detailed detection rules, see the per-parser reference documents:

| Parser | Reference |
|--------|----------|
| XMLReader | [PARSERS.md - XMLReader section](references/PARSERS.md#1-xmlreader) |
| SAXBuilder (JDOM2) | [PARSERS.md - SAXBuilder section](references/PARSERS.md#2-saxbuilder-jdom2) |
| SAXReader (dom4j) | [PARSERS.md - SAXReader section](references/PARSERS.md#3-saxreader-dom4j) |
| SAXParserFactory | [PARSERS.md - SAXParserFactory section](references/PARSERS.md#4-saxparserfactory) |
| DocumentBuilderFactory | [PARSERS.md - DocumentBuilderFactory section](references/PARSERS.md#5-documentbuilderfactory) |

#### 2.2 Tracing XML Input Sources

For each XML parsing point, trace the input source:

```
HTTP request body: request.getInputStream()
     ↓
InputSource / StringReader / StreamSource
     ↓
XMLReader.parse() / SAXBuilder.build() / SAXReader.read() / ...
     ↓
Parse result: Document / Element / Node
     ↓
Echo: response.getWriter().write() / model.addAttribute() / ...
```

| Input Source | User Controllability | Risk Level |
|:---------|:-----------|:---------|
| `request.getInputStream()` | **Fully controllable** | High |
| `request.getParameter("xml")` | **Fully controllable** | High |
| `@RequestBody String xml` | **Fully controllable** | High |
| `MultipartFile.getInputStream()` | **Fully controllable** | High |
| XML field read from a database | Indirectly controllable | Medium |
| Configuration file / hardcoded XML | Not controllable | Low |

#### 2.3 Echo Path Check

The XXE exploitation technique depends on whether an echo exists:

| Echo Mechanism | Exploitation Type | Detection Method |
|:---------|:---------|:---------|
| Parse result written to the HTTP response | **XXE with echo** | Search `response.getWriter()`, `getText()`, `getTextContent()` |
| Parse result written to the page model | **XXE with echo** | Search `model.addAttribute()`, `request.setAttribute()` |
| Parse result only used for logic processing | **Blind XXE (OOB)** | Exfiltration is required via an external DTD |
| Parsed but never output | **Blind XXE (OOB)** | Exfiltration is required via an external DTD |

### Stage 3: Detailed Detection and Reporting

#### 3.1 Triggering java-route-tracer

When any of the following is found, call java-route-tracer to obtain the complete call chain:

| Trigger Condition | Invocation Method |
|:---------|:---------|
| XML input passes through multiple layers | `Skill(skill="java-route-tracer", args="--route {route}")` |
| The parser lives in a utility class or base class | `Skill(skill="java-route-tracer", args="--route {route}")` |
| The echo path is unclear | `Skill(skill="java-route-tracer", args="--route {route}")` |

#### 3.2 Generating the Report

Consolidate all detection results and generate a comprehensive audit report.

---

## XML Parser Identification

| Parser | Identification Signature | Package/Dependency | Reference |
|--------|----------|-------------|----------|
| XMLReader | `XMLReaderFactory.createXMLReader()`, `xmlReader.parse()` | `org.xml.sax` (JDK built-in) | [PARSERS.md](references/PARSERS.md) |
| SAXBuilder | `new SAXBuilder()`, `saxBuilder.build()` | `org.jdom2` (jdom2) | [PARSERS.md](references/PARSERS.md) |
| SAXReader | `new SAXReader()`, `reader.read()` | `org.dom4j.io` (dom4j) | [PARSERS.md](references/PARSERS.md) |
| SAXParserFactory | `SAXParserFactory.newInstance()`, `.getXMLReader().parse()` | `javax.xml.parsers` (JDK built-in) | [PARSERS.md](references/PARSERS.md) |
| DocumentBuilderFactory | `DocumentBuilderFactory.newInstance()`, `builder.parse()` | `javax.xml.parsers` (JDK built-in) | [PARSERS.md](references/PARSERS.md) |

### Other Components That May Be Affected by XXE

| Component | Identification Signature | Vulnerability Notes |
|------|----------|----------|
| TransformerFactory | `TransformerFactory.newInstance()` | XSLT processing can trigger XXE |
| SchemaFactory | `SchemaFactory.newInstance()` | XML Schema validation can trigger XXE |
| XMLInputFactory (StAX) | `XMLInputFactory.newInstance()` | StAX parsers can trigger XXE |
| JAXB Unmarshaller | `JAXBContext.newInstance()`, `unmarshaller.unmarshal()` | XML deserialization can trigger XXE |

---

## Decompilation Stage (CRITICAL)

**When the source code is unavailable, you must use MCP Java Decompiler to decompile the XML-parsing-related classes.**

See [DECOMPILE_STRATEGY.md](references/DECOMPILE_STRATEGY.md) for the detailed strategy

### Decompiler Tool Invocation

```python
# Decompile a single XML handling class
mcp__java-decompile-mcp__decompile_file(
    file_path="/path/to/XmlParser.class",
    output_dir="/path/to/decompiled",
    save_to_file=True
)

# Decompile a directory containing XML handling code
mcp__java-decompile-mcp__decompile_directory(
    directory_path="/path/to/WEB-INF/classes/com/example/util",
    output_dir="/path/to/decompiled",
    recursive=True,
    save_to_file=True,
    max_workers=4
)

# Decompile multiple specified files
mcp__java-decompile-mcp__decompile_files(
    file_paths=[
        "/path/to/XmlUtil.class",
        "/path/to/XmlParser.class",
        "/path/to/SoapHandler.class"
    ],
    output_dir="/path/to/decompiled",
    save_to_file=True
)
```

### Classes That Must Be Decompiled

| Type | Match Pattern | Purpose |
|------|----------|------|
| XML utility classes | `*Xml*.class`, `*XML*.class`, `*Parser*.class` | Extract XML parsing logic |
| Servlets | `*Servlet.class`, `*Controller.class` | Trace input sources |
| WebServices | `*WebService*.class`, `*Soap*.class`, `*WS*.class` | SOAP XML handling |
| Filters | `*Filter.class` | XML request preprocessing |

---

## XXE Detection Rules Quick Reference

### ⚠️ Dangerous Patterns (parsers without security configuration)

| Parser | Dangerous Code | Vulnerability Notes |
|:-------|:---------|:---------|
| XMLReader | `XMLReaderFactory.createXMLReader()` followed directly by `parse()` | External entities are not disabled |
| SAXBuilder | `new SAXBuilder()` followed directly by `build()` | External entities are not disabled |
| SAXReader | `new SAXReader()` followed directly by `read()` | External entities are not disabled |
| SAXParserFactory | `SAXParserFactory.newInstance()` followed directly by `parse()` | External entities are not disabled |
| DocumentBuilderFactory | `DocumentBuilderFactory.newInstance()` followed directly by `parse()` | External entities are not disabled |

### ✅ Safe Patterns (protection already configured)

**The secure remediation is identical for all parsers — disable DOCTYPE or external entities:**

```java
// Option 1: Disallow DOCTYPE declarations (strictest, recommended)
setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);

// Option 2: Disable external entities individually
setFeature("http://xml.org/sax/features/external-general-entities", false);
setFeature("http://xml.org/sax/features/external-parameter-entities", false);
setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
```

### ⚠️ Input Source Detection (CRITICAL - confirm user controllability)

**Input source patterns that must be searched:**

```bash
# HTTP request body
grep -ri "getInputStream" --include="*.java"
grep -ri "getReader" --include="*.java"

# XML passed in as a parameter
grep -ri "getParameter.*xml\|getParameter.*XML" --include="*.java"

# Spring annotations
grep -ri "@RequestBody" --include="*.java"

# File upload
grep -ri "MultipartFile" --include="*.java" | grep -i "xml"

# SOAP/WebService
grep -ri "@WebService\|@WebMethod" --include="*.java"
```

---

## Data Flow Tracing (load java-route-tracer when needed)

### When Parameter Tracing Is Needed

| Scenario | Description | Operation |
|------|------|------|
| XML input passes through multiple layers | The HTTP request body is parsed after passing through Controller → Service → Util | Load java-route-tracer |
| The parser lives in a utility class | XML parsing happens in a shared XmlUtil class called from many places | Load java-route-tracer |
| The echo path is unclear | The parse result is output after multiple transformations | Load java-route-tracer |
| SOAP processing chain | WebService requests pass through an interceptor/handler chain | Load java-route-tracer |

### Automatically Triggering java-route-tracer

```python
# When the XML input flow needs to be traced
Skill(
    skill="java-route-tracer",
    args="--route {controller_route} --project {project_path}"
)
```

---

## Report Generation

**Output a single comprehensive audit report file:**

```
{project_name}_audit/xxe_audit/
└── {route_name}/
    └── {project_name}_xxe_audit_{timestamp}.md      # comprehensive audit report
```

**Route Name Notes:**
- Route names are extracted from the route path, stripping leading slashes and special characters
- Example: `/api/xml/parse` → `api_xml_parse`
- Example: `/ws/soap/endpoint` → `ws_soap_endpoint`

---

## Output Format

**Generate the output file strictly following the fill-in template in [references/OUTPUT_TEMPLATE.md](references/OUTPUT_TEMPLATE.md).**

- Filename format: `{project_name}_xxe_audit_{YYYYMMDD_HHMMSS}.md`
- Do not modify the template structure, add or remove sections, or change their order
- All [FILL IN] placeholders must be replaced with actual content
- Common specification reference: [shared/OUTPUT_STANDARD.md](../shared/OUTPUT_STANDARD.md)

---

## Verification Checklist

**Before marking the audit as complete, the following checks must be performed:**

### Code Detection Check
- [ ] All XML parsing classes have been inspected
- [ ] All 5 parser types have been searched
- [ ] The security configuration of every parser instance has been checked

### Input Source Check
- [ ] The XML input source of every parser has been traced
- [ ] Whether the input is user-controllable has been confirmed
- [ ] The echo path has been checked

### Vulnerability Detection Check
- [ ] All unprotected parsers have been flagged
- [ ] All user-controllable inputs have been traced
- [ ] XXE with echo and Blind XXE have been distinguished

### Report Completeness Check
- [ ] **The comprehensive audit report has been generated and passes the self-check checklist at the end of OUTPUT_TEMPLATE.md**

---

## References

- [OUTPUT_TEMPLATE.md](references/OUTPUT_TEMPLATE.md) - Fill-in template for the output report
- [PARSERS.md](references/PARSERS.md) - Detailed detection rules for the five XML parsers
- [DECOMPILE_STRATEGY.md](references/DECOMPILE_STRATEGY.md) - Decompilation strategy guide
