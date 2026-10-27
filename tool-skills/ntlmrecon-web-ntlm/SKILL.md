---
name: ntlmrecon-web-ntlm
description: ntlmrecon: NTLM 认证端点全网发现。信号:ad攻击,域渗透,NTLM 端点枚举,网段。
---

# ntlmrecon

- 攻击大类:C30 AD域渗透与域控攻击
- 上游仓库:https://github.com/sachinkamath/ntlmrecon
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install ntlmrecon
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `ntlmrecon -d t.com -i urls.txt` | NTLM 端点枚举 |
| `-d domain -t 10.0.0.0/24` | 网段 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### NTLM 认证端点全网发现

```bash
ntlmrecon -d t.com -i webpaths.txt
# Exchange/OWA/Autodiscover NTLM 枚举
```

## 注意事项

Web NTLM 端点枚举+信息提取。
