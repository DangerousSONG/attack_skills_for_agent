---
name: petools-pe-analysis
description: 渗透工具 skill:pe-tools 的安装、参数速查与攻击场景 playbook。当任务涉及 逆向工程辅助 需要调用 pe-tools 时使用。
when-to-use: 渗透工具 skill:pe-tools 的安装、参数速查与攻击场景 playbook。当任务涉及 逆向工程辅助 需要调用 pe-tools 时使用。
---

# pe-tools

- 攻击大类:C47 逆向工程辅助
- 上游仓库:https://github.com/petoolse/petools
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/petoolse/petools
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 pe_parser.py sample.exe` | PE 结构解析(IAT/节/资源) |
| `-v` | 详细输出 |
| `-d` | DOS 头解析 |
| `--extract-resources` | 提取资源 |

## 攻击场景 Playbook

### PE 文件静态解剖

```bash
python3 pe_parser.py malware.exe -v
# 导入表看功能(联网/注入 API),节名看壳(UPX/VMProtect)
```

## 注意事项

纯 Python PE 解析器,无依赖看 PE 头/节/IAT/资源,免杀分析第一步。
