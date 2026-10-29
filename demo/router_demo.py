# -*- coding: utf-8 -*-
"""三层漏斗 skill 路由 demo：L1 embedding 粗筛 -> L2 TF-IDF 召回 -> L3 cross-encoder 精排。

方案见仓库根目录 DESIGN.md（对应 SKILL-PLAN.md 第三章的最小验证版）。
评测集为仓库评测 harness 中的 107 条金标查询（运行时从 git blob 提取，避免依赖工作区文件状态）。

用法:
    python router_demo.py                  # 全量评测
    python router_demo.py --l1-tau 0.40    # 固定 L1 余弦阈值
    python router_demo.py --no-l3          # 消融: 只跑 L1+L2
"""
import argparse
import ast
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
CACHE = os.path.join(ROOT, 'demo', 'cache')
LOGDIR = os.path.join(ROOT, 'demo', 'logs')
HARNESS = 'scripts/eval_recall.py'
REGISTERED = {'attack-skill-router', 'engagement-discipline', 'java-deserialization-gadget-selector'}
EMB_MODEL = 'BAAI/bge-small-en-v1.5'  # 默认英文模型; 可用 --emb-model 切换(如 BAAI/bge-small-zh-v1.5 / nomic-ai/nomic-embed-text-v1.5)
RERANK_MODEL = 'BAAI/bge-reranker-v2-m3'


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
            log_sample('缓存 embedding 完整向量样例 (slug: 512维)',
                       ['%s: %s' % (s, np.round(v, 6).tolist())
                        for s, v in zip(z['slugs'], z['emb'])])
            return z['emb'], model
    print('[L1] 编码全库 %d 条 (model=%s) ...' % (len(slugs), emb_model))
    emb = model.encode(texts, batch_size=64, normalize_embeddings=True,
                       show_progress_bar=True).astype('float32')
    np.savez_compressed(path, slugs=np.array(slugs), emb=emb)
    log('数据落盘: L1 全库 embedding 编码完成 shape=%s, 写入 %s' % (emb.shape, path))
    log_sample('新编码 embedding 完整向量样例 (slug: 512维)',
               ['%s: %s' % (s, np.round(v, 6).tolist()) for s, v in zip(slugs, emb)])
    return emb, model


def slugs_set(mask, slugs):
    return {s for s, m in zip(slugs, mask) if m}


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


