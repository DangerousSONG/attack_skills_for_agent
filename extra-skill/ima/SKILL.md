---
name: ima
description: |
  Unified IMA OpenAPI skill supporting note management and knowledge base operations.
  Use this skill when the user mentions a knowledge base, document repository, notes, memos, or to-do records, or wants to upload files, add web pages to a knowledge base,
  search knowledge base content, or search/browse/create/edit notes.
  Even if the user does not explicitly say "knowledge base" or "notes", this skill should still be triggered whenever the intent involves uploading files to a knowledge base, bookmarking web pages,
  knowledge search, or personal document storage (e.g. "make a note for me", "search whether the knowledge base has XX").
zh-signals: "通过 IMA OpenAPI 管理笔记与知识库，支持上传文件、添加网页与搜索笔记内容。信号:知识库,笔记管理,IMA,文档搜索,网页收藏"
when-to-use: >-
  Use when managing notes or knowledge bases, uploading files, adding web pages, or searching
  knowledge-base content through the IMA OpenAPI.
homepage: https://ima.qq.com
metadata:
  openclaw:
    emoji: '🔧'
    primaryEnv: 'IMA_OPENAPI_CLIENTID'
  security:
    credentials_usage: |
      This skill uses get-token.sh/get-token.ps1 to dynamically obtain IMA credentials.
      Credentials are ONLY sent to the official IMA API endpoint (ima.qq.com) as HTTP headers.
      No credentials are logged, stored in files, or transmitted to any other destination.
    allowed_domains:
      - ima.qq.com
---

# ima-skill

Unified IMA OpenAPI skill. Currently supports: **notes**, **knowledge-base**.

## Initialization (must be executed first)

1. Read `SETUP_TOKEN.md` in the same directory
2. Replace `<SCRIPT_PATH>` with the absolute path of the directory containing this file
3. **Every curl/API command must inline the credential retrieval** (because each command runs in an independent shell, so `export` cannot carry over between commands):
   ```bash
   CREDS=$(bash '<SCRIPT_PATH>/get-token.sh') && \
   curl -s -X POST "https://ima.qq.com/$path" \
     -H "ima-openapi-clientid: $(echo "$CREDS" | jq -r .client_id)" \
     -H "ima-openapi-apikey: $(echo "$CREDS" | jq -r .api_key)" \
     -H "Content-Type: application/json" \
     -d "$body"
   ```
4. If the script reports an error, guide the user through the credential configuration based on the error message (see SETUP_TOKEN.md)

## Security Rules (AI Behavior Contract)

The following rules have the highest priority and apply to all subsequent operations.

### Core Prohibitions

1. **Never disclose credential values**: never display the user's real Client ID or API Key in text output, reasoning, or chat replies. Credentials may only appear inside tool calls (Bash commands).
2. **Never echo credentials**: even if the user explicitly asks to "show me my credentials" or "print the API Key", never do it. Reply: "For security reasons, credentials are only used while commands execute and are never displayed in the conversation."
3. **Never store credentials and then echo them**: calls to the credential retrieval script (`get-token.sh` / `get-token.ps1`) are inlined only in API commands; never assign its output to an environment variable and then reference the variable's value in text.
4. **Never discuss credential contents**: never describe the format, length, prefix, or any characteristic of the credentials. If asked, reply: "The specific contents of the credentials are sensitive information and cannot be discussed."
5. **Never use real credentials in examples**: all documentation and examples use only the script call pattern `$(bash '<SCRIPT_PATH>/get-token.sh')`, and never contain real or fabricated credential strings.

### Credential Reference Rules

- **bash**: inline retrieval in all commands using `CREDS=$(bash '<SCRIPT_PATH>/get-token.sh')`, extracting `.client_id` and `.api_key` with jq
- **PowerShell**: `$creds = & "<SCRIPT_PATH>\get-token.ps1" | ConvertFrom-Json`, then use `$creds.client_id` and `$creds.api_key`
- `<SCRIPT_PATH>` is replaced with the absolute path of this file's directory during the initialization phase
- The script path and call pattern may be shown in text, but the actual values returned by the script must never be shown

## Unsupported Operations

