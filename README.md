# Attack Skills for Agent · 攻击侧 Skills 集（996 个 · 1k 达成）

> 面向渗透测试 Agent 的即插即用 SKILL.md 能力库：每个 skill = frontmatter + 方法论 + 命令速查 + 攻击场景 Playbook，Agent 按需加载、照抄执行。
> 逐条明细（名称/来源/License/简介/链接）见 [INDEX.md](INDEX.md)。维护流程（新增/修改 skill 的三步级联 + 门禁）见 [CONTRIBUTING](CONTRIBUTING.md)。
> ⚠️ 仅限授权安全测试使用（authorized security testing only）。

## 核心价值

- **两层部署，根治 token 爆炸**：996 个 skill 全量注册时每个 step 携带约 20K tokens 索引，实测 prompt cache 命中率 84.9% → 14.8%，成本放大 3.9 倍。改为「3 注册 + 993 文件库」后常驻索引 <2K tokens/step（详见下文部署模型）。
- **检索质量可量化**：107 条中文渗透任务查询 × 人工金标 slug 的 Recall 评测，当前 **Recall@5 = 82.2% / Recall@20 = 100.0%**（description 全英文 + `zh-signals` 中文检索信号口径），description 历经 3 轮数据驱动迭代（详见下文质量评测）。
- **口径干净**：攻击侧 only（剔除无线/硬件、纯防御、纯逆向）；跨 10 个源零重名；License 全部可二创（Apache-2.0 / MIT / CC BY 4.0），工具改写类逐条标注上游 License。
- **56% 自研资产**：561 个工具改写 skill（一个真实工具一个 playbook）+ 路由表 + gadget 决策表，独立知识产权，二创版权最干净。

## 仓库结构

| 目录 | 内容 | 数量 |
| --- | --- | ---: |
| `tool-skills/` | 工具改写 skill：一个真实渗透工具（ffuf/mimikatz/nuclei…）一个标准 SKILL.md | 559 |
| `Anthropic-Cybersecurity-Skills/` | 上游 mukul975/ACS（Apache-2.0）：AD/云/钓鱼/C2/API 方法论 | 188 |
| `hack-skills/` | 上游 yaklang/hack-skills（MIT）：Web 漏洞专项（SQLi/XSS/SSRF/SSTI…） | 95 |
| `Claude-Red-pentest-set/` | 上游 tmenov（MIT）：红队全流程（初始访问/横向/免杀） | 59 |
| `pentest-ai-agents/` | 上游 0xSteph（MIT）：角色型 skill（recon/planner/opsec…） | 38 |
| `offensive-claude/` | 上游 hypnguyen1209（MIT）：纪律类（scope/engagement/finding） | 29 |
| `Claude-OSINT/` `ctf-skills/` `awesome-web3-security/` `yak-skills/` `awesome-ai-security/` | 上游 OSINT/CTF/Web3/Yakit/LLM 安全 | 26 |
| `attack-skill-router/` | 注册层：压缩路由主表（15KB）+ reference.md 展开层 + MERGES 合并裁决 + 生成脚本 | 1 |
| `engagement-discipline/` | 注册层：纪律元技能（scope 边界/授权约束） | 1 |
| `java-deserialization-gadget-selector/` | 注册层：Java 反序列化 gadget 决策表 | 1 |
| `scripts/` | 治理/部署/评测脚本（见下） | — |
| `INDEX.md` / `攻击侧Skills清单.csv` / `attack-skill-router/MERGES.md` | 全量清单 / 结构化导出 / 重名合并裁决记录 | — |

### scripts/ 速查

| 脚本 | 用途 |
| --- | --- |
| `deploy.py` | 两层部署：`--dry-run` 预演、`--clean` 清空重布、路径可用 `--skills-dir`/`--library-dir` 覆盖 |
| `govern_skills.py` | 质量门禁：frontmatter 校验、断链扫描（含"未随库分发"豁免）、路径存在性检查 |
| `eval_recall.py` | 检索质量评测：BEFORE=git HEAD / AFTER=工作区，输出 Recall@5/@20 对比 |
| `attack-skill-router/gen_router.py` / `regenerate_index.py` / `export_csv.py` | 路由表两层生成（主表+reference）/ INDEX.md 再生成 / CSV 清单导出 |

## 部署（两层模型 · v2.0）

| 层 | 位置 | 内容 | 加载方式 |
| --- | --- | --- | --- |
| 注册层（Skill 协议） | `/root/.claude/skills/` | 3 个：`attack-skill-router`、`engagement-discipline`、`java-deserialization-gadget-selector` | Agent 原生 skill 索引 |
| 文件库（Read 协议） | `/opt/attack-skill-library/` | 993 个 skill 扁平存放 + `INDEX.md` + `MERGES.md` | 按路由表 Read 按需加载 |

