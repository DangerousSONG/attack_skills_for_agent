---
name: attack-skill-router
description: 攻击侧 Skill 库的路由层。当任务涉及渗透测试任一环节（侦察/利用/提权/横向/持久化等）时，先加载本 skill 按「服务/技术/CVE → 推荐 skill」表选用 3-5 个 primary skill，再定向加载；不要在 1000 个 SKILL.md 里盲目 grep 全读。
when-to-use: 任何渗透任务开题时；已加载 skill 不足以解决当前障碍时回来换路由。
---

# Attack Skill Router · 攻击 Skill 路由层（v0.1）

## 用途

本库共 ~1000 个 skill（50 个攻击大类）。直接全库搜索会让 Agent 面对过量同质选项（实测：反序列化主题曾一次装入 3 个重叠 skill）。
**本路由层把「1000 选 N」压缩为「50 类选 1 类 → 每类 3-5 个 primary 选 1-3 个」**。

## 使用流程（必须按序）

1. **定位大类**：用下方「路由表」按 服务类型 / 漏洞类别 / 技术关键词 / CVE 命中一行；
2. **选 primary**：在该行的 3-5 个 slug 中，按 when-to-use 选 1-3 个最贴切的，用 Skill 工具加载；
3. **不够再扩**：primary 解决不了时，回路由表看 secondary 提示（`更多: grep -ril <关键词> /root/.claude/skills`），或按工具名定向加载 tool-skills/ 下的工具改写 skill；
4. **报告**：最终报告末尾列出实际加载的 slug（与评测工作流一致）。

## 选用规则

- **方法论优先于工具**：先选 methodology skill（教你利用链），工具改写 skill（单个工具的说明书）在方法论缺具体命令时补；
- **同主题只装一个**：路由表内同主题已做去重（见配套 MERGES.md），若 grep 仍命中多个相似 slug，选 frontmatter 里 when-to-use 与当前服务/版本最贴合的那个；
- **版本敏感型任务**（Java 反序列化 gadget、内核 exploit 等）：方法论 skill 只能给思路，gadget 适配属 exploit 工程，按 skill 指引 + 目标版本自建，不要反复重试库内旧 gadget。

## 路由表（50 类 · 每类 primary slug）

### C27 本地凭证与浏览器窃取（4 个 · TA0006）

- 触发词：本地凭证 / 浏览器窃取 ｜ EN: credential, access, abusing, dpapi
- `abusing-dpapi-for-credential-access` — Anthropic-Cybersecurity-Skills
- `extracting-browser-history-artifacts` — Anthropic-Cybersecurity-Skills
- `performing-credential-access-with-lazagne` — Anthropic-Cybersecurity-Skills
- 更多 1 个: `grep -ril -e credential -e access /root/.claude/skills --include=SKILL.md`

### C33 数据收集与打包暂存（4 个 · TA0009）

- 触发词：数据收集 / 打包暂存 ｜ EN: acquiring, disk, image, dcfldd
- `acquiring-disk-image-with-dd-and-dcfldd` — Anthropic-Cybersecurity-Skills
- `paramspider-param-harvest` — 改写
- `tlsx-tls-enum` — 改写
- 更多 1 个: `grep -ril -e acquiring -e disk /root/.claude/skills --include=SKILL.md`

### C30 AD域渗透与域控攻击（50 个 · TA0008）

- 触发词：AD域渗透 / 域控攻击 ｜ EN: active, directory, bloodhound, exploiting
- `abusing-shadow-credentials-for-privesc` — Anthropic-Cybersecurity-Skills
- `attacking-entra-id-with-roadtools` — Anthropic-Cybersecurity-Skills
- `conducting-internal-reconnaissance-with-bloodhound-ce` — Anthropic-Cybersecurity-Skills
- `aclpwn-acl-abuse` — 改写
- `activedirectoryenum-ad` — 改写
- 更多 45 个: `grep -ril -e active -e directory /root/.claude/skills --include=SKILL.md`

### C44 AI与大模型安全（12 个 · TA0001）

