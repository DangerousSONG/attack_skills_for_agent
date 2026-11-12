---
name: mat-metadata-clean
description: "MAT: Clean metadata from exfiltrated files. Signals: trace cleanup, anti-forensics, batch in-place cleanup, list metadata without clearing, verify."
zh-signals: "MAT (Metadata Anonymisation Toolkit): 外传文件元数据清洗。信号:痕迹清理,反取证,批量原地清理,列出元数据不清除,验证。"
when-to-use: >-
  Use when preparing files for exfiltration or release and you must strip author, timestamp, GPS,
  and other metadata to prevent attribution.
---

# MAT (Metadata Anonymisation Toolkit)

- Attack Category: C20 Anti-Forensics and Trace Cleanup
- Upstream Repository: https://0xacab.org/jvoisin/mat2 or https://gitweb.torproject.org/mat.git
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install mat2 (newer) or apt install mat
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `mat2 sensitive.pdf` | Clear all metadata from a single file (author/time/GPS) |
| `mat2 --inplace *.jpg` | Batch in-place cleanup |
| `-l` | List metadata without clearing it |
| `--check` | Verify |

## Attack Scenario Playbook

### Metadata Cleaning for Exfiltrated Files

```bash
mat2 report_draft.docx  # Outputs report_draft.cleaned.docx with all Exif/XMP removed
```

## Notes

mat2 is the active successor to MAT; clears PDF/JPG/Office metadata to prevent attribution, and works just as well on screenshots.
