---
name: phoneinfoga-osint
description: 渗透工具 skill:PhoneInfoga 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 PhoneInfoga 时使用。
---

# PhoneInfoga

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/sundowndev/PhoneInfoga
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
docker run --rm -it sundowndev/phoneinfoga scan -n +8613800000000 或 release 二进制
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `scan -n +86...` | 号码 OSINT 扫描 |
| `-n 号码 -s twint` | 指定扫描器 |
| `serve -p 8080` | 起 Web UI |
| `-o json` | 输出 |

## 攻击场景 Playbook

### 手机号归属/公开足迹

```bash
./phoneinfoga scan -n '+86 138 0000 0000' -o json | jq
# 输出 carrier/地域/是否注册 Google/Twitter 等
```

## 注意事项

不发短信不打电话,纯公开源聚合;国内号码覆盖有限。
