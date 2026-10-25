import os,re,sys
base='/tmp/oaimath/013'
def path(mod):
    parts=mod.split('.')
    cands=[]
    if parts[0]=='PrimeNumberTheoremAnd': cands=[f'{base}/ext/PrimeNumberTheoremAnd/'+'/'.join(parts)+'.lean']
    elif parts[0]=='StrongPNT': cands=[f'{base}/ext/StrongPNT/'+'/'.join(parts)+'.lean']
    elif parts[0]=='BernoulliRegular': cands=[f'{base}/ext/AINTLIB/projects/FltRegularBernoulli/'+'/'.join(parts)+'.lean']
    elif parts[0]=='Common': cands=[f'{base}/ext/AINTLIB/'+'/'.join(parts)+'.lean']
    elif parts[0]=='OAI': cands=[f'{base}/repo/lean/'+'/'.join(parts)+'.lean']
    for c in cands:
        if os.path.exists(c): return c
    return None
pats={k:re.compile(v) for k,v in {'axiom':r'^\s*(private\s+|protected\s+)?axiom\b','sorry':r'\bsorry\b','admit':r'\badmit\b','native_decide':r'native_decide','implemented_by':r'implemented_by','extern':r'@\[extern','unsafe':r'\bunsafe\b','csimp':r'csimp','opaque':r'^\s*(private\s+)?opaque\b','ofReduceBool':r'ofReduceBool'}.items()}
for fn in sys.argv[1:]:
    mods=[l.strip() for l in open(fn) if l.strip()]
    missing=[];hits={}
    for m in mods:
        p=path(m)
        if p is None: missing.append(m); continue
        for i,line in enumerate(open(p,errors='replace')):
            s=line.split('--')[0]
            for k,r in pats.items():
                if r.search(s): hits.setdefault(k,[]).append(f'{p}:{i+1}:{line.strip()[:100]}')
    print(fn, 'modules',len(mods),'missing',len(missing), missing[:5])
    for k,v in hits.items(): print(' ',k,len(v)); [print('    ',x) for x in v[:8]]