- 触发词：AI / 大模型安全 ｜ EN: llm, attacks, threat, security
- `assessing-vector-and-embedding-weaknesses` — Anthropic-Cybersecurity-Skills
- `orchestrating-llm-attacks-with-pyrit` — Anthropic-Cybersecurity-Skills
- `performing-threat-modeling-with-owasp-threat-dragon` — Anthropic-Cybersecurity-Skills
- `hexstrike-ai` — 改写
- `pentestagent-crewai` — 改写
- 更多 7 个: `grep -ril -e llm -e attacks /root/.claude/skills --include=SKILL.md`

### C08 钓鱼与社会工程（25 个 · TA0001）

- 触发词：钓鱼 / 社会工程 ｜ EN: phishing, social, performing, phish
- `attacking-oauth-with-device-code-phishing` — Anthropic-Cybersecurity-Skills
- `conducting-phishing-incident-response` — Anthropic-Cybersecurity-Skills
- `conducting-social-engineering-pretext-call` — Anthropic-Cybersecurity-Skills
- `bad-pdf-phish` — 改写
- `credsniper-phish` — 改写
- 更多 20 个: `grep -ril -e phishing -e social /root/.claude/skills --include=SKILL.md`

### C18 云与容器提权（14 个 · TA0004）

- 触发词：云 / 容器提权 ｜ EN: performing, kubernetes, privilege, escalation
- `auditing-kubernetes-rbac-privilege-escalation` — Anthropic-Cybersecurity-Skills
- `performing-agentless-vulnerability-scanning` — Anthropic-Cybersecurity-Skills
- `performing-aws-account-enumeration-with-scout-suite` — Anthropic-Cybersecurity-Skills
- `cloudlist-multi-cloud` — 改写
- `microburst-azure` — 改写
- 更多 9 个: `grep -ril -e performing -e kubernetes /root/.claude/skills --include=SKILL.md`

### C35 C2框架与远控（22 个 · TA0011）

- 触发词：C2框架 / 远控 ｜ EN: performing, infrastructure, building, red
- `building-c2-redirector-infrastructure` — Anthropic-Cybersecurity-Skills
- `building-red-team-c2-infrastructure-with-havoc` — Anthropic-Cybersecurity-Skills
- `exploiting-aws-with-pacu` — Anthropic-Cybersecurity-Skills
- `adaptix-c2-framework` — 改写
- `emp3r0r-c2` — 改写
- 更多 17 个: `grep -ril -e performing -e infrastructure /root/.claude/skills --include=SKILL.md`

### C42 网络扫描与枚举（40 个 · TA0043）

- 触发词：网络扫描 / 枚举 ｜ EN: scan, network, offensive, sip
- `building-vulnerability-scanning-workflow` — Anthropic-Cybersecurity-Skills
- `scanning-network-with-nmap-advanced` — Anthropic-Cybersecurity-Skills
- `offensive-bug-identification` — Claude-Red-pentest-set
- `angry-ip-scan` — 改写
- `apachetomcatscanner-tomcat` — 改写
- 更多 35 个: `grep -ril -e scan -e network /root/.claude/skills --include=SKILL.md`

### C01 资产测绘与指纹识别（62 个 · TA0043）

- 触发词：资产测绘 / 指纹识别 ｜ EN: recon, osint, performing, enum
- `collecting-open-source-intelligence` — Anthropic-Cybersecurity-Skills
- `performing-ai-driven-osint-correlation` — Anthropic-Cybersecurity-Skills
- `performing-asset-criticality-scoring-for-vulns` — Anthropic-Cybersecurity-Skills
- `alterx-dsl-subdomains` — 改写
- `amass-attack-surface` — 改写
- 更多 57 个: `grep -ril -e recon -e osint /root/.claude/skills --include=SKILL.md`

### C46 二进制漏洞利用与Pwn（47 个 · TA0002）

- 触发词：二进制漏洞利用 / Pwn ｜ EN: offensive, exploitation, penetration, ctf
- `coercing-authentication-with-coercer-petitpotam` — Anthropic-Cybersecurity-Skills
- `conducting-cloud-penetration-testing` — Anthropic-Cybersecurity-Skills
- `conducting-network-penetration-test` — Anthropic-Cybersecurity-Skills
- `angrop-rop-gen` — 改写
- `armscgen-shellcode` — 改写
- 更多 42 个: `grep -ril -e offensive -e exploitation /root/.claude/skills --include=SKILL.md`

