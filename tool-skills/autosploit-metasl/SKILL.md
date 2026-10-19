---
name: autosploit-metasl
description: 渗透工具 skill:AutoSploit 的安装、参数速查与攻击场景 playbook。当任务涉及 二进制漏洞利用与Pwn 需要调用 AutoSploit 时使用。
---

# AutoSploit

- 攻击大类:C46 二进制漏洞利用与Pwn
- 上游仓库:https://github.com/NullArray/AutoSploit
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/NullArray/AutoSploit && cd AutoSploit && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python autosploit.py -e -q apache -c` | Shodan 搜目标并自动喂 Metasploit |
| `-f hosts.txt` | 本地目标清单 |
| `-p default` | 默认端口集 |
| `--exploit-only -f x.txt` | 只对清单跑 exploit |

## 攻击场景 Playbook

### 批量 CVE 自动打点(授权靶场)

```bash
python autosploit.py -e -q 'Hikvision' -c -p default
# 调 Shodan→选目标→逐台套 Metasploit 模块
```

## 注意事项

全自动但噪声大,误报/破坏风险高;仅限授权靶场/演练环境。
