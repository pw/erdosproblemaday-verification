# exact test of Lemma 2: beta(y) >= a y + b y^2 on every cell of every certificate grid, at many y;
# positive control: the 'largest single piece' reading must be violated somewhere.
import json, glob, random
from fractions import Fraction as F
import verify3 as v
random.seed(1186)
grids = {tuple(json.load(open(f))['grid']) for f in glob.glob('../repo/certs/delta3/*.json')}
viol_summed = viol_single = tests = 0
for grid in grids:
    for i in range(len(grid) - 1):
        p, q = grid[i], grid[i + 1]
        a, b = v.bathtub(p, q, 'summed')
        a2, b2 = v.bathtub(p, q, 'single')
        ys = [F(k, 64) for k in range(65)] + [F(random.randint(1, 10**6), 10**6) for _ in range(20)]
        for y in ys:
            be = v.beta_exact(p, q, y)
            tests += 1
            if be < a * y + b * y * y: viol_summed += 1
            if be < a2 * y + b2 * y * y: viol_single += 1
print(f'grids {len(grids)}  tests {tests}  violations: summed reading {viol_summed}, single-piece reading {viol_single}')
