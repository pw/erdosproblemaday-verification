#!/usr/bin/env python3
"""Greedy symmetric extension of the H=5 obstruction: start from P, repeatedly add the smallest x such that
{0} ∪ ±(P ∪ {x}) still has no admissible 6-subset (literal definition). Each accepted set is re-verified to have an
admissible 5-subset (so H = 5 exactly). Prints every accepted step; stops when no x ≤ XMAX extends."""
import itertools, time, sys
from hcheck import admissible
P = [1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 17]; XMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 80
def sym(P): return sorted(set(P + [-x for x in P] + [0]))
def no_adm(A, k): return not any(admissible(S) for S in itertools.combinations(A, k))
A = sym(P); assert no_adm(A, 6) and not no_adm(A, 5)
print("start P =", P, "n =", len(A), flush=True)
while True:
    found = None
    for x in range(1, XMAX + 1):
        if x in P: continue
        B = sym(P + [x]); t0 = time.time()
        if no_adm(B, 6):
            found = x; print(f"  accepted x={x}: n={len(B)}, no admissible 6-subset ({time.time()-t0:.0f}s); has admissible 5-subset: {not no_adm(B,5)}", flush=True)
            P = sorted(P + [x]); break
    if found is None: print("no further single extension up to", XMAX, "; final P =", P, "n =", len(sym(P)), flush=True); break
    print("P =", P, "=> h(%d) <= 5" % len(sym(P)), flush=True)
