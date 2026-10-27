---
name: cloudlist-multi-cloud
description: cloudlist: 多云攻击面枚举。信号:云提权,iam提权,枚举 AWS 资产,JSON。
---

# cloudlist

- 攻击大类:C18 云与容器提权
- 上游仓库:https://github.com/projectdiscovery/cloudlist
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/projectdiscovery/cloudlist/cmd/cloudlist@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `cloudlist -provider aws -id test` | 枚举 AWS 资产 |
| `-p gcp,azure,digitalocean` | 多云 |
| `-o out.txt` | 输出 |
| `-j` | JSON |
| `-ep aws_ec2,aws_s3` | 只选服务类型 |

## 攻击场景 Playbook

### 多云攻击面枚举

```bash
cloudlist -p aws,gcp,azure -o assets.txt
# 输出所有实例/IP/桶/DB 端点,直接并入扫描清单
```

## 注意事项

pd 生态多云枚举;凭据配 ~/.config/cloudlist/provider-config.yaml。
