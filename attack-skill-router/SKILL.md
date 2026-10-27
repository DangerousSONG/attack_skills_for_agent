---
name: attack-skill-router
description: 攻击侧 Skill 库的路由层。当任务涉及渗透测试任一环节（侦察/利用/提权/横向/持久化等）时，先读本 skill 的 50 类路由速查表定位大类和 top3 primary，再用 Read 按需读库文件；不要全库 grep 盲读。
when-to-use: 任何渗透任务开题时；已读 skill 不足以解决当前障碍时回来换路由。
---

# Attack Skill Router · 攻击 Skill 路由层（v0.2 压缩主表）

## 用途

本库 ~1000 个 skill（50 个攻击大类），部署为两层：**注册层**（本 skill 等 3 个，走 Skill 协议）+ **文件库**（其余 ~987 个纯 markdown，走 Read 按需读）。路由层把「1000 选 N」压缩为「50 类选 1 类 → top3 选 1-2 个 → 按需展开」。

## 使用流程（必须按序）

1. **定位大类**：按下表「触发词」命中一行（服务名/漏洞类别/技术关键词/CVE 均可）；
2. **读 primary**：`Read /opt/attack-skill-library/<slug>/SKILL.md`，top3 中选 1-2 个最贴切的（按 description 触发条件判断），不要三个全读；
3. **不够再扩**：该类的完整 5 个 primary、二级子路由和 secondary 检索词在同目录 `reference.md` 的对应小节（`#Cxx`）；全库定向搜索用 `grep -ril <关键词> /opt/attack-skill-library --include=SKILL.md`；
4. **报告**：最终报告末尾列出实际读取的 slug（与评测工作流一致）。

## 选用规则

- **方法论优先于工具**：先选方法论 skill（讲利用链），工具改写 skill（单工具说明书）在缺具体命令时补；
- **同主题只读一个**：同主题已在路由层去重（见库根 `MERGES.md`）；若 grep 仍命中多个相似 slug，选 description 与当前服务/版本最贴合的；
- **版本敏感型任务**（Java 反序列化 gadget、内核 exploit 等）：方法论只给思路，gadget 适配按目标版本自建，不要反复重试库内旧 gadget（专项见注册层 `java-deserialization-gadget-selector`）；
- **单点限时**：一个认证/利用点 20-30 分钟无进展必须回退换路（详见注册层 `engagement-discipline`）。

## 路由速查表（50 类 · 每类 top3 primary · 完整表见 reference.md）

