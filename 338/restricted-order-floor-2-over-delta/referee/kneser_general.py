# Model test of Kneser's two-set equality in the "classes met at all" form (Ackelsberg-Richter Thm 1.3):
# A = full classes IA + single points in classes FA, B likewise. Cofinite classes U = (IA + SB) u (SA + IB),
# SA = IA u FA, SB = IB u FB. Kneser case: |U| < |IA| + |IB|. Claim: at the minimal period p of U,
# |U mod p| = |SA mod p| + |SB mod p| - 1, and every class met by A+B (= SA+SB) is cofinite.
import itertools, sys
def ss(X,Y,g): return frozenset((x+y)%g for x in X for y in Y)
G=int(sys.argv[1]) if len(sys.argv)>1 else 7
cases=fail=notall=0; ex=None
for g in range(2,G+1):
    subsets=[frozenset(c for c in range(g) if b>>c&1) for b in range(1<<g)]
    for IA in subsets:
        if not IA: continue
        for FA in subsets:
            if FA & IA or len(FA)>2: continue
            SA=IA|FA
            for IB in subsets:
                if not IB: continue
                for FB in subsets:
                    if FB & IB or len(FB)>2: continue
                    SB=IB|FB
                    U=ss(IA,SB,g)|ss(SA,IB,g)
                    if len(U) >= len(IA)+len(IB): continue
                    cases+=1
                    p=min(q for q in range(1,g+1) if g%q==0 and all(((u+q)%g) in U for u in U))
                    Ur={u%p for u in U}; Ar={x%p for x in SA}; Br={x%p for x in SB}
                    if len(Ur)!=len(Ar)+len(Br)-1:
                        fail+=1
                        if ex is None: ex=(g,sorted(IA),sorted(FA),sorted(IB),sorted(FB),p,sorted(Ur),sorted(Ar),sorted(Br))
                    if set(Ur)!=set(ss(frozenset(Ar),frozenset(Br),p)): notall+=1
print("Kneser-case pairs:",cases," equality failures:",fail," met-but-not-cofinite cases:",notall," first failure:",ex)
