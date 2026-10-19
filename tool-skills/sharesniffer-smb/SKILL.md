---
name: sharesniffer-smb
description: 渗透工具 skill:sharesniffer 的安装、参数速查与攻击场景 playbook。当任务涉及 内网发现与枚举 需要调用 sharesniffer 时使用。
---

# sharesniffer

- 攻击大类:C29 内网发现与枚举
- 上游仓库:https://github.com/shirosaidev/sharesniffer
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/shirosaidev/sharesniffer && cd sharesniffer
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 sharesniffer.py -h 10.0.0.0/24` | SMB 共享嗅探 |
| `-h cidr -u user -p pass` | 凭据 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 内网共享批量发现

```bash
python3 sharesniffer.py -h 10.0.0.0/24
# 匿名+认证双模式
```

## 注意事项

SMB 共享发现+访问测试。
