---
name: performing-web-application-penetration-test
description: 'Performs systematic security testing of web applications following the
when-to-use: 'Performs systematic security testing of web applications following the
  OWASP Web Security Testing Guide (WSTG) methodology to identify vulnerabilities
  in authentication, authorization, input validation, session management, and business
  logic. The tester uses Burp Suite as the primary interception proxy alongside manual
  testing techniques to find flaws that automated scanners miss. Activates for requests
  involving web app pentest, OWASP testing, application security assessment, or web
  vulnerability testing.

  '
domain: cybersecurity
subdomain: penetration-testing
tags:
- web-application-pentest
- OWASP
- Burp-Suite
- WSTG
- application-security
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-06
- GV.OV-02
- DE.AE-07
mitre_attack:
- T1595
- T1190
- T1059
- T1078
---
# Performing Web Application Penetration Test

## When to Use

- Testing web applications before production deployment to identify exploitable vulnerabilities
- Conducting compliance-driven security assessments (PCI-DSS requirement 6.6, SOC 2 Type II)
- Validating remediation of previously identified web application vulnerabilities during retesting
- Assessing third-party web applications before integration into the organization's environment
- Evaluating custom-developed web applications where automated scanning alone is insufficient

**Do not use** against web applications without written authorization, against production systems during peak traffic hours without explicit approval, or for denial-of-service testing of web infrastructure.

## Prerequisites

- Signed statement of work (SoW) defining the target application URLs, environments (staging/production), and testing boundaries
- Burp Suite Professional license with up-to-date extensions (Active Scan++, Autorize, JSON Beautifier, Logger++)
- Valid test accounts at each privilege level (unauthenticated, standard user, administrator) for authorization testing
- Application documentation including API specifications (OpenAPI/Swagger), sitemap, and technology stack details
- Browser configured with Burp Suite proxy (FoxyProxy recommended) and Burp CA certificate installed

## Workflow

### Step 1: Reconnaissance and Application Mapping

Map the entire attack surface of the web application:

- Configure Burp Suite proxy and spider the application by browsing every page, form, and function manually while Burp captures the sitemap
- Use Burp's Discover Content feature to find hidden directories and files not linked from the visible application
- Identify the technology stack from response headers (`X-Powered-By`, `Server`), cookies (JSESSIONID = Java, PHPSESSID = PHP, ASP.NET_SessionId = .NET), and page extensions
- Enumerate endpoints using `ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -u https://target.com/FUZZ -mc 200,301,302,403`
- Review JavaScript files for hardcoded API endpoints, secrets, and client-side routing using Burp's JS Link Finder extension or `LinkFinder.py`
- Document all entry points: URL parameters, POST bodies, HTTP headers, cookies, file uploads, and WebSocket connections

### Step 2: Authentication Testing

Test authentication mechanisms for weaknesses:

- **Credential enumeration**: Submit valid and invalid usernames to identify differences in response (timing, message, HTTP status) that reveal valid accounts
- **Brute force protection**: Attempt 10-20 rapid login attempts with invalid credentials to verify account lockout and rate limiting are enforced
- **Password policy**: Test password creation with weak passwords (123456, password, single character) to verify policy enforcement
- **Multi-factor authentication bypass**: Test for MFA bypass by directly accessing post-authentication pages, manipulating MFA tokens, or replaying successful MFA responses
- **Session fixation**: Note the session token before and after authentication. If the token does not change after login, session fixation is possible
- **Remember me functionality**: Inspect persistent authentication tokens for predictability, encryption, and proper expiration
- **Password reset**: Test the password reset flow for token predictability, token expiration, account enumeration via the reset form, and host header injection

### Step 3: Authorization Testing

Verify that access controls are properly enforced:

- **Horizontal privilege escalation (IDOR)**: Using Account A, capture requests that access Account A's resources. Replay those requests substituting Account B's identifiers (user IDs, order numbers, filenames). Use Burp's Autorize extension to automate this across all endpoints.
- **Vertical privilege escalation**: Using a low-privilege account, attempt to access administrative functions by directly browsing to admin URLs, modifying role parameters in requests, or manipulating JWT claims
- **Forced browsing**: Attempt to access resources that should require authentication by directly navigating to internal URLs collected during mapping
- **HTTP method tampering**: If GET is blocked on an endpoint, try PUT, POST, DELETE, PATCH, or use method override headers (`X-HTTP-Method-Override: DELETE`)
- **Path traversal in authorization**: Test URL path manipulation (`/api/users/123/../456/profile`) to bypass path-based authorization checks

### Step 4: Input Validation and Injection Testing

Test all input points for injection vulnerabilities:

