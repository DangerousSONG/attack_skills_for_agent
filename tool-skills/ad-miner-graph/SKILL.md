---
name: ad-miner-graph
description: "AD Miner: visualizes BloodHound data and rates risk. Signals: ad attack, domain pentest, control path graph generation, control path depth, direct DC collection"
zh-signals: "AD Miner: BH 数据可视化风险评级。信号:ad攻击,域渗透,生成控制路径图,控制路径层数,直接连域控采集。"
---

# AD Miner

- 攻击大类:C30 AD与横向移动
- 上游仓库:https://github.com/Mazars-Tech/AD_Miner
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install ad-miner
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `AD-miner -b mycontext -u neo4j -p pass` | 从 BloodHound 数据生成风险图 |
| `-c -cf mycontext` | 生成控制路径图 |
| `-l 3` | 控制路径层数 |
| `-d 10.0.0.1` | 直接连域控采集 |

## 攻击场景 Playbook

### BH 数据可视化风险评级

```bash
bloodhound-python -u svc -p pass -d corp.local -c All
AD-miner -b context -u neo4j -p pass
# 得到风险评分图,展示 tier0 资产暴露面
```

## 注意事项

Mazars 出品,消费 BloodHound 数据库生成 AD 风险的图形化评级报告。
