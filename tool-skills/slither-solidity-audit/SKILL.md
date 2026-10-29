---
name: slither-solidity-audit
description: "Slither: audits contract reentrancy and permission flaws, plus proxy upgrade integrity. Signals: blockchain, web3, scan current contract project, summary."
zh-signals: "Slither: 合约重入/权限漏洞审计、代理升级合约完整性检查。信号:区块链,web3,扫当前合约项目,摘要。"
---

# Slither

- 攻击大类:C48 区块链与Web3安全
- 上游仓库:https://github.com/crytic/slither
- 上游 License:AGPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install slither-analyzer
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `slither .` | 扫当前合约项目 |
| `--print human-summary` | 摘要 |
| `--detect reentrancy-eth` | 单类检测 |
| `--print call-graph` | 调用图 |
| `--json out.json` | 结构化输出 |
| `-triage` | 交互式筛选误报 |

## 攻击场景 Playbook

### 合约重入/权限漏洞审计

```bash
slither contracts/ --detect reentrancy-eth,unprotected-upgrade
# 高危项: 状态变量在 external call 后修改且无常量锁
```

### 代理升级合约完整性检查

```bash
slither . --detect delegatecall-loop,incorrect-proxy-implementation
```

## 注意事项

静态分析秒级出结果;复杂业务逻辑漏洞要结合 echidna 模糊测试。本项目内容二次开源为 Apache-2.0。
