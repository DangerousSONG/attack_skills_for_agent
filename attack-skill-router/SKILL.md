---
name: attack-skill-router
description: "Attack-side skill library routing layer (996 pentest skills) exposing a search_skills semantic-retrieval HTTP API served by a resident host process, a same-named local CLI fallback, and a 50-category static routing table as last resort. Signals: skill routing, semantic skill search, penetration testing, CVE, reconnaissance, exploitation, privilege escalation, lateral movement, persistence, evasion, C2."
zh-signals: "攻击侧 Skill 库（996 个渗透测试 skill）的路由层。提供 search_skills 语义检索 HTTP API（curl 调用宿主常驻服务，默认带 L3 cross-encoder 精排，约 1.4s 返回 top-k 候选与可直接 Read 的绝对路径，容器内无需挂载 venv/模型权重）、同名本地 CLI 兜底，以及 50 类静态路由表（前两者都不可用时兜底）。任务涉及侦察、漏洞利用、提权、横向移动、持久化、免杀、C2 等任一渗透环节时先加载本 skill，用它定位该读的 1-3 个 SKILL.md；不要在近千个 SKILL.md 里盲目 grep 全读。"
when-to-use: "At the start of a pentest engagement; when an already-loaded skill no longer resolves the current obstacle and you need to re-route; whenever the user names a concrete service / tool / technique / CVE id (e.g. unauthenticated Redis, sqlmap, Java deserialization, domain lateral movement, UAC bypass, CVE-xxxx-xxxx)."
---

# Attack Skill Router (v2.2)

> ## GLOBAL RULE - how a library skill gets loaded (applies to routing path A, B and every fallback)
>
> The **Skill tool works for exactly 3 registered skills**: `attack-skill-router`, `engagement-discipline`, `java-deserialization-gadget-selector`. **All the other 994 library skills are plain markdown files, NOT registered Claude Code skills** - the only way to load one is to open its absolute path with the **Read** tool (`candidates[].path` from path A, or the Glob-resolved path from path B) and follow it yourself.
> Calling `Skill(<library slug>)` always returns `Unknown skill`: it wastes a turn and silently breaks the routing chain, so never treat a `slug` from this router as a skill name.

## Purpose

This library holds 996 skills across 50 attack categories. Searching the whole library directly confronts the Agent with too many homogeneous options (measured: one deserialization query pulled in 3 overlapping skills at once).
**This routing layer compresses "pick N out of 996" into "pick 1 of 50 categories → pick 1-3 of that category's 3-5 primaries"**, and also exposes a semantic routing API that returns top-k candidates directly (about 1.4s per curl, since L3 reranking is on by default).

## Direct invocation (`/attack-skill-router`)

The user can trigger this skill explicitly with `/attack-skill-router <one-sentence task description>`. The arguments passed to this invocation are:

> $ARGUMENTS

- **Arguments non-empty** → use them as-is as the query and run "Routing path A - standard call" below;
- **Arguments empty** (or this skill was auto-loaded) → first distill a "task + signal words" query yourself from the current conversation context (see the table in section A), then run the same steps. Never pick a skill from memory without having run a routing query first.

## Routing path A: search_skills HTTP API (must - try this first)

Three-stage funnel semantic routing (L1 embedding top-k coarse filter → L2 RRF fused ranking [cosine rank + TF-IDF rank] → L3 cross-encoder rerank). L3 runs **by default** - you get the reranked ordering without asking for it. It covers the whole library and is not limited by the 50-category granularity of the static table below.


### Step 0: confirm the service is alive (run once at the start of a task, not before every query)

```bash
curl -sf --max-time 2 "${ROUTER_API:-http://10.22.16.51:8787}/health"
```

- Reachable → returns silently; go straight to the standard call;
- `/health` only reports corpus size / uptime / whether L3 is loaded / the `rerank` default. It does not leak library contents.

### Standard call (copy this verbatim, do not rewrite it)

```bash
curl -sS --max-time 30 -G "${ROUTER_API:-http://10.22.16.51:8787}/search" \
  --data-urlencode 'query=<one-sentence task description>' \
  --data-urlencode top_k=5 --data-urlencode desc_chars=120
```

