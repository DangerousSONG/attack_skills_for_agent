# attack-skill-router — 完整路由表（50 类 · 每类全量 primary + 二级路由）

> 本文件由 gen_router.py 生成（展开层）。主表（每类一行 top5）在 SKILL.md；全库搜索：`grep -ril <关键词> /opt/attack-skill-library --include=SKILL.md`

### C01 资产测绘与指纹识别（62 个）

- 触发词：资产测绘 / 指纹识别 ｜ EN: recon, osint, performing, enum
- `collecting-open-source-intelligence`
- `performing-ai-driven-osint-correlation`
- `performing-asset-criticality-scoring-for-vulns`
- `alterx-dsl-subdomains`
- `amass-attack-surface`
- 二级路由（本类超过 40 个，按子标签细分）：
  - WAF 绕过（1 个）: `wafw00f-waf-detect`
  - 扫描/爬虫/综合（19 个）: `performing-asset-criticality-scoring-for-vulns`, `performing-timeline-reconstruction-with-plaso`, `identity-provider-recon` …
  - 其他（42 个）: `collecting-open-source-intelligence`, `performing-ai-driven-osint-correlation`, `performing-cloud-asset-inventory-with-cartography` …

### C02 域名与DNS侦察（19 个）

- 触发词：域名 / DNS侦察 ｜ EN: dns, subdomain, performing, enumeration
- `performing-dns-enumeration-and-zone-transfer`
- `performing-subdomain-enumeration-with-subfinder`
- `cors-cross-origin-misconfiguration`
- `aiodnsbrute-dns`
- `altdns-permutation`
- 更多 14 个: `grep -ril -e dns -e subdomain /opt/attack-skill-library --include=SKILL.md`

### C03 邮箱与人员OSINT（27 个）

- 触发词：邮箱 / 人员OSINT ｜ EN: osint, username, email, breach
- `profiling-threat-actor-groups`
- `bridgekeeper-username-mangle`
- `cr3dov3r-leak-lookup`
- 更多 24 个: `grep -ril -e osint -e username /opt/attack-skill-library --include=SKILL.md`

### C04 网络拓扑与互联网测绘（10 个）

- 触发词：网络拓扑 / 互联网测绘 ｜ EN: shodan, network, exploiting, bgp
- `exploiting-bgp-hijacking-vulnerabilities`
- `performing-ip-reputation-analysis-with-shodan`
- `ctf-osint`
- `asnmap-network-recon`
- `fav-up-favicon-lookup`
- 更多 5 个: `grep -ril -e shodan -e network /opt/attack-skill-library --include=SKILL.md`

### C05 外部攻击面与云资产暴露（31 个）

- 触发词：外部攻击面 / 云资产暴露 ｜ EN: exposure, offensive, cloud, scan
- `conducting-external-reconnaissance-with-osint`
- `enumerating-cloud-with-cloudfox`
- `exploiting-excessive-data-exposure-in-api`
- `apkleaks-endpoint-scan`
- `gh-dork-github`
- 更多 26 个: `grep -ril -e exposure -e offensive /opt/attack-skill-library --include=SKILL.md`

### C06 漏洞情报与漏洞库（14 个）

- 触发词：漏洞情报 / 漏洞库 ｜ EN: cve, exploiting, search, log4j
- `exploiting-nopac-cve-2021-42278-42287`
- `exploiting-zerologon-vulnerability-cve-2020-1472`
- `prototype-pollution`
- `exploitdb-search`
- `getsploit-exploit-search`
- 更多 9 个: `grep -ril -e cve -e exploiting /opt/attack-skill-library --include=SKILL.md`

### C07 载荷开发与武器化（24 个）

- 触发词：载荷开发 / 武器化 ｜ EN: shellcode, evasion, payload, conducting
- `conducting-spearphishing-simulation-campaign`
- `csv-formula-injection`
- `reverse-shell-techniques`
- `chankro-php-binary`
- `gadgettojscript-deser`
- 更多 19 个: `grep -ril -e shellcode -e evasion /opt/attack-skill-library --include=SKILL.md`

### C08 钓鱼与社会工程（25 个）

