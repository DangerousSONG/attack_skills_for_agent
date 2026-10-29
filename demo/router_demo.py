# -*- coding: utf-8 -*-
"""三层漏斗 skill 路由 demo：L1 embedding top-k 粗筛 -> L2 RRF 融合召回 -> L3 cross-encoder 精排。

方案见仓库根目录 DESIGN.md（对应 SKILL-PLAN.md 第三章的最小验证版）。
评测集为仓库评测 harness 中的 107 条金标查询（运行时从 git blob 提取，避免依赖工作区文件状态）。

用法:
    python router_demo.py                  # 全量评测 (L1 取余弦 top-50)
    python router_demo.py --l1-topk 100    # 放宽 L1 候选预算
    python router_demo.py --no-l3          # 消融: 只跑 L1+L2
    python router_demo.py --grid           # 网格搜索 l1-topk x l2-topn, 结果表写入 DESIGN.md §2.3
"""
import argparse
import ast
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time

import numpy as np

np.set_printoptions(threshold=np.inf)  # 日志中完整输出向量, 不显示 ... 省略号

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'demo', 'cache')     # 可重建的中间产物: embedding/CE 分数/网格结果
REPORT = os.path.join(ROOT, 'demo', 'report')   # 评测报告 report_*.json 的落盘目录
LOGDIR = os.path.join(ROOT, 'demo', 'logs')
HARNESS = 'scripts/eval_recall.py'
REGISTERED = {'attack-skill-router', 'engagement-discipline', 'java-deserialization-gadget-selector'}
# 语料侧 994 条 description 100% 含中文(每条尾部都有中文「信号:…」标签), 纯英文模型必然跨语言失配:
# bge-small-en 下全库相似度被压缩进 0.55~0.72 窄带, 金标最低分 0.536 落在背景分布 p5 以下,
# 任何阈值都筛不掉东西(零丢失时仅剔除 9.5%)。故默认用多语言 bge-m3(1024 维)。
EMB_MODEL = 'BAAI/bge-m3'  # 默认多语言模型(语料中英混排); 可用 --emb-model 切换(如 BAAI/bge-small-en-v1.5)
RERANK_MODEL = 'BAAI/bge-reranker-v2-m3'
RRF_K0 = 60  # reciprocal rank fusion 平滑常数, 越大越弱化头部名次的权重
GRID_TOPK = '20,30,50,80,120'  # --grid 默认扫描的 l1-topk 取值
GRID_TOPN = '5,10,15,20,30'    # --grid 默认扫描的 l2-topn 取值
GRID_KS = (1, 3, 5, 10, 20)    # 网格表固定口径, 不随 --ks 变化, 保证多次运行可比
GRID_BEGIN = '<!-- GRID:BEGIN 由 `python demo/router_demo.py --grid` 自动生成, 标记块内勿手改 -->'
GRID_END = '<!-- GRID:END -->'


def model_path(hub_id):
    """优先用 demo/models/ 下的本地副本(见 fetch_models.sh), 否则回落到 hub id。"""
    local = os.path.join(ROOT, 'demo', 'models', *hub_id.split('/'))
    return local if os.path.isdir(local) else hub_id


_LOGF = [None]


def log(msg):
    """数据生成/变化追踪: 打印到 stdout 并写入 demo/logs/ 下的本次运行日志。"""
    line = '[%s] %s' % (time.strftime('%H:%M:%S'), msg)
    print(line)
    if _LOGF[0]:
        _LOGF[0].write(line + '\n')
        _LOGF[0].flush()


def log_sample(title, items, limit=10):
    """把当前处理的数据样例(前 limit 行)完整写入日志文件, 不截断。

    只写文件不刷 stdout, 避免终端被大数据淹没; 行数受 limit 控制, 单行内容完整输出。
    """
    if not _LOGF[0]:
        return
    items = list(items)
    _LOGF[0].write('[%s] 数据样例: %s (共 %d 行, 展示前 %d 行)\n'
                   % (time.strftime('%H:%M:%S'), title, len(items), min(limit, len(items))))
    for it in items[:limit]:
        s = it if isinstance(it, str) else repr(it)
        _LOGF[0].write('    %s\n' % s.replace('\n', '\\n'))
    _LOGF[0].flush()


# ---------------------------------------------------------------- 数据加载
def load_queries():
    """从 git HEAD 的评测 harness 中提取 QUERIES 常量 (query, [gold slugs])。"""
    src = subprocess.run(['git', 'show', 'HEAD:' + HARNESS], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', '') == 'QUERIES' for t in node.targets):
            val = ast.literal_eval(node.value)
            log('数据生成: QUERIES 提取完成, %d 条查询 (source=git blob %s)' % (len(val), HARNESS))
            log_sample('QUERIES 原始数据 (query, gold_slugs)',
                       ['%r -> %r' % (q, g) for q, g in val])
            return val
    raise RuntimeError('QUERIES not found in %s' % HARNESS)


def load_skills():
    """遍历仓库 SKILL.md, 返回 {slug: (name, description)}, 口径与评测 harness 一致。"""
    docs = {}
    for dp, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ('.git', 'demo') and not d.startswith('_')]
        if 'SKILL.md' not in files:
            continue
        rel = os.path.relpath(dp, ROOT).replace(os.sep, '/')
        parts = rel.split('/')
        if parts[0] in REGISTERED or len(parts) < 2 or parts[0] == 'scripts':
            continue
        s = io.open(os.path.join(dp, 'SKILL.md'), encoding='utf-8', errors='replace').read()
        fm = re.search(r'^---\n(.*?)\n---', s, re.S)
        if not fm:
            continue
        dm = re.search(r'^description:\s*(.+)$', fm.group(1), re.M)
        nm = re.search(r'^name:\s*(.+)$', fm.group(1), re.M)
        if not dm:
            continue
        docs[parts[-1]] = (nm.group(1).strip() if nm else parts[-1], dm.group(1).strip())
    log('数据生成: skill 语料加载完成, %d 条 (slug -> name/description)' % len(docs))
    log_sample('skill 语料 (slug | name | description)',
               ['%s | %s | %s' % (s, docs[s][0], docs[s][1]) for s in sorted(docs)], limit=20)
    return docs


