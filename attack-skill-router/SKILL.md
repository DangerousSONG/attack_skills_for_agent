---
name: attack-skill-router
description: 攻击侧 Skill 库的路由层。当任务涉及渗透测试任一环节（侦察/利用/提权/横向/持久化等）时，先加载本 skill 按「服务/技术/CVE → 推荐 skill」表选用 3-5 个 primary skill，再定向加载；不要在 1000 个 SKILL.md 里盲目 grep 全读。
when-to-use: 任何渗透任务开题时；已加载 skill 不足以解决当前障碍时回来换路由。
---

# Attack Skill Router · 攻击 Skill 路由层（v2.0）

## 用途

本库共 996 个 skill（50 个攻击大类）。直接全库搜索会让 Agent 面对过量同质选项（实测：反序列化主题曾一次装入 3 个重叠 skill）。
**本路由层把「996 选 N」压缩为「50 类选 1 类 → 每类 3-5 个 primary 选 1-3 个」**。

## 使用流程（必须按序）

1. **定位大类**：用下方「路由表」按 服务类型 / 漏洞类别 / 技术关键词 / CVE 命中一行；
2. **选 primary**：在该行的 3-5 个 slug 中，按 when-to-use 选 1-3 个最贴切的，用 Skill 工具加载；
3. **不够再扩**：大类标了〔二级子类→ref〕的（本类 skill 多），展开同目录 `reference.md` 按子标签细选；其余用 `grep -ril <关键词> /opt/attack-skill-library` 定向补；
4. **报告**：最终报告末尾列出实际加载的 slug（与评测工作流一致）。

## 选用规则

- **方法论优先于工具**：先选 methodology skill（教你利用链），工具改写 skill（单个工具的说明书）在方法论缺具体命令时补；
- **同主题只装一个**：路由表内同主题已做去重（见配套 MERGES.md，已完成人工裁决 13 并 / 7 不并），若 grep 仍命中多个相似 slug，选 frontmatter 里 when-to-use 与当前服务/版本最贴合的那个；
- **版本敏感型任务**（Java 反序列化 gadget、内核 exploit 等）：方法论 skill 只能给思路，gadget 适配属 exploit 工程，按 skill 指引 + 目标版本自建，不要反复重试库内旧 gadget。

## 路由表（50 类 · 每类 primary 5 个 · 一行一类）

