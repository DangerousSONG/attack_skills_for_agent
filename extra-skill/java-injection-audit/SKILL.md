---
name: java-injection-audit
description: |
  Java source code injection vulnerability audit. Triggered when injection vulnerabilities must be detected during a Java white-box audit.
  Covers 6 injection classes: SQL injection (JDBC/MyBatis/Hibernate/JPA), command injection (Runtime.exec/ProcessBuilder),
  SSRF (HttpURLConnection/OkHttp/RestTemplate), LDAP injection, SpEL/OGNL expression injection, and NoSQL injection (MongoDB).
  Requires the data-flow evidence (EVID_*) provided by java-audit-pipeline as audit input.
zh-signals: "Java 源码注入类漏洞审计（SQL、命令、SSRF、LDAP、SpEL/OGNL、NoSQL）。信号:java审计,注入漏洞,sql注入,命令注入,ssrf"
when-to-use: "Use during Java white-box audits when detecting injection vulnerabilities (SQL, command, SSRF, LDAP, SpEL/OGNL, NoSQL), given data-flow evidence from java-audit-pipeline."
metadata:
  tags: java injection, sql injection, command injection, ssrf, spel, ognl, ldap injection, mybatis, hibernate, jpa, nosql, injection audit, java source audit
  category: code-audit
---

# Java Injection Vulnerability Source Code Audit
This skill focuses on determining at the source level whether "the injection holds", with the core task being verifying whether filtering along the Source→Sink path is sufficient. Crafting payloads, bypassing WAFs, and other runtime exploitation techniques belong to the corresponding black-box exploit skill.

## Further Reading

- Dangerous vs. safe code patterns for the 6 injection classes / EVID evidence examples → [references/injection-patterns.md](references/injection-patterns.md)

---

## Quick Reference: 6 Injection Classes

| Type | Typical Sink | Dangerous Pattern | Severity |
|------|-----------|----------|--------|
| SQL injection | `Statement.execute`, `session.createQuery`, MyBatis `${}`, JPA `nativeQuery` | String concatenation into SQL | Critical-High |
| Command injection | `Runtime.exec`, `ProcessBuilder.start`, `commons-exec` | User input concatenated into the command string or wrapped via `sh -c` | Critical |
| SSRF | `HttpURLConnection`, `OkHttpClient`, `RestTemplate`, `WebClient` | Server-side request with a user-controllable URL | High-Medium |
| SpEL/OGNL injection | `ExpressionParser.parseExpression`, `ValueStack.findValue`, `@Value` | User input enters the expression evaluation context | Critical |
| LDAP injection | `DirContext.search`, `LdapTemplate.search` | User input concatenated into the filter string | High-Medium |
| NoSQL injection | `MongoCollection.find`, `@Query`, `$where` | String concatenation into the query or operator injection | High |

## General Audit Workflow (4 Steps)

**Step 1 -- Confirm EVID evidence points**: From the EVID_* evidence produced by Phase 3 of `java-audit-pipeline`, filter the injection-class entries (EVID_SQL_*, EVID_CMD_*, EVID_SSRF_*, EVID_EXPR_*, EVID_LDAP_*, EVID_NOSQL_*). A sink without EVID evidence can only be marked "Unverified".

**Step 2 -- Judge filter effectiveness**: Trace every filtering/escaping step along the Source→Sink path and assess whether it is effective for the current injection type. Common pitfalls: `PreparedStatement` but the SQL fragment is still built by concatenation, MyBatis `${}` mistakenly used instead of `#{}`, or PHP-style thinking such as `escapeshellarg` migrated to Java where it does not apply.

**Step 3 -- Assess bypass potential**: When filtering exists but is insufficient, analyze the concrete bypass path (encoding differences, type confusion, secondary processing, etc.). If a bypass idea can be given, mark it "Confirmed"; otherwise mark it "Unverified" and record the known filtering method.

**Step 4 -- Determine severity**: Use the three-dimension scoring formula of `java-audit-pipeline`: `Score = R*0.40 + I*0.35 + C*0.25`. Impact is usually high for injection flaws (command/expression injection I=3, SQL injection I=2-3), but reachability and exploitation complexity must be factored in.

## SQL Injection Audit Points

