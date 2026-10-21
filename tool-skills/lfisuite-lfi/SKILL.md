---
name: lfisuite-lfi
description: 渗透工具 skill:LFISuite 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 LFISuite 时使用。
when-to-use: 渗透工具 skill:LFISuite 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 LFISuite 时使用。
---

# LFISuite

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/D35m0nd142/LFISuite
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/D35m0nd142/LFISuite && cd LFISuite
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python lfisuite.py` | 交互菜单 |
| `选择 [1] 自动 LFI 扫描` | 目标 URL |
| `Log poison 模块` | 日志投毒 getshell |
| `phpinfo 模块` | 通过 phpinfo 落地文件 |

## 攻击场景 Playbook

### 全自动 LFI 打点

```bash
python lfisuite.py
# 输入目标 → 自动遍历绕过技巧(filter/日志/会话/phpinfo) → 交互 shell
```

## 注意事项

把 LFI 所有手工技巧集成化;日志投毒和 phpinfo+临时文件两条链都内置。
