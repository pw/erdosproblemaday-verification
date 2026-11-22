# second_check.py: written 2026-11-19 (Claude Opus 5.5, under the author's direction);
# shares no code with knm_check.c or the search programs. Second method, plain
# Python, no libraries. Counts ALL independent sets of size n and ALL transitive
# tournaments on m vertices by plain enumeration (no bounding), for one graph.
# Usage: python3 -I second_check.py N n m arcfile
# arcfile: first line "N A" (vertices, arcs), then lines "a b" meaning a -> b.
# (2026-11-20: header reading added for the Zenodo record; nothing else changed.)
import sys
N,n,m=map(int,sys.argv[1:4]); out=[set() for _ in range(N)]
L=[l for l in open(sys.argv[4]) if l.strip() and not l.startswith('#')]
hN,hA=map(int,L[0].split()); assert hN==N and hA==len(L)-1, 'header "N A" does not match'
for l in L[1:]:
    a,b=map(int,l.split()); assert 0<=a<N and 0<=b<N; out[a].add(b)
assert sum(len(o) for o in out)==hA, 'duplicate arcs'
adj=[out[v]|{u for u in range(N) if v in out[u]} for v in range(N)]
assert all(v not in out[v] for v in range(N)) and all(not(b in out[a] and a in out[b]) for a in range(N) for b in range(N))
def count_ind(k):
    # enumerate independent sets in increasing order of vertices, stop at size k
    cnt=0
    def rec(start,cands,size):
        nonlocal cnt
        if size==k: cnt+=1; return
        for v in cands:
            if v<start: continue
            rec(v+1,[w for w in cands if w>v and w not in adj[v]],size+1)
    rec(0,list(range(N)),0); return cnt
def count_tt(k):
    # a transitive tournament is a chain v1->v2->...->vk with all forward arcs
    cnt=0
    def rec(cands,size):
        nonlocal cnt
        if size==k: cnt+=1; return
        for v in cands: rec(cands & out[v], size+1)
    rec(set(range(N)),0); return cnt
print('N=%d independent %d-sets=%d independent %d-sets=%d TT%d=%d TT%d=%d'%(N,n-1,count_ind(n-1),n,count_ind(n),m-1,count_tt(m-1),m,count_tt(m)))
