---
name: lorsrf-ssrf-hunt
description: 渗透工具 skill:lorsrf 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 lorsrf 时使用。
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
