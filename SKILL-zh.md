---
name: attack-skill-router
description: "攻击侧 Skill 库（996 个渗透测试 skill）的路由层。提供 search_skills 语义检索 HTTP API（由宿主常驻进程提供服务）、同名本地 CLI 兜底，以及作为最后手段的 50 类静态路由表。信号词：skill 路由、语义 skill 检索、渗透测试、CVE、侦察、漏洞利用、提权、横向移动、持久化、免杀、C2。"
zh-signals: "攻击侧 Skill 库（996 个渗透测试 skill）的路由层。提供 search_skills 语义检索 HTTP API（curl 调用宿主常驻服务，默认带 L3 cross-encoder 精排，约 1.4s 返回 top-k 候选与可直接 Read 的绝对路径，容器内无需挂载 venv/模型权重）、同名本地 CLI 兜底，以及 50 类静态路由表（前两者都不可用时兜底）。任务涉及侦察、漏洞利用、提权、横向移动、持久化、免杀、C2 等任一渗透环节时先加载本 skill，用它定位该读的 1-3 个 SKILL.md；不要在近千个 SKILL.md 里盲目 grep 全读。"
when-to-use: "渗透测试任务开始时；当已加载的 skill 无法解决当前障碍、需要重新路由时；当用户点名了具体的服务 / 工具 / 技术 / CVE 编号时（例如未授权 Redis、sqlmap、Java 反序列化、域内横向移动、UAC 绕过、CVE-xxxx-xxxx）。"
---

# 攻击侧 Skill 路由器（v2.2）

> ## 全局规则 —— 库内 skill 的加载方式（适用于路由路径 A、B 以及所有兜底分支）
>
> **Skill 工具只对 3 个已注册的 skill 生效**：`attack-skill-router`、`engagement-discipline`、`java-deserialization-gadget-selector`。**其余 994 个库内 skill 都是普通 markdown 文件，并非已注册的 Claude Code skill** —— 加载它们的唯一方式是用 **Read** 工具打开其绝对路径（路径 A 返回的 `candidates[].path`，或路径 B 中用 Glob 解析出的路径），然后自行遵循其中步骤。
> 调用 `Skill(<库内 slug>)` 永远返回 `Unknown skill`：这会浪费一轮交互，并悄无声息地中断路由链。所以永远不要把本路由器给出的 `slug` 当作 skill 名称。

## 目的

本库共有 996 个 skill，覆盖 50 个攻击类别。直接检索整个库会让 Agent 面对过多同质选项（实测：一次反序列化查询同时拉进了 3 个重叠的 skill）。
**本路由层把"从 996 个里选 N 个"压缩为"先选 50 类中的 1 类 → 再从该类的 3-5 个主选中挑 1-3 个"**，同时提供直接返回 top-k 候选的语义路由 API（每次 curl 约 1.4s，因为默认开启 L3 精排）。

## 直接调用（`/attack-skill-router`）

用户可以用 `/attack-skill-router <一句话任务描述>` 显式触发本 skill。传给本次调用的参数为：

> $ARGUMENTS

- **参数非空** → 直接把它当作 query，执行下文"路由路径 A —— 标准调用"；
- **参数为空**（或本 skill 是被自动加载的）→ 先自行从当前对话上下文中提炼出一个"任务 + 信号词"的 query（见 A 节的表格），再执行同样的步骤。绝不允许在未跑过路由查询的情况下凭记忆挑选 skill。

## 路由路径 A：search_skills HTTP API（必须优先尝试）

三级漏斗式语义路由（L1 embedding top-k 粗筛 → L2 RRF 融合排序 [余弦排名 + TF-IDF 排名] → L3 cross-encoder 精排）。L3 **默认开启** —— 你无需额外请求就能拿到精排后的顺序。它覆盖整个库，不受下文静态路由表 50 类粒度的限制。


### 第 0 步：确认服务存活（任务开始时跑一次，不要每次查询前都跑）

