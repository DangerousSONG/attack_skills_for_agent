# -*- coding: utf-8 -*-
r"""skill_route — L1+L2+L3 三层漏斗统一入口（给渗透 Agent 的一次性调用工具）

输入任务描述, 输出 JSON: 推荐 skill 列表 / 命中来源 / 是否弃权。
Agent 用法(注册层 attack-skill-router 已改为调本工具, 不再人肉读索引):
  python scripts/skill_route.py "Kerberoasting 导出服务账户票据并破解"
  python scripts/skill_route.py "..." --top 5 --rerank llm --model qwen3.8-flash
  python scripts/skill_route.py "..." --coarse --tau 0.45          # 万级规模: embedding 粗筛后进 L2
  python scripts/skill_route.py "..." --rerank local               # 本地 bge-reranker-v2-m3 重排(离线)

漏斗:
  L0c 粗筛(可选, --coarse): Qwen3-Embedding-0.6B-Q 余弦>=tau 才进 L2
      (994 skills 实测 tau=0.40 剔除 75.6% 且 recall 100%, 见 exp_l1_sweep.py;
       L2 并集自动加入 embedding 余弦第三路, 见 eval_pipeline.py 全链路结果)
  L1  字典实体匹配(entity_registry.json): CVE 正则/工具别名命中即置顶, 零成本, 不受粗筛影响
  L2  混合召回(skill_retrieval 同款): TF-IDF top-K ∪ BM25(字+词) top-K, 轮询交错
  L3  重排(可插拔):
      none  直接用 L2 交错序(默认, 零依赖零成本)
      llm   千问/GLM flash 点对点 1-5 打分(需 TENSORIS_API_KEY 环境变量, 走网关)
      local 本地 bge-reranker-v2-m3-int8(fastembed, 首次自动下载 0.57GB, 之后离线)

可弃权: L3 开启时无强相关候选 -> abstain=true, Agent 应裸跑(永不差于基线)。
  llm: Top-N 无 >=4 分; local: 最高分 < 0 (bge-reranker logit 口径)。

依赖: scikit-learn, scipy, rank_bm25; --coarse/--rerank local 需 fastembed(懒加载, 默认路径不触发);
      --rerank llm 时需网关 key; 索引先 build。
"""
import argparse, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
# 索引/字典解析顺序: 本目录(部署态 _router/) -> 仓库 scripts/(开发态)
INDEX_PKL = next((p for p in (os.path.join(HERE, '_retrieval_index.pkl'),
                              os.path.join(ROOT, 'scripts', '_retrieval_index.pkl'))
                  if os.path.exists(p)), os.path.join(HERE, '_retrieval_index.pkl'))
REGISTRY = next((p for p in (os.path.join(HERE, 'entity_registry.json'),
                             os.path.join(ROOT, 'scripts', 'entity_registry.json'))
                 if os.path.exists(p)), os.path.join(HERE, 'entity_registry.json'))
CVE_RE = re.compile(r'CVE-\d{4}-\d{4,7}', re.I)

# ---- L0c 粗筛(可选, 懒加载) ----
COARSE_MODEL = os.environ.get('SKILL_COARSE_MODEL', 'Qwen/Qwen3-Embedding-0.6B-Q')
COARSE_TAU = 0.40                      # exp_l1_sweep 标定: 100% recall 下最大剔除率对应阈值
Q_PREFIX = {
    'Qwen/Qwen3-Embedding-0.6B-Q': 'Instruct: Given a web search query, retrieve relevant passages that answer the query\nQuery: ',
    'BAAI/bge-small-zh-v1.5': '为这个句子生成表示以用于检索相关文章：',
}
COARSE_CACHE_DIR = os.path.join(HERE, '_coarse_cache')
_RERANK_MODEL = os.environ.get('SKILL_RERANKER', 'BAAI/bge-reranker-v2-m3-int8')
_coarse_state = {}                     # {model: (slugs, Xn)} 进程内单例
_reranker = None


