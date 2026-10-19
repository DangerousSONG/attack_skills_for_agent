---
name: ja3-fingerprint
description: 渗透工具 skill:JA3 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 JA3 时使用。
---

# JA3

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/salesforce/ja3
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/salesforce/ja3
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python ja3.py -r traffic.pcap` | 从 pcap 提 TLS 指纹 |
| `ja3 指纹库比对` | 识别 malware/C2 家族 |

## 攻击场景 Playbook

### TLS 指纹威胁识别

```bash
python ja3.py -r capture.pcap | jq '.ja3'
# 指纹与公开库比对,识别 C2/恶意软件家族(即使加密)
```

## 注意事项

Salesforce 的 TLS 指纹标准;JA3S/JA4 同源,是加密流量威胁狩猎的基础。