- 触发词：钓鱼 / 社会工程 ｜ EN: phishing, social, performing, phish
- `attacking-oauth-with-device-code-phishing`
- `conducting-phishing-incident-response`
- `conducting-social-engineering-penetration-test`
- `bad-pdf-phish`
- `credsniper-phish`
- 更多 20 个: `grep -ril -e phishing -e social /opt/attack-skill-library --include=SKILL.md`

### C09 Web应用漏洞利用（171 个）

- 触发词：Web应用漏洞利用 ｜ EN: offensive, exploiting, injection, performing
- `bypassing-authentication-with-forced-browsing`
- `escaping-containers-to-host`
- `exploiting-broken-function-level-authorization`
- `bbqsql-blind-sqlmap`
- `java-deserialization-gadget-selector`
- 二级路由（本类超过 40 个，按子标签细分）：
  - SQL/Nosql 注入（10 个）: `exploiting-nosql-injection-vulnerabilities`, `exploiting-sql-injection-vulnerabilities`, `exploiting-sql-injection-with-sqlmap` …
  - XSS（8 个）: `testing-for-xss-vulnerabilities`, `offensive-xss`, `traxss-xss` …
  - SSRF（9 个）: `performing-blind-ssrf-exploitation`, `performing-ssrf-vulnerability-exploitation`, `offensive-ssrf` …
  - 反序列化（4 个）: `exploiting-insecure-deserialization`, `offensive-deserialization`, `deserialization-insecure` …
  - 文件上传/包含（8 个）: `offensive-file-upload`, `path-traversal-lfi`, `fdsploit-lfi-rfi` …
  - 模板/命令注入（7 个）: `exploiting-template-injection-vulnerabilities`, `offensive-ssti`, `ssti-server-side-template-injection` …
  - 认证与授权(JWT/会话/越权)（9 个）: `bypassing-authentication-with-forced-browsing`, `exploiting-broken-function-level-authorization`, `performing-content-security-policy-bypass` …
  - 请求走私/缓存（8 个）: `performing-web-cache-deception-attack`, `performing-web-cache-poisoning-attack`, `offensive-request-smuggling` …
  - XXE/XML（6 个）: `testing-for-xml-injection-vulnerabilities`, `testing-for-xxe-injection-vulnerabilities`, `offensive-xxe` …
  - CORS/CSRF（6 个）: `performing-csrf-attack-simulation`, `csrf-cross-site-request-forgery`, `corscanner-cors-misconfig` …
  - 开放重定向（1 个）: `testing-for-open-redirect-vulnerabilities`
  - WAF 绕过（1 个）: `identywaf-fingerprint`
  - CMS 专项(WordPress/Joomla/Drupal等)（13 个）: `cmseek-cms-detect`, `cmsscan-multi-cms`, `cmsscanner-wp-lib` …
  - 扫描/爬虫/综合（24 个）: `exploiting-race-condition-vulnerabilities`, `exploiting-type-juggling-vulnerabilities`, `exploiting-websocket-vulnerabilities` …
  - 其他（57 个）: `escaping-containers-to-host`, `exploiting-mass-assignment-in-rest-apis`, `exploiting-prototype-pollution-in-javascript` …

### C10 API与业务逻辑攻击（54 个）

- 触发词：API / 业务逻辑攻击 ｜ EN: api, jwt, performing, graphql
- `conducting-api-security-testing`
- `exploiting-api-injection-vulnerabilities`
- `exploiting-idor-vulnerabilities`
- `astra-api-scan`
- `cariddi-crawler-secrets`
- 二级路由（本类超过 40 个，按子标签细分）：
  - 认证与授权(JWT/会话/越权)（23 个）: `exploiting-idor-vulnerabilities`, `exploiting-jwt-algorithm-confusion-attack`, `exploiting-oauth-misconfiguration` …
  - GraphQL（9 个）: `performing-graphql-depth-limit-attack`, `performing-graphql-introspection-attack`, `performing-graphql-security-assessment` …
  - 扫描/爬虫/综合（12 个）: `exploiting-api-injection-vulnerabilities`, `performing-api-fuzzing-with-restler`, `performing-osint-with-spiderfoot` …
  - 其他（10 个）: `conducting-api-security-testing`, `performing-api-inventory-and-discovery`, `performing-api-security-testing-with-postman` …

### C11 边界设备与VPN攻击（4 个）

