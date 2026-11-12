---
name: python-prototype-pollution
description: "Python prototype pollution (attribute injection/Class Pollution) detection and exploitation. Use when the target is a Python web application (Flask/Sanic/Django/FastAPI) that exposes recursive merge, deep attribute setting (pydash.set_), or JSON configuration update endpoints. Covers pollution entry point identification, __globals__ chain construction, Flask SECRET_KEY/Jinja2 delimiter/searchpath pollution, pydash path filter bypass, Sanic pollution chains, and RCE/file read/privilege escalation exploitation"
zh-signals: "检测并利用 Python 原型链污染，通过 merge 或 pydash 等深度属性设置入口篡改全局对象实现 RCE、文件读取或权限提升。信号:Python 原型链污染,Class Pollution,pydash,merge 注入,Flask RCE"
when-to-use: "Use when a Python web application (Flask/Sanic/Django/FastAPI) exposes recursive merge or deep attribute-setting interfaces such as pydash.set_ and you need to test or exploit class pollution."
metadata:
  tags: "prototype-pollution,python,pydash,merge,class-pollution,attribute-injection,flask,sanic,jinja2,rce,proto,deep-set,recursive-merge,globals,config-pollution,cookie,octal,bypass,waf"
  category: "exploit"
---

# Python Prototype Pollution Methodology

Python prototype pollution (also known as Class Pollution / Attribute Injection) abuses Python class inheritance and the `__globals__` mechanism. Through recursive merge functions or deep attribute-setting functions (such as `pydash.set_()`), it "escapes" the current scope from an ordinary object to modify global variables, Flask configuration, and Jinja2 engine settings, achieving RCE, file read, or privilege escalation.

## Further Reading

- Complete Flask/Jinja2 pollution target list → [references/flask-jinja2-targets.md](references/flask-jinja2-targets.md)
- Detailed Phase 3A-3I exploitation payloads and advanced Phase 4 chains → [references/exploitation-payloads.md](references/exploitation-payloads.md)
- pydash path filter bypass + cookie octal bypass → [references/pydash-bypass.md](references/pydash-bypass.md)
- Sanic framework pollution chain → [references/sanic-pollution-chain.md](references/sanic-pollution-chain.md)
- Quick reference checklist of complete pollution chains → [references/quick-reference.md](references/quick-reference.md)

---

## Phase 0: Identify Pollution Entry Points

Look for code patterns that recursively merge/set user JSON input into Python objects:

| Entry point type | Code signature | Common endpoints |
|---------|---------|---------|
| Custom merge function | `def merge(src, dst)` + `setattr(dst, k, v)` | POST JSON configuration update |
| pydash.set_() | `pydash.set_(obj, path, value)` | API attribute setting |
| pydash.get() | `pydash.get(obj, path)` | API attribute query |
| pydash.invoke() | `pydash.invoke(obj, path, arg)` | API method invocation |
| Other deep-set libraries | `glom`, `box`, any deep-set implementation | Configuration update endpoints |

**Identification signals**:
- The endpoint accepts nested JSON objects (`{"a": {"b": {"c": "value"}}}` format)
- The endpoint accepts dotted path strings (`"a.b.c"` format)
- Response headers reveal Python/Flask/Werkzeug/uvicorn
- Pages/source code/requirements.txt mention pydash, merge, update

## Phase 1: Confirm Pollution Feasibility

### 1.1 Determine the obj type

| obj type | Starting path | Identification method |
|---------|---------|---------|
| **Custom class instance** | `__init__.__globals__` | Setting `__init__.__globals__.xxx` directly works |
| **Dictionary (dict)** | `__class__.__init__.__globals__` | Must first use `__class__` to escape the dictionary key/value logic |

### 1.2 Harmless probing (does not damage the target)

```bash
# merge function scenario: nested JSON
curl -X POST http://target/api/merge \
  -H 'Content-Type: application/json' \
  -d '{"__class__": {"__name__": "test"}}'

# pydash.set_ scenario: dotted path
curl -X POST http://target/api/update \
  -H 'Content-Type: application/json' \
  -d '{"path": "__class__.__name__", "value": "test"}'

# pydash.get scenario: information leak probe
curl -X POST http://target/api/get \
  -H 'Content-Type: application/json' \
  -d '{"path": "__class__"}'
```

## Phase 2: Select the Pollution Target

### Decision tree

```
Confirm Python prototype pollution is feasible
├── Target uses pydash.invoke()?
│   └── Yes → direct RCE (Phase 3A)
├── Target uses Flask?
│   ├── Need privilege escalation? → pollute class attribute is_admin (Phase 3B)
│   ├── Has session? → pollute SECRET_KEY → forge session (Phase 3C)
│   ├── Has SSTI but it is filtered? → pollute Jinja2 delimiters (Phase 3D)
│   ├── Has render_template? → pollute searchpath/static directory (Phase 3E)
│   └── Has before_first_request? → reset _got_first_request (Phase 3F)
├── Target has file upload?
│   ├── Code calls commands with relative paths → PATH hijacking (Phase 3G)
│   └── Code has lazy-loaded imports → sys.path hijacking (Phase 3H)
└── Has functions with default args such as shell=False?
    └── Pollute __defaults__ / __kwdefaults__ (Phase 3I)
```

> Detailed exploitation commands and code for each Phase see [references/exploitation-payloads.md](references/exploitation-payloads.md)

### Recommended Attack Order

Escalate gradually from low risk to high risk:

1. **Harmless probing** → confirm pollution is feasible (Phase 1.2)
2. **Information leak** → read SECRET_KEY, app.config, etc. via get (Phase 3C step 1)
3. **Privilege escalation** → pollute is_admin or global variables (Phase 3B)
4. **File read** → _static_url_path or searchpath (Phase 3E)
5. **RCE** → invoke / delimiter+SSTI / PATH hijacking (Phase 3A/3D/3G)

If there are pydash-related leads, also run `search_vulndb("pydash")` to obtain the detailed exploit chain from the CVE-2023-26145 entry; the two approaches complement each other.

## Relationship with SSTI and Deserialization

| Technique | Entry point | Relationship |
|------|------|------|
| **Prototype pollution** | merge/set_ endpoints | This skill |
| **SSTI** | Template injection points | Prototype pollution can change Jinja2 delimiters to bypass SSTI filters |
| **Deserialization** | pickle/json | Once SECRET_KEY is polluted, sessions can be forged → trigger pickle deserialization |

The three can be combined: prototype pollution → modify SECRET_KEY → forge session → pickle RCE.