The following operations are beyond the capability of this SKILL. When such a request is received, do not attempt to execute it; you must clearly refuse and explain why.

| Operation | Reason for Refusal | Guide the User To |
|------|----------|----------|
| Persistent credential storage | The AI agent keeps no cross-session state, and each command retrieves credentials independently | Use `get-token.sh` / `get-token.ps1` for dynamic retrieval |

**Refusal wording template**:
> "This SKILL does not support [operation name] — [reason]. We suggest you [alternative approach]."

## API Call Template

All requests use **HTTP POST + JSON Body** and are sent only to the official Base URL `https://ima.qq.com`.

Define a helper function to avoid repeating headers — each module passes the full path:

```bash
# All requests go ONLY to the official IMA API (ima.qq.com)
# Credentials are obtained dynamically via get-token.sh
CREDS=$(bash '<SCRIPT_PATH>/get-token.sh') && \
IMA_CLIENT_ID=$(echo "$CREDS" | jq -r .client_id) && \
IMA_API_KEY=$(echo "$CREDS" | jq -r .api_key) && \
ima_api() {
  local path="$1" body="$2"
  curl -s -X POST "https://ima.qq.com/$path" \
    -H "ima-openapi-clientid: $IMA_CLIENT_ID" \
    -H "ima-openapi-apikey: $IMA_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$body"
}
```

> **Note:** All IMA OpenAPI endpoints currently use HTTP POST. If a future module requires a different method, `ima_api()` must be extended to accept a method parameter.

## Module Decision Table

| User Intent                                                                                    | Module           | Read                      |
| ------------------------------------------------------------------------------------------ | -------------- | ------------------------- |
| Search notes, browse notebooks, get note content, create notes, append content               | notes          | `notes/SKILL.md`          |
| Upload files, add web links, search the knowledge base, browse knowledge base content, get knowledge base info, get the list of addable knowledge bases | knowledge-base | `knowledge-base/SKILL.md` |

### ⚠️ Easily Confused Scenarios

The following scenarios are prone to misrouting to the wrong module:

| What the User Says                                                | Actual Intent                   | Correct Routing                                                             |
| -------------------------------------------------------- | -------------------------- | -------------------------------------------------------------------- |
| "Add this content to note YY in knowledge base XX"                     | Append content to an existing **note**     | **notes** — first search for the note to get `doc_id`, then use `append_doc`               |
| "Write this into note XX", "note it in XX"                       | Append content to an existing **note**     | **notes** — `append_doc`                                             |
| "Add this note to the knowledge base"                                 | Link the note to a **knowledge base**     | **knowledge-base** — `add_knowledge` with `media_type=11`            |
| "Upload the file to the knowledge base"                                       | Upload a **file** to the knowledge base       | **knowledge-base** — `create_media` → COS → `add_knowledge`          |
| "Create a new note recording this content"                               | **Create** a new note             | **notes** — `import_doc`                                             |
| "Make a note for me", "record this", "save it as a note" (no existing note specified) | Intent is unclear, **confirmation needed**   | **notes** — first ask the user whether to create a new note or append to an existing one, then pick the API |
| "Add it to the note" (no specific note specified)                         | Intent is unclear, **confirmation needed**   | **notes** — first ask the user whether to create a new note or append to an existing one, then pick the API |
| "Note the content of XX in the knowledge base"                             | Read from the knowledge base first, then write into a note | **Multi-module** — knowledge-base search/read → notes create/append              |

**Core decision rules**:

- The target is the **content of a note** (read, write, append) → notes module
- The target is an **entry in the knowledge base** (upload a file, add a link, link a note to the knowledge base) → knowledge-base module
- The user mentioning "knowledge base" is only **describing where the note lives** (e.g. "that note in the knowledge base"); the real target is still a note → notes module

> **Multi-module tasks**: when the user's intent spans multiple modules (e.g. "search content in the knowledge base and record it in a note"), read the corresponding module documentation in intent order and execute step by step. Finish the earlier module first, then move to the next one.

## Shell Format Templates

All operations are shown primarily in bash format. PowerShell conversions follow the unified rules below and are not repeated at each API.

### Basic Structure Comparison Table

