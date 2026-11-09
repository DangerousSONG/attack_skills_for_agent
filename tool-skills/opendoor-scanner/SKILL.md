---
name: opendoor-scanner
description: "Directory scanning with multiple reports. Signals: web vulnerability, injection, wordlist, threads, specified paths."
zh-signals: "OpenDoor: 目录扫描+多报告。信号:web漏洞,注入,字典,线程,指定路径。"
---

# OpenDoor

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/stanislav-web/OpenDoor
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/stanislav-web/OpenDoor && cd OpenDoor && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 opendoor.py --host https://t.com` | 目录扫描 |
| `--wordlist /usr/share/wordlists/dirb/common.txt` | 字典 |
| `--threads 25` | 线程 |
| `--scan-dir /admin,/backup` | 指定路径 |
| `--report json` | 报告 |

## 攻击场景 Playbook

### 目录扫描+多报告

```bash
python3 opendoor.py --host https://t.com --threads 50 --report json
# HTML/JSON/TXT 三种报告,适合交付
```

## 注意事项

目录/后台扫描器,多线程+代理支持,报告输出齐全。
