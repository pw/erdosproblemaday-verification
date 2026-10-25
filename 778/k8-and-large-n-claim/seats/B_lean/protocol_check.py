# Literal transcription of Game.lean's RoundReachable/Terminal vs a direct move-by-move game tree.
import itertools, hashlib
def run(n, sig):
    V=range(n)
    E=[frozenset(p) for p in itertools.combinations(V,2)]
    allE=frozenset(E)
    free=lambda b,c: allE-(b|c)
    # --- Lean encoding ---
    RR=set(); frontier=[(frozenset([e]),frozenset()) for e in E]
    RR.update(frontier)
    while frontier:
        new=[]
        for (b,c) in frontier:
            c1=sig(b,c)
            if c1 not in free(b,c): continue
            cA=c|{c1}
            c2=sig(b,cA)
            if c2 not in free(b,cA): continue
            cB=cA|{c2}
            for e in free(b,cB):
                p=(b|{e},cB)
                if p not in RR: RR.add(p); new.append(p)
        frontier=new
    T=set()
    for (b,c) in RR:
        if not free(b,c): T.add((b,c))
        c1=sig(b,c)
        if c1 in free(b,c):
            cA=c|{c1}
            if not free(b,cA): T.add((b,cA))
            c2=sig(b,cA)
            if c2 in free(b,cA):
                cB=cA|{c2}
                if not free(b,cB): T.add((b,cB))
    # --- direct game tree: Bella 1, then (C,C,B)* ; Chingiz takes min(2,remaining) ---
    G=set(); stuck=[0]
    def bella(b,c):
        f=free(b,c)
        if not f: G.add((b,c)); return
        for e in f: chingiz(b|{e},c)
    def chingiz(b,c):
        for _ in range(2):
            f=free(b,c)
            if not f: G.add((b,c)); return
            x=sig(b,c)
            if x not in f: stuck[0]+=1; return
            c=c|{x}
        bella(b,c)
    if E: bella(frozenset(),frozenset())
    return T,G,stuck[0]
def lexmin(b,c,n):
    E=sorted([tuple(sorted(p)) for p in itertools.combinations(range(n),2)])
    for t in E:
        e=frozenset(t)
        if e not in b and e not in c: return e
    return frozenset()
def hashy(b,c,n):
    E=[frozenset(p) for p in itertools.combinations(range(n),2)]
    f=[e for e in E if e not in b and e not in c]
    if not f: return frozenset()
    key=hashlib.md5(repr((sorted(map(sorted,b)),sorted(map(sorted,c)))).encode()).digest()[0]
    return f[key%len(f)]
for n in [2,3,4,5]:
    for name,s in [("lexmin",lexmin),("hashy",hashy)]:
        T,G,stuck=run(n,lambda b,c,s=s,n=n:s(b,c,n))
        print(n,name,"|Terminal|=",len(T),"|game leaves|=",len(G),"equal:",T==G,"stuck:",stuck)
# illegal strategy (returns an already-claimed edge when it can): plays escape Terminal
def bad(b,c,n):
    if b: return next(iter(b))
    return lexmin(b,c,n)
T,G,stuck=run(4,lambda b,c:bad(b,c,4))
print("illegal sigma n=4: |Terminal|=",len(T),"stuck plays=",stuck,"(vacuous win possible only for illegal sigma)")
