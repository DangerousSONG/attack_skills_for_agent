# -*- coding: utf-8 -*-
# L1 粗筛 embedding 选型: 阈值扫描, 找 "100% recall 前提下的最大剔除率"
# 口径与同事实验一致: 每查询保留 sim>=tau 的 skill, 统计剔除率与金标存活
import io, os, re, json, sys
import numpy as np

REPO = r'D:\研究\网安工具\1000攻击skills'
WS = os.path.dirname(os.path.abspath(__file__))
REGISTERED = {'attack-skill-router', 'engagement-discipline', 'java-deserialization-gadget-selector'}
MODELS = os.environ.get('SWEEP_MODELS', 'BAAI/bge-small-zh-v1.5,Qwen/Qwen3-Embedding-0.6B-Q').split(',')
TAUS = [round(0.30 + 0.05 * i, 2) for i in range(12)]  # 0.30 ~ 0.85
# 查询侧指令前缀(官方推荐, 文档侧不加): 与句子嵌入模型评测口径一致
Q_PREFIX = {
    'BAAI/bge-small-zh-v1.5': '为这个句子生成表示以用于检索相关文章：',
    'Qwen/Qwen3-Embedding-0.6B-Q': 'Instruct: Given a web search query, retrieve relevant passages that answer the query\nQuery: ',
}


def load_data():
    src = io.open(os.path.join(REPO, 'scripts', 'eval_recall.py'), encoding='utf-8').read()
    _mod = {'__file__': os.path.join(REPO, 'scripts', 'eval_recall.py')}
    exec(src[:src.index('def evaluate(')], _mod)
    queries = _mod['QUERIES']
    docs = {}
    for dp, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in ('.git', '_before_tmp')]
        if 'SKILL.md' not in files:
            continue
        rel = os.path.relpath(dp, REPO).replace(os.sep, '/')
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
        zm = re.search(r'^zh-signals:\s*(.+)$', fm.group(1), re.M)
        docs[parts[-1]] = (nm.group(1).strip() if nm else parts[-1], dm.group(1).strip(), zm.group(1).strip().strip(chr(34)).strip(chr(39)) if zm else '')
    return queries, docs


def embed(model_name, texts, cache_key):
    from fastembed import TextEmbedding
    cache = os.path.join(WS, '_l1_emb_cache')
    os.makedirs(cache, exist_ok=True)
    fp = os.path.join(cache, cache_key + '.npy')
    if os.path.exists(fp):
        return np.load(fp)
    print('  下载/加载模型并编码 {0} 条文本...'.format(len(texts)), flush=True)
    emb = TextEmbedding(model_name)
    arr = np.array(list(emb.embed(texts)))
    np.save(fp, arr)
    return arr


def main():
    queries, docs = load_data()
    slugs = sorted(docs)
    corpus = ['{0} {0} {0} {1} {2}'.format(docs[s][0], docs[s][1], docs[s][2]) for s in slugs]
    qtexts = [q for q, _ in queries]
    golds = [[g for g in gold if g in docs] for _, gold in queries]
    n = len(slugs)
    print('corpus {0} skills / {1} queries'.format(n, len(queries)))

    for model in MODELS:
        key = model.replace('/', '_')
        X = embed(model, corpus, key + '_corpus')
        qp = Q_PREFIX.get(model, '')
        Q = embed(model, [qp + q for q in qtexts], key + '_queries_v2')
        Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
        Qn = Q / np.linalg.norm(Q, axis=1, keepdims=True)
        S = Qn @ Xn.T                                    # [107, 994] 余弦相似度
        print()
        print('=== {0} (dim={1}) ==='.format(model, X.shape[1]))
        print('tau     剔除率    recall   (剔除率=各查询保留 sim>=tau 后平均削减比例)')
        for tau in TAUS:
            keep_ratios, recall = [], 0
            for i in range(len(queries)):
                kept = S[i] >= tau
                keep_ratios.append(kept.sum() / n)
                gi = [slugs.index(g) for g in golds[i]]
                recall += any(kept[j] for j in gi)
            print('{0:.2f}  {1:7.1%}  {2:6.1%}'.format(tau, 1 - np.mean(keep_ratios), recall / len(queries)))
        # 100% recall 对应的最大剔除率
        best = None
        for tau in TAUS:
            ok, ratios = True, []
            for i in range(len(queries)):
                kept = S[i] >= tau
                ratios.append(kept.sum() / n)
                gi = [slugs.index(g) for g in golds[i]]
                if not any(kept[j] for j in gi):
                    ok = False
                    break
            if ok:
                best = (tau, 1 - np.mean(ratios))
        if best:
            print('>> 100% recall 最大剔除率: {0:.1%} (tau={1})'.format(best[1], best[0]))
        else:
            print('>> 所有 tau 均无法 100% recall')


if __name__ == '__main__':
    main()
