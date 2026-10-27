# -*- coding: utf-8 -*-
# Phase 3 对照评测: description 改写前后 Recall@20
# BEFORE = git HEAD 版本(未改写), AFTER = 当前工作区; 查询集为中文渗透任务语句 + 人工金标 slug
import io, os, re, subprocess, sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTERED = {'attack-skill-router', 'engagement-discipline', 'java-deserialization-gadget-selector'}

QUERIES = [
    # (query, [gold slugs])
    ("目标可能有SQL注入,用自动化工具验证并拖库", ["exploiting-sql-injection-with-sqlmap", "sqli-sql-injection", "bbqsql-blind-sqlmap"]),
    ("怀疑有SSRF,需要带外(OOB)验证", ["performing-blind-ssrf-exploitation", "ssrf-sheriff-oob", "ssrfmap-exploit", "ssrf-server-side-request-forgery"]),
    ("检测并利用模板注入SSTI", ["ssti-server-side-template-injection", "exploiting-template-injection-vulnerabilities"]),
    ("文件上传限制绕过拿webshell", ["offensive-file-upload", "weevely-webshell"]),
    ("路径遍历读取服务器配置文件", ["path-traversal-lfi", "performing-directory-traversal-testing"]),
    ("命令注入漏洞检测与利用", ["cmdi-command-injection", "commix-command-injection"]),
    ("Java反序列化漏洞利用,选择合适的gadget", ["deserialization-insecure", "exploiting-insecure-deserialization", "java-deserialization-gadget-selector", "serializationdumper-java"]),
    ("XXE外部实体注入测试", ["testing-for-xxe-injection-vulnerabilities", "testing-for-xml-injection-vulnerabilities"]),
    ("GraphQL接口安全评估与内省查询", ["performing-graphql-security-assessment", "performing-graphql-introspection-attack"]),
    ("JWT none算法攻击伪造令牌", ["performing-jwt-none-algorithm-attack", "exploiting-jwt-algorithm-confusion-attack", "jwt-tool-token"]),
    ("IDOR水平越权漏洞测试", ["exploiting-idor-vulnerabilities", "testing-api-for-broken-object-level-authorization"]),
    ("API限流/速率限制绕过测试", ["performing-api-rate-limiting-bypass"]),
    ("目录和隐藏路径爆破发现后台", ["dirsearch-dir-bruteforce", "feroxbuster-content-discovery", "dirb-dir-scan", "kiterunner-api-routes"]),
    ("从历史存档批量收集带参数URL辅助漏扫", ["paramspider-param-harvest", "gau-url-history", "waybackurls-history"]),
    ("WordPress站点插件漏洞检测", ["wpscan-wp-audit"]),
    ("大规模全网快速端口扫描", ["masscan-internet", "scanning-network-with-nmap-advanced"]),
    ("nmap服务版本识别与脚本扫描", ["scanning-network-with-nmap-advanced"]),
    ("BloodHound分析域内攻击路径", ["conducting-internal-reconnaissance-with-bloodhound-ce", "mapping-attack-paths-with-bloodhound-ce", "exploiting-active-directory-with-bloodhound", "performing-active-directory-bloodhound-analysis"]),
    ("用NetExec在SMB上横向验证凭据", ["moving-laterally-with-netexec", "crackmapexec-smb"]),
    ("Kerberoasting导出服务账户票据并破解", ["performing-kerberoasting-attack", "exploiting-kerberoasting-with-impacket", "targetedkerberoast-ad"]),
    ("AD CS证书模板ESC1配置错误利用", ["exploiting-adcs-with-certipy", "exploiting-active-directory-certificate-services-esc1"]),
    ("影子凭证接管域内账户", ["abusing-shadow-credentials-for-privesc"]),
    ("约束委派滥用横向到高权限", ["exploiting-constrained-delegation-abuse"]),
    ("DCSync复制域控目录持久化", ["conducting-domain-persistence-with-dcsync"]),
    ("Pass-the-Ticket票据传递", ["conducting-pass-the-ticket-attack"]),
    ("NTLM中继结合ADCS ESC8", ["relaying-ntlm-for-adcs-esc8", "ntlm-relay-coercion"]),
    ("LDAP枚举域内用户和计算机", ["ad-ldap-enum-ldap", "windapsearch-ldap-ad", "ldeep-ldap-query", "enum4linux-ng"]),
    ("低权限域账户快速摸底找提权路径", ["adpeas-quickwin", "deathstar-automation"]),
    ("ACL滥用自动化提权到域管", ["aclpwn-acl-abuse", "bloodyad-ad-privesc"]),
    ("GPO组策略滥用提权", ["pygpoabuse-gpo-privesc"]),
    ("抓取lsass进程内存中的凭据", ["mimikatz-credentials"]),
    ("导出浏览器保存的账号密码", ["performing-credential-access-with-lazagne", "extracting-browser-history-artifacts", "donpapi-dpapi-harvest"]),
    ("DPAPI保护的密钥和凭据解密", ["abusing-dpapi-for-credential-access", "extractbitlockerkeys-dpapi"]),
    ("NTLM哈希离线破解", ["performing-hash-cracking-with-hashcat"]),
    ("已控主机上搭建SOCKS代理穿透内网", ["3proxy-pivot", "tunneling-and-pivoting", "stowaway-pivot"]),
    ("流量加密隧道规避检测", ["crypthook-encrypted-tunnel", "sniffjoke-traffic-obf"]),
    ("DNS隧道外传数据", ["dnsteal-dns-exfil", "dbd-dns-tunnel-shell"]),
    ("敏感数据打包外传", ["data-exfiltrator", "cloakify-exfil", "offensive-data-exfiltration"]),
    ("图片隐写隐藏外传数据", ["zsteg-png-stego", "outguess-jpeg-stego", "openstego-general-stego"]),
    ("安卓APP静态安全分析", ["performing-android-app-static-analysis-with-mobsf", "qark-android"]),
    ("安卓APP动态分析与hook", ["performing-dynamic-analysis-of-android-app", "dwarf-android-hook", "drozer-android"]),
    ("Docker容器逃逸到宿主机", ["offensive-container-escape", "container-escape-techniques", "escaping-containers-to-host", "shocker-docker-escape", "deepce-container-escape", "botb-container-attack"]),
    ("Kubernetes集群渗透", ["performing-kubernetes-penetration-testing", "offensive-k8s-attacks", "kubernetes-pentesting"]),
    ("K8s RBAC配置错误提权审计", ["auditing-kubernetes-rbac-privilege-escalation"]),
    ("搭建钓鱼演练平台批量发钓鱼邮件", ["performing-phishing-simulation-with-gophish", "performing-red-team-phishing-with-gophish"]),
    ("反向代理钓鱼页面实时接管会话", ["modlishka-reverse-proxy-phishing"]),
    ("子域名全量枚举", ["performing-subdomain-enumeration-with-subfinder", "amass-attack-surface", "sublist3r-passive-subdomains", "findomain-fast-enum", "shuffledns-brute"]),
    ("邮箱和员工OSINT情报收集", ["osint-collector", "gmask-osint-all", "gasmask-osint-all"]),
    ("DNS记录收割与区域枚举", ["fierce-dns-recon", "dnsmap-subdomain", "adidnsdump-ldap-enum", "zdns-lookup"]),
    ("外部攻击面测绘与资产梳理", ["amass-attack-surface", "gowitness-screenshot"]),
    ("根据CVE编号查找可用EXP", ["rext-exploit-db", "offensive-vuln-classes"]),
    ("shellcode编写与编码", ["armscgen-shellcode", "shellcode-dev", "offensive-shellcode", "shellnoob-shellcode"]),
    ("Windows杀软与EDR规避", ["edr-evasion", "windows-av-evasion"]),
    ("Linux环境安全限制绕过", ["linux-security-bypass"]),
    ("权限维持后门方案规划", ["offensive-persistence", "persistence-planner", "thefatrat-backdoor"]),
    ("Linux本地提权向量排查", ["linux-privilege-escalation", "offensive-linux-privesc", "suid3num-privesc", "pspy-process-monitor"]),
    ("SUID二进制文件提权", ["suid3num-privesc", "linux-privilege-escalation"]),
    ("内网流量嗅探抓取明文凭据", ["net-creds-sniff", "responder-ntlm-poison", "sslsniff-cert-mitm", "driftnet-image-sniff"]),
    ("SSH/RDP等服务的口令爆破", ["medusa-bruteforce", "brutespray-service-brute", "crowbar-brute", "shreder-ssh-brute"]),
    ("Web登录表单口令爆破", ["brutemap-smart-brute", "mybff-login-brute", "patator-multi-brute"]),
    ("搭建C2控制框架管理会话", ["adaptix-c2-framework"]),
    ("主机信息收集坐席排查(windows安全基线核查)", ["seatbelt-host-survey"]),
]


