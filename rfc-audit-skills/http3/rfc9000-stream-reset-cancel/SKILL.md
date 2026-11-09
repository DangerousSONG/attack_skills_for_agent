---
name: rfc9000-stream-reset-cancel
description: 审计 QUIC 流重置/取消（RESET_STREAM/STOP_SENDING）的状态机校验与成本对称性是否按 RFC 9000 §3.4/§3.5——Final Size 不变量、状态错配未判 STREAM_STATE_ERROR、取消成本远低于服务端处理成本即 H3 版 Rapid Reset DoS 面（关联 CVE-2023-44487 HTTP/2 Rapid Reset 同模式，H3 栈被建议主动缓解；2025 年 MadeYouReset 变体证实该族持续演化）
rfc: RFC 9000 §3.4 / §3.5（Solicited State Transitions / Stream Final Size）/ §19.4 / §19.5（RESET_STREAM、STOP_SENDING 帧）/ RFC 9114 §4.1（H3 流取消语义）
license: Apache-2.0
---

# RFC 9000 §3.4/§3.5 流重置与取消成本对称性审计

## 1. 约束条款（原文出处）

RFC 9000 §3.4（要点）：
- RESET_STREAM / STOP_SENDING 用于请求对方中止流；接收方收到后对相应方向停止处理/释放资源；
- 对**已关闭 / 不存在的流**收到 RESET_STREAM，MUST 按 STREAM_STATE_ERROR 处理（除非该流从未存在过且允许静默丢弃的豁免场景）——状态机错配不是"无所谓"。

RFC 9000 §3.5 / §4.5（Final Size 不变量，要点）：
- 流一旦关闭，Final Size 即固定，不可变更；
- 收到 RESET_STREAM 的 Final Size 字段：小于已确认接收的字节数，或大于流量控制允许的上限，MUST 按 FLOW_CONTROL_ERROR 关闭连接。

RFC 9000 §19.4（RESET_STREAM 帧格式义务，要点）：
- Error Code（varint）+ Final Size（varint）两字段；帧只能出现在对该流有发送权的方向上。

核心模式一句话：**取消一个流的帧只有十几字节、发送方零等待——如果服务端对"开了又取消"的流仍付出完整解析/调度成本，并发上限就成了纸面数字。HTTP/2 Rapid Reset（CVE-2023-44487）已经证明这个成本不对称可以打垮 Google/Cloudflare/AWS；H3 把同样的取消机器（RESET_STREAM/STOP_SENDING）搬进 QUIC，该约束是 H3 栈的必答题。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| RS-1 | H3 场景下打开请求流并立即 RESET_STREAM/STOP_SENDING（canonical Rapid Reset 移植），测量服务端 CPU/分配速率 | 取消路径仍完整解析 HEADERS/QPACK/调度 → 成本不对称成立，标记 H3 Rapid Reset 面 |
| RS-2 | 对不存在/已关闭/只读状态的流注入 RESET_STREAM | 未判 STREAM_STATE_ERROR（沉默或错误释放活流资源）→ §3.4 违规 |
| RS-3 | 构造 Final Size 小于已收字节数、或大于流控上限的 RESET_STREAM | 未按 FLOW_CONTROL_ERROR 关闭 → §3.5/§4.5 违规（流控记账可被重置帧污染） |
| RS-4 | 变体节奏：批量开流-延迟批量取消（绕纯速率阈值）、超限开流依赖服务端逐条拒绝 | 无连接级工作预算/无强制关闭 → 2023-44487 变体 1/2 均未缓解 |
| RS-5 | STOP_SENDING 与 RESET_STREAM 交叉时序（双向同时取消、取消后补数据帧） | 半关闭状态机处理断言/资源泄漏 → 状态机缺陷 |

判定方法：aioquic 客户端帧级控制；对照组=攻击前后服务端每请求 CPU 与分配曲线；连接级指标（关闭率/工作预算）非单请求指标。

## 3. 攻击面猜想

- **H3 Rapid Reset DoS**：RS-1/RS-4 ——单连接打满服务端 CPU，并发上限形同虚设（H2 版已造成史上最大层 7 DDoS 之一）
- **流控记账污染**：RS-3 ——伪造 Final Size 干扰连接级流量控制账本，制造窗口通胀/紧缩
- **半关闭状态混淆**：RS-5 ——双向取消竞态下的资源释放漏洞（UAF/泄漏族，配合关闭态审计联动）

## 4. 关联历史 CVE

| CVE / 实证 | 实现 | 根因 |
|---|---|---|
| **CVE-2023-44487** | HTTP/2 全生态（nghttp2 <1.57、Netty、Envoy、Go x/net、nginx、Caddy、F5 等） | Rapid Reset：RST_STREAM 立即关闭流不占并发槽，服务端为每个被取消请求付出解析/调度成本。官方结论：无证据影响 H3，但**建议 H3 栈主动实施同类缓解**——本 Skill 即该建议的审计落地 |
| **MadeYouReset（2025 变体实证）** | HTTP/2 生态残留 | 只按"重置频率"缓解的实现被行为型变体绕过——教训：缓解必须在连接级工作预算，不能数帧 |
| RFC 9113 §5.1.2 模式复刻 | QUIC 流并发模型 | H2"只有 open/half-closed 计入并发上限"的结构性弱点在 QUIC 流状态机（§3）中同构存在，审计时按同模式检查 H3 栈 |

## 5. 差分验证方法

对照组：已实现连接级工作预算的 H3 栈（如带 rapid-reset 缓解的 nghttp3 新版本）、quic-go 最新版。
对比字段：RS-1 单连接请求处理速率上限、RS-2/RS-3 错误码正确性、RS-4 变体下是否强制 GOAWAY/关闭。
误报排除：服务端对已重置流立即释放且不产生应用层副作用属合规实现，RS-1 须以"服务端总工作量随取消率线性增长"为判定而非"允许取消"本身；HTTP 网关取消后仍需回源的架构标注"缓解在网关层"，审计对象转为网关。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`slowhttptest-dos`（H3 取消风暴时序模式）、`fuzzowski-network-fuzz`（RESET/STOP_SENDING 状态机 fuzz）
- 工具层（用什么打）：aioquic（帧级取消时序控制）、h3 load generator（RS-1 吞吐对照）、quic-interop-runner
- 命中后动作：测量单连接最大服务端成本注入速率 → 变体 1/2 复测缓解有效性 → RS-3 记账污染单独做流控账本差分 → 证据并入 DDoS 原语库
