---
name: rfc9000-migration-congestion-window
description: 审计 QUIC 实现在连接迁移/NAT 重绑定时是否违反 RFC 9000 §8.1 反放大 3 倍限制与 §9.4 路径验证前限速义务——未验证新地址即全速发送即 UDP 反射放大与流量劫持攻击面（关联 CVE-2026-35191 OpenSSL QUIC 非验证模式记账错误违反 3x；TMA 2025：20% IPv4 服务器违反放大限制；HAProxy#3329 disable_active_migration 过度解释实证）
rfc: RFC 9000 §8.1 / §9.2 / §9.4（连接迁移与拥塞控制恢复）/ §18.2（disable_active_migration 语义）
license: Apache-2.0
---

# RFC 9000 §9.4 连接迁移拥塞控制与反放大审计

## 1. 约束条款（原文出处）

RFC 9000 §8.1（原文）：
> an endpoint MUST limit the amount of data it sends to the unvalidated address to three times the amount of data received from that address.

RFC 9000 §18.2（原文要点，disable_active_migration 传输参数）：
> even when a server sets disable_active_migration, it can still respond to packets from a new peer address. 该参数只禁止主动发起迁移，不免除响应新地址的义务。

RFC 9000 §9.2 / §9.4（要点）：
- 新路径 MUST 经 PATH_CHALLENGE / PATH_RESPONSE 验证后才视为可用；
- §9.4：路径验证前拥塞控制窗口 MUST 保持保守（初始窗口级别），验证后才可恢复旧路径拥塞状态——**拥塞窗恢复是验证后的奖励，不是默认**；
- 只有"最大包号的非探测帧"才能触发地址变更处理（探测帧：PATH_CHALLENGE/PATH_RESPONSE/_PADDING/NEW_CONNECTION_ID）。

核心模式一句话：**连接迁移把"往哪发"的决定权交给了对端报文——不验证新地址就全速发送，等于把服务端变成对任意声称地址的放大器；拥塞窗在验证前恢复到旧值，3x 闸门名存实亡。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| MI-1 | 完成握手后从伪造源地址发送单包（含非探测帧），测量服务端回包总量 | 回包 > 3× 收包量即违反 §8.1（TMA 2025 实测 20% IPv4 服务器违规） |
| MI-2 | 同一数据报携带多个 QUIC 包的场景（smuggled Initial），观察放大记账口径 | 按整数据报长记账而非按包实际占用 → 记账虚高违反 3x（CVE-2026-35191 同款） |
| MI-3 | NAT 重绑定（源端口变化）后，检测服务端是否在 PATH_CHALLENGE 验证前继续发送 STREAM 数据 | 未验证即发非 ACK/CRYPTO 数据 → 违反 §9.2/§9.4 |
| MI-4 | 设置 disable_active_migration 的目标上发起被动迁移 | 服务端完全无视新地址包导致连接卡死 → 违反 §18.2 响应义务（HAProxy#3329 实证）；相反方向：接受迁移不做路径验证 → 放大漏洞 |
| MI-5 | 检测验证前拥塞窗：新路径上测量服务端发送速率斜率 | 速率迅速爬升至旧路径 cwnd 水平而未经验证 → §9.4 违规 |

判定方法：双地址客户端（aioquic 自定义 + 源地址伪造 UDP socket）；对照组速率曲线 + 抓包统计放大比。

## 3. 攻击面猜想

- **UDP 反射放大**：MI-1/MI-2 ——握手完成后伪造地址即可让服务端向受害者全速发送，3x 记账错误把放大系数做高（OpenSSL QUIC 非验证模式实证）
- **流量劫持/重定向**：on-path 攻击者抢先改源地址并到达 → 服务端把流定向到攻击者地址（RFC 设计明示风险）
- **DoS 资源消耗**：PATH_CHALLENGE 状态表被海量伪造迁移灌爆（PATH validation 本身是攻击面的双面性，IETF QUIC WG 已披露协议级弱点）

## 4. 关联历史 CVE

| CVE / 实证 | 实现 | 根因 |
|---|---|---|
| **CVE-2026-35191** | OpenSSL QUIC（非验证模式） | 处理含多个 QUIC 包的数据报时把整报文长度计入未验证地址的放大额度，违反 3x 限制（Tenable 2026-09 披露，Linux 发行版未修补） |
| **TMA 2025（Buchet/Pelsser, UCLouvain）** | 45 万+ IPv4 实测 | 握手与迁移两类放大攻击：20% IPv4 服务器违反放大限制；支持迁移的服务器大多强制执行路径验证，但仍有部分直接回数据 |
| **HAProxy#3329**（2026-04，quic-interop-runner 实证） | HAProxy QUIC | 设置 disable_active_migration 后完全停止地址变更处理，NAT 重绑定即断连——参数语义过度解释，§18.2 义务被吞 |
| IETF QUIC WG 披露（2023-12，seemann.io） | quic-go / quiche / quicly 均受影响 | PATH_CHALLENGE/PATH_RESPONSE 验证状态可被诱导无界内存消耗——协议级弱点（实现侧已修，审计时对照检查） |

## 5. 差分验证方法

对照组：quic-go 最新版（严格 3x + 验证前保守 cwnd）、启用了验证模式的 OpenSSL QUIC。
对比字段：MI-1 放大比、MI-3 验证前数据帧、MI-5 速率斜率、MI-4 双向行为（既不能无视也不能轻信）。
误报排除：服务端发 PATH_CHALLENGE 期间仅发 ACK/CRYPTO 属于合规探测响应，不计入违规；负载均衡器以 CID 转发而忽略源地址的场景标注"迁移由 LB 终结"，审计对象转为 LB。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`slowhttptest-dos`（低速率迁移欺骗放大）、`fuzzowski-network-fuzz`（多包数据报/源地址组合 fuzz）
- 工具层（用什么打）：aioquic（自定义 PATH_CHALLENGE 时序）、源地址伪造 UDP socket、quic-interop-runner（NAT rebinding 场景）
- 命中后动作：量化放大比（>3x 即违规实证）→ 评估反射 DoS 可行性（伪造源 + 大响应流）→ MI-2 记账路径单独最小化复现
