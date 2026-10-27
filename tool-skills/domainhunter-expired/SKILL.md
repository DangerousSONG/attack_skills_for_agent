---
name: domainhunter-expired
description: DomainHunter: 挑钓鱼域名(高信誉过期域名)。信号:钓鱼,社会工程,搜过期可注册域名,查分类信誉,过滤成人类。
---

# DomainHunter

- 攻击大类:C08 钓鱼与社会工程
- 上游仓库:https://github.com/threatexpress/domainhunter
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/threatexpress/domainhunter && cd domainhunter && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python domainhunter.py -k keywords.txt` | 搜过期可注册域名 |
| `-c` | 查分类信誉 |
| `-f` | 过滤成人类 |
| `-t` | 用 Tor 查信誉 |
| `-r` | 只显示可注册 |

## 攻击场景 Playbook

### 挑钓鱼域名(高信誉过期域名)

```bash
python domainhunter.py -k 'security,login,update' -c -r
# 输出可注册域名+BlueCoat/McAfee 分类,挑'企业/金融'类注册做钓鱼基础设施
```

## 注意事项

自动查过期域名在 Symantec BlueCoat 的分类信誉;分类良好的域名能过邮件网关。
