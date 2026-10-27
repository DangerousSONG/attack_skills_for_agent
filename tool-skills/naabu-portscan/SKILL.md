---
name: naabu-portscan
description: naabu: 与 nmap 联动的攻击面流水线。信号:端口扫描,nmap,单目标,批量,top 100 端口。
---

# naabu

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/projectdiscovery/naabu
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-host target.com` | 单目标 |
| `-list hosts.txt` | 批量 |
| `-top-ports 100` | top 100 端口 |
| `-p -` | 全端口 |
| `-rate 3000` | 速率 |
| `-nmap-cli 'nmap -sV -oX nmap-output.xml'` | 发现端口后自动联动 nmap |

## 攻击场景 Playbook

### 与 nmap 联动的攻击面流水线

```bash
naabu -list subdomains.txt -top-ports 1000 -rate 5000 -nmap-cli 'nmap -sV -sC -oX nmap.xml'
# naabu 快速筛存活端口,nmap 接管服务指纹与脚本扫描
```

## 注意事项

pd 生态标准件;-nmap-cli 是灵魂,把快扫和深扫串成一条命令。