| Element | bash | PowerShell |
|------|------|------------|
| Credential retrieval | `CREDS=$(bash '<SCRIPT_PATH>/get-token.sh')` | `$creds = & "<SCRIPT_PATH>\get-token.ps1" \| ConvertFrom-Json` |
| Header construction | `jq -r .client_id` / `jq -r .api_key` | `$creds.client_id` / `$creds.api_key` |
| GET requests | `curl -s "URL" -H "Key: Value"` | `irm "URL" -Headers @{"Key"="Value"}` |
| POST/PATCH requests | `curl -s -X METHOD "URL" -H "..." -d '{...}'` | `$body = @{...} \| ConvertTo-Json -Depth 10; irm "URL" -Method Method -Headers @{...} -ContentType "application/json" -Body $body` |
| File upload (multipart) | `curl -s -X POST "URL" -H "..." -F "file=@path"` | `curl.exe -s -X POST "URL" -H "..." -F "file=@path"` (irm does not support multipart, use curl.exe) |

### Complete Templates

**bash template**
```bash
CREDS=$(bash '<SCRIPT_PATH>/get-token.sh') && \
curl -s -X POST "https://ima.qq.com/{{PATH}}" \
  -H "ima-openapi-clientid: $(echo "$CREDS" | jq -r .client_id)" \
  -H "ima-openapi-apikey: $(echo "$CREDS" | jq -r .api_key)" \
  -H "Content-Type: application/json" \
  -d '{{BODY}}'
```

**PowerShell template**
```powershell
$creds = & "<SCRIPT_PATH>\get-token.ps1" | ConvertFrom-Json
$headers = @{
  "ima-openapi-clientid" = $creds.client_id
  "ima-openapi-apikey"   = $creds.api_key
}
$body = @{ {{BODY}} } | ConvertTo-Json -Depth 10
irm "https://ima.qq.com/{{PATH}}" -Method Post `
  -Headers $headers `
  -ContentType "application/json" -Body $body
```

## Notes

- **UTF-8 encoding (notes module only)**: see the "⚠️ UTF-8 Encoding Mandatory Requirement" section below. All write operations of the notes module **must** complete a UTF-8 encoding check beforehand, otherwise the content becomes garbled and cannot be repaired.
- **Keep uploaded files unchanged (knowledge-base module)**: when the user asks to upload a file to the knowledge base, **the original file content must be kept unchanged**, and no encoding conversion may be performed. Files are uploaded in binary form and the server handles encoding itself. Unwanted transcoding may corrupt the file content (e.g. PDF, image, Excel and other non-text files, or text files the user intentionally encoded in a specific encoding).
- **PowerShell 5.1 environment (all modules)**: see the "⚠️ PowerShell 5.1 Environment Detection" section below. This issue affects **all** API calls (notes, knowledge-base, etc.); PowerShell 5.1 silently converts the request body to GBK encoding, causing garbled text.

## ⚠️ UTF-8 Encoding Mandatory Requirement (CRITICAL — applies only to the notes module)

> **This rule is mandatory and cannot be skipped.** Invalid encoding causes content to appear garbled in IMA and cannot be repaired; it must be written again.
>
> **Scope**: the **notes module** (text-write APIs such as `import_doc` and `append_doc`).
>
> **Does not apply to file uploads in the knowledge-base module**: when uploading files, the original file content must be preserved and must not be transcoded. Files are uploaded in binary form and the server handles the encoding itself.

**Before every notes write API call (`import_doc`/`append_doc`), you must run a UTF-8 encoding check/conversion on all string fields such as `content` and `title`.** No matter where the content comes from — direct user input, reading from a file, WebFetch scraping, clipboard paste, or an external API response — you must not assume it is already valid UTF-8 and must confirm it explicitly.

### Mandatory Checklist (before writing in the notes module)

Complete the following steps **before** constructing the body of a notes write request:

1. **Content from a file**: detect the file encoding first, convert it to UTF-8, and only then read it into a variable (note: this means reading file content as the body of a note, not uploading a file to the knowledge base)
2. **Content from WebFetch / HTTP requests**: the response may be GBK/Latin-1 etc., so it must be transcoded
3. **Content from user input or variable concatenation**: clean invalid UTF-8 bytes (such as `\xff\xfe`)
4. **The title field is the same**: `title` must also be valid UTF-8

