---
name: rfc9113-h2c-upgrade-pseudoheader
description: 审计 h2c 升级协商与伪头校验——反向代理透传 Upgrade: h2c + HTTP2-Settings 即打开绕过认证/WAF 的原始字节隧道（CVE-2026-88008 Traefik GHSA-w4v4-9rw7-5326 CVSS 9.1 CWE-444+863，修复 PR #13797 剥离 h2c token；CVE-2026-88011 v2 同族；CVE-2026-73548 Envoy 通用升级走私）；HTTP2-Settings 不得随请求转发（RFC 9113 §3.2）、伪头字段规则（§8.3）是判定锚点；BishopFox h2csmuggler 2020 年已实证 HAProxy/Traefik/Nuster 默认透传
rfc: RFC 9113 §3.2（Starting HTTP/2 with Prior Knowledge / h2c Upgrade）/ §8.1.2.1（伪头字段规则）+ RFC 7540 §3.2
license: Apache-2.0
---

# RFC 9113 §3.2 h2c 升级协商与伪头校验审计

## 1. 约束条款（原文出处）

RFC 9113 §3.2（要点）：
> `HTTP2-Settings` 是**连接专用**头字段（hop-by-hop），不得由中介转发；h2c 升级仅允许发生在明文连接上。

RFC 9113 §8.1.2.1（要点）：
> 伪头字段（:method/:path/:authority/:scheme）必须出现在所有常规字段**之前**、且不得重复；常规字段不得使用":"前缀。

核心模式一句话：**h2c 升级的本质是"代理和服务器对协议状态的理解分叉"——代理以为自己在转发 HTTP/1.1，后端回了 101 之后整条连接变成代理看不见的原始隧道。RFC 给的两道闸（HTTP2-Settings 不转发、升级仅限明文）在 2026 年的 Traefik/Envoy 上仍然失守，说明这是持续复活的漏洞类，不是历史 CVE。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| HU-1 | 对目标发 HTTP/1.1 `Upgrade: h2c` + `HTTP2-Settings` + `Connection: Upgrade, HTTP2-Settings`（h2csmuggler 标准负载） | 代理/网关透传升级头至后端 → CVE-2026-88008 同款；收到 101 后连接变隧道 → 认证/WAF 全绕过 |
| HU-2 | 在 TLS 连接上发起 h2c 升级（规范禁止，多数客户端拒绝） | 代理仍转发 → BishopFox h2-over-TLS 走私通道成立 |
| HU-3 | H2 帧中含重复/乱序/常规字段冒号前缀伪头（`:path` 两次、`:x-foo: bar`） | 未按流错误/连接错误拒绝 → §8.1.2.1 伪头校验缺失（H2→H1 降级走私入口） |
| HU-4 | 升级请求本身带 body 且连接为 keep-alive | 升级前 body 未消耗即进入隧道 → 字节残留走私（CVE-2026-73548 Envoy 同类根因：升级载荷未等 101 确认即转发） |
| HU-5 | `HTTP2-Settings` 值非法（非合法 base64url / 解码后非法 SETTINGS 负载） | 后端仍回 101 → §3.2 升级载荷校验缺失（指纹+利用面） |

判定方法：h2csmuggler（BishopFox/Assetnote 双版本）扫描 + 手工构造升级请求；验证隧道建立后访问受保护路径是否 200。

## 3. 攻击面猜想

- **认证/WAF 全绕过**：HU-1/HU-2 ——101 之后代理退化为 TCP 隧道，所有中间件（BasicAuth/IPAllowList/RateLimit）失效
- **请求走私/租户串扰**：HU-4 ——共享 keep-alive 连接池中的字节残留可让下游租户收到他人响应（CVE-2026-73548 机制）
- **H2→H1 降级走私**：HU-3 ——伪头校验缺失在 H2 前端 + H1 后端架构中恢复 HTTP/1.1 语义分歧（与 `rfc9113-content-length-data-mismatch` 互补）

## 4. 关联历史 CVE

| CVE | 实现 | 根因 |
|---|---|---|
| **CVE-2026-88008** | Traefik v2.11.26–2.11.56 / v3.4.2–3.7.12（修复 3.7.13，GHSA-w4v4-9rw7-5326） | forwardedheaders 中间件原样透传 Upgrade token + HTTP2-Settings；101 后 net/http ReverseProxy 切隧道模式 → 中间件链全跳过。CVSS 9.1，CWE-444 + CWE-863 |
| **CVE-2026-88011** | Traefik v2 系（GHSA 同族） | 同上机制 v2 分支独立编号 |
| **CVE-2026-73548** | Envoy 通用升级路径 | 升级载荷在收到上游 101 确认前即被转发，上游视为 keep-alive 管线第二个请求 → 响应投毒；根因 pausedForGenericUpgrade 状态缺失 |
| BishopFox h2csmuggler 研究（2020） | HAProxy / Traefik / Nuster 默认透传；AWS ALB / NGINX / Apache / Squid / Envoy 可配置失误 | 首次系统性实证 h2c 走私类；工具与 Docker demo 公开 |

## 5. 差分验证方法

对照组：修复版 Traefik 3.7.13（剥离 h2c token + 删除 HTTP2-Settings）；AWS ALB/NGINX 默认配置（不透传）作为"正确默认标杆"。
对比字段：HU-1 是否透传、HU-2 TLS 上升级是否被代理自身终结、HU-3 伪头违规的错误码正确性。
误报排除：代理自身支持 h2c 并终结升级（返回自己的 101）→ 非透传，判定通过；后端不回 101 即升级链不成立 → 记"依赖后端配置"不记代理违规。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`h2csmuggler-http2`（h2c 升级自动化）、`smuggler-desync` / `http2smugl-desync`（升级载荷与降级走私组合）
- 工具层（用什么打）：h2csmuggler（BishopFox/Assetnote）、hyper-2 自定义客户端（TLS 上 h2c）
- 命中后动作：HU-1 确认 → 枚举隧道可达的受保护路径清单 → 验证 WAF 规则是否在隧道流量上生效 → 输出绕过证据链
