---
name: java-framework-audit
description: |
  Java framework-specific vulnerability source code audit. Trigger it during Java white-box audits
  when detecting known vulnerability patterns at the framework level.
  Covers 5 major frameworks/components: the Spring family (SpEL/Actuator/parameter binding/Spring Cloud Gateway),
  Struts2 (OGNL/ActionMapping/Content-Type parsing), Shiro (RememberMe deserialization/URI bypass),
  FastJSON/Jackson/Gson (deserialization autotype/polymorphic), MyBatis (`${}` injection/dynamic SQL).
  These are the framework-level vulnerabilities that occur most frequently and have the broadest impact in the Java ecosystem.
zh-signals: "审计 Java 框架层面漏洞，涵盖 Spring、Struts2、Shiro、FastJSON/Jackson 与 MyBatis。信号:Java 框架审计,Spring 漏洞,Shiro 反序列化,FastJSON,源码审计"
when-to-use: "Use when performing white-box Java source audit and you need to detect framework-level vulnerability patterns in Spring, Struts2, Shiro, JSON libraries, or MyBatis."
metadata:
  tags: spring, struts2, shiro, fastjson, jackson, mybatis, ognl, spel, actuator, rememberme, spring cloud, framework vulnerabilities, java source audit
  category: code-audit
---

