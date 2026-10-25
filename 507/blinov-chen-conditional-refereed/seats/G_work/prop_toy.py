"""Seat G: toy checks of the three facts behind the sharpened proportional-pair bound (report, finding 1).

 (a) If integer columns u, v are proportional and u = G c, v = G c' (mod h) with det G a unit mod h, then all
     2x2 minors of (c | c') vanish mod h, hence c' = (c'_1/c_1) c (mod h) when c_1 is a unit.
     Mutation 'singularG': det G divisible by B -> implication must FAIL for some instance.
 (b) Digit strings d_0..d_{k-1} with 1 <= d_v <= L3 < B give pairwise distinct residues sum d_v B^v mod B^k.
     Mutation 'bigL': L3 = B + 1 -> a collision must appear.
 (c) A line through the origin meets a cap translate image V = G(a+S) in <= 2 points (exhaustive, small q);
     mutation 'plane': S = an affine plane slice (not a cap) -> some line meets V in >= 3 points.
"""
import sys, random, itertools
MUT = sys.argv[1] if len(sys.argv) > 1 else None
random.seed(7)

def det3(G, m):
    return (G[0][0] * (G[1][1] * G[2][2] - G[1][2] * G[2][1])
            - G[0][1] * (G[1][0] * G[2][2] - G[1][2] * G[2][0])
            + G[0][2] * (G[1][0] * G[2][1] - G[1][1] * G[2][0])) % m

# (a)
B, k = 5, 3
h = B ** k
viol = 0
for trial in range(6000):
    while True:
        if MUT == "singularG":
            av = [random.randrange(h) for _ in range(3)]; bv = [random.randrange(h) for _ in range(3)]
            G = [[av[i] * bv[j] % h for j in range(3)] for i in range(3)]   # rank one: det = 0
            break
        G = [[random.randrange(h) for _ in range(3)] for _ in range(3)]
        if det3(G, h) % B:
            break
    c = [random.randrange(h) for _ in range(3)]
    if trial % 2 == 0:
        lam = random.randrange(h)
        cp = [lam * t % h for t in c]          # premise true by construction
    else:
        cp = [random.randrange(h) for _ in range(3)]
    u = [sum(G[i][j] * c[j] for j in range(3)) % h for i in range(3)]
    v = [sum(G[i][j] * cp[j] for j in range(3)) % h for i in range(3)]
    mu = [(u[i] * v[j] - u[j] * v[i]) % h for i, j in ((0, 1), (0, 2), (1, 2))]
    mc = [(c[i] * cp[j] - c[j] * cp[i]) % h for i, j in ((0, 1), (0, 2), (1, 2))]
    if not any(mu) and any(mc):
        viol += 1
    if not any(mu) and c[0] % B:
        lam2 = cp[0] * pow(c[0], -1, h) % h
        if any((cp[i] - lam2 * c[i]) % h for i in range(3)):
            viol += 1
assert viol == 0, f"minor implication violated {viol} times"

# (b)
B2, k2 = 7, 4
L3 = 6 if MUT != "bigL" else 8
seen = set()
for digits in itertools.product(range(1, L3 + 1), repeat=k2):
    val = sum(dv * B2 ** i for i, dv in enumerate(digits)) % B2 ** k2
    assert val not in seen, "digit-string collision"
    seen.add(val)

# (c)
def projective(v, q):
    for c_ in v:
        if c_:
            iv = pow(c_, q - 2, q)
            return tuple(x * iv % q for x in v)
for q in (11, 13, 17, 19):
    nu = next(t for t in range(2, q) if pow(t, (q - 1) // 2, q) != 1)
    w = 3
    if MUT == "plane":
        S = [(x, y, (x + 2 * y + 1) % q) for x in range(w) for y in range(q)]
    else:
        S = [(x, y, (x * x - nu * y * y) % q) for x in range(w) for y in range(q)]
    for trial in range(30):
        while True:
            G = [[random.randrange(q) for _ in range(3)] for _ in range(3)]
            if det3(G, q):
                break
        a = [random.randrange(q) for _ in range(3)]
        V = [tuple(sum(G[i][j] * ((a[j] + s[j]) % q) for j in range(3)) % q for i in range(3)) for s in S]
        cnt = {}
        for v in V:
            if v == (0, 0, 0):
                continue
            pv = projective(v, q)
            cnt[pv] = cnt.get(pv, 0) + 1
        assert max(cnt.values()) <= 2, "line through origin meets V in >= 3 points"
print("ALL PROP TOY CHECKS PASSED" + (f" (mutation {MUT} NOT detected!)" if MUT else ""))
