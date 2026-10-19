---
name: juumla-joomla-check
description: 渗透工具 skill:juumla 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 juumla 时使用。
---

# juumla

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/oppsec/juumla
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install juumla
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `juumla -u https://t.com` | Joomla 检测+漏洞扫描 |
| `-u url --backup-files` | 备份文件探测 |
| `-u url -c` | 组件检测 |

## 攻击场景 Playbook

### Joomla 快速体检

```bash
juumla -u https://t.com
# 版本/CVE/备份文件/可读配置一次出
```

## 注意事项

轻量 Joomla 扫描,oppsec 出品。
