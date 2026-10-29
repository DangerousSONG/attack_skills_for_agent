# -*- coding: utf-8 -*-
"""A/B/C 三组检索对比实验: TF-IDF 基线 / +LLM重排 / 混合向量召回+重排
A: TF-IDF top20 (复现基线)
B: TF-IDF top20 -> flash LLM 点对点重排
C0(诊断): 向量 top20 召回率 (默认 bge-small-zh-v1.5, 可换 bge-m3)
C: (TF-IDF top20 ∪ 向量 top50) -> flash LLM 重排

用法:
  python exp_rerank.py ab|b|vec|c|a [模型名...] [--key-file PATH]

可配置项(全部环境变量, 同事用自己的 key 零改代码):
  TENSORIS_API_KEY   API key 明文(推荐方式, 不落盘)
  TENSORIS_KEY_FILE  存放 key 的文件路径(备选, 或命令行 --key-file)
  TENSORIS_BASE      网关地址, 默认 https://api.tensoris.ai/v1
  TENSORIS_MODELS    重排模型, 逗号分隔, 默认 glm-5.3-flash,qwen3.8-flash
  SKILLS_REPO        skills 仓库路径, 默认取脚本所在仓库(scripts/ 的上一级)

示例:
  set TENSORIS_API_KEY=sk-xxx   (Windows)  或  export TENSORIS_API_KEY=sk-xxx
  python scripts/exp_rerank.py b qwen3.8-flash
"""
import ast, json, os, re, sys, time
import numpy as np

REPO = os.environ.get('SKILLS_REPO', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.environ.get('TENSORIS_BASE', 'https://api.tensoris.ai/v1')
MODELS = [m.strip() for m in os.environ.get('TENSORIS_MODELS', 'glm-5.3-flash,qwen3.8-flash').split(',') if m.strip()]
WS = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = os.path.join(WS, '_exp_cache.json')
VEC_PATH = os.path.join(WS, '_vec_index.npz')
SCORES_PATH = os.path.join(WS, '_exp_scores.json')
REGISTERED = {'attack-skill-router', 'engagement-discipline', 'java-deserialization-gadget-selector'}


def _parse_key_file_arg():
    """从 argv 中提取并移除 --key-file PATH, 使位置参数解析不受影响"""
    if '--key-file' in sys.argv:
        i = sys.argv.index('--key-file')
        path = sys.argv[i + 1]
        del sys.argv[i:i + 2]
        return path
    return None


_KEY_FILE_ARG = _parse_key_file_arg()


def load_api_key():
    """key 只从环境变量/参数读取, 永不硬编码、永不写入任何文件"""
    key = os.environ.get('TENSORIS_API_KEY')
    if key:
        return key.strip()
    kf = _KEY_FILE_ARG or os.environ.get('TENSORIS_KEY_FILE')
    if kf and os.path.exists(kf):
        return open(kf, encoding='utf-8').read().strip()
    raise SystemExit('缺少 API key: 请设置环境变量 TENSORIS_API_KEY, 或用 --key-file / TENSORIS_KEY_FILE 指定 key 文件路径')


def load_queries():
    src = open(os.path.join(REPO, 'scripts', 'eval_recall.py'), encoding='utf-8').read()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if getattr(t, 'id', '') == 'QUERIES':
                    return ast.literal_eval(node.value)
    raise RuntimeError('QUERIES not found in eval_recall.py')


def load_skills():
    docs = {}
    for dp, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d != '.git']
        if 'SKILL.md' not in files:
            continue
        slug = os.path.relpath(dp, REPO).replace(os.sep, '/')
        parts = slug.split('/')
        if parts[0] in REGISTERED or len(parts) < 2 or parts[0] == 'scripts':
            continue
        s = open(os.path.join(dp, 'SKILL.md'), encoding='utf-8', errors='replace').read()
        fm = re.search(r'^---\n(.*?)\n---', s, re.S)
        if not fm:
            continue
        dm = re.search(r'^description:\s*(.+)$', fm.group(1), re.M)
        nm = re.search(r'^name:\s*(.+)$', fm.group(1), re.M)
        if not dm:
            continue
        docs[parts[-1]] = (nm.group(1).strip() if nm else parts[-1], dm.group(1).strip())
    return docs


def tfidf_top(docs, queries, topn=20):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from scipy.sparse import hstack
    slugs = sorted(docs)
    corpus = ['{0} {0} {0} {1}'.format(docs[s][0], docs[s][1]) for s in slugs]
    vw = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    vc = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5), min_df=1)
    X = hstack([vw.fit_transform(corpus), vc.fit_transform(corpus)])
    Q = hstack([vw.transform(queries), vc.transform(queries)])
    sim = (Q @ X.T).toarray()
    return slugs, [[slugs[j] for j in np.argsort(-sim[i])[:topn]] for i in range(len(queries))]


# ---------------- LLM rerank ----------------