- **The command must start with `curl`** (`allowed-tools` pre-approval matches by prefix; prefixing an environment-variable assignment breaks it);
- Pass `query` via `--data-urlencode` - English, spaces and quotes all need no escaping on your side;
- `top_k=5 desc_chars=120` is the standard configuration chosen to control context tokens; the response body is about 800 tokens;
- Do **not** add `rerank=1` - it is already the default. Add `--data-urlencode rerank=0` only if you are batch-screening many queries and can accept a visibly worse head of the list (~0.1s instead of ~1.4s);
- The result JSON goes to stdout and can be parsed directly; **`candidates[].path` is an absolute path inside the deployed skill library** - just open it with Read, no need to prepend the repo root;

### Agent execution sequence

1. Run step 0 to confirm the service;
2. Write the current obstacle as a one-sentence "task + signal words" query in English and run the standard call;
3. Read the JSON and pick **1-3** `slug`s out of `candidates`. Judge by whether the `description` matches the current service / version / tech stack, **not by the absolute value of `score`**;
4. Open the corresponding `path` with Read and follow that skill's steps. **The Skill tool is only valid for the 3 registered skills listed in the GLOBAL RULE at the top - every library skill must be loaded as `Read <path>`, never as `Skill(<slug>)`. Do not read all 5, and do not grep the whole library again**;
5. If none of the top-5 is relevant, escalate in this order, trying each step only once:
   - (1) Rewrite the query, adding the service name / version number / error keywords / current privilege state → re-run the standard call;
   - (2) Fall back to routing path B (static table);
6. List the slugs actually loaded at the end of the final report.

**~1.4s per query, but a task usually still needs only 1-2 queries**: querying more does not make the answer more accurate, it just keeps loading homogeneous candidates into the context.

### How to write the query

| Good (task + signal words) | Bad |
|---|---|
| `Unauthenticated Redis instance exposed on the network, gain code execution via the database` | `redis` |
| `Credentials for domain users have been obtained from the target DC; planning lateral movement to other hosts within the intranet` | `横向` |
| `Java deserialization vulnerability on WebLogic 10.3.6; need to craft a gadget chain` | `deserialization` |
| `SQL injection in the login form, verify with an automated tool and dump the DB` | `exploiting-sql-injection-with-sqlmap` (a slug is not a query) |

**The key is to write out every retrievable signal word**: service name + version, vulnerability type, the privileges/credentials you already hold, and the action you want to achieve.

### Response body

```json
{"query": "...",
 "candidates": [{"slug": "database-attacker", "name": "...",
                 "description": "...", "path": "/opt/attack-skill-library/database-attacker/SKILL.md",
                 "score": 0.5484, "l1_sim": 0.575, "rerank_score": 0.5484,
                 "load": "Read the \"path\" field above. This is NOT a registered Claude skill - the Skill tool only knows attack-skill-router / engagement-discipline / java-deserialization-gadget-selector"}],
 "meta": {"l1_kept": 50, "n_skills": 994, "l1_topk": 50, "rrf_k0": 60,
          "emb_model": "BAAI/bge-m3", "rerank": true, "degraded": false,
          "ready_ms": 5206, "latency_ms": {"l1": 72, "l2": 8, "l3": 1347, "total": 1427},
          "consume": "Load each candidate with the Read tool on its absolute \"path\" field. Only attack-skill-router / engagement-discipline / java-deserialization-gadget-selector are registered skills; every other library skill is a plain file, so Skill(<slug>) returns \"Unknown skill\"."}}
```

The directory prefix of `path` is whatever the deployment configured (`--lib-prefix`, default `/opt/attack-skill-library`); it is always absolute, so Read it verbatim. `load` / `meta.consume` restate the GLOBAL RULE inside the data itself - obey them: a `slug` is a retrieval key for reporting, never a Skill-tool argument.

`score` is the ranking criterion of the current stage. With the default `rerank: true` it equals `rerank_score`, the cross-encoder score in 0-1 - and it **does** discriminate: measured top1 0.5484 vs top2 0.0165 for an unauthenticated-Redis query, so a large gap between #1 and #2 is a real signal that #1 is the right skill. With `rerank=0` it is instead the RRF fused score (magnitude ~0.03, and the top candidates come out nearly tied - **use it only for relative ordering; the absolute value is meaningless, do not treat it as a similarity threshold**). `l1_sim` is always the cosine similarity. `ready_ms` is the one-off loading time at service startup (not counted in this query); `latency_ms.total` is this query's own latency (including concurrent queueing), ~1.4s of which is L3 on CPU. `n_skills=994` is the retrieval-corpus figure (996 on disk minus the registered skills such as this routing layer), consistent with the evaluation harness.

