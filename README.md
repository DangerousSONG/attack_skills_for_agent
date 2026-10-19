# Attack Skills for Agent · 攻击侧 Skills 集（1000 个）

> 面向渗透测试 Agent 的即插即用 SKILL.md 能力库。每个 skill 是一个标准化 SKILL.md 文件（frontmatter + 方法论 + 命令 + 攻击链），Agent 按需加载。
>
> ⚠️ 仅限授权安全测试使用（authorized security testing only）。



## v1.8 更新(2026-10-19):③ 工具改写流水线 第五批(冲刺) 72 个 —— **1000 指标达成**

- `tool-skills/` 新增 **72 个**(累计 558):OSINT 侦察 21(waymore/favfreak/maryam/datasploit/CrossLinked/SlackPirate/gitGraber...)、DNS/网络枚举 10(aiodnsbrute/dnsprobe/hakrevdns/scannerl...)、中间人 10(PCredz/interactsh/BinProxy/DNSWatch...)、密码字典与破解 11(pydictor/duplicut/cracken/wordlistctl...)、AD 5(PKINITtools/targetedKerberoast/DeathStar...)、C2 4(emp3r0r/koadic/portia...)、AI 渗透 Agent 3(HexStrike-AI/PentestGPT/PentestAgent,补齐 C44 窄类)、钓鱼 3(CredSniper/SocialFish/SimpleEmailSpoofer)
- **当前合计:1000 个攻击侧 skill(现成 442 + 工具改写 558)—— 1k 目标 100% 达成**
- 50 个攻击大类全覆盖,License 全部开源可二创(SKILL.md 以 Apache-2.0 二次开源+上游版权头,WPScan 上游 CC BY-NC 除外)

## v1.7 更新(2026-10-19):③ 工具改写流水线 第四批 180 个

- `tool-skills/` 新增 **180 个**(累计 486):Web 应用攻击 65(bbscan/jaeles/v3n0m/w13scan/sourcemapper/xxexploiter/myjwt...)、网络枚举 14(v3n0m/nray/pbscan/changeme/atscan...)、嗅探与中间人 14(seth/xerosploit/sslstrip/net-creds/snarf...)、密码学与 TLS 11(hash_extender/tlsfuzzer/padre/a2sv...)、Pwn 与利用框架 8(zeratool/angrop/isf/richsploit...)、口令喷射 6(spray365/spraycharles/barq/msmailprobe...)、隧道代理 6(stowaway/mubeng/proxify/torpy...)、横向移动 5(barmie/sjet/sireprat/tomcatWarDeployer...)等
- 当前合计:**928 个攻击侧 skill**(现成 442 + 工具改写 486)
- 进度:928/1000 = 92.8%,最后 ~72 个需从 BlackArch 语料+窄类(C44 AI 安全/C48 Web3)定向补充

## v1.6 更新(2026-10-19):③ 工具改写流水线 第三批 149 个

- `tool-skills/` 新增 **149 个**(累计 306):侦察/资产测绘 30(waybackurls/shuffledns/finalrecon/fierce/zgrab2/zdns...)、Web 利用 19(ghauri/kadimus/lfimap/nosqli/crlfuzz/wcvs/h2csmuggler...)、AD 与横向 18(sccmhunter/donpapi/jackdaw/adpeas/HEKATOMB...)、口令破解 10(crowbar/brutespray/credmaster/bkcrack...)、LDAP 枚举 7、移动端 5、免杀 5、模糊测试 5、密码误用 4、载荷投递 4、身份喷洒 4、Web 扫描 3、服务枚举 3、反取证 3、横向执行 3、隧道 1、CVE 专项 1 等
- 当前合计:**748 个攻击侧 skill**(现成 442 + 工具改写 306)
- 进度:748/1000 = 74.8%,第四批从 BlackArch/awesome 系语料补充剩余 ~250 个

## v1.5 更新(2026-10-19):③ 工具改写流水线 第二批 104 个

- `tool-skills/` 新增 **104 个**(累计 157):Web 利用 17(bloodyAD/jwt_tool/ssrfmap/tplmap/commix...)、侦察 26(amass/sublist3r/aquatone/maigret/holehe...)、AD/Kerberos 8、云 6、免杀/反取证/C2/隐写等空类全部补齐
- **50 个攻击大类首次全部有 skill 覆盖**(C23 LOLBins / C36 隐蔽回连 / C39 影响 / C45 免杀等由本批落地)
- 当前合计:**599 个攻击侧 skill**(现成 442 + 工具改写 157)
- 进度:599/1000 = 59.9%,第三批从 P2 池剩余 400+ 候选继续

## v1.4 更新(2026-10-19):③ 工具改写流水线 第一批 53 个