def _cache():
    if os.path.exists(CACHE_PATH):
        return json.load(open(CACHE_PATH, encoding='utf-8'))
    return {}


def _save_cache(c):
    json.dump(c, open(CACHE_PATH, 'w', encoding='utf-8'), ensure_ascii=False)


def llm_scores(model, query, cands, docs, cache):
    import hashlib
    ckey = hashlib.md5(json.dumps(cands, ensure_ascii=False).encode('utf-8')).hexdigest()[:10]
    ck = model + '|' + query + '|' + ckey
    if ck in cache:
        return cache[ck], 0.0, None
    items = []
    for i, c in enumerate(cands):
        name, desc = docs[c]
        desc = desc if len(desc) <= 300 else desc[:300]
        items.append('[{0}] {1} — {2}: {3}'.format(i + 1, c, name, desc))
    sys_prompt = ('你是渗透测试技能路由专家。给定用户任务和候选技能列表,为每个候选打相关性分数:'
                  '5=完成该任务的核心工具,4=强相关可用于该任务,3=部分相关,2=弱相关,1=无关。'
                  '只输出JSON对象,格式 {"scores":[{"id":候选序号,"score":1到5整数},...]},'
                  '必须覆盖列表中的每一个候选,不要输出任何其他内容。')
    user = '任务:{0}\n\n候选技能:\n{1}'.format(query, '\n'.join(items))
    key = load_api_key()
    payload = {'model': model, 'temperature': 0,
               'messages': [{'role': 'system', 'content': sys_prompt},
                            {'role': 'user', 'content': user}]}
    last_err = None
    for attempt in range(4):
        t0 = time.time()
        try:
            r = requests_post(payload, key)
            dt = time.time() - t0
            if r.status != 200:
                last_err = 'HTTP {0}: {1}'.format(r.status, r.body[:200])
                if r.status in (429, 500, 502, 503):
                    time.sleep(5 * (attempt + 1))
                    continue
                break
            j = json.loads(r.body)
            txt = j['choices'][0]['message']['content']
            m = re.search(r'\{.*\}', txt, re.S)
            data = json.loads(m.group(0))
            smap = {}
            for it in data.get('scores', []):
                try:
                    idx = int(it.get('id')) - 1
                    smap[idx] = float(it.get('score'))
                except Exception:
                    pass
            scores = [smap.get(i, 0.0) for i in range(len(cands))]
            usage = j.get('usage', {})
            entry = {'scores': scores, 'prompt_tokens': usage.get('prompt_tokens'),
                     'completion_tokens': usage.get('completion_tokens'), 'latency': round(dt, 3)}
            cache[ck] = entry
            return entry, dt, None
        except Exception as e:
            last_err = repr(e)[:300]
            time.sleep(5 * (attempt + 1))
    return None, 0.0, last_err


class _Resp:
    def __init__(self, status, body):
        self.status, self.body = status, body


def requests_post(payload, key):
    import urllib.request
    req = urllib.request.Request(BASE + '/chat/completions',
                                 data=json.dumps(payload).encode('utf-8'),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + key})
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return _Resp(resp.status, resp.read().decode('utf-8', 'replace'))
    except urllib.error.HTTPError as e:
        return _Resp(e.code, e.read().decode('utf-8', 'replace'))


def recall_metrics(queries, ranked_lists):
    hits5 = hits20 = 0
    n = 0
    missing = []
    fails = []  # 金标不在候选集里(召回失败)
    for (q, gold), lst in zip(queries, ranked_lists):
        gold = [g for g in gold]
        n += 1
        top5 = set(lst[:5])
        top20 = set(lst[:20])
        h5 = any(g in top5 for g in gold)
        h20 = any(g in top20 for g in gold)
        hits5 += h5
        hits20 += h20
        if not any(g in lst for g in gold):
            fails.append(q)
    return hits5 / n, hits20 / n, fails


def apply_rerank(model, queries, cand_lists, docs, cache):
    """对每条查询的候选重排, 返回重排后的 slug 列表"""
    ranked, lat, ptok, ctok, errs = [], [], 0, 0, []
    from concurrent.futures import ThreadPoolExecutor
    def work(arg):
        i, (q, _) = arg
        entry, dt, err = llm_scores(model, q, cand_lists[i], docs, cache)
        return i, entry, dt, err
    with ThreadPoolExecutor(max_workers=10) as ex:
        for i, entry, dt, err in ex.map(work, list(enumerate(queries))):
            _save_cache(cache)  # 增量落盘, 超时/崩溃不丢进度
            if err or entry is None or len(entry.get('scores', [])) != len(cand_lists[i]):
                if entry is not None and not err:
                    errs.append((queries[i][0], 'score_len_mismatch'))
                elif err:
                    errs.append((queries[i][0], err))
                ranked.append(cand_lists[i])
                continue
            order = sorted(range(len(cand_lists[i])), key=lambda k: -entry['scores'][k])
            ranked.append([cand_lists[i][k] for k in order])
            lat.append(entry['latency'])
            ptok += entry['prompt_tokens'] or 0
            ctok += entry['completion_tokens'] or 0
    return ranked, {'avg_latency_ms': round(1000 * sum(lat) / max(len(lat), 1), 1),
                    'prompt_tokens': ptok, 'completion_tokens': ctok,
                    'n_req': len(lat), 'errors': errs}


