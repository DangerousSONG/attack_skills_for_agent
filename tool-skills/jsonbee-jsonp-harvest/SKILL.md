---
name: jsonbee-jsonp-harvest
description: 渗透工具 skill:JSONBee 的安装、参数速查与攻击场景 playbook。当任务涉及 载荷与文件投递 需要调用 JSONBee 时使用。
---

# JSONBee

- 攻击大类:C07 载荷与文件投递
- 上游仓库:https://github.com/zigoo0/JSONBee
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/zigoo0/JSONBee
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `grep -h 'google' *.txt` | 挑可用 JSONP 端点 |
| `组合 payload: <script src='https://victim.com/jsonp?callback=steal'></script>` | XSS/数据窃取 |
| `cc理想.jsonp 文件批量看` | 预整理端点 |

## 攻击场景 Playbook

### JSONP 回调劫持

```bash
cat cc理想.jsonp | head
# 找含敏感数据的 JSONP 端点,伪造回调函数窃取
```

## 注意事项

JSONP 端点收集(google/github/默认回调等),XSS 和跨域数据窃取素材库。
