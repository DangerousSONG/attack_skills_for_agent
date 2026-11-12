---
name: java-file-audit
description: |
  Java source code file operation vulnerability audit. Triggered when file-related vulnerabilities must be detected during a Java white-box audit.
  Covers 5 file risk classes: arbitrary file upload (MultipartFile/Servlet Part/type bypass), arbitrary file read (NIO/IO streams/path traversal),
  arbitrary file write (configuration overwrite/webshell drop), archive extraction vulnerabilities (ZipInputStream/Zip Slip), and file delete/rename race conditions.
  Requires the data-flow evidence provided by java-audit-pipeline.
zh-signals: "审计 Java 源码中文件上传、读取、写入、归档提取与删除类漏洞。信号:Java审计,文件上传,路径穿越,Zip Slip,文件读写"
when-to-use: >-
  Use during Java white-box auditing when reviewing code touching MultipartFile, file streams, path handling, or archive extraction.
metadata:
  tags: file upload, file read, file write, path traversal, zip slip, file upload, arbitrary read, arbitrary write, java nio, multipartfile, path traversal
  category: code-audit
---

# Java File Operation Vulnerability Source Code Audit
This skill focuses on determining at the source level whether "the file operation flaw holds", with the core task being verifying path controllability, filename controllability, and content controllability. Upload-bypass payloads, directory traversal exploit chains, and other runtime exploitation techniques belong to the corresponding black-box exploit skill.

## Further Reading

- Dangerous vs. safe code patterns for the 5 file vulnerability classes / EVID evidence examples → [references/file-vuln-patterns.md](references/file-vuln-patterns.md)

---

## Sink Classification Decision Tree

Enter a different audit branch based on the type of sink function encountered:

| Sink Function | Branch | Typical Severity |
|-----------|------|-----------|
| `MultipartFile.transferTo()` / `Part.write()` | File upload | Critical-High |
| `FileInputStream` / `Files.readAllBytes()` / `new File(path)` / `ClassLoader.getResourceAsStream()` | File read | High-Medium |
| `FileOutputStream` / `Files.write()` / `FileWriter` | File write | Critical-High |
| `ZipInputStream.getNextEntry()` / `ZipFile.entries()` | Archive extraction | High |
| `File.delete()` / `Files.delete()` | File delete | Medium |

## File Upload Audit Points

The essence of an upload vulnerability is that three conditions are met simultaneously: an executable extension + a web-reachable storage path + no renaming/content sanitization.

- **MultipartFile**: `file.transferTo(new File(dir + file.getOriginalFilename()))` — `getOriginalFilename()` returns the client-supplied original filename and may contain `../` path traversal or a malicious extension
- **Servlet Part**: `part.write(uploadPath + fileName)` — check whether `fileName` comes from `part.getSubmittedFileName()` and is not sanitized
- **ContentType validation vs extension validation**: `file.getContentType()` comes from the client's HTTP header and can be fully forged; an extension whitelist is more reliable but requires `toLowerCase()` handling
- **Storage path controllability**: A `../` in the filename escapes the upload directory; after `Paths.get(dir, fileName).normalize()` the prefix must be validated
- **Spring multipart-config**: `spring.servlet.multipart.location` / `max-file-size` / `max-request-size` settings affect upload behavior; check whether the limits are reasonable
- **Magic bytes validation**: Real type detection requires reading the file header bytes (e.g. `ImageIO.read()` or Apache Tika) instead of trusting the Content-Type

## File Read Audit Points

Path traversal is the core of file read vulnerabilities; `../` and its variants can escape the intended directory:

- **Path traversal `../`**: `new FileInputStream("/data/" + userPath)` — user input `../../etc/passwd` reads arbitrary files
- **NIO safe pattern**: `Path resolved = baseDir.resolve(userInput).normalize(); if (!resolved.startsWith(baseDir)) throw ...` — `normalize()` eliminates `../`, `startsWith()` validates the prefix
- **URL encoding bypass**: `%2e%2e%2f` (`../`), double encoding `%252e%252e%252f` — check whether the framework auto-decodes before passing the value into the path
- **ClassLoader.getResourceAsStream**: Classpath reads are limited by the ClassLoader sandbox and usually cannot traverse to arbitrary filesystem paths, but sensitive configuration inside the classpath can still be read
- **Spring Resource paths**: The `classpath:` protocol is limited to the classpath, while the `file:` protocol can access the filesystem — check whether the protocol is user-switchable

## File Write Audit Points

Write vulnerabilities require: a controllable path + controllable content + a write path executable by the web container.

- **Webshell write**: `Files.write(Paths.get(dir + filename), content.getBytes())` — when both path and content are controllable, writing `.jsp` into the web root yields RCE
- **Configuration file overwrite**: Overwriting `application.yml` / `application.properties` modifies datasource, redirect, and other settings; overwriting `web.xml` adds a malicious Servlet mapping
- **Log injection to plant a shell**: The logging framework records user input → the log file path is predictable → combine with file inclusion or directly write JSP content into the log
- **Template file overwrite**: A writable Thymeleaf / FreeMarker template directory → overwrite the template with an SSTI payload → triggers on the next render
- **Safe pattern**: Path whitelist + content type validation + store files outside the web root + minimize write permissions

## Archive Extraction Audit Points

Zip Slip is the most classic archive extraction vulnerability, where a malicious archive entry name contains `../` and leads to an arbitrary path write:

- **ZipEntry.getName() containing `../`**: `new File(destDir, entry.getName())` — an entry name such as `../../webapps/ROOT/shell.jsp` writes directly into the web directory
- **Safe pattern (canonical path validation)**: Before extraction, obtain `file.getCanonicalPath()` and `destDir.getCanonicalPath()` and verify that the file path starts with the target directory
- **TarInputStream / GzipInputStream**: Similar risk, since tar entry names can also contain path traversal
- **File overwrite**: Even without directory traversal, a malicious archive can overwrite existing files in the same directory (configuration files, library files)

## File Delete Audit Points

- **Path traversal delete**: `new File(dir + userInput).delete()` — user input `../../important.conf` deletes a critical file
- **TOCTOU race**: The time window between the permission check and the delete lets an attacker replace the target with a symlink pointing at a sensitive file
- **Symlink following**: `Files.delete(path)` deletes the link target rather than the link itself (implementation-dependent), while `File.delete()` only deletes the link

## Detection Checklist

- [ ] All file-class EVID_* evidence points have been reviewed one by one
- [ ] The filename sanitization method of upload features has been confirmed (UUID renaming vs. original filename vs. extension whitelist)
- [ ] Whether the upload storage path is inside the web root and directly reachable by URL has been verified
- [ ] ContentType validation has been distinguished from file header magic bytes validation
- [ ] Traversal protection on file read paths has been checked (normalize + startsWith pattern)
- [ ] The path and content sources of file writes have been traced, and whether an executable location can be written has been confirmed
- [ ] Entry name validation of archive extraction functions has been checked (canonical path verification)
- [ ] Path validation and symlink risks of file delete operations have been assessed
- [ ] Points with insufficient filtering have a concrete bypass idea or are marked "Unverified"
- [ ] Severity scoring used the unified formula, consistent with the pipeline
