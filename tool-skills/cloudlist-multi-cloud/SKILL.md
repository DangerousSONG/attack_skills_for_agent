---
name: cloudlist-multi-cloud
description: "cloudlist: Enumerates attack surfaces across multiple clouds. Signals: cloud privilege escalation, IAM privilege escalation, AWS asset enumeration, JSON."
zh-signals: "cloudlist: 多云攻击面枚举。信号:云提权,iam提权,枚举 AWS 资产,JSON。"
when-to-use: >-
  Use when enumerating assets across authorized AWS, GCP, Azure or other cloud providers
  with configured credentials to build an external attack surface inventory.
---

# cloudlist

- Attack Category: C18 Cloud and Container Privilege Escalation
- Upstream Repository: https://github.com/projectdiscovery/cloudlist
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/projectdiscovery/cloudlist/cmd/cloudlist@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `cloudlist -provider aws -id test` | Enumerate AWS assets |
| `-p gcp,azure,digitalocean` | Multi-cloud |
| `-o out.txt` | Output |
| `-j` | JSON |
| `-ep aws_ec2,aws_s3` | Select only specific service types |

## Attack Scenario Playbook

### Multi-Cloud Attack Surface Enumeration

```bash
cloudlist -p aws,gcp,azure -o assets.txt
# Output all instances, IPs, buckets and DB endpoints, then merge them into the scanning list
```

## Notes

Part of the pd ecosystem for multi-cloud enumeration; configure credentials in ~/.config/cloudlist/provider-config.yaml.
