---
name: kiterunner-api-routes
description: 渗透工具 skill:kiterunner 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 kiterunner 时使用。
---

# kiterunner

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/assetnote/kiterunner
- 上游 License:AGPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/assetnote/kiterunner/cmd/kr@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `kr scan https://api.target.com -w routes.kite` | API 路由扫描 |
| `-A=apiroutes-210228` | 内置字典 |
| `-x 100` | 最大连接 |
| `-d 3` | 爬深 |
| `kr scan targets.txt --depth 3 -A` | 批量 |

## 攻击场景 Playbook

### API 隐藏路由爆破

```bash
kr scan https://api.target.com -w ~/kiterunner/routes.kite -x 100
# Assetnote 出品,路由上下文感知,专出 /internal/v2/admin 这类端点
```

## 注意事项

API 路由发现比目录爆破器准一个量级;字典基于真实 API 流量构建。