- **C27 本地凭证与浏览器窃取**（4） 触发:本地凭证 / 浏览器窃取 ; credential, access, abusing, dpapi → `abusing-dpapi-for-credential-access`, `extracting-browser-history-artifacts`, `performing-credential-access-with-lazagne`
- **C33 数据收集与打包暂存**（4） 触发:数据收集 / 打包暂存 ; acquiring, disk, image, dcfldd → `acquiring-disk-image-with-dd-and-dcfldd`, `paramspider-param-harvest`, `tlsx-tls-enum`
- **C30 AD域渗透与域控攻击**（50）〔二级子类→ref〕 触发:AD域渗透 / 域控攻击 ; active, directory, bloodhound, exploiting → `abusing-shadow-credentials-for-privesc`, `attacking-entra-id-with-roadtools`, `conducting-internal-reconnaissance-with-bloodhound-ce`
- **C44 AI与大模型安全**（12） 触发:AI / 大模型安全 ; llm, attacks, threat, security → `assessing-vector-and-embedding-weaknesses`, `orchestrating-llm-attacks-with-pyrit`, `performing-threat-modeling-with-owasp-threat-dragon`
- **C08 钓鱼与社会工程**（25） 触发:钓鱼 / 社会工程 ; phishing, social, performing, phish → `attacking-oauth-with-device-code-phishing`, `conducting-phishing-incident-response`, `conducting-social-engineering-pretext-call`
- **C18 云与容器提权**（14） 触发:云 / 容器提权 ; performing, kubernetes, privilege, escalation → `auditing-kubernetes-rbac-privilege-escalation`, `performing-agentless-vulnerability-scanning`, `performing-aws-account-enumeration-with-scout-suite`
- **C35 C2框架与远控**（21） 触发:C2框架 / 远控 ; performing, infrastructure, building, red → `building-c2-redirector-infrastructure`, `building-red-team-c2-infrastructure-with-havoc`, `exploiting-aws-with-pacu`
- **C42 网络扫描与枚举**（40） 触发:网络扫描 / 枚举 ; scan, network, offensive, sip → `building-vulnerability-scanning-workflow`, `scanning-network-with-nmap-advanced`, `offensive-bug-identification`
- **C01 资产测绘与指纹识别**（62）〔二级子类→ref〕 触发:资产测绘 / 指纹识别 ; recon, osint, performing, enum → `collecting-open-source-intelligence`, `performing-ai-driven-osint-correlation`, `performing-asset-criticality-scoring-for-vulns`
- **C46 二进制漏洞利用与Pwn**（46）〔二级子类→ref〕 触发:二进制漏洞利用 / Pwn ; offensive, exploitation, penetration, ctf → `coercing-authentication-with-coercer-petitpotam`, `conducting-cloud-penetration-testing`, `conducting-network-penetration-test`
- **C10 API与业务逻辑攻击**（54）〔二级子类→ref〕 触发:API / 业务逻辑攻击 ; api, jwt, performing, graphql → `conducting-api-security-testing`, `exploiting-api-injection-vulnerabilities`, `exploiting-idor-vulnerabilities`
- **C05 外部攻击面与云资产暴露**（31） 触发:外部攻击面 / 云资产暴露 ; exposure, offensive, cloud, scan → `conducting-external-reconnaissance-with-osint`, `enumerating-cloud-with-cloudfox`, `exploiting-excessive-data-exposure-in-api`
- **C15 持久化与后门植入**（13） 触发:持久化 / 后门植入 ; persistence, shell, conducting, domain → `conducting-domain-persistence-with-dcsync`, `operating-sliver-c2`, `performing-malware-persistence-investigation`
- **C50 红队方法论与自动化**（38） 触发:红队方法论 / 自动化 ; offensive, team, red, engagement → `conducting-full-scope-red-team-engagement`, `designing-adversary-engagement-with-mitre-engage`, `emulating-cloud-attacks-with-stratus-red-team`
- **C40 嗅探与中间人攻击**（37） 触发:嗅探 / 中间人攻击 ; mitm, network, performing, simulation → `conducting-man-in-the-middle-attack-simulation`, `performing-arp-spoofing-attack-simulation`, `performing-bandwidth-throttling-attack-simulation`
- **C43 移动端攻击**（21） 触发:移动端攻击 ; android, mobile, app, performing → `conducting-mobile-app-penetration-test`, `exploiting-deeplink-vulnerabilities`, `exploiting-insecure-data-storage-in-mobile`
- **C07 载荷开发与武器化**（24） 触发:载荷开发 / 武器化 ; shellcode, evasion, payload, conducting → `conducting-spearphishing-simulation-campaign`, `xss-cross-site-scripting`, `csv-formula-injection`
- **C24 内存转储与LSASS窃取**（5） 触发:内存转储 / LSASS窃取 ; credentials, conducting, pass, ticket → `conducting-pass-the-ticket-attack`, `active-directory-acl-abuse`, `mimikatz-credentials`
- **C12 供应链与CI/CD攻击**（16） 触发:供应链 / CI/CD攻击 ; cicd, offensive, dependency, supply → `continuous-llm-red-teaming-with-promptfoo`, `defending-llms-with-guardrails`, `implementing-fuzz-testing-in-cicd-with-aflplusplus`
- **C04 网络拓扑与互联网测绘**（10） 触发:网络拓扑 / 互联网测绘 ; shodan, network, exploiting, bgp → `exploiting-bgp-hijacking-vulnerabilities`, `performing-ip-reputation-analysis-with-shodan`, `ctf-osint`
- **C26 Kerberos与票据攻击**（8） 触发:Kerberos / 票据攻击 ; kerberos, kerberoasting, exploiting, impacket → `exploiting-kerberoasting-with-impacket`, `extracting-credentials-from-memory-dump`, `performing-kerberoasting-attack`
- **C31 远程服务横向移动**（13） 触发:远程服务横向移动 ; lateral, movement, performing, windows → `exploiting-ms17-010-eternalblue-vulnerability`, `performing-lateral-movement-with-wmiexec`, `performing-lateral-movement-detection`
- **C06 漏洞情报与漏洞库**（14） 触发:漏洞情报 / 漏洞库 ; cve, exploiting, search, log4j → `exploiting-nopac-cve-2021-42278-42287`, `exploiting-zerologon-vulnerability-cve-2020-1472`, `prototype-pollution`
- **C19 EDR与AV规避**（4） 触发:EDR / AV规避 ; evasion, operating, havoc, offensive → `operating-havoc-c2`, `offensive-edr-evasion`, `evasion-specialist`
- **C39 数据破坏与擦除**（3） 触发:数据破坏 / 擦除 ; performing, binary, exploitation, analysis → `performing-binary-exploitation-analysis`, `exploit-development`, `slowhttptest-dos`
- **C41 Web漏洞扫描与验证**（18） 触发:Web漏洞扫描 / 验证 ; performing, scanning, web, dir → `performing-container-security-scanning-with-trivy`, `performing-ssl-tls-security-assessment`, `performing-vulnerability-scanning-with-nessus`
- **C02 域名与DNS侦察**（20） 触发:域名 / DNS侦察 ; dns, subdomain, recon, performing → `performing-dns-enumeration-and-zone-transfer`, `performing-subdomain-enumeration-with-subfinder`, `cors-cross-origin-misconfiguration`
- **C25 哈希与密码破解**（33） 触发:哈希 / 密码破解 ; wordlist, hash, brute, mask → `performing-gcp-penetration-testing-with-gcpbucketbrute`, `performing-hash-cracking-with-hashcat`, `authbypass-authentication-flaws`
- **C22 进程注入与内存执行**（19） 触发:进程注入 / 内存执行 ; injection, header, redteam, llm → `performing-packet-injection-attack`, `red-teaming-llms-with-garak`, `testing-for-host-header-injection`
- **C03 邮箱与人员OSINT**（27） 触发:邮箱 / 人员OSINT ; osint, username, email, breach → `profiling-threat-actor-groups`, `bridgekeeper-username-mangle`, `cr3dov3r-leak-lookup`
- **C17 Windows本地提权**（11） 触发:Windows本地提权 ; windows, privesc, offensive, k8s → `windows-privilege-escalation`, `defi-attack-patterns`, `offensive-k8s-attacks`
- **C49 密码学攻击**（22） 触发:密码学攻击 ; crypto, attacks, rsa, tls → `rsa-attack-techniques`, `symmetric-cipher-attacks`, `lattice-crypto-attacks`
- **C11 边界设备与VPN攻击**（4） 触发:边界设备 / VPN攻击 ; offensive, anti, forensics, scada → `offensive-anti-forensics`, `scada-attacker`, `cameradar-rtsp`
- **C34 屏幕与输入捕获**（3） 触发:屏幕 / 输入捕获 ; offensive, keylogger, arch, scrying → `offensive-keylogger-arch`, `scrying-multi-screenshot`, `witnessme-web-shot`
- **C21 流量混淆与加密隧道**（1） 触发:流量混淆 / 加密隧道 ; offensive, data, exfiltration → `offensive-data-exfiltration`
- **C16 Linux本地提权**（9） 触发:Linux本地提权 ; linux, privesc, escape, container → `linux-privilege-escalation`, `sandbox-escape-techniques`, `privesc-advisor`
- **C47 逆向工程**（4） 触发:逆向工程 ; open, redirect, petools, analysis → `open-redirect`, `exe2hexbat-payload-transfer`, `petools-pe-analysis`
- **C32 隧道与内网穿透**（10） 触发:隧道 / 内网穿透 ; pivot, tunneling, pivoting, stack → `tunneling-and-pivoting`, `stack-overflow-and-rop`, `3proxy-pivot`
- **C37 数据外传**（2） 触发:数据外传 ; data, exfiltrator, dnsteal, dns → `data-exfiltrator`, `dnsteal-dns-exfil`
- **C48 区块链与Web3安全**（5） 触发:区块链 / Web3安全 ; security, mev, smart, contract → `mev-security`, `smart-contract-security`, `solana-security`
- **C28 暴力破解与口令喷射**（14） 触发:暴力破解 / 口令喷射 ; spray, brute, idp, login → `barq-azure-ad`, `kerbrute-kerberos-enum`
- **C29 内网发现与枚举**（18） 触发:内网发现 / 枚举 ; ldap, smb, enum, windapsearch → `ad-ldap-enum-ldap`, `adidnsdump-ldap-enum`
- **C13 远程命令执行与WebShell**（8） 触发:远程命令执行 / WebShell ; shell, manager, pwncat, shellpop → `htshells-htaccess`, `novahot-web-shell`
- **C14 云与容器执行**（3） 触发:云 / 容器执行 ; container, escape, deepce, botb → `botb-container-attack`, `deepce-container-escape`
- **C20 反取证与痕迹清理**（4） 触发:反取证 / 痕迹清理 ; anti, forensic, saruman, mat → `mat-metadata-clean`, `moonwalk-anti-forensic`
- **C38 隐写与隐藏通道**（4） 触发:隐写 / 隐藏通道 ; stego, cloakify, exfil, zsteg → `cloakify-exfil`, `openstego-general-stego`
- **C23 无文件与LOLBins滥用**（2） 触发:无文件 / LOLBins滥用 ; lolbas, living, off, land → `lolbas-living-off-land`, `m3-gen-msbuild`
- **C36 隐蔽回连与通信通道**（3） 触发:隐蔽回连 / 通信通道 ; websockify, bridge, icmpsh, reverse → `icmpsh-reverse`, `interactsh-oob`
- **C45 恶意软件开发与免杀**（9） 触发:恶意软件开发 / 免杀 ; macro, veil, framework, sigthief → `avet-av-evasion`, `bluffy-hollow`
- **C09 Web应用漏洞利用**（171）〔二级子类→ref〕 触发:Web应用漏洞利用 ; offensive, exploiting, injection, performing → `bypassing-authentication-with-forced-browsing`, `escaping-containers-to-host`, `exploiting-broken-function-level-authorization`

## 库结构

- 文件库根：`/opt/attack-skill-library/`（可用环境变量 `SKILL_LIBRARY` 覆盖，下文路径均以库根为准）
- 每个 skill 一个目录：`{LIB}/<slug>/SKILL.md`（正文，只留决策树+核心命令），同目录可能有 `reference.md`（按需展开的详情）
- 库根索引：[INDEX.md](../INDEX.md)（989 skill 全清单，按 50 类分组；部署后位于库根）、`MERGES.md`（重叠团合并裁决记录）

> 📎 每类完整 primary（最多 5 个）、二级子路由样例、secondary grep 词，全部在同目录 `reference.md` 对应 `#Cxx` 小节，用 Read 按需读取。