- 触发词：边界设备 / VPN攻击 ｜ EN: offensive, anti, forensics, scada
- `offensive-anti-forensics`
- `scada-attacker`
- `cameradar-rtsp`
- `sigploit-telecom`
- 更多 0 个: `grep -ril -e offensive -e anti /opt/attack-skill-library --include=SKILL.md`

### C12 供应链与CI/CD攻击（16 个）

- 触发词：供应链 / CI/CD攻击 ｜ EN: cicd, offensive, dependency, supply
- `continuous-llm-red-teaming-with-promptfoo`
- `defending-llms-with-guardrails`
- `implementing-fuzz-testing-in-cicd-with-aflplusplus`
- `dvcs-ripper-vcs`
- `git-dumper-repo`
- 更多 11 个: `grep -ril -e cicd -e offensive /opt/attack-skill-library --include=SKILL.md`

### C13 远程命令执行与WebShell（8 个）

- 触发词：远程命令执行 / WebShell ｜ EN: shell, manager, htshells, htaccess
- `htshells-htaccess`
- `novahot-web-shell`
- 更多 6 个: `grep -ril -e shell -e manager /opt/attack-skill-library --include=SKILL.md`

### C14 云与容器执行（3 个）

- 触发词：云 / 容器执行 ｜ EN: container, escape, botb, deepce
- `botb-container-attack`
- `deepce-container-escape`
- 更多 1 个: `grep -ril -e container -e escape /opt/attack-skill-library --include=SKILL.md`

### C15 持久化与后门植入（13 个）

- 触发词：持久化 / 后门植入 ｜ EN: persistence, shell, conducting, domain
- `conducting-domain-persistence-with-dcsync`
- `operating-sliver-c2`
- `performing-malware-persistence-investigation`
- `dbd-dns-tunnel-shell`
- `gcat-gmail-c2`
- 更多 8 个: `grep -ril -e persistence -e shell /opt/attack-skill-library --include=SKILL.md`

### C16 Linux本地提权（8 个）

- 触发词：Linux本地提权 ｜ EN: privesc, linux, escape, privilege
- `linux-privilege-escalation`
- `sandbox-escape-techniques`
- `privesc-advisor`
- `linenum-privesc-scan`
- `suid3num-privesc`
- 更多 3 个: `grep -ril -e privesc -e linux /opt/attack-skill-library --include=SKILL.md`

### C17 Windows本地提权（11 个）

- 触发词：Windows本地提权 ｜ EN: windows, privesc, offensive, k8s
- `defi-attack-patterns`
- `windows-privilege-escalation`
- `offensive-k8s-attacks`
- `beroot-privesc-check`
- `powershdll-nopowershell`
- 更多 6 个: `grep -ril -e windows -e privesc /opt/attack-skill-library --include=SKILL.md`

### C18 云与容器提权（14 个）

- 触发词：云 / 容器提权 ｜ EN: performing, kubernetes, privilege, escalation
- `auditing-kubernetes-rbac-privilege-escalation`
- `performing-agentless-vulnerability-scanning`
- `performing-aws-account-enumeration-with-scout-suite`
- `cloudlist-multi-cloud`
- `microburst-azure`
- 更多 9 个: `grep -ril -e performing -e kubernetes /opt/attack-skill-library --include=SKILL.md`

### C19 EDR与AV规避（4 个）

- 触发词：EDR / AV规避 ｜ EN: evasion, operating, havoc, offensive
- `operating-havoc-c2`
- `offensive-edr-evasion`
- `evasion-specialist`
- 更多 1 个: `grep -ril -e evasion -e operating /opt/attack-skill-library --include=SKILL.md`

### C20 反取证与痕迹清理（4 个）

- 触发词：反取证 / 痕迹清理 ｜ EN: anti, forensic, mat, metadata
- `mat-metadata-clean`
- `moonwalk-anti-forensic`
- 更多 2 个: `grep -ril -e anti -e forensic /opt/attack-skill-library --include=SKILL.md`

### C21 流量混淆与加密隧道（1 个）

- 触发词：流量混淆 / 加密隧道 ｜ EN: offensive, data, exfiltration
- `offensive-data-exfiltration`
- 更多 0 个: `grep -ril -e offensive -e data /opt/attack-skill-library --include=SKILL.md`

### C22 进程注入与内存执行（19 个）