**Agent 入口**：3 个注册 skill 常驻索引（<2K tokens/step）→ 路由表命中场景 → Read 打开 `/opt/attack-skill-library/<slug>/SKILL.md`。

```bash
python scripts/deploy.py [--dry-run] [--clean] [--skills-dir 注册层目录] [--library-dir 文件库目录]
```

- 默认注册层 `/root/.claude/skills/`、文件库 `/opt/attack-skill-library/`（环境变量 `SKILL_LIBRARY` 可覆盖）
- 换文件库路径需同步改 `attack-skill-router/SKILL.md` 中的基准路径

## 质量评测（Recall）

评测回答一个问题：**一条渗透任务描述丢进来，该用的 skill 能不能被检索到前 N 名**。

- 评测集：107 条中文渗透任务查询，每条人工标注金标 slug（如「SQL 注入验证并拖库」→ `exploiting-sql-injection-with-sqlmap` 等 3 个标准答案），50 个攻击大类全覆盖
- 方法：TF-IDF（词 1-2 gram + 字 3-5 gram）对 `name×3 + description + zh-signals` 排序；Recall@N = 金标至少 1 个进前 N 的查询占比
- 当前：**Recall@5 82.2% / Recall@20 100.0%**（v2.2 英文化后口径）；边界：只测"找不找得到"，不测"用得好不好"

```bash
python scripts/eval_recall.py   # 约 1-2 分钟，输出 BEFORE(HEAD) vs AFTER(工作区)
```

## 口径

- 攻击侧 only：剔除无线/硬件（WiFi/蓝牙/SDR/固件/IoT）、纯防御（检测/狩猎/响应/加固/ZTNA/PAM/IDS）、纯逆向与恶意软件分析
- 跨仓库按 skill 名称去重，与 mukul975/ACS 及其余各源零重名
- License 全部开源可二创；CC BY 内容需署名（见末节）
- 工具改写 skill 标注上游仓库与上游 License，二创以 Apache-2.0 发布

## 来源分布（996 = 现成 435 + 工具改写 561）

| 来源 | License | 数量 |
| --- | --- | ---: |
| mukul975/Anthropic-Cybersecurity-Skills | Apache-2.0 | 188 |
| yaklang/hack-skills | MIT | 95 |
| tmenov/Claude-Red-pentest-set | MIT | 59 |
| 0xSteph/pentest-ai-agents | MIT | 38 |
| hypnguyen1209/offensive-claude | MIT | 29 |
| elementalsouls/Claude-OSINT | MIT(代码)/CC BY 4.0(内容) | 7 |
| ljagiello/ctf-skills | MIT | 6 |
| gmh5225/awesome-web3-security | MIT | 5 |
| yaklang/yak-skills | MIT | 5 |
| gmh5225/awesome-ai-security | MIT | 3 |
| 本仓库 tool-skills/ 改写 + 原创（router/discipline/gadget） | Apache-2.0（上游 License 逐条见各 SKILL.md） | 561 |
| **合计** | | **996** |

## 攻击大类分布（50 类全覆盖 · ATT&CK 骨架）

Top 12：C09 Web应用漏洞利用 171 · C01 资产测绘与指纹识别 62 · C10 API与业务逻辑攻击 54 · C30 AD域渗透与域控攻击 50 · C46 二进制漏洞利用与Pwn 46 · C42 网络扫描与枚举 40 · C50 红队方法论与自动化 38 · C40 嗅探与中间人攻击 36 · C25 哈希与密码破解 34 · C05 外部攻击面与云资产暴露 31 · C03 邮箱与人员OSINT 27 · C08 钓鱼与社会工程 25。

<details>
<summary>矩阵分布（大类 × 来源，50 类全量）</summary>

