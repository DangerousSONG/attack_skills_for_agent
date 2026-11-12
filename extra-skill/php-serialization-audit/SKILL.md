---
name: php-serialization-audit
description: |
  PHP source code audit for serialization and template class vulnerabilities. Trigger when a PHP white-box audit needs to detect deserialization, XML parsing, or template injection vulnerabilities.
  Covers 3 risk classes: PHP deserialization (unserialize / phar deserialization / POP chain construction),
  XXE (XML external entity injection / libxml configuration), SSTI (template injection / Twig / Blade / Smarty engines).
  Requires data-flow evidence provided by php-audit-pipeline.
zh-signals: "审计 PHP 源码中的反序列化、XXE 与模板注入漏洞，判断 Source→Sink 数据可控性与安全配置。信号:PHP反序列化,XXE,SSTI,模板注入,POP链"
when-to-use: >-
  Use during PHP white-box audits when detecting deserialization, XML external entity,
  or template injection vulnerabilities, with data-flow evidence from the audit pipeline.
metadata:
  tags: deserialization, unserialize, phar, pop chain, xxe, xml, libxml, ssti, template injection, twig, smarty, blade, php-deserialization, template-injection, xml-external-entity
  category: code-audit
---

# PHP Source Code Audit for Serialization and Template Vulnerabilities
This skill focuses on the source code level to determine whether "deserialization/XXE/SSTI actually hold", focusing on validating data controllability and secure configuration along the Source→Sink path. Runtime techniques such as payload construction and chain exploitation belong to the corresponding black-box exploit skills.

## Further Reading

- Dangerous patterns for the 3 vulnerability classes / secure pattern code comparison / EVID examples → [references/deser-patterns.md](references/deser-patterns.md)

---

## Quick Reference Table for the 3 Vulnerability Classes

| Type | Typical Sink | Exploitation Condition | Severity |
|------|-----------|----------|--------|
| Deserialization | `unserialize`, `phar://` trigger functions | User-controllable serialized data + usable Gadget classes | Critical |
| XXE | `DOMDocument::loadXML`, `simplexml_load_string`, `XMLReader::xml` | External entities not disabled + user-controllable XML input | High-Critical |
| SSTI | `Twig::render`, `Smarty::display`, `Blade {!! !!}`, `eval` | User input flows directly into the template rendering context | Critical |

## Deserialization Audit Checklist

- **unserialize() entry points**: search all `unserialize` calls, trace where the argument comes from (Cookie, Session, cache, database, HTTP request body), and determine whether the user controls it
- **Phar deserialization**: 40+ filesystem functions such as `file_exists`/`is_dir`/`fopen`/`filesize`/`copy` automatically trigger deserialization when handling the `phar://` protocol; check whether the path argument is user-controllable
- **POP chain search**: start from `__destruct`/`__wakeup`/`__toString` entry points and follow chained method calls to dangerous sinks (file write / command execution / SQL operations). Focus on Gadget classes inside Composer dependencies
- **allowed_classes restriction**: is `unserialize($data, ['allowed_classes' => [...]])` in effect? Only an empty array `[]` or `false` is completely safe, `true` (the default) applies no restriction at all

## XXE Audit Checklist

- **libxml_disable_entity_loader**: in PHP < 8.0 you must explicitly call `libxml_disable_entity_loader(true)` to disable external entities. The function is deprecated in PHP 8.0+ and external entities are disabled by default, but the `LIBXML_NOENT` flag can re-enable them
- **DOMDocument risk**: `loadXML($input, LIBXML_NOENT)` is the highest risk point because the flag expands external entities. Even without passing `LIBXML_NOENT`, PHP < 8.0 may still load entities by default
- **SimpleXML/XMLReader**: `simplexml_load_string` is safe by default (PHP 8.0+), but the `LIBXML_NOENT` flag makes it dangerous; `XMLReader::xml` is the same
- **Blind XXE vs out-of-band**: is the parse result echoed back to the page? When there is no output, check whether an out-of-band channel (HTTP/FTP/DNS) can be abused

## SSTI Audit Checklist

- **Twig**: ordinary `{{ user_input }}` variable output usually just renders a variable and is protected by autoescaping; for SSTI check whether user input enters the template source parsing flow, such as `createTemplate($userInput)`, dynamically concatenated template strings, or a too-permissive `sandbox` policy (allowing dangerous filters/functions)
- **Smarty**: `{php}` tags (deprecated since Smarty 3.1+ but possibly not disabled), PHP function calls injected into `{if}` expressions (`{if system('id')}{/if}`)
- **Blade**: `{!! $var !!}` outputs unescaped content, so a user-controllable `$var` leads to XSS or worse; an injectable `@php` directive leads directly to RCE
- **Custom template engines**: search for `eval`/`preg_replace(/e)` combined with string replacement patterns — a fatal combination common in in-house template engines

## Detection Checklist

- [ ] The argument source of every `unserialize` call site has been reviewed
- [ ] Path argument controllability of Phar protocol trigger functions has been checked
- [ ] POP chain entry magic methods have been enumerated and chain reachability traced
- [ ] `allowed_classes` configuration has been verified and the default value `true` has been flagged
- [ ] Usage of the `LIBXML_NOENT` flag in XML parsers has been confirmed
- [ ] Invocation status of `libxml_disable_entity_loader` has been checked (PHP < 8.0)
- [ ] How user input is rendered in Twig/Smarty/Blade templates has been reviewed
- [ ] eval calls in custom template engines have been ruled out
- [ ] Severity scoring used the unified formula, consistent with the pipeline
