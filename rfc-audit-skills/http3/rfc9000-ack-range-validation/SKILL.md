---
name: rfc9000-ack-range-validation
description: 审计 QUIC 实现对 ACK 帧确认范围的校验是否按 RFC 9000 §13.1/§21.4——确认未发送的包、ACK 范围畸形、乐观确认（Optimistic ACK）未检测即拥塞控制被欺骗的 DDoS 放大原语（关联 CVE-2025-4820/CVE-2025-4821 quiche < 0.24.4；ANRW 2025：16 个 Interop 实现中 11 个脆弱）
rfc: RFC 9000 §13.1 / §21.4（ACK 处理与乐观确认攻击）/ RFC 9002 §6（拥塞控制信号）
license: Apache-2.0
---

# RFC 9000 §13.1 ACK 确认范围校验审计

## 1. 约束条款（原文出处）

RFC 9000 §13.1（原文）：
> An endpoint SHOULD treat receipt of an acknowledgment for a packet it did not send as a connection error of type PROTOCOL_VIOLATION, if it is able to detect the condition.

RFC 9000 §21.4（原文要点）：
> An endpoint that acknowledges packets it has not received might cause a congestion controller to permit sending at rates beyond what the network supports. An endpoint MAY skip packet numbers when sending packets to detect this behavior. An endpoint can then immediately close the connection with a connection error of type PROTOCOL_VIOLATION.

IETF draft-chen-quic-logical-vuln-mitigations（补强）：ACK 范围在变更丢包恢复状态前**应当**校验为格式良好、无重叠、严格降序；同一包号不得因畸形 ACK 中被重复出现而反复变更确认状态。

核心模式一句话：**ACK 是拥塞控制的唯一反馈信号——确认"没发过的包"等于伪造"网络很好"的测量值，拥塞窗被顶到网络真实容量之上，服务端就成了自己流量放大 DoS 的共犯。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| AK-1 | 服务端已发送至 PN=N，发送 ACK 范围 [0, N+50]（确认未发送包） | 未关闭连接（PROTOCOL_VIOLATION） → 违规（quiche CVE-2025-4821 同款） |
| AK-2 | 构造重叠 / 重复包号 / 算术下溢的畸形 ACK 范围（多 First Range + 重叠 Gap） | 丢包恢复状态被反复变更 / 崩溃 → 违规；按 draft-chen 归一化处理 → 合规 |
| AK-3 | 乐观确认：按预测的包号节奏抢先确认尚未到达的包（ pacing 精细时序） | 发送速率被人为顶高且持续不检测 → 违规（RFC 要求跳号检测；§21.4 MAY 级但 Cloudflare 实证为必修） |
| AK-4 | 检测实现是否做**随机跳包号**并关联"幽灵包"（skip PN + dummy packet） | 无跳号机制 → 对 AK-3 无防御能力，标记为高风险缺口 |
| AK-5 | ACK 帧确认数秒后已判定丢失并重传的旧包时序组合，检测重复确认引发的拥塞窗回退异常 | cwnd 异常收缩/膨胀 → 记账违规 |

判定方法：aioquic 自写客户端精细控制 ACK 时序；测量服务端发送速率变化（对照组：无攻击基线速率）。

## 3. 攻击面猜想

- **拥塞控制欺骗 → 出站放大 DDoS**：AK-1/AK-3 ——单客户端把服务端发送速率顶高数倍，多客户端并发即成 DDoS 向量（Cloudflare 定性）
- **ACK 解析崩溃面**：AK-2 ——范围算术下溢/重叠是丢包恢复代码的 fuzz 高频区
- **带宽窃取**：攻击连接挤占同一出口的其他连接带宽（不公平竞争）

## 4. 关联历史 CVE

| CVE | 实现 | 根因 |
|---|---|---|
| **CVE-2025-4821** | Cloudflare quiche < 0.24.4 | 缺乏 ACK 范围校验：客户端可确认服务端从未发送的大范围包号（0-100），为乐观确认攻击铺路。修复：按最大已发包号强制校验并关闭违规连接 |
| **CVE-2025-4820** | Cloudflare quiche < 0.24.4 | 乐观确认（Optimistic ACK）攻击可被预测包号节奏绕过校验，虚报低 RTT 顶高发送速率。修复：动态 CWND 感知跳频 |
| ANRW 2025 论文（UCLouvain） | QUIC Interop Runner 16 实现中 **11 个**（quic-go、ngtcp2、mvfst、quiche、kwik、picoquic、aioquic、nginx、lsquic、quinn、s2n-quic 部分版本） | 不跳包号或不对 ACK 正确性做校验即对 OACK 攻击脆弱——该约束是 RFC 9002/9000 中"MAY 级条款实际是必修"的典型案例，生态级盲区 |

## 5. 差分验证方法

对照组：quiche ≥ 0.24.4（已修复）、quic-go 最新版（跳号 + 校验）。
对比字段：AK-1 是否关闭、AK-2 状态机一致性、AK-4 跳号机制存在性、攻击前后发送速率比。
误报排除：实现仅处理已发送范围内的 ACK（丢弃超出部分）且无法检测时属"无法检测"豁免，但须标记跳号防御缺失；只标记"确认未发送包被接受"与"无跳号无校验"。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`slowhttptest-dos`（速率欺骗时序模式）、`fuzzowski-network-fuzz`（ACK 范围语法 fuzz）
- 工具层（用什么打）：aioquic（ACK 帧字节级控制）、速率测量脚本
- 命中后动作：量化发送速率放大比 → 评估多连接 DDoS 可行性 → AK-2 崩溃路径单独最小化复现