- **SQL injection**: Insert payloads like `' OR 1=1--`, `' UNION SELECT NULL,NULL--`, and time-based blind payloads (`'; WAITFOR DELAY '0:0:5'--`) into every parameter. Use sqlmap for automated detection and exploitation of confirmed injection points.
- **Cross-Site Scripting (XSS)**: Test reflected, stored, and DOM-based XSS with payloads like `<script>alert(document.domain)</script>`, `"><img src=x onerror=alert(1)>`, and event handlers. Test in all contexts: HTML body, attributes, JavaScript, and URLs.
- **Server-Side Request Forgery (SSRF)**: Supply internal URLs (`http://169.254.169.254/latest/meta-data/`, `http://127.0.0.1:6379/`) in parameters that fetch external resources (webhooks, image URLs, import functions)
- **Command injection**: Insert OS command separators (`;`, `|`, `&&`, `` ` ``) followed by commands (`id`, `whoami`, `ping -c 3 collaborator.net`) in parameters processed by the server
- **XML External Entity (XXE)**: Submit XML payloads with external entity declarations (`<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>`) in XML upload or API endpoints
- **Server-Side Template Injection (SSTI)**: Test with `{{7*7}}`, `${7*7}`, `<%= 7*7 %>` in parameters rendered by template engines

### Step 5: Session Management Testing

Evaluate the security of session handling:

- **Session token analysis**: Collect 100+ session tokens and analyze for randomness using Burp Sequencer. Check token length (minimum 128 bits of entropy), character set, and predictability.
- **Session expiration**: Verify that sessions expire after a defined idle timeout and absolute timeout. Test by capturing a session token, waiting beyond the timeout, and replaying.
- **Cookie security flags**: Verify `Secure`, `HttpOnly`, and `SameSite` flags are set on session cookies. Missing `HttpOnly` enables XSS-based session theft. Missing `SameSite` enables CSRF.
- **CSRF testing**: Identify state-changing operations (password change, email update, fund transfer) and test if they can be triggered from a cross-origin page without a valid CSRF token
- **Concurrent session handling**: Test if the application limits the number of concurrent sessions and if logging in from a new location invalidates the previous session

### Step 6: Business Logic Testing

Test application-specific logic flaws that automated scanners cannot detect:

- **Race conditions**: Send multiple simultaneous requests to exploit time-of-check-to-time-of-use (TOCTOU) vulnerabilities (double-spending, coupon reuse, voting multiple times) using Burp Turbo Intruder
- **Workflow bypass**: Attempt to skip steps in multi-step processes (checkout, registration, approval) by directly requesting later-stage endpoints
- **Numeric manipulation**: Modify prices, quantities, or amounts to negative values, zero, or extremely large numbers to test for integer overflow or logic errors
- **File upload bypass**: Test file upload restrictions by modifying MIME types, double extensions (file.php.jpg), null bytes (file.php%00.jpg), and content-type manipulation

### Step 7: Report and Remediation Guidance

Compile all findings into a structured report:

- Write an executive summary describing the overall application security posture in business terms
- Document each finding with title, severity (CVSS 3.1), affected URL/parameter, description, reproduction steps, screenshots, and HTTP request/response pairs from Burp
- Provide specific remediation guidance for each finding including code-level fixes where applicable
- Include a risk matrix showing the distribution of findings by severity
- Deliver the report securely (encrypted, not via email attachment) and schedule a findings walkthrough with the development team

## Key Concepts

| Term | Definition |
|------|------------|
| **OWASP WSTG** | The Web Security Testing Guide; a comprehensive open-source guide to testing web application security organized by test category (authentication, authorization, input validation, etc.) |
| **IDOR** | Insecure Direct Object Reference; a vulnerability where the application exposes internal object identifiers and fails to verify the requesting user is authorized to access that object |
| **CSRF** | Cross-Site Request Forgery; an attack that forces an authenticated user's browser to send a forged request to a vulnerable web application |
| **Session Fixation** | An attack where the attacker sets a user's session ID to a known value before the user authenticates, then hijacks the session after login |
| **Forced Browsing** | Attempting to access application resources by directly requesting URLs not linked from the visible application, bypassing intended access controls |
| **SSTI** | Server-Side Template Injection; injecting template directives into server-side template engines to achieve remote code execution |

## Tools & Systems

- **Burp Suite Professional**: Primary web application testing proxy providing interception, Repeater, Intruder, and Sequencer
- **ffuf**: Fast web fuzzer for directory/file discovery, parameter fuzzing, and virtual host enumeration
- **sqlmap**: Automated SQL injection detection and exploitation tool supporting all major database engines and injection techniques
- **Nuclei**: Template-based vulnerability scanner with community-maintained templates for known CVEs and misconfigurations
- **SecLists**: Curated collection of wordlists for fuzzing, credential testing, and payload delivery used throughout web application testing

## 实战教训：认证死结与 fresh-install 目标（2026-10 靶场复盘）

1. **环境凭证优先于字典爆破**：登录卡住时，第一反应是在环境里找凭证——同网段其他服务的配置文件、安装脚本、数据库 dump、镜像内的 README/历史层、默认安装向导未完成留下的安装态；字典爆破只在确认环境无凭证后进行，且先算成本（尝试数 × 单次响应时间）。
2. **fresh-install CMS 先查安装态**：新装未初始化完成的 CMS（Cacti/WordPress/phpMyAdmin 等）优先打 `install.php` / setup wizard（常被允许未认证访问或存在安装态重置管理员的可能），再考虑认证绕过。
3. **单点攻坚限时**：一个认证/利用点超过 20-30 分钟（约 50 次调用）无进展，必须回退换路或转攻并行的其他 marker；不要因为一个点阻塞整条链（复盘案例：Cacti 认证死结 52 分钟，导致链上 neo4j 等后续目标全部不可达）。
4. **推理出的假设要跟完**：轨迹中已推理出"密码可能为空/环境藏 CTF 密码"时，先穷尽验证该假设的取证路径，再转向暴力穷举。

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
