---
name: webpwn3r-xss-scan
description: "webpwn3r: Parameter-level vulnerability scanning. Signals: web vulnerabilities, injection, XSS/injection scan, batch."
zh-signals: "webpwn3r: 参数级漏洞扫描。信号:web漏洞,注入,XSS/注入扫描,批量。"
---

# webpwn3r

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/zigoo0/webpwn3r
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/zigoo0/webpwn3r
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python webpwn3r.py -u https://t.com` | XSS/注入扫描 |
| `-u url -w urls.txt` | 批量 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 参数级漏洞扫描

```bash
python webpwn3r.py -u https://t.com
# 对爬到的参数逐一测试
```

## 注意事项

参数量级 Web 漏洞扫描。
