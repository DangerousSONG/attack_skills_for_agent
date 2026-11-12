---
name: java-deserialization-methodology
description: "Java deserialization vulnerability detection and exploitation. Use when the target is a Java application (Tomcat/Spring/WebLogic/JBoss/Jenkins), when Base64 data starting with rO0AB/aced0005 is found, when HTTP requests carry a application/x-java-serialized-object Content-Type, or when T3/IIOP/RMI/JNDI protocol ports are present. Covers ysoserial gadget chains, JNDI injection, Fastjson/Jackson deserialization, Shiro rememberMe, and common middleware CVE exploitation"
zh-signals: "Java 反序列化漏洞检测与利用，覆盖 ysoserial gadget、JNDI 注入、Fastjson/Jackson、Shiro 与中间件 CVE。信号:Java反序列化,ysoserial,JNDI,Shiro,中间件CVE"
when-to-use: >-
  Use when targeting Java applications with serialized data (rO0AB/aced0005),
  T3/IIOP/RMI/JNDI ports, or middleware such as WebLogic, JBoss, or Jenkins.
metadata:
  tags: "java,deserialization,ysoserial,jndi,rmi,ldap,fastjson,jackson,shiro,weblogic,jboss,jenkins,log4j,gadget,rce"
  category: "exploit"
---

# Java Deserialization Vulnerability Methodology

Java deserialization is one of the most dangerous vulnerability classes in the Java ecosystem — once successful it usually leads straight to RCE.

## ⛔ Further Reading (Must Read)

- Need the ysoserial gadget chain priority table, URLDNS detection, and payload construction → [references/ysoserial-gadgets.md](references/ysoserial-gadgets.md)
- Need JNDI injection, Fastjson version payloads, and Shiro/WebLogic/JBoss/Jenkins specifics → [references/jndi-fastjson.md](references/jndi-fastjson.md)

---

## Phase 1: Identify Java Deserialization Entry Points

### 1.1 Native Java Serialized Data (Magic Bytes)
- Binary: `\xac\xed\x00\x05` (hex: `aced0005`)
- After Base64 encoding: starts with `rO0AB`
- After Gzip compression then Base64: starts with `H4sIAAAA`

**Check locations**: cookies (`rememberMe`/`VIEWSTATE`), POST body, custom headers, WebSocket, RMI/T3/IIOP protocol ports

### 1.2 JSON Deserialization (Fastjson/Jackson)
- Fastjson: JSON contains an `@type` field → [references/jndi-fastjson.md](references/jndi-fastjson.md)
- Jackson: `DefaultTyping` enabled → JSON contains a class name array `["com.xxx.Class", {...}]`
- Identification: send malformed JSON and observe the library name in the error stack trace

### 1.3 Specific Middleware Ports

| Port | Service | Vulnerability Direction |
|------|------|----------|
| 7001/7002 | WebLogic | T3/IIOP deserialization |
| 8009 | AJP (Tomcat) | GhostCat (CVE-2020-1938) |
| 1099 | RMI Registry | RMI deserialization |
| 1090/8500 | JBoss JMX | JMXInvokerServlet |
| 50000 | Jenkins | Jenkins CLI deserialization |

## Phase 2: Exploitation Decision Tree

```
Deserialization entry point found
├─ Native serialization (rO0AB/aced0005)?
│   ├─ Confirm the vulnerability with URLDNS first → [references/ysoserial-gadgets.md](references/ysoserial-gadgets.md)
│   └─ Try CC1-7 → CommonsBeanutils → Spring → Groovy one by one
├─ Fastjson (`@type` field)?
│   └─ Identify the version → pick the matching payload → [references/jndi-fastjson.md](references/jndi-fastjson.md)
├─ Shiro (rememberMe=deleteMe)?
│   └─ Default key kPH+bIxk5D2deZiIxcaaaA== → [references/jndi-fastjson.md](references/jndi-fastjson.md)
└─ Log4j (Java application + user input)?
    └─ ${jndi:ldap://...} → [references/jndi-fastjson.md](references/jndi-fastjson.md)
```

## Notes
- **Detect with URLDNS first**, then try command-execution gadgets once the vulnerability is confirmed
- ysoserial's `Runtime.exec()` does not support pipes/redirection, so Base64-encode the command
- The Java version affects how JNDI can be exploited (JDK < 8u191 is the simplest, 8u191+ needs a local gadget)
- Try multiple gadget chains one by one — different classpath environments suit different gadgets