```bash
curl -sf --max-time 2 "${ROUTER_API:-http://10.22.16.51:8787}/health"
```

- 可达 → 静默返回；直接进入标准调用；
- `/health` 只报告语料规模 / 运行时长 / L3 是否已加载 / `rerank` 默认值，不会泄露库内容。

### 标准调用（原样复制，不要改写）

```bash
curl -sS --max-time 30 -G "${ROUTER_API:-http://10.22.16.51:8787}/search" \
  --data-urlencode 'query=<一句话任务描述>' \
  --data-urlencode top_k=5 --data-urlencode desc_chars=120
```

- **命令必须以 `curl` 开头**（`allowed-tools` 的预授权是按前缀匹配的；前面加环境变量赋值会破坏匹配）；
- `query` 通过 `--data-urlencode` 传入 —— 英文、空格、引号在你这一侧都无需转义；
- `top_k=5 desc_chars=120` 是为控制上下文 token 而选定的标准配置；响应体约 800 token；
- **不要**加 `rerank=1` —— 它已经是默认值。只有在批量筛选大量 query、且可以接受列表头部明显变差时才加 `--data-urlencode rerank=0`（约 0.1s 而非约 1.4s）；
- 结果 JSON 输出到 stdout，可直接解析；**`candidates[].path` 是已部署 skill 库内的绝对路径** —— 直接用 Read 打开即可，无需拼接仓库根目录；

### Agent 执行顺序

1. 执行第 0 步确认服务；
2. 把当前障碍写成一句英文的"任务 + 信号词" query，执行标准调用；
3. 读取 JSON，从 `candidates` 中挑出 **1-3** 个 `slug`。判断依据是 `description` 是否匹配当前的服务 / 版本 / 技术栈，**而不是 `score` 的绝对值**；
4. 用 Read 打开对应的 `path`，并遵循该 skill 的步骤。**Skill 工具只对顶部全局规则中列出的 3 个已注册 skill 有效 —— 所有库内 skill 都必须以 `Read <path>` 加载，绝不能用 `Skill(<slug>)`。不要把 5 个全读完，也不要再去 grep 整个库**；
5. 如果 top-5 全都不相关，按以下顺序升级，每一步只尝试一次：
   - (1) 改写 query，补充服务名 / 版本号 / 报错关键词 / 当前权限状态 → 重新执行标准调用；
   - (2) 回退到路由路径 B（静态路由表）；
6. 在最终报告末尾列出实际加载的 slug。

**每次查询约 1.4s，但一个任务通常仍只需 1-2 次查询**：查得更多并不会让答案更准，只会不断把同质候选塞进上下文。

### query 怎么写

| 好（任务 + 信号词） | 坏 |
|---|---|
| `Unauthenticated Redis instance exposed on the network, gain code execution via the database`（网络上暴露了未授权 Redis 实例，通过数据库获取代码执行） | `redis` |
| `Credentials for domain users have been obtained from the target DC; planning lateral movement to other hosts within the intranet`（已从目标域控获取域用户凭据，计划向内网其他主机横向移动） | `横向` |
| `Java deserialization vulnerability on WebLogic 10.3.6; need to craft a gadget chain`（WebLogic 10.3.6 存在 Java 反序列化漏洞，需要构造 gadget 链） | `deserialization` |
| `SQL injection in the login form, verify with an automated tool and dump the DB`（登录表单存在 SQL 注入，用自动化工具验证并脱库） | `exploiting-sql-injection-with-sqlmap`（slug 不是 query） |

**关键在于把每一个可被检索到的信号词都写出来**：服务名 + 版本、漏洞类型、你已掌握的权限/凭据，以及你想达成的动作。

### 响应体

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

（以上为服务端真实返回，故保持英文原样：`load` 与 `meta.consume` 在数据本身里重申了顶部全局规则 —— 用 Read 打开每个候选的绝对 `path` 字段；只有 attack-skill-router / engagement-discipline / java-deserialization-gadget-selector 是已注册 skill，其余库内 skill 都是普通文件，`Skill(<slug>)` 会返回 "Unknown skill"。）

