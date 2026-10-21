---
name: shodanhat-shodan-query
description: 渗透工具 skill:ShodanHat 的安装、参数速查与攻击场景 playbook。当任务涉及 网络拓扑测绘 需要调用 ShodanHat 时使用。
when-to-use: 渗透工具 skill:ShodanHat 的安装、参数速查与攻击场景 playbook。当任务涉及 网络拓扑测绘 需要调用 ShodanHat 时使用。
---

# ShodanHat

- 攻击大类:C04 网络拓扑测绘
- 上游仓库:https://github.com/HatBashBR/ShodanHat
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/HatBashBR/ShodanHat && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python ShodanHat.py -k $KEY -q 'org:Target'` | Shodan 搜索+结果落库 |
| `-q 'ssl:corp.com'` | 证书匹配 |
| `-q 'product:Apache' --country BR` | 组合过滤 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### Shodan 批量资产收割

```bash
python ShodanHat.py -k KEY -q 'hostname:corp.com 200 OK'
# 绕过 CDN 直打源站/管理后台
```

## 注意事项

Shodan 查询封装+结果导出,附批量 IP 处理,配合 API key 做企业资产普查。