def main():
    stage = sys.argv[1] if len(sys.argv) > 1 else 'ab'
    queries = load_queries()
    docs = load_skills()
    qs = [q for q, _ in queries]
    print('查询 {0} 条, skills {1} 个'.format(len(queries), len(docs)))
    cache = _cache()

    if stage in ('ab', 'a'):
        slugs, tf_lists = tfidf_top(docs, qs, 20)
        r5, r20, fails = recall_metrics(queries, tf_lists)
        print('[A] TF-IDF基线        Recall@5={0:.1%}  Recall@20={1:.1%}'.format(r5, r20))
        if stage == 'a':
            return

    if stage in ('ab', 'b'):
        slugs, tf_lists = tfidf_top(docs, qs, 20)
        models = sys.argv[2:] if len(sys.argv) > 2 else MODELS
        for model in models:
            t0 = time.time()
            ranked, info = apply_rerank(model, queries, tf_lists, docs, cache)
            _save_cache(cache)
            r5, r20, fails = recall_metrics(queries, ranked)
            print('[B] {0}  Recall@5={1:.1%}  Recall@20={2:.1%}  avg延迟={3}ms  输入token={4} 输出token={5} 错误={6} 耗时{7:.0f}s'.format(
                model, r5, r20, info['avg_latency_ms'], info['prompt_tokens'],
                info['completion_tokens'], len(info['errors']), time.time() - t0))
            if info['errors']:
                print('   错误样例:', info['errors'][:3])
        return

    if stage == 'vec':
        from fastembed import TextEmbedding
        vec_model = sys.argv[2] if len(sys.argv) > 2 else 'BAAI/bge-m3'
        print('加载 {0} ...'.format(vec_model))
        emb = TextEmbedding(vec_model)
        slugs = sorted(docs)
        texts = ['{0}: {1}'.format(docs[s][0], docs[s][1]) for s in slugs]
        t0 = time.time()
        D = np.array(list(emb.embed(texts)), dtype=np.float32)
        Q = np.array(list(emb.embed(qs)), dtype=np.float32)
        print('编码完成 {0:.0f}s, D={1}, Q={2}'.format(time.time() - t0, D.shape, Q.shape))
        Dn = D / np.linalg.norm(D, axis=1, keepdims=True)
        Qn = Q / np.linalg.norm(Q, axis=1, keepdims=True)
        sim = Qn @ Dn.T
        np.savez_compressed(VEC_PATH, sim=sim, slugs=np.array(slugs))
        vec_lists = [[slugs[j] for j in np.argsort(-sim[i])[:50]] for i in range(len(qs))]
        r5, r20, fails = recall_metrics(queries, [[s for s in lst[:20]] for lst in vec_lists])
        print('[C0] 纯向量top20      Recall@5={0:.1%}  Recall@20={1:.1%}'.format(r5, r20))
        return

    if stage == 'c':
        z = np.load(VEC_PATH, allow_pickle=True)
        sim, vslugs = z['sim'], list(z['slugs'])
        slugs, tf_lists = tfidf_top(docs, qs, 20)
        assert vslugs == slugs, 'slug 顺序不一致'
        union_lists = []
        for i in range(len(qs)):
            vtop = [vslugs[j] for j in np.argsort(-sim[i])[:50]]
            seen, u = set(), []
            for s in tf_lists[i] + vtop:
                if s not in seen:
                    seen.add(s)
                    u.append(s)
            union_lists.append(u)
        # 候选集内召回复核
        in_cand = sum(1 for (q, gold), u in zip(queries, union_lists) if any(g in u for g in gold))
        print('混合候选集(并集)内召回: {0}/{1} = {2:.1%}, 平均候选数 {3:.0f}'.format(
            in_cand, len(queries), in_cand / len(queries), np.mean([len(u) for u in union_lists])))
        scores_dump = {}
        for model in MODELS:
            t0 = time.time()
            ranked, info = apply_rerank(model, queries, union_lists, docs, cache)
            _save_cache(cache)
            r5, r20, fails = recall_metrics(queries, ranked)
            print('[C] {0}  Recall@5={1:.1%}  Recall@20={2:.1%}  avg延迟={3}ms  输入token={4} 输出token={5} 错误={6} 耗时{7:.0f}s'.format(
                model, r5, r20, info['avg_latency_ms'], info['prompt_tokens'],
                info['completion_tokens'], len(info['errors']), time.time() - t0))
            if fails:
                print('   并集仍漏召:', fails)
        return

    print('unknown stage', stage)


if __name__ == '__main__':
    main()
