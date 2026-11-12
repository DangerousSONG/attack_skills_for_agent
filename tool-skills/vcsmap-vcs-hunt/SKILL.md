---
name: vcsmap-vcs-hunt
description: "vcsmap: Code repository exposure discovery. Signals: attack surface, cloud assets, version control repository discovery, platform."
zh-signals: "vcsmap: 代码仓库暴露发现。信号:攻击面,云资产,版本控制仓库发现,平台。"
when-to-use: >-
  Use when mapping an organization's external attack surface and you need to discover exposed
  source-code repositories across platforms such as GitHub, GitLab, and Bitbucket.
---

# vcsmap

- Attack Category: C05 External Attack Surface and Cloud Asset Exposure
- Upstream Repository: https://github.com/melvinsh/vcsmap
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
gem install vcsmap
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `vcsmap scan corp` | Version control repository discovery |
| `scan org -g github,gitlab` | Platform |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Exposed Code Repository Discovery

```bash
vcsmap scan corp
# Search github/gitlab/bitbucket for sensitive repositories
```

## Notes

Multi-platform code repository discovery.
