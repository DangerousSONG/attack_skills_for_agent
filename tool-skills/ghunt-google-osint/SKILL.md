---
name: ghunt-google-osint
description: GHunt: 邮箱反查 Google 足迹。信号:邮箱收集,员工信息,GAIA ID 反查,地图评价账号关联。
---

# GHunt

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/mxrch/GHunt
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/mxrch/GHunt && cd GHunt && pip install -r requirements.txt && python ghunt.py login
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `ghunt email victim@gmail.com` | 邮箱→Google 账号画像 |
| `ghunt gaia <id>` | GAIA ID 反查 |
| `ghunt review <place_id>` | 地图评价账号关联 |

## 攻击场景 Playbook

### 邮箱反查 Google 足迹

```bash
python ghunt.py email target@gmail.com
# 返回 G+ 头像/地图评论/Youtube 频道等公开痕迹
```

## 注意事项

需先 login 注入 cookies(GHunt 自身浏览器扩展导出);仅查询公开数据。
