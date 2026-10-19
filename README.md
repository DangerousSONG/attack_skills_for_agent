# Attack Skills for Agent · 攻击侧 Skills 集（403 个）

> 面向渗透测试 Agent 的即插即用 SKILL.md 能力库。每个 skill 是一个标准化 SKILL.md 文件（frontmatter + 方法论 + 命令 + 攻击链），Agent 按需加载。
>
> ⚠️ 仅限授权安全测试使用（authorized security testing only）。

## 口径

- 攻击侧 only：已剔除无线/硬件（WiFi/蓝牙/SDR/固件/IoT）、纯防御（检测/狩猎/取证响应/加固合规）、纯逆向与恶意软件分析
- 跨仓库按 Skill 名称去重，与 mukul975/Anthropic-Cybersecurity-Skills 零重名
- License 全部开源可二创：Apache-2.0 / MIT / CC BY 4.0（CC BY 内容需署名，见下）

## 目录结构

```
pentest-ai-agents/          # 38 个 skill（含 LICENSE）
Claude-OSINT/          # 7 个 skill（含 LICENSE）
awesome-web3-security/          # 5 个 skill（含 LICENSE）
offensive-claude/          # 29 个 skill（含 LICENSE）
Anthropic-Cybersecurity-Skills/          # 160 个 skill（含 LICENSE）
Claude-Red-pentest-set/          # 63 个 skill（含 LICENSE）
hack-skills/          # 96 个 skill（含 LICENSE）
yak-skills/          # 5 个 skill（含 LICENSE）
攻击侧Skills清单.csv   # 总索引表（名称/来源/License/分类/ATT&CK/简介/链接）
```

## 来源分布

| 来源仓库 | License | 数量 |
| --- | --- | --- |
| mukul975/Anthropic-Cybersecurity-Skills | Apache-2.0 | 160 |
| yaklang/hack-skills | MIT | 96 |
| tmenov/Claude-Red-pentest-set | MIT | 63 |
| 0xSteph/pentest-ai-agents | MIT | 38 |
| hypnguyen1209/offensive-claude | MIT | 29 |
| elementalsouls/Claude-OSINT | MIT(代码)/CC BY 4.0(内容) | 7 |
| gmh5225/awesome-web3-security | MIT | 5 |
| yaklang/yak-skills | MIT | 5 |

## 攻击大类分布

Web应用攻击 92 · AD与横向移动 65 · 漏洞利用框架 44 · 红队自动化与 BAS 44 · 后渗透与C2 39 · 凭据攻击与破解 32 · AI/大模型安全 16 · 扫描与枚举 15 · 侦察与资产测绘 13 · 云与容器攻防 12 · 移动端攻击 12 · 嗅探与中间人 6 · 钓鱼与社会工程 6 · 供应链与开发安全 4 · 漏洞扫描与验证 3

## 署名与许可

- 各目录内 LICENSE 文件为对应上游仓库原始许可，二次分发请遵守
- elementalsouls/Claude-OSINT 的 SKILL.md 内容以 CC BY 4.0 授权，二次使用须署名 **Sachin Sharma / Claude-OSINT** 并链接原仓库
- 其余仓库均以 Apache-2.0 / MIT 授权，可自由二创

## ⚠️ 本地杀毒软件拦截说明

`Claude-Red-pentest-set/offensive-file-upload`（文件上传攻击技能）的 SKILL.md 被本机 Windows Defender 实时查杀，无法在工作区落盘。上游原始文件：
https://github.com/tmenov/Claude-Red-pentest-set/blob/main/Skills/web/offensive-file-upload/SKILL.md

如需本地完整 403 个：为本目录添加 Defender 排除项后重新拉取即可。

实际拦截 7 个（Windows Defender 实时查杀，无法落盘）：

| 缺失 Skill | 上游文件 |
| --- | --- |
| Claude-Red-pentest-set/offensive-file-upload | https://github.com/tmenov/Claude-Red-pentest-set/blob/main/Skills/web/offensive-file-upload/SKILL.md |
| Claude-Red-pentest-set/offensive-rce | https://github.com/tmenov/Claude-Red-pentest-set/blob/main/Skills/web/offensive-rce/SKILL.md |
| hack-skills/nosql-injection | https://github.com/yaklang/hack-skills/blob/main/skills/nosql-injection/SKILL.md |
| hack-skills/reverse-shell-techniques | https://github.com/yaklang/hack-skills/blob/main/skills/reverse-shell-techniques/SKILL.md |
| hack-skills/unauthorized-access-common-services | https://github.com/yaklang/hack-skills/blob/main/skills/unauthorized-access-common-services/SKILL.md |
| hack-skills/upload-insecure-files | https://github.com/yaklang/hack-skills/blob/main/skills/upload-insecure-files/SKILL.md |

本地实际落盘 396 个 SKILL.md + README + 索引 CSV + 8 份 LICENSE。
| Claude-Red-pentest-set/offensive-sqli | https://github.com/tmenov/Claude-Red-pentest-set/blob/main/Skills/web/offensive-sqli/SKILL.md |
