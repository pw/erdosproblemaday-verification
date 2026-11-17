# Model check of Kneser's conclusion as used: B = full classes I (mod g) + finitely many single elements in classes F,
# B0 = B u {0}, X = i*B0. Cofinite classes of X+B0: U = I + iS ; classes met: (i+1)S, with S = I u F u {0}.
# d(X) = |I + (i-1)S|/g, d(B0) = |I|/g. In the Kneser case d(X+B0) < d(X)+d(B0) check:
#  (1) |U| == |P|+|S|-1 where P = iS (classes met by X)  [Kneser's equality with classes-met counts]
#  (2) whether U == P+S (all classes met are cofinite) -- the CLAIMS sentence "Y = P + S".
import itertools, sys
def ss(X,Y,g): return frozenset((x+y)%g for x in X for y in Y)
def mult(k,S,g):
    R=frozenset([0])
    for _ in range(k): R=ss(R,S,g)
    return R
G=int(sys.argv[1]) if len(sys.argv)>1 else 9
cases=0; eq_fail=0; YneqPS=0; ex=None
for g in range(2,G+1):
    cls=range(g)
    for Ibits in range(1,1<<g):
        I=frozenset(c for c in cls if Ibits>>c&1)
        rest=[c for c in cls if c not in I]
        for r in range(0,min(3,len(rest))+1):
            for F in itertools.combinations(rest,r):
                S=I|frozenset(F)|frozenset([0])
                for i in (1,2,3):
                    IX=ss(I,mult(i-1,S,g),g); P=mult(i,S,g)
                    U=ss(I,mult(i,S,g),g)
                    if len(U) < len(IX)+len(I):      # Kneser case (strict)
                        # need the minimal period: the theorem says SOME g works; test with g' = minimal period of U
                        per=min(p for p in range(1,g+1) if g%p==0 and all(((u+p)%g in U) for u in U))
                        cases+=1
                        # reduce mod per
                        Ur=frozenset(u%per for u in U); Pr=frozenset(x%per for x in P); Sr=frozenset(x%per for x in S)
                        if len(Ur)!=len(Pr)+len(Sr)-1: eq_fail+=1; print("EQ FAIL",g,sorted(I),F,i,per)
                        if Ur!=ss(Pr,Sr,per):
                            YneqPS+=1
                            if ex is None: ex=(g,sorted(I),F,i,per,sorted(Ur),sorted(ss(Pr,Sr,per)))
print("Kneser-case configurations:",cases,"equality failures:",eq_fail,"cases with cofinite classes != P+S:",YneqPS)
print("example:",ex)
