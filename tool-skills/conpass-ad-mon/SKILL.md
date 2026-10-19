---
name: conpass-ad-mon
description: 渗透工具 skill:conpass 的安装、参数速查与攻击场景 playbook。当任务涉及 AD域渗透与域控攻击 需要调用 conpass 时使用。
---

# conpass

- 攻击大类:C30 AD域渗透与域控攻击
- 上游仓库:https://github.com/login-securite/conpass
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/login-securite/conpass && pip install .
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `conpass -d corp.local -u svc -p pass --dc-ip 10.0.0.1` | 密码策略+强度审计 |
| `-d d -u u -p p --dc-ip ip -w` | 弱口令检测 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### AD 密码策略审计

```bash
conpass -d corp.local -u svc -p pass
# 找弱口令账户(login-securite 出品)
```

## 注意事项

login-securite 出品,AD 密码策略分析。
