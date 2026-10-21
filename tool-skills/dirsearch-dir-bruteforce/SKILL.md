---
name: dirsearch-dir-bruteforce
description: 渗透工具 skill:dirsearch 的安装、参数速查与攻击场景 playbook。当任务涉及 Web漏洞扫描与验证 需要调用 dirsearch 时使用。
when-to-use: 渗透工具 skill:dirsearch 的安装、参数速查与攻击场景 playbook。当任务涉及 Web漏洞扫描与验证 需要调用 dirsearch 时使用。
---

# dirsearch

- 攻击大类:C41 Web漏洞扫描与验证
- 上游仓库:https://github.com/maurosoria/dirsearch
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install dirsearch 或 git clone https://github.com/maurosoria/dirsearch
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-u URL -e php,html,bak` | 扩展名枚举目录 |
| `-w /path/wordlist.txt` | 自定义字典 |
| `-r -R 3` | 递归扫描 3 层 |
| `--exclude-status=403,404` | 过滤无效状态码 |
| `-t 50` | 50 线程 |
| `-x 302` | 排除重定向 |
| `--proxy=http://127.0.0.1:8080` | 过 Burp 调试 |

## 攻击场景 Playbook

### 后台与备份文件发现

```bash
dirsearch -u https://target.com -e php,bak,old,zip -t 80 --exclude-status=404
dirsearch -u https://target.com/admin/ -r -R 2
```

## 注意事项

默认字典在 db/ 目录;扫到 .git/.env/.bak 是常见突破口。
