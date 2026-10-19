---
name: smbsr-smb-regret
description: 渗透工具 skill:SMBSR 的安装、参数速查与攻击场景 playbook。当任务涉及 内网发现与枚举 需要调用 SMBSR 时使用。
---

# SMBSR

- 攻击大类:C29 内网发现与枚举
- 上游仓库:https://github.com/oldboy21/SMBSR
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/oldboy21/SMBSR && cd SMBSR
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./smbsr -r 10.0.0.0/24 -u user -p pass` | SMB 内容搜索 |
| `-r cidr -f 'passw|token'` | 正则 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 内网密码文件全网搜

```bash
./smbsr -r 10.0.0.0/24 -f 'password|passwd|pwd'
# 找脚本/文档中的明文密码
```

## 注意事项

SMB 内容搜索工具,正则匹配文件名+内容。
