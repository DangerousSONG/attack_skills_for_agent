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
- 二级路由（本类超过 40 个，按子标签细分）：
  - 扫描/爬虫/综合（5 个）: `conducting-internal-reconnaissance-with-bloodhound-ce`, `performing-active-directory-vulnerability-assessment`, `smart-contract-vulnerabilities` …
  - 其他（45 个）: `abusing-shadow-credentials-for-privesc`, `attacking-entra-id-with-roadtools`, `conducting-internal-network-penetration-test` …

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

### C35 C2框架与远控（21 个 · TA0011）

- 触发词：C2框架 / 远控 ｜ EN: performing, infrastructure, building, red
- `building-c2-redirector-infrastructure` — Anthropic-Cybersecurity-Skills
- `building-red-team-c2-infrastructure-with-havoc` — Anthropic-Cybersecurity-Skills
- `exploiting-aws-with-pacu` — Anthropic-Cybersecurity-Skills
- `adaptix-c2-framework` — 改写
- `emp3r0r-c2` — 改写
- 更多 16 个: `grep -ril -e performing -e infrastructure /root/.claude/skills --include=SKILL.md`

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
- 二级路由（本类超过 40 个，按子标签细分）：
  - WAF 绕过（1 个）: `wafw00f-waf-detect`
  - 扫描/爬虫/综合（19 个）: `performing-asset-criticality-scoring-for-vulns`, `performing-timeline-reconstruction-with-plaso`, `recon-for-sec` …
  - 其他（42 个）: `collecting-open-source-intelligence`, `performing-ai-driven-osint-correlation`, `performing-cloud-asset-inventory-with-cartography` …

### C46 二进制漏洞利用与Pwn（46 个 · TA0002）

- 触发词：二进制漏洞利用 / Pwn ｜ EN: offensive, exploitation, penetration, ctf
- `coercing-authentication-with-coercer-petitpotam` — Anthropic-Cybersecurity-Skills
- `conducting-cloud-penetration-testing` — Anthropic-Cybersecurity-Skills
- `conducting-network-penetration-test` — Anthropic-Cybersecurity-Skills
- `angrop-rop-gen` — 改写
- `armscgen-shellcode` — 改写
- 二级路由（本类超过 40 个，按子标签细分）：
  - 认证与授权(JWT/会话/越权)（1 个）: `coercing-authentication-with-coercer-petitpotam`
  - 扫描/爬虫/综合（12 个）: `exploiting-ipv6-vulnerabilities`, `exploiting-smb-vulnerabilities-with-metasploit`, `exploiting-vulnerabilities-with-metasploit-framework` …
  - 其他（33 个）: `conducting-cloud-penetration-testing`, `conducting-network-penetration-test`, `performing-cloud-penetration-testing-with-pacu` …

### C10 API与业务逻辑攻击（54 个 · TA0001）

- 触发词：API / 业务逻辑攻击 ｜ EN: api, jwt, performing, graphql
- `conducting-api-security-testing` — Anthropic-Cybersecurity-Skills
- `exploiting-api-injection-vulnerabilities` — Anthropic-Cybersecurity-Skills
- `exploiting-idor-vulnerabilities` — Anthropic-Cybersecurity-Skills
- `astra-api-scan` — 改写
- `cariddi-crawler-secrets` — 改写
- 二级路由（本类超过 40 个，按子标签细分）：
  - 认证与授权(JWT/会话/越权)（23 个）: `exploiting-idor-vulnerabilities`, `exploiting-jwt-algorithm-confusion-attack`, `exploiting-oauth-misconfiguration` …
  - GraphQL（9 个）: `performing-graphql-introspection-attack`, `performing-graphql-security-assessment`, `performing-graphql-depth-limit-attack` …
  - 扫描/爬虫/综合（12 个）: `exploiting-api-injection-vulnerabilities`, `performing-api-fuzzing-with-restler`, `performing-osint-with-spiderfoot` …
  - 其他（10 个）: `conducting-api-security-testing`, `performing-api-security-testing-with-postman`, `performing-api-inventory-and-discovery` …

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