- **JDBC PreparedStatement vs Statement**: `PreparedStatement` + `?` placeholders are safe, `Statement.execute(sql)` with concatenation is dangerous; note that concatenation fragments may still exist inside `PreparedStatement`
- **MyBatis `#{}` vs `${}`**: `#{}` parameter binding is safe, `${}` direct concatenation is dangerous; the ORDER BY scenario often forces `${}`, which requires whitelist validation
- **Hibernate HQL concatenation**: `session.createQuery("from User where name='" + input + "'")` is HQL but is still injectable
- **JPA @Query nativeQuery**: In `@Query(value="...", nativeQuery=true)`, both SpEL `#{#param}` and string concatenation are dangerous
- **Dynamic ORDER BY**: Identifiers cannot be parameterized, so a whitelist is the only safe option; Spring Data's `Sort` object is safe

## Command Injection Audit Points

- **Runtime.exec(String) vs exec(String[])**: The single-string form splits on whitespace into program and arguments and is not automatically interpreted by a shell; the array form is more explicit, but both require attention to `-flag` argument injection
- **ProcessBuilder**: The argument-list form is similar to array exec, but wrapping it in `sh -c "cmd"` degrades it to shell interpretation
- **Reflection calls**: Invoking `Runtime.getRuntime()` or `ProcessBuilder` through reflection can bypass static scanning
- **commons-exec CommandLine**: `CommandLine.parse(userInput)` is dangerous, `addArgument(input, false)` is safe

## SSRF Audit Points

- **HttpURLConnection**: `new URL(userInput).openConnection()` — the most basic SSRF entry point
- **OkHttp / Apache HttpClient / RestTemplate / WebClient**: All require checking whether the URL parameter is user-controllable
- **Protocol restrictions**: Check whether `http/https` is restricted (`file://` reads files, `jar://` SSRF, `netdoc://` information disclosure)
- **DNS Rebinding**: Resolve-then-request introduces a TOCTOU race condition
- **Redirect following**: `HttpURLConnection` follows same-protocol redirects by default; use `setInstanceFollowRedirects(false)`

## SpEL/OGNL Expression Injection Audit Points

- **SpEL**: `new SpelExpressionParser().parseExpression(userInput).getValue()` — direct RCE
- **@Value / @PreAuthorize**: Referencing a user-controllable configuration value in the annotation can trigger SpEL evaluation
- **Thymeleaf SSTI**: The `__${expr}__` preprocessing syntax triggers SpEL execution
- **OGNL (Struts2)**: `ActionContext` / `ValueStack` injection, with a long history of vulnerabilities
- **Safe mode**: `SimpleEvaluationContext` restricts SpEL functionality (disables type references and constructors)

## LDAP Injection Audit Points

- **Filter concatenation**: `"(uid=" + username + ")"` — injecting `*)(uid=*))(|(uid=*` can modify the query logic
- **Safe mode**: Manually escape `( ) * \ \0`, or use Spring LDAP's `LdapQueryBuilder` / `LdapEncoder`
- **DN injection**: Different from filter injection, it requires escaping DN special characters such as `, + " \ < > ;`

## NoSQL Injection Audit Points

- **MongoDB Java Driver**: `BasicDBObject` / `Document` construction is injectable with operators if JSON strings are concatenated
- **Spring Data MongoDB**: `@Query("{'name': ?0}")` is parameterized and safe; building queries by string concatenation is dangerous
- **$where / $regex**: `$where` accepts JavaScript expressions, which is equivalent to code execution when user-controllable
- **Criteria API**: `Criteria.where("name").is(input)` is a safe parameterized query pattern

## Detection Checklist

- [ ] All injection-class EVID_* evidence points have been reviewed one by one
- [ ] Every SQL concatenation point has been verified for parameterized/prepared usage, and all MyBatis `${}` occurrences are flagged
- [ ] Every parameter source and construction method of the command execution entry points has been checked
- [ ] The URL source, protocol restrictions, and redirect policy of each SSRF sink have been confirmed
- [ ] The expression source of every SpEL/OGNL evaluation entry point has been traced
- [ ] The escaping handling for LDAP filters and DNs has been confirmed
- [ ] The construction method of NoSQL query parameters has been checked
- [ ] Points with insufficient filtering have a concrete bypass idea or are marked "Unverified"
- [ ] Severity scoring used the unified formula, consistent with the pipeline