### C10 API与业务逻辑攻击（54 个 · TA0001）

- 触发词：API / 业务逻辑攻击 ｜ EN: api, jwt, performing, graphql
- `conducting-api-security-testing` — Anthropic-Cybersecurity-Skills
- `exploiting-api-injection-vulnerabilities` — Anthropic-Cybersecurity-Skills
- `exploiting-idor-vulnerabilities` — Anthropic-Cybersecurity-Skills
- `astra-api-scan` — 改写
- `cariddi-crawler-secrets` — 改写
- 更多 49 个: `grep -ril -e api -e jwt /root/.claude/skills --include=SKILL.md`

### C09 Web应用漏洞利用（177 个 · TA0001）

- 触发词：Web应用漏洞利用 ｜ EN: offensive, exploiting, injection, performing
- `bypassing-authentication-with-forced-browsing` — Anthropic-Cybersecurity-Skills
- `escaping-containers-to-host` — Anthropic-Cybersecurity-Skills
- `exploiting-broken-function-level-authorization` — Anthropic-Cybersecurity-Skills
- `bbqsql-blind-sqlmap` — 改写
- `bbscan-batch-scan` — 改写
- `java-deserialization-gadget-selector` — 改写
- 更多 171 个: `grep -ril -e offensive -e exploiting /root/.claude/skills --include=SKILL.md`

### C05 外部攻击面与云资产暴露（31 个 · TA0043）

- 触发词：外部攻击面 / 云资产暴露 ｜ EN: exposure, offensive, cloud, scan
- `conducting-external-reconnaissance-with-osint` — Anthropic-Cybersecurity-Skills
- `enumerating-cloud-with-cloudfox` — Anthropic-Cybersecurity-Skills
- `exploiting-excessive-data-exposure-in-api` — Anthropic-Cybersecurity-Skills
- `apkleaks-endpoint-scan` — 改写
- `gh-dork-github` — 改写
- 更多 26 个: `grep -ril -e exposure -e offensive /root/.claude/skills --include=SKILL.md`

### C15 持久化与后门植入（13 个 · TA0003）

- 触发词：持久化 / 后门植入 ｜ EN: persistence, shell, conducting, domain
- `conducting-domain-persistence-with-dcsync` — Anthropic-Cybersecurity-Skills
- `operating-sliver-c2` — Anthropic-Cybersecurity-Skills
- `performing-malware-persistence-investigation` — Anthropic-Cybersecurity-Skills
- `dbd-dns-tunnel-shell` — 改写
- `gcat-gmail-c2` — 改写
- 更多 8 个: `grep -ril -e persistence -e shell /root/.claude/skills --include=SKILL.md`

### C50 红队方法论与自动化（38 个 · TA0002）

- 触发词：红队方法论 / 自动化 ｜ EN: offensive, team, red, engagement
- `conducting-full-scope-red-team-engagement` — Anthropic-Cybersecurity-Skills
- `designing-adversary-engagement-with-mitre-engage` — Anthropic-Cybersecurity-Skills
- `emulating-cloud-attacks-with-stratus-red-team` — Anthropic-Cybersecurity-Skills
- `cloudfail-cloud-origin` — 改写
- `interlace-parallel` — 改写
- 更多 33 个: `grep -ril -e offensive -e team /root/.claude/skills --include=SKILL.md`

### C40 嗅探与中间人攻击（37 个 · TA0009）

- 触发词：嗅探 / 中间人攻击 ｜ EN: mitm, network, performing, simulation
- `conducting-man-in-the-middle-attack-simulation` — Anthropic-Cybersecurity-Skills
- `performing-arp-spoofing-attack-simulation` — Anthropic-Cybersecurity-Skills
- `performing-bandwidth-throttling-attack-simulation` — Anthropic-Cybersecurity-Skills
- `above-protocol-anomaly` — 改写
- `arpspoof-smikims` — 改写
- 更多 32 个: `grep -ril -e mitm -e network /root/.claude/skills --include=SKILL.md`

