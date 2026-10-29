---
name: xsscon-xss
description: "XSSCon: Reflected/stored XSS probing. Signals: web vulnerability, injection, XSS scan, with cookie, threads."
zh-signals: "XSSCon: 反射/存储 XSS 探测。信号:web漏洞,注入,XSS 扫描,带 Cookie,线程。"
---

# XSSCon

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/menkrep1337/XSSCon
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/menkrep1337/XSSCon && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 xsscon.py -u 'https://t.com/?q=x'` | XSS 扫描 |
| `-u url --cookies 'x=1'` | 带 Cookie |
| `-u url -t 10` | 线程 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 反射/存储 XSS 探测

```bash
python3 xsscon.py -u 'https://t.com/search?q=test'
# DOM/反射双模式
```

## 注意事项

轻量 XSS 扫描器,支持 Cookie 认证。