# ---------------------------------------------------------------- 评测
def recall_at(ranking, gold, ks):
    out = {}
    for k in ks:
        out[k] = float(any(g in ranking[:k] for g in gold))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--l1-tau', default='auto', help='L1 余弦阈值, auto=金标零丢失前提下取最大')
    ap.add_argument('--l2-topn', type=int, default=20, help='L2 送进 L3 的条数')
    ap.add_argument('--ks', default='1,3,5,10,20')
    ap.add_argument('--emb-model', default=EMB_MODEL,
                    help='L1 embedding 模型 (hub id 或 demo/models/ 下的本地目录名)')
    ap.add_argument('--no-l3', action='store_true')
    ap.add_argument('--refresh-cache', action='store_true')
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
    t0 = time.time()
    emb, enc = build_l1_embeddings(slugs, l1_texts, args.refresh_cache, args.emb_model)
    q_emb = enc.encode(qtext, batch_size=64, normalize_embeddings=True,
                       show_progress_bar=False).astype('float32')
    log('数据生成: query embedding 完成 shape=%s' % (q_emb.shape,))
    log_sample('query embedding 完整向量样例 (512维)',
               [np.round(v, 6).tolist() for v in q_emb])
    t_l1 = time.time() - t0
    sims = q_emb @ emb.T
    log('数据生成: L1 余弦相似度矩阵 sims shape=%s, mean=%.3f max=%.3f'
        % (sims.shape, float(sims.mean()), float(sims.max())))
    log_sample('L1 相似度 top-5 (query -> [(slug, sim)])',
               ['%s -> %s' % (qtext[i], [(slugs[j], round(float(sims[i][j]), 3))
                                          for j in np.argsort(-sims[i])[:5]])
                for i in range(nq)])

    grid = [round(i, 2) for i in np.arange(0.1, 0.9, 0.01)]
    sweep = []
    for tau in grid:
        kept = float((sims >= tau).sum()) / nq
        hit = sum(1 for i in range(nq) if any(g in slugs_set(sims[i] >= tau, slugs) for g in gold[i])) / nq
        sweep.append((tau, kept, hit))
    print('\n[L1 阈值扫描] tau | 平均存活数 | L1 recall')
    for tau, kept, hit in sweep:
        print('   %.2f | %8.1f | %.1f%%' % (tau, kept, hit * 100))
        log('数据生成: 阈值扫描行 tau=%.2f avg_kept=%.1f l1_recall=%.4f' % (tau, kept, hit))
    if args.l1_tau == 'auto':
        ok = [tau for tau, kept, hit in sweep if hit == 1.0]
        tau = max(ok) if ok else min(grid)
    else:
        tau = float(args.l1_tau)
    log('数据生成: L1 阈值选定 tau=%.2f (mode=%s)' % (tau, args.l1_tau))
    print('[L1] 选定 tau=%.2f' % tau)

    survivors = [np.flatnonzero(sims[i] >= tau) for i in range(nq)]
    l1_recall = sum(1 for i in range(nq) if any(g in slugs_set(sims[i] >= tau, slugs) for g in gold[i])) / nq
    avg_keep = float(sum(len(s) for s in survivors)) / nq
    log('数据生成: L1 存活集 %d 组, 平均 %.1f 条 (min=%d max=%d), l1_recall=%.4f'
        % (len(survivors), avg_keep, min(len(s) for s in survivors),
           max(len(s) for s in survivors), l1_recall))
    log_sample('L1 存活集样例 (query -> 存活数 + 前10个存活 slug)',
               ['%s -> 存活 %d 个: %s' % (qtext[i], len(survivors[i]),
                                          [slugs[j] for j in survivors[i][:10]])
                for i in range(nq)], limit=20)
    print('[L1] recall=%.1f%% | 平均存活 %.1f / %d (%.0f%% 被粗筛剔除) | 耗时 %.1fs'
          % (l1_recall * 100, avg_keep, len(slugs), 100 - 100 * avg_keep / len(slugs), t_l1))

    # ---- L2
    t0 = time.time()
    sim_tfidf = build_l2(corpus, qtext)
    log('数据生成: L2 TF-IDF 相似度矩阵 shape=%s' % (sim_tfidf.shape,))
    log_sample('TF-IDF 全库 top-5 (query -> [(slug, score)])',
               ['%s -> %s' % (qtext[i], [(slugs[j], round(float(sim_tfidf[i][j]), 3))
                                          for j in np.argsort(-sim_tfidf[i])[:5]])
                for i in range(nq)])
    t_l2 = time.time() - t0
    l2_rank = []
    base_rank = []
    for i in range(nq):
        cand = survivors[i]
        order = cand[np.argsort(-sim_tfidf[i][cand])]
        l2_rank.append([slugs[j] for j in order])
        base_rank.append([slugs[j] for j in np.argsort(-sim_tfidf[i])])
    log('数据生成: L2 排序完成, l2_rank/base_rank 各 %d 组全列表 (头 %d 名送 L3)'
        % (len(l2_rank), args.l2_topn))
    log_sample('L2 存活集内排序 top-10 (query -> l2_rank)',
               ['%s -> %s' % (qtext[i], l2_rank[i][:10]) for i in range(nq)])
    log_sample('baseline 全库排序 top-10 (query -> base_rank)',
               ['%s -> %s' % (qtext[i], base_rank[i][:10]) for i in range(nq)])
    print('[L2] TF-IDF 在存活集内排序 top-%d | 耗时 %.1fs' % (args.l2_topn, t_l2))

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
    rows = {'L1': {k: l1_recall for k in ks}}
    for name, rank in (('L2', l2_rank), ('L3', l3_rank), ('baseline', base_rank)):
        if rank is None:
            continue
        rows[name] = {k: sum(recall_at(rank[i], gold[i], [k])[k] for i in range(nq)) / nq for k in ks}
        log('数据生成: 指标行 %s recall@k=%s'
            % (name, {k: round(v, 4) for k, v in rows[name].items()}))
        log_sample('%s 逐查询命中明细 (query | gold | top5 | 命中@5)' % name,
                   ['%s | %r | %s | %s' % (qtext[i], gold[i], rank[i][:5],
                                           'Y' if any(g in rank[i][:5] for g in gold[i]) else 'N')
                    for i in range(nq)], limit=50)

    print('\n=== Recall@k (n=%d) ===' % nq)
    head = 'layer      | ' + ' | '.join('@%-8d' % k for k in ks)
    print(head)
    for name in ('L1', 'L2', 'L3', 'baseline'):
        if name not in rows:
            continue
        print('%-10s | ' % name + ' | '.join('%-9.1f%%' % (rows[name][k] * 100) for k in ks))
    print('\n延迟(全量/查询): L1 %.0fms | L2 %.0fms | L3 %.0fms'
          % (1000 * t_l1 / nq, 1000 * t_l2 / nq, 1000 * t_l3 / nq if not args.no_l3 else 0))

    os.makedirs(CACHE, exist_ok=True)
    report = {'timestamp': ts,
              'params': {'args': vars(args), 'ks': ks,
                         'emb_model': args.emb_model, 'rerank_model': RERANK_MODEL,
                         'python': sys.version.split()[0]},
              'n_queries': nq, 'n_skills': len(slugs), 'l1_tau': tau,
              'l1_avg_kept': avg_keep, 'l1_recall': l1_recall,
              'recall': {name: {str(k): v for k, v in r.items()} for name, r in rows.items()},
              'latency_ms_per_query': {'l1': 1000 * t_l1 / nq, 'l2': 1000 * t_l2 / nq,
                                       'l3': 1000 * t_l3 / nq},
              'sweep': [{'tau': t, 'avg_kept': k, 'recall': r} for t, k, r in sweep]}
    rpath = os.path.join(CACHE, 'report_%s.json' % ts)
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
