---
name: meg-path-check
description: 渗透工具 skill:meg 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 meg 时使用。
when-to-use: 渗透工具 skill:meg 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 meg 时使用。
---

# meg

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/tomnomnom/meg
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/tomnomnom/meg@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `meg paths.txt hosts.txt` | 多 host×多路径请求 |
| `meg -X POST` | POST 模式 |
| `meg -s 200` | 只存 200 响应 |
| `-c 20` | 并发 |

## 攻击场景 Playbook

### 全路径批量请求

```bash
meg /usr/share/seclists/Discovery/Web-Content/common.txt subs.txt out/
# 结果按 host 分目录存,二次处理方便
```

## 注意事项

tomnomnom 出品,host×path 矩阵请求器,输出结构化适合后续 grep 分析。