# Java Framework-Specific Vulnerability Source Code Audit
Framework vulnerabilities fall into two categories: **flaws in the framework itself** (known CVEs, fixed by upgrading) and **framework misuse** (configuration/coding flaws caused by developers misunderstanding the framework's security mechanisms). The core question this skill addresses is: how does the code of the audited project trigger these known framework vulnerability patterns.

## Further Reading

- Detailed vulnerability patterns for the 5 major frameworks/components → [references/framework-vulns.md](references/framework-vulns.md)

---

## Quick Reference Table for the 5 Major Frameworks/Components

| Framework/Component | Core Risk | Primary Search Keywords | Typical Severity |
|-----------|---------|---------------|-----------|
| Spring family | SpEL injection / Actuator exposure / Mass Assignment | `@Value` `SpelExpression` `Actuator` `management.endpoints` | High-Critical |
| Struts2 | OGNL injection / Content-Type parsing | `struts.xml` `ActionSupport` `ValueStack` `ognl` | Critical |
| Shiro | RememberMe deserialization / URI bypass | `setCipherKey` `rememberMe` `ShiroFilterChain` | Critical |
| FastJSON/Jackson/Gson | Deserialization autotype / polymorphic | `JSON.parseObject` `JSON.parse` `enableDefaultTyping` `@JsonTypeInfo` | Critical |
| MyBatis | `${}` SQL concatenation injection | `${` in Mapper XML / `@Select` `@Update` annotations | High |

### Spring Family Audit Points

- **Spring MVC parameter binding (Mass Assignment)**: `@ModelAttribute` automatically binds request parameters to object fields. If the entity class contains sensitive fields such as `role`/`isAdmin`/`price` and no `@InitBinder` + `WebDataBinder.setAllowedFields()` whitelist is used, an attacker can overwrite sensitive properties by adding extra parameters
- **Spring Boot Actuator**: check the `management.endpoints.web.exposure.include` configuration. High-risk endpoints: `/actuator/env` (configuration leak + restart RCE), `/actuator/jolokia` (JNDI injection), `/actuator/heapdump` (heap dump for key/password extraction), `/actuator/gateway/routes` (Gateway route injection)
- **SpEL injection**: 5 common injection points — `@Value("#{externInput}")`, `@Cacheable(key="#root.args[0]")` concatenating user input, `@PreAuthorize` / `@PostAuthorize` expression concatenation, `ExpressionParser.parseExpression()` directly parsing external input, and SpEL `?#{...}` in Spring Data `@Query`
- **Spring Cloud Gateway**: CVE-2022-22947 type vulnerability, SpEL expressions embedded in route Predicate/Filter configuration, registering malicious routes dynamically through the Actuator `/gateway/routes`
- **Spring Security configuration traps**: wrong `antMatchers` ordering (a permissive rule placed before a strict rule overrides it), overly broad `.permitAll()`, and path matching inconsistent with the Servlet path (e.g. trailing slash `/admin` vs `/admin/`)

### Struts2 Audit Points

- **OGNL injection**: user-controllable data enters OGNL expression evaluation. Parameter names/values enter the `ValueStack` through `ParametersInterceptor`; if `SecurityMemberAccess` restrictions are loose, arbitrary code execution is possible
- **Content-Type parsing**: improper error handling for malformed Content-Type in the Jakarta Multipart parser leads to OGNL execution (S2-045); the filename field of Content-Disposition is similar (S2-046)
- **ActionMapping parameter prefixes**: `method:` (invoke arbitrary Action methods), `redirect:`/`redirectAction:` (OGNL injection). Check `struts.enable.DynamicMethodInvocation` and `struts.mapper.alwaysSelectFullNamespace`
- **Version CVE mapping**: Struts 2.0.x~2.3.x is the high-risk range; S2-001/005/009/012/013/015/016/019/032/033/037/045/046/048/052/053/057/059/061/062 are all remote code execution level

### Shiro Audit Points

- **RememberMe deserialization**: Shiro 1.2.4 and earlier encrypt the RememberMe cookie with the hardcoded AES key `kPH+bIxk5D2deZiIxcaaaA==`. Even after upgrading, if the developer uses a custom but predictable/leaked key, the risk remains
- **URI bypass**: semicolon truncation `/admin/;.js` bypasses Shiro but is routed normally by Spring, `/..;/admin` path traversal, double URL encoding, and mixed case to bypass the Filter. The root cause is that Shiro's URL matching is inconsistent with the parsing rules of the backend framework (Spring/Servlet)
- **Version CVEs**: CVE-2016-4437 (hardcoded key), CVE-2020-1957 (`/toLogin;/../admin` bypass), CVE-2020-11989 (double encoding), CVE-2021-41303 (path normalization bypass)

### FastJSON/Jackson/Gson Audit Points

- **FastJSON**: `JSON.parseObject(input)` or `JSON.parse(input)` supports the `@type` field to specify the deserialization class by default. The autotype blacklist is bypassed over and over as versions increase (1.2.24→1.2.47→1.2.68→1.2.80). With `Feature.SupportNonPublicField` enabled, private fields can be set. 1.2.83+ introduced `safeMode`, which disables autotype entirely
- **Jackson**: `ObjectMapper.enableDefaultTyping()` or `ObjectMapper.activateDefaultTyping()` enables global polymorphic deserialization, which is equivalent to a global RCE entry point. Field-level `@JsonTypeInfo(use=Id.CLASS)` or `@JsonTypeInfo(use=Id.MINIMAL_CLASS)` is equally dangerous
- **Gson**: does not support polymorphic deserialization natively and is relatively safe. However, a custom `TypeAdapter` / `JsonDeserializer` that loads a user-supplied class name with `Class.forName` introduces risk
- **Detection method**: search for `JSON.parseObject` / `JSON.parse` (FastJSON), `enableDefaultTyping` / `activateDefaultTyping` / `@JsonTypeInfo` (Jackson), and custom `TypeAdapter` (Gson)

### MyBatis Audit Points

- **`${}` vs `#{}`**: `${}` is direct string concatenation (equivalent to `String.format`), while `#{}` is precompiled parameter binding. `${}` in Mapper XML and in `@Select`/`@Update`/`@Delete`/`@Insert` annotations is a SQL injection entry point
- **`${}` in dynamic SQL**: `${}` inside `<if test="sort != null">ORDER BY ${sort}</if>`, `<where>`, and `<foreach>` tags is equally dangerous
- **Safe patterns for ORDER BY / LIKE / IN**: ORDER BY cannot use `#{}` precompilation, so the column name must be whitelist-validated; LIKE should be rewritten as `LIKE CONCAT('%', #{keyword}, '%')`; IN should use `<foreach collection="ids" item="id">#{id}</foreach>`
- **Two entry points**: Mapper XML files (`*Mapper.xml`) and the annotation style (`@Select("SELECT * FROM ${table}")`); both need auditing

## Detection Checklist

- [ ] The frameworks used by the project and their exact version numbers are confirmed and compared against known CVEs
- [ ] The exposure scope of the Spring Actuator endpoints has been checked, and it is confirmed whether sensitive endpoints require authentication
- [ ] All 5 SpEL injection scenarios have been searched for one by one
- [ ] It has been checked whether entities bound via Spring MVC `@ModelAttribute` contain sensitive fields without a whitelist
- [ ] For Struts2 projects, the OGNL security configuration and `SecurityMemberAccess` settings are confirmed
- [ ] Whether Shiro `setCipherKey` uses the default or a weak key is confirmed, and whether the URI matching of the Filter Chain is consistent with the actual routes
- [ ] The FastJSON version and autotype configuration are confirmed, as well as whether Jackson has `enableDefaultTyping` enabled
- [ ] All uses of `${}` in Mapper XML and `@Select` annotations are marked, and unavoidable cases are confirmed to have whitelist protection
- [ ] `${}` inside dynamic SQL tags (`<if>` / `<where>` / `<foreach>`) has been checked
- [ ] Every discovered framework vulnerability has an EVID_* evidence chain (Source→Sink path + version/configuration evidence)