- **C01 资产测绘与指纹识别**（62）〔二级子类→ref〕 触发:资产测绘 / 指纹识别 ; recon, osint, performing → `performing-timeline-reconstruction-with-plaso`, `collecting-open-source-intelligence`, `performing-asset-criticality-scoring-for-vulns`, `alterx-dsl-subdomains`, `amass-attack-surface`
- **C02 域名与DNS侦察**（19） 触发:域名 / DNS侦察 ; dns, subdomain, performing → `performing-dns-enumeration-and-zone-transfer`, `performing-subdomain-enumeration-with-subfinder`, `cors-cross-origin-misconfiguration`, `aiodnsbrute-dns`, `altdns-permutation` ; 更多 14 个 grep 扩
- **C03 邮箱与人员OSINT**（27） 触发:邮箱 / 人员OSINT ; osint, username, email → `profiling-threat-actor-groups`, `bridgekeeper-username-mangle`, `cr3dov3r-leak-lookup` ; 更多 24 个 grep 扩
- **C04 网络拓扑与互联网测绘**（10） 触发:网络拓扑 / 互联网测绘 ; shodan, network, performing → `performing-ip-reputation-analysis-with-shodan`, `exploiting-bgp-hijacking-vulnerabilities`, `ctf-osint`, `asnmap-network-recon`, `fav-up-favicon-lookup` ; 更多 5 个 grep 扩
- **C05 外部攻击面与云资产暴露**（31） 触发:外部攻击面 / 云资产暴露 ; exposure, offensive, cloud → `enumerating-cloud-with-cloudfox`, `conducting-external-reconnaissance-with-osint`, `exploiting-excessive-data-exposure-in-api`, `apkleaks-endpoint-scan`, `gh-dork-github` ; 更多 26 个 grep 扩
- **C06 漏洞情报与漏洞库**（14） 触发:漏洞情报 / 漏洞库 ; cve, exploiting, log4j → `exploiting-nopac-cve-2021-42278-42287`, `exploiting-zerologon-vulnerability-cve-2020-1472`, `race-condition`, `exploitdb-search`, `getsploit-exploit-search` ; 更多 9 个 grep 扩
- **C07 载荷开发与武器化**（24） 触发:载荷开发 / 武器化 ; shellcode, payload, evasion → `conducting-spearphishing-simulation-campaign`, `reverse-shell-techniques`, `csv-formula-injection`, `chankro-php-binary`, `gadgettojscript-deser` ; 更多 19 个 grep 扩
- **C08 钓鱼与社会工程**（25） 触发:钓鱼 / 社会工程 ; phishing, performing, social → `performing-red-team-phishing-with-gophish`, `attacking-oauth-with-device-code-phishing`, `conducting-social-engineering-pretext-call`, `bad-pdf-phish`, `credsniper-phish` ; 更多 20 个 grep 扩
- **C09 Web应用漏洞利用**（171）〔二级子类→ref〕 触发:Web应用漏洞利用 ; offensive, performing, exploiting → `performing-web-cache-poisoning-attack`, `exploiting-template-injection-vulnerabilities`, `testing-for-xml-injection-vulnerabilities`, `bbqsql-blind-sqlmap`, `java-deserialization-gadget-selector`
- **C10 API与业务逻辑攻击**（54）〔二级子类→ref〕 触发:API / 业务逻辑攻击 ; api, jwt, performing → `exploiting-idor-vulnerabilities`, `testing-api-security-with-owasp-top-10`, `performing-graphql-security-assessment`, `astra-api-scan`, `cariddi-crawler-secrets`
- **C11 边界设备与VPN攻击**（4） 触发:边界设备 / VPN攻击 ; scada, attacker, cameradar → `offensive-anti-forensics`, `scada-attacker`, `cameradar-rtsp`, `sigploit-telecom` ; 更多 0 个 grep 扩
- **C12 供应链与CI/CD攻击**（16） 触发:供应链 / CI/CD攻击 ; cicd, offensive, dependency → `testing-prompt-injection-in-rag-pipelines`, `implementing-fuzz-testing-in-cicd-with-aflplusplus`, `performing-sca-dependency-scanning-with-snyk`, `dvcs-ripper-vcs`, `git-dumper-repo` ; 更多 11 个 grep 扩
- **C13 远程命令执行与WebShell**（8） 触发:远程命令执行 / WebShell ; shell, manager, shellme → `htshells-htaccess`, `novahot-web-shell` ; 更多 6 个 grep 扩
- **C14 云与容器执行**（3） 触发:云 / 容器执行 ; container, escape, deepce → `botb-container-attack`, `deepce-container-escape` ; 更多 1 个 grep 扩
- **C15 持久化与后门植入**（13） 触发:持久化 / 后门植入 ; persistence, shell, performing → `performing-malware-persistence-investigation`, `operating-sliver-c2`, `conducting-domain-persistence-with-dcsync`, `dbd-dns-tunnel-shell`, `gcat-gmail-c2` ; 更多 8 个 grep 扩
- **C16 Linux本地提权**（8） 触发:Linux本地提权 ; privesc, linux, escape → `sandbox-escape-techniques`, `linux-privilege-escalation`, `privesc-advisor`, `linenum-privesc-scan`, `suid3num-privesc` ; 更多 3 个 grep 扩
- **C17 Windows本地提权**（11） 触发:Windows本地提权 ; windows, privesc, lateral → `defi-attack-patterns`, `windows-privilege-escalation`, `offensive-k8s-attacks`, `beroot-privesc-check`, `powershdll-nopowershell` ; 更多 6 个 grep 扩
- **C18 云与容器提权**（14） 触发:云 / 容器提权 ; performing, kubernetes, privilege → `auditing-kubernetes-rbac-privilege-escalation`, `performing-kubernetes-penetration-testing`, `performing-agentless-vulnerability-scanning`, `cloudlist-multi-cloud`, `microburst-azure` ; 更多 9 个 grep 扩
- **C19 EDR与AV规避**（4） 触发:EDR / AV规避 ; evasion, operating, havoc → `operating-havoc-c2`, `offensive-edr-evasion`, `evasion-specialist` ; 更多 1 个 grep 扩
- **C20 反取证与痕迹清理**（4） 触发:反取证 / 痕迹清理 ; anti, forensic, mat → `mat-metadata-clean`, `moonwalk-anti-forensic` ; 更多 2 个 grep 扩
- **C21 流量混淆与加密隧道**（1） 触发:流量混淆 / 加密隧道 ; offensive, data, exfiltration → `offensive-data-exfiltration` ; 更多 0 个 grep 扩
- **C22 进程注入与内存执行**（19） 触发:进程注入 / 内存执行 ; injection, header, llm → `red-teaming-llms-with-garak`, `testing-for-email-header-injection`, `testing-for-host-header-injection`, `amber-reflective-packer` ; 更多 15 个 grep 扩
- **C23 无文件与LOLBins滥用**（2） 触发:无文件 / LOLBins滥用 ; lolbas, living, off → `lolbas-living-off-land`, `m3-gen-msbuild` ; 更多 0 个 grep 扩
- **C24 内存转储与LSASS窃取**（5） 触发:内存转储 / LSASS窃取 ; credentials, conducting, pass → `conducting-pass-the-ticket-attack`, `active-directory-acl-abuse`, `mimikatz-credentials`, `mimipenguin-linux` ; 更多 1 个 grep 扩
- **C25 哈希与密码破解**（34） 触发:哈希 / 密码破解 ; wordlist, hash, brute → `performing-hash-cracking-with-hashcat`, `performing-gcp-penetration-testing-with-gcpbucketbrute`, `authbypass-authentication-flaws`, `bkcrack-zip-plaintext`, `john-hash-crack` ; 更多 29 个 grep 扩
- **C26 Kerberos与票据攻击**（8） 触发:Kerberos / 票据攻击 ; kerberos, kerberoasting, extracting → `extracting-credentials-from-memory-dump`, `exploiting-kerberoasting-with-impacket`, `performing-kerberoasting-attack`, `kekeo-kerberos`, `krbrelayx-kerberos-relay` ; 更多 3 个 grep 扩
- **C27 本地凭证与浏览器窃取**（4） 触发:本地凭证 / 浏览器窃取 ; credential, access, extracting → `extracting-browser-history-artifacts`, `performing-credential-access-with-lazagne`, `abusing-dpapi-for-credential-access` ; 更多 1 个 grep 扩
- **C28 暴力破解与口令喷射**（15） 触发:暴力破解 / 口令喷射 ; spray, brute, o365 → `barq-azure-ad`, `hydra-service-brute` ; 更多 13 个 grep 扩
- **C29 内网发现与枚举**（17） 触发:内网发现 / 枚举 ; ldap, smb, enum → `ad-ldap-enum-ldap`, `adidnsdump-ldap-enum` ; 更多 15 个 grep 扩
- **C30 AD域渗透与域控攻击**（50）〔二级子类→ref〕 触发:AD域渗透 / 域控攻击 ; active, directory, exploiting → `moving-laterally-with-netexec`, `exploiting-constrained-delegation-abuse`, `relaying-ntlm-for-adcs-esc8`, `aclpwn-acl-abuse`, `activedirectoryenum-ad`
- **C31 远程服务横向移动**（13） 触发:远程服务横向移动 ; lateral, movement, performing → `performing-lateral-movement-with-wmiexec`, `performing-lateral-movement-detection`, `exploiting-ms17-010-eternalblue-vulnerability`, `barmie-rmi-attack`, `impacket-protocol-exec` ; 更多 8 个 grep 扩
- **C32 隧道与内网穿透**（12） 触发:隧道 / 内网穿透 ; pivot, tunnel, trevorproxy → `stack-overflow-and-rop`, `tunneling-and-pivoting`, `frp-tunnel`, `chisel-tunnel` ; 更多 8 个 grep 扩
- **C33 数据收集与打包暂存**（4） 触发:数据收集 / 打包暂存 ; acquiring, disk, image → `acquiring-disk-image-with-dd-and-dcfldd`, `paramspider-param-harvest`, `tlsx-tls-enum` ; 更多 1 个 grep 扩
- **C34 屏幕与输入捕获**（3） 触发:屏幕 / 输入捕获 ; witnessme, web, shot → `offensive-keylogger-arch`, `scrying-multi-screenshot`, `witnessme-web-shot` ; 更多 0 个 grep 扩
- **C35 C2框架与远控**（21） 触发:C2框架 / 远控 ; performing, infrastructure, red → `performing-red-team-with-covenant`, `performing-privilege-escalation-on-linux`, `performing-automated-malware-analysis-with-cape`, `adaptix-c2-framework`, `emp3r0r-c2` ; 更多 16 个 grep 扩
- **C36 隐蔽回连与通信通道**（3） 触发:隐蔽回连 / 通信通道 ; icmpsh, reverse, websockify → `icmpsh-reverse`, `interactsh-oob` ; 更多 1 个 grep 扩
- **C37 数据外传**（2） 触发:数据外传 ; data, exfiltrator, dnsteal → `data-exfiltrator`, `dnsteal-dns-exfil` ; 更多 0 个 grep 扩
- **C38 隐写与隐藏通道**（4） 触发:隐写 / 隐藏通道 ; stego, zsteg, png → `cloakify-exfil`, `openstego-general-stego` ; 更多 2 个 grep 扩
- **C39 数据破坏与擦除**（3） 触发:数据破坏 / 擦除 ; performing, binary, exploitation → `performing-binary-exploitation-analysis`, `exploit-development`, `slowhttptest-dos` ; 更多 0 个 grep 扩
- **C40 嗅探与中间人攻击**（36） 触发:嗅探 / 中间人攻击 ; mitm, performing, network → `performing-arp-spoofing-attack-simulation`, `performing-network-packet-capture-analysis`, `performing-network-traffic-analysis-with-zeek`, `above-protocol-anomaly`, `arpspoof-smikims` ; 更多 31 个 grep 扩
- **C41 Web漏洞扫描与验证**（21） 触发:Web漏洞扫描 / 验证 ; performing, web, dir → `performing-container-security-scanning-with-trivy`, `performing-ssl-tls-security-assessment`, `nuclei-template-scan`, `gobuster-dir-dns`, `ffuf-web-fuzz` ; 更多 16 个 grep 扩
- **C42 网络扫描与枚举**（40） 触发:网络扫描 / 枚举 ; scan, network, sip → `scanning-network-with-nmap-advanced`, `building-vulnerability-scanning-workflow`, `offensive-bug-identification`, `angry-ip-scan`, `apachetomcatscanner-tomcat` ; 更多 35 个 grep 扩
- **C43 移动端攻击**（21） 触发:移动端攻击 ; android, mobile, app → `conducting-mobile-app-penetration-test`, `performing-dynamic-analysis-of-android-app`, `performing-android-app-static-analysis-with-mobsf`, `appmon-ios-android`, `bagbak-ios-decrypt` ; 更多 16 个 grep 扩
- **C44 AI与大模型安全**（12） 触发:AI / 大模型安全 ; threat, llm, attacks → `assessing-vector-and-embedding-weaknesses`, `testing-for-system-prompt-leakage`, `performing-threat-modeling-with-owasp-threat-dragon`, `hexstrike-ai`, `pentestagent-crewai` ; 更多 7 个 grep 扩
- **C45 恶意软件开发与免杀**（9） 触发:恶意软件开发 / 免杀 ; macro, dkmc, gen → `avet-av-evasion`, `bluffy-hollow` ; 更多 7 个 grep 扩
- **C46 二进制漏洞利用与Pwn**（46）〔二级子类→ref〕 触发:二进制漏洞利用 / Pwn ; offensive, exploitation, penetration → `performing-external-network-penetration-test`, `exploiting-smb-vulnerabilities-with-metasploit`, `exploiting-vulnerabilities-with-metasploit-framework`, `angrop-rop-gen`, `armscgen-shellcode`
- **C47 逆向工程**（4） 触发:逆向工程 ; sickle, shellcode, exe2hexbat → `open-redirect`, `exe2hexbat-payload-transfer`, `petools-pe-analysis` ; 更多 1 个 grep 扩
- **C48 区块链与Web3安全**（5） 触发:区块链 / Web3安全 ; security, slither, solidity → `smart-contract-security`, `solana-security`, `web3-security-tooling`, `slither-solidity-audit` ; 更多 1 个 grep 扩
- **C49 密码学攻击**（22） 触发:密码学攻击 ; crypto, rsa, tls → `lattice-crypto-attacks`, `symmetric-cipher-attacks`, `rsa-attack-techniques`, `a2sv-ssl-vuln`, `cero-tls-cert` ; 更多 17 个 grep 扩
- **C50 红队方法论与自动化**（38） 触发:红队方法论 / 自动化 ; team, offensive, engagement → `conducting-full-scope-red-team-engagement`, `designing-adversary-engagement-with-mitre-engage`, `performing-purple-team-atomic-testing`, `cloudfail-cloud-origin`, `engagement-discipline` ; 更多 33 个 grep 扩

## 附

- primary 总数：197（磁盘总量 996，二级子类见 reference.md，其余按需 grep，不主动加载）
- 维护：新增/删除 skill 后重跑 `python attack-skill-router/gen_router.py`（直扫仓库 + INDEX.md，无需 CSV）；类别内排名按「方法论仓库优先级 + 工具名字序」，FORCE_PRIMARY 名单见脚本
- 配套文件：reference.md（本脚本生成的展开层）、MERGES.md（重叠团合并裁决记录，已完成人工裁决 13 并 / 7 不并，非本脚本生成）
