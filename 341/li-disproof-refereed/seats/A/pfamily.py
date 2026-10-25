import sys
def explicitF(p):
    M=7*p
    return [0,2,p-6,p-4,p,p+1,p+3,2*p-3,2*p,2*p+1,2*p+3,3*p-3,3*p-1,3*p,4*p,4*p+1,4*p+3,
            5*p-3,5*p-1,5*p,5*p+3,6*p-3,6*p-1,6*p,6*p+3,6*p+4,6*p+6,M-3,M-2,M-1]
def analyse(p,verbose=False):
    M=7*p; Z=set(range(M))
    P={p%M,2*p%M,4*p%M}; B={(M-3)%M,(M-1)%M,(6*p+3)%M}; Q=P|B
    F=Q|{(x-b)%M for x in Q for b in B}|{(x-a)%M for x in Q for a in P}
    D=Z-F
    ss=lambda X,Y:{(x+y)%M for x in X for y in Y}
    ex=explicitF(p); exs={e%M for e in ex}
    res={}
    res['F_explicit_matches']= (F==exs)
    res['30_distinct_in_range']= (len(set(ex))==30 and all(0<=e<M for e in ex))
    res['|F|']=len(F)
    res['cover D+B = Z\\Q']= (ss(D,B)==Z-Q)
    res['avoid']= not (Q&(ss(B,B)|ss(P,B)|ss(D,B)|ss(D,P)))
    res['PP∩Q=P']= (ss(P,P)&Q)==P
    res['diag only']= sorted((x,y) for x in P for y in P if (x+y)%M in Q)==sorted([(p,p),(2*p,2*p),(4*p,4*p)])
    res['P∩B empty']= not (P&B)
    # seed A_p = D ∪ B ∪ (M+B) ∪ {p,4p,M+2p,M+4p}
    A=set(D)|set(B)|{M+b for b in B}|{p,4*p,M+2*p,M+4*p}
    res['|A_p|==7p-20']= (len(A)==7*p-20, len(A))
    res['0 in D']= 0 in D
    # Lemma 5.2 internal claims
    G={0,p+1,2*p+1,4*p+1,6*p+4,M-2}; E={p-6,3*p-3,5*p-3,6*p-3,M-3}
    res['G⊂F,E⊂F']= G<=F and E<=F
    res['f in G => f-1 in Q']= all(((f-1)%M) in Q for f in G)
    res['f in F\\(G∪E) => f+2 notin F']= all(((f+2)%M) not in F for f in F-G-E)
    reps=[(p-7,2*p-10,6*p+3),(3*p-4,4*p-7,6*p+3),(5*p-4,6*p-7,6*p+3),(6*p-4,M-7,6*p+3),(M-4,p-7,6*p+3)]
    res['E reps valid']= all((d%M) in D and ((d+b)%M)==(r%M) for r,d,b in reps)
    return res
bad=[]
for p in range(18,401):
    r=analyse(p)
    ok=all((v if not isinstance(v,tuple) else v[0]) for k,v in r.items() if k not in ('|F|','0 in D')) and r['|F|']==30 and not r['0 in D']
    if not ok: bad.append((p,r))
print("p in [18,400]: failures:",len(bad)); 
for p,r in bad[:3]: print(p,r)
print("p=18:",analyse(18)); print("p=19:",analyse(19))
for p in range(3,18):
    r=analyse(p); fails=[k for k,v in r.items() if k not in ('|F|','0 in D') and not (v if not isinstance(v,tuple) else v[0])]
    print("p=%d |F|=%d fails:"%(p,r['|F|']),fails)
