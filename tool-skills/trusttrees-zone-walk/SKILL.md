---
name: trusttrees-zone-walk
description: "TrustTrees finds DNS delegation-chain takeover vulnerabilities. Signals: AD attack, domain penetration, DNS trust-boundary visualization, Graphviz output, Gandi integration"
zh-signals: "TrustTrees: DNS 委托链漏洞找接管。信号:ad攻击,域渗透,DNS 信任边界可视化,Graphviz 输出,Gandi 集成。"
when-to-use: >-
  Use when assessing DNS delegation chains for dangling NS records that enable
  subdomain takeover. Produces Graphviz output and can integrate with Gandi
  and Route53.
---

# TrustTrees

- Attack Category: C30 AD and Lateral Movement
- Upstream Repository: https://github.com/mandatoryprogrammer/TrustTrees
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/mandatoryprogrammer/TrustTrees && cd TrustTrees && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 trusttrees.py --domain example.com` | DNS trust boundary visualization |
| `-o report.dot` | Graphviz output |
| `--gandi-apikey X` | Gandi integration |
| `--aws-access-key X` | Route53 integration |

## Attack Scenario Playbook

### Find takeover vectors in DNS delegation chains

```bash
python3 trusttrees.py --domain target.com
# Discover dangling NS delegations (the subdomain can be registered and taken over) → host a malicious site for phishing/cookie theft
```

## Notes

Enumerates and visualizes DNS delegation chains, focusing on the subdomain takeover surface caused by dangling delegations.