On error the response is `{"error": {"code": 4xx/5xx, "message": "...", "hint": "..."}}` - fix the parameters according to `message`, no guessing needed.



## Routing path B: static routing table (when the CLI is unavailable, execute in order)

1. **Locate the category**: use the "Routing table" below to match a row by service type / vulnerability class / technique keyword / CVE;
2. **Pick a primary**: among that row's 3-5 slugs, choose the 1-3 best fits by their frontmatter `when-to-use`;
3. **slug → path**: the static table gives slugs but not paths, so resolve them with Glob (one call can take multiple patterns): `/opt/attack-skill-library/**/<slug>/SKILL.md` - if that root does not exist on this machine, use the directory a previous path-A `candidates[].path` pointed into - then open with Read. Per the GLOBAL RULE at the top these are plain files: **Read them, never `Skill(<slug>)`**;
4. **Expand if that is not enough**: for categories marked `[sub-cats → ref]` (many skills in that category), open `reference.md` (next to this SKILL.md, in the registered skill directory - it is **not** under `/opt/attack-skill-library`) and narrow down by sub-tag; for the rest use the Grep tool (`path` set to `/opt/attack-skill-library`, `-i` on) to search targeted keywords - do not read through the whole library;
5. **Report**: list the slugs actually loaded at the end of the final report (consistent with the evaluation workflow).

Note: the 50 category names and their trigger words below stay Chinese on purpose - they are data derived from the Chinese `INDEX.md` (the classification authority) and they are the Chinese matching surface of routing path B.

## Selection rules (common to A and B)

- **Methodology over tooling**: prefer methodology skills (they teach you the exploitation chain); tool-wrapper skills (a manual for one tool) fill in when the methodology lacks concrete commands;
- **Load only one skill per topic**: same-topic entries are already deduplicated inside the routing table (see `MERGES.md`, next to this SKILL.md; human adjudication complete, 13 merged / 7 not merged). If the CLI or grep still returns several similar slugs, pick the one whose frontmatter `when-to-use` best fits the current service/version;
- **Version-sensitive tasks** (Java deserialization gadgets, kernel exploits, etc.): a methodology skill can only give you the approach; gadget adaptation is exploit engineering - build it yourself from the skill's guidance plus the target version, and do not keep retrying the library's stale gadgets.

## Routing table (50 categories, 5 primaries each, one line per category)

