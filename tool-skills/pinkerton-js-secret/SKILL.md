---
name: pinkerton-js-secret
description: 渗透工具 skill:Pinkerton 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 Pinkerton 时使用。
---

# Pinkerton

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/oppsec/Pinkerton
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install pinkerton
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `pinkerton -u https://t.com` | JS 密钥/端点提取 |
| `-u url -d 3` | 深度 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 前端密钥收割

```bash
pinkerton -u https://t.com
# API key/AccessToken/私钥正则匹配 JS
```

## 注意事项

JS 文件敏感信息提取,30+ 种密钥正则。