### C43 移动端攻击（21 个 · TA0001）

- 触发词：移动端攻击 ｜ EN: android, mobile, app, performing
- `conducting-mobile-app-penetration-test` — Anthropic-Cybersecurity-Skills
- `exploiting-deeplink-vulnerabilities` — Anthropic-Cybersecurity-Skills
- `exploiting-insecure-data-storage-in-mobile` — Anthropic-Cybersecurity-Skills
- `appmon-ios-android` — 改写
- `bagbak-ios-decrypt` — 改写
- 更多 16 个: `grep -ril -e android -e mobile /root/.claude/skills --include=SKILL.md`

### C07 载荷开发与武器化（24 个 · TA0042）

- 触发词：载荷开发 / 武器化 ｜ EN: shellcode, evasion, payload, conducting
- `conducting-spearphishing-simulation-campaign` — Anthropic-Cybersecurity-Skills
- `xss-cross-site-scripting` — hack-skills
- `csv-formula-injection` — hack-skills
- `chankro-php-binary` — 改写
- `gadgettojscript-deser` — 改写
- 更多 19 个: `grep -ril -e shellcode -e evasion /root/.claude/skills --include=SKILL.md`

### C24 内存转储与LSASS窃取（5 个 · TA0006）

- 触发词：内存转储 / LSASS窃取 ｜ EN: credentials, conducting, pass, ticket
- `conducting-pass-the-ticket-attack` — Anthropic-Cybersecurity-Skills
- `active-directory-acl-abuse` — hack-skills
- `mimikatz-credentials` — 改写
- `mimipenguin-linux` — 改写
- 更多 1 个: `grep -ril -e credentials -e conducting /root/.claude/skills --include=SKILL.md`

### C12 供应链与CI/CD攻击（16 个 · TA0001）

- 触发词：供应链 / CI/CD攻击 ｜ EN: cicd, offensive, dependency, supply
- `continuous-llm-red-teaming-with-promptfoo` — Anthropic-Cybersecurity-Skills
- `defending-llms-with-guardrails` — Anthropic-Cybersecurity-Skills
- `implementing-fuzz-testing-in-cicd-with-aflplusplus` — Anthropic-Cybersecurity-Skills
- `dvcs-ripper-vcs` — 改写
- `git-dumper-repo` — 改写
- 更多 11 个: `grep -ril -e cicd -e offensive /root/.claude/skills --include=SKILL.md`

### C04 网络拓扑与互联网测绘（10 个 · TA0043）

- 触发词：网络拓扑 / 互联网测绘 ｜ EN: shodan, network, exploiting, bgp
- `exploiting-bgp-hijacking-vulnerabilities` — Anthropic-Cybersecurity-Skills
- `performing-ip-reputation-analysis-with-shodan` — Anthropic-Cybersecurity-Skills
- `ctf-osint` — ctf-skills
- `asnmap-network-recon` — 改写
- `fav-up-favicon-lookup` — 改写
- 更多 5 个: `grep -ril -e shodan -e network /root/.claude/skills --include=SKILL.md`

### C26 Kerberos与票据攻击（8 个 · TA0006）

- 触发词：Kerberos / 票据攻击 ｜ EN: kerberos, kerberoasting, exploiting, impacket
- `exploiting-kerberoasting-with-impacket` — Anthropic-Cybersecurity-Skills
- `extracting-credentials-from-memory-dump` — Anthropic-Cybersecurity-Skills
- `performing-kerberoasting-attack` — Anthropic-Cybersecurity-Skills
- `kekeo-kerberos` — 改写
- `krbrelayx-kerberos-relay` — 改写
- 更多 3 个: `grep -ril -e kerberos -e kerberoasting /root/.claude/skills --include=SKILL.md`

### C31 远程服务横向移动（13 个 · TA0008）

