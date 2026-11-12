# -*- coding: utf-8 -*-
"""两层部署脚本：注册层(3 skill) + 文件库(993 skill 扁平化)

用法:
  python scripts/deploy.py                 # 实际部署(默认 /root/.claude/skills + /opt/attack-skill-library)
  python scripts/deploy.py --dry-run       # 只打印计划不动盘
  python scripts/deploy.py --skills-dir X --library-dir Y   # 自定义目标路径(本地调试)

设计:
  - 注册层 = Skill 协议发现目录, 只放路由/纪律/专项 3 个, 控制常驻系统提示词税
  - 文件库 = 纯 markdown 扁平目录 <slug>/SKILL.md, Agent 经 router 指引用 Read 按需读
  - 幂等: 目标目录已存在同名内容则整目录覆盖复制; --clean 可先清空再部署
"""
import os, sys, io, shutil, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTERED = ['attack-skill-router', 'engagement-discipline', 'java-deserialization-gadget-selector']
# 库根索引: (仓库内路径, 库内文件名)，存在才拷
ROOT_FILES = [('INDEX.md', 'INDEX.md'), ('attack-skill-router/MERGES.md', 'MERGES.md')]
# 路由工具: 随库部署到 _router/, 镜像烘焙时已 build 好索引则一并带上
ROUTER_FILES = ['skill_route.py', 'skill_retrieval.py', 'build_entity_registry.py', 'entity_registry.json']

def find_skills(base):
    """返回 {slug: abs_dir}，校验重名"""
    out, dup = {}, []
    for dp, dirs, files in os.walk(base):
        if 'SKILL.md' not in files:
            continue
        rel = os.path.relpath(dp, base)
        if rel.startswith('.git'):
            continue
        slug = os.path.basename(dp)
        if slug in out:
            dup.append(slug)
        out[slug] = dp
    return out, dup

def copy_skill(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '.git'))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skills-dir', default='/root/.claude/skills', help='注册层目标目录')
    ap.add_argument('--library-dir', default='/opt/attack-skill-library', help='文件库目标目录')
    ap.add_argument('--dry-run', action='store_true', help='只打印计划')
    ap.add_argument('--clean', action='store_true', help='部署前清空目标目录(危险,仅限重建)')
    a = ap.parse_args()

    skills, dup = find_skills(ROOT)
    if dup:
        print('!! slug 重名, 拒绝部署:', dup); sys.exit(1)
    for r in REGISTERED:
        if r not in skills:
            print('!! 注册层 skill 在仓库中不存在:', r); sys.exit(1)

    lib = {s: p for s, p in skills.items() if s not in REGISTERED}
    plan = []
    for r in REGISTERED:
        plan.append((skills[r], os.path.join(a.skills_dir, r), '注册层'))
    for s, p in sorted(lib.items()):
        plan.append((p, os.path.join(a.library_dir, s), '文件库'))
    for f_src, f_dst in ROOT_FILES:
        fp = os.path.join(ROOT, f_src)
        if os.path.exists(fp):
            plan.append((fp, os.path.join(a.library_dir, f_dst), '库根索引'))
    for f in ROUTER_FILES:
        fp = os.path.join(ROOT, 'scripts', f)
        if os.path.exists(fp):
            plan.append((fp, os.path.join(a.library_dir, '_router', f), '路由工具'))
    # 索引产物(烘焙进镜像时预建): 存在才带, 不存在则由 skill_retrieval.py build 现建
    idx = os.path.join(ROOT, 'scripts', '_retrieval_index.pkl')
    if os.path.exists(idx):
        plan.append((idx, os.path.join(a.library_dir, '_router', '_retrieval_index.pkl'), '路由索引'))

    print('注册层 %d 个, 文件库 %d 个, 库根文件 %d 个' % (
        len(REGISTERED), len(lib), len([1 for _,_,k in plan if k=='库根索引'])))
    if a.dry_run:
        for src, dst, kind in plan[:8]:
            print('  [%s] %s -> %s' % (kind, os.path.relpath(src, ROOT), dst))
        print('  ... 共 %d 项' % len(plan))
        return

    if a.clean:
        for d in (a.skills_dir, a.library_dir):
            if os.path.exists(d):
                shutil.rmtree(d)
    for src, dst, kind in plan:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.isdir(src):
            copy_skill(src, dst)
        else:
            shutil.copy2(src, dst)
    print('部署完成 -> %s (注册层) + %s (文件库)' % (a.skills_dir, a.library_dir))
    print('提示: 文件库默认路径可用环境变量 SKILL_LIBRARY 在靶机内覆盖')

if __name__ == '__main__':
    main()