- 触发词：进程注入 / 内存执行 ｜ EN: injection, header, llm, redteam
- `performing-packet-injection-attack`
- `red-teaming-llms-with-garak`
- `testing-for-email-header-injection`
- `amber-reflective-packer`
- 更多 15 个: `grep -ril -e injection -e header /opt/attack-skill-library --include=SKILL.md`

### C23 无文件与LOLBins滥用（2 个）

- 触发词：无文件 / LOLBins滥用 ｜ EN: lolbas, living, off, land
- `lolbas-living-off-land`
- `m3-gen-msbuild`
- 更多 0 个: `grep -ril -e lolbas -e living /opt/attack-skill-library --include=SKILL.md`

### C24 内存转储与LSASS窃取（5 个）

- 触发词：内存转储 / LSASS窃取 ｜ EN: credentials, conducting, pass, ticket
- `conducting-pass-the-ticket-attack`
- `active-directory-acl-abuse`
- `mimikatz-credentials`
- `mimipenguin-linux`
- 更多 1 个: `grep -ril -e credentials -e conducting /opt/attack-skill-library --include=SKILL.md`

### C25 哈希与密码破解（34 个）

- 触发词：哈希 / 密码破解 ｜ EN: wordlist, hash, brute, mask
- `performing-gcp-penetration-testing-with-gcpbucketbrute`
- `performing-hash-cracking-with-hashcat`
- `authbypass-authentication-flaws`
- `bkcrack-zip-plaintext`
- `john-hash-crack`
- 更多 29 个: `grep -ril -e wordlist -e hash /opt/attack-skill-library --include=SKILL.md`

### C26 Kerberos与票据攻击（8 个）

- 触发词：Kerberos / 票据攻击 ｜ EN: kerberos, kerberoasting, exploiting, impacket
- `exploiting-kerberoasting-with-impacket`
- `extracting-credentials-from-memory-dump`
- `performing-kerberoasting-attack`
- `kekeo-kerberos`
- `krbrelayx-kerberos-relay`
- 更多 3 个: `grep -ril -e kerberos -e kerberoasting /opt/attack-skill-library --include=SKILL.md`

### C27 本地凭证与浏览器窃取（4 个）

- 触发词：本地凭证 / 浏览器窃取 ｜ EN: credential, access, abusing, dpapi
- `abusing-dpapi-for-credential-access`
- `extracting-browser-history-artifacts`
- `performing-credential-access-with-lazagne`
- 更多 1 个: `grep -ril -e credential -e access /opt/attack-skill-library --include=SKILL.md`

### C28 暴力破解与口令喷射（15 个）

- 触发词：暴力破解 / 口令喷射 ｜ EN: spray, brute, o365, login
- `barq-azure-ad`
- `hydra-service-brute`
- 更多 13 个: `grep -ril -e spray -e brute /opt/attack-skill-library --include=SKILL.md`

### C29 内网发现与枚举（17 个）

- 触发词：内网发现 / 枚举 ｜ EN: ldap, enum, smb, windapsearch
- `ad-ldap-enum-ldap`
- `adidnsdump-ldap-enum`
- 更多 15 个: `grep -ril -e ldap -e enum /opt/attack-skill-library --include=SKILL.md`

### C30 AD域渗透与域控攻击（50 个）

- 触发词：AD域渗透 / 域控攻击 ｜ EN: active, directory, bloodhound, exploiting
- `abusing-shadow-credentials-for-privesc`
- `attacking-entra-id-with-roadtools`
- `conducting-internal-network-penetration-test`
- `aclpwn-acl-abuse`
- `activedirectoryenum-ad`
- 二级路由（本类超过 40 个，按子标签细分）：
  - 扫描/爬虫/综合（5 个）: `conducting-internal-reconnaissance-with-bloodhound-ce`, `performing-active-directory-vulnerability-assessment`, `smart-contract-vulnerabilities` …
  - 其他（45 个）: `abusing-shadow-credentials-for-privesc`, `attacking-entra-id-with-roadtools`, `conducting-internal-network-penetration-test` …

### C31 远程服务横向移动（13 个）

