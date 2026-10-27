---
name: exe2hexbat-payload-transfer
description: exe2hex: 无文件落地传二进制。信号:逆向,反汇编,C 代码格式。
---

# exe2hex

- 攻击大类:C47 逆向工程辅助
- 上游仓库:https://github.com/g0tmi1k/exe2hex
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/g0tmi1k/exe2hex && cd exe2hex
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `bash exe2hex.sh -x /usr/share/windows-binaries/nc.exe -e nc.cmd` | exe→BAT/TXT 转移 |
| `-b` | PowerShell/BAT 混合 |
| `-cc` | C 代码格式 |

## 攻击场景 Playbook

### 无文件落地传二进制

```bash
bash exe2hex.sh -x procdump.exe -e dump.cmd
# 把 exe 编码成 cmd 脚本, echo 重组成 exe,过白名单
```

## 注意事项

g0tmi1k 出品,把二进制转成 BAT/PowerShell 脚本重建,适合禁止上传环境的载荷传递。
