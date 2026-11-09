---
name: finalrecon-allinone
description: "FinalRecon generates a full OSINT report for a single target. Signals: asset mapping, subdomains, full reconnaissance, DNS only, subdomains only."
zh-signals: "FinalRecon: 单目标全量 OSINT 报告。信号:资产测绘,子域名,全量侦察,仅 DNS,仅子域。"
---

# FinalRecon

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/thewhiteh4t/FinalRecon
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/thewhiteh4t/FinalRecon && cd FinalRecon && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 finalrecon.py --full https://target.com` | 全量侦察 |
| `--dns` | 仅 DNS |
| `--sub` | 仅子域 |
| `--dir` | 仅目录 |
| `--wayback` | 仅历史 |
| `-o dir` | 输出 |

## 攻击场景 Playbook

### 单目标全量 OSINT 报告

```bash
python3 finalrecon.py --full https://target.com -o report
# DNS/WHOIS/子域/目录/端口/技术栈/证书/历史一次出 Markdown 报告
```

## 注意事项

模块化报告型侦察,输出适合直接贴进渗透报告附录。