- 触发词：远程服务横向移动 ｜ EN: lateral, movement, performing, windows
- `exploiting-ms17-010-eternalblue-vulnerability`
- `performing-lateral-movement-detection`
- `performing-lateral-movement-with-wmiexec`
- `barmie-rmi-attack`
- `impacket-protocol-exec`
- 更多 8 个: `grep -ril -e lateral -e movement /opt/attack-skill-library --include=SKILL.md`

### C32 隧道与内网穿透（12 个）

- 触发词：隧道 / 内网穿透 ｜ EN: pivot, tunnel, stack, overflow
- `stack-overflow-and-rop`
- `tunneling-and-pivoting`
- `frp-tunnel`
- `chisel-tunnel`
- 更多 8 个: `grep -ril -e pivot -e tunnel /opt/attack-skill-library --include=SKILL.md`

### C33 数据收集与打包暂存（4 个）

- 触发词：数据收集 / 打包暂存 ｜ EN: acquiring, disk, image, dcfldd
- `acquiring-disk-image-with-dd-and-dcfldd`
- `paramspider-param-harvest`
- `tlsx-tls-enum`
- 更多 1 个: `grep -ril -e acquiring -e disk /opt/attack-skill-library --include=SKILL.md`

### C34 屏幕与输入捕获（3 个）

- 触发词：屏幕 / 输入捕获 ｜ EN: offensive, keylogger, arch, scrying
- `offensive-keylogger-arch`
- `scrying-multi-screenshot`
- `witnessme-web-shot`
- 更多 0 个: `grep -ril -e offensive -e keylogger /opt/attack-skill-library --include=SKILL.md`

### C35 C2框架与远控（21 个）

- 触发词：C2框架 / 远控 ｜ EN: performing, infrastructure, building, red
- `building-c2-redirector-infrastructure`
- `building-red-team-c2-infrastructure-with-havoc`
- `exploiting-aws-with-pacu`
- `adaptix-c2-framework`
- `emp3r0r-c2`
- 更多 16 个: `grep -ril -e performing -e infrastructure /opt/attack-skill-library --include=SKILL.md`

### C36 隐蔽回连与通信通道（3 个）

- 触发词：隐蔽回连 / 通信通道 ｜ EN: icmpsh, reverse, interactsh, oob
- `icmpsh-reverse`
- `interactsh-oob`
- 更多 1 个: `grep -ril -e icmpsh -e reverse /opt/attack-skill-library --include=SKILL.md`

### C37 数据外传（2 个）

- 触发词：数据外传 ｜ EN: data, exfiltrator, dnsteal, dns
- `data-exfiltrator`
- `dnsteal-dns-exfil`
- 更多 0 个: `grep -ril -e data -e exfiltrator /opt/attack-skill-library --include=SKILL.md`

### C38 隐写与隐藏通道（4 个）

- 触发词：隐写 / 隐藏通道 ｜ EN: stego, cloakify, exfil, openstego
- `cloakify-exfil`
- `openstego-general-stego`
- 更多 2 个: `grep -ril -e stego -e cloakify /opt/attack-skill-library --include=SKILL.md`

### C39 数据破坏与擦除（3 个）

- 触发词：数据破坏 / 擦除 ｜ EN: performing, binary, exploitation, analysis
- `performing-binary-exploitation-analysis`
- `exploit-development`
- `slowhttptest-dos`
- 更多 0 个: `grep -ril -e performing -e binary /opt/attack-skill-library --include=SKILL.md`

### C40 嗅探与中间人攻击（36 个）

- 触发词：嗅探 / 中间人攻击 ｜ EN: mitm, performing, network, simulation
- `conducting-man-in-the-middle-attack-simulation`
- `performing-arp-spoofing-attack-simulation`
- `performing-bandwidth-throttling-attack-simulation`
- `above-protocol-anomaly`
- `arpspoof-smikims`
- 更多 31 个: `grep -ril -e mitm -e performing /opt/attack-skill-library --include=SKILL.md`

### C41 Web漏洞扫描与验证（21 个）

- 触发词：Web漏洞扫描 / 验证 ｜ EN: performing, web, dir, scanning
- `performing-container-security-scanning-with-trivy`
- `performing-ssl-tls-security-assessment`
- `ffuf-web-fuzz`
- `nuclei-template-scan`
- `gobuster-dir-dns`
- 更多 16 个: `grep -ril -e performing -e web /opt/attack-skill-library --include=SKILL.md`

### C42 网络扫描与枚举（40 个）