- 触发词：远程服务横向移动 ｜ EN: lateral, movement, performing, windows
- `exploiting-ms17-010-eternalblue-vulnerability` — Anthropic-Cybersecurity-Skills
- `performing-lateral-movement-with-wmiexec` — Anthropic-Cybersecurity-Skills
- `performing-lateral-movement-detection` — Anthropic-Cybersecurity-Skills
- `barmie-rmi-attack` — 改写
- `impacket-protocol-exec` — 改写
- 更多 8 个: `grep -ril -e lateral -e movement /root/.claude/skills --include=SKILL.md`

### C06 漏洞情报与漏洞库（14 个 · TA0043）

- 触发词：漏洞情报 / 漏洞库 ｜ EN: cve, exploiting, search, log4j
- `exploiting-nopac-cve-2021-42278-42287` — Anthropic-Cybersecurity-Skills
- `exploiting-zerologon-vulnerability-cve-2020-1472` — Anthropic-Cybersecurity-Skills
- `prototype-pollution` — hack-skills
- `exploitdb-search` — 改写
- `getsploit-exploit-search` — 改写
- 更多 9 个: `grep -ril -e cve -e exploiting /root/.claude/skills --include=SKILL.md`

### C19 EDR与AV规避（4 个 · TA0005）

- 触发词：EDR / AV规避 ｜ EN: evasion, operating, havoc, offensive
- `operating-havoc-c2` — Anthropic-Cybersecurity-Skills
- `offensive-edr-evasion` — Claude-Red-pentest-set
- `evasion-specialist` — pentest-ai-agents
- 更多 1 个: `grep -ril -e evasion -e operating /root/.claude/skills --include=SKILL.md`

### C39 数据破坏与擦除（3 个 · TA0040）

- 触发词：数据破坏 / 擦除 ｜ EN: performing, binary, exploitation, analysis
- `performing-binary-exploitation-analysis` — Anthropic-Cybersecurity-Skills
- `exploit-development` — offensive-claude
- `slowhttptest-dos` — 改写

### C41 Web漏洞扫描与验证（18 个 · TA0043）

- 触发词：Web漏洞扫描 / 验证 ｜ EN: performing, scanning, web, dir
- `performing-container-security-scanning-with-trivy` — Anthropic-Cybersecurity-Skills
- `performing-ssl-tls-security-assessment` — Anthropic-Cybersecurity-Skills
- `performing-vulnerability-scanning-with-nessus` — Anthropic-Cybersecurity-Skills
- `arjun-param-discovery` — 改写
- `cangibrina-admin-finder` — 改写
- 更多 13 个: `grep -ril -e performing -e scanning /root/.claude/skills --include=SKILL.md`

### C02 域名与DNS侦察（20 个 · TA0043）

- 触发词：域名 / DNS侦察 ｜ EN: dns, subdomain, recon, performing
- `performing-dns-enumeration-and-zone-transfer` — Anthropic-Cybersecurity-Skills
- `performing-subdomain-enumeration-with-subfinder` — Anthropic-Cybersecurity-Skills
- `cors-cross-origin-misconfiguration` — hack-skills
- `aiodnsbrute-dns` — 改写
- `altdns-permutation` — 改写
- 更多 15 个: `grep -ril -e dns -e subdomain /root/.claude/skills --include=SKILL.md`

### C25 哈希与密码破解（33 个 · TA0006）

- 触发词：哈希 / 密码破解 ｜ EN: wordlist, hash, brute, mask
- `performing-gcp-penetration-testing-with-gcpbucketbrute` — Anthropic-Cybersecurity-Skills
- `performing-hash-cracking-with-hashcat` — Anthropic-Cybersecurity-Skills
- `authbypass-authentication-flaws` — hack-skills
- `bkcrack-zip-plaintext` — 改写
- `bopscrk-smart-wordlist` — 改写
- 更多 28 个: `grep -ril -e wordlist -e hash /root/.claude/skills --include=SKILL.md`

### C22 进程注入与内存执行（19 个 · TA0005）

- 触发词：进程注入 / 内存执行 ｜ EN: injection, header, redteam, llm
- `performing-packet-injection-attack` — Anthropic-Cybersecurity-Skills
- `red-teaming-llms-with-garak` — Anthropic-Cybersecurity-Skills
- `testing-for-host-header-injection` — Anthropic-Cybersecurity-Skills
- `amber-reflective-packer` — 改写
- 更多 15 个: `grep -ril -e injection -e header /root/.claude/skills --include=SKILL.md`

