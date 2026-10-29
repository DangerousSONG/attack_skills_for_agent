---
name: attack-skill-router
description: 攻击侧 Skill 库（996 个渗透测试 skill）的路由层。提供 search_skills 语义检索 HTTP API（curl 调用宿主常驻服务，约 0.1s 返回 top-k 候选与可直接 Read 的绝对路径，容器内无需挂载 venv/模型权重）、同名本地 CLI 兜底，以及 50 类静态路由表（前两者都不可用时兜底）。任务涉及侦察、漏洞利用、提权、横向移动、持久化、免杀、C2 等任一渗透环节时先加载本 skill，用它定位该读的 1-3 个 SKILL.md；不要在近千个 SKILL.md 里盲目 grep 全读。
when_to_use: 渗透任务开题时；已加载的 skill 解决不了当前障碍、需要换路由时；用户提到具体服务/工具/技术/CVE 编号（如 Redis 未授权、sqlmap、Java 反序列化、域渗透、UAC 绕过、CVE-xxxx-xxxx）时。
argument-hint: 一句话任务描述，例如 Redis 未授权访问想拿 shell
allowed-tools: Bash(curl:*), Bash(bash /home/panjiahao/safe-range/attack_skills_for_agent/scripts/router_server.sh:*), Bash(/home/panjiahao/safe-range/attack_skills_for_agent/scripts/search_skills:*)
---

# Attack Skill Router · 攻击 Skill 路由层（v2.2）

## 用途

本库共 996 个 skill（50 个攻击大类）。直接全库搜索会让 Agent 面对过量同质选项（实测：反序列化主题曾一次装入 3 个重叠 skill）。
**本路由层把「996 选 N」压缩为「50 类选 1 类 → 每类 3-5 个 primary 选 1-3 个」**，并提供语义路由 API 直接输出 top-k 候选（curl 一次约 0.1s）。

## 直接调用（`/attack-skill-router`）

用户可用 `/attack-skill-router <一句话任务描述>` 显式触发本 skill。本次调用传入的参数为：

> $ARGUMENTS

- **参数非空** → 直接把它当作 query，执行下方「路由方式 A · 标准调用」；
- **参数为空**（或本 skill 是被自动加载的）→ 先从当前对话上下文里自己提炼一句「任务 + 信号词」的 query（写法见 A 节表格），再执行同样步骤。不要在没跑过路由检索的情况下直接凭印象挑 skill。

## 路由方式 A：search_skills HTTP API（推荐，先试这个）

三层漏斗语义路由（L1 embedding top-k 粗筛 → L2 RRF 融合排序〔余弦名次 + TF-IDF 名次〕→ L3 cross-encoder 精排），覆盖全库，不受下方静态表 50 类粒度限制。

检索逻辑跑在**宿主常驻服务**（`/home/panjiahao/safe-range/attack_skills_for_agent/scripts/router_server.py`）里：bge-m3、全库 994 条向量、TF-IDF 向量器都只在启动时加载一次，所以**单次查询约 0.1s**（本地 CLI 每次进程冷启动要重付约 5.3s 建模，故约 6s）。容器里的 Agent 只要能发 HTTP 就能用，**不必挂载 5.6G 的 venv 或 4.5G 的模型权重**。设计与评测数据见 `/home/panjiahao/safe-range/attack_skills_for_agent/DESIGN.md`。

### 第 0 步：确认服务活着（每次任务开头跑一次即可，不是每次查询都跑）

```bash
curl -sf --max-time 2 "${ROUTER_API:-http://127.0.0.1:8787}/health" >/dev/null || bash /home/panjiahao/safe-range/attack_skills_for_agent/scripts/router_server.sh start
```

- 通了 → 静默返回，直接进标准调用；
- 不通 → 后半句拉起服务（阻塞到就绪；索引已缓存时约 5-10s，`_index/` 缺失需现场编码全库则约 2 分钟）。**只试这一次**：退出码非 0（3=环境未就绪 / 4=启动失败）就走下面的「降级链」，不要反复重试；
- `/health` 只报语料条数 / 存活时长 / 是否已加载 L3，不泄露库内容。

### 标准调用（照抄这一条，不要改写）

```bash
curl -sS --max-time 30 -G "${ROUTER_API:-http://127.0.0.1:8787}/search" \
  --data-urlencode 'query=<一句话任务描述>' \
  --data-urlencode top_k=5 --data-urlencode desc_chars=120
```

