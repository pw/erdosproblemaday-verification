# sanity of beta_exact against a fine numerical rearrangement (independent route)
import json
from fractions import Fraction as F
import verify3 as v
grid = json.load(open('../repo/certs/delta3/slab-9_20-1_2-g8_4_0.json'))['grid']
worst = 0
for i in range(0, len(grid) - 1, 7):
    p, q = grid[i], grid[i + 1]
    M = 4000 * (q - p)
    hs = []
    for t in range(M):
        x = (t + 0.5) / M * (q - p)          # in units
        k = p + int(x); f = x - int(x)
        hs.append(float(v.HL[k]) + f * (float(v.HR[k]) - float(v.HL[k])))
    hs.sort()
    w = (q - p) / v.U
    for y in (0.1, 0.37, 0.5, 0.9):
        num = sum(hs[: int(y * M)]) * w / M
        ex = float(v.beta_exact(p, q, F(y).limit_denominator(1000)))
        worst = max(worst, abs(num - ex) / max(1e-12, abs(ex)))
print('max relative diff exact vs numeric rearrangement:', worst)