### C03 邮箱与人员OSINT（27 个 · TA0043）

- 触发词：邮箱 / 人员OSINT ｜ EN: osint, username, email, breach
- `profiling-threat-actor-groups` — Anthropic-Cybersecurity-Skills
- `bridgekeeper-username-mangle` — 改写
- `cr3dov3r-leak-lookup` — 改写
- 更多 24 个: `grep -ril -e osint -e username /root/.claude/skills --include=SKILL.md`

### C17 Windows本地提权（11 个 · TA0004）

- 触发词：Windows本地提权 ｜ EN: windows, privesc, offensive, k8s
- `windows-privilege-escalation` — hack-skills
- `defi-attack-patterns` — hack-skills
- `offensive-k8s-attacks` — Claude-Red-pentest-set
- `beroot-privesc-check` — 改写
- `powershdll-nopowershell` — 改写
- 更多 6 个: `grep -ril -e windows -e privesc /root/.claude/skills --include=SKILL.md`

### C49 密码学攻击（22 个 · TA0006）

- 触发词：密码学攻击 ｜ EN: crypto, attacks, rsa, tls
- `rsa-attack-techniques` — hack-skills
- `symmetric-cipher-attacks` — hack-skills
- `lattice-crypto-attacks` — hack-skills
- `a2sv-ssl-vuln` — 改写
- `cero-tls-cert` — 改写
- 更多 17 个: `grep -ril -e crypto -e attacks /root/.claude/skills --include=SKILL.md`

### C11 边界设备与VPN攻击（4 个 · TA0001）

- 触发词：边界设备 / VPN攻击 ｜ EN: offensive, anti, forensics, scada
- `offensive-anti-forensics` — Claude-Red-pentest-set
- `scada-attacker` — pentest-ai-agents
- `cameradar-rtsp` — 改写
- `sigploit-telecom` — 改写

### C34 屏幕与输入捕获（3 个 · TA0009）

- 触发词：屏幕 / 输入捕获 ｜ EN: offensive, keylogger, arch, scrying
- `offensive-keylogger-arch` — Claude-Red-pentest-set
- `scrying-multi-screenshot` — 改写
- `witnessme-web-shot` — 改写

### C21 流量混淆与加密隧道（1 个 · TA0005）

- 触发词：流量混淆 / 加密隧道 ｜ EN: offensive, data, exfiltration
- `offensive-data-exfiltration` — Claude-Red-pentest-set

### C16 Linux本地提权（9 个 · TA0004）

- 触发词：Linux本地提权 ｜ EN: linux, privesc, escape, container
- `linux-privilege-escalation` — hack-skills
- `sandbox-escape-techniques` — hack-skills
- `privesc-advisor` — pentest-ai-agents
- `climber-linux-audit` — 改写
- `linenum-privesc-scan` — 改写
- 更多 4 个: `grep -ril -e linux -e privesc /root/.claude/skills --include=SKILL.md`

### C47 逆向工程（4 个 · TA0007）

- 触发词：逆向工程 ｜ EN: open, redirect, petools, analysis
- `open-redirect` — hack-skills
- `exe2hexbat-payload-transfer` — 改写
- `petools-pe-analysis` — 改写
- 更多 1 个: `grep -ril -e open -e redirect /root/.claude/skills --include=SKILL.md`

### C32 隧道与内网穿透（10 个 · TA0008）

- 触发词：隧道 / 内网穿透 ｜ EN: pivot, tunneling, pivoting, stack
- `tunneling-and-pivoting` — hack-skills
- `stack-overflow-and-rop` — hack-skills
- `3proxy-pivot` — 改写
- `crypthook-encrypted-tunnel` — 改写
- 更多 6 个: `grep -ril -e pivot -e tunneling /root/.claude/skills --include=SKILL.md`

### C37 数据外传（2 个 · TA0010）

