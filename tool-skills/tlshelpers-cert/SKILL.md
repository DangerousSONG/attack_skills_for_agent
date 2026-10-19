---
name: tlshelpers-cert
description: 渗透工具 skill:tlshelpers 的安装、参数速查与攻击场景 playbook。当任务涉及 密码学攻击 需要调用 tlshelpers 时使用。
---

# tlshelpers

- 攻击大类:C49 密码学攻击
- 上游仓库:https://github.com/hannob/tlshelpers
- 上游 License:0BSD(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/hannob/tlshelpers
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./getcert.sh t.com` | 证书下载 |
| `./cipherscan.sh t.com` | 套件扫描 |
| `./sniffer2ciphers.py pcap` | PCAP 分析 |

## 攻击场景 Playbook

### TLS 快速检查

```bash
./getcert.sh t.com > cert.pem
# 证书链分析
```

## 注意事项

Hanno Böck 的 TLS 检查脚本集。