- **命令必须以 `curl` 开头**（`allowed-tools` 的预批准按前缀匹配；前面加环境变量赋值会让它失效）；
- `query` 用 `--data-urlencode` 传，中英文、空格、引号都不用你自己转义；
- `top_k=5 desc_chars=120` 是为控上下文 token 定的标准配置，返回体约 800 token；
- 结果 JSON 走 stdout，可直接解析；**`candidates[].path` 是绝对路径**，用 Read 打开即可，不需要再拼仓库根；
- **服务无鉴权**：能连到 `${ROUTER_API}` 就能查，不需要任何凭据。不要去找 token 文件，也不要自己加 `-H "Authorization: ..."`（旧文档里可能有，已废弃）。

### Agent 执行序列

1. 跑第 0 步确认服务；
2. 把当前障碍写成一句「任务 + 信号词」的 query（写法见下表），跑标准调用；
3. 读 JSON，从 `candidates` 里挑 **1-3 个** `slug`。判断依据是 `description` 与当前 服务/版本/技术栈 是否对得上，**不是 `score` 的绝对值**；
4. 用 Read 打开对应 `path`，按该 skill 的步骤执行。**不要全读 5 个，不要再 grep 全库**；
5. top-5 全不相关时，按此顺序升级，每步只试一次：
   - ① 重写 query，补上服务名 / 版本号 / 报错关键词 / 已有权限状态 → 重跑标准调用；
   - ② 加 `--data-urlencode rerank=1`（L3 cross-encoder 精排，已预热约 +2.6s，首次调用还要多约 2s 加载）；
   - ③ 转路由方式 B（静态表）；
6. 最终报告末尾列出实际加载的 slug。

**约 0.1s 一次，但一次任务通常仍只需 1-2 次查询**：多查不会更准，只会把同质候选反复装进上下文。

### query 写法

| 好（任务 + 信号词） | 差 |
|---|---|
| `Unauthenticated Redis instance exposed on the network, gain code execution via the database` | `redis` |
| `目标域控已拿到域用户凭据，想做横向移动到内网其他主机` | `横向` |
| `Java 应用反序列化漏洞，WebLogic 10.3.6，需要构造 gadget 链` | `deserialization` |
| `SQL injection in the login form, verify with an automated tool and dump the DB` | `exploiting-sql-injection-with-sqlmap`（slug 不是 query）|

中英文均可（默认模型 `BAAI/bge-m3` 为多语言）。**关键是把可检索的信号词写全**：服务名 + 版本、漏洞类型、当前已有的权限/凭据状态、想达成的动作。

### 返回体

```json
{"query": "...",
 "candidates": [{"slug": "database-attacker", "name": "...",
                 "description": "...", "path": "/home/panjiahao/safe-range/attack_skills_for_agent/Anthropic-Cybersecurity-Skills/.../SKILL.md",
                 "score": 0.0328, "l1_sim": 0.575, "rerank_score": 0.63}],
 "meta": {"l1_kept": 50, "n_skills": 994, "l1_topk": 50, "rrf_k0": 60,
          "emb_model": "BAAI/bge-m3", "rerank": false, "degraded": false,
          "ready_ms": 5149, "latency_ms": {"l1": 80, "l2": 4, "l3": 0, "total": 85}}}
```

`score` 是当层排序依据：未开 `rerank` 时为 RRF 融合分（量级约 0.03，**只用来看相对次序，绝对值无意义，不要当相似度阈值**）；开了则为 cross-encoder 分。`l1_sim` 始终是余弦相似度。`ready_ms` 是服务启动时的一次性加载耗时（不计入本次查询），`latency_ms.total` 才是本次查询耗时（含并发排队）。`n_skills=994` 是检索语料口径（磁盘 996 减去本路由层等注册 skill），与评测 harness 一致。

出错时返回 `{"error": {"code": 4xx/5xx, "message": "...", "hint": "..."}}`，按 message 改参数即可，不必猜。

### 降级链（严格按序，每级只试一次）

```
① HTTP API（约 0.1s）→ ② 本地 CLI /home/panjiahao/safe-range/attack_skills_for_agent/scripts/search_skills（约 6s）→ ③ 静态路由表 B
```

