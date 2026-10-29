---
name: talon-kerberos-check
description: "Talon validates domain account existence. Signals: AD attack, domain penetration, domain controller"
zh-signals: "Talon: 域账户有效性验证。信号:ad攻击,域渗透,域控。"
---

# Talon

- 攻击大类:C30 AD域渗透与域控攻击
- 上游仓库:https://github.com/optiv/Talon
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/optiv/Talon && cd Talon
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 talon.py -D corp.local -U users.txt -p 'Pass123!'` | Kerberos 预认证枚举 |
| `-D d -U u.txt -p p.txt -A` | AS-REP roastable |
| `-t 10.0.0.1` | 域控 |

## 攻击场景 Playbook

### 域账户有效性验证

```bash
python3 talon.py -D corp.local -U users.txt -p Pass1
# 不出警报的账户枚举
```

## 注意事项

optiv 出品,Kerberos 错误码枚举账户。