| 攻击大类 | 现成 | 改写 | 合计 |
| --- | ---: | ---: | ---: |
| C09 Web应用漏洞利用 | 72 | 99 | 171 |
| C01 资产测绘与指纹识别 | 14 | 48 | 62 |
| C10 API与业务逻辑攻击 | 40 | 14 | 54 |
| C30 AD域渗透与域控攻击 | 26 | 24 | 50 |
| C46 二进制漏洞利用与Pwn | 29 | 17 | 46 |
| C42 网络扫描与枚举 | 7 | 33 | 40 |
| C50 红队方法论与自动化 | 31 | 7 | 38 |
| C40 嗅探与中间人攻击 | 8 | 28 | 36 |
| C25 哈希与密码破解 | 5 | 29 | 34 |
| C05 外部攻击面与云资产暴露 | 17 | 14 | 31 |
| C03 邮箱与人员OSINT | 1 | 26 | 27 |
| C08 钓鱼与社会工程 | 15 | 10 | 25 |
| C07 载荷开发与武器化 | 12 | 12 | 24 |
| C49 密码学攻击 | 5 | 17 | 22 |
| C41 Web漏洞扫描与验证 | 7 | 14 | 21 |
| C35 C2框架与远控 | 13 | 8 | 21 |
| C43 移动端攻击 | 14 | 7 | 21 |
| C02 域名与DNS侦察 | 4 | 15 | 19 |
| C22 进程注入与内存执行 | 18 | 1 | 19 |
| C29 内网发现与枚举 | 0 | 17 | 17 |
| C12 供应链与CI/CD攻击 | 14 | 2 | 16 |
| C28 暴力破解与口令喷射 | 0 | 15 | 15 |
| C18 云与容器提权 | 11 | 3 | 14 |
| C06 漏洞情报与漏洞库 | 8 | 6 | 14 |
| C15 持久化与后门植入 | 9 | 4 | 13 |
| C31 远程服务横向移动 | 4 | 9 | 13 |
| C32 隧道与内网穿透 | 2 | 10 | 12 |
| C44 AI与大模型安全 | 9 | 3 | 12 |
| C17 Windows本地提权 | 5 | 6 | 11 |
| C04 网络拓扑与互联网测绘 | 3 | 7 | 10 |
| C45 恶意软件开发与免杀 | 0 | 9 | 9 |
| C16 Linux本地提权 | 4 | 4 | 8 |
| C13 远程命令执行与WebShell | 0 | 8 | 8 |
| C26 Kerberos与票据攻击 | 5 | 3 | 8 |
| C24 内存转储与LSASS窃取 | 2 | 3 | 5 |
| C48 区块链与Web3安全 | 4 | 1 | 5 |
| C11 边界设备与VPN攻击 | 2 | 2 | 4 |
| C19 EDR与AV规避 | 4 | 0 | 4 |
| C20 反取证与痕迹清理 | 0 | 4 | 4 |
| C27 本地凭证与浏览器窃取 | 4 | 0 | 4 |
| C33 数据收集与打包暂存 | 1 | 3 | 4 |
| C38 隐写与隐藏通道 | 0 | 4 | 4 |
| C47 逆向工程 | 1 | 3 | 4 |
| C34 屏幕与输入捕获 | 1 | 2 | 3 |
| C39 数据破坏与擦除 | 2 | 1 | 3 |
| C14 云与容器执行 | 0 | 3 | 3 |
| C36 隐蔽回连与通信通道 | 0 | 3 | 3 |
| C37 数据外传 | 1 | 1 | 2 |
| C23 无文件与LOLBins滥用 | 0 | 2 | 2 |
| C21 流量混淆与加密隧道 | 1 | 0 | 1 |
| **合计** | **435** | **561** | **996** |

</details>

## 版本记录

- v1.1：ACS 误伤复议回收 8 个 + 新增 blockint/ctf/awesome-ai-security 三源
- v1.9：口径定稿（blockint 移出；MERGES 20 团裁决 13 并 7 不并）→ 989
- v2.0：补 nuclei/gobuster/ffuf/hydra/frp/chisel/john 七工具 → 996；两层部署（router 15KB 主表 + reference 展开层 + deploy.py）；description 三轮迭代 + Recall 评测 @20 100%；评测集扩至 107 条（零覆盖大类补齐）@5 84.1% / @20 100%
- v2.1：治理修复 —— 路由表数据源由外部旧 CSV 改为「INDEX.md + 仓库直扫」重生成（7 新工具全收录、数字口径 996 全同步）；CSV 清单重导出（599 → 996）；4 处 frontmatter name 与目录名对齐；死金标清理；gen_router 修复多强制项互相挤占 bug
- v2.2：997 个 SKILL.md description 全英文统一（when-to-use / 检索一致性），中文检索信号改存 `zh-signals` 字段（仅检索用、不进展示）；评测口径同步为 `name×3 + description + zh-signals`，Recall @5 82.2% / @20 100%（英文版 R@20 守住 100%）

## 署名与许可

- 各目录内 LICENSE 文件为对应上游仓库原始许可，二次分发请遵守
- elementalsouls/Claude-OSINT 的 SKILL.md 内容以 CC BY 4.0 授权，二次使用须署名 **Sachin Sharma / Claude-OSINT** 并链接原仓库
- 其余上游均以 Apache-2.0 / MIT 授权，可自由二创；本仓库改写内容以 Apache-2.0 发布






## TODO
### 1. main分支更新路由表