② 的调用方式：`/home/panjiahao/safe-range/attack_skills_for_agent/scripts/search_skills "<query>" --top-k 5 --desc-chars 120`（无扩展名 bash 包装脚本，自定位仓库根、自动解析带 torch 的解释器、预检模型与索引；不需要 cd、不需要自己找 python）。**②③ 的返回体与 query 写法与 ① 完全一致**，换级不用改判断逻辑。

| 现象 | 含义 | 该怎么办 |
|---|---|---|
| `curl: (7) Failed to connect` | 服务没起 | 跑一次第 0 步（内含 `router_server.sh start`）；仍不通 → 降级 ② |
| HTTP **422** + `error.message` | 参数名写错或超范围 | 按 message 改。合法参数：`query` `top_k`(1-50) `desc_chars`(0-2000) `l1_topk` `l2_topn` `rerank` `format`(json 或 text) |
| HTTP **500** | 服务端检索异常（索引/权重损坏） | `bash /home/panjiahao/safe-range/attack_skills_for_agent/scripts/router_server.sh logs 50` 看原因；必要时 `stop` 后手动带 `--rebuild-index` 重启。期间降级 ② |
| ② 退出码 **3** + `环境未就绪` | 缺可用解释器，或缺 `demo/models/BAAI/bge-m3` 权重 | **别重试**。stderr 已给出确切修复命令；无人值守时直接转 ③，并在报告里注明 A 不可用 |
| ② 退出码 **2** / 首次约 **2 分钟** | 参数或索引错误 / 正在编码全库 994 条写入 `_index/` | 2 → 加 `--rebuild-index` 重跑一次；首次编码属正常，**不是卡死**，别中断 |
| `degraded: true` | `l1_topk` ≥ 语料规模，粗筛没剔除任何候选 | 结果仍可用，只是没享受漏斗加速。默认 50 时不会出现，出现说明有人手工放宽了 k |
| 候选全是 `offensive-*` / `auth-sec` 这类泛化兜底 slug | query 信号词不足 | 按升级步骤 ① 重写 query |

### 容器内调用（本方案的主要收益之一）

容器里**不需要** python 依赖、不需要 venv、不需要模型权重，只要能发 HTTP：

- `ROUTER_API` 指向宿主的 docker 网桥网关。**本机实测是 `172.16.0.1`，不是 docker 默认的 `172.17.0.1`** —— 别硬编码，容器内这样取：读 `/proc/net/route` 里 `Destination` 为 `00000000` 那行的 `Gateway`（十六进制小端），或起容器时加 `--add-host=host.docker.internal:host-gateway` 后用 `http://host.docker.internal:8787`；
- 服务无鉴权，容器里**不用传任何凭据**，`ROUTER_API` 一个环境变量就够；
- **`candidates[].path` 是宿主绝对路径**，容器里直接 Read 会失败。要能读原文就得把库挂进容器且**挂在同一路径**：`-v /home/panjiahao/safe-range/attack_skills_for_agent:/home/panjiahao/safe-range/attack_skills_for_agent:ro`（去掉 `demo/models`、`.git`、`_index` 后仅约 17M）。不想挂就只用 `slug` + `description` 判断，再让宿主侧 Agent 去 Read。

### 服务托管

`bash /home/panjiahao/safe-range/attack_skills_for_agent/scripts/router_server.sh` 不带参数即打印用法（start / stop / restart / status / logs / curl）。端口与监听地址用 `ROUTER_PORT`（默认 8787）、`ROUTER_HOST`（默认 `0.0.0.0`）覆盖。**服务无鉴权**，默认绑 `0.0.0.0` 是为了让容器能连，代价是**同网段任何人都能无凭据查到全库 skill 清单与宿主机绝对路径**；要收窄暴露面就设 `ROUTER_HOST=127.0.0.1`（仅本机，容器需 `--network host`）或 docker 网桥地址（仅容器可达，LAN 连不上）。

### 其他参数（日常不用，列出备查）

`rerank=1`（追加 L3 cross-encoder，精度最高）、`format=text`（人读格式，`text/plain`）、`l1_topk`（L1 候选预算，默认 50，本语料金标零丢失）、`l2_topn`（送 L3 的条数，默认 20）、`desc_chars`（description 截断长度，API 默认 200、标准调用传 120）。CLI 侧另有 `-`（从 stdin 读 query）、`--emb-model`（默认 `BAAI/bge-m3`，1024 维多语言；语料 description 100% 中英混排，**勿换纯英文模型**）、`--rebuild-index`（skill 增删改后必须）。API 与 CLI 同名参数语义一致，只是 API 用下划线（`top_k`）、CLI 用连字符（`--top-k`）。

