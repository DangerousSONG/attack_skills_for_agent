---
name: dontgo403-bypass
description: "dontgo403: 403 endpoint bypass. Signals: web vulnerability, injection, 403 bypass testing, batch paths, request method rotation."
zh-signals: "dontgo403: 403 端点绕过。信号:web漏洞,注入,403 绕过测试,批量路径,请求方式轮换。"
---

# dontgo403

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/ivan-sincek/dontgo403
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/ivan-sincek/dontgo403@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `dontgo403 -u https://t.com/admin` | 403 绕过测试 |
| `-p paths.txt` | 批量路径 |
| `-m 5` | 请求方式轮换 |
| `-H 'Header: value'` | 自定义头 |

## 攻击场景 Playbook

### 403 端点绕过

```bash
dontgo403 -u https://target/admin -p admin_paths.txt
# 自动轮换: 尾斜杠/../绕过/IP 头伪造(X-Forwarded-For 127.0.0.1)/大写方法/编码
```

## 注意事项

内置 40+ 绕过技巧模板;与 4xx 扫描器(bypass-403 类)互补。
