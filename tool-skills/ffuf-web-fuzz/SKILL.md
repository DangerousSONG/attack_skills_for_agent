---
name: ffuf-web-fuzz
description: "ffuf fuzzes directories and parameters, including simultaneous multi-location payloads. Signals: web scanning, vulnerability scanning, wordlists, multiple wordlists, placeholders."
zh-signals: "ffuf: 目录与参数点 fuzz、多位置同时 fuzz(用户+ID)。信号:web扫描,漏洞扫描,字典文件,多字典多占位符。"
---

# ffuf

- 攻击大类:C41 Web漏洞扫描与验证
- 上游仓库:https://github.com/ffuf/ffuf
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/ffuf/ffuf/v2@latest
# 或 apt install ffuf (Kali 自带)
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-u URL/FUZZ` | FUZZ 占位符被字典逐行替换 |
| `-w /path/wordlist.txt` | 字典文件 |
| `-w wl.txt:FUZZ2` | 多字典多占位符 |
| `-mc 200,301,302` | 只保留指定状态码 |
| `-fc 404` | 过滤状态码 |
| `-ac` | 自动校准,过滤软 404 与相似页面 |
| `-rate 100` | 全局请求限速 |
| `-t 80` | 线程数 |
| `-recursion -recursion-depth 2` | 递归发现新目录 |
| `-H "Cookie: session=xxx"` | 带认证头扫描后台 |
| `-o result.json -of json` | JSON 输出供脚本消费 |

## 攻击场景 Playbook

### 目录与参数点 fuzz

```bash
ffuf -u https://target.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt -ac -t 80
ffuf -u "https://target.com/api/FUZZ=test" -w params.txt -mc 200 -ac
```

### 多位置同时 fuzz(用户+ID)

```bash
ffuf -u https://target.com/users/FUZZ/orders/FUZZ2 -w users.txt:FUZZ -w ids.txt:FUZZ2 -ac
```

### 带登录态扫后台功能点

```bash
ffuf -u https://target.com/admin/FUZZ -w endpoints.txt -H "Cookie: session=admin_token" -mc 200,302 -o admin_fuzz.json -of json
```

## 注意事项

FUZZ 占位符大小写敏感(全大写);上线前必开 `-ac` 否则结果被软 404 淹没;结果用 `-of json` 导出便于二次处理。
