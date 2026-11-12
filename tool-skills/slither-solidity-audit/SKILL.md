---
name: slither-solidity-audit
description: "Slither: audits contract reentrancy and permission flaws, plus proxy upgrade integrity. Signals: blockchain, web3, scan current contract project, summary."
zh-signals: "Slither: 合约重入/权限漏洞审计、代理升级合约完整性检查。信号:区块链,web3,扫当前合约项目,摘要。"
when-to-use: >-
  Use when auditing a Solidity codebase for reentrancy, access-control, or proxy-upgrade issues,
  or when triaging static-analysis findings before deeper fuzzing.
---

# Slither

- Attack Category: C48 Blockchain and Web3 Security
- Upstream Repository: https://github.com/crytic/slither
- Upstream License: AGPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install slither-analyzer
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `slither .` | Scan the current contract project |
| `--print human-summary` | Summary |
| `--detect reentrancy-eth` | Single detector |
| `--print call-graph` | Call graph |
| `--json out.json` | Structured output |
| `-triage` | Interactively triage false positives |

## Attack Scenario Playbook

### Contract reentrancy and permission flaw audit

```bash
slither contracts/ --detect reentrancy-eth,unprotected-upgrade
# High risk items: a state variable modified after an external call without a reentrancy guard
```

### Proxy upgrade contract integrity check

```bash
slither . --detect delegatecall-loop,incorrect-proxy-implementation
```

## Notes

Static analysis returns results in seconds; complex business logic flaws need to be combined with echidna fuzzing. The content of this project is re-released under Apache-2.0.
