# -*- coding: utf-8 -*-
"""全链路评测: L1字典 (+L0c粗筛) → L2混合召回 (+L3重排) 在 107 条金标上的 recall 与延迟

配置:
  l2              L1 字典 + L2 (生产基线, 默认路径)
  coarse-l2       + L0c embedding 粗筛(tau 可配, 默认 0.45)
  l2-local        L1 + L2 + L3 本地 bge-reranker-v2-m3-int8
  coarse-l2-local 全链路: 粗筛 → L2 → 本地重排

用法:
  python scripts/eval_pipeline.py                      # 全部 4 配置
  python scripts/eval_pipeline.py --configs coarse-l2-local --start 0 --end 50
"""
import argparse, io, os, sys, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skill_route as R
from skill_retrieval import load_corpus

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_queries():
    src = io.open(os.path.join(ROOT, 'scripts', 'eval_recall.py'), encoding='utf-8').read()
    mod = {'__file__': os.path.join(ROOT, 'scripts', 'eval_recall.py')}
    exec(src[:src.index('def evaluate(')], mod)
    return mod['QUERIES']


def load_query_sims(queries, slugs):
    """批量查询嵌入(缓存 scripts/_coarse_cache/*.queries.npy, 与 QUERIES 同序) -> S[查询, skill]
    缓存缺失时自动批量嵌入全部查询(约 1 分钟)并落盘, 保证克隆后开箱可跑"""
    key = R.COARSE_MODEL.replace('/', '_')
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_coarse_cache')
    fp = os.path.join(cache_dir, key + '.queries.npy')
    if os.path.exists(fp):
        Q = np.load(fp).astype(np.float32)
    else:
        print('查询嵌入缓存缺失, 批量嵌入 {0} 条查询(约 1 分钟, 之后走缓存)...'.format(len(queries)), flush=True)
        from fastembed import TextEmbedding
        emb = TextEmbedding(R.COARSE_MODEL)
        prefix = R.Q_PREFIX.get(R.COARSE_MODEL, '')
        Q = np.array(list(emb.embed([prefix + q for q, _ in queries])), dtype=np.float32)
        os.makedirs(cache_dir, exist_ok=True)
        np.save(fp, Q)
    Q = Q[:len(queries)]
    X = np.load(os.path.join(cache_dir, key + '.npy')).astype(np.float32)
    assert X.shape[0] == len(slugs)
    Qn = Q / np.linalg.norm(Q, axis=1, keepdims=True)
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    return Qn @ Xn.T


def run_config(name, queries, sims, docs, slugs, idx, tau):
    vec_w, vec_c, X, bm25 = idx['vec_w'], idx['vec_c'], idx['X'], idx['bm25']
    use_coarse = name.startswith('coarse')
    use_local = name.endswith('local')
    slug_pos = {s: i for i, s in enumerate(slugs)}
    h5 = h20 = 0
    n_cand, kept_sum, t_sum, miss = [], 0, 0.0, []
    for qi, (q, gold) in enumerate(queries):
        gold = [g for g in gold if g in docs]
        if not gold:
            continue
        t0 = time.time()
        l1_hits, _ = R.l1_dict_match(q, slugs)
        mask = third = None
        if use_coarse:
            mask = np.array(sims[qi] >= tau)
            kept_sum += int(mask.sum())
            for s in l1_hits:
                mask[slug_pos[s]] = True
            third = np.where(mask, sims[qi], -np.inf)
        cands = R.l2_recall(q, slugs, vec_w, vec_c, X, bm25, 25, mask, third)
        for s in l1_hits:
            if s in cands:
                cands.remove(s)
            cands.insert(0, s)
        if not use_local:
            cands = cands[:20]
        else:
            cands = cands[:40]          # 重排看全并集, 最终截 20
            cands, scored, _ = R.l3_local_rerank(q, cands, docs)
            cands = cands[:20]
        t_sum += time.time() - t0
        n_cand.append(len(cands))
        top5, top20 = set(cands[:5]), set(cands[:20])
        if any(g in top5 for g in gold):
            h5 += 1
        if any(g in top20 for g in gold):
            h20 += 1
        else:
            miss.append(q)
    n = len(queries)
    line = '[{0}] R@5={1:.1%} R@20={2:.1%} | 候选均值 {3:.1f} | {4:.0f}ms/查询'.format(
        name, h5 / n, h20 / n, float(np.mean(n_cand)), 1000 * t_sum / n)
    if use_coarse:
        line += ' | 粗筛后均值 {0:.0f}/994'.format(kept_sum / n)
    print(line, flush=True)
    if miss:
        print('  漏召(@20):', '；'.join(miss), flush=True)
    return h5 / n, h20 / n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--configs', default='l2,coarse-l2,l2-local,coarse-l2-local')
    ap.add_argument('--tau', type=float, default=R.COARSE_TAU)
    ap.add_argument('--start', type=int, default=0)
    ap.add_argument('--end', type=int, default=10 ** 9)
    a = ap.parse_args()

    import pickle
    with open(R.INDEX_PKL, 'rb') as f:
        idx = pickle.load(f)
    slugs = idx['slugs']
    docs = load_corpus()
    all_queries = load_queries()
    queries = all_queries[a.start:a.end]
    sims = load_query_sims(all_queries, slugs)[a.start:a.end]
    print('评测 {0} 条查询 / {1} skills / tau={2}'.format(len(queries), len(slugs), a.tau), flush=True)
    for cfg in a.configs.split(','):
        run_config(cfg.strip(), queries, sims, docs, slugs, idx, a.tau)


if __name__ == '__main__':
    main()