选点标定与 recall 回归属于**维护动作，Agent 日常不用跑**：`demo/router_demo.py`（107 条金标，报告落 `demo/report/report_<ts>.json`；`--grid` 跑 l1-topk × l2-topn 网格搜索，结果表自动写入 DESIGN.md §2.3）。当前 bge-m3 实测：L1 存活集召回 100%、L2 @5 94.4%、**L3 @5 95.3% / @20 100%**（纯 TF-IDF baseline @5 仅 84.1%）。

## 路由方式 B：静态路由表（CLI 不可用时，按序执行）

1. **定位大类**：用下方「路由表」按 服务类型 / 漏洞类别 / 技术关键词 / CVE 命中一行；
2. **选 primary**：在该行的 3-5 个 slug 中，按 frontmatter 的 when-to-use 选 1-3 个最贴切的；
3. **slug → 路径**：静态表只给 slug 不给路径，用 Glob 解析（一次调用可传多个 pattern）：`/home/panjiahao/safe-range/attack_skills_for_agent/**/<slug>/SKILL.md`，再用 Read 打开。库内 skill **没有**注册成 Claude Code skill，**不要用 Skill 工具加载它们**，只能 Read 文件后自己照做；
4. **不够再扩**：大类标了〔二级子类→ref〕的（本类 skill 多），展开 `/home/panjiahao/safe-range/attack_skills_for_agent/attack-skill-router/reference.md` 按子标签细选；其余用 Grep 工具（`path` 设为 `/home/panjiahao/safe-range/attack_skills_for_agent`，`-i` 开）按关键词定向补，不要全库通读；
5. **报告**：最终报告末尾列出实际加载的 slug（与评测工作流一致）。

## 选用规则（A / B 通用）

- **方法论优先于工具**：先选 methodology skill（教你利用链），工具改写 skill（单个工具的说明书）在方法论缺具体命令时补；
- **同主题只装一个**：路由表内同主题已做去重（见 `/home/panjiahao/safe-range/attack_skills_for_agent/attack-skill-router/MERGES.md`，已完成人工裁决 13 并 / 7 不并），若 CLI 返回或 grep 仍命中多个相似 slug，选 frontmatter 里 when-to-use 与当前服务/版本最贴合的那个；
- **版本敏感型任务**（Java 反序列化 gadget、内核 exploit 等）：方法论 skill 只能给思路，gadget 适配属 exploit 工程，按 skill 指引 + 目标版本自建，不要反复重试库内旧 gadget。

## 路由表（50 类 · 每类 primary 5 个 · 一行一类）

