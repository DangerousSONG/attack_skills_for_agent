---
name: net-creds-sniff
description: 渗透工具 skill:net-creds 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 net-creds 时使用。
---

# net-creds

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/DanMcInerney/net-creds
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/DanMcInerney/net-creds && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python net-creds.py -i eth0` | 被动凭据嗅探 |
| `-i eth0 -f` | 过滤本机 |
| `-p` | PCAP 分析 |

## 攻击场景 Playbook

### 内网凭据被动收割

```bash
python net-creds.py -i eth0
# HTTP/FTP/POP/SNMP 凭据全收
```

## 注意事项

被动嗅探凭据,协议覆盖全。
