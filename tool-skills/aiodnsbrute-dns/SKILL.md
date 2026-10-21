---
name: aiodnsbrute-dns
description: 渗透工具 skill:aiodnsbrute 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 aiodnsbrute 时使用。
when-to-use: 渗透工具 skill:aiodnsbrute 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 aiodnsbrute 时使用。
---

# aiodnsbrute

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/blark/aiodnsbrute
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install aiodnsbrute
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `aiodnsbrute -w wordlist.txt -t 500 corp.com` | 异步 DNS 爆破 |
| `-w w.txt -t t -o out.txt` | 输出 |
| `--max-tasks 5000` | 并发 |

## 攻击场景 Playbook

### 百万级子域爆破

```bash
aiodnsbrute -w all.txt -t 2000 corp.com
# asyncio 异步,速度碾压 dnsrecon
```

## 注意事项

异步 DNS 爆破,性能极强。