def load_skills(from_git=False):
    docs = {}
    # BEFORE 只有 tool-skills 组被改过, 该组一次性从 git archive 解包, 其余直接读工作区
    tmp = None
    if from_git:
        tmp = os.path.join(ROOT, 'scripts', '_before_tmp')
        if not os.path.exists(tmp):
            os.makedirs(tmp)
            subprocess.check_call('git archive HEAD tool-skills | tar -x -C scripts/_before_tmp', cwd=ROOT, shell=True,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for dp, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ('.git', '_before_tmp')]
        if 'SKILL.md' not in files:
            continue
        slug = os.path.relpath(dp, ROOT).replace(os.sep, '/')
        parts = slug.split('/')
        if parts[0] in REGISTERED or len(parts) < 2 or parts[0] == 'scripts':
            continue
        src = os.path.join(dp, 'SKILL.md')
        if from_git and parts[0] == 'tool-skills':
            src = os.path.join(ROOT, 'scripts', '_before_tmp', slug, 'SKILL.md')
            if not os.path.exists(src):
                continue
        s = io.open(src, encoding='utf-8', errors='replace').read()
        fm = re.search(r'^---\n(.*?)\n---', s, re.S)
        if not fm:
            continue
        dm = re.search(r'^description:\s*(.+)$', fm.group(1), re.M)
        nm = re.search(r'^name:\s*(.+)$', fm.group(1), re.M)
        if not dm:
            continue
        docs[parts[-1]] = (nm.group(1).strip() if nm else parts[-1], dm.group(1).strip())
    return docs


