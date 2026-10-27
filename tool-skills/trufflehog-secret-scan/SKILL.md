---
name: trufflehog-secret-scan
description: trufflehog: Github 密钥泄露收割、员工 fork 仓库找内部凭证。信号:攻击面,云资产,扫单个仓库,扫整个 org。
---

# trufflehog

- 攻击大类:C05 外部攻击面与云资产暴露
- 上游仓库:https://github.com/trufflesecurity/trufflehog
- 上游 License:AGPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/trufflesecurity/trufflehog@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `trufflehog github --repo=https://github.com/org/repo` | 扫单个仓库 |
| `trufflehog github --org=orgname` | 扫整个 org |
| `trufflehog gitlab --endpoint=...` | GitLab |
| `--only-verified` | 只报已验证可活的密钥 |
| `-j` | JSON 输出 |
| `trufflehog filesystem ./leak-repo` | 扫本地目录 |

## 攻击场景 Playbook

### Github 密钥泄露收割

```bash
trufflehog github --org=target-org --only-verified -j | tee keys.json
# AWS key/Slack token/私钥等自动验证有效性
```

### 员工 fork 仓库找内部凭证

```bash
trufflehog github --repo=https://github.com/employee/fork --only-verified
```

## 注意事项

支持 800+ 密钥类型并自动验证;--only-verified 大幅降低误报。
