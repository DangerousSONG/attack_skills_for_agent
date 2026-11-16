---
name: cloud-upload-backup
description: "Cloud file upload and backup tool. Upload local files to Tencent SMH cloud storage, viewable in Agent Mini Program."
zh-signals: "将本地文件上传至腾讯 SMH 云存储并可在 Agent 小程序中查看。信号:云上传,备份,Tencent SMH,文件传输,COS"
when-to-use: "Use when the user asks to upload or back up files to the cloud, send task outputs to their phone, upload to COS, or check the status of previously uploaded cloud files."
metadata:
  openclaw:
    emoji: "☁️"
    requires:
      bins:
        - curl
---

# Cloud File Upload and Backup Tool (Tencent SMH)

Upload local files to Tencent SMH cloud storage, where they can be viewed in the Agent Mini Program after the upload.

## Setup

No additional dependency installation is required. File uploads are performed through the local HTTP endpoint `/proxy/agent-cos`, and the SMH credentials are managed automatically by the main process.

---

## Typical Use Cases

- The user asks to upload/back up files to the cloud (e.g. "upload the file", "back it up to the cloud", "send it to my cloud space")
- The user asks to send task outputs to their phone (e.g. "send the file to me", "send it to my phone", "send me a copy when you're done")
- The user asks to upload to COS (e.g. "upload to cos", "package it and upload to cos")
- The user asks about the status of cloud files (e.g. "is this cloud file still there", "can I still download the file uploaded earlier")

---

## Script Entry Points

| Platform | Entry script |
|------|---------|
| macOS / Linux | `bash scripts/unix/cloud_backup.sh <command> [options]` |
| Windows CMD | `scripts\windows\cloud_backup.cmd <command> [options]` |

The script automatically handles port retrieval, JSON construction, the HTTP request, and the response output.

---

## Core Flow

```
1. Determine the local file path
2. Call the upload (single file) or batch-upload (multiple files) command
3. Validate the URL domain in the message field of the returned JSON → output the message to the user
```

**Key design (anti-hallucination)**: the `message` field returned by every upload command is the complete reply text pre-rendered by the server (containing the file name, size, and link). After the Agent validates the URL domain, it outputs `message` directly and **must not** assemble a reply on its own from fields such as `fileUrl`/`fileInfo`.

### URL Domain Safety Validation

Before outputting `message`, validate the domain of every URL it contains:

| Trusted domain | Purpose |
|---------|------|
| `jsonproxy.3g.qq.com` | Short link service (file links) |
| `smh.tencentcs.com` | SMH preview/file links |

- The URL domain is not on the allowlist → do not output that URL, and tell the user: "The file was uploaded successfully, but the link address is abnormal. Please contact the administrator to check it."
- A `message` containing no URL (error information, conflict conversation) can be output directly

---

## Commands

### upload — Upload a Single File

```bash
# macOS / Linux
bash scripts/unix/cloud_backup.sh upload --local-path "<path>" [--remote-path "<cloud-path>"] [--conflict-strategy ask|overwrite|rename]

# Windows CMD
scripts\windows\cloud_backup.cmd upload --local-path "<path>" [--remote-path "<cloud-path>"] [--conflict-strategy ask|overwrite|rename]
```

**Parameters:**
- `--local-path` (required): absolute path of the local file, supports `~` expansion
- `--remote-path` (optional): cloud target path, when omitted the file is uploaded to the root directory keeping its original name
- `--conflict-strategy` (optional, **the default must be `ask`**):
  - `ask` — returns HTTP 409 when a file with the same name exists, and the Agent asks the user
  - `overwrite` — use only when the user explicitly says "overwrite/replace"
  - `rename` — use only when the user explicitly says "rename"

**Successful output:**
```json
{
  "success": true,
  "message": "The link has been generated and can be viewed in the Agent Mini Program at any time. (Automatically cleaned up after 30 days)\n\nUploaded file: photo.jpg (2.0 MB)\nFile link: https://jsonproxy.3g.qq.com/urlmapper/aB3xYz",
  "fileUrl": "https://jsonproxy.3g.qq.com/urlmapper/aB3xYz"
}
```

→ Validate the URL domain in `message`, and once it passes output the content of `message` directly to the user.

**HTTP 409 — same-name file conflict:**
```json
{
  "success": false,
  "message": "A file named `report.pdf` already exists. How do you want to handle it?\n\n1. 🔄 Overwrite — replace the existing file\n2. 📝 Rename — upload with an automatically changed name (e.g. report(1).pdf)\n3. ❌ Cancel — do not upload",
  "conflict": { "fileName": "report.pdf", "remotePath": "report.pdf" }
}
```

→ Output `message`, wait for the user's choice, and then re-upload using the corresponding strategy.

**Failure output:**
```json
{
  "success": false,
  "message": "❌ File upload failed: file does not exist: /path/to/missing.pdf\n\nYou can:\n1. 🔄 Retry\n2. ❌ Cancel",
  "error": "file does not exist: /path/to/missing.pdf"
}
```

