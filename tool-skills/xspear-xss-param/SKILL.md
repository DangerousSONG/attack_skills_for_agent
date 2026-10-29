---
name: xspear-xss-param
description: "XSpear: Parameter-level XSS validation. Signals: web vulnerability, injection, XSS scan, POST data, header injection."
zh-signals: "XSpear: 参数级 XSS 验证。信号:web漏洞,注入,XSS 扫描,POST 数据,头注入。"
---

# XSpear

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/hahwul/XSpear
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
gem install XSpear
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `XSpear -u 'https://t.com/?q=123'` | XSS 扫描 |
| `-d 'q=123'` | POST 数据 |
| `--headers='Cookie: a=1'` | 头注入 |
| `-b http://127.0.0.1:8080` | 过 Burp |
| `--filter-body='unique'` | 过滤 |
| `-v` | 详细 |

## 攻击场景 Playbook

### 参数级 XSS 验证

```bash
XSpear -u 'https://target/item?id=1' -b http://127.0.0.1:8080
# 结果同步到 Burp 人工确认;支持 blind XSS 回调
```

## 注意事项

Ruby 写的 XSS 专用扫描;报告按参数分组,配 Burp 做二次确认效率高。
