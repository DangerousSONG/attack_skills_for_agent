---
name: gitem-github-org
description: 渗透工具 skill:Gitem 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 Gitem 时使用。
when-to-use: 渗透工具 skill:Gitem 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 Gitem 时使用。
---

# Gitem

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/mswell/gitem
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install gitem
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `gitem -u target` | 拉组织全部 repos |
| `-a` | 含 releases/packages |
| `-m` | 只 metadata |

## 攻击场景 Playbook

### 组织仓库批量克隆审计

```bash
gitem -u targetorg  # 全 repos 克隆到本地,trufflehog/gitleaks 批量扫密钥
```

## 注意事项

配合密钥扫描器做组织级代码审计前置。
