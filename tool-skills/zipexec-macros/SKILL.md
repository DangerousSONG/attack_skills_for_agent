---
name: zipexec-macros
description: 渗透工具 skill:ZipExec 的安装、参数速查与攻击场景 playbook。当任务涉及 载荷开发与武器化 需要调用 ZipExec 时使用。
when-to-use: 渗透工具 skill:ZipExec 的安装、参数速查与攻击场景 playbook。当任务涉及 载荷开发与武器化 需要调用 ZipExec 时使用。
---

# ZipExec

- 攻击大类:C07 载荷开发与武器化
- 上游仓库:https://github.com/Tylous/ZipExec
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Tylous/ZipExec && cd ZipExec && go build
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./ZipExec -I payload.exe -O out.js` | EXE 藏 JS |
| `-I shellcode.bin -O out.ps1` | shellcode 转 PS |
| `-a` | 附加选项 |

## 攻击场景 Playbook

### 载荷免杀投递

```bash
./ZipExec -I beacon.exe -O invoice.js
# 双扩展钓鱼附件
```

## 注意事项

Tylous 出品,EXE 转 JS/PS 载荷,绕过文件过滤。
