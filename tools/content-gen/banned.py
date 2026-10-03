import re,glob,sys,collections
DRY = '--apply' not in sys.argv
KEEP_VEC = r'(?=\s*[- ]?(?:database|databases|db|dbs|search|embeddings?|index|indices|indexing|storage|store|stores|datastores?|schemas?|memory|-lexical|or\b|calculation|retrieval|similarity))'
TABLE_WORDS = 'compliance|governance|classification|alignment|control|design|transformation|service|provisioning|validation|risk|critical|replication|continuity|topology|lifesafety|generation|strategic|synergy|analytics|deployment|compute|infrastructure'
rules = [
 (r'(?i)\bsovereign\s+iron(\s+matrix)?', 'Bare-Metal'),
 (r'(?i)\b(parallel)\s+matrix\b', r'\1 MATRIXKEEPLOW'),
 (r'(?i)\bfinancial\s+matrix\b', 'financial comparison'),
 (r'(?i)\bpriority\s+matrix\b', 'priority map'),
 (r'(?i)\bstress\s+matrices\b', 'stress tests'),
 (r'(?i)\bIOPS\s+matrices\b', 'IOPS profiles'),
 (r'(?i)\bcomparison\s+matrices\b', 'comparisons'),
 (r'(?i)\bimage\s+vectors\b', 'image data'),
 (r'(?i)\bdata\s+vectors\b', 'data flows'),
 (r'(?i)\bprivate\s+sovereign\s+cloud', 'private cloud'),
 (r'(?i)\bsovereign\s+AI\b', 'Private AI'),
 (r'(?i)\bsovereign\s+(?=cloud)', 'in-country '),
 (r'(?i)\bdata\s+sovereignty\b', 'data residency'),
 (r'(?i)\bsovereignty\b', 'data residency'),
 (r'(?i)\bsovereign\s+', ''),
 (r'(?i)\s*\bsovereign\b', ''),
 (r'(?i)\bmaster\s+matrix\b', 'Whitepaper'),
 (r'(?i)\b(XProtect)\s+Matrix\b', r'\1 MATRIXKEEP'),
 (r'(?i)\b('+TABLE_WORDS+r')\s+matrices\b', r'\1 tables'),
 (r'(?i)\b('+TABLE_WORDS+r')\s+matrix\b', r'\1 table'),
 (r'(?i)\s+matrices\b', ' options'),
 (r'(?i)\s+matrix\b', ''),
 (r'(?i)\bmatrix\s+', ''),
 (r'(?i)\bmatrix\b', 'overview'),
 (r'(?i)\b(exposure|entry|risk|ip|attack)\s+vectors\b', r'\1 points'),
 (r'(?i)\bvectors(?!\s*(?:database|db|search|embedding|index))\b', 'areas'),
 (r'(?i)\s+vector\b'+r'(?!'+KEEP_VEC[3:], ''),
 (r'(?i)\bbattle[- ]tested\b', 'proven'),
 (r'(?i)\bcutting[- ]edge\b', 'current'),
 (r'(?i)\brevolutionary\b', 'new'),
]
def fix(t):
    for a,b in rules:
        def rep(m, b=b):
            out = m.expand(b)
            g = m.group(0).lstrip()
            if out and g[:1].isupper() and out[:1].islower(): out = out[0].upper()+out[1:]
            if g.isupper() and len(g)>3: out = out.upper()
            return out
        t = re.sub(a, rep, t)
    t = t.replace('MATRIXKEEPLOW','matrix').replace('matrixkeeplow','matrix').replace('MATRIXKEEP','Matrix').replace('matrixkeep','Matrix')
    t = re.sub(r'(?i)\bPrivate AI(,| &| and) Private AI\b', 'Private AI', t)
    t = re.sub(r',\s*,', ',', t)
    t = re.sub(r'(?i)\bData residency\b', lambda m: 'Data Residency' if m.group(0)[0]=='D' else m.group(0), t)
    return t
changes = collections.Counter(); files_changed=0
for f in glob.glob('views/**/*.html', recursive=True):
    src = open(f, encoding='utf-8').read()
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', src, flags=re.S|re.I)
    out=[]
    for p in parts:
        if not p: out.append(p); continue
        if p.startswith('<'):
            if re.match(r'(?i)<(script|style)', p): out.append(p); continue
            def attr(m):
                n = fix(m.group(2))
                if n!=m.group(2): changes[(m.group(2)[:80], n[:80])]+=1
                return m.group(1)+n+m.group(3)
            out.append(re.sub(r'(\b(?:content|alt|title|aria-label|placeholder)=")([^"]*)(")', attr, p))
        else:
            n = fix(p)
            if n!=p: changes[(p.strip()[:80], n.strip()[:80])]+=1
            out.append(n)
    new=''.join(out)
    if new!=src:
        files_changed+=1
        if not DRY: open(f,'w',encoding='utf-8',newline='').write(new)
print('files',files_changed,'edits',sum(changes.values()))
for (a,b),v in changes.most_common(400 if DRY else 0): print(v,'|',a,'  ==>  ',b)
