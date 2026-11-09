---
name: rfc7541-hpack-decompression-accounting
description: 审计 HPACK 解码侧的资源记账模型——动态表 4KiB 上限管不住解码过程中的逐条目物化分配，索引引用放大（1 字节引用 → 全量头副本）与逐条目簿记开销叠加即成 HTTP/2 Bomb（CVE-2026-49975 Apache httpd / CVE-2026-47774 Envoy，nginx/IIS/Pingora 全栈，单连接 20 秒 32GB）；经典 HPACK Bomb 谱系 CVE-2016-6581（python-hpack）/CVE-2016-1544（nghttpd）/CVE-2025-53020（Apache 4000x）/CVE-2026-10725（Perl Protocol::HTTP2 头列表上限通告不执行）；RFC 7541 §7.3 被实证为规范缺陷——解码后大小与头字段数是两个独立上限，实现缺一不可
rfc: RFC 7541 §7.3（内存消耗，已实证缺陷条款）/ §4.1（条目尺寸记账）+ RFC 9113 §6.5.2（SETTINGS_MAX_HEADER_LIST_SIZE）
license: Apache-2.0
---

# RFC 7541 §7.3 / RFC 9113 §6.5.2 HPACK 解码资源记账审计

## 1. 约束条款（原文出处）

RFC 9113 §6.5.2（要点）：
> 端点通告 `SETTINGS_MAX_HEADER_LIST_SIZE` 后，**收到超出该限制的头列表必须视为流错误/连接错误**。

RFC 7541 §7.3（要点，已被实证为缺陷）：
> 攻击者可使端点耗尽内存。HPACK 通过 SETTINGS_HEADER_TABLE_SIZE 限制动态表内存……（仅此一句，认为问题已解决）。

核心模式一句话：**§7.3 用"压缩比"框定了内存风险，但 2026 年 HTTP/2 Bomb 证明这个模型是错的——单条几乎为空的头（解压缩尺寸极小、解压根不触发限制）也能让服务端为每个条目付簿记开销（池块、结构体、零终止拷贝），放大系数 68:1（IIS）到 5700:1（Envoy）。五个独立实现团队读了同一段规范犯了同一个错，说明审计点不在"有没有上限"，而在"上限管的是哪一层内存"。解码后总尺寸和头字段个数是两个独立上限，缺一即洞。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| HA-1 | 单头块内数千个"索引引用同一条大 cookie 条目"（1 字节/引用） | 服务端逐引用物化全量副本且头列表总量上限未拦截 → HTTP/2 Bomb 第 1 阶段成立 |
| HA-2 | 单头块内塞入数千个独立小头字段（总量低于解码尺寸上限） | 字段数无上限 → 簿记放大绕过尺寸上限（Calif 变体核心） |
| HA-3 | 头列表超过 SETTINGS_MAX_HEADER_LIST_SIZE 通告值 | 未按流错误拒绝 → §6.5.2 通告-执行不一致（CVE-2026-10725 同款：通告 65536 但解码器从不查） |
| HA-4 | Huffman 编码的极小线上负载展开为大字符串（压缩比 >100:1） | 展开后无字符串级上限 → 与 `rfc7541-hpack-decode-limit` 互补的字段级维度 |
| HA-5 | HA-1/HA-2 与流控持有（INITIAL_WINDOW_SIZE=0）组合 | 缓冲不可回收 → 全链成立，对照 CVE-2026-49975 复现表 |

判定方法：python-hpack 手工构造头块；观测每请求服务端内存增量；分别测"尺寸上限"与"字段数上限"两个维度。

## 3. 攻击面猜想

- **内存耗尽 DoS**：HA-1/HA-2/HA-5 ——五大实现 2026-06 同步中招的当前最高危 H2 攻击类
- **通告-执行分歧指纹**：HA-3 ——SETTINGS 宣称的值与实际执行不一致暴露栈与版本
- **字段数走私**：HA-2 ——WAF/网关按字节数限额时，海量小头字段可绕过审计规则

## 4. 关联历史 CVE

| CVE | 实现 | 根因 |
|---|---|---|
| **CVE-2026-49975 / CVE-2026-47774** | Apache httpd（mod_http2 <2.0.41）/ Envoy / nginx（1.29.8 max_headers 修复）/ IIS / Cloudflare Pingora（RHSB-2026-007，2026-06-02 Calif 披露，OpenAI Codex 辅助发现） | 逐条目簿记开销不在动态表预算内 + 零窗口持有钉住内存；放大 68:1–5700:1；约 88 万公网站点暴露 |
| **CVE-2026-10725** | Perl Protocol::HTTP2 <1.13 | 入向 HPACK 无头列表上限：SETTINGS 通告 MAX_HEADER_LIST_SIZE 默认 65536 但解码路径从不查询；CONTINUATION 缓冲无界累加 |
| **CVE-2025-53020** | Apache httpd（Gal Bar Nahum，~4000x 放大） | HTTP/2 Bomb 前奏：压缩头展开与驻留的放大实现 |
| **CVE-2016-6581 / CVE-2016-1544** | python-hpack <2.3.0 / nghttpd、nghttp、libnghttp2_asio | 经典 HPACK Bomb：动态表塞满大条目后数千次引用，16KB 线上 → 64MB 解码；nghttp2 库本身不受影响的边界案例（应用层义务） |

## 5. 差分验证方法

对照组：nginx ≥1.29.8（max_headers 字段数上限）与 mod_http2 ≥2.0.41（修复版）作为双上限标杆。
对比字段：HA-1 单引用物化成本、HA-2 字段数上限值、HA-3 通告-执行一致性、HA-5 与流控持有的组合放大系数。
误报排除：实现字段数上限极高（如 2^20）但仍存在 → 判定违规（拒绝服务下限过低才算数）；实现按解码后尺寸限额且字段数受尺寸间接约束（大字段挤占）→ 对 HA-1 判定通过但对 HA-2 仍须实测。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（HPACK 头块变异）、`dharma-grammar-fuzz`（条目数/引用模式组合生成）
- 工具层（用什么打）：python-hpack 手工编码、CVE-2026-49975 公开复现工程（razureink/cve-2026-49975-http2bomb_reproduction）做对照基线
- 命中后动作：HA-2 确认 → 测"字段数 × 条目大小"放大矩阵 → 对照五大实现修复表定级 → 与 `rfc9113-flow-control-window-stall` 组合测全链
