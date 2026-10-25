import re,collections
exec(open('holes.py').read().split("pats={")[0])
pats={'#exit':r'#exit','decide +native':r'decide\s*\+\s*native|decide\s*\(config\s*:=\s*\{\s*native','decide +kernel':r'decide\s*\+\s*kernel|decide!','csimp':r'@\[csimp','import Lean':r'^import\s+Lean\b','open Lean':r'^\s*open\s+.*\bLean\b','Lean.Elab/Meta usage':r'\b(MetaM|TermElabM|TacticM|CoreM)\b',
'bv_decide':r'bv_decide','Lean.ofReduce':r'Lean\.ofReduce','unsafeCast':r'unsafeCast|ptrAddrUnsafe','addDecl/modifyEnv':r'addDecl|modifyEnv','Classical.axiom-ish: propext/ choice custom':r'Classical\.choice','Quot.sound':r'Quot\.sound','ULift hack':r'XXXXX','instance_priority_global_classical':r'^\s*(open\s+Classical|open\s+scoped\s+Classical)','attribute global':r'^\s*attribute\s*\[(?!local|scoped)','local instance Classical':r'attribute\s*\[local instance\]\s*Classical\.propDecidable','simp +arith decide':r'XXXXXX'}
files=open('files.txt').read().split()
cnt={k:collections.Counter() for k in pats};hits={k:[] for k in pats}
for f in files:
    s=strip(open(f,encoding='utf8').read())
    pk='OAI' if '/repo/lean/' in f else f.split('/ext/')[1].split('/')[0]
    for k,p in pats.items():
        for m in re.finditer(p,s,flags=re.M):
            cnt[k][pk]+=1
            ln=s.count('\n',0,m.start())+1
            hits[k].append((f,ln,s.splitlines()[ln-1].strip()[:120]))
for k in pats:
    print(f'{k:40s} total={sum(cnt[k].values()):5d} ',dict(cnt[k]))
for k in ['#exit','decide +native','decide +kernel','csimp','import Lean','MetaM-types','Lean.ofReduce','unsafeCast','addDecl/modifyEnv','Quot.sound','attribute global']:
    if hits.get(k):
        print('==',k)
        for h in hits[k][:15]: print('  ',h[0].replace('/tmp/oaimath/021/',''),h[1],h[2])
