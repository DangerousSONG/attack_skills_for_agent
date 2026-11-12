---
name: php-xxe-audit
description: "PHP Web source code XXE audit tool. Identifies XML parsing points and entity handling configuration, traces the XML input source and the echo-back channel, and outputs exploitability grading, PoC and remediation recommendations (must not be omitted)."
zh-signals: "审计 PHP 源码中的 XXE 风险，识别 XML 解析点、输入来源与回显通道并输出分级与 PoC。信号:PHP 审计,XXE,XML 解析,外部实体,源码审计"
when-to-use: "Use when reviewing PHP source code for XML parsing points that may allow external entities and need exploitability grading."
---

# PHP XXE Audit (php-xxe-audit)

Analyze PHP project source code to identify XXE (XML External Entity) risks: when an XML parsing point allows external entities/DOCTYPE, the XML input is controllable, and an echo-back or OOB channel exists, it may lead to file read / SSRF / DoS.

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-XXE-{sequence}`

## XXE Sinks (Required)
Identify the XML parsing related code:
- `DOMDocument->loadXML/loadHTML`
- `simplexml_load_string/simplexml_load_file`
- `XMLReader->open/xml`
- `DOMDocument->load` (if the content comes from a user-controllable string/stream)
Dangerous patterns:
- External entities not disabled / network access not restricted
- The parsing options allow DOCTYPE

## Protection Checks (Required)
Must output the parser protection evidence:
- Usage of libxml safe flags: `LIBXML_NONET`, `LIBXML_NOENT` (note: NOENT may amplify the risk), `LIBXML_DTDLOAD`, etc.
- Whether `libxml_disable_entity_loader(true)` is used (the strategy differs across PHP versions, evidence is still required)
- Whether safe options are passed at parse time and network access is disabled

## Input Source and Echo-back (Required)
Must output separately:
- XML input source: `$_POST` / `php://input` / uploaded file stream, etc.
- Echo-back path: whether the parse result is written back to the response (`echo` / template output) or is only blind (OOB).

## tracer Trigger Conditions (Required)
- The XML passes through several layers of passing/parsing before the field is output
- The echo-back location is unclear or lives in a utility class

## Evidence Citation (Mandatory: from php-route-tracer)
Every suspected XXE vulnerability must cite the matching evidence points of the **XXE row** in the `## 9) Sink Evidence Type Checklist` section of the trace output item by item (the status may be pending verification, but the evidence citations must exist):
1. `EVID_XXE_PARSER_CALL`: location evidence of the XML parser call site (DOMDocument->loadXML/simplexml_load_string/XMLReader->open, etc.)
2. `EVID_XXE_INPUT_SOURCE`: evidence of the input stream source ($_POST / `php://input` / upload read / the parameter entering the parser)
3. `EVID_XXE_ENTITY_DOCTYPE_SAFETY_AND_ECHO`: evidence of the security options that disable external entities/DOCTYPE (LIBXML_* or the disabling strategy) and of the location where the parse result is echoed back

## Handling Missing tracer Evidence (Mandatory)
- If none of the key evidence points 1-3 above can be located: the vulnerability status may only be marked `⚠️ Unverified`, and must not be directly marked `✅ Confirmed Exploitable`.

## Report Output
Output to:
```
{output_path}/vuln_audit/xxe_{timestamp}.md
```
