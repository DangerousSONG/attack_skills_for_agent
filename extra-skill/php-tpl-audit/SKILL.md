---
name: php-tpl-audit
description: "PHP web source code template injection / SSTI audit tool. Identifies template engine rendering points and the controllability of template names / expressions, traces them to eval / execution chains, and outputs exploitability rating, PoC and remediation recommendations (must not be omitted)."
zh-signals: "审计 PHP 源码中的模板注入/SSTI，追踪模板名与表达式可控性至执行链。信号:PHP模板注入,SSTI,Twig,Blade,源码审计"
when-to-use: "Use when auditing PHP projects for SSTI where user input controls template names, expressions, or rendering paths."
---

# PHP Template Injection / SSTI Audit (php-tpl-audit)

Analyze PHP project source code to identify template injection (SSTI) and dangerous expression execution risks: user-controllable content influencing template selection, rendered expression parsing, or conversion into executable code.

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-TPL-{seq}`

## TPL Sink (Required)
Template-related rendering / execution points:
- Twig:
  - `Environment->load($templateName)` / `createTemplate($name)` / `render($template)`
  - `|raw` or a disabled auto-escaping policy (must have evidence points)
- Laravel Blade (Illuminate/View, common in native PHP):
  - `view($templateName, $data)` / `View::make($templateName, $data)`
  - `Illuminate\View\Factory->make($template)` / rendering entry `$engine->render({value})`
  - When the template is controllable: Blade raw output (`{!! !!}`) and `@php` directives form a high-risk execution chain (must anchor evidence points to the rendering / compilation entry)
- Smarty:
  - `Smarty->fetch($template)` / `display($template)`
- Custom template engines:
  - `eval()`, `preg_replace('/e')`, `create_function`, etc. used for template expressions
  - `call_user_func` / `call_user_func_array` whose arguments come from user input (may trigger expression evaluation)

## Controllability (Required)
Must output:
- How user input reaches the "template name / template fragment / expression string"
- Whether a strict template name allowlist mapping exists
- Whether sandboxing / expression restrictions exist

## tracer Trigger Conditions (Required)
- Template selection / expression construction spans multiple functions or goes through string concatenation

## Evidence Citation (Mandatory: from php-route-tracer)
Every suspected template injection / SSTI finding must cite, item by item, the evidence points for the **TPL rows** in the `## 9) Sink Evidence Type Checklist` section of the trace output (the status may be "to be verified", but the evidence citation must exist):
1. `EVID_TPL_ENGINE_RENDER_OR_PARSE_ENTRY`: evidence of the template engine rendering / expression parsing location (load/createTemplate/fetch/render or an equivalent entry)
2. `EVID_TPL_TEMPLATE_OR_EXPR_CONTROL`: evidence of whether the template name or expression is controllable (derived from the mapping of route parameters to template construction variables)
3. `EVID_TPL_EXEC_CHAIN_ENTRY`: evidence of the execution chain entry (expression evaluation / compilation / execution: e.g. raw/disable escape, eval/use of call_user_func)

## Handling Missing tracer Evidence (Mandatory)
- If none of the key evidence points 1-3 above can be located: the vulnerability status may only be marked `⚠️ Unverified`, and must not be directly marked `✅ Confirmed Exploitable`.

## Report Output
Output to:
```
{output_path}/vuln_audit/tpl_{timestamp}.md
```

Each entry must contain: the data flow chain, exploitability preconditions, an executable PoC framework, remediation recommendations and search queries.
