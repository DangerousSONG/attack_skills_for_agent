# -*- coding: utf-8 -*-
# 批量翻译 SKILL.md frontmatter description 为英文(统一英文口径)
# 用法: python scripts/translate_descriptions.py [--limit N] [--apply]
#   默认 dry-run 只打印计划; --apply 才写回。缓存 _trans_cache.json 支持断点续跑。
# key: TENSORIS_API_KEY 或 TENSORIS_KEY_FILE 环境变量, 模型 TENSORIS_MODEL 默认 qwen3.8-flash
import io, json, os, re, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'scripts', '_trans_cache.json')
REGISTERED = {'scripts'}
BATCH = 50
MODEL = os.environ.get('TENSORIS_MODEL', 'qwen3.8-flash')
BASE = os.environ.get('TENSORIS_BASE', 'https://api.tensoris.ai/v1')


def load_key():
    key = os.environ.get('TENSORIS_API_KEY')
    if key:
        return key.strip()
    kf = os.environ.get('TENSORIS_KEY_FILE')
    if kf and os.path.exists(kf):
        return open(kf, encoding='utf-8').read().strip()
    raise SystemExit('缺 key: 设 TENSORIS_API_KEY 或 TENSORIS_KEY_FILE')


def find_targets():
    """所有含中文的 description -> [(path, slug, desc)]"""
    out = []
    for dp, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ('.git', '_before_tmp')]
        if 'SKILL.md' not in files:
            continue
        rel = os.path.relpath(dp, ROOT).replace(os.sep, '/')
        if rel.split('/')[0] in REGISTERED or rel.startswith('.git'):
            continue
        p = os.path.join(dp, 'SKILL.md')
        s = io.open(p, encoding='utf-8', errors='replace').read()
        fm = re.search(r'^---\n(.*?)\n---', s, re.S)
        if not fm:
            continue
        m = re.search(r'^description:\s*(.+?)$', fm.group(1), re.M)
        if not m:
            continue
        desc = m.group(1).strip().strip('"').strip("'")
        if re.search(r'[\u4e00-\u9fff]', desc):
            out.append((p, rel.split('/')[-1], desc))
    return out


def translate_batch(key, items):
    """items=[(slug, desc)] -> {slug: english_desc}; 失败返回 None"""
    import urllib.request
    payload_txt = '\n'.join('[{0}] {1}'.format(i + 1, d) for i, (_, d) in enumerate(items))
    sys_prompt = ('You are a technical translator for a cybersecurity skill library. '
                  'Translate each description to concise English. Rules: '
                  '1) Keep the same structure: one sentence summary, then "Signals: " followed by comma-separated trigger keywords (translate the signal keywords too). '
                  '2) Keep cybersecurity terminology precise (CVE IDs, tool names, protocol names stay as-is). '
                  '3) Total under 60 words. 4) Output ONLY a JSON object: {"translations": [{"id": 1, "text": "..."}, ...]} covering every item.')
    payload = {'model': MODEL, 'temperature': 0,
               'messages': [{'role': 'system', 'content': sys_prompt},
                            {'role': 'user', 'content': 'Descriptions:\n' + payload_txt}]}
    req = urllib.request.Request(BASE + '/chat/completions',
                                 data=json.dumps(payload).encode('utf-8'),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + key})
    with urllib.request.urlopen(req, timeout=180) as resp:
        j = json.loads(resp.read().decode('utf-8', 'replace'))
    m = re.search(r'\{.*\}', j['choices'][0]['message']['content'], re.S)
    data = json.loads(m.group(0))
    out = {}
    for t in data.get('translations', []):
        try:
            idx = int(t['id']) - 1
            out[items[idx][0]] = t['text'].strip().strip('"')
        except Exception:
            pass
    return out if len(out) == len(items) else None


def main():
    apply_mode = '--apply' in sys.argv
    limit = None
    if '--limit' in sys.argv:
        limit = int(sys.argv[sys.argv.index('--limit') + 1])
    targets = find_targets()
    if limit:
        targets = targets[:limit]
    print('含中文 description 的 SKILL.md: {0} 个'.format(len(targets)), flush=True)

    cache = json.load(open(CACHE, encoding='utf-8')) if os.path.exists(CACHE) else {}
    pending = [t for t in targets if t[1] not in cache]
    print('已缓存 {0}, 待翻译 {1}'.format(len(cache), len(pending)), flush=True)

    if pending:
        key = load_key()
        done = 0
        for i in range(0, len(pending), BATCH):
            batch = pending[i:i + BATCH]
            for attempt in range(3):
                try:
                    res = translate_batch(key, [(s, d) for _, s, d in batch])
                    if res:
                        break
                except Exception as e:
                    print('  批次 {0} 第 {1} 次失败: {2}'.format(i // BATCH, attempt + 1, repr(e)[:120]), flush=True)
                    time.sleep(5 * (attempt + 1))
                    res = None
            if not res:
                print('  批次 {0} 三次均失败, 跳过(缓存外, 下轮重试)'.format(i // BATCH), flush=True)
                continue
            cache.update(res)
            done += len(res)
            json.dump(cache, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
            print('  批次 {0}/{1} 完成, 累计缓存 {2}'.format(i // BATCH + 1, (len(pending) + BATCH - 1) // BATCH, len(cache)), flush=True)
        print('本轮翻译完成 {0} 条'.format(done), flush=True)

    if not apply_mode:
        print('dry-run 模式, 不写回。加 --apply 落盘。', flush=True)
        return

    written = 0
    for p, slug, old in targets:
        if slug not in cache:
            continue
        s = io.open(p, encoding='utf-8', errors='replace').read()
        new = cache[slug].replace('\\', '\\\\').replace('"', "'")
        s2 = re.sub(r'^(description:\s*).+$', lambda m: m.group(1) + '"' + new + '"',
                    s, count=1, flags=re.M)
        if s2 != s:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(s2)
            written += 1
    print('写回 {0} 个 SKILL.md'.format(written), flush=True)


if __name__ == '__main__':
    main()
