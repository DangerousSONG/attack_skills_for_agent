---
name: stews-websocket-scan
description: "STEWS discovers WebSocket endpoints. Signals: web vulnerability, injection, vulnerability detection"
zh-signals: "STEWS: WebSocket 端点发现。信号:web漏洞,注入,漏洞检测。"
---

# STEWS

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/PalindromeLabs/STEWS
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/PalindromeLabs/STEWS && cd STEWS
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 stews.py -u wss://t.com/ws` | WebSocket 安全扫描 |
| `-u url -m discovery` | 端点发现 |
| `-u url -m vuln` | 漏洞检测 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### WebSocket 端点发现

```bash
python3 stews.py -u wss://api.t.com -m discovery
# 发现隐藏 ws 端点+弱鉴权
```

## 注意事项

WebSocket 专项扫描框架,Palindrome Labs 出品。
