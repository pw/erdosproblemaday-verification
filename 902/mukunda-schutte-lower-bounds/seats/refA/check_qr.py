"""Sanity: QR_59 triples >= 5 dominators; QR_67 has S_4; QR_47 etc.
Also nu_1, nu_2, nu_3 for each Paley p.
"""
import sys, time
sys.path.insert(0, '/home/exedev/MathDyad/subs-1126/902/refA')
from tlib import *

for p in [7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83]:
    A = paley(p)
    check_tournament(A)
    t0 = time.time()
    nu1 = min_dom(A, 1)
    nu2 = min_dom(A, 2)
    nu3 = min_dom(A, 3)
    line = f"QR_{p}: nu1={nu1} nu2={nu2} nu3={nu3}"
    if p <= 71:
        ok4, w = has_S(A, 4)
        line += f" S4={ok4}"
        if not ok4:
            line += f" (undominated 4-set {w})"
        if p == 67:
            nu4 = min_dom(A, 4)
            line += f" nu4={nu4}"
    line += f" [{time.time()-t0:.1f}s]"
    print(line, flush=True)
