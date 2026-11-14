# Referee: rank mod p of own random copies (role form, random permutation), via PARI matrank over F_p.
import random, subprocess
from itertools import combinations
V = [frozenset(c) for c in combinations(range(13), 5)]; I = {s: i for i, s in enumerate(V)}
def build(inf, a, b, S12, S13, S23):
    B = [{a[0], b[0]} | S12 | S13, {a[1], b[1]} | S12 | S23, {a[2], b[2]} | S13 | S23]
    out = set()
    for Bk in B: out |= {frozenset(Bk - {x}) for x in Bk}
    out |= {frozenset({inf, *a, s}) for s in S12 | S13 | S23}
    out |= {frozenset({inf, *b, y}) for y in range(13) if y not in {inf, *b}}
    assert len(out) == 33
    return out
random.seed(777)
rows = []
for _ in range(1400):
    p = list(range(13)); random.shuffle(p)
    F = build(p[0], p[1:4], p[4:7], set(p[7:9]), set(p[9:11]), set(p[11:13]))
    r = [0]*1287
    for s in F: r[I[s]] = 1
    rows.append(r)
with open('/tmp/ref_rank.gp', 'w') as f:
    f.write('M=Mat([' + ';'.join(','.join(map(str, r)) for r in rows) + ']);\n')
    f.write('foreach([2,3,5,7,11,13,17,19,23,59,347,389],p,print("p=",p," rank=",matrank(M*Mod(1,p))));\n')
    f.write('print("rank over Q (via p=1000003): ", matrank(M*Mod(1,1000003)));\n')
print(subprocess.run(['gp', '-q', '-s', '2000000000', '/tmp/ref_rank.gp'], input='', capture_output=True, text=True, timeout=600).stdout)
