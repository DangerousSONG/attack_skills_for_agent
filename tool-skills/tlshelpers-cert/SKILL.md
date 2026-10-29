---
name: tlshelpers-cert
description: "tlshelpers performs quick TLS checks. Signals: cryptographic attack, cryptographic cracking, certificate download, cipher scan, PCAP analysis"
zh-signals: "tlshelpers: TLS 快速检查。信号:密码学攻击,加密破解,证书下载,套件扫描,PCAP 分析。"
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
