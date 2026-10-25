import json
from fractions import Fraction
from collections import Counter
rows = json.load(open("/tmp/evidence203/all_e_le_5040.json"))
n = Counter(e for p, e in rows)
M = 5040
dens = {}
for N in range(1, M + 1):
    s = Fraction(0)
    for d in range(1, N + 1):
        if N % d == 0 and n[d]: s += Fraction(n[d], d)
    dens[N] = s
ge1 = [N for N in dens if dens[N] >= 1]
ge09 = sorted([N for N in dens if dens[N] >= Fraction(9, 10)], key=lambda N: (-dens[N], N))
print("N<=5040 with density >= 1:", ge1)
print("N<=5040 with density >= 0.9 (sorted by density desc):")
for N in ge09: print(f"  N={N}  density={dens[N]}  ~{float(dens[N]):.6f}")
top = sorted(dens, key=lambda N: -dens[N])[:15]
print("top 15:", [(N, str(dens[N]), round(float(dens[N]),6)) for N in top])
# sanity vs pool.py
for N in (720, 5040):
    print(N, dens[N])
json.dump({str(N): [dens[N].numerator, dens[N].denominator] for N in dens}, open("/tmp/evidence203/dens_le_5040.json","w"))
