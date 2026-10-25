# End-to-end integration test of the proof of Shi-Dong Corollary 1.3 on [N]:
# product of  F1 = Thm 1.1/Cor 4.3 (k=4) colouring of Z/p^4Z restricted to [N],
#             F2 = a colouring with no monochromatic DTZ 4-pattern (stand-in for Lemma 5.1/DTZ L3.2; built greedily),
#             F3 = DTZ Lemma 7.11 colouring (a=(1,2,3,4)) of Z/M^mZ restricted to [N]   (Lemma 5.2),
#             F4 = psi_N of Lemma 5.3.
# Claim: every nontrivial 4-AP in [N] receives >= 3 distinct product colours.  Controls: drop one factor at a time.
import math, sys, itertools
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
def isprime(q): return q > 1 and all(q % r for r in range(2, int(q**.5)+1))
# ---- F1
f4 = math.floor(N ** 0.25 + 1e-12)
p = next(q for q in range(f4+1, 2*f4) if isprime(q) and q > 4)
assert p**4 > N
def irreducible_cubic(p):
    for c2, c1, c0 in itertools.product(range(p), repeat=3):
        if all((t**3 + c2*t*t + c1*t + c0) % p for t in range(p)): return (c0, c1, c2)
f = irreducible_cubic(p)
def mul(a, b):
    c0, c1, c2 = f; r = [0]*5
    for i in range(3):
        for j in range(3): r[i+j] = (r[i+j] + a[i]*b[j]) % p
    for deg in (4, 3):
        co = r[deg]
        if co:
            r[deg] = 0; s = deg-3
            r[s+2] = (r[s+2]-co*c2) % p; r[s+1] = (r[s+1]-co*c1) % p; r[s] = (r[s]-co*c0) % p
    return r[:3]
def pw(a, e):
    res = [1,0,0]
    while e:
        if e & 1: res = mul(res, a)
        a = mul(a, a); e >>= 1
    return res
NT = {z: pw(list(z), 1+p+p*p)[0] for z in itertools.product(range(p), repeat=3)}
assert all(v for z, v in NT.items() if z != (0,0,0))
def F1(n):
    n %= p**4; x = [(n // p**j) % p for j in range(4)]
    return tuple((3*x[j])//p for j in range(3)) + (((x[0] + NT[(x[1],x[2],x[3])]) % p),)
# ---- F2 greedy: no monochromatic 3-subset of a 4-AP (= DTZ 4-patterns: 3-APs and 2n1+n2=3n3)
col2 = [None]*(N+1)
def triples_with_top(n):
    for e in range(1, n):
        for (i, j) in ((1, 2), (1, 3), (2, 3)):   # {n-j e, n-i e, n} scaled patterns with n largest
            pass
    return
cls = {}
for n in range(1, N+1):
    forb = set()
    for e in range(1, n):
        # n is the largest element of the 3-subset {y, y+ae, y+be} of a 4-AP with step e: shapes (0,1,2),(0,1,3),(0,2,3)
        for (a, b) in ((1, 2), (1, 3), (2, 3)):
            y = n - b*e
            if y >= 1 and col2[y] == col2[y + a*e]: forb.add(col2[y])
    c = 0
    while c in forb: c += 1
    col2[n] = c
# ---- F3 DTZ 7.11, M coprime to 24
M3 = next(q for q in itertools.count(5) if math.gcd(q, 24) == 1 and q*q > N)
def F3(n):
    n %= M3*M3; xs = [n % M3, n // M3]
    return (sum(x*x for x in xs), tuple(x % 24 for x in xs))
# ---- F4 Lemma 5.3
M4 = 2**math.ceil(math.sqrt(math.log2(N))); m4 = 1
while M4**m4 < N+1: m4 += 1
def F4(n):
    xs = []; t = n
    for _ in range(m4): xs.append(t % M4); t //= M4
    return tuple((M4-x).bit_length()-1 for x in xs) + (sum(x*x for x in xs),)
cols = [[None]+[F(n) for n in range(1, N+1)] for F in (F1, lambda n: col2[n], F3, F4)]
def check(use):
    prod = [None] + [tuple(cols[i][n] for i in use) for n in range(1, N+1)]
    bad = 0; ex = None
    for d in range(1, (N-1)//3 + 1):
        for a in range(1, N-3*d+1):
            if len({prod[a], prod[a+d], prod[a+2*d], prod[a+3*d]}) <= 2:
                bad += 1
                if ex is None:
                    q = [prod[a+i*d] for i in range(4)]; lab = {}
                    ex = (a, d, "".join(chr(65+lab.setdefault(c, len(lab))) for c in q))
    return bad, ex, len(set(prod[1:]))
bad, ex, pal = check((0,1,2,3))
print(f"N={N}: p={p} (F1 palette<=27p={27*p}), F2 greedy colours={max(col2[1:])+1}, M3={M3}, M4={M4},m4={m4}; "
      f"product palette={pal}; 4-APs with <=2 colours: {bad}")
names = ["F1(Thm1.1)", "F2(L5.1)", "F3(L5.2)", "F4(L5.3)"]
for drop in range(4):
    b, e, _ = check(tuple(i for i in range(4) if i != drop))
    print(f"  control drop {names[drop]}: {b} bad 4-APs, first {e}")
sys.exit(1 if bad else 0)
