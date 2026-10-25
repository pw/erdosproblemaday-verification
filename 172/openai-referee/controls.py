#!/usr/bin/env python3
"""Two cheap exact controls on the OpenAI #172 paper, run 2026-10-11 (erdos cron tick).
1. Identity (8.2): with p_l = 2^{n-l}, lambda_e = p_A - p_C + p_{T0} > 0 for every pair e=(U,A) at a pivot i
   (U = C ∪ {i}, A = P ∪ {j}, ∅≠P<C<j<i), exhaustively for n ≤ 8.
2. Corollary 1.2: a_1 ≥ 2 and a_d > sum_{k<d} a_k + prod_{k<d} a_k  ⇒ subset sums injective, subset products
   injective, FS ∩ FP = A.  Positive control: 3000 random separated sets.  Negative control: 3000 random
   unseparated sets, which must (and do) produce collisions — so the checker can fail."""
import itertools, random
def p(l,n): return 2**(n-l)
bad=0; checked=0
for n in range(3,9):
    idx=list(range(1,n+1))
    for i in idx:
        below=[l for l in idx if l<i]
        for r in range(1,len(below)+1):
            for T0 in itertools.combinations(below,r):
                for s in range(1,len(below)+1):
                    for C in itertools.combinations(below,s):
                        for t in range(1,len(below)+1):
                            for P in itertools.combinations(below,t):
                                if max(P)>=min(C): continue
                                for j in below:
                                    if not (max(C)<j<i): continue
                                    A=set(P)|{j}
                                    lam=sum(p(l,n) for l in A)-sum(p(l,n) for l in C)+sum(p(l,n) for l in T0)
                                    checked+=1; bad+= (lam<=0)
print("control (8.2) lambda_e>0: checked",checked,"violations",bad)
assert bad==0
def check(A):
    m=len(A); S={}; Pp={}
    for mask in range(1,1<<m):
        sub=[A[k] for k in range(m) if mask>>k&1]
        s=sum(sub); pr=1
        for x in sub: pr*=x
        if s in S: return "sum collision"
        if pr in Pp: return "prod collision"
        S[s]=mask; Pp[pr]=mask
    return "ok" if set(S)&set(Pp)==set(A) else "FS∩FP != A"
random.seed(1); pos={}; neg={}
for _ in range(3000):
    m=random.randint(1,7); A=[random.randint(2,9)]
    for d in range(1,m):
        s=sum(A); pr=1
        for x in A: pr*=x
        A.append(s+pr+random.randint(1,5))
    r=check(A); pos[r]=pos.get(r,0)+1
for _ in range(3000):
    A=sorted(random.sample(range(2,40),random.randint(2,6))); r=check(A); neg[r]=neg.get(r,0)+1
print("Corollary 1.2 positive control:",pos); print("negative control (unseparated):",neg)
assert pos=={"ok":3000} and neg.get("ok",0)<3000
print("CONTROLS PASS")
