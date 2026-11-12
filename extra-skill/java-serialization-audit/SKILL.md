---
name: java-serialization-audit
description: |
  Java source code audit for serialization-class vulnerabilities. Triggered during Java white-box audits when serialization/deserialization related vulnerabilities need to be detected.
  Covers 3 risk classes: native Java deserialization (ObjectInputStream/Gadget Chain/ysoserial),
  XXE (five parsers: DocumentBuilderFactory/SAXParser/XMLInputFactory/TransformerFactory/SchemaFactory),
  and template injection SSTI (code execution via Velocity/FreeMarker/Thymeleaf template engines).
  Java deserialization is the most distinctive high-risk vulnerability class in the Java ecosystem, and gadget chain analysis is the core difficulty.
zh-signals: "Java 源码序列化类漏洞审计，覆盖反序列化、XXE 与模板注入 SSTI 的白盒检测。信号:Java反序列化,XXE,SSTI,gadget链,源码审计"
when-to-use: >-
  Use when auditing Java source code for deserialization, XXE, or SSTI
  vulnerabilities, especially when ObjectInputStream or XML parsers process
  user-controlled input.
metadata:
  tags: deserialization, xxe, ssti, objectinputstream, gadget chain, ysoserial, xml, velocity, freemarker, thymeleaf, deserialization, template injection, java source audit
  category: code-audit
---

# Java Serialization-Class Vulnerability Source Code Audit
This skill focuses on source-level judgement of "whether deserialization/XXE/SSTI holds". The core work is: white-box confirmation of deserialization entry points, tracing data sources, assessing the gadget chains available in the classpath, verifying the secure configuration of XML parsers, and checking the rendering context of template engines. Runtime black-box techniques such as crafting exploit payloads and sending remote exploit chains fall within the scope of the corresponding exploit skill.

## Further Reading

- Dangerous patterns / secure pattern code comparisons / Gadget dependency tables / EVID evidence examples for the 3 vulnerability classes → [references/serialization-patterns.md](references/serialization-patterns.md)

---

## Quick Reference Table for the 3 Vulnerability Classes

| Type | Typical Sink | Exploitation Condition | Severity |
|------|-----------|----------|--------|
| Java deserialization | `ObjectInputStream.readObject()`, `XMLDecoder.readObject()` | User-controllable serialized stream + a usable gadget chain in the classpath | Critical |
| XXE | `DocumentBuilderFactory`, `SAXParser`, `XMLInputFactory`, `TransformerFactory`, `SchemaFactory` | External entities/DTD not disabled + user-controllable XML input | High-Critical |
| SSTI | `Velocity.evaluate`, `FreeMarker Template`, Thymeleaf pre-processing expressions | User input flows directly into the template compilation/rendering context | Critical |

## Java Deserialization Audit Points

- **Entry point identification**: `ObjectInputStream.readObject()`, `ObjectInputStream.readUnshared()`, `XMLDecoder.readObject()`, plus the extra attack surface in custom `readObject`/`readResolve`/`readExternal` implementations
- **Data source tracing**: HTTP request body (magic bytes `AC ED 00 05` or Base64 encoded `rO0AB`), RMI/JMX remote calls, JMS message queues, Redis/Memcached cache deserialization, file reads, ViewState, Cookie/Session serialized storage
- **Gadget availability assessment**: check `pom.xml`/`build.gradle` and the classpath for libraries with known gadget chains (commons-collections 3.x/4.x, commons-beanutils, spring-core, Groovy, hibernate-core, etc.), and whether the versions fall within the affected ranges
- **Defense mechanism verification**: whether JEP 290 `ObjectInputFilter` is configured, allowlist vs blacklist strategy, whether third-party protection libraries such as `SerialKiller`/`NotSoSerial` are enabled, whether `resolveClass` has been overridden with allowlist validation
- **readResolve/readObject custom logic**: even without a generic gadget, file operations, network requests, and dynamic class loading inside custom deserialization methods also constitute attack surface

## XXE Audit Points

- **Secure configuration for the 5 XML parsers**:
  - `DocumentBuilderFactory`: `setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)`
  - `SAXParserFactory`: same as above + `setFeature("http://xml.org/sax/features/external-general-entities", false)` + `setFeature("http://xml.org/sax/features/external-parameter-entities", false)`
  - `XMLInputFactory` (StAX): `setProperty(XMLInputFactory.SUPPORT_DTD, false)` + `setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, false)`
  - `TransformerFactory`: `setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, "")` + `setAttribute(XMLConstants.ACCESS_EXTERNAL_STYLESHEET, "")`
  - `SchemaFactory`: `setProperty(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "")` + `setProperty(XMLConstants.ACCESS_EXTERNAL_DTD, "")`
- **Data flow analysis**: XML input source (HTTP request body, file upload, SOAP message, SVG/Office file) → enters the parser → parsed result echoed back (direct XXE) or not echoed (blind injection / out-of-band OOB)
- **Java-specific protocols**: the `jar:` protocol can trigger remote file download and extraction, and the `netdoc:` protocol (older JDKs) is equivalent to `file://`

## Template Injection SSTI Audit Points

- **Velocity**: `Velocity.evaluate(context, writer, tag, userTemplate)` — if the `userTemplate` parameter is user-controllable it is a direct RCE
- **FreeMarker**: `new Template("t", new StringReader(userInput), cfg).process(dataModel, writer)` — user input used as the template source is dangerous once compiled
- **Thymeleaf**: controller return value concatenation leads to SSTI; with `return "user/" + input`, the input can inject the `__${expr}__` pre-processing expression to trigger SpEL → RCE
- **Secure patterns**: template name/path allowlist, FreeMarker setting `TemplateClassResolver.ALLOWS_NOTHING_RESOLVER` to disable the `?new()` built-in function, Velocity using `SecureUberspector`, Thymeleaf restricting view names so user input cannot be concatenated

## Detection Checklist

- [ ] All `ObjectInputStream.readObject()`/`XMLDecoder.readObject()` call sites have been reviewed one by one
- [ ] Data sources of deserialization entry points (HTTP/RMI/JMS/cache/file) have been traced and confirmed
- [ ] Classpath dependencies have been checked for known gadget chain libraries and their affected versions
- [ ] Defense mechanisms such as JEP 290 ObjectInputFilter / SerialKiller / allowlist resolveClass have been verified
- [ ] Extra attack surface in custom readObject/readResolve methods has been ruled out
- [ ] Secure feature configuration of the 5 XML parsers has been confirmed one by one
- [ ] XML input sources (request body/upload/SOAP/SVG) and the echo behavior have been analyzed
- [ ] User-input controllability of the Velocity/FreeMarker/Thymeleaf template rendering entry points has been checked
- [ ] Template engine secure patterns (sandbox/allowlist/disabled dangerous functions) have been verified
- [ ] Severity scoring used the unified formula, consistent with the pipeline