- **C01 资产测绘与指纹识别**（62）〔二级子类→ref〕 触发:资产测绘 / 指纹识别 ; recon, osint, performing → `collecting-open-source-intelligence`, `performing-ai-driven-osint-correlation`, `performing-asset-criticality-scoring-for-vulns`, `alterx-dsl-subdomains`, `amass-attack-surface`
- **C02 域名与DNS侦察**（19） 触发:域名 / DNS侦察 ; dns, subdomain, performing → `performing-dns-enumeration-and-zone-transfer`, `performing-subdomain-enumeration-with-subfinder`, `cors-cross-origin-misconfiguration`, `aiodnsbrute-dns`, `altdns-permutation` ; 更多 14 个 grep 扩
- **C03 邮箱与人员OSINT**（27） 触发:邮箱 / 人员OSINT ; osint, username, email → `profiling-threat-actor-groups`, `bridgekeeper-username-mangle`, `cr3dov3r-leak-lookup` ; 更多 24 个 grep 扩
- **C04 网络拓扑与互联网测绘**（10） 触发:网络拓扑 / 互联网测绘 ; shodan, network, exploiting → `exploiting-bgp-hijacking-vulnerabilities`, `performing-ip-reputation-analysis-with-shodan`, `ctf-osint`, `asnmap-network-recon`, `fav-up-favicon-lookup` ; 更多 5 个 grep 扩
- **C05 外部攻击面与云资产暴露**（31） 触发:外部攻击面 / 云资产暴露 ; exposure, offensive, cloud → `conducting-external-reconnaissance-with-osint`, `enumerating-cloud-with-cloudfox`, `exploiting-excessive-data-exposure-in-api`, `apkleaks-endpoint-scan`, `gh-dork-github` ; 更多 26 个 grep 扩
- **C06 漏洞情报与漏洞库**（14） 触发:漏洞情报 / 漏洞库 ; cve, exploiting, search → `exploiting-nopac-cve-2021-42278-42287`, `exploiting-zerologon-vulnerability-cve-2020-1472`, `prototype-pollution`, `exploitdb-search`, `getsploit-exploit-search` ; 更多 9 个 grep 扩
- **C07 载荷开发与武器化**（24） 触发:载荷开发 / 武器化 ; shellcode, evasion, payload → `conducting-spearphishing-simulation-campaign`, `csv-formula-injection`, `reverse-shell-techniques`, `chankro-php-binary`, `gadgettojscript-deser` ; 更多 19 个 grep 扩
- **C08 钓鱼与社会工程**（25） 触发:钓鱼 / 社会工程 ; phishing, social, performing → `attacking-oauth-with-device-code-phishing`, `conducting-phishing-incident-response`, `conducting-social-engineering-penetration-test`, `bad-pdf-phish`, `credsniper-phish` ; 更多 20 个 grep 扩
- **C09 Web应用漏洞利用**（171）〔二级子类→ref〕 触发:Web应用漏洞利用 ; offensive, exploiting, injection → `bypassing-authentication-with-forced-browsing`, `escaping-containers-to-host`, `exploiting-broken-function-level-authorization`, `bbqsql-blind-sqlmap`, `java-deserialization-gadget-selector`
- **C10 API与业务逻辑攻击**（54）〔二级子类→ref〕 触发:API / 业务逻辑攻击 ; api, jwt, performing → `conducting-api-security-testing`, `exploiting-api-injection-vulnerabilities`, `exploiting-idor-vulnerabilities`, `astra-api-scan`, `cariddi-crawler-secrets`
- **C11 边界设备与VPN攻击**（4） 触发:边界设备 / VPN攻击 ; offensive, anti, forensics → `offensive-anti-forensics`, `scada-attacker`, `cameradar-rtsp`, `sigploit-telecom` ; 更多 0 个 grep 扩
- **C12 供应链与CI/CD攻击**（16） 触发:供应链 / CI/CD攻击 ; cicd, offensive, dependency → `continuous-llm-red-teaming-with-promptfoo`, `defending-llms-with-guardrails`, `implementing-fuzz-testing-in-cicd-with-aflplusplus`, `dvcs-ripper-vcs`, `git-dumper-repo` ; 更多 11 个 grep 扩
- **C13 远程命令执行与WebShell**（8） 触发:远程命令执行 / WebShell ; shell, manager, htshells → `htshells-htaccess`, `novahot-web-shell` ; 更多 6 个 grep 扩
- **C14 云与容器执行**（3） 触发:云 / 容器执行 ; container, escape, botb → `botb-container-attack`, `deepce-container-escape` ; 更多 1 个 grep 扩
- **C15 持久化与后门植入**（13） 触发:持久化 / 后门植入 ; persistence, shell, conducting → `conducting-domain-persistence-with-dcsync`, `operating-sliver-c2`, `performing-malware-persistence-investigation`, `dbd-dns-tunnel-shell`, `gcat-gmail-c2` ; 更多 8 个 grep 扩
- **C16 Linux本地提权**（8） 触发:Linux本地提权 ; privesc, linux, escape → `linux-privilege-escalation`, `sandbox-escape-techniques`, `privesc-advisor`, `linenum-privesc-scan`, `suid3num-privesc` ; 更多 3 个 grep 扩
- **C17 Windows本地提权**（11） 触发:Windows本地提权 ; windows, privesc, offensive → `defi-attack-patterns`, `windows-privilege-escalation`, `offensive-k8s-attacks`, `beroot-privesc-check`, `powershdll-nopowershell` ; 更多 6 个 grep 扩
- **C18 云与容器提权**（14） 触发:云 / 容器提权 ; performing, kubernetes, privilege → `auditing-kubernetes-rbac-privilege-escalation`, `performing-agentless-vulnerability-scanning`, `performing-aws-account-enumeration-with-scout-suite`, `cloudlist-multi-cloud`, `microburst-azure` ; 更多 9 个 grep 扩
- **C19 EDR与AV规避**（4） 触发:EDR / AV规避 ; evasion, operating, havoc → `operating-havoc-c2`, `offensive-edr-evasion`, `evasion-specialist` ; 更多 1 个 grep 扩
- **C20 反取证与痕迹清理**（4） 触发:反取证 / 痕迹清理 ; anti, forensic, mat → `mat-metadata-clean`, `moonwalk-anti-forensic` ; 更多 2 个 grep 扩
- **C21 流量混淆与加密隧道**（1） 触发:流量混淆 / 加密隧道 ; offensive, data, exfiltration → `offensive-data-exfiltration` ; 更多 0 个 grep 扩
- **C22 进程注入与内存执行**（19） 触发:进程注入 / 内存执行 ; injection, header, llm → `performing-packet-injection-attack`, `red-teaming-llms-with-garak`, `testing-for-email-header-injection`, `amber-reflective-packer` ; 更多 15 个 grep 扩
- **C23 无文件与LOLBins滥用**（2） 触发:无文件 / LOLBins滥用 ; lolbas, living, off → `lolbas-living-off-land`, `m3-gen-msbuild` ; 更多 0 个 grep 扩
- **C24 内存转储与LSASS窃取**（5） 触发:内存转储 / LSASS窃取 ; credentials, conducting, pass → `conducting-pass-the-ticket-attack`, `active-directory-acl-abuse`, `mimikatz-credentials`, `mimipenguin-linux` ; 更多 1 个 grep 扩
- **C25 哈希与密码破解**（34） 触发:哈希 / 密码破解 ; wordlist, hash, brute → `performing-gcp-penetration-testing-with-gcpbucketbrute`, `performing-hash-cracking-with-hashcat`, `authbypass-authentication-flaws`, `bkcrack-zip-plaintext`, `john-hash-crack` ; 更多 29 个 grep 扩
- **C26 Kerberos与票据攻击**（8） 触发:Kerberos / 票据攻击 ; kerberos, kerberoasting, exploiting → `exploiting-kerberoasting-with-impacket`, `extracting-credentials-from-memory-dump`, `performing-kerberoasting-attack`, `kekeo-kerberos`, `krbrelayx-kerberos-relay` ; 更多 3 个 grep 扩
- **C27 本地凭证与浏览器窃取**（4） 触发:本地凭证 / 浏览器窃取 ; credential, access, abusing → `abusing-dpapi-for-credential-access`, `extracting-browser-history-artifacts`, `performing-credential-access-with-lazagne` ; 更多 1 个 grep 扩
- **C28 暴力破解与口令喷射**（15） 触发:暴力破解 / 口令喷射 ; spray, brute, o365 → `barq-azure-ad`, `hydra-service-brute` ; 更多 13 个 grep 扩
- **C29 内网发现与枚举**（17） 触发:内网发现 / 枚举 ; ldap, enum, smb → `ad-ldap-enum-ldap`, `adidnsdump-ldap-enum` ; 更多 15 个 grep 扩
- **C30 AD域渗透与域控攻击**（50）〔二级子类→ref〕 触发:AD域渗透 / 域控攻击 ; active, directory, bloodhound → `abusing-shadow-credentials-for-privesc`, `attacking-entra-id-with-roadtools`, `conducting-internal-network-penetration-test`, `aclpwn-acl-abuse`, `activedirectoryenum-ad`
- **C31 远程服务横向移动**（13） 触发:远程服务横向移动 ; lateral, movement, performing → `exploiting-ms17-010-eternalblue-vulnerability`, `performing-lateral-movement-detection`, `performing-lateral-movement-with-wmiexec`, `barmie-rmi-attack`, `impacket-protocol-exec` ; 更多 8 个 grep 扩
- **C32 隧道与内网穿透**（12） 触发:隧道 / 内网穿透 ; pivot, tunnel, stack → `stack-overflow-and-rop`, `tunneling-and-pivoting`, `frp-tunnel`, `chisel-tunnel` ; 更多 8 个 grep 扩
- **C33 数据收集与打包暂存**（4） 触发:数据收集 / 打包暂存 ; acquiring, disk, image → `acquiring-disk-image-with-dd-and-dcfldd`, `paramspider-param-harvest`, `tlsx-tls-enum` ; 更多 1 个 grep 扩
- **C34 屏幕与输入捕获**（3） 触发:屏幕 / 输入捕获 ; offensive, keylogger, arch → `offensive-keylogger-arch`, `scrying-multi-screenshot`, `witnessme-web-shot` ; 更多 0 个 grep 扩
- **C35 C2框架与远控**（21） 触发:C2框架 / 远控 ; performing, infrastructure, building → `building-c2-redirector-infrastructure`, `building-red-team-c2-infrastructure-with-havoc`, `exploiting-aws-with-pacu`, `adaptix-c2-framework`, `emp3r0r-c2` ; 更多 16 个 grep 扩
- **C36 隐蔽回连与通信通道**（3） 触发:隐蔽回连 / 通信通道 ; icmpsh, reverse, interactsh → `icmpsh-reverse`, `interactsh-oob` ; 更多 1 个 grep 扩
- **C37 数据外传**（2） 触发:数据外传 ; data, exfiltrator, dnsteal → `data-exfiltrator`, `dnsteal-dns-exfil` ; 更多 0 个 grep 扩
- **C38 隐写与隐藏通道**（4） 触发:隐写 / 隐藏通道 ; stego, cloakify, exfil → `cloakify-exfil`, `openstego-general-stego` ; 更多 2 个 grep 扩
- **C39 数据破坏与擦除**（3） 触发:数据破坏 / 擦除 ; performing, binary, exploitation → `performing-binary-exploitation-analysis`, `exploit-development`, `slowhttptest-dos` ; 更多 0 个 grep 扩
- **C40 嗅探与中间人攻击**（36） 触发:嗅探 / 中间人攻击 ; mitm, performing, network → `conducting-man-in-the-middle-attack-simulation`, `performing-arp-spoofing-attack-simulation`, `performing-bandwidth-throttling-attack-simulation`, `above-protocol-anomaly`, `arpspoof-smikims` ; 更多 31 个 grep 扩
- **C41 Web漏洞扫描与验证**（21） 触发:Web漏洞扫描 / 验证 ; performing, web, dir → `performing-container-security-scanning-with-trivy`, `performing-ssl-tls-security-assessment`, `ffuf-web-fuzz`, `nuclei-template-scan`, `gobuster-dir-dns` ; 更多 16 个 grep 扩
- **C42 网络扫描与枚举**（40） 触发:网络扫描 / 枚举 ; scan, network, offensive → `building-vulnerability-scanning-workflow`, `scanning-network-with-nmap-advanced`, `offensive-bug-identification`, `angry-ip-scan`, `apachetomcatscanner-tomcat` ; 更多 35 个 grep 扩
- **C43 移动端攻击**（21） 触发:移动端攻击 ; android, mobile, app → `conducting-mobile-app-penetration-test`, `exploiting-deeplink-vulnerabilities`, `exploiting-insecure-data-storage-in-mobile`, `appmon-ios-android`, `bagbak-ios-decrypt` ; 更多 16 个 grep 扩
- **C44 AI与大模型安全**（12） 触发:AI / 大模型安全 ; llm, attacks, threat → `assessing-vector-and-embedding-weaknesses`, `orchestrating-llm-attacks-with-pyrit`, `performing-threat-modeling-with-owasp-threat-dragon`, `hexstrike-ai`, `pentestagent-crewai` ; 更多 7 个 grep 扩
- **C45 恶意软件开发与免杀**（9） 触发:恶意软件开发 / 免杀 ; macro, avet, evasion → `avet-av-evasion`, `bluffy-hollow` ; 更多 7 个 grep 扩
- **C46 二进制漏洞利用与Pwn**（46）〔二级子类→ref〕 触发:二进制漏洞利用 / Pwn ; offensive, exploitation, penetration → `coercing-authentication-with-coercer-petitpotam`, `conducting-cloud-penetration-testing`, `conducting-network-penetration-test`, `angrop-rop-gen`, `armscgen-shellcode`
- **C47 逆向工程**（4） 触发:逆向工程 ; open, redirect, exe2hexbat → `open-redirect`, `exe2hexbat-payload-transfer`, `petools-pe-analysis` ; 更多 1 个 grep 扩
- **C48 区块链与Web3安全**（5） 触发:区块链 / Web3安全 ; security, mev, smart → `mev-security`, `smart-contract-security`, `solana-security`, `slither-solidity-audit` ; 更多 1 个 grep 扩
- **C49 密码学攻击**（22） 触发:密码学攻击 ; crypto, attacks, rsa → `classical-cipher-analysis`, `lattice-crypto-attacks`, `rsa-attack-techniques`, `a2sv-ssl-vuln`, `cero-tls-cert` ; 更多 17 个 grep 扩
- **C50 红队方法论与自动化**（38） 触发:红队方法论 / 自动化 ; team, offensive, engagement → `conducting-full-scope-red-team-engagement`, `designing-adversary-engagement-with-mitre-engage`, `emulating-cloud-attacks-with-stratus-red-team`, `cloudfail-cloud-origin`, `engagement-discipline` ; 更多 33 个 grep 扩

