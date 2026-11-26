# Independent check of Kirtchakov's k(3,6) >= 73 witness, written from the definitions only (erdos seat 2026-11-26).
# Vertex (x,y) in Z_24 x Z_3 -> 3x+y; arc g -> g+s for s in S.
import itertools, sys, json
S=[(0,2),(2,0),(2,1),(2,2),(3,0),(5,1),(6,1),(6,2),(8,0),(8,1),(9,2),(10,0),(10,1),(11,0),(11,1),(11,2),(12,2),(14,1),(15,2),(16,1),(18,0),(19,0),(19,1),(21,1),(21,2)]
def build(S, n1=24, n2=3):
    V=[(x,y) for x in range(n1) for y in range(n2)]
    idx={v:3*v[0]+v[1] for v in V}
    N=len(V); out=[0]*N
    for (x,y) in V:
        for (a,b) in S:
            w=((x+a)%n1,(y+b)%n2)
            out[idx[(x,y)]] |= 1<<idx[w]
    return N,out
def neg(s,n1=24,n2=3): return ((-s[0])%n1,(-s[1])%n2)
def analyse(N,out,maxk=7):
    inn=[0]*N
    for u in range(N):
        for v in range(N):
            if out[u]>>v&1: inn[v]|=1<<u
    # oriented: no 2-cycles, no loops
    two=sum(1 for u in range(N) for v in range(N) if out[u]>>v&1 and out[v]>>u&1)
    loops=sum(1 for u in range(N) if out[u]>>u&1)
    arcs=sum(bin(o).count('1') for o in out)
    adj=[out[u]|inn[u] for u in range(N)]
    # independent triples: u<v<w pairwise non-adjacent
    full=(1<<N)-1
    indep=0
    for u in range(N):
        nonu=full & ~adj[u] & ~((1<<(u+1))-1)
        m=nonu
        while m:
            v=(m&-m).bit_length()-1; m&=m-1
            indep+=bin(nonu & ~adj[v] & ~((1<<(v+1))-1)).count('1')
    # count transitive tournaments TT_k: ordered by source-first chains; each TT_k counted once
    # TT_k with source v = TT_{k-1} inside out-neighbourhood of v (restricted to current candidate set)
    def cnt(cand,k):
        if k==0: return 1
        tot=0; m=cand
        while m:
            v=(m&-m).bit_length()-1; m&=m-1
            tot+=cnt(cand & out[v], k-1)
        return tot
    tt={k:cnt(full,k) for k in range(1,maxk+1)}
    return dict(N=N,arcs=arcs,two_cycles=two,loops=loops,indep_triples=indep,tt_counts=tt)
if __name__=='__main__':
    print('S size',len(S),'distinct',len(set(S)),'0 in S',(0,0) in S,'S cap -S',sorted(set(S)&{neg(s) for s in S}))
    N,out=build(S)
    r=analyse(N,out); print(json.dumps(r))
    # controls
    # (c1) S u {-s0}: introduces 2-cycles -> must be detected
    N1,o1=build(S+[neg(S[0])]); r1=analyse(N1,o1,maxk=3); print('ctl two-cycle:',r1['two_cycles'])
    # (c2) drop elements of S until independent triples appear (fewer arcs) -> must detect
    N2,o2=build(S[:-6]); r2=analyse(N2,o2,maxk=3); print('ctl sparse indep triples:',r2['indep_triples'])
    # (c3) transitive tournament on 8 vertices: TT_k counts = C(8,k)
    o3=[sum(1<<j for j in range(i+1,8)) for i in range(8)]; r3=analyse(8,o3,maxk=8); print('ctl TT8 counts:',r3['tt_counts'], [__import__('math').comb(8,k) for k in range(1,9)])
