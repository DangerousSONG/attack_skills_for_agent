---
name: rfc9113-flow-control-window-stall
description: 审计 HTTP/2 流控窗口（WINDOW_UPDATE）实现的对称性与有界性——窗口操纵强制服务端以 1 字节粒度排队即 Data Dribble（CVE-2019-9511，CVSS 7.5）；零增量 WINDOW_UPDATE 属非法帧，服务端逐帧回 RST_STREAM 即 MadeYouReset 资源消耗链（CVE-2025-5115 Jetty GHSA-mmxm-8w33-wc4h）；INITIAL_WINDOW_SIZE=0 + 涓流 WINDOW_UPDATE 的 Slowloris 持有是 HTTP/2 Bomb（CVE-2026-49975/47774）的半条链；RFC 9113 §5.2/§6.9 给了窗口语义但"stalled 流生命周期预算"是留白
rfc: RFC 9113 §5.2（流控原则）/ §6.9（WINDOW_UPDATE）/ §6.5.2（INITIAL_WINDOW_SIZE）
license: Apache-2.0
---

# RFC 9113 §5.2/§6.9 流控窗口操纵与 stalled 流审计

## 1. 约束条款（原文出处）

RFC 9113 §6.9（要点）：
> WINDOW_UPDATE 的增量为 0 必须按**流错误**（PROTOCOL_ERROR）处理；窗口仅可由 WINDOW_UPDATE 增大，发送端不得依赖对端窗口收缩以外的行为。

RFC 9113 §5.2（要点）：
> 流控仅适用于 DATA 帧；HEADERS 不受流控约束。

核心模式一句话：**H2 流控是"发送方看接收方脸色"的信用系统——攻击者反着用：开足信用让服务端拼命产数据，然后以最小粒度（甚至 0 增量非法帧）回收或赖账，服务端的队列就替攻击者存着内存。RFC 定义了非法帧的处置（0 增量 → 流错误），但"一个 stalled 流能赖多久"没有答案，这正是 2026 年 HTTP/2 Bomb 能一次打穿五大实现的根。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| FW-1 | 多流请求大对象，每流仅以 1 字节 WINDOW_UPDATE  trickle 回收信用 | 服务端按最小粒度切片排队、CPU/内存随流数放大 → CVE-2019-9511 同款 Data Dribble |
| FW-2 | 发送增量为 0 的 WINDOW_UPDATE（流级 + 连接级） | 未按流错误回 RST_STREAM/未断连 → §6.9 非法帧处置缺失（兼作指纹） |
| FW-3 | SETTINGS 宣告 INITIAL_WINDOW_SIZE=0，随后极慢 trickle | 服务端无限期持有已分配的响应缓冲 → HTTP/2 Bomb hold 半链成立 |
| FW-4 | stalled 流持续期间叠加新请求 | 服务端无 stalled 流生命周期预算/无上限 → 缓冲可无限累积 |
| FW-5 | 窗口溢出构造：发送超出可用窗口的 DATA | 未按 FLOW_CONTROL_ERROR 断开 → §5.2 窗口记账缺失 |
| FW-6 | 连接级窗口耗尽但流级窗口充足（或反之） | 流/连接两级窗口记账不一致 → 记账缺陷 |

判定方法：h2 客户端多流 + 窗口操纵脚本；观测服务端内存驻留、切片粒度、stalled 流回收时间；对照组为正常窗口基线。

## 3. 攻击面猜想

- **内存耗尽 DoS**：FW-3/FW-4 ——与 HPACK 放大链组合即 CVE-2026-49975 全链（与本层 `rfc7541-hpack-decompression-accounting` 交叉引用）
- **CPU 耗尽 DoS**：FW-1 ——1 字节切片把发送路径变 N 倍系统调用
- **RST 风暴资源消耗**：FW-2 批量重复 ——服务端每帧一个 RST_STREAM，Jetty MadeYouReset 实证（发非法帧 → 服务端回 RST → 不计并发上限 → 短时钟高速造流）

## 4. 关联历史 CVE

| CVE | 实现 | 根因 |
|---|---|---|
| **CVE-2019-9511** | 多实现（Data Dribble，2019-08 CERT 批次） | 窗口操纵 + 优先级操纵强制服务端 1 字节排队；CVSS 7.5 / CWE-400 |
| **CVE-2025-5115** | Eclipse Jetty ≤9.4.57/≤10.0.25/≤11.0.25/≤12.0.21（GHSA-mmxm-8w33-wc4h） | 客户端发 0 增量 WINDOW_UPDATE 等非法帧 → 服务端回 RST_STREAM 消耗资源；MadeYouReset 变体，RFC 9113 §6.9 的合规处置被武器化 |
| **CVE-2026-49975 / CVE-2026-47774** | Apache httpd（mod_http2 <2.0.41）/ Envoy（RHSB-2026-007） | HTTP/2 Bomb：HPACK 条目记账放大 + 零窗口 Slowloris 持有；nginx 1.29.8 以 max_headers 修复（未分配 CVE）；IIS/Envoy/Pingora 当时无补丁 |
| 谱系 | CVE-2016-1546（Apache worker 饿死）等 | Slowloris 型持有自 2016 年起反复复发，本 Skill 标记为**与压缩层审计组合必查项** |

## 5. 差分验证方法

对照组：修复版 nginx（1.29.8+，max_headers + stalled 流预算）；Cloudflare 边缘（stalled 流强回收）作为标杆。
对比字段：FW-1 切片粒度下限、FW-3 stalled 流最大存活时长、FW-2 错误码正确性、FW-5/FW-6 记账一致性。
误报排除：实现有 stalled 流全局上限（如连接内存配额）且触发即 GOAWAY → 判定通过；0 增量帧处置正确但资源消耗与修复版相当 → 判定通过。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`slowhttptest-dos`（Slowloris 型窗口持有）、`fuzzowski-network-fuzz`（WINDOW_UPDATE 增量/时机变异）
- 工具层（用什么打）：Python h2 窗口操纵脚本、内存驻留采样
- 命中后动作：FW-3+FW-4 确认 → 与 HPACK 放大探测组合复测 HTTP/2 Bomb 全链 → 测单连接最大可钉住内存 → 对照 CVE-2026-49975 放大系数表定级
