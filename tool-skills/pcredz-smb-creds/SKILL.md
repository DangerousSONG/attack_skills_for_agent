---
name: pcredz-smb-creds
description: 渗透工具 skill:PCredz 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 PCredz 时使用。
---

# PCredz

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/lgandx/PCredz
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/lgandx/PCredz && cd PCredz
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3Pcredz -i eth0` | 流量凭据提取 |
| `-f capture.pcap` | PCAP 分析 |
| `-v` | 详细 |

## 攻击场景 Playbook

### SMB/HTTP 凭据嗅探

```bash
python3 Pcredz -i eth0
# NTLM 哈希/HTTP Basic/Kerberos 全收
```

## 注意事项

lgandx 出品(Responder 作者),流量凭据提取。
