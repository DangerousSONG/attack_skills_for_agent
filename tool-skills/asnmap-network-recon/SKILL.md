---
name: asnmap-network-recon
description: "asnmap: maps all enterprise network ranges for a target ASN. Signals: network topology, internet mapping, asnmap"
zh-signals: "asnmap: 目标企业网段全量测绘。信号:网络拓扑,互联网测绘,asnmap`。"
---

# asnmap

- 攻击大类:C04 网络拓扑测绘
- 上游仓库:https://github.com/projectdiscovery/asnmap
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/projectdiscovery/asnmap/cmd/asnmap@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `echo corp.com | asnmap` | 域名→ASN/CIDR |
| `asnmap -a AS15169 -silent` | 按 ASN 出 CIDR 列表 |
| `cat ips.txt | asnmap -json` | 批量 IP→ASN 归属 |

## 攻击场景 Playbook

### 目标企业网段全量测绘

```bash
echo corp.com | asnmap -silent | tee cidrs.txt
# 出该企业全部 ASN+CIDR,喂 amass/nmap 全量扫描
```

## 注意事项

ProjectDiscovery 出品,IP→ASN/CIDR 映射,摸清企业网段资产边界。
