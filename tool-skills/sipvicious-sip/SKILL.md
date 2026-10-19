---
name: sipvicious-sip
description: 渗透工具 skill:SIPVicious 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 SIPVicious 时使用。
---

# SIPVicious

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/EnableSecurity/sipvicious
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install sipvicious
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `svmap 10.0.0.0/24` | SIP 设备发现 |
| `svwar -m INVITE 10.0.0.5` | 分机枚举 |
| `svcrack -u 100 -d wordlist.txt 10.0.0.5` | SIP 爆破 |
| `svreport -t onlinehosts` | 报告 |

## 攻击场景 Playbook

### VoIP 内网渗透

```bash
svmap 10.0.0.0/24 && svwar -m INVITE 10.0.0.5
# 发现+枚举+爆破
```

## 注意事项

EnableSecurity 出品,VoIP 安全测试标准工具。
