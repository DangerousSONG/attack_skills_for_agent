---
name: middleware-tactics
description: "Middleware vulnerability exploitation methodology. Use when discovering web middleware such as Tomcat/WebLogic/JBoss/WildFly/IIS/Nginx/Apache. Covers admin console default credentials, WAR/JSP webshell deployment, parsing vulnerabilities, misconfiguration exploitation, and AJP protocol exploitation. This skill should be used for any scenario involving middleware, application servers, or parsing vulnerabilities"
zh-signals: "Web 中间件弱口令、部署与解析漏洞利用方法论。信号:中间件,Tomcat,WebLogic,弱口令,WAR部署。"
when-to-use: "Use when identifying Tomcat, WebLogic, JBoss, WildFly, IIS, Nginx, or Apache middleware, testing admin console default credentials, deploying WAR or JSP webshells, exploiting AJP Ghostcat, path traversal, or extension parsing flaws."
metadata:
  tags: "middleware,tomcat,weblogic,jboss,wildfly,iis,nginx,apache,middleware,parsing-vulnerability,war,deployment,admin-console,ajp"
  category: "postexploit"
  mitre_attack: "T1190,T1210"
---

# Middleware Vulnerability Exploitation Methodology

Middleware is the runtime environment of web applications — taking over the middleware equals executing code directly on the server.

## ⛔ Further Reading (Must Read)

Detailed exploitation commands and payloads for each middleware type are organized by middleware type, covering Tomcat, WebLogic, JBoss, IIS, Nginx, and Apache HTTPD.

---

## Phase 1: Middleware Identification

```bash
# Automated fingerprinting
whatweb http://TARGET
curl -sI http://TARGET | grep -i "Server\|X-Powered-By"
nmap -sV -p 80,443,8080,8009,8443,9090,7001,4848,9200 TARGET

# Common port fingerprints
```

| Port | Middleware | Admin Console Path |
|------|--------|-------------|
| 8080 | Tomcat | /manager/html |
| 7001 | WebLogic | /console |
| 8080/9990 | JBoss/WildFly | /admin-console, /management |
| 4848 | GlassFish | /common/index.jsf |
| 80/443 | IIS | — |
| 80/443 | Nginx | — |
| 80/443 | Apache | /server-status |

## Phase 2: Attack Decision Tree

```
Which middleware did you identify?
├─ Tomcat
│   ├─ /manager reachable → default credentials → deploy WAR
│   ├─ 8009 AJP open → Ghostcat file read/RCE
│   └─ PUT method enabled → write JSP directly
│
├─ WebLogic
│   ├─ /console reachable → default credentials → deploy WAR
│   └─ T3/IIOP protocol → deserialization RCE (many CVEs)
│
├─ JBoss/WildFly
│   ├─ JMX Console unauthenticated → deploy WAR
│   └─ Deserialization (JMXInvokerServlet)
│
├─ IIS
│   ├─ PUT method → WebDAV upload
│   ├─ Short filename → information disclosure
│   └─ Parsing vulnerability (6.0/7.5)
│
├─ Nginx
│   ├─ Path traversal (alias misconfiguration)
│   ├─ Parsing vulnerability (cgi.fix_pathinfo)
│   └─ CRLF injection
│
└─ Apache
    ├─ Path traversal (CVE-2021-41773)
    └─ mod_cgi/mod_cgid → RCE
```

## Phase 3: Generic Attack — Admin Console Default Credentials

**Methodology**: for identified middleware admin interfaces, test default credential combinations.

1. Confirm the admin interface is reachable (Phase 1 port/path table)
2. Try logging in with a default credential dictionary (each middleware has specific default username/password combinations)
3. Mind the lockout policy — some middleware lock accounts after multiple failures
4. After a successful login, proceed to Phase 4

## Phase 4: WAR Deployment Getshell

**Methodology**: after obtaining admin console access, use the deployment feature to upload a webshell.

1. **Tomcat Manager** — deploy the WAR package through the manager text interface or the HTML UI
2. **WebLogic Console** — deploy the application through the Console UI or the REST API
3. **JBoss/WildFly** — deploy through the JMX Console or the admin interface

Generic flow:
- Generate a WAR-format webshell (msfvenom or manually packaged JSP)
- Deploy it to the target through the admin interface
- Access the deployment path to trigger the webshell

## Phase 5: Parsing Vulnerability Exploitation

**Methodology**: exploit differences in how middleware parses file extensions to bypass upload restrictions.

Core idea:
1. **Suffix deception** — abuse the middleware's parsing logic for multi-suffix names, truncation characters, and directories, so uploaded image/text files are executed as scripts
2. **FastCGI/CGI path parsing** — abuse configurations such as `cgi.fix_pathinfo` to pass non-script paths to the interpreter
3. **PUT method** — write executable files directly into the web directory