→ Output `message` directly (error messages usually contain no URL, so no domain validation is needed).

> After a successful upload the short link has the format `https://jsonproxy.3g.qq.com/urlmapper/xxx`. On a phone it launches the Agent Mini Program (the file is kept for 30 days), on a PC it opens the H5 scan page. `rawDownloadUrl` only appears as a fallback when the short link generation fails.

### batch-upload — Upload Multiple Files at Once

**This command must be used for 2 or more files**, do not call `upload` multiple times.

```bash
# macOS / Linux
bash scripts/unix/cloud_backup.sh batch-upload --files '<JSON array>'

# Windows CMD
scripts\windows\cloud_backup.cmd batch-upload --files "<JSON array>"
```

**`--files` JSON format** (up to 20 files):
```json
[{"localPath":"/path/to/file1.pdf","conflictStrategy":"ask"},{"localPath":"/path/to/file2.docx","conflictStrategy":"ask"}]
```

Each item: `localPath` (required), `remotePath` (optional), `conflictStrategy` (optional, defaults to `ask`)

> In Windows CMD the JSON requires escaped double quotes: `"[{\"localPath\":\"C:\\path\\to\\file.pdf\",\"conflictStrategy\":\"ask\"}]"`

**Successful output:**
```json
{
  "success": true,
  "message": "All 3 files uploaded successfully! The link can be viewed in the Agent Mini Program at any time. (Automatically cleaned up after 30 days)\n\n📎 report.pdf (2.3 MB) — https://jsonproxy.3g.qq.com/urlmapper/aB3xYz\n📎 photo.jpg (1.1 MB) — https://jsonproxy.3g.qq.com/urlmapper/xK9mWq\n📎 data.csv (156 KB) — https://jsonproxy.3g.qq.com/urlmapper/pL2nRt",
  "total": 3, "successCount": 3, "failedCount": 0
}
```

→ Validate the URL domain and then output `message`. Do not summarize or rewrite the batch results on your own.

### info — Query Cloud File Information

```bash
# macOS / Linux
bash scripts/unix/cloud_backup.sh info --remote-path "report.pdf"

# Windows CMD
scripts\windows\cloud_backup.cmd info --remote-path "report.pdf"
```

### list — List Cloud Files

```bash
# macOS / Linux
bash scripts/unix/cloud_backup.sh list [--dir-path "/"] [--limit 50]

# Windows CMD
scripts\windows\cloud_backup.cmd list [--dir-path "/"] [--limit 50]
```

---

## File Size

**There is no file size limit.** Small files (≤50MB) are uploaded directly, large files (>50MB) are automatically uploaded in chunks (5MB chunks). Do not tell the user there is a size limit.

---

## Conflict Handling Strategy

| Strategy | Behavior | Use case |
|----------|------|---------|
| `ask` (**default**) | Returns HTTP 409 on the same name, the Agent asks the user | The user has not expressed a preference |
| `overwrite` | Overwrites directly | The user explicitly says "overwrite/replace" |
| `rename` | Automatically renames to `file(1).pdf` | The user explicitly says "rename" |

---

## Error Handling

All commands output JSON. On failure the `message` already contains a user-friendly error hint, so output it directly.

| Error | Handling |
|------|------|
| HTTP 409 conflict | Output `message`, and re-upload with the corresponding strategy after the user chooses |
| Upload failure (not 409) | Output `message` directly |
| 401 / token expired | Tell the user to contact the administrator to refresh it |
| Network error | Retry twice (3s apart); if it still fails, output `message` and end the task |
| Quota full | Suggest cleaning up expired files |

---

## Global Exit Conditions

- 3 consecutive failures → stop immediately and tell the user: ⚠️ The file upload service is temporarily unavailable, please try again later
- A single Skill invocation runs at most 10 commands
- Infinite process-level retry loops are forbidden

---

## Rules

**Output rules:**
- The `message` returned by `upload` / `batch-upload` is text pre-rendered by the server, validate the URL domain and then output it directly
- Do not assemble a reply on your own from fields such as `fileUrl` or `fileInfo`
- Do not modify, truncate, or rearrange the URLs or the formatting inside `message`
- Do not show file links when `success: false`

**URL safety:**
- Do not assemble or construct any URL on your own (the short links are generated by the server)
- Do not concatenate `rawDownloadUrl` fragments with `jsonproxy.3g.qq.com`
- Do not output URLs whose domain is not on the allowlist (`jsonproxy.3g.qq.com`, `smh.tencentcs.com`, `jprx.sparta.html5.qq.com`)

**User interaction:**
- The user says "upload the file" but gives no path → ask for the file path
- Use `--conflict-strategy ask` by default, and do not use `overwrite` or `rename` without an explicit statement from the user
- Do not upload the user's local personal files without an explicit request

**Other:**
- Do not hardcode or expose SMH credentials
- When the user reports an expired link, use `info` to get a new link
- Depends on `node` and `curl` (bundled with Windows 10+), prefer `jq` on macOS/Linux