`path` 的目录前缀取决于部署配置（`--lib-prefix`，默认 `/opt/attack-skill-library`）；它始终是绝对路径，原样 Read 即可。

`score` 是当前阶段的排序依据。在默认的 `rerank: true` 下它等于 `rerank_score`，即 0-1 之间的 cross-encoder 分数 —— 而且它**确实**有区分度：实测某未授权 Redis 查询的 top1 为 0.5484、top2 为 0.0165，所以第 1 名与第 2 名之间的巨大差距是"第 1 名就是正确 skill"的真实信号。在 `rerank=0` 下它则是 RRF 融合分数（量级约 0.03，且头部候选几乎打平 —— **只能用于相对排序；绝对值没有意义，不要把它当相似度阈值**）。`l1_sim` 始终是余弦相似度。`ready_ms` 是服务启动时的一次性加载耗时（不计入本次查询）；`latency_ms.total` 是本次查询自身的延迟（含并发排队），其中约 1.4s 是 CPU 上的 L3。`n_skills=994` 是检索语料的数字（磁盘上的 996 减去本路由层等已注册 skill），与评测框架保持一致。

出错时响应为 `{"error": {"code": 4xx/5xx, "message": "...", "hint": "..."}}` —— 按 `message` 修正参数即可，无需猜测。



## 路由路径 B：静态路由表（CLI 不可用时，按顺序执行）

1. **定位类别**：用下面的"路由表"按服务类型 / 漏洞类别 / 技术关键词 / CVE 匹配到某一行；
2. **选定主选 skill**：在该行的 3-5 个 slug 中，依据其 frontmatter 的 `when-to-use` 选出最贴合的 1-3 个；
3. **slug → path**：静态表只给 slug 不给路径，因此用 Glob 解析（一次调用可传多个模式）：`/opt/attack-skill-library/**/<slug>/SKILL.md` —— 如果本机不存在该根目录，就改用此前路径 A 的 `candidates[].path` 所指向的目录 —— 然后用 Read 打开。按顶部全局规则，这些都是普通文件：**Read 它们，绝不要 `Skill(<slug>)`**；
4. **不够就扩展**：对于标注了 `[sub-cats → ref]` 的类别（该类别下 skill 很多），打开 `reference.md`（它在本 SKILL.md 旁边，位于已注册 skill 目录内 —— 并**不在** `/opt/attack-skill-library` 下），按子标签收窄；其余情况使用 Grep 工具（`path` 设为 `/opt/attack-skill-library`，开启 `-i`）搜索有针对性的关键词 —— 不要通读整个库；
5. **汇报**：在最终报告末尾列出实际加载的 slug（与评测流程保持一致）。

注意：下面 50 个类别名及其触发词有意保留中文 —— 它们是源自中文 `INDEX.md`（分类权威）的数据，也是路由路径 B 的中文匹配面。

## 选择规则（A、B 通用）

- **方法论优先于工具**：优先选方法论类 skill（它们教你完整的利用链）；当方法论缺少具体命令时，再用工具封装类 skill（某个单一工具的说明书）补足；
- **同一主题只加载一个 skill**：同主题条目已在路由表内去重（见本 SKILL.md 旁边的 `MERGES.md`；人工裁决已完成，13 条合并 / 7 条不合并）。如果 CLI 或 grep 仍返回多个相似 slug，选 frontmatter 的 `when-to-use` 最贴合当前服务/版本的那一个；
- **版本敏感任务**（Java 反序列化 gadget、内核利用等）：方法论类 skill 只能给你思路；gadget 适配属于漏洞利用工程 —— 请依据该 skill 的指导加上目标版本自行构造，不要反复重试库里已过时的 gadget。

## 路由表（50 类，每类 5 个主选，一类一行）

