---
name: gitrecon-github-osint
description: "GitRecon collects GitHub organization information. Signals: asset mapping, subdomains, token."
zh-signals: "GitRecon: GitHub 组织信息收集。信号:资产测绘,子域名,token。"
when-to-use: >-
  Use during asset mapping to collect information about a GitHub user or
  organization, including repositories and exposed subdomains, optionally with a
  token for higher rate limits.
---

# GitRecon

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/GONZOsint/gitrecon
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/GONZOsint/gitrecon && cd gitrecon && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python gitrecon.py -s target` | Search GitHub by user/organization |
| `-t X` | token |

## Attack Scenario Playbook

### GitHub Organization Information Gathering

```bash
python gitrecon.py -s targetcorp -t $GITHUB_TOKEN
# lists all employee accounts, repos, gists, and events — watch for secret leaks
```

## Notes

Account-level OSINT on GitHub; organization members' public gists are a prime target for secret leaks.
