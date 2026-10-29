---
name: corscanner-cors-misconfig
description: "CORScanner: Scans for CORS cross-origin hijacking. Signals: web vulnerability, injection, CORS configuration scanning, batch, threads."
zh-signals: "CORScanner: CORS 跨域劫持。信号:web漏洞,注入,CORS 配置扫描,批量,线程。"
---

# CORScanner

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/chenjj/CORScanner
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/chenjj/CORScanner && cd CORScanner && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python cors_scan.py -u https://t.com` | CORS 配置扫描 |
| `-i urls.txt` | 批量 |
| `-t 100` | 线程 |
| `-o out.json` | JSON 输出 |
| `-d example.com` | 自定义 Origin 测试 |

## 攻击场景 Playbook

### CORS 跨域劫持

```bash
python cors_scan.py -i subs.txt -t 100
# 命中 ACAO 反射任意源且 ACAC=true → 偷 token
```

## 注意事项

检测 CORS 误配置(任意源反射/null origin/前缀匹配),输出可利用的 origin 列表。