def evaluate(docs, tag):
    slugs = sorted(docs)
    corpus = ['{0} {0} {0} {1}'.format(docs[s][0], docs[s][1]) for s in slugs]
    vec_w = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    vec_c = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5), min_df=1)
    X = hstack([vec_w.fit_transform(corpus), vec_c.fit_transform(corpus)])
    Q = hstack([vec_w.transform([q for q, _ in QUERIES]), vec_c.transform([q for q, _ in QUERIES])])
    sim = (Q @ X.T).toarray()
    hits20 = hits5 = 0
    missing_gold = []
    detail = []
    for i, (q, gold) in enumerate(QUERIES):
        gold = [g for g in gold if g in docs]
        if not gold:
            missing_gold.append(q)
            continue
        top = np.argsort(-sim[i])[:20]
        top20 = {slugs[j] for j in top}
        top5 = {slugs[j] for j in top[:5]}
        hit20 = any(g in top20 for g in gold)
        hit5 = any(g in top5 for g in gold)
        hits20 += hit20
        hits5 += hit5
        detail.append((q, hit20, hit5, [slugs[j] for j in top[:3]]))
    n = len(QUERIES) - len(missing_gold)
    print('[{0}] 查询数 {1} | Recall@5 = {2:.1%} | Recall@20 = {3:.1%}'.format(tag, n, hits5 / n, hits20 / n))
    return hits5 / n, hits20 / n, detail, missing_gold


before = load_skills(from_git=True)
after = load_skills(from_git=False)
print('corpus: BEFORE {0} / AFTER {1} 个 skill'.format(len(before), len(after)))
r5_b, r20_b, det_b, miss_b = evaluate(before, 'BEFORE(HEAD)')
r5_a, r20_a, det_a, miss_a = evaluate(after, 'AFTER(工作区)')
import shutil
shutil.rmtree(os.path.join(ROOT, 'scripts', '_before_tmp'), ignore_errors=True)
print()
if miss_b:
    print('金标缺失(BEFORE):', miss_b)
if miss_a:
    print('金标缺失(AFTER):', miss_a)
print()
print('=== 改写后仍漏召(@20)的查询 ===')
for (q, h20b, h5b, tb), (_, h20a, h5a, ta) in zip(det_b, det_a):
    if not h20a:
        print(' *', q)
        print('   BEFORE top3:', tb)
        print('   AFTER  top3:', ta)
