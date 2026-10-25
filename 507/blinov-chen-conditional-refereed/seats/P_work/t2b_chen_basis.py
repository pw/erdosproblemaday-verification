# Seat P, task 2b: Chen's variant -- Z built from an ARBITRARY F-basis beta_0..beta_4 (not the power basis),
# l and the interpolation in the power basis of theta. Same literal recipe otherwise.
import sys, random
sys.path.insert(0, '/tmp/oaimath/191b/seats/P_work')
import t2_norm as T2
random.seed(5)
r = int(sys.argv[1])
uval = T2.find_root_u(r)[0]
nodes = list(range(9))
K, csum_pow, dnorm_pow, Zvec_pow = T2.build(r, uval, nodes)
# random basis beta (5 K-elements, linearly independent over F_r)
def rank_mod(rows):
    rows = [list(x) for x in rows]; rk = 0
    for c in range(5):
        piv = next((i for i in range(rk, len(rows)) if rows[i][c] % r), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        inv = pow(rows[rk][c], r-2, r)
        rows[rk] = [x*inv % r for x in rows[rk]]
        for i in range(len(rows)):
            if i != rk and rows[i][c]:
                f = rows[i][c]; rows[i] = [(x - f*y) % r for x, y in zip(rows[i], rows[rk])]
        rk += 1
    return rk
while True:
    beta = [tuple(random.randrange(r) for _ in range(5)) for _ in range(5)]
    if rank_mod(beta) == 5: break
def Zbeta(X):  # X: 3x5 coefficient vectors w.r.t. beta
    out = []
    for i in range(3):
        acc = K.const(0)
        for nu in range(5): acc = K.add(acc, K.scal(X[i][nu], beta[nu]))
        out.append(acc)
    return out
# Rebuild construction_sum using Zbeta: easiest is to map X (beta-coords) -> power-basis coords Y and reuse
def to_pow(X):
    return [list(Zbeta(X)[i]) for i in range(3)]
ok = 0
for t in range(30):
    Xs = [[[random.randrange(r) for _ in range(5)] for _ in range(3)] for _ in range(3)]
    Ys = [to_pow(X) for X in Xs]
    # direct norm in beta basis
    Zs = [Zbeta(X) for X in Xs]
    Mx = [[Zs[j][i] for j in range(3)] for i in range(3)]
    N = K.norm(K.det3(Mx))
    ok += csum_pow(Ys) == N
print(f'r={r}: Chen arbitrary-basis variant (via coordinate change): {ok}/30 agree')
