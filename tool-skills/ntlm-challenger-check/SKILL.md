---
name: ntlm-challenger-check
description: "Extract NTLM information leakage. Signals: AD attack, domain penetration, parse NTLM authentication headers."
zh-signals: "ntlm-challenger: NTLM 信息泄露提取。信号:ad攻击,域渗透,解析 NTLM 认证头。"
---

# ntlm-challenger

- 攻击大类:C30 AD域渗透与域控攻击
- 上游仓库:https://github.com/b17zr/ntlm_challenger
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install ntlm-challenger
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `ntlm-challenger http://t.com/ntlm-auth` | 解析 NTLM 认证头 |
| `-t url -o out.txt` | 输出 |

## 攻击场景 Playbook

### NTLM 信息泄露提取

```bash
ntlm-challenger http://mail.t.com/autodiscover
# 提取域名/主机/版本,内网画像
```

## 注意事项

解析 HTTP NTLM 质询头,泄露内网信息。
