---
name: changeme-default-creds
description: 渗透工具 skill:changeme 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 changeme 时使用。
---

# changeme

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/ztgrace/changeme
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/ztgrace/changeme && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `changeme -s 10.0.0.0/24` | 默认凭据扫描 |
| `-s subnet -p 22,80,443` | 端口 |
| `-a tomcat,apache` | 指定应用 |
| `-o out.json` | 输出 |

## 攻击场景 Playbook

### 默认口令全网扫描

```bash
changeme -s 10.0.0.0/24 -p 22,80,443,3306
# 路由器/摄像头/数据库默认凭据
```

## 注意事项

默认凭据扫描器,289+ 应用的默认口令库。
