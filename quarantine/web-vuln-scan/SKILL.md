---
name: web-vuln-scan
description: "Single-target in-depth web vulnerability scanning strategy. Use when the target URL is already known and you need deep vulnerability testing on a single web application. Unlike recon-full (asset discovery), this skill assumes the target is already identified and focuses on depth-first vulnerability testing. Covers fingerprint-driven scan strategy selection, a combination of automated and manual testing, and vulnerability prioritization. Prioritize finding high-severity issues such as RCE and SQL injection"
zh-signals: "针对已确定的单个 Web 目标进行指纹驱动、自动化结合手动的深度漏洞测试。信号:web漏洞扫描,指纹识别,nuclei,深度测试,单目标,优先级"
when-to-use: >-
  Use when the target URL is already known and you need depth-first vulnerability testing of a
  single web application, prioritizing high-impact bugs such as RCE and SQL injection.
metadata:
  tags: "web,vuln,poc,scan,vulnerability-scan,fingerprinting,security-assessment,nuclei,deep-testing"
  category: "exploit"
---

# Single-Target In-Depth Web Vulnerability Scanning Methodology

Unlike `recon-full` (breadth-first, asset discovery), this skill is **depth-first** — it performs comprehensive vulnerability testing against an already identified single web target.

## Phase 1: Technology-Stack-Driven Scan Strategy

Fingerprint first, then choose a targeted scanning route based on the results:

```bash
# Fingerprinting
curl -sI http://target | grep -i "Server\|X-Powered-By\|X-AspNet"
httpx -u http://target -tech-detect -silent
```

| Technology Stack | Automated Scanning Focus | Manual Testing Focus |
|--------|---------------|-------------|
| PHP (WordPress/Laravel/ThinkPHP) | CMS-specific POCs, PHP deserialization | LFI / file upload / `include()` parameters |
| Java (Spring/Struts/Tomcat) | Log4j/Spring4Shell/Struts2 | Deserialization entry points, Actuator exposure |
| Python (Flask/Django) | SSTI, debug mode | Pickle deserialization, secret key exposure |
| Node.js (Express/Koa) | Prototype pollution | Dependency vulnerabilities, `eval()` injection |
| .NET (ASP.NET/IIS) | ViewState deserialization | web.config exposure |

The vulnerability distribution differs hugely across technology stacks — blind full scans waste time.

## Phase 2: Automated Scanning

### 2.1 Known Vulnerability Scanning
```bash
# Nuclei scan (filtered by severity to save time)
nuclei -u http://target -severity critical,high
```
If the fingerprint is clear, narrow the scope:
- WordPress → `nuclei -u http://target -tags wordpress`
- Known CVE → `nuclei -u http://target -t cves/`

### 2.2 Default Credential Detection
```bash
nuclei -u http://target -t default-logins/ -silent
```
Many applications are installed and the password is never changed — this is the "cheapest" attack path.

### 2.3 Directories and Sensitive Files
```bash
# spray directory brute-forcing (recommended, smart filtering + high performance)
spray -u http://target -d /pentest/AboutSecurity/Dic/Web/Directory/Fuzz_common.txt
# or use ffuf
ffuf -u http://target/FUZZ -w /pentest/AboutSecurity/Dic/Web/Directory/Fuzz_common.txt -mc 200,301,302,403
```
The focus is not on running a large wordlist, but on checking whether the results contain:
- **Admin panels** (`/admin`, `/manager`, `/console`) → try logging in directly
- **Configuration exposure** (`.env`, `config.php`, `web.config`) → may contain database passwords
- **Source code exposure** (`/.git`, `.svn`, `backup.zip`)
- **Debug endpoints** (`/actuator`, `/debug`, `/phpinfo.php`) → a lot of internal information

## Phase 3: Manual Testing (What Automated Scanning Cannot Reach)

Automated tools cannot cover logic flaws or vulnerabilities that require contextual understanding. Test each functional area in a targeted way:

### 3.1 Input Point Test Matrix
| Functional Area | Test First | Reference Skill |
|--------|----------|----------|
| Search / query | SQL injection | `sql-injection-methodology` |
| Login form | Weak passwords, SQL injection, brute force | `default-cred-sweep` |
| File upload | Type bypass, path traversal | `file-upload-methodology` |
| User input reflection | XSS, SSTI | `xss-methodology`, `ssti-methodology` |
| Comments / guestbook | Stored XSS | `xss-methodology` |
| URL / file path parameters | LFI/SSRF | `lfi-rfi-methodology`, `ssrf-methodology` |
| XML input/SOAP/file upload | XXE | `xxe-injection-methodology` |
| API endpoints | IDOR, authentication bypass | `api-fuzz`, `idor-methodology` |
| JWT token | Algorithm bypass, key brute force | `jwt-attack-methodology` |

### 3.2 Testing Priority
1. **Directly lead to RCE** → command injection, deserialization, SSTI, file upload
2. **Can read sensitive data** → SQL injection, LFI, IDOR
3. **Can yield credentials** → default credentials, information disclosure, weak encryption
4. **Require user interaction** → XSS, CSRF (usually not tested in CTFs)

## Phase 4: Result Analysis and Attack Path Planning

After the scan completes, listing a pile of vulnerabilities is not enough — you must assess **which vulnerabilities can be combined into an attack path**:

**Direct paths** (one step):
- RCE vulnerability → get a shell directly
- Admin panel weak password → exploit the backend features

**Combined paths** (multi-step chains):
- Information disclosure → obtain credentials → log into the backend → file upload in the backend → webshell
- SQL injection → read the config file → obtain the key → forge a JWT → administrator privileges
- SSRF → read cloud metadata → cloud credentials

## Notes
- Automated scanning is the starting point, not the endpoint — truly high-severity vulnerabilities usually require manual discovery
- Fingerprinting accuracy directly affects downstream efficiency; spending one round on good fingerprinting is worth it
- When you find a low-severity issue, consider whether it can be combined with other findings into a high-severity attack chain

## Testing Priority
- RCE first: command execution vulnerabilities directly yield the flag
- Default credentials second: backend access quickly provides more information

## Further Reading

- Web vulnerability checklist and advanced wfuzz usage → [references/scan-methodology.md](references/scan-methodology.md)