## 附

- primary 总数：197（磁盘总量 996，二级子类见 `/home/panjiahao/safe-range/attack_skills_for_agent/attack-skill-router/reference.md`，其余按需 grep，不主动加载）
- 维护：新增/删除 skill 后重跑 `python attack-skill-router/gen_router.py`（直扫仓库 + INDEX.md，无需 CSV；会覆写本文件与 reference.md）。**警示：当前脚本重跑会改写约 39/50 行 primary 挑选（与已提交表格存在漂移，因 INDEX.md/仓库快照与脚本排序逻辑版本不同步），重跑后必须 `git diff` 逐行人工复核再提交，禁止盲提交**；类别内排名按「方法论仓库优先级 + 工具名字序」，FORCE_PRIMARY 名单见脚本
- 路由 CLI 维护：skill 增删改后另需 `/home/panjiahao/safe-range/attack_skills_for_agent/scripts/search_skills --rebuild-index` 重建 `_index/` 向量索引，并跑 `/home/panjiahao/safe-range/attack_skills_for_agent/demo/router_demo.py` 复标 L1 top-k（门禁 Recall@20 ≥ 95%、L3 后 Recall@5 ≥ 85%，见 DESIGN.md §7）
- Claude Code 接入：跑 `bash /home/panjiahao/safe-range/attack_skills_for_agent/scripts/install_skill.sh` —— 它探测可用解释器写入 `.python-path`、把 `SKILL.md`（及能写的 `reference.md`/`MERGES.md`）**软链**进 `~/.claude/skills/attack-skill-router/`，最后从 `/tmp` 自检一次 CLI。软链而非复制 = 仓库即唯一真源，改完立刻生效、不会副本漂移；本文所有配套文件都写绝对路径，故**只有 SKILL.md 必须在 skill 目录里**，其余软链被沙箱拦下也不影响使用。改了本文件后无需重装
- 路由服务：`bash /home/panjiahao/safe-range/attack_skills_for_agent/scripts/router_server.sh start` 起常驻 HTTP 服务（约 5-10s 就绪，之后单次查询约 0.1s）。服务不是开机自启的，重启机器后需手动再 start；Agent 侧的第 0 步会在探测不到 `/health` 时自动拉起一次。改了 `search_skills.py` 的排序逻辑后必须 `restart`，常驻进程不会自动重载。pidfile 与日志在 `/home/panjiahao/safe-range/attack_skills_for_agent/.run/`，与 `.python-path` 一样已 gitignore（因机器而异）。**服务无鉴权**且默认绑 `0.0.0.0`，只适合可信隔离网段，收窄方式见 A 节「服务托管」
- 配套文件：`/home/panjiahao/safe-range/attack_skills_for_agent/attack-skill-router/reference.md`（本脚本生成的展开层）、`/home/panjiahao/safe-range/attack_skills_for_agent/attack-skill-router/MERGES.md`（重叠团合并裁决记录，已完成人工裁决 13 并 / 7 不并，非本脚本生成）、`/home/panjiahao/safe-range/attack_skills_for_agent/scripts/router_server.py`（HTTP 服务实现，仅标准库）、`/home/panjiahao/safe-range/attack_skills_for_agent/scripts/router_server.sh`（进程托管：start/stop/status/logs/curl）、`/home/panjiahao/safe-range/attack_skills_for_agent/scripts/search_skills`（本地 CLI 入口，无扩展名 bash 包装，兼作降级路径）、`/home/panjiahao/safe-range/attack_skills_for_agent/scripts/search_skills.py`（检索实现，`Router` 类被 CLI 与 HTTP 服务共用，排序不分叉）、`/home/panjiahao/safe-range/attack_skills_for_agent/DESIGN.md`（三层漏斗设计与评测数据）
