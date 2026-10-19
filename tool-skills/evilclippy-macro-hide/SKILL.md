---
name: evilclippy-macro-hide
description: 渗透工具 skill:EvilClippy 的安装、参数速查与攻击场景 playbook。当任务涉及 免杀与载荷投递 需要调用 EvilClippy 时使用。
---

# EvilClippy

- 攻击大类:C45 免杀与载荷投递
- 上游仓库:https://github.com/outflanknl/EvilClippy
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/outflanknl/EvilClippy && 用 mono/xbuild 编译
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `EvilClippy.exe -s fakecode.vba macro.doc` | VBA 代码欺骗(分析器看错代码) |
| `-g` | GUI 混淆 |
| `-r` | 移除宏 VBA 项目 |
| `-u` | URL 注入宏 |
| `-st` | VBA stomping |

## 攻击场景 Playbook

### 宏文档免杀

```bash
EvilClippy.exe -s benign.vba payload.docm
# 预览/沙箱看到 benign 宏,实际执行 stomped p-code
```

## 注意事项

Outflank 出品,Office 宏武器化: VBA stomping(源码与 p-code 分离)+GUI 伪装,绕过多数杀软静态查杀。
