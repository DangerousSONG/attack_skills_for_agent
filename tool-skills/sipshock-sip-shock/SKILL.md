---
name: sipshock-sip-shock
description: "sipshock: SIP device Shellshock testing. Signals: port scan, nmap, Range."
zh-signals: "sipshock: SIP 设备 Shellshock。信号:端口扫描,nmap,Range。"
---

# sipshock

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/zaf/sipshock
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/zaf/sipshock@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `sipshock -t 10.0.0.5` | SIP Shellshock 扫描 |
| `-t ip -r` | Range |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### SIP 设备 Shellshock

```bash
sipshock -t 10.0.0.0/24
# CVE-2014-6271 SIP 头注入
```

## 注意事项

SIP 协议 Shellshock 检测。
