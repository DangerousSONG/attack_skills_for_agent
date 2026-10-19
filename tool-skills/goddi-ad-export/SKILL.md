---
name: goddi-ad-export
description: 渗透工具 skill:goddi 的安装、参数速查与攻击场景 playbook。当任务涉及 AD与横向移动 需要调用 goddi 时使用。
---

# goddi

- 攻击大类:C30 AD与横向移动
- 上游仓库:https://github.com/NetSPI/goddi
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/NetSPI/goddi@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `goddi -username svc@corp.local -password pass -domain corp.local -dc 10.0.0.1 -unsafe` | 导出 AD 全量(用户/组/计算机/GPO) |
| `-format csv|json` | 输出格式 |

## 攻击场景 Playbook

### AD 结构全量导出(离线分析)

```bash
goddi -u svc@corp.local -p pass -domain corp.local -dc 10.0.0.1 -unsafe
# 拿 CSV 后离线画权限关系,挑提权路径
```

## 注意事项

NetSPI 出品,AD 信息(用户/组/计算机/信任/GPO/OU)一键全导出为 CSV,适合离线建攻击路径图。
