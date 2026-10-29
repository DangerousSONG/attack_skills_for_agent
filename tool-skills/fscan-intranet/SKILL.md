---
name: fscan-intranet
description: "fscan performs one-shot internal initial scans and deep single-host validation. Signals: port scanning, nmap, specified ports, single module."
zh-signals: "fscan: 内网一把梭初扫、单主机深度验证。信号:端口扫描,nmap,指定端口,单模块。"
---

# fscan

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/shadow1ng/fscan
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
release 下载 fscan.exe / fscan
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `fscan -h 192.168.0.0/16` | 全功能扫(端口+服务+弱口令+漏洞) |
| `-h ip -p 22,80,3306` | 指定端口 |
| `-m smb` | 单模块 |
| `-user admin -pwd admin` | 爆破凭据 |
| `-nopoc` | 禁漏洞探测 |
| `-o result.txt` | 见上游文档 |
| `输出` | 见上游文档 |

## 攻击场景 Playbook

### 内网一把梭初扫

```bash
fscan -h 10.0.0.0/16 -o result.txt
# 自动: 存活→端口→服务指纹→默认凭据→MS17-010/永恒之蓝等内置 POC
```

### 单主机深度验证

```bash
fscan -h 10.0.0.5 -m all -user administrator -pwd 'Admin@123'
```

## 注意事项

国产红队内网神器,内置 POC 库(2021-2023 为主)注意时效;输出对接到 CSV 很规整。
