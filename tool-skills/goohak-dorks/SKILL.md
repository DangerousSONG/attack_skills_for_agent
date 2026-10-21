---
name: goohak-dorks
description: 渗透工具 skill:GooHak 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 GooHak 时使用。
when-to-use: 渗透工具 skill:GooHak 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 GooHak 时使用。
---

# GooHak

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/1N3/Goohak
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/1N3/Goohak && cd Goohak
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./goohak.sh target.com` | 自动跑 20+ Google Dork |
| `输出` | 多个浏览器标签打开结果 |

## 攻击场景 Playbook

### Google Hacking 自动化

```bash
./goohak.sh corp.com  # site:corp.com 敏感路径/泄露/后台 dork 一键跑
```

## 注意事项

1N3 出品;Google dork 自动化,懒人包。