- 触发词：数据外传 ｜ EN: data, exfiltrator, dnsteal, dns
- `data-exfiltrator` — pentest-ai-agents
- `dnsteal-dns-exfil` — 改写

### C48 区块链与Web3安全（5 个 · TA0001）

- 触发词：区块链 / Web3安全 ｜ EN: security, mev, smart, contract
- `mev-security` — awesome-web3-security
- `smart-contract-security` — awesome-web3-security
- `solana-security` — awesome-web3-security
- `slither-solidity-audit` — 改写
- 更多 1 个: `grep -ril -e security -e mev /root/.claude/skills --include=SKILL.md`

### C28 暴力破解与口令喷射（14 个 · TA0006）

- 触发词：暴力破解 / 口令喷射 ｜ EN: spray, brute, idp, login
- `barq-azure-ad` — 改写
- `kerbrute-kerberos-enum` — 改写
- 更多 12 个: `grep -ril -e spray -e brute /root/.claude/skills --include=SKILL.md`

### C29 内网发现与枚举（18 个 · TA0007）

- 触发词：内网发现 / 枚举 ｜ EN: ldap, smb, enum, windapsearch
- `ad-ldap-enum-ldap` — 改写
- `adidnsdump-ldap-enum` — 改写
- 更多 16 个: `grep -ril -e ldap -e smb /root/.claude/skills --include=SKILL.md`

### C13 远程命令执行与WebShell（8 个 · TA0002）

- 触发词：远程命令执行 / WebShell ｜ EN: shell, manager, pwncat, shellpop
- `htshells-htaccess` — 改写
- `novahot-web-shell` — 改写
- 更多 6 个: `grep -ril -e shell -e manager /root/.claude/skills --include=SKILL.md`

### C14 云与容器执行（3 个 · TA0002）

- 触发词：云 / 容器执行 ｜ EN: container, escape, deepce, botb
- `botb-container-attack` — 改写
- `deepce-container-escape` — 改写
- 更多 1 个: `grep -ril -e container -e escape /root/.claude/skills --include=SKILL.md`

### C20 反取证与痕迹清理（4 个 · TA0005）

- 触发词：反取证 / 痕迹清理 ｜ EN: anti, forensic, saruman, mat
- `mat-metadata-clean` — 改写
- `moonwalk-anti-forensic` — 改写
- 更多 2 个: `grep -ril -e anti -e forensic /root/.claude/skills --include=SKILL.md`

### C38 隐写与隐藏通道（4 个 · TA0010）

- 触发词：隐写 / 隐藏通道 ｜ EN: stego, cloakify, exfil, zsteg
- `cloakify-exfil` — 改写
- `openstego-general-stego` — 改写
- 更多 2 个: `grep -ril -e stego -e cloakify /root/.claude/skills --include=SKILL.md`

### C23 无文件与LOLBins滥用（2 个 · TA0005）

- 触发词：无文件 / LOLBins滥用 ｜ EN: lolbas, living, off, land
- `lolbas-living-off-land` — 改写
- `m3-gen-msbuild` — 改写

### C36 隐蔽回连与通信通道（3 个 · TA0011）

- 触发词：隐蔽回连 / 通信通道 ｜ EN: websockify, bridge, icmpsh, reverse
- `icmpsh-reverse` — 改写
- `interactsh-oob` — 改写
- 更多 1 个: `grep -ril -e websockify -e bridge /root/.claude/skills --include=SKILL.md`

### C45 恶意软件开发与免杀（9 个 · TA0005）

- 触发词：恶意软件开发 / 免杀 ｜ EN: macro, veil, framework, sigthief
- `avet-av-evasion` — 改写
- `bluffy-hollow` — 改写
- 更多 7 个: `grep -ril -e macro -e veil /root/.claude/skills --include=SKILL.md`

## 附

- primary 总数：198（磁盘总量 ~1000，secondary 按需 grep，不主动加载）
- 维护：新增 skill 入 CSV 后重跑路由生成脚本；类别内排名按「方法论仓库优先级 + 工具名字序」
- 配套文件：MERGES.md（建议合并的重叠团清单，v0.1 待人工裁决）
