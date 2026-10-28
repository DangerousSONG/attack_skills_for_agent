---
name: injection-checking
description: "注入漏洞路由入口:按解释器分流到XSS/SQLi/SSRF/XXE/SSTI/命令注入/NoSQL注入的检测与利用流程。信号:注入,xss,sqli,ssrf,xxe,ssti,命令注入。"
when-to-use: Injection Testing Router
  Entry P1 category router for injection testing. Use when routing between XSS,
  SQLi, SSRF, XXE, SSTI, command injection, and NoSQL injection workflows based
  on how attacker-controlled input is consumed.
---

# Injection Testing Router

This is the routing entry point when input reaches a dangerous interpreter or execution environment.

After confirming this is an injection-class issue, use it to decide whether it is mainly browser context, database, template engine, server-side requests, XML parsing, or system commands.

## When to Use

- Input reaches HTML, JS, SQL, templates, URL fetchers, XML parsers, or shell
- You have not yet decided whether to start with XSS, SQLi, SSRF, XXE, SSTI, CMDi, or NoSQL
- You need to choose the correct deep-topic skill based on input flow

## Skill Map

- [XSS Cross Site Scripting](../xss-cross-site-scripting/SKILL.md)
- [SQLi SQL Injection](../sqli-sql-injection/SKILL.md)
- [SSRF Server Side Request Forgery](../ssrf-server-side-request-forgery/SKILL.md)
- [XXE XML External Entity](../xxe-xml-external-entity/SKILL.md)
- [SSTI Server Side Template Injection](../ssti-server-side-template-injection/SKILL.md)
- [CMDi Command Injection](../cmdi-command-injection/SKILL.md)
- [NoSQL Injection](../nosql-injection/SKILL.md)
- [Deserialization Insecure](../deserialization-insecure/SKILL.md)
- [JNDI Injection](../jndi-injection/SKILL.md)
- [Expression Language Injection](../expression-language-injection/SKILL.md)
- [CRLF Injection](../crlf-injection/SKILL.md)
- Extra Injection Types (SSI, LDAP, XPath)
- [Request Smuggling](../request-smuggling/SKILL.md)
- [Prototype Pollution](../prototype-pollution/SKILL.md)
- [Type Juggling](../type-juggling/SKILL.md)
- [HTTP Parameter Pollution](../http-parameter-pollution/SKILL.md)
- [XSLT Injection](../xslt-injection/SKILL.md)
- [CSV Formula Injection](../csv-formula-injection/SKILL.md)

## Recommended Flow

1. First identify the final sink of the input
2. Then choose the topic skill that best matches that interpreter
3. Small payload samples and quick triage are merged into each main skill; no extra payload router is needed

## Related Categories

- [file-access-vuln](../file-access-vuln/SKILL.md)

> 📎 **参考文档说明**：本 skill 转自上游开源仓库，以下参考文档**未随本库分发**：`EXTRA_INJECTION_TYPES.md`。相关主题的要点已保留在本文对应描述中；如需展开内容，请按正文关键词在库内 grep 或自行检索。