def _coarse_corpus(slugs, docs):
    """语料 embedding, 按 slug 清单对齐 + manifest 校验, 缓存 scripts/_coarse_cache/"""
    import hashlib
    import numpy as np
    from skill_retrieval import corpus_text
    os.makedirs(COARSE_CACHE_DIR, exist_ok=True)
    key = COARSE_MODEL.replace('/', '_')
    manifest = os.path.join(COARSE_CACHE_DIR, key + '.manifest.json')
    fp = os.path.join(COARSE_CACHE_DIR, key + '.npy')
    if os.path.exists(fp) and os.path.exists(manifest):
        if json.load(open(manifest, encoding='utf-8'))['slugs'] == list(slugs):
            X = np.load(fp)
            return X / np.linalg.norm(X, axis=1, keepdims=True)
        print('粗筛缓存 slug 清单与索引不一致, 重新嵌入...', file=sys.stderr)
    print('首次粗筛: 加载 {0} 并嵌入 {1} 条语料(约 1-3 分钟, 之后走缓存)...'.format(COARSE_MODEL, len(slugs)),
          file=sys.stderr)
    from fastembed import TextEmbedding
    emb = TextEmbedding(COARSE_MODEL)
    X = np.array(list(emb.embed([corpus_text(docs[s]) for s in slugs])), dtype=np.float32)
    np.save(fp, X)
    with open(manifest, 'w', encoding='utf-8') as f:
        json.dump({'model': COARSE_MODEL, 'slugs': list(slugs)}, f, ensure_ascii=False)
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def l0c_coarse_mask(text, slugs, docs, tau):
    """L0c: embedding 余弦 >= tau 的保留, 返回 (keep_mask, kept_count, sim)"""
    import numpy as np
    key = COARSE_MODEL
    if key not in _coarse_state:
        _coarse_state[key] = (list(slugs), _coarse_corpus(slugs, docs))
    c_slugs, Xn = _coarse_state[key]
    if c_slugs != list(slugs):
        _coarse_state[key] = (list(slugs), _coarse_corpus(slugs, docs))
        c_slugs, Xn = _coarse_state[key]
    from fastembed import TextEmbedding
    emb = TextEmbedding(COARSE_MODEL)
    q = np.array(list(emb.embed([Q_PREFIX.get(COARSE_MODEL, '') + text])), dtype=np.float32)[0]
    qn = q / np.linalg.norm(q)
    sim = Xn @ qn
    keep = sim >= tau
    return keep, int(keep.sum()), sim


def load_index():
    if not os.path.exists(INDEX_PKL):
        raise SystemExit('索引不存在: 先运行 python scripts/skill_retrieval.py build')
    import pickle
    with open(INDEX_PKL, 'rb') as f:
        idx = pickle.load(f)
    return idx['slugs'], idx['vec_w'], idx['vec_c'], idx['X'], idx['bm25']


def l1_dict_match(text, slugs):
    """L1: CVE 正则/俗名别名 + 工具别名命中, 返回 (hit_slugs, matched_entities)"""
    if not os.path.exists(REGISTRY):
        return [], []
    reg = json.load(open(REGISTRY, encoding='utf-8'))
    low = text.lower()
    hits, ents = [], []
    for e in reg['entities']:
        if e['type'] == 'cve':
            cve_hit = any(m.upper() == e['value'] for m in CVE_RE.findall(text))
            alias_hit = any(a.lower() in low for a in e.get('aliases', []))
            if cve_hit or alias_hit:
                hits += e['skills']; ents.append(e['value'])
        elif e['type'] == 'tool':
            names = [e['value']] + e.get('aliases', [])
            if any(n.lower() in low for n in names):
                hits += e['skills']; ents.append(e['value'])
    seen = set()
    uniq = [s for s in hits if not (s in seen or seen.add(s))]
    eseen = set()
    uents = [s for s in ents if not (s in eseen or eseen.add(s))]
    return [s for s in uniq if s in set(slugs)], uents


def l2_recall(text, slugs, vec_w, vec_c, X, bm25, k, mask=None, third=None):
    """L2: TF-IDF ∪ BM25 (粗筛时再加 embedding 余弦第三路) 并集, 轮询交错序(TF-IDF 优先)
    mask=粗筛保留布尔数组(可选); third=粗筛余弦相似度数组(可选, 仅在 mask 开启时有意义)"""
    import numpy as np
    from scipy.sparse import hstack
    q = hstack([vec_w.transform([text]), vec_c.transform([text])])
    sim = (q @ X.T).toarray()[0]
    ana_w, ana_c = vec_w.build_analyzer(), vec_c.build_analyzer()
    bms = bm25.get_scores(ana_w(text) + ana_c(text))
    if mask is not None:
        sim = np.where(mask, sim, -np.inf)
        bms = np.where(mask, bms, -np.inf)
    t_k = list(np.argsort(-sim)[:k]); b_k = list(np.argsort(-bms)[:k])
    pools = [t_k, b_k]
    if third is not None:
        pools.append(list(np.argsort(-third)[:k]))
    merged, pools = [], [p[:] for p in pools]
    while any(pools):
        for pool in pools:
            while pool and pool[0] in merged:
                pool.pop(0)
            if pool:
                merged.append(pool.pop(0))
    return [slugs[j] for j in merged]


