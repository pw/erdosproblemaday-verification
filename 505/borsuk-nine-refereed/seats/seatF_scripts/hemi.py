import itertools, math
phi=(1+5**0.5)/2
V=[]
for s1 in (1,-1):
  for s2 in (1,-1):
    V += [(0,s1,s2*phi),(s1,s2*phi,0),(s2*phi,0,s1)]
def d(a,b): return math.dist(a,b)
edge=min(d(a,b) for a,b in itertools.combinations(V,2))
faces=[f for f in itertools.combinations(range(12),3) if all(abs(d(V[a],V[b])-edge)<1e-9 for a,b in itertools.combinations(f,2))]
# line index: identify v with -v
key=lambda v: min(v, tuple(-x for x in v))
lines=sorted(set(key(v) for v in V)); L={v:lines.index(key(v)) for v in V}
tri=set(frozenset(L[V[i]] for i in f) for f in faces)
print("faces",len(faces),"projective triangles",len(tri))
C=set(range(6))
ok1=all((frozenset(t) in tri)!=(frozenset(C-set(t)) in tri) for t in itertools.combinations(C,3))
ok2=all(sum(1 for t in tri if set(p)<=t)==2 for p in itertools.combinations(C,2))
print("Def 5.1(1) exactly one of T, C\\T:",ok1," Def 5.1(2) each pair in exactly two:",ok2)
