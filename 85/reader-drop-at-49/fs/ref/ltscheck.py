import itertools, json
def canon(sysT):
    t=len(sysT); best=None
    pts=sorted({x for b in sysT for x in b})
    for order in itertools.permutations(range(t)):
        pos={j:i for i,j in enumerate(order)}
        types=sorted(tuple(sorted(pos[j] for j,b in enumerate(sysT) if x in b)) for x in pts)
        key=tuple(types)
        if best is None or key<best: best=key
    return best
def classes(npts,tmax):
    TR=list(itertools.combinations(range(npts),3))
    reps={0:[()]}; out={0:1}
    for t in range(1,tmax+1):
        seen={}
        for base in reps[t-1]:
            for tr in TR:
                if tr in base: continue
                if any(len(set(tr)&set(b))>1 for b in base): continue
                s=tuple(sorted(base+(tr,)))
                c=canon(s)
                if c not in seen: seen[c]=s
        reps[t]=list(seen.values()); out[t]=len(seen)
    return out,reps
for npts,tmax,f in [(7,7,'reps7.json'),(9,4,'reps.json'),(9,4,'reps9b.json')]:
    cnt,mine=classes(npts,tmax)
    theirs=json.load(open('/home/exedev/MathDyad/erdos85/h9/'+f))
    tc={int(k):len(v) for k,v in theirs.items()}
    # canon of their reps cover mine
    ok=True
    for t in range(tmax+1):
        tcan={canon(tuple(tuple(b) for b in T)) for T in theirs[str(t)]}
        lin=all(all(len(set(a)&set(b))<=1 for a,b in itertools.combinations(T,2)) and all(len(set(b))==3 and max(b)<npts for b in T) and len(T)==t for T in theirs[str(t)])
        mcan={canon(s) for s in mine[t]}
        if tcan!=mcan or not lin or len(tcan)!=len(theirs[str(t)]): ok=False; print("MISMATCH",f,t,len(tcan),len(mcan),lin)
    print(npts,f,"mine",cnt,"theirs",tc,"match",ok)