# ---------------------------------------------------------------- L1 embedding 粗筛
def build_l1_embeddings(slugs, texts, refresh, emb_model):
    from sentence_transformers import SentenceTransformer
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, 'l1_embs_%s.npz' % emb_model.replace('/', '__'))
    model = SentenceTransformer(model_path(emb_model))
    if not refresh and os.path.exists(path):
        z = np.load(path)
        if list(z['slugs']) == slugs:
            print('[L1] 复用缓存 embedding: %s (%d x %d)' % (path, len(slugs), z['emb'].shape[1]))
            log('数据生成: L1 全库 embedding 取自缓存 %s, shape=%s' % (path, z['emb'].shape))
            log_sample('缓存 embedding 完整向量样例 (slug: 全维向量)',
                       ['%s: %s' % (s, np.round(v, 6).tolist())
                        for s, v in zip(z['slugs'], z['emb'])])
            return z['emb'], model
    print('[L1] 编码全库 %d 条 (model=%s) ...' % (len(slugs), emb_model))
    emb = model.encode(texts, batch_size=64, normalize_embeddings=True,
                       show_progress_bar=True).astype('float32')
    np.savez_compressed(path, slugs=np.array(slugs), emb=emb)
    log('数据落盘: L1 全库 embedding 编码完成 shape=%s, 写入 %s' % (emb.shape, path))
    log_sample('新编码 embedding 完整向量样例 (slug: 全维向量)',
               ['%s: %s' % (s, np.round(v, 6).tolist()) for s, v in zip(slugs, emb)])
    return emb, model


def slugs_set(mask, slugs):
    return {s for s, m in zip(slugs, mask) if m}


def rank_matrix(S):
    """相似度矩阵 -> 名次矩阵 (0 = 最高分), 供 RRF 融合使用。"""
    order = np.argsort(-S, axis=1)
    rank = np.empty_like(order)
    for i in range(order.shape[0]):
        rank[i, order[i]] = np.arange(order.shape[1])
    return rank


# ---------------------------------------------------------------- L2 TF-IDF
def build_l2(corpus, queries):
    from scipy.sparse import hstack
    from sklearn.feature_extraction.text import TfidfVectorizer
    vec_w = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    vec_c = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5), min_df=1)
    X = hstack([vec_w.fit_transform(corpus), vec_c.fit_transform(corpus)])
    Q = hstack([vec_w.transform(queries), vec_c.transform(queries)])
    return (Q @ X.T).toarray()


# ---------------------------------------------------------------- L3 reranker
def build_l3():
    try:
        from sentence_transformers import CrossEncoder
    except ImportError:  # pragma: no cover
        from sentence_transformers.cross_encoder import CrossEncoder
    return CrossEncoder(model_path(RERANK_MODEL))


def ce_key(query, doc):
    """CE 分数缓存的键: 按 pair 文本 hash, 语料/查询增删后旧分数仍然有效。"""
    return hashlib.md5(('%s\x00%s' % (query, doc)).encode('utf-8')).hexdigest()


# ---------------------------------------------------------------- 评测
def recall_at(ranking, gold, ks):
    out = {}
    for k in ks:
        out[k] = float(any(g in ranking[:k] for g in gold))
    return out


# ---------------------------------------------------------------- 网格搜索
def mrr(ranking, gold):
    """首个金标的倒数名次; 比 recall@k 更能反映头部排序质量。"""
    for r, s in enumerate(ranking):
        if s in gold:
            return 1.0 / (r + 1)
    return 0.0


def metric_bundle(rank, gold, nq):
    """一次算完三类口径: 召回率(recall@k) / 准确率(hit@1=r@1, P@3) / 排序质量(MRR)。"""
    gs = [set(g) for g in gold]
    out = {'r@%d' % k: sum(bool(gs[i] & set(rank[i][:k])) for i in range(nq)) / nq
           for k in GRID_KS}
    out['p@3'] = sum(len(gs[i] & set(rank[i][:3])) / 3.0 for i in range(nq)) / nq
    out['mrr'] = sum(mrr(rank[i], gs[i]) for i in range(nq)) / nq
    return out