- 新增 `tool-skills/` 目录:**53 个由开源渗透工具改写的 SKILL.md**(来源:工具注册表 P1/P2 池,人工质量过滤+家族合并)
- 分类体系升级为 **50 个攻击大类**(ATT&CK 14 战术为骨架 + 技术细分 + 垂直域),全部 495 个 skill 完成重打标
- 去重规则:与现有 442 个现成 skill 功能重复者剔除(如 netexec/john/metasploit/hydra/dnscat2 已有覆盖),`impacket × 56` / `Responder × 6` 家族合并为单 skill
- 权利链条:每个 SKILL.md 以 Apache-2.0 二次开源,头部标注上游仓库与 License,上游版权归原项目所有
- 覆盖补齐:原 9 个空类目(C13/C14/C20/C23/C28/C29/C33/C38/C45 中除 C23/C36/C45 外)本批全部落地,剩余 3 类在第二批补齐
- 当前合计:**495 个攻击侧 skill**(现成 442 + 工具改写 53)

## 口径

- 攻击侧 only：已剔除无线/硬件（WiFi/蓝牙/SDR/固件/IoT）、纯防御（检测/狩猎/取证响应/加固合规/ZTNA/PAM/IDS）、纯逆向与恶意软件分析
- 跨仓库按 Skill 名称去重，与 mukul975/Anthropic-Cybersecurity-Skills 内部及其余各源零重名
- License 全部开源可二创：Apache-2.0 / MIT / CC BY 4.0（CC BY 内容需署名，见下）
- v1.1 更新：ACS 误伤复议回收 8 个 + 新增 blockint-skills / ctf-skills / awesome-ai-security 三源 20 个（低质量与合规/筛查类目录已剔除）

## 来源分布（11 个仓库）

| 来源仓库 | License | 数量 |
| --- | --- | --- |
| mukul975/Anthropic-Cybersecurity-Skills | Apache-2.0 | 168 |
| yaklang/hack-skills | MIT | 96 |
| tmenov/Claude-Red-pentest-set | MIT | 63 |
| 0xSteph/pentest-ai-agents | MIT | 38 |
| hypnguyen1209/offensive-claude | MIT | 29 |
| agentic-reserve/blockint-skills | MIT | 11 |
| elementalsouls/Claude-OSINT | MIT(代码)/CC BY 4.0(内容) | 7 |
| ljagiello/ctf-skills | MIT | 6 |
| gmh5225/awesome-web3-security | MIT | 5 |
| yaklang/yak-skills | MIT | 5 |
| gmh5225/awesome-ai-security | MIT | 3 |

## 攻击大类分布

Web应用攻击 93 · AD与横向移动 66 · 红队自动化与 BAS 52 · 漏洞利用框架 46 · 后渗透与C2 41 · 凭据攻击与破解 33 · AI/大模型安全 22 · 扫描与枚举 16 · 侦察与资产测绘 16 · 云与容器攻防 13 · 移动端攻击 12 · 嗅探与中间人 6 · 钓鱼与社会工程 6 · 漏洞扫描与验证 5 · 供应链与开发安全 4

## 署名与许可

- 各目录内 LICENSE 文件为对应上游仓库原始许可，二次分发请遵守
- elementalsouls/Claude-OSINT 的 SKILL.md 内容以 CC BY 4.0 授权，二次使用须署名 **Sachin Sharma / Claude-OSINT** 并链接原仓库
- 其余仓库均以 Apache-2.0 / MIT 授权，可自由二创

## ⚠️ 本地杀毒软件拦截说明

以下 7 个 SKILL.md 在 Windows Defender 实时查杀环境下无法落盘（内容为文件上传/WebShell/SQLi/反弹Shell等攻击技术，属误杀范畴）。上游原始文件：

| 缺失 Skill | 上游文件 |
| --- | --- |
| Claude-Red-pentest-set/offensive-file-upload | https://github.com/tmenov/Claude-Red-pentest-set/blob/main/Skills/web/offensive-file-upload/SKILL.md |
| Claude-Red-pentest-set/offensive-rce | https://github.com/tmenov/Claude-Red-pentest-set/blob/main/Skills/web/offensive-rce/SKILL.md |
| Claude-Red-pentest-set/offensive-sqli | https://github.com/tmenov/Claude-Red-pentest-set/blob/main/Skills/web/offensive-sqli/SKILL.md |
| hack-skills/nosql-injection | https://github.com/yaklang/hack-skills/blob/main/skills/nosql-injection/SKILL.md |
| hack-skills/reverse-shell-techniques | https://github.com/yaklang/hack-skills/blob/main/skills/reverse-shell-techniques/SKILL.md |
| hack-skills/unauthorized-access-common-services | https://github.com/yaklang/hack-skills/blob/main/skills/unauthorized-access-common-services/SKILL.md |
| hack-skills/upload-insecure-files | https://github.com/yaklang/hack-skills/blob/main/skills/upload-insecure-files/SKILL.md |

本地实际落盘 424 个 SKILL.md + README + 索引 CSV + 11 份 LICENSE。补齐方法：为 D:\研究\网安工具@0攻击skills 添加 Defender 排除项后重新拉取。
