---
name: sslyze-deep-tls
description: sslyze: 合规级 TLS 评估。信号:密码学攻击,加密破解,TLS 深度扫描,合规检查,证书链详情。
---

# sslyze

- 攻击大类:C49 密码学攻击
- 上游仓库:https://github.com/nabla-c0d3/sslyze
- 上游 License:AGPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install sslyze
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `sslyze t.com` | TLS 深度扫描 |
| `sslyze --mozilla_config=intermediate t.com` | 合规检查 |
| `sslyze --certinfo t.com` | 证书链详情 |
| `-j out.json` | JSON 输出 |

## 攻击场景 Playbook

### 合规级 TLS 评估

```bash
sslyze --mozilla_config=modern t.com -j tls.json
# Mozilla 配置规范比对
```

## 注意事项

Python TLS 扫描库,深度协议检测+合规检查。