def l3_llm_rerank(text, cands, docs, model):
    """L3(llm): 网关 flash 点对点 1-5 分; 返回 (ordered, scored, error)"""
    api_key = os.environ.get('TENSORIS_API_KEY')
    if not api_key:
        raise SystemExit('缺 TENSORIS_API_KEY 环境变量(或用 --rerank none)')
    import time, urllib.request
    base = os.environ.get('TENSORIS_BASE', 'https://api.tensoris.ai/v1')
    items = []
    for i, c in enumerate(cands):
        name, desc = docs[c][0], docs[c][1]
        desc = desc if len(desc) <= 300 else desc[:300]
        items.append('[{0}] {1} — {2}: {3}'.format(i + 1, c, name, desc))
    sys_prompt = ('你是渗透测试技能路由专家。给定用户任务和候选技能列表,为每个候选打相关性分数:'
                  '5=完成该任务的核心工具,4=强相关,3=部分相关,2=弱相关,1=无关。'
                  '只输出JSON对象,格式 {"scores":[{"id":候选序号,"score":1到5整数},...]},'
                  '必须覆盖每一个候选,不要输出任何其他内容。')
    payload = {'model': model, 'temperature': 0,
               'messages': [{'role': 'system', 'content': sys_prompt},
                            {'role': 'user', 'content': '任务:{0}\n\n候选技能:\n{1}'.format(text, '\n'.join(items))}]}
    req = urllib.request.Request(base + '/chat/completions',
                                 data=json.dumps(payload).encode('utf-8'),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + api_key.strip()})
    with urllib.request.urlopen(req, timeout=180) as resp:
        j = json.loads(resp.read().decode('utf-8', 'replace'))
    m = re.search(r'\{.*\}', j['choices'][0]['message']['content'], re.S)
    smap = {}
    for it in json.loads(m.group(0)).get('scores', []):
        try:
            smap[int(it['id']) - 1] = float(it['score'])
        except Exception:
            pass
    scored = sorted(((smap.get(i, 0.0), c) for i, c in enumerate(cands)), reverse=True)
    return [c for _, c in scored], scored, None


def l3_local_rerank(text, cands, docs):
    """L3(local): 本地 bge-reranker-v2-m3-int8 交叉打分; 返回 (ordered, scored, error)"""
    global _reranker
    if _reranker is None:
        from fastembed.rerank.cross_encoder import TextCrossEncoder
        print('首次本地重排: 加载 {0}(权重缺失时自动下载, 之后离线)...'.format(_RERANK_MODEL), file=sys.stderr)
        _reranker = TextCrossEncoder(_RERANK_MODEL)
    doctexts = ['{0}: {1}'.format(docs[c][0], docs[c][1] if len(docs[c][1]) <= 400 else docs[c][1][:400])
                for c in cands]
    scores = list(_reranker.rerank(text, doctexts, batch_size=32))
    scored = sorted(zip(scores, cands), reverse=True)
    return [c for _, c in scored], scored, None


def main():
    ap = argparse.ArgumentParser(description='L1+L2+L3 skill 路由工具')
    ap.add_argument('text', help='任务描述(自然语言)')
    ap.add_argument('--top', type=int, default=5, help='最终输出个数(默认 5)')
    ap.add_argument('--cand', type=int, default=20, help='L2 每路召回 top-K(默认 20)')
    ap.add_argument('--rerank', choices=['none', 'llm', 'local'], default='none', help='L3 重排方式')
    ap.add_argument('--coarse', action='store_true', help='L0c embedding 粗筛后再进 L2(万级规模启用, 默认关)')
    ap.add_argument('--tau', type=float, default=COARSE_TAU, help='粗筛余弦阈值(默认 0.40, 标定见 exp_l1_sweep)')
    ap.add_argument('--model', default='qwen3.8-flash', help='--rerank llm 的模型名')
    ap.add_argument('--docs', action='store_true', help='输出含 description 全文(注入上下文用)')
    a = ap.parse_args()

    slugs, vec_w, vec_c, X, bm25 = load_index()
    docs = {}
    if a.rerank in ('llm', 'local') or a.docs or a.coarse:
        from skill_retrieval import load_corpus
        docs = load_corpus()

    l1_hits, l1_ents = l1_dict_match(a.text, slugs)
    mask, kept, third = None, len(slugs), None
    if a.coarse:
        mask, kept, third = l0c_coarse_mask(a.text, slugs, docs, a.tau)
        for s in l1_hits:               # 字典命中不受粗筛约束
            mask[slugs.index(s)] = True
    cands = l2_recall(a.text, slugs, vec_w, vec_c, X, bm25, a.cand, mask, third)
    for s in l1_hits:                   # L1 命中置顶, 保持 L2 序补位
        if s in cands:
            cands.remove(s)
        cands.insert(0, s)
    cands = cands[:max(a.cand, a.top)]

    source = 'l1' if l1_hits else 'l2'
    if a.coarse:
        source = 'l0c({0}/{1})+'.format(kept, len(slugs)) + source
    abstain, scores = False, None
    if a.rerank == 'llm':
        cands, scores, err = l3_llm_rerank(a.text, cands, docs, a.model)
        source += '+l3llm'
        if not any(s >= 4 for s, _ in scores[:a.top]):
            abstain = True
    elif a.rerank == 'local':
        cands, scores, err = l3_local_rerank(a.text, cands, docs)
        source += '+l3local'
        if scores and scores[0][0] < 0:     # bge-reranker logit 口径: 最高分为负=全员不相关
            abstain = True
    else:
        source += '(no-rerank)'

    out = {'query': a.text, 'skills': cands[:a.top], 'source': source,
           'l1_entities': l1_ents, 'abstain': abstain}
    if a.docs:
        out['descriptions'] = {s: docs[s][1] for s in out['skills']}
    if scores:
        out['scores'] = {c: s for s, c in scores[:a.top]}
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
