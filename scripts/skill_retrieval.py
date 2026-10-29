# -*- coding: utf-8 -*-
"""L2 混合召回检索器: TF-IDF ∪ BM25 并集版（2026-10-29 实测验收, 见飞书方案第九章）

召回层唯一职责是「不漏候选」，排序精度交给 L3 重排。两路误差分布不同:
  - TF-IDF: 词 1-2gram + 字 3-5gram, 余弦相似度
  - BM25:    词+字混合 token(纯英文词空间在中文查询上 R@20 仅 42%, 不可单独用)
各取 top-K 取并集, 按轮询交错排序(TF-IDF 优先)。实测 107 查询:
  并集候选集 R@20 = 100%, 交错序 R@5 = 89.7%(TF-IDF 基线 84.1%), 平均候选 22 个。

用法:
  python scripts/skill_retrieval.py build                 # 离线建索引(约 10s)
  python scripts/skill_retrieval.py query "SSRF 带外验证"   # 输出并集候选 slug 列表
  python scripts/skill_retrieval.py query "..." --top 30

依赖: scikit-learn, scipy, rank_bm25
索引产物 scripts/_retrieval_index.pkl 已 gitignore, 不入库, 部署前重新 build。
"""
import argparse, io, os, pickle, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PKL = os.path.join(ROOT, 'scripts', '_retrieval_index.pkl')
REGISTERED = {'attack-skill-router', 'engagement-discipline', 'java-deserialization-gadget-selector'}


def load_corpus():
    """{slug: (name, description)}，与 eval_recall.load_skills 同口径(排除注册层与 scripts)"""
    docs = {}
    for dp, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ('.git', '_before_tmp')]
        if 'SKILL.md' not in files:
            continue
        slug = os.path.relpath(dp, ROOT).replace(os.sep, '/').split('/')[-1]
        parts = os.path.relpath(dp, ROOT).replace(os.sep, '/').split('/')
        # 兼容两种布局: 仓库(组目录/slug) 与 部署态库根(扁平 slug); 排除注册层/工具目录
        if parts[0] in REGISTERED or parts[0] in ('scripts', '_router') or '.git' in parts:
            continue
        s = io.open(os.path.join(dp, 'SKILL.md'), encoding='utf-8', errors='replace').read()
        fm = re.search(r'^---\n(.*?)\n---', s, re.S)
        if not fm:
            continue
        dm = re.search(r'^description:\s*(.+)$', fm.group(1), re.M)
        nm = re.search(r'^name:\s*(.+)$', fm.group(1), re.M)
        if not dm:
            continue
        docs[slug] = (nm.group(1).strip() if nm else slug, dm.group(1).strip())
    return docs


def build():
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from scipy.sparse import hstack
    from rank_bm25 import BM25Okapi

    docs = load_corpus()
    slugs = sorted(docs)
    corpus = ['{0} {0} {0} {1}'.format(docs[s][0], docs[s][1]) for s in slugs]
    vec_w = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    vec_c = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5), min_df=1)
    X = hstack([vec_w.fit_transform(corpus), vec_c.fit_transform(corpus)]).tocsr()
    ana_w, ana_c = vec_w.build_analyzer(), vec_c.build_analyzer()
    bm25 = BM25Okapi([ana_w(c) + ana_c(c) for c in corpus])
    with open(INDEX_PKL, 'wb') as f:
        pickle.dump({'slugs': slugs, 'vec_w': vec_w, 'vec_c': vec_c, 'X': X, 'bm25': bm25}, f)
    print('索引完成: {0} 个 skill -> {1}'.format(len(slugs), INDEX_PKL))


def tops(row, k):
    import numpy as np
    return list(np.argsort(-row)[:k])


def query(text, top):
    import numpy as np
    from scipy.sparse import hstack
    if not os.path.exists(INDEX_PKL):
        print('索引不存在, 先运行: python scripts/skill_retrieval.py build', file=sys.stderr)
        sys.exit(1)
    with open(INDEX_PKL, 'rb') as f:
        idx = pickle.load(f)
    slugs, vec_w, vec_c, X, bm25 = idx['slugs'], idx['vec_w'], idx['vec_c'], idx['X'], idx['bm25']
    q = hstack([vec_w.transform([text]), vec_c.transform([text])])
    sim = (q @ X.T).toarray()[0]
    ana_w, ana_c = vec_w.build_analyzer(), vec_c.build_analyzer()
    bm = bm25.get_scores(ana_w(text) + ana_c(text))
    t_k, b_k = tops(sim, top), tops(bm, top)
    merged, pool_t, pool_b = [], [j for j in t_k], [j for j in b_k]   # 轮询交错, TF-IDF 优先
    while pool_t or pool_b:
        for pool in (pool_t, pool_b):
            while pool and pool[0] in merged:
                pool.pop(0)
            if pool:
                merged.append(pool.pop(0))
    for rank, j in enumerate(merged, 1):
        print('{0:3d}. {1}'.format(rank, slugs[j]))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='L2 混合召回: TF-IDF ∪ BM25')
    ap.add_argument('command', choices=['build', 'query'])
    ap.add_argument('text', nargs='?', help='query 模式的查询语句')
    ap.add_argument('--top', type=int, default=20, help='每路取 top-K(默认 20)')
    a = ap.parse_args()
    if a.command == 'build':
        build()
    else:
        if not a.text:
            ap.error('query 模式需要查询语句')
        query(a.text, a.top)
