---
name: php-deser-audit
description: "PHP Web source code deserialization / object injection audit tool. Identifies unserialize injection points and controllable data sources, traces magic-method chains, and outputs exploitability grading, PoC and remediation recommendations (must not be omitted)."
zh-signals: "审计 PHP 源码中的反序列化与对象注入，追踪魔术方法链并评估可利用性。信号:php,反序列化,对象注入,gadget链,unserialize,源码审计"
when-to-use: >-
  Use when auditing PHP source code for user-controlled data reaching unserialize() or
  equivalent deserialization sinks, or when tracing magic-method gadget chains.
---

# PHP Deserialization Audit (php-deser-audit)

Analyze PHP project source code to identify user-controlled data reaching `unserialize()` or an equivalent deserialization sink, then combine it with the magic methods of the involved classes (`__wakeup/__destruct/__call/__toString/{value}`) to determine whether an object injection exploit chain exists.

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-DESER-{sequence}`

## Dangerous Sinks (Required)
- `unserialize($data)`
- `unserialize(base64_decode({value}))`
- Any path that transforms user input and then deserializes it

## Controllability (Required)
Must trace and output:
- Where the deserialization argument comes from: GET/POST/Cookie/Session/Header/database field, etc.
- Whether base64/encryption/decoding/concatenation steps exist (the data may still be controllable)
- Whether validation or a signature (e.g. `hash_hmac`) exists, and whether the signature is reliable (evidence required)

## Gadget Chain Identification (Required)
Must output:
- The object type after deserialization (or the set of possible types)
- The list of magic methods in that class and their trigger conditions
- The data flow chain "object creation -> magic method trigger -> final sensitive operation (e.g. file / command / SSRF / database)"

## tracer Trigger Conditions (Required)
- The deserialization argument passes through multiple decode/wrapping layers
- The magic method chain spans multiple classes/files

## Evidence Citation (Mandatory: from php-route-tracer)
Every suspected deserialization / object injection vulnerability must cite the matching evidence points of the **DESER row** in the `## 9) Sink Evidence Type Checklist` section of the trace output item by item (the status may be pending verification, but the evidence citations must exist):
1. `EVID_DESER_CALLSITE`: location evidence of the deserialization call site (the unserialize and equivalent sinks)
2. `EVID_DESER_INPUT_SOURCE`: evidence of the user-controllable source of the argument
3. `EVID_DESER_OBJECT_TYPE_MAGIC_TRIGGER_CHAIN`: evidence of the object type / magic method trigger conditions after deserialization (and the chain to the final sensitive operation, if it can be located)

## Handling Missing tracer Evidence (Mandatory)
- If none of the key evidence points 1-3 above can be located: the vulnerability status may only be marked `⚠️ Unverified`, and must not be directly marked `✅ Confirmed Exploitable`.

## Report Output
Output to:
```
{output_path}/vuln_audit/deser_{timestamp}.md
```

## PoC (Mandatory, but labeled as "conceptual PoC / verification PoC")
Must provide:
- The real route (or the usage pattern of the cookie/session field)
- The payload generation approach (if a real gadget payload cannot be produced, state the "parts that must be filled in manually" and explain why, while still keeping an executable framework with replaceable fields)
