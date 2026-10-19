---
name: stews-websocket-scan
description: 渗透工具 skill:STEWS 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 STEWS 时使用。
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
