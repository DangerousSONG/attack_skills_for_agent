# -*- coding: utf-8 -*-
r"""skill_route — L1+L2+L3 三层漏斗统一入口（给渗透 Agent 的一次性调用工具）

输入任务描述, 输出 JSON: 推荐 skill 列表 / 命中来源 / 是否弃权。
Agent 用法(注册层 attack-skill-router 已改为调本工具, 不再人肉读索引):
  python scripts/skill_route.py "Kerberoasting 导出服务账户票据并破解"
  python scripts/skill_route.py "..." --top 5 --rerank llm --model qwen3.8-flash

漏斗:
  L1  字典实体匹配(entity_registry.json): CVE 正则/工具别名命中即置顶, 零成本
  L2  混合召回(skill_retrieval 同款): TF-IDF top-K ∪ BM25(字+词) top-K, 轮询交错
  L3  重排(可插拔):
      none  直接用 L2 交错序(默认, 零依赖零成本)
      llm   千问/GLM flash 点对点打分(需 TENSORIS_API_KEY 环境变量, 走网关)
      local 本地 bge-reranker-v2-m3(离线, 需自行提供 onnx 权重, 接口预留)

可弃权: L3 开启时, Top-N 无 >=4 分候选 -> abstain=true, Agent 应裸跑(永不差于基线)。

依赖: scikit-learn, scipy, rank_bm25; --rerank llm 时需网关 key; 索引先 build。
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


def load_index():
    if not os.path.exists(INDEX_PKL):
        raise SystemExit('索引不存在: 先运行 python scripts/skill_retrieval.py build')
    import pickle
    with open(INDEX_PKL, 'rb') as f:
        idx = pickle.load(f)
    return idx['slugs'], idx['vec_w'], idx['vec_c'], idx['X'], idx['bm25']


def l1_dict_match(text, slugs):
    """L1: CVE 正则 + 工具别名命中, 返回 (hit_slugs, matched_entities)"""
    if not os.path.exists(REGISTRY):
        return [], []
    reg = json.load(open(REGISTRY, encoding='utf-8'))
    low = text.lower()
    hits, ents = [], []
    for e in reg['entities']:
        if e['type'] == 'cve':
            for m in CVE_RE.findall(text):
                if m.upper() == e['value']:
                    hits += e['skills']; ents.append(e['value'])
        elif e['type'] == 'tool':
            names = [e['value']] + e.get('aliases', [])
            if any(n.lower() in low for n in names):
                hits += e['skills']; ents.append(e['value'])
    seen = set()
    uniq = [s for s in hits if not (s in seen or seen.add(s))]
    return [s for s in uniq if s in set(slugs)], ents


def l2_recall(text, slugs, vec_w, vec_c, X, bm25, k):
    """L2: TF-IDF ∪ BM25 并集, 轮询交错序(TF-IDF 优先)"""
    import numpy as np
    from scipy.sparse import hstack
    q = hstack([vec_w.transform([text]), vec_c.transform([text])])
    sim = (q @ X.T).toarray()[0]
    ana_w, ana_c = vec_w.build_analyzer(), vec_c.build_analyzer()
    bms = bm25.get_scores(ana_w(text) + ana_c(text))
    t_k = list(np.argsort(-sim)[:k]); b_k = list(np.argsort(-bms)[:k])
    merged, pt, pb = [], t_k[:], b_k[:]
    while pt or pb:
        for pool in (pt, pb):
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
        name, desc = docs[c]
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


def main():
    ap = argparse.ArgumentParser(description='L1+L2+L3 skill 路由工具')
    ap.add_argument('text', help='任务描述(自然语言)')
    ap.add_argument('--top', type=int, default=5, help='最终输出个数(默认 5)')
    ap.add_argument('--cand', type=int, default=20, help='L2 每路召回 top-K(默认 20)')
    ap.add_argument('--rerank', choices=['none', 'llm', 'local'], default='none', help='L3 重排方式')
    ap.add_argument('--model', default='qwen3.8-flash', help='--rerank llm 的模型名')
    ap.add_argument('--docs', action='store_true', help='输出含 description 全文(注入上下文用)')
    a = ap.parse_args()

    slugs, vec_w, vec_c, X, bm25 = load_index()
    docs = {}
    if a.rerank in ('llm',) or a.docs:
        from skill_retrieval import load_corpus
        docs = load_corpus()

    l1_hits, l1_ents = l1_dict_match(a.text, slugs)
    cands = l2_recall(a.text, slugs, vec_w, vec_c, X, bm25, a.cand)
    for s in l1_hits:                       # L1 命中置顶, 保持 L2 序补位
        if s in cands:
            cands.remove(s)
        cands.insert(0, s)
    cands = cands[:max(a.cand, a.top)]

    source = 'l1' if l1_hits else 'l2'
    abstain, scores = False, None
    if a.rerank == 'llm':
        cands, scores, err = l3_llm_rerank(a.text, cands, docs, a.model)
        source += '+l3llm'
        if not any(s >= 4 for s, _ in scores[:a.top]):
            abstain = True
    elif a.rerank == 'local':
        raise SystemExit('--rerank local 接口预留: 需本地 bge-reranker-v2-m3 onnx 权重(见交接文档)')
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