- **C01 资产测绘与指纹识别**（62）[子类 → ref] 触发词：资产测绘 / 指纹识别 ; recon, osint, performing → `collecting-open-source-intelligence`、`performing-ai-driven-osint-correlation`、`performing-asset-criticality-scoring-for-vulns`、`alterx-dsl-subdomains`、`amass-attack-surface`
- **C02 域名与DNS侦察**（19）触发词：域名 / DNS侦察 ; dns, subdomain, performing → `performing-dns-enumeration-and-zone-transfer`、`performing-subdomain-enumeration-with-subfinder`、`cors-cross-origin-misconfiguration`、`aiodnsbrute-dns`、`altdns-permutation` ; 另有 14 个，用 grep 扩展
- **C03 邮箱与人员OSINT**（27）触发词：邮箱 / 人员OSINT ; osint, username, email → `profiling-threat-actor-groups`、`bridgekeeper-username-mangle`、`cr3dov3r-leak-lookup` ; 另有 24 个，用 grep 扩展
- **C04 网络拓扑与互联网测绘**（10）触发词：网络拓扑 / 互联网测绘 ; shodan, network, exploiting → `exploiting-bgp-hijacking-vulnerabilities`、`performing-ip-reputation-analysis-with-shodan`、`ctf-osint`、`asnmap-network-recon`、`fav-up-favicon-lookup` ; 另有 5 个，用 grep 扩展
- **C05 外部攻击面与云资产暴露**（31）触发词：外部攻击面 / 云资产暴露 ; exposure, offensive, cloud → `conducting-external-reconnaissance-with-osint`、`enumerating-cloud-with-cloudfox`、`exploiting-excessive-data-exposure-in-api`、`apkleaks-endpoint-scan`、`gh-dork-github` ; 另有 26 个，用 grep 扩展
- **C06 漏洞情报与漏洞库**（14）触发词：漏洞情报 / 漏洞库 ; cve, exploiting, search → `exploiting-nopac-cve-2021-42278-42287`、`exploiting-zerologon-vulnerability-cve-2020-1472`、`prototype-pollution`、`exploitdb-search`、`getsploit-exploit-search` ; 另有 9 个，用 grep 扩展
- **C07 载荷开发与武器化**（24）触发词：载荷开发 / 武器化 ; shellcode, evasion, payload → `conducting-spearphishing-simulation-campaign`、`csv-formula-injection`、`reverse-shell-techniques`、`chankro-php-binary`、`gadgettojscript-deser` ; 另有 19 个，用 grep 扩展
- **C08 钓鱼与社会工程**（25）触发词：钓鱼 / 社会工程 ; phishing, social, performing → `attacking-oauth-with-device-code-phishing`、`conducting-phishing-incident-response`、`conducting-social-engineering-penetration-test`、`bad-pdf-phish`、`credsniper-phish` ; 另有 20 个，用 grep 扩展
- **C09 Web应用漏洞利用**（171）[子类 → ref] 触发词：Web应用漏洞利用 ; offensive, exploiting, injection → `bypassing-authentication-with-forced-browsing`、`escaping-containers-to-host`、`exploiting-broken-function-level-authorization`、`bbqsql-blind-sqlmap`、`java-deserialization-gadget-selector`
- **C10 API与业务逻辑攻击**（54）[子类 → ref] 触发词：API / 业务逻辑攻击 ; api, jwt, performing → `conducting-api-security-testing`、`exploiting-api-injection-vulnerabilities`、`exploiting-idor-vulnerabilities`、`astra-api-scan`、`cariddi-crawler-secrets`
- **C11 边界设备与VPN攻击**（4）触发词：边界设备 / VPN攻击 ; offensive, anti, forensics → `offensive-anti-forensics`、`scada-attacker`、`cameradar-rtsp`、`sigploit-telecom` ; 另有 0 个，用 grep 扩展
- **C12 供应链与CI/CD攻击**（16）触发词：供应链 / CI/CD攻击 ; cicd, offensive, dependency → `continuous-llm-red-teaming-with-promptfoo`、`defending-llms-with-guardrails`、`implementing-fuzz-testing-in-cicd-with-aflplusplus`、`dvcs-ripper-vcs`、`git-dumper-repo` ; 另有 11 个，用 grep 扩展
- **C13 远程命令执行与WebShell**（8）触发词：远程命令执行 / WebShell ; shell, manager, htshells → `htshells-htaccess`、`novahot-web-shell` ; 另有 6 个，用 grep 扩展
- **C14 云与容器执行**（3）触发词：云 / 容器执行 ; container, escape, botb → `botb-container-attack`、`deepce-container-escape` ; 另有 1 个，用 grep 扩展
- **C15 持久化与后门植入**（13）触发词：持久化 / 后门植入 ; persistence, shell, conducting → `conducting-domain-persistence-with-dcsync`、`operating-sliver-c2`、`performing-malware-persistence-investigation`、`dbd-dns-tunnel-shell`、`gcat-gmail-c2` ; 另有 8 个，用 grep 扩展
- **C16 Linux本地提权**（8）触发词：Linux本地提权 ; privesc, linux, escape → `linux-privilege-escalation`、`sandbox-escape-techniques`、`privesc-advisor`、`linenum-privesc-scan`、`suid3num-privesc` ; 另有 3 个，用 grep 扩展
- **C17 Windows本地提权**（11）触发词：Windows本地提权 ; windows, privesc, offensive → `defi-attack-patterns`、`windows-privilege-escalation`、`offensive-k8s-attacks`、`beroot-privesc-check`、`powershdll-nopowershell` ; 另有 6 个，用 grep 扩展
- **C18 云与容器提权**（14）触发词：云 / 容器提权 ; performing, kubernetes, privilege → `auditing-kubernetes-rbac-privilege-escalation`、`performing-agentless-vulnerability-scanning`、`performing-aws-account-enumeration-with-scout-suite`、`cloudlist-multi-cloud`、`microburst-azure` ; 另有 9 个，用 grep 扩展
- **C19 EDR与AV规避**（4）触发词：EDR / AV规避 ; evasion, operating, havoc → `operating-havoc-c2`、`offensive-edr-evasion`、`evasion-specialist` ; 另有 1 个，用 grep 扩展
- **C20 反取证与痕迹清理**（4）触发词：反取证 / 痕迹清理 ; anti, forensic, mat → `mat-metadata-clean`、`moonwalk-anti-forensic` ; 另有 2 个，用 grep 扩展
- **C21 流量混淆与加密隧道**（1）触发词：流量混淆 / 加密隧道 ; offensive, data, exfiltration → `offensive-data-exfiltration` ; 另有 0 个，用 grep 扩展
- **C22 进程注入与内存执行**（19）触发词：进程注入 / 内存执行 ; injection, header, llm → `performing-packet-injection-attack`、`red-teaming-llms-with-garak`、`testing-for-email-header-injection`、`amber-reflective-packer` ; 另有 15 个，用 grep 扩展
- **C23 无文件与LOLBins滥用**（2）触发词：无文件 / LOLBins滥用 ; lolbas, living, off → `lolbas-living-off-land`、`m3-gen-msbuild` ; 另有 0 个，用 grep 扩展
- **C24 内存转储与LSASS窃取**（5）触发词：内存转储 / LSASS窃取 ; credentials, conducting, pass → `conducting-pass-the-ticket-attack`、`active-directory-acl-abuse`、`mimikatz-credentials`、`mimipenguin-linux` ; 另有 1 个，用 grep 扩展
- **C25 哈希与密码破解**（34）触发词：哈希 / 密码破解 ; wordlist, hash, brute → `performing-gcp-penetration-testing-with-gcpbucketbrute`、`performing-hash-cracking-with-hashcat`、`authbypass-authentication-flaws`、`bkcrack-zip-plaintext`、`john-hash-crack` ; 另有 29 个，用 grep 扩展
- **C26 Kerberos与票据攻击**（8）触发词：Kerberos / 票据攻击 ; kerberos, kerberoasting, exploiting → `exploiting-kerberoasting-with-impacket`、`extracting-credentials-from-memory-dump`、`performing-kerberoasting-attack`、`kekeo-kerberos`、`krbrelayx-kerberos-relay` ; 另有 3 个，用 grep 扩展
- **C27 本地凭证与浏览器窃取**（4）触发词：本地凭证 / 浏览器窃取 ; credential, access, abusing → `abusing-dpapi-for-credential-access`、`extracting-browser-history-artifacts`、`performing-credential-access-with-lazagne` ; 另有 1 个，用 grep 扩展
- **C28 暴力破解与口令喷射**（15）触发词：暴力破解 / 口令喷射 ; spray, brute, o365 → `barq-azure-ad`、`hydra-service-brute` ; 另有 13 个，用 grep 扩展
- **C29 内网发现与枚举**（17）触发词：内网发现 / 枚举 ; ldap, enum, smb → `ad-ldap-enum-ldap`、`adidnsdump-ldap-enum` ; 另有 15 个，用 grep 扩展
- **C30 AD域渗透与域控攻击**（50）[子类 → ref] 触发词：AD域渗透 / 域控攻击 ; active, directory, bloodhound → `abusing-shadow-credentials-for-privesc`、`attacking-entra-id-with-roadtools`、`conducting-internal-network-penetration-test`、`aclpwn-acl-abuse`、`activedirectoryenum-ad`
- **C31 远程服务横向移动**（13）触发词：远程服务横向移动 ; lateral, movement, performing → `exploiting-ms17-010-eternalblue-vulnerability`、`performing-lateral-movement-detection`、`performing-lateral-movement-with-wmiexec`、`barmie-rmi-attack`、`impacket-protocol-exec` ; 另有 8 个，用 grep 扩展
- **C32 隧道与内网穿透**（12）触发词：隧道 / 内网穿透 ; pivot, tunnel, stack → `stack-overflow-and-rop`、`tunneling-and-pivoting`、`frp-tunnel`、`chisel-tunnel` ; 另有 8 个，用 grep 扩展
- **C33 数据收集与打包暂存**（4）触发词：数据收集 / 打包暂存 ; acquiring, disk, image → `acquiring-disk-image-with-dd-and-dcfldd`、`paramspider-param-harvest`、`tlsx-tls-enum` ; 另有 1 个，用 grep 扩展
- **C34 屏幕与输入捕获**（3）触发词：屏幕 / 输入捕获 ; offensive, keylogger, arch → `offensive-keylogger-arch`、`scrying-multi-screenshot`、`witnessme-web-shot` ; 另有 0 个，用 grep 扩展
- **C35 C2框架与远控**（21）触发词：C2框架 / 远控 ; performing, infrastructure, building → `building-c2-redirector-infrastructure`、`building-red-team-c2-infrastructure-with-havoc`、`exploiting-aws-with-pacu`、`adaptix-c2-framework`、`emp3r0r-c2` ; 另有 16 个，用 grep 扩展
- **C36 隐蔽回连与通信通道**（3）触发词：隐蔽回连 / 通信通道 ; icmpsh, reverse, interactsh → `icmpsh-reverse`、`interactsh-oob` ; 另有 1 个，用 grep 扩展
- **C37 数据外传**（2）触发词：数据外传 ; data, exfiltrator, dnsteal → `data-exfiltrator`、`dnsteal-dns-exfil` ; 另有 0 个，用 grep 扩展
- **C38 隐写与隐藏通道**（4）触发词：隐写 / 隐藏通道 ; stego, cloakify, exfil → `cloakify-exfil`、`openstego-general-stego` ; 另有 2 个，用 grep 扩展
- **C39 数据破坏与擦除**（3）触发词：数据破坏 / 擦除 ; performing, binary, exploitation → `performing-binary-exploitation-analysis`、`exploit-development`、`slowhttptest-dos` ; 另有 0 个，用 grep 扩展
- **C40 嗅探与中间人攻击**（36）触发词：嗅探 / 中间人攻击 ; mitm, performing, network → `conducting-man-in-the-middle-attack-simulation`、`performing-arp-spoofing-attack-simulation`、`performing-bandwidth-throttling-attack-simulation`、`above-protocol-anomaly`、`arpspoof-smikims` ; 另有 31 个，用 grep 扩展
- **C41 Web漏洞扫描与验证**（21）触发词：Web漏洞扫描 / 验证 ; performing, web, dir → `performing-container-security-scanning-with-trivy`、`performing-ssl-tls-security-assessment`、`ffuf-web-fuzz`、`nuclei-template-scan`、`gobuster-dir-dns` ; 另有 16 个，用 grep 扩展
- **C42 网络扫描与枚举**（40）触发词：网络扫描 / 枚举 ; scan, network, offensive → `building-vulnerability-scanning-workflow`、`scanning-network-with-nmap-advanced`、`offensive-bug-identification`、`angry-ip-scan`、`apachetomcatscanner-tomcat` ; 另有 35 个，用 grep 扩展
- **C43 移动端攻击**（21）触发词：移动端攻击 ; android, mobile, app → `conducting-mobile-app-penetration-test`、`exploiting-deeplink-vulnerabilities`、`exploiting-insecure-data-storage-in-mobile`、`appmon-ios-android`、`bagbak-ios-decrypt` ; 另有 16 个，用 grep 扩展
- **C44 AI与大模型安全**（12）触发词：AI / 大模型安全 ; llm, attacks, threat → `assessing-vector-and-embedding-weaknesses`、`orchestrating-llm-attacks-with-pyrit`、`performing-threat-modeling-with-owasp-threat-dragon`、`hexstrike-ai`、`pentestagent-crewai` ; 另有 7 个，用 grep 扩展
- **C45 恶意软件开发与免杀**（9）触发词：恶意软件开发 / 免杀 ; macro, avet, evasion → `avet-av-evasion`、`bluffy-hollow` ; 另有 7 个，用 grep 扩展
- **C46 二进制漏洞利用与Pwn**（46）[子类 → ref] 触发词：二进制漏洞利用 / Pwn ; offensive, exploitation, penetration → `coercing-authentication-with-coercer-petitpotam`、`conducting-cloud-penetration-testing`、`conducting-network-penetration-test`、`angrop-rop-gen`、`armscgen-shellcode`
- **C47 逆向工程**（4）触发词：逆向工程 ; open, redirect, exe2hexbat → `open-redirect`、`exe2hexbat-payload-transfer`、`petools-pe-analysis` ; 另有 1 个，用 grep 扩展
- **C48 区块链与Web3安全**（5）触发词：区块链 / Web3安全 ; security, mev, smart → `mev-security`、`smart-contract-security`、`solana-security`、`slither-solidity-audit` ; 另有 1 个，用 grep 扩展
- **C49 密码学攻击**（22）触发词：密码学攻击 ; crypto, attacks, rsa → `classical-cipher-analysis`、`lattice-crypto-attacks`、`rsa-attack-techniques`、`a2sv-ssl-vuln`、`cero-tls-cert` ; 另有 17 个，用 grep 扩展
- **C50 红队方法论与自动化**（38）触发词：红队方法论 / 自动化 ; team, offensive, engagement → `conducting-full-scope-red-team-engagement`、`designing-adversary-engagement-with-mitre-engage`、`emulating-cloud-attacks-with-stratus-red-team`、`cloudfail-cloud-origin`、`engagement-discipline` ; 另有 33 个，用 grep 扩展
