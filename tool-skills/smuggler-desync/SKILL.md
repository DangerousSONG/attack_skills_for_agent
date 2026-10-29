---
name: smuggler-desync
description: "Smuggler: frontend and CDN smuggling detection. Signals: web vulnerability, injection, HTTP request smuggling detection, detailed, deep mode."
zh-signals: "Smuggler: 前端/CDN 走私检测。信号:web漏洞,注入,HTTP 请求走私检测,详细,深入模式。"
---

# Smuggler

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/defparam/smuggler
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/defparam/smuggler
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python smuggler.py -u https://t.com` | HTTP 请求走私检测 |
| `-v 2` | 详细 |
| `-x` | 深入模式 |
| `-m GET` | 方法 |
| `--no-color` | 无颜色 |

## 攻击场景 Playbook

### 前端/CDN 走私检测

```bash
python smuggler.py -u https://target -v 2
# 测试 CL.TE/TE.CL/TE.TE 混淆,命中给完整 PoC 请求
```

## 注意事项

HTTP Desync 检测标杆;命中后按其 PoC 构造走私请求绕过前端 ACL 打内网。
