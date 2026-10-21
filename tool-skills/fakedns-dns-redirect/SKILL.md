---
name: fakedns-dns-redirect
description: 渗透工具 skill:FakeDns 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 FakeDns 时使用。
when-to-use: 渗透工具 skill:FakeDns 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 FakeDns 时使用。
---

# FakeDns

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/Crypt0s/FakeDns
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Crypt0s/FakeDns && cd FakeDns
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 fakedns.py -c dns.conf` | DNS 伪造 |
| `fakedns.py --rebind` | 重绑定 |
| `--non authoritative` | 非权威 |

## 攻击场景 Playbook

### DNS 钓鱼重定向

```bash
echo '*.corp.com 10.0.0.5' > dns.conf && python3 fakedns.py -c dns.conf
# 内网 DNS 劫持钓鱼
```

## 注意事项

可配置 DNS 伪造,支持重绑定。
