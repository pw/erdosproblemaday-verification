# Does the NMAX cap ever bind?  Instrument both searches: max vertices ever in a state, and #times a new-vertex branch was refused.
import sys, importlib.util, time
sys.argv=[sys.argv[0]]+sys.argv[1:]
X=sys.argv[1]; NM=int(sys.argv[2])
spec=importlib.util.spec_from_file_location("indep","/tmp/ref151/scripts/indep_search.py"); I=importlib.util.module_from_spec(spec); spec.loader.exec_module(I)
k,Xadj=I.make_X(X); S=I.Indep(k,Xadj,NM)
S.maxn=0; S.refused=0
orig_fill=S.fill
def fill(nb, non, closed, v, placed, free, i, cand, nnew):
    S.maxn=max(S.maxn, len(nb)+nnew)
    if i<len(free) and not (len(nb)+nnew+1<=S.nmax): S.refused+=1
    return orig_fill(nb, non, closed, v, placed, free, i, cand, nnew)
S.fill=fill
S.run(); print(f"[indep] {X} NMAX={NM}: completions {len(S.out)}, nodes {S.nodes}, max vertices ever in a state {S.maxn}, new-vertex branches refused by the cap {S.refused}")
sys.path.insert(0,"/home/exedev/MathDyad/erdos151/locally")
import locally
L=locally.Search(locally.make_X(X), NM); L.maxn=0; L.refused=0
of=L.fill
def fill2(adj, non, closed, v, K, pos, slots, i, assign, U, newcount):
    L.maxn=max(L.maxn, len(adj)+newcount)
    if i<len(slots) and not (len(adj)+newcount+1<=L.nmax): L.refused+=1
    return of(adj, non, closed, v, K, pos, slots, i, assign, U, newcount)
L.fill=fill2
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()): L.run()
print(f"[locally.py] {X} NMAX={NM}: found {[G.number_of_nodes() for G in L.found]}, nodes {L.nodes}, max vertices ever in a state {L.maxn}, new-vertex branches refused by the cap {L.refused}")
