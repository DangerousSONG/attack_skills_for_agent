---
name: feroxbuster-content-discovery
description: "feroxbuster performs recursive content discovery and API endpoint brute-forcing. Signals: web scanning, vulnerability scanning, single-target scan, deep recursion."
zh-signals: "feroxbuster: 递归内容发现、API 端点爆破。信号:web扫描,漏洞扫描,单目标扫描,深度递归。"
---

# feroxbuster

- 攻击大类:C41 Web漏洞扫描与验证
- 上游仓库:https://github.com/epi052/feroxbuster
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
cargo install feroxbuster 或 brew install feroxbuster;也有单二进制 release
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-u URL` | 单目标扫描 |
| `--deep-scan` | 深度递归 |
| `-w wordlist -x php js` | 多扩展名 |
| `-C 403` | 过滤状态码 |
| `--collect-extensions` | 从响应自动收集新扩展名 |
| `--smart-scan` | 先 HEAD 探测再 GET 确认 |
| `-r` | follow redirects |
| `--insecure` | 忽略 TLS 证书错误 |

## 攻击场景 Playbook

### 递归内容发现

```bash
feroxbuster -u https://target.com -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt -x php,js,html -C 404,403 -t 80
```

### API 端点爆破

```bash
feroxbuster -u https://api.target.com/v1 -w endpoints.txt -C 404 -r --insecure
```

## 注意事项

Rust 编写速度极快,支持从响应自动学习扩展名;状态码过滤用 -C(排除)而非 -x。
