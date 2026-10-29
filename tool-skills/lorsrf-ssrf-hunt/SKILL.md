---
name: lorsrf-ssrf-hunt
description: "lorsrf: Batch SSRF probing. Signals: web vulnerability, injection, SSRF parameter testing, OOB receiver, batch URLs."
zh-signals: "lorsrf: SSRF 批量探测。信号:web漏洞,注入,SSRF 参数测试,OOB 接收,批量 URL。"
---

# lorsrf

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/knassar702/lorsrf
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/knassar702/lorsrf && cd lorsrf
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./lorsrf -u 'https://t.com/?u=x' -p u` | SSRF 参数测试 |
| `-u url -b http://burp.collab` | OOB 接收 |
| `-w wordlist.txt` | 批量 URL |

## 攻击场景 Playbook

### SSRF 批量探测

```bash
./lorsrf -u urls.txt -b http://vps.interactsh.com
# 全参数注入回调 payload
```

## 注意事项

SSRF 探测工具,支持 OOB 回调验证。
