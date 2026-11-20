# Three routes: (1) Fraction sum, (2) integer LCM numerator sum, (3) floating/modular sanity is NOT used; route 3 = PARI/GP if present.
import json, sys, math
from fractions import Fraction
C = json.load(open(sys.argv[1]))
ok = True
for N, s in C.items():
    N = int(N)
    distinct = len(set(s)) == len(s); inc = s == sorted(s); low = min(s) >= N
    f = sum(Fraction(1, x) for x in s)
    L = 1
    for x in s: L = L * x // math.gcd(L, x)
    num = sum(L // x for x in s)
    r1 = (f == 1); r2 = (num == L)
    print(f"N={N} k={len(s)} distinct={distinct} increasing={inc} min>=N={low} max={max(s):,} lcm={L:,} fraction==1:{r1} lcm-sum==lcm:{r2}")
    ok &= distinct and inc and low and r1 and r2
    # negative controls: drop each term / perturb last term -> must fail
    bad = 0
    for i in range(len(s)):
        t = s[:i] + s[i+1:]
        if sum(Fraction(1, x) for x in t) == 1: bad += 1
    t = s[:-1] + [s[-1] + 1]
    pert = sum(Fraction(1, x) for x in t) == 1
    print(f"   controls: drop-one sums equal to 1: {bad} (want 0); last+1 sums to 1: {pert} (want False)")
    ok &= bad == 0 and not pert
print("ALL OK" if ok else "FAIL"); sys.exit(0 if ok else 1)
