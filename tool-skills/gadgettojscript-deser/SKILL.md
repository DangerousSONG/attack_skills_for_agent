---
name: gadgettojscript-deser
description: "GadgetToJScript builds Office macro deserialization payloads. Signals: payload development, weaponization, .NET serialized payloads, VBS output, obfuscation."
zh-signals: "GadgetToJScript: Office 宏反序列化。信号:载荷开发,武器化,.NET 序列化载荷,VBS 输出,混淆。"
---

# GadgetToJScript

- 攻击大类:C07 载荷开发与武器化
- 上游仓库:https://github.com/med0x2e/GadgetToJScript
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/med0x2e/GadgetToJScript && cd GadgetToJScript && dotnet build
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `GadgetToJScript.exe -b -c -e binary -w vba -o macro` | .NET 序列化载荷 |
| `-e binary -w vbs` | VBS 输出 |
| `-c` | 混淆 |

## 攻击场景 Playbook

### Office 宏反序列化

```bash
GadgetToJScript.exe -b -e shellcode -w vba -o invoice
# 宏内 .NET 反序列化执行
```

## 注意事项

.NET 序列化载荷嵌入 Office 文档。
