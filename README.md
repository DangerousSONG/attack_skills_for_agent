# Attack Skills for Agent · 攻击侧 Skills 集（1000 个）

> 面向渗透测试 Agent 的即插即用 SKILL.md 能力库。每个 skill 是一个标准化 SKILL.md 文件（frontmatter + 方法论 + 命令 + 攻击链），Agent 按需加载。
>
> **逐条明细见 [INDEX.md](INDEX.md)**：1000 个 skill 按 50 个攻击大类全量列出。
>
> ⚠️ 仅限授权安全测试使用（authorized security testing only）。

## 口径

- 攻击侧 only：已剔除无线/硬件（WiFi/蓝牙/SDR/固件/IoT）、纯防御（检测/狩猎/取证响应/加固合规/ZTNA/PAM/IDS）、纯逆向与恶意软件分析
- 跨仓库按 Skill 名称去重，与 mukul975/Anthropic-Cybersecurity-Skills 内部及其余各源零重名
- License 全部开源可二创：Apache-2.0 / MIT / CC BY 4.0（CC BY 内容需署名，见下）
- v1.1 更新：ACS 误伤复议回收 8 个 + 新增 blockint-skills / ctf-skills / awesome-ai-security 三源 20 个（低质量与合规/筛查类目录已剔除）
- v1.8 口径定稿：blockint-skills（11 个区块链情报）按实际需求移出；ACS 最终回收至 190 个，现成合计 442 = 10 个仓库

## 来源分布（现成 442 = 10 个仓库 + 工具改写 558）

| 来源 | License | 数量 |
| --- | --- | --- |
| mukul975/Anthropic-Cybersecurity-Skills | Apache-2.0 | 190 |
| yaklang/hack-skills | MIT | 96 |
| tmenov/Claude-Red-pentest-set | MIT | 63 |
| 0xSteph/pentest-ai-agents | MIT | 38 |
| hypnguyen1209/offensive-claude | MIT | 29 |
| elementalsouls/Claude-OSINT | MIT(代码)/CC BY 4.0(内容) | 7 |
| ljagiello/ctf-skills | MIT | 6 |
| gmh5225/awesome-web3-security | MIT | 5 |
| yaklang/yak-skills | MIT | 5 |
| gmh5225/awesome-ai-security | MIT | 3 |
| 工具改写（本仓库 tool-skills/） | Apache-2.0 二次开源（保留上游版权） | 558 |
| **合计** | | **1000** |

注：blockint-skills（11 个区块链情报）已于 v1.8 按需求移出；与 Anthropic-Cybersecurity-Skills 零重名（跨仓库按 skill 名称去重）。

## 攻击大类分布（50 类全覆盖 · ATT&CK 骨架）

Top 12：C09 Web应用漏洞利用 176 · C01 资产测绘与指纹识别 62 · C10 API与业务逻辑攻击 54 · C30 AD域渗透与域控攻击 50 · C46 二进制漏洞利用与Pwn 47 · C42 网络扫描与枚举 40 · C50 红队方法论与自动化 38 · C40 嗅探与中间人攻击 37 · C25 哈希与密码破解 33 · C05 外部攻击面与云资产暴露 31 · C03 邮箱与人员OSINT 27 · C08 钓鱼与社会工程 25。

### 矩阵分布（大类 × 来源，50 类全量）

| 攻击大类 | 现成 Skill | 工具改写 Skill | 合计 |
| --- | ---: | ---: | ---: |
| C09 Web应用漏洞利用 | 75 | 101 | 176 |
| C01 资产测绘与指纹识别 | 14 | 48 | 62 |
| C10 API与业务逻辑攻击 | 40 | 14 | 54 |
| C30 AD域渗透与域控攻击 | 26 | 24 | 50 |
| C46 二进制漏洞利用与Pwn | 30 | 17 | 47 |
| C42 网络扫描与枚举 | 7 | 33 | 40 |
| C50 红队方法论与自动化 | 32 | 6 | 38 |
| C40 嗅探与中间人攻击 | 9 | 28 | 37 |
| C25 哈希与密码破解 | 5 | 28 | 33 |
| C05 外部攻击面与云资产暴露 | 17 | 14 | 31 |
| C03 邮箱与人员OSINT | 1 | 26 | 27 |
| C08 钓鱼与社会工程 | 15 | 10 | 25 |
| C07 载荷开发与武器化 | 12 | 12 | 24 |
| C35 C2框架与远控 | 14 | 8 | 22 |
| C49 密码学攻击 | 5 | 17 | 22 |
| C43 移动端攻击 | 14 | 7 | 21 |
| C02 域名与DNS侦察 | 4 | 16 | 20 |
| C22 进程注入与内存执行 | 18 | 1 | 19 |
| C41 Web漏洞扫描与验证 | 7 | 11 | 18 |
| C29 内网发现与枚举 | 0 | 18 | 18 |
| C12 供应链与CI/CD攻击 | 14 | 2 | 16 |
| C18 云与容器提权 | 11 | 3 | 14 |
| C06 漏洞情报与漏洞库 | 8 | 6 | 14 |
| C28 暴力破解与口令喷射 | 0 | 14 | 14 |
| C15 持久化与后门植入 | 9 | 4 | 13 |
| C31 远程服务横向移动 | 4 | 9 | 13 |
| C44 AI与大模型安全 | 9 | 3 | 12 |
| C17 Windows本地提权 | 5 | 6 | 11 |
| C04 网络拓扑与互联网测绘 | 3 | 7 | 10 |
| C32 隧道与内网穿透 | 2 | 8 | 10 |
| C16 Linux本地提权 | 4 | 5 | 9 |
| C45 恶意软件开发与免杀 | 0 | 9 | 9 |
| C26 Kerberos与票据攻击 | 5 | 3 | 8 |
| C13 远程命令执行与WebShell | 0 | 8 | 8 |
| C24 内存转储与LSASS窃取 | 2 | 3 | 5 |
| C48 区块链与Web3安全 | 4 | 1 | 5 |
| C27 本地凭证与浏览器窃取 | 4 | 0 | 4 |
| C33 数据收集与打包暂存 | 1 | 3 | 4 |
| C19 EDR与AV规避 | 4 | 0 | 4 |
| C11 边界设备与VPN攻击 | 2 | 2 | 4 |
| C47 逆向工程 | 1 | 3 | 4 |
| C20 反取证与痕迹清理 | 0 | 4 | 4 |
| C38 隐写与隐藏通道 | 0 | 4 | 4 |
| C39 数据破坏与擦除 | 2 | 1 | 3 |
| C34 屏幕与输入捕获 | 1 | 2 | 3 |
| C14 云与容器执行 | 0 | 3 | 3 |
| C36 隐蔽回连与通信通道 | 0 | 3 | 3 |
| C37 数据外传 | 1 | 1 | 2 |
| C23 无文件与LOLBins滥用 | 0 | 2 | 2 |
| C21 流量混淆与加密隧道 | 1 | 0 | 1 |
| **合计** | **442** | **558** | **1000** |

逐条明细（1000 个 · 名称/来源/License/简介/可跳转链接）见 [INDEX.md](INDEX.md)

## 署名与许可

- 各目录内 LICENSE 文件为对应上游仓库原始许可，二次分发请遵守
- elementalsouls/Claude-OSINT 的 SKILL.md 内容以 CC BY 4.0 授权，二次使用须署名 **Sachin Sharma / Claude-OSINT** 并链接原仓库
- 其余仓库均以 Apache-2.0 / MIT 授权，可自由二创
