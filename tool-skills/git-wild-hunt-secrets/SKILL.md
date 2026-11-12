---
name: git-wild-hunt-secrets
description: "git-wild-hunt mines leaked secrets in public repositories. Signals: attack surface, cloud assets, bulk scanning, custom rules."
zh-signals: "git-wild-hunt: 公开仓库密钥泄露挖掘。信号:攻击面,云资产,批量,自定义规则。"
when-to-use: >-
  Use when mining public GitHub repositories, single or bulk, for leaked secrets
  such as cloud keys and credentials, including custom detection rules.
---

# git-wild-hunt

- Attack Category: C05 Cloud Asset Discovery
- Upstream Repository: https://github.com/d1vious/git-wild-hunt
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/d1vious/git-wild-hunt && cd git-wild-hunt && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python git-wild-hunt.py -i https://github.com/org/repo` | GitHub repository secret mining |
| `-i repos.txt` | Batch |
| `--regex custom.txt` | Custom rules |
| `-o out.json` | Output |

## Attack Scenario Playbook

### Mining leaked secrets in public repositories

```bash
python git-wild-hunt.py -i https://github.com/corp/web
# Regex-scan everything for AWS keys / passwords / tokens to obtain cloud credentials
```

## Notes

By d1vious; scans the full history of GitHub repositories for secrets, with regex coverage for mainstream cloud/service credentials.