def run_grid(args, nq, qtext, gold, docs, slugs, fused, order_l1, t_l1, t_l2):
    """遍历 l1-topk x l2-topn, 产出召回/准确率/成本网格表, 写入日志、cache/grid_*.json 与 DESIGN.md。"""
    topks = sorted({min(int(x), len(slugs)) for x in args.grid_topk.split(',')})
    topns = sorted({int(x) for x in args.grid_topn.split(',')})
    cells = [(K, n) for K in topks for n in topns if n <= K]
    log('网格搜索: l1_topk=%s x l2_topn=%s -> %d 个有效 cell (约束 topn<=topk)'
        % (topks, topns, len(cells)))

    # L1 存活集与 L2 排序只依赖 topk -> 每个 topk 算一次, 该列所有 topn 共用。
    l2_by_k, l1rec = {}, {}
    for K in topks:
        pool = [order_l1[i][:K] for i in range(nq)]
        l2_by_k[K] = [[slugs[j] for j in pool[i][np.argsort(-fused[i][pool[i]])]]
                      for i in range(nq)]
        l1rec[K] = sum(any(g in set(l2_by_k[K][i]) for g in gold[i]) for i in range(nq)) / nq
        log('网格搜索: topk=%d 存活集与 L2 RRF 排序完成, 存活集召回=%.4f' % (K, l1rec[K]))

    # CE 分数是 (query, doc) 文本的纯函数, 与 topk/topn 无关 -> 全网格共用一份, 并按文本 hash
    # 落盘缓存: 一次打分 10 分钟量级, 缓存后调整选点规则/扩网格重跑只需几秒。
    need = sorted({(i, s) for K, n in cells for i in range(nq) for s in l2_by_k[K][i][:n]})
    naive = sum(n for _, n in cells) * nq
    texts = {p: (qtext[p[0]], '%s %s' % (docs[p[1]][0], docs[p[1]][1])) for p in need}
    log('网格搜索: 待打分 CE pair 去重后 %d (平均 %.1f/query), 不去重需 %d 次, 省 %.1fx'
        % (len(need), len(need) / nq, naive, naive / max(len(need), 1)))
    cpath = os.path.join(CACHE, 'ce_scores_%s.json' % RERANK_MODEL.replace('/', '__'))
    blob = json.load(io.open(cpath, encoding='utf-8')) if os.path.exists(cpath) \
        else {'meta': {}, 'scores': {}}
    todo = [p for p in need if ce_key(*texts[p]) not in blob['scores']]
    log('网格搜索: CE 分数缓存 %s 命中 %d/%d, 本次需打分 %d'
        % (os.path.basename(cpath), len(need) - len(todo), len(need), len(todo)))
    if todo:
        ce = build_l3()
        t0 = time.time()
        vals = ce.predict([texts[p] for p in todo], batch_size=args.ce_batch,
                          show_progress_bar=True)
        ce_s = time.time() - t0
        for p, v in zip(todo, vals):
            blob['scores'][ce_key(*texts[p])] = float(v)
        blob['meta'] = {'rerank_model': RERANK_MODEL, 'batch_size': args.ce_batch,
                        'pairs_scored': len(todo), 'seconds': ce_s,
                        'ms_per_pair': 1000 * ce_s / len(todo),
                        'updated': time.strftime('%Y-%m-%d %H:%M:%S')}
        with io.open(cpath, 'w', encoding='utf-8') as f:
            json.dump(blob, f)
        log('数据落盘: CE 分数缓存写入 %s (累计 %d 条, %d bytes)'
            % (cpath, len(blob['scores']), os.path.getsize(cpath)))
    meta = blob['meta']
    ms_pair = float(meta.get('ms_per_pair', 0.0))
    ce_note = '本次 %d pair / %.1fs 实测' % (meta.get('pairs_scored', 0), meta.get('seconds', 0.0)) \
        if todo else '取自缓存 meta：%s 实测 %d pair / %.1fs' % (
            meta.get('updated', '?'), meta.get('pairs_scored', 0), meta.get('seconds', 0.0))
    scores = {p: blob['scores'][ce_key(*texts[p])] for p in need}
    log_sample('网格搜索 CE 打分 (query_idx | slug | score)',
               ['%d | %s | %.4f' % (i, s, scores[(i, s)]) for i, s in need], limit=50)
    log('网格搜索: CE 分数就绪 %d pair, 成本口径 %.1fms/pair (%.1f pair/s) [%s]'
        % (len(need), ms_pair, 1000 / ms_pair if ms_pair else 0, ce_note))

    ms_l1, ms_l2 = 1000 * t_l1 / nq, 1000 * t_l2 / nq
    rows = []
    for K, n in cells:
        l2r = l2_by_k[K]
        # L3 = 在 L2 top-n 内按 CE 分重排, n 名之后保持 L2 序 (与单点路径同口径)
        l3r = [sorted(l2r[i][:n], key=lambda s: -scores[(i, s)]) + l2r[i][n:]
               for i in range(nq)]
        m2, m3 = metric_bundle(l2r, gold, nq), metric_bundle(l3r, gold, nq)
        rows.append({'topk': K, 'topn': n, 'l1_recall': l1rec[K], 'l2': m2, 'l3': m3,
                     'pairs_q': float(n), 'l3_ms_q': n * ms_pair,
                     'e2e_ms_q': ms_l1 + ms_l2 + n * ms_pair})
        log('网格搜索: cell topk=%d topn=%d | L1存活集召回=%.4f | L2 hit@1=%.4f r@5=%.4f'
            ' | L3 hit@1=%.4f r@3=%.4f r@5=%.4f r@10=%.4f r@20=%.4f p@3=%.4f MRR=%.4f'
            ' | pair/q=%d L3ms/q=%.0f e2ems/q=%.0f'
            % (K, n, l1rec[K], m2['r@1'], m2['r@5'], m3['r@1'], m3['r@3'], m3['r@5'],
               m3['r@10'], m3['r@20'], m3['p@3'], m3['mrr'], n, n * ms_pair,
               ms_l1 + ms_l2 + n * ms_pair))
        log_sample('网格搜索 cell(topk=%d,topn=%d) L3 排序 top-10' % (K, n),
                   ['%s -> %s' % (qtext[i], l3r[i][:10]) for i in range(nq)], limit=10)

    # 选点(字典序, 不引入人工权重; 规则原文同步写进 DESIGN.md):
    #   0) 硬约束: L1 存活集召回=100%(端到端上限, 不可交易) + §1 门禁 R@20>=95% / R@5>=85%
    #   1) 主指标 L3 R@5 最大 —— 模式 b 实际返回 5 条, 返回集召回就是产品契约
    #   2) tie-break: L3 hit@1 最大 (top-1 准确率)
    #   3) tie-break: L3 R@10 最大
    #   4) tie-break: CE pair/查询最小 —— 唯一随超参变化的真实成本(L1/L2 延迟与两超参无关);
    #      生产 CE 走 GPU 批量服务, 10 pair 与 5 pair 墙钟几乎相同, 故成本只做并列时的 tie-break
    #   5) tie-break: l1-topk 最小 —— 同质量下剪枝更狠, 语料涨到 1w 时相对余量更大
    # 1~3 均带 1 条查询(1/nq)的噪声带: 指标取值天然是 1/nq 的整数倍, 差 1 条不算真实优劣。
    eps = 1.0 / nq

    def band(cands, val):
        """在 cands 里取 val 最大的噪声带内子集 (差 <=1 条查询视为并列)。"""
        top = max(val(r) for r in cands)
        return [r for r in cands if top - val(r) <= eps + 1e-9]

    elig = [r for r in rows if r['l1_recall'] >= 1 - 1e-9
            and r['l3']['r@20'] >= 0.95 and r['l3']['r@5'] >= 0.85]
    if not elig:
        log('网格搜索: 无 cell 满足硬约束, 退回全集选点 (检查 --grid-topk/--grid-topn 范围)')
        elig = rows
    log('网格搜索: 硬约束(L1 存活集召回=100%% + L3 R@20>=95%% + R@5>=85%%)后剩 %d/%d 个 cell'
        % (len(elig), len(rows)))
    s1 = band(elig, lambda r: r['l3']['r@5'])
    s2 = band(s1, lambda r: r['l3']['r@1'])
    tied = band(s2, lambda r: r['l3']['r@10'])
    pmin = min(r['pairs_q'] for r in tied)
    cheap = [r for r in tied if r['pairs_q'] == pmin]
    best = min(cheap, key=lambda r: r['topk'])

    def dominated(r):
        return any(o is not r and o['l3']['r@5'] >= r['l3']['r@5']
                   and o['pairs_q'] <= r['pairs_q']
                   and (o['l3']['r@5'] > r['l3']['r@5'] + eps or o['pairs_q'] < r['pairs_q'])
                   for o in rows)
    pareto = [r for r in elig if not dominated(r)]
    log('网格搜索: 字典序收敛 R@5 并列 %d 个 -> hit@1 并列 %d 个 -> R@10 并列 %d 个 '
        '-> 最低成本 pair/q=%.0f 剩 %d 个 => 最优 topk=%d topn=%d; Pareto 前沿(R@5 vs 成本) %d 个'
        % (len(s1), len(s2), len(tied), pmin, len(cheap), best['topk'], best['topn'],
           len(pareto)))
    log('网格搜索: 最优 cell 指标 L1存活集召回=%.4f | L3 hit@1=%.4f r@3=%.4f r@5=%.4f r@10=%.4f'
        ' r@20=%.4f p@3=%.4f MRR=%.4f | pair/q=%d e2ems/q=%.0f'
        % (best['l1_recall'], best['l3']['r@1'], best['l3']['r@3'], best['l3']['r@5'],
           best['l3']['r@10'], best['l3']['r@20'], best['l3']['p@3'], best['l3']['mrr'],
           best['pairs_q'], best['e2e_ms_q']))
    log_sample('网格搜索 与最优 cell 统计并列的候选 (topk,topn)',
               ['%d,%d' % (r['topk'], r['topn']) for r in cheap])

    body = grid_markdown(rows, best, pareto, cheap, len(elig), nq, len(slugs), ms_l1, ms_l2,
                         ms_pair, ce_note, len(need), args)
    print()
    for line in body.split('\n'):
        log(line)

    gpath = os.path.join(CACHE, 'grid_%s.json' % time.strftime('%Y%m%d-%H%M%S'))
    payload = {'timestamp': time.strftime('%Y%m%d-%H%M%S'), 'n_queries': nq,
               'n_skills': len(slugs), 'params': vars(args),
               'emb_model': args.emb_model, 'rerank_model': RERANK_MODEL, 'rrf_k0': RRF_K0,
               'cost_model': {'ms_l1_per_query': ms_l1, 'ms_l2_per_query': ms_l2,
                              'ms_per_ce_pair': ms_pair, 'ce_pairs_dedup': len(need),
                              'ce_pairs_naive': sum(n for _, n in cells) * nq,
                              'ce_measure': ce_note},
               'selection': {
                   'rule': 'hard(L1 survivor recall=100% & L3 R@20>=95% & R@5>=85%) '
                           '-> max L3 R@5 (band<=1/nq) -> max L3 hit@1 (band) '
                           '-> max L3 R@10 (band) -> min CE pairs/query -> min l1_topk',
                   'primary_metric': 'l3_r@5', 'noise_band_pp': 100 * eps,
                   'best': [best['topk'], best['topn']],
                   'eligible_cells': [[r['topk'], r['topn']] for r in elig],
                   'band_r5_cells': [[r['topk'], r['topn']] for r in s1],
                   'band_hit1_cells': [[r['topk'], r['topn']] for r in s2],
                   'band_r10_cells': [[r['topk'], r['topn']] for r in tied],
                   'min_cost_cells': [[r['topk'], r['topn']] for r in cheap],
                   'pareto_cells': [[r['topk'], r['topn']] for r in pareto]},
               'cells': [{'l1_topk': r['topk'], 'l2_topn': r['topn'],
                          'l1_survivor_recall': r['l1_recall'],
                          'l2': {k: v for k, v in r['l2'].items()},
                          'l3': {k: v for k, v in r['l3'].items()},
                          'ce_pairs_per_query': r['pairs_q'], 'l3_ms_per_query': r['l3_ms_q'],
                          'e2e_ms_per_query': r['e2e_ms_q'],
                          'is_best': r is best, 'is_pareto': r in pareto} for r in rows],
               'design_table': body.split('\n')}
    with io.open(gpath, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    log('数据落盘: 网格搜索报告写入 %s (%d bytes)' % (gpath, os.path.getsize(gpath)))
    write_design_grid(args.design, body)
    log('数据落盘: 网格结果表已写入 %s 的标记块' % args.design)
    return gpath


def grid_markdown(rows, best, pareto, tied, n_elig, nq, n_skills, ms_l1, ms_l2, ms_pair,
                  ce_note, n_pair, args):
    """把网格结果拼成 DESIGN.md 的一个小节 (含成本模型、表格、选点规则与结论)。"""
    L = ['### 2.3 超参数网格搜索：l1-topk × l2-topn（%s，CPU，%d 查询 × %d skills）'
         % (time.strftime('%Y-%m-%d'), nq, n_skills), '',
         '> 复现：`python demo/router_demo.py --grid`。L1/L2 = %s，L3 = %s，RRF K0=%d。'
         % (args.emb_model, RERANK_MODEL, RRF_K0),
         '> CE 分数是 (query, doc) 的纯函数，与两个超参无关，故全网格共用一份缓存：'
         '%d 个 cell 只对去重后的 %d 个 pair 打一次分（不去重需 %d 次）。'
         % (len(rows), n_pair, sum(r['topn'] for r in rows) * nq), '',
         '**成本模型**（均为**在线单查询**口径，不含一次性的全库编码与模型加载；'
         '一次性成本见运行日志 `性能: L1 索引侧一次性耗时`，冷启动约 10²s，稳态读 npz 缓存约 1s）：'
         'L1（query 编码 + 全库余弦 + argsort）与 L2（全库 TF-IDF + RRF）的延迟与两个超参**无关**，'
         '实测 L1 %.0fms/查询、L2 %.0fms/查询；L3 延迟 = l2-topn × %.1fms/pair'
         '（%s，batch=%d 摊薄口径，不含模型加载）。'
         % (ms_l1, ms_l2, ms_pair, ce_note, args.ce_batch), '',
         '| l1-topk | l2-topn | L1 存活集召回 | L2 hit@1 | L2 R@5 | L3 hit@1 | L3 R@3 | **L3 R@5** '
         '| L3 R@10 | L3 R@20 | L3 P@3 | L3 MRR | CE pair/q | L3 ms/q | 端到端 ms/q |',
         '| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: '
         '| ---: | ---: | ---: |']
    for r in rows:
        tag = ' **← 最优**' if r is best else (' ← Pareto' if r in pareto else '')
        L.append('| %d | %d | %.1f%%%s | %.1f%% | %.1f%% | %.1f%% | %.1f%% | **%.1f%%**%s '
                 '| %.1f%% | %.1f%% | %.3f | %.3f | %d | %.0f | %.0f |'
                 % (r['topk'], r['topn'], 100 * r['l1_recall'],
                    '' if r['l1_recall'] >= 1 - 1e-9 else ' ✗',
                    100 * r['l2']['r@1'], 100 * r['l2']['r@5'], 100 * r['l3']['r@1'],
                    100 * r['l3']['r@3'], 100 * r['l3']['r@5'], tag,
                    100 * r['l3']['r@10'], 100 * r['l3']['r@20'], r['l3']['p@3'],
                    r['l3']['mrr'], r['pairs_q'], r['l3_ms_q'], r['e2e_ms_q']))
    # l1-topk 的"饱和点": 与更大 k 的逐格指标全部落在 1 条查询噪声带内的最小 k
    eps, ks = 1.0 / nq, sorted({r['topk'] for r in rows})
    prof = {K: {r['topn']: [r['l2']['r@5']] + [r['l3'][m] for m in
                ('r@1', 'r@3', 'r@5', 'r@10', 'r@20', 'p@3', 'mrr')]
                for r in rows if r['topk'] == K} for K in ks}
    sat_k = min(K for K in ks if all(abs(a - b) <= eps + 1e-9 for K2 in ks if K2 > K
                                     for n, v in prof[K].items()
                                     for a, b in zip(v, prof[K2][n])))
    L += ['', '**选点规则**（字典序，不引入人工权重，避免在 %d 条样本上过拟合）：' % nq,
          '0. **硬约束**（不可交易）：L1 存活集召回 = 100%%（被 L1 漏掉的候选 L2/L3 永远救不回来，'
          '它就是端到端召回上限）＋ §1 门禁 L3 R@20 ≥ 95%%、R@5 ≥ 85%%。'
          '本网格 %d/%d 个 cell 通过（L1 列标 ✗ 者被剔除）；' % (n_elig, len(rows)),
          '1. **主指标 = L3 R@5**（模式 b 实际返回 5 条，返回集召回就是产品契约）取最大；',
          '2. 依次 tie-break：**L3 hit@1**（top-1 准确率）最大 → **L3 R@10** 最大 → '
          '**CE pair/查询**最小 → **l1-topk** 最小；',
          '3. 1~2 中所有召回/准确率指标都带 **1 条查询（%.2fpp）的噪声带**：取值天然是 1/%d 的'
          '整数倍，差 1 条即视为统计并列，不当作真实优劣；' % (100.0 / nq, nq),
          '4. 成本只作 tie-break 而非主指标：CE pair 数是唯一随超参变化的真实成本（L1/L2 延迟与'
          '两超参无关），但生产上 CE 走 GPU 批量服务，10 pair 与 5 pair 的墙钟延迟几乎相同，'
          'CPU 原型上的成本差不应主导选点；l1-topk 最后取小，是因为同质量下剪枝更狠、'
          '语料涨到 1w 时相对余量更大。',
          '',
          '**结论**：最优组合 `l1-topk=%d, l2-topn=%d`——L1 存活集召回 %.1f%%、'
          '**L3 R@5 %.1f%%**、hit@1 %.1f%%、R@10 %.1f%%、R@20 %.1f%%、P@3 %.3f、MRR %.3f，'
          'CE %d pair/查询、CPU 端到端 %.0fms/查询（其中 L1 %.0fms + L2 %.0fms + L3 %.0fms）。'
          % (best['topk'], best['topn'], 100 * best['l1_recall'], 100 * best['l3']['r@5'],
             100 * best['l3']['r@1'], 100 * best['l3']['r@10'], 100 * best['l3']['r@20'],
             best['l3']['p@3'], best['l3']['mrr'], best['pairs_q'], best['e2e_ms_q'],
             ms_l1, ms_l2, best['l3_ms_q']),
          '',
          '- 硬约束后 %d 个 cell 里，与最优**统计并列且同成本**的有 %d 个：%s；'
          'Pareto 前沿（R@5 vs CE 成本，限通过硬约束的 cell）%d 个：%s。'
          % (n_elig, len(tied), ', '.join('(%d,%d)' % (r['topk'], r['topn']) for r in tied),
             len(pareto), ', '.join('(%d,%d)' % (r['topk'], r['topn']) for r in pareto)),
          '- **l2-topn 的规律**：本网格中 hit@1 随 n 单调下降（见表）。CE 只在 top-n 窗口内重排，'
          '窗口越大越容易把 L2 排在 6~n 名的弱候选误提到第 1 位；反之 n 太小时窗口 == 返回集，'
          'CE 对召回**零贡献**（L3 R@5 与 L2 R@5 完全相同，表中可直接对照），只重排不救回。'
          '本次最优取 n=%d：CE 仍能救回 L2 第 6~%d 名，hit@1 又未被大窗口稀释。'
          % (best['topn'], best['topn']),
          '- **l1-topk 的规律**：k ≥ %d 后存活集召回恒为 100%%，但 L2/L3 的 R@5/R@10 仍随 k 增大'
          '而提升——RRF 需要更宽的候选池才能把"TF-IDF 强、embedding 弱"的项提上来；k = %d 起'
          '继续加大已无可测收益（与更大 k 的逐格差异全落在 1 条查询噪声带内），且 k 不进入任何'
          '延迟项（L1 恒为 query 编码 + 全库余弦 + 全库 argsort），故按 tie-break 在质量并列的 cell 中取最小 k = %d，'
          '剪枝最狠、语料涨到 1w 时相对余量最大。'
          % (min(r['topk'] for r in rows if r['l1_recall'] >= 1 - 1e-9), sat_k,
             best['topk']), '']
    return '\n'.join(L)


def write_design_grid(path, body):
    """把网格表写进 DESIGN.md 的标记块; 标记不存在则插到「## 三、总体架构」之前。"""
    src = io.open(path, encoding='utf-8').read() if os.path.exists(path) else ''
    block = '%s\n%s\n%s' % (GRID_BEGIN, body, GRID_END)
    if GRID_BEGIN in src:
        new = re.sub(re.escape(GRID_BEGIN) + r'.*?' + re.escape(GRID_END),
                     lambda _: block, src, flags=re.S)
    else:
        anchor = '\n## 三、总体架构'
        new = (src.replace(anchor, '\n' + block + '\n' + anchor, 1) if anchor in src
               else src.rstrip() + '\n\n' + block + '\n')
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--l1-topk', type=int, default=50,
                    help='L1 保留的候选条数; 与语料规模 N 解耦的成本预算 '
                         '(默认 50 = --grid 网格搜索最优, k>=30 本语料零丢失, 见 DESIGN §2.3)')
    ap.add_argument('--l2-topn', type=int, default=10,
                    help='L2 送进 L3 重排的窗口条数 (默认 10 = --grid 网格搜索最优, 见 DESIGN §2.3)')
    ap.add_argument('--ks', default='1,3,5,10,20,50')
    ap.add_argument('--emb-model', default=EMB_MODEL,
                    help='L1 embedding 模型 (hub id 或 demo/models/ 下的本地目录名)')
    ap.add_argument('--no-l3', action='store_true')
    ap.add_argument('--refresh-cache', action='store_true')
    ap.add_argument('--grid', action='store_true',
                    help='网格搜索 l1-topk x l2-topn; 结果写日志、cache/grid_*.json 与 DESIGN.md 标记块')
    ap.add_argument('--grid-topk', default=GRID_TOPK, help='网格搜索的 l1-topk 取值 (逗号分隔)')
    ap.add_argument('--grid-topn', default=GRID_TOPN, help='网格搜索的 l2-topn 取值 (逗号分隔)')
    ap.add_argument('--ce-batch', type=int, default=64, help='reranker 打分 batch size')
    ap.add_argument('--design', default=os.path.join(ROOT, 'DESIGN.md'),
                    help='网格结果表写入的文档 (仅 --grid 生效)')
    args = ap.parse_args()
    ks = [int(x) for x in args.ks.split(',')]
    ts = time.strftime('%Y%m%d-%H%M%S')
    os.makedirs(LOGDIR, exist_ok=True)
    _LOGF[0] = io.open(os.path.join(LOGDIR, 'router_demo_%s.log' % ts),
                       'w', encoding='utf-8')
    log('数据生成: 运行参数 args=%s, ks=%s' % (vars(args), ks))

    queries = load_queries()
    docs = load_skills()
    slugs = sorted(docs)
    idx = {s: i for i, s in enumerate(slugs)}
    log('数据生成: slugs 排序与 idx 反查表完成, n_skills=%d' % len(slugs))
    corpus = ['%s %s %s %s' % (docs[s][0], docs[s][0], docs[s][0], docs[s][1]) for s in slugs]
    l1_texts = ['%s %s' % (docs[s][0], docs[s][1]) for s in slugs]
    log('数据生成: L2 语料(name x3 + desc) %d 条 / L1 文本(name + desc) %d 条'
        % (len(corpus), len(l1_texts)))
    log_sample('L1 输入文本 (slug: name + desc)',
               ['%s: %s' % (s, t) for s, t in zip(slugs, l1_texts)])
    log_sample('L2 语料 (slug: name x3 + desc)',
               ['%s: %s' % (s, t) for s, t in zip(slugs, corpus)])
    print('语料: %d 个 skill / %d 条查询' % (len(slugs), len(queries)))

    gold, qtext = [], []
    for q, g in queries:
        g = [x for x in g if x in idx]
        if not g:
            continue
        gold.append(g)
        qtext.append(q)
    nq = len(qtext)
    log('数据变化: 金标清洗(剔除语料外 slug / 空金标)后有效查询 %d / %d, 剔除 %d 条'
        % (nq, len(queries), len(queries) - nq))
    log_sample('清洗后有效查询 (qtext | gold)',
               ['%s | %r' % (q, g) for q, g in zip(qtext, gold)], limit=20)
    print('有效查询: %d (金标均存在于语料)' % nq)

    # ---- L1
    # 计时分两段: 索引侧(全库编码/读 npz + 模型加载)是**一次性**成本, 冷启动约 100s, 绝不能摊进
    # 单查询延迟(否则冷启动那次会把 L1 报成 ~966ms/查询, 稳态其实 ~85ms); 在线侧只计 query 编码
    # + 全库余弦 + argsort。
    t0 = time.time()
    emb, enc = build_l1_embeddings(slugs, l1_texts, args.refresh_cache, args.emb_model)
    t_index = time.time() - t0
    log('性能: L1 索引侧一次性耗时 %.2fs (全库 %d 条编码或读缓存 + 模型加载), 不计入单查询延迟'
        % (t_index, len(slugs)))
    t0 = time.time()
    q_emb = enc.encode(qtext, batch_size=64, normalize_embeddings=True,
                       show_progress_bar=False).astype('float32')
    sims = q_emb @ emb.T
    t_l1 = time.time() - t0
    log('数据生成: query embedding 完成 shape=%s' % (q_emb.shape,))
    log_sample('query embedding 完整向量样例 (全维向量)',
               [np.round(v, 6).tolist() for v in q_emb])
    log('数据生成: L1 余弦相似度矩阵 sims shape=%s, mean=%.3f max=%.3f'
        % (sims.shape, float(sims.mean()), float(sims.max())))
    log_sample('L1 相似度 top-5 (query -> [(slug, sim)])',
               ['%s -> %s' % (qtext[i], [(slugs[j], round(float(sims[i][j]), 3))
                                          for j in np.argsort(-sims[i])[:5]])
                for i in range(nq)])

    # 诊断: 相似度分布形态决定"绝对阈值"能不能筛动东西。分布越窄, 零丢失阈值越贴近背景分位数,
    # 阈值就退化成套不住任何东西(换英文模型时这里会立刻暴露), 所以只写日志留档, 不用于选点。
    gmask = np.zeros_like(sims, dtype=bool)
    for i in range(nq):
        for g in gold[i]:
            gmask[i, idx[g]] = True
    grid = [round(i, 2) for i in np.arange(0.1, 0.9, 0.01)]
    sweep = []
    for tau in grid:
        kept = float((sims >= tau).sum()) / nq
        hit = sum(1 for i in range(nq) if any(g in slugs_set(sims[i] >= tau, slugs) for g in gold[i])) / nq
        sweep.append((tau, kept, hit))
        log('数据生成: 阈值扫描行 tau=%.2f avg_kept=%.1f l1_recall=%.4f' % (tau, kept, hit))
    log_sample('L1 绝对阈值扫描全表 (tau | avg_kept | recall)',
               ['%.2f | %.1f | %.4f' % s for s in sweep], limit=len(sweep))
    nz = [(t, k) for t, k, h in sweep if h == 1.0]
    p5, p50, p95 = np.percentile(sims[~gmask], [5, 50, 95])
    print('\n[L1 分布诊断] 背景 sim p5/p50/p95 = %.3f/%.3f/%.3f | 金标 min/中位 = %.3f/%.3f'
          % (p5, p50, p95, sims[gmask].min(), np.median(sims[gmask])))
    if nz:
        zt, zk = max(nz)
        print('[L1 分布诊断] 零丢失绝对阈值 tau=%.2f -> 平均存活 %.0f/%d (仅剔除 %.1f%%); '
              '绝对阈值与语料分布耦合, 选点改用 top-k' % (zt, zk, len(slugs), 100 - 100 * zk / len(slugs)))
    else:
        print('[L1 分布诊断] 扫描区间内不存在零丢失绝对阈值; 选点改用 top-k')

    # 选点用 top-k: k 是与语料规模 N 解耦的成本预算, 直接等于 L2/L3 的候选量上限。
    t0 = time.time()
    order_l1 = np.argsort(-sims, axis=1)
    t_l1 += time.time() - t0          # 在线口径: argsort 属于单查询延迟, 累加进 t_l1
    ksweep = []
    print('\n[L1 top-k 扫描] k | 剔除率 | 存活集召回')
    for k in sorted({min(x, len(slugs)) for x in (10, 20, 30, 40, 50, 80, 100, 150, 200, 300, 400)}
                    | {len(slugs)}):
        hit = sum(1 for i in range(nq)
                  if any(g in {slugs[j] for j in order_l1[i][:k]} for g in gold[i])) / nq
        ksweep.append((k, hit))
        print('   %4d | %5.1f%% | %.1f%%' % (k, 100 - 100.0 * k / len(slugs), hit * 100))
        log('数据生成: top-k 扫描行 k=%d pruned=%.4f l1_recall=%.4f'
            % (k, 1 - float(k) / len(slugs), hit))

    topk = min(args.l1_topk, len(slugs))
    survivors = [order_l1[i][:topk] for i in range(nq)]
    l1_rank = [[slugs[j] for j in order_l1[i][:topk]] for i in range(nq)]
    l1_recall = sum(1 for i in range(nq) if any(g in set(l1_rank[i]) for g in gold[i])) / nq
    avg_keep = float(sum(len(s) for s in survivors)) / nq
    log('数据生成: L1 存活集 %d 组, 平均 %.1f 条 (min=%d max=%d), topk=%d, 存活集召回=%.4f'
        % (len(survivors), avg_keep, min(len(s) for s in survivors),
           max(len(s) for s in survivors), topk, l1_recall))
    log_sample('L1 存活集样例 (query -> 存活数 + 前10个存活 slug)',
               ['%s -> 存活 %d 个: %s' % (qtext[i], len(survivors[i]),
                                          [slugs[j] for j in survivors[i][:10]])
                for i in range(nq)], limit=20)
    print('[L1] top-%d | 存活集召回=%.1f%% (端到端上限) | 平均存活 %.1f / %d (%.0f%% 被粗筛剔除) | 耗时 %.1fs'
          % (topk, l1_recall * 100, avg_keep, len(slugs), 100 - 100 * avg_keep / len(slugs), t_l1))

    # ---- L2
    t0 = time.time()
    sim_tfidf = build_l2(corpus, qtext)
    log('数据生成: L2 TF-IDF 相似度矩阵 shape=%s' % (sim_tfidf.shape,))
    log_sample('TF-IDF 全库 top-5 (query -> [(slug, score)])',
               ['%s -> %s' % (qtext[i], [(slugs[j], round(float(sim_tfidf[i][j]), 3))
                                          for j in np.argsort(-sim_tfidf[i])[:5]])
                for i in range(nq)])
    t_l2 = time.time() - t0
    # RRF 融合: 在全库名次上做 reciprocal rank fusion, 再限制到 L1 存活集内排序。
    # 单用 TF-IDF 会丢掉 embedding 的语义信号 (bge-m3 实测 baseline @5 84.1% -> L2 @5 94.4% -> L3 @5 96.3%)。
    fused = 1.0 / (RRF_K0 + rank_matrix(sims)) + 1.0 / (RRF_K0 + rank_matrix(sim_tfidf))
    log('数据生成: RRF 融合分数矩阵 shape=%s (k0=%d, 输入=余弦全库名次 + TF-IDF 全库名次)'
        % (fused.shape, RRF_K0))
    log_sample('RRF 融合分 top-5 (query -> [(slug, fused)])',
               ['%s -> %s' % (qtext[i], [(slugs[j], round(float(fused[i][j]), 5))
                                         for j in np.argsort(-fused[i])[:5]])
                for i in range(nq)])
    l2_rank = []
    base_rank = []
    for i in range(nq):
        cand = survivors[i]
        order = cand[np.argsort(-fused[i][cand])]
        l2_rank.append([slugs[j] for j in order])
        base_rank.append([slugs[j] for j in np.argsort(-sim_tfidf[i])])
    log('数据生成: L2 排序完成, l2_rank/base_rank 各 %d 组全列表 (头 %d 名送 L3)'
        % (len(l2_rank), args.l2_topn))
    log_sample('L2 存活集内 RRF 排序 top-10 (query -> l2_rank)',
               ['%s -> %s' % (qtext[i], l2_rank[i][:10]) for i in range(nq)])
    log_sample('baseline 全库 TF-IDF 排序 top-10 (query -> base_rank)',
               ['%s -> %s' % (qtext[i], base_rank[i][:10]) for i in range(nq)])
    print('[L2] RRF(TF-IDF + embedding) 在存活集内排序 top-%d | 耗时 %.1fs' % (args.l2_topn, t_l2))

    # ---- 网格搜索分支: sims/fused/order_l1 都与超参无关, 在此复用, 只重算 L2 截断与 L3 重排。
    if args.grid:
        gpath = run_grid(args, nq, qtext, gold, docs, slugs, fused, order_l1, t_l1, t_l2)
        if _LOGF[0]:
            _LOGF[0].close()
            _LOGF[0] = None
        print('网格报告: %s' % os.path.relpath(gpath, ROOT))
        return

    # ---- L3
    l3_rank = None
    t_l3 = 0.0
    if not args.no_l3:
        t0 = time.time()
        ce = build_l3()
        l3_rank = []
        pairs, spans = [], []
        for i in range(nq):
            top = l2_rank[i][:args.l2_topn]
            spans.append((len(pairs), len(pairs) + len(top)))
            pairs += [(qtext[i], docs[s][0] + ' ' + docs[s][1]) for s in top]
        log('数据生成: L3 待重排 pair 摊平完成, %d 对 (spans %d 段)' % (len(pairs), len(spans)))
        log_sample('L3 待重排 pair (query || doc)',
                   ['%s || %s' % (q, d) for q, d in pairs], limit=20)
        scores = ce.predict(pairs, batch_size=32, show_progress_bar=True)
        log('数据生成: L3 reranker 打分完成 shape=%s, min=%.2f max=%.2f'
            % (scores.shape, float(scores.min()), float(scores.max())))
        log_sample('L3 打分前 50 个 (pair_index: score)',
                   ['%d: %.4f' % (i, float(s)) for i, s in enumerate(scores)], limit=50)
        for i in range(nq):
            a, b = spans[i]
            top = l2_rank[i][:args.l2_topn]
            order = np.argsort(-scores[a:b])
            rest = l2_rank[i][args.l2_topn:]
            l3_rank.append([top[j] for j in order] + rest)
        log('数据生成: L3 重排完成, l3_rank %d 组 (top-%d 内重排, 其余保持 L2 序)'
            % (len(l3_rank), args.l2_topn))
        log_sample('L3 重排后 top-10 (query -> l3_rank)',
                   ['%s -> %s' % (qtext[i], l3_rank[i][:10]) for i in range(nq)])
        t_l3 = time.time() - t0
        print('[L3] reranker 重排 %d 对 | 耗时 %.1fs' % (len(pairs), t_l3))

    # ---- 指标
    # L1 行是 top-k 存活集按余弦排序后的真实 ranked recall@k (k > topk 时自然封顶,
    # 因为下游看不到存活集之外的东西); 存活集本身的召回率另见上面 [L1] 行与报告 l1_recall。
    rows = {}
    for name, rank in (('L1', l1_rank), ('L2', l2_rank), ('L3', l3_rank), ('baseline', base_rank)):
        if rank is None:
            continue
        rows[name] = {k: sum(recall_at(rank[i], gold[i], [k])[k] for i in range(nq)) / nq for k in ks}
        log('数据生成: 指标行 %s recall@k=%s'
            % (name, {k: round(v, 4) for k, v in rows[name].items()}))
        log_sample('%s 逐查询命中明细 (query | gold | top5 | 命中@5)' % name,
                   ['%s | %r | %s | %s' % (qtext[i], gold[i], rank[i][:5],
                                           'Y' if any(g in rank[i][:5] for g in gold[i]) else 'N')
                    for i in range(nq)], limit=50)

    # 结果表: stdout / 运行日志 / report.json 三处同源, 避免只看终端丢结论。
    table = ['=== Recall@k (n=%d) ===' % nq,
             'layer      | ' + ' | '.join('@%-8d' % k for k in ks)]
    for name in ('L1', 'L2', 'L3', 'baseline'):
        if name in rows:
            table.append('%-10s | ' % name
                         + ' | '.join('%-9.1f%%' % (rows[name][k] * 100) for k in ks))
    table.append('(L1 top-%d 存活集召回 %.1f%% = 端到端上限; L2/L3 不可能超过它)'
                 % (topk, l1_recall * 100))
    table.append('延迟(在线/查询, 不含一次性索引构建 %.0fs): L1 %.0fms | L2 %.0fms | L3 %.0fms'
                 % (t_index, 1000 * t_l1 / nq, 1000 * t_l2 / nq,
                    1000 * t_l3 / nq if not args.no_l3 else 0))
    print()
    for line in table:
        log(line)

    os.makedirs(REPORT, exist_ok=True)
    report = {'timestamp': ts,
              'params': {'args': vars(args), 'ks': ks,
                         'emb_model': args.emb_model, 'rerank_model': RERANK_MODEL,
                         'rrf_k0': RRF_K0, 'python': sys.version.split()[0]},
              'n_queries': nq, 'n_skills': len(slugs), 'l1_topk': topk,
              'l1_avg_kept': avg_keep, 'l1_recall': l1_recall,
              'recall': {name: {str(k): v for k, v in r.items()} for name, r in rows.items()},
              'recall_table': table,
              'latency_ms_per_query': {'l1': 1000 * t_l1 / nq, 'l2': 1000 * t_l2 / nq,
                                       'l3': 1000 * t_l3 / nq},
              # 在线延迟口径 = query 编码 + 全库余弦 + argsort(L1) / TF-IDF+RRF(L2) / CE(L3)。
              # 索引侧(全库编码或读 npz + 模型加载)是**一次性**成本, 冷启动量级 ~10^2 秒, 单独记不摊入。
              'one_time_s': {'l1_index_build': t_index},
              'k_sweep': [{'k': k, 'recall': r} for k, r in ksweep],
              'tau_sweep': [{'tau': t, 'avg_kept': k, 'recall': r} for t, k, r in sweep]}
    rpath = os.path.join(REPORT, 'report_%s.json' % ts)
    with io.open(rpath, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    log('数据落盘: 评测报告写入 %s (%d bytes)' % (rpath, os.path.getsize(rpath)))
    log_sample('report.json 顶层内容', [json.dumps(report, ensure_ascii=False)], limit=1)
    if _LOGF[0]:
        _LOGF[0].close()
        _LOGF[0] = None
    print('报告: %s' % os.path.relpath(rpath, ROOT))


if __name__ == '__main__':
    sys.exit(main())
