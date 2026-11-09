---
name: rfc9113-ping-empty-frame-flood
description: 审计 HTTP/2 实现对强制应答帧（PING）与空载帧（DATA/HEADERS/CONTINUATION/PUSH_PROMISE）的处理代价是否有界——PING 强制逐帧 ACK 应答（CVE-2019-9512 Ping Flood：持续 PING 造成应答队列膨胀 CPU/内存耗尽）；空载帧不吃流控、单帧处理成本不对称（CVE-2019-9518 Empty Frame Flood，Envoy 安全团队致谢披露）；0 长度头字段内存驻留（CVE-2019-9516 Header Leak）；RFC 9113 §6.7/§6.1 给了语义没给成本护栏
rfc: RFC 9113 §6.7（PING）/ §6.1（DATA）/ §6.2（HEADERS）/ §6.6（PUSH_PROMISE）
license: Apache-2.0
---

# RFC 9113 §6.7/§6.1 PING 与空载帧成本不对称审计

## 1. 约束条款（原文出处）

RFC 9113 §6.7（要点）：
> 收到 PING 帧**必须**回一个 ACK 标志置位的 PING 应答（负载逐字节复制）；PING 不计入流控。

核心模式一句话：**PING 和空载帧的共同点是"线上几乎免费、线下强制工作"——PING 逐帧强制 ACK，空载 DATA/HEADERS 不计流控、却走完整帧解析管线。RFC 的应答义务是刚性的，护栏（每连接帧率上限、最小负载、节流）是实现的义务。审计对象是"强制工作量的斜率是否被夹住"。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| PF-1 | 单连接持续发送 PING（无 ACK 等待，背压打满） | 服务端无每连接 PING 频率上限，ACK 应答队列无界增长 → CVE-2019-9512 同款 |
| PF-2 | PING 出现在流 ID 非 0 的流上 | 未按连接错误处理 → §6.7 流定向校验缺失（指纹点） |
| PF-3 | 空载 DATA 帧洪水（len=0，无 END_STREAM） | 单帧处理成本 / 攻击带宽比 > 100x 且无帧率熔断 → CVE-2019-9518 同款 |
| PF-4 | 空载 HEADERS/CONTINUATION 帧洪水（len=0 无 END_HEADERS） | 同上 → 2019-9518 明确列出帧类 |
| PF-5 | 0 长度头名 + 0 长度头值（可选 Huffman 编码成 1 字节）持续发送 | 每次分配驻留至会话结束 → CVE-2019-9516 Header Leak 同款 |

判定方法：帧级客户端压测 PING 与空载帧各 baseline；观测 CPU、内存驻留、正常请求 P99；对照组为 idle 连接基线。

## 3. 攻击面猜想

- **CPU/内存耗尽 DoS**：PF-1/PF-3/PF-4 ——三类均为"攻击带宽 KB 级、处理成本 MB 级"的不对称消耗
- **连接保活滥用**：PF-1 ——PING 风暴让 idle 连接永远无法被回收（配合慢速连接占满连接表）
- **内存驻留泄漏**：PF-5 ——0 长度头触发分配但永不释放（会话生命周期内），多流并发放大

## 4. 关联历史 CVE

| CVE | 实现 | 根因 |
|---|---|---|
| **CVE-2019-9512** | 多实现全栈（RHSA-2019:2692/2745 系列批量修复） | Ping Flood：强制逐帧 ACK 义务 + 无频率上限 → 应答队列膨胀；Cloudflare 后续以 GOAWAY+ENHANCE_YOUR_CALM 缓解（Hyper adaptive window 误伤事件亦源于此） |
| **CVE-2019-9518** | 多实现（RHSA-2019:2925/2939/2955/3892；netty 4.1.13 全系列受影响） | 空帧洪水：DATA/HEADERS/CONTINUATION/PUSH_PROMISE 空载帧处理成本远超带宽占比；Envoy 安全团队致谢披露 |
| **CVE-2019-9516** | nginx（修复 commit 6dfbc8b1c211）、Node.js、IBM 系产品 | 0-Length Headers Leak：0 长度头名/值分配驻留至会话死；CVSS 7.5/6.5 |

## 5. 差分验证方法

对照组：修复版 nginx（1.17.x 2019-08 批次）；Cloudflare 边缘行为（高频 PING → GOAWAY ENHANCE_YOUR_CALM）作为"缓解标杆"。
对比字段：PF-1 熔断阈值（帧/秒）、PF-3/4 单帧处理成本比、PF-5 内存驻留斜率。
误报排除：实现有每连接帧率总上限且 PING/空载帧共享配额 → 判定通过；实现仅延迟 ACK 但队列有界 → 判定通过。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`slowhttptest-dos`（PING/空载帧慢速流）、`fuzzowski-network-fuzz`（帧类型/负载组合变异）
- 工具层（用什么打）：Python h2 帧级构造、CPU/内存采样
- 命中后动作：PF-1 确认 → 测单连接打满 ACK 产的阈值帧率 → 对照 Cloudflare ENHANCE_YOUR_CALM 阈值做缓解基线；PF-5 确认 → 测单会话驻留上限与多流放大系数
