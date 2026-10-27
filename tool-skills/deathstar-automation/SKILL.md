---
name: deathstar-automation
description: DeathStar: 一键自动化域渗透。信号:ad攻击,域渗透,自动化域管路径,域控。
---

# DeathStar

- 攻击大类:C30 AD域渗透与域控攻击
- 上游仓库:https://github.com/ByronLeeeee/DeathStar
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/ByronLeeeee/DeathStar && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 deathstar.py -u svc -p pass -d corp.local` | 自动化域管路径 |
| `-u u -p p -d d -dc 10.0.0.1` | 域控 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 一键自动化域渗透

```bash
python3 deathstar.py -u lowpriv -p pass -d corp.local
# Empire 生态,自动 BloodHound+自动提权
```

## 注意事项

自动化 AD 攻击框架,Empire 联动。
