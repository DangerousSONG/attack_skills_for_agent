---
name: v3n0m-sql-xss
description: V3n0M-Scanner: 多漏洞批量扫描。信号:web漏洞,注入,dork 扫描,SSRF 模式,XSS 模式。
---

# V3n0M-Scanner

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/v3n0m-Scanner/V3n0M-Scanner
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/v3n0m-Scanner/V3n0M-Scanner && cd V3n0M-Scanner && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 v3n0m.py -d 'dork' -p 10` | dork 扫描 |
| `-s 'dork' -x ssrf` | SSRF 模式 |
| `-s dork -x xss` | XSS 模式 |
| `-f out.txt` | 输出 |

## 攻击场景 Playbook

### 多漏洞批量扫描

```bash
python3 v3n0m.py -d 'inurl:php?id=' -p 20
# SQLi/XSS/SSRF/LFI 四合一
```

## 注意事项

老牌批量漏洞扫描,支持 6 种漏洞类型。
