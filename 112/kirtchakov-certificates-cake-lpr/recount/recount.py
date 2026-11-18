# Independent recount by hereditary extension: every {I3,TT3}-free oriented graph on k vertices
# minus a vertex is one on k-1; so extending one rep of every (k-1)-class by a new vertex in all 3^(k-1)
# ways reaches every k-class. Dedupe by brute-force isomorphism restricted to degree-profile-preserving maps.
import itertools, sys, json
def ok_or(k, S):  # S[(u,v)] in {0: none, 1: u->v} for ordered pairs; build arcs set
    pass
def valid_I3L3(k, A):
    adj=lambda u,v: (u,v) in A or (v,u) in A
    for t in itertools.combinations(range(k),3):
        if not any(adj(u,v) for u,v in itertools.combinations(t,2)): return False
        for o in itertools.permutations(t):
            if (o[0],o[1]) in A and (o[0],o[2]) in A and (o[1],o[2]) in A: return False
    return True
def valid_TT4F(k, A):
    for t in itertools.combinations(range(k),4):
        for o in itertools.permutations(t):
            if all((o[i],o[j]) in A for i in range(4) for j in range(i+1,4)): return False
    return True
def prof(k,A,v):
    o=sum(1 for (a,b) in A if a==v); i=sum(1 for (a,b) in A if b==v); return (o,i)
def iso(k,A,B):
    if len(A)!=len(B): return False
    pa=[prof(k,A,v) for v in range(k)]; pb=[prof(k,B,v) for v in range(k)]
    if sorted(pa)!=sorted(pb): return False
    cand=[[w for w in range(k) if pb[w]==pa[v]] for v in range(k)]
    m={}; used=set()
    def rec(v):
        if v==k: return all((m[a],m[b]) in B for a,b in A)
        for w in cand[v]:
            if w in used: continue
            # partial check
            okp=True
            for u in range(v):
                if ((u,v) in A) != ((m[u],w) in B) or ((v,u) in A) != ((w,m[u]) in B): okp=False; break
            if not okp: continue
            m[v]=w; used.add(w)
            if rec(v+1): return True
            used.discard(w); del m[v]
        return False
    return rec(0)
def run(valid, tournament, kmax):
    reps={1:[frozenset()]}
    for k in range(2,kmax+1):
        new=[]
        states=(1,2) if tournament else (0,1,2)
        for A in reps[k-1]:
            for st in itertools.product(states, repeat=k-1):
                B=set(A)
                for u,s in enumerate(st):
                    if s==1: B.add((u,k-1))
                    elif s==2: B.add((k-1,u))
                B=frozenset(B)
                if not valid(k,B): continue
                if any(iso(k,B,C) for C in new): continue
                new.append(B)
        reps[k]=new; print('tournament' if tournament else 'I3L3', k, len(new), flush=True)
    return reps
R1=run(valid_I3L3, False, 9)
R2=run(valid_TT4F, True, 8)
json.dump({'I3L3':{k:[sorted(a) for a in v] for k,v in R1.items()}, 'TT4F':{k:[sorted(a) for a in v] for k,v in R2.items()}}, open('recount.json','w'))
