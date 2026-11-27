import sys
from fractions import Fraction as F
sys.path.insert(0, '/home/exedev/MathDyad/subs-1127/36/mine')
from overlap_eval import *
path = sys.argv[1]
raw = open(path, 'rb').read()
toks = raw.split()
pd, pa = int(toks[0]), [int(x) for x in toks[1:]]
N = len(pa)
print(path, "N", N, "denominator", pd, "side:", side_conditions(pa, pd) or "pass")
T, mx, am, sc = scores(pa, pd)
P = mx * sc
print("parent max H =", P, float(P), "argmax", am, " == claimed P:", P == F(123113681346619, 323255185441944))
# relation child <-> parent: is the child a refinement (each parent cell split in two)?
import json
obj = json.load(open('/home/exedev/MathDyad/subs-1127/36/repo/construction.json'))
a, D = obj['numerators'], obj['denominator']
if len(a) == 2 * N:
    scale = D // pd
    up = [x * scale for x in pa for _ in (0, 1)]
    diff = [x - y for x, y in zip(a, up)]
    nz = [i for i, d in enumerate(diff) if d]
    print("child vs parent cell-doubled: cells differing:", len(nz), "of", len(a), "; max |diff|/D = %.3e" % (max(abs(d) for d in diff) / D))
    print("parent doubled (same function on 9408 grid) score == P:", scores(up, D)[1] * scores(up, D)[3] == P)
    Uc = F(2462273619527794579322422405079, 6465103708838880000000000000000)
    print("P - U =", P - Uc, float(P - Uc), "== claimed gain:", P - Uc == F(2468195140225859198307, 2155034569612960000000000000000))
