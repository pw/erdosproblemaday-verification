# Seat S: algebraic containment checks behind claim 1, exhaustive on small moduli.
# (1) For G in SL3(Z/h): minors(Gc|Gc') = 0 mod h  =>  minors(c|c') = 0 mod h, over ALL pairs (c,c') in (Z/h)^3.
#     Mutation 'singular': G with det divisible by B must violate it.
# (2) For ALL ordered proportional pairs u != v in the box [0,N)^2 x [N,2N), N = hq: with c = G^-1 (u mod h),
#     c' = G^-1 (v mod h): if c_1 is a unit then c'_3 = c'_1 c_1^-1 c_3 (mod h); and if u mod q != 0 then
#     v mod q lies on the line F_q (u mod q).  Mutation 'wrongalpha' (c'_3 = c_3) must be violated.
# Usage: python3 -I prop_alg.py <seed> [singular|wrongalpha]
import sys, random, math, itertools
seed = int(sys.argv[1]); mut = sys.argv[2] if len(sys.argv) > 2 else "none"
rng = random.Random(seed)
B, k, q = 3, 2, 7
h = B**k; N = h*q
def det3(a, m):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1]) - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])) % m
def mv(G, x, m): return tuple(sum(G[i][j]*x[j] for j in range(3)) % m for i in range(3))
def minors0(x, y, m): return all((x[i]*y[j]-x[j]*y[i]) % m == 0 for i in range(3) for j in range(i+1, 3))
def inv3(G, m):
    d = det3(G, m); di = pow(d, -1, m)
    C = [[0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            rows = [r for r in range(3) if r != j]; cols = [c for c in range(3) if c != i]
            mnr = G[rows[0]][cols[0]]*G[rows[1]][cols[1]] - G[rows[0]][cols[1]]*G[rows[1]][cols[0]]
            C[i][j] = ((-1)**(i+j) * mnr * di) % m
    return C
while True:
    G = [[rng.randrange(h) for _ in range(3)] for _ in range(3)]
    d = det3(G, h)
    if mut == "singular":
        if d % B == 0 and d != 0 or (d == 0 and any(G[i][j] % B for i in range(3) for j in range(3))): break
    elif math.gcd(d, h) == 1:
        di = pow(d, -1, h); G[0] = [(x*di) % h for x in G[0]]; break
fails = []
# (1) exhaustive over (Z/h)^3 x (Z/h)^3
vecs = list(itertools.product(range(h), repeat=3))
img = {c: mv(G, c, h) for c in vecs}
viol1 = 0; checked1 = 0
for c in vecs:
    gc = img[c]
    for cp in vecs:
        if minors0(gc, img[cp], h):
            checked1 += 1
            if not minors0(c, cp, h): viol1 += 1
print(f"seed={seed} mut={mut} h={h} det(G)={det3(G,h)}: (1) pairs with minors(Gc|Gc')=0: {checked1}, violations of minors(c|c')=0: {viol1}")
if viol1: fails.append(f"(1) {viol1} violations")
# (2) all proportional pairs in the box (only for invertible G)
if mut != "singular":
    Gi = inv3(G, h)
    assert all(mv(Gi, mv(G, c, h), h) == c for c in vecs[:50])
    pairs = 0; a_checked = 0; a_viol = 0; b_checked = 0; b_viol = 0
    for z3 in range(1, 2*N):
        for z1 in range(0, N):
            for z2 in range(0, N):
                if math.gcd(math.gcd(z1, z2), z3) != 1: continue
                mults = [l for l in range(1, 2*N) if N <= l*z3 < 2*N and l*z1 < N and l*z2 < N]
                if len(mults) < 2: continue
                for l1 in mults:
                    for l2 in mults:
                        if l1 == l2: continue
                        u = (l1*z1, l1*z2, l1*z3); v = (l2*z1, l2*z2, l2*z3); pairs += 1
                        c = mv(Gi, tuple(x % h for x in u), h); cp = mv(Gi, tuple(x % h for x in v), h)
                        if math.gcd(c[0], h) == 1:
                            a_checked += 1
                            ok = (cp[2] % h == c[2] % h) if mut == "wrongalpha" else \
                                 ((cp[2] - cp[0]*pow(c[0], -1, h)*c[2]) % h == 0)
                            a_viol += (not ok)
                        uq = tuple(x % q for x in u); vq = tuple(x % q for x in v)
                        if any(uq):
                            b_checked += 1
                            b_viol += (not any(all((t*uq[i] - vq[i]) % q == 0 for i in range(3)) for t in range(q)))
    print(f"   (2) proportional pairs u!=v in box N={N}: {pairs}; alpha checked {a_checked} viol {a_viol}; beta checked {b_checked} viol {b_viol}")
    if a_viol: fails.append(f"(2alpha) {a_viol} violations")
    if b_viol: fails.append(f"(2beta) {b_viol} violations")
if fails:
    print("   FAIL:", *fails); sys.exit(1)
print("   PASS")
