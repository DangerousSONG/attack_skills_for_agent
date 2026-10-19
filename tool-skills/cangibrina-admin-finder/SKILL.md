---
name: cangibrina-admin-finder
description: 渗透工具 skill:cangibrina 的安装、参数速查与攻击场景 playbook。当任务涉及 Web漏洞扫描与验证 需要调用 cangibrina 时使用。
---

# cangibrina

- 攻击大类:C41 Web漏洞扫描与验证
- 上游仓库:https://github.com/fnk0c/cangibrina
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/fnk0c/cangibrina && cd cangibrina
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python cangibrina.py -u https://t.com` | 后台扫描 |
| `-u url -w wordlist.txt` | 字典 |
| `-t 20` | 线程 |

## 攻击场景 Playbook

### 后台地址发现

```bash
python cangibrina.py -u https://t.com -w /usr/share/wordlists/dirb/common.txt
# 多引擎后台爆破
```

## 注意事项

多引擎后台发现工具。