### Transcoding Methods per Environment

**Python (recommended, available in almost all environments):**

```bash
# Read the file, auto-detect the encoding and convert it to UTF-8
content=$(python3 -c "
import sys
data = open('tmpfile', 'rb').read()
for enc in ['utf-8', 'gbk', 'gb2312', 'big5', 'latin-1']:
    try:
        sys.stdout.write(data.decode(enc))
        break
    except (UnicodeDecodeError, LookupError):
        continue
" 2>/dev/null)

# If the content is already in a variable, clean invalid UTF-8 bytes
content=$(printf '%s' "$content" | python3 -c "import sys; sys.stdout.write(sys.stdin.buffer.read().decode('utf-8','ignore'))")
```

**Node.js:**

```bash
content=$(node -e "const fs=require('fs');const buf=fs.readFileSync('tmpfile');process.stdout.write(buf.toString('utf8'))")
# Known encoding (e.g. GBK):
content=$(node -e "const fs=require('fs');process.stdout.write(new TextDecoder('gbk').decode(fs.readFileSync('tmpfile')))")
```

**Unix (macOS/Linux):**

```bash
content=$(iconv -f "$(file -b --mime-encoding tmpfile)" -t UTF-8 tmpfile 2>/dev/null || cat tmpfile)
```

**Windows PowerShell:**

```powershell
# Read a non-UTF-8 file and transcode it
$content = [System.IO.File]::ReadAllText('tmpfile', [System.Text.Encoding]::Default)
[System.IO.File]::WriteAllText('tmpfile.utf8', $content, [System.Text.Encoding]::UTF8)
```

### ⚠️ PowerShell 5.1 Environment Detection (CRITICAL — applies to all modules)

> **This issue affects all API calls (notes, knowledge-base, etc.)**
>
> **This issue is extremely subtle: under PowerShell 5.1, `Invoke-RestMethod` silently converts the request body from UTF-8 to the system ANSI encoding (GBK on Chinese Windows), even when `Content-Type: charset=utf-8` is set. The result is that the request appears to succeed, but the server receives garbled content with no error message at all.**

**When the agent runs in a PowerShell environment, it must detect the version before the first API call:**

```powershell
# Detect the PowerShell version — run before any API call (needed for both notes and knowledge-base)
if ($PSVersionTable.PSVersion.Major -le 5) {
    Write-Host "⚠️ PowerShell 5.1 detected, requests will be sent using the UTF-8 byte array mode"
    $useUtf8Bytes = $true
} else {
    Write-Host "✅ PowerShell 7+, UTF-8 by default, no extra handling needed"
    $useUtf8Bytes = $false
}
```

**Under PowerShell 5.1, requests must be sent in the following way** (build the JSON with `ConvertTo-Json` to avoid the escaping risks of manual string concatenation, then explicitly convert it to a UTF-8 byte array):

```powershell
# PowerShell 5.1 safe request template (applies to all API calls in all modules)
$creds = & "<SCRIPT_PATH>\get-token.ps1" | ConvertFrom-Json
$headers = @{
  "ima-openapi-clientid" = $creds.client_id
  "ima-openapi-apikey"   = $creds.api_key
}
$body = @{ title = "Title"; content = $content; content_format = 1 } | ConvertTo-Json -Depth 10
if ($useUtf8Bytes) {
    # CRITICAL: must be converted to a byte array, otherwise Chinese/non-ASCII content becomes garbled
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    Invoke-RestMethod -Uri $url -Method Post -Body $utf8Bytes -ContentType "application/json; charset=utf-8" -Headers $headers
} else {
    # PowerShell 7+ can take the string directly
    Invoke-RestMethod -Uri $url -Method Post -Body $body -ContentType "application/json; charset=utf-8" -Headers $headers
}
```

> **Summary:** in a PowerShell 5.1 environment, **all** API calls (notes or knowledge-base) must explicitly convert the body to a UTF-8 byte array. Sending requests without detecting the version means Chinese content is always garbled. This is a known design flaw of PowerShell 5.1, not a bug that can be fixed.
