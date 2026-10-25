# Arithmetic checks for §8 (Lemma 8.1, Lemma 8.2 classification, Lemma 8.3, Prop 8.4 packings), all t in 9..TMAX.
import math, sys
TMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 400
# ---- Lemma 8.1: no (t,k,j,r) with t>=9, t<=k<=2t+1, 1<=j<=5, 2r >= t-j+1, (r-1)(j+2) <= k-t
bad = []
for t in range(9, TMAX+1):
    for k in range(t, 2*t+2):
        for j in range(1, 6):
            for r in range(1, t+2):
                if 2*r >= t-j+1 and (r-1)*(j+2) <= k-t:
                    bad.append((t,k,j,r))
print("Lemma 8.1 counterexamples to the 'all amounts >= j+2' contradiction, t=9..%d:" % TMAX, bad[:5], len(bad))
# tightness: at t = 8 the inequality is NOT contradictory
t8 = [(8,k,j,r) for k in range(8,18) for j in range(1,6) for r in range(1,10) if 2*r >= 8-j+1 and (r-1)*(j+2) <= k-8]
print("  (control) t=8 solutions exist:", t8[:3], len(t8))
# ---- Lemma 8.2: enumerate (t,k,d,e,v,a) satisfying the constraints proved in its proof, compare with the 3 alternatives
surv = set(); unexplained = []
for t in range(9, TMAX+1):
    for k in range(t, 2*t+2):
        L = k - t
        for d in range(2, 7):
            for e in range(0, L+1):
                if d*e > L: continue
                for v in range(0, t+1):
                    if v > 2*e: continue
                    if e >= 1 and v < e+1: continue
                    if e == 0 and v != 0: continue
                    for a in range(0, 3):
                        if a > t - v: continue
                        if v + a >= t - d + 2:
                            alt = None
                            if d == 2 and v >= t-2: alt = 1
                            if d == 3 and t in (9, 11) and 2*e == t-3 and v == t-3 and a == 2: alt = 2
                            if d == 5 and t == 9 and k == 19 and e == 2 and v == 4 and a == 2: alt = 3
                            if alt is None: unexplained.append((t,k,d,e,v,a))
                            else: surv.add((alt,t,k,d,e,v,a))
print("Lemma 8.2: unexplained survivors:", unexplained[:10], len(unexplained))
alt2 = sorted(s for s in surv if s[0]==2); alt3 = sorted(s for s in surv if s[0]==3)
print("  Alt 2 survivors:", alt2)
print("  Alt 3 survivors:", alt3)
# Alt 1 with d=2: check endpoint claim 'union of targets contains all missing' <=> a >= t-v
print("  Alt1 survivors with a < t-v:", [s for s in surv if s[0]==1 and s[6] < s[1]-s[5]][:5])
# ---- Lemma 8.3, Alt 1: one nonsingleton chain impossible: v=e+1, 2e<=L<=t+1  => e+1 < t-2
print("Lemma 8.3 Alt1 one-chain bound fails for t:", [t for t in range(9,TMAX+1) if (t+1)//2 + 1 >= t-2])
# ---- Prop 8.4 packings
fail = []
for t in range(9, TMAX+1):
    for k in range(t, 2*t+2):
        L = k-t
        # Alt 1, c in {1,2}: need k >= 2t-2 (derived), bound 3(t-c) > k ; also |B2| >= k+3 > max(k,2t) needs k+3 > 2t
        for c in (1, 2):
            v = t - c
            # feasibility: v <= 2e <= L
            if v <= L:   # L >= 2e >= v
                if not (3*(t-c) > k): fail.append(("A1c", t, k, c))
                if not (k + 3 > 2*t and k + 3 > k): fail.append(("A1c-size", t, k, c))
        # Alt 1, c = 0: t <= 2e <= L <= t+1 ; 3(t-1) > k
        if L >= t:
            if not (3*(t-1) > k): fail.append(("A1-0", t, k))
            if not (k >= 2*t): fail.append(("A1-0 k>=2t", t, k))
        # Alt 2
        if t in (9, 11) and L >= 3*(t-3)//2:
            if not (k >= 2*t and 3*(t-2) > k): fail.append(("A2", t, k))
    if t == 9:
        k = 19
        if not (4*3 + 5*2 > k and k >= 2*t): fail.append(("A3",))
print("Prop 8.4 packing failures:", fail[:10], len(fail))
