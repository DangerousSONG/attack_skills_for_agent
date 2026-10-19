---
name: opendoor-scanner
description: 渗透工具 skill:OpenDoor 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 OpenDoor 时使用。
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
