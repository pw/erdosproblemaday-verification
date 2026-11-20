# brute-force control for core.c on small parameters: build the band, take its minimal elements directly.
import sys
from sympy import primerange, factorint
y, L, T = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
A = [s for s in range(T+1, L*T+1) if max(factorint(s) or {1:1}) <= y]
S = set(A)
core = [s for s in A if not any(s % p == 0 and s//p in S for p in primerange(2, y+1))]
# minimal under divisibility: no proper divisor in A. (A divisor d of s in A with d>T; if s has a divisor in A it has one of form s/p? check fully:)
core2 = [s for s in A if not any(d in S for d in range(T+1, s) if s % d == 0)]
psi = sum(1 for s in range(1, T+1) if max(factorint(s) or {1:1}) <= y)
print(f"y={y} L={L} T={T} |A|={len(A)} core={len(core)} core_fulldivisorcheck={len(core2)} Psi(T)={psi}")