- **C01 资产测绘与指纹识别** (62) [sub-cats → ref] triggers: 资产测绘 / 指纹识别 ; recon, osint, performing → `collecting-open-source-intelligence`, `performing-ai-driven-osint-correlation`, `performing-asset-criticality-scoring-for-vulns`, `alterx-dsl-subdomains`, `amass-attack-surface`
- **C02 域名与DNS侦察** (19) triggers: 域名 / DNS侦察 ; dns, subdomain, performing → `performing-dns-enumeration-and-zone-transfer`, `performing-subdomain-enumeration-with-subfinder`, `cors-cross-origin-misconfiguration`, `aiodnsbrute-dns`, `altdns-permutation` ; 14 more, grep to expand
- **C03 邮箱与人员OSINT** (27) triggers: 邮箱 / 人员OSINT ; osint, username, email → `profiling-threat-actor-groups`, `bridgekeeper-username-mangle`, `cr3dov3r-leak-lookup` ; 24 more, grep to expand
- **C04 网络拓扑与互联网测绘** (10) triggers: 网络拓扑 / 互联网测绘 ; shodan, network, exploiting → `exploiting-bgp-hijacking-vulnerabilities`, `performing-ip-reputation-analysis-with-shodan`, `ctf-osint`, `asnmap-network-recon`, `fav-up-favicon-lookup` ; 5 more, grep to expand
- **C05 外部攻击面与云资产暴露** (31) triggers: 外部攻击面 / 云资产暴露 ; exposure, offensive, cloud → `conducting-external-reconnaissance-with-osint`, `enumerating-cloud-with-cloudfox`, `exploiting-excessive-data-exposure-in-api`, `apkleaks-endpoint-scan`, `gh-dork-github` ; 26 more, grep to expand
- **C06 漏洞情报与漏洞库** (14) triggers: 漏洞情报 / 漏洞库 ; cve, exploiting, search → `exploiting-nopac-cve-2021-42278-42287`, `exploiting-zerologon-vulnerability-cve-2020-1472`, `prototype-pollution`, `exploitdb-search`, `getsploit-exploit-search` ; 9 more, grep to expand
- **C07 载荷开发与武器化** (24) triggers: 载荷开发 / 武器化 ; shellcode, evasion, payload → `conducting-spearphishing-simulation-campaign`, `csv-formula-injection`, `reverse-shell-techniques`, `chankro-php-binary`, `gadgettojscript-deser` ; 19 more, grep to expand
- **C08 钓鱼与社会工程** (25) triggers: 钓鱼 / 社会工程 ; phishing, social, performing → `attacking-oauth-with-device-code-phishing`, `conducting-phishing-incident-response`, `conducting-social-engineering-penetration-test`, `bad-pdf-phish`, `credsniper-phish` ; 20 more, grep to expand
- **C09 Web应用漏洞利用** (171) [sub-cats → ref] triggers: Web应用漏洞利用 ; offensive, exploiting, injection → `bypassing-authentication-with-forced-browsing`, `escaping-containers-to-host`, `exploiting-broken-function-level-authorization`, `bbqsql-blind-sqlmap`, `java-deserialization-gadget-selector`
- **C10 API与业务逻辑攻击** (54) [sub-cats → ref] triggers: API / 业务逻辑攻击 ; api, jwt, performing → `conducting-api-security-testing`, `exploiting-api-injection-vulnerabilities`, `exploiting-idor-vulnerabilities`, `astra-api-scan`, `cariddi-crawler-secrets`
- **C11 边界设备与VPN攻击** (4) triggers: 边界设备 / VPN攻击 ; offensive, anti, forensics → `offensive-anti-forensics`, `scada-attacker`, `cameradar-rtsp`, `sigploit-telecom` ; 0 more, grep to expand
- **C12 供应链与CI/CD攻击** (16) triggers: 供应链 / CI/CD攻击 ; cicd, offensive, dependency → `continuous-llm-red-teaming-with-promptfoo`, `defending-llms-with-guardrails`, `implementing-fuzz-testing-in-cicd-with-aflplusplus`, `dvcs-ripper-vcs`, `git-dumper-repo` ; 11 more, grep to expand
- **C13 远程命令执行与WebShell** (8) triggers: 远程命令执行 / WebShell ; shell, manager, htshells → `htshells-htaccess`, `novahot-web-shell` ; 6 more, grep to expand
- **C14 云与容器执行** (3) triggers: 云 / 容器执行 ; container, escape, botb → `botb-container-attack`, `deepce-container-escape` ; 1 more, grep to expand
- **C15 持久化与后门植入** (13) triggers: 持久化 / 后门植入 ; persistence, shell, conducting → `conducting-domain-persistence-with-dcsync`, `operating-sliver-c2`, `performing-malware-persistence-investigation`, `dbd-dns-tunnel-shell`, `gcat-gmail-c2` ; 8 more, grep to expand
- **C16 Linux本地提权** (8) triggers: Linux本地提权 ; privesc, linux, escape → `linux-privilege-escalation`, `sandbox-escape-techniques`, `privesc-advisor`, `linenum-privesc-scan`, `suid3num-privesc` ; 3 more, grep to expand
- **C17 Windows本地提权** (11) triggers: Windows本地提权 ; windows, privesc, offensive → `defi-attack-patterns`, `windows-privilege-escalation`, `offensive-k8s-attacks`, `beroot-privesc-check`, `powershdll-nopowershell` ; 6 more, grep to expand
- **C18 云与容器提权** (14) triggers: 云 / 容器提权 ; performing, kubernetes, privilege → `auditing-kubernetes-rbac-privilege-escalation`, `performing-agentless-vulnerability-scanning`, `performing-aws-account-enumeration-with-scout-suite`, `cloudlist-multi-cloud`, `microburst-azure` ; 9 more, grep to expand
- **C19 EDR与AV规避** (4) triggers: EDR / AV规避 ; evasion, operating, havoc → `operating-havoc-c2`, `offensive-edr-evasion`, `evasion-specialist` ; 1 more, grep to expand
- **C20 反取证与痕迹清理** (4) triggers: 反取证 / 痕迹清理 ; anti, forensic, mat → `mat-metadata-clean`, `moonwalk-anti-forensic` ; 2 more, grep to expand
- **C21 流量混淆与加密隧道** (1) triggers: 流量混淆 / 加密隧道 ; offensive, data, exfiltration → `offensive-data-exfiltration` ; 0 more, grep to expand
- **C22 进程注入与内存执行** (19) triggers: 进程注入 / 内存执行 ; injection, header, llm → `performing-packet-injection-attack`, `red-teaming-llms-with-garak`, `testing-for-email-header-injection`, `amber-reflective-packer` ; 15 more, grep to expand
- **C23 无文件与LOLBins滥用** (2) triggers: 无文件 / LOLBins滥用 ; lolbas, living, off → `lolbas-living-off-land`, `m3-gen-msbuild` ; 0 more, grep to expand
- **C24 内存转储与LSASS窃取** (5) triggers: 内存转储 / LSASS窃取 ; credentials, conducting, pass → `conducting-pass-the-ticket-attack`, `active-directory-acl-abuse`, `mimikatz-credentials`, `mimipenguin-linux` ; 1 more, grep to expand
- **C25 哈希与密码破解** (34) triggers: 哈希 / 密码破解 ; wordlist, hash, brute → `performing-gcp-penetration-testing-with-gcpbucketbrute`, `performing-hash-cracking-with-hashcat`, `authbypass-authentication-flaws`, `bkcrack-zip-plaintext`, `john-hash-crack` ; 29 more, grep to expand
- **C26 Kerberos与票据攻击** (8) triggers: Kerberos / 票据攻击 ; kerberos, kerberoasting, exploiting → `exploiting-kerberoasting-with-impacket`, `extracting-credentials-from-memory-dump`, `performing-kerberoasting-attack`, `kekeo-kerberos`, `krbrelayx-kerberos-relay` ; 3 more, grep to expand
- **C27 本地凭证与浏览器窃取** (4) triggers: 本地凭证 / 浏览器窃取 ; credential, access, abusing → `abusing-dpapi-for-credential-access`, `extracting-browser-history-artifacts`, `performing-credential-access-with-lazagne` ; 1 more, grep to expand
- **C28 暴力破解与口令喷射** (15) triggers: 暴力破解 / 口令喷射 ; spray, brute, o365 → `barq-azure-ad`, `hydra-service-brute` ; 13 more, grep to expand
- **C29 内网发现与枚举** (17) triggers: 内网发现 / 枚举 ; ldap, enum, smb → `ad-ldap-enum-ldap`, `adidnsdump-ldap-enum` ; 15 more, grep to expand
- **C30 AD域渗透与域控攻击** (50) [sub-cats → ref] triggers: AD域渗透 / 域控攻击 ; active, directory, bloodhound → `abusing-shadow-credentials-for-privesc`, `attacking-entra-id-with-roadtools`, `conducting-internal-network-penetration-test`, `aclpwn-acl-abuse`, `activedirectoryenum-ad`
- **C31 远程服务横向移动** (13) triggers: 远程服务横向移动 ; lateral, movement, performing → `exploiting-ms17-010-eternalblue-vulnerability`, `performing-lateral-movement-detection`, `performing-lateral-movement-with-wmiexec`, `barmie-rmi-attack`, `impacket-protocol-exec` ; 8 more, grep to expand
- **C32 隧道与内网穿透** (12) triggers: 隧道 / 内网穿透 ; pivot, tunnel, stack → `stack-overflow-and-rop`, `tunneling-and-pivoting`, `frp-tunnel`, `chisel-tunnel` ; 8 more, grep to expand
- **C33 数据收集与打包暂存** (4) triggers: 数据收集 / 打包暂存 ; acquiring, disk, image → `acquiring-disk-image-with-dd-and-dcfldd`, `paramspider-param-harvest`, `tlsx-tls-enum` ; 1 more, grep to expand
- **C34 屏幕与输入捕获** (3) triggers: 屏幕 / 输入捕获 ; offensive, keylogger, arch → `offensive-keylogger-arch`, `scrying-multi-screenshot`, `witnessme-web-shot` ; 0 more, grep to expand
- **C35 C2框架与远控** (21) triggers: C2框架 / 远控 ; performing, infrastructure, building → `building-c2-redirector-infrastructure`, `building-red-team-c2-infrastructure-with-havoc`, `exploiting-aws-with-pacu`, `adaptix-c2-framework`, `emp3r0r-c2` ; 16 more, grep to expand
- **C36 隐蔽回连与通信通道** (3) triggers: 隐蔽回连 / 通信通道 ; icmpsh, reverse, interactsh → `icmpsh-reverse`, `interactsh-oob` ; 1 more, grep to expand
- **C37 数据外传** (2) triggers: 数据外传 ; data, exfiltrator, dnsteal → `data-exfiltrator`, `dnsteal-dns-exfil` ; 0 more, grep to expand
- **C38 隐写与隐藏通道** (4) triggers: 隐写 / 隐藏通道 ; stego, cloakify, exfil → `cloakify-exfil`, `openstego-general-stego` ; 2 more, grep to expand
- **C39 数据破坏与擦除** (3) triggers: 数据破坏 / 擦除 ; performing, binary, exploitation → `performing-binary-exploitation-analysis`, `exploit-development`, `slowhttptest-dos` ; 0 more, grep to expand
- **C40 嗅探与中间人攻击** (36) triggers: 嗅探 / 中间人攻击 ; mitm, performing, network → `conducting-man-in-the-middle-attack-simulation`, `performing-arp-spoofing-attack-simulation`, `performing-bandwidth-throttling-attack-simulation`, `above-protocol-anomaly`, `arpspoof-smikims` ; 31 more, grep to expand
- **C41 Web漏洞扫描与验证** (21) triggers: Web漏洞扫描 / 验证 ; performing, web, dir → `performing-container-security-scanning-with-trivy`, `performing-ssl-tls-security-assessment`, `ffuf-web-fuzz`, `nuclei-template-scan`, `gobuster-dir-dns` ; 16 more, grep to expand
- **C42 网络扫描与枚举** (40) triggers: 网络扫描 / 枚举 ; scan, network, offensive → `building-vulnerability-scanning-workflow`, `scanning-network-with-nmap-advanced`, `offensive-bug-identification`, `angry-ip-scan`, `apachetomcatscanner-tomcat` ; 35 more, grep to expand
- **C43 移动端攻击** (21) triggers: 移动端攻击 ; android, mobile, app → `conducting-mobile-app-penetration-test`, `exploiting-deeplink-vulnerabilities`, `exploiting-insecure-data-storage-in-mobile`, `appmon-ios-android`, `bagbak-ios-decrypt` ; 16 more, grep to expand
- **C44 AI与大模型安全** (12) triggers: AI / 大模型安全 ; llm, attacks, threat → `assessing-vector-and-embedding-weaknesses`, `orchestrating-llm-attacks-with-pyrit`, `performing-threat-modeling-with-owasp-threat-dragon`, `hexstrike-ai`, `pentestagent-crewai` ; 7 more, grep to expand
- **C45 恶意软件开发与免杀** (9) triggers: 恶意软件开发 / 免杀 ; macro, avet, evasion → `avet-av-evasion`, `bluffy-hollow` ; 7 more, grep to expand
- **C46 二进制漏洞利用与Pwn** (46) [sub-cats → ref] triggers: 二进制漏洞利用 / Pwn ; offensive, exploitation, penetration → `coercing-authentication-with-coercer-petitpotam`, `conducting-cloud-penetration-testing`, `conducting-network-penetration-test`, `angrop-rop-gen`, `armscgen-shellcode`
- **C47 逆向工程** (4) triggers: 逆向工程 ; open, redirect, exe2hexbat → `open-redirect`, `exe2hexbat-payload-transfer`, `petools-pe-analysis` ; 1 more, grep to expand
- **C48 区块链与Web3安全** (5) triggers: 区块链 / Web3安全 ; security, mev, smart → `mev-security`, `smart-contract-security`, `solana-security`, `slither-solidity-audit` ; 1 more, grep to expand
- **C49 密码学攻击** (22) triggers: 密码学攻击 ; crypto, attacks, rsa → `classical-cipher-analysis`, `lattice-crypto-attacks`, `rsa-attack-techniques`, `a2sv-ssl-vuln`, `cero-tls-cert` ; 17 more, grep to expand
- **C50 红队方法论与自动化** (38) triggers: 红队方法论 / 自动化 ; team, offensive, engagement → `conducting-full-scope-red-team-engagement`, `designing-adversary-engagement-with-mitre-engage`, `emulating-cloud-attacks-with-stratus-red-team`, `cloudfail-cloud-origin`, `engagement-discipline` ; 33 more, grep to expand
