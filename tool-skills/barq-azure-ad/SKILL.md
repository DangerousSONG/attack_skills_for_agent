---
name: barq-azure-ad
description: "barq: sprays Azure AD passwords. Signals: brute force, password spraying, Azure AD spraying, conditional access probing"
zh-signals: "barq: Azure AD 密码喷洒。信号:暴力破解,口令喷射,Azure AD 喷洒,条件访问探测。"
---

# barq

- 攻击大类:C28 暴力破解与口令喷射
- 上游仓库:https://github.com/Voulnet/barq
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install barq
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `barq -u user@corp.com -p pass.txt` | Azure AD 喷洒 |
| `-u u -p p -c` | 条件访问探测 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### Azure AD 密码喷洒

```bash
barq -u admin@corp.com -p top100.txt
# 智能识别条件访问
```

## 注意事项

Azure AD 喷洒工具。