- 触发词：网络扫描 / 枚举 ｜ EN: scan, network, offensive, sip
- `building-vulnerability-scanning-workflow`
- `scanning-network-with-nmap-advanced`
- `offensive-bug-identification`
- `angry-ip-scan`
- `apachetomcatscanner-tomcat`
- 更多 35 个: `grep -ril -e scan -e network /opt/attack-skill-library --include=SKILL.md`

### C43 移动端攻击（21 个）

- 触发词：移动端攻击 ｜ EN: android, mobile, app, performing
- `conducting-mobile-app-penetration-test`
- `exploiting-deeplink-vulnerabilities`
- `exploiting-insecure-data-storage-in-mobile`
- `appmon-ios-android`
- `bagbak-ios-decrypt`
- 更多 16 个: `grep -ril -e android -e mobile /opt/attack-skill-library --include=SKILL.md`

### C44 AI与大模型安全（12 个）

- 触发词：AI / 大模型安全 ｜ EN: llm, attacks, threat, security
- `assessing-vector-and-embedding-weaknesses`
- `orchestrating-llm-attacks-with-pyrit`
- `performing-threat-modeling-with-owasp-threat-dragon`
- `hexstrike-ai`
- `pentestagent-crewai`
- 更多 7 个: `grep -ril -e llm -e attacks /opt/attack-skill-library --include=SKILL.md`

### C45 恶意软件开发与免杀（9 个）

- 触发词：恶意软件开发 / 免杀 ｜ EN: macro, avet, evasion, bluffy
- `avet-av-evasion`
- `bluffy-hollow`
- 更多 7 个: `grep -ril -e macro -e avet /opt/attack-skill-library --include=SKILL.md`

### C46 二进制漏洞利用与Pwn（46 个）

- 触发词：二进制漏洞利用 / Pwn ｜ EN: offensive, exploitation, penetration, ctf
- `coercing-authentication-with-coercer-petitpotam`
- `conducting-cloud-penetration-testing`
- `conducting-network-penetration-test`
- `angrop-rop-gen`
- `armscgen-shellcode`
- 二级路由（本类超过 40 个，按子标签细分）：
  - 认证与授权(JWT/会话/越权)（1 个）: `coercing-authentication-with-coercer-petitpotam`
  - 扫描/爬虫/综合（12 个）: `exploiting-ipv6-vulnerabilities`, `exploiting-smb-vulnerabilities-with-metasploit`, `exploiting-vulnerabilities-with-metasploit-framework` …
  - 其他（33 个）: `conducting-cloud-penetration-testing`, `conducting-network-penetration-test`, `performing-cloud-penetration-testing-with-pacu` …

### C47 逆向工程（4 个）

- 触发词：逆向工程 ｜ EN: open, redirect, exe2hexbat, payload
- `open-redirect`
- `exe2hexbat-payload-transfer`
- `petools-pe-analysis`
- 更多 1 个: `grep -ril -e open -e redirect /opt/attack-skill-library --include=SKILL.md`

### C48 区块链与Web3安全（5 个）

- 触发词：区块链 / Web3安全 ｜ EN: security, mev, smart, contract
- `mev-security`
- `smart-contract-security`
- `solana-security`
- `slither-solidity-audit`
- 更多 1 个: `grep -ril -e security -e mev /opt/attack-skill-library --include=SKILL.md`

### C49 密码学攻击（22 个）

- 触发词：密码学攻击 ｜ EN: crypto, attacks, rsa, tls
- `classical-cipher-analysis`
- `lattice-crypto-attacks`
- `rsa-attack-techniques`
- `a2sv-ssl-vuln`
- `cero-tls-cert`
- 更多 17 个: `grep -ril -e crypto -e attacks /opt/attack-skill-library --include=SKILL.md`

### C50 红队方法论与自动化（38 个）

- 触发词：红队方法论 / 自动化 ｜ EN: team, offensive, engagement, red
- `conducting-full-scope-red-team-engagement`
- `designing-adversary-engagement-with-mitre-engage`
- `emulating-cloud-attacks-with-stratus-red-team`
- `cloudfail-cloud-origin`
- `engagement-discipline`
- 更多 33 个: `grep -ril -e team -e offensive /opt/attack-skill-library --include=SKILL.md`
