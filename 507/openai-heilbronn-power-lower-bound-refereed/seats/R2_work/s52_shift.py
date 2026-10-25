# Lemma 5.2 checks: |A|>=q^3/2 (exact, real constants), 0 notin V, short-relation exclusion (exhaustive over x, S^3).
import itertools, random, math
from sympy import nextprime

def normq(t, q):
    t %= q
    return min(t, q - t)

def allowed_a1(q, H, w):
    return [a1 for a1 in range(q) if all(normq(m*a1, q) > 3*H*w for m in range(1, 3*H+1))]

def short_x(H):
    return [x for x in itertools.product(range(-H, H+1), repeat=3)
            if x != (0, 0, 0) and x[0]**2 + x[1]**2 + x[2]**2 <= H*H]

def aff_indep(u1, u2, u3, q):
    a = [(u2[i]-u1[i]) % q for i in range(3)]
    b = [(u3[i]-u1[i]) % q for i in range(3)]
    cr = [(a[1]*b[2]-a[2]*b[1]) % q, (a[2]*b[0]-a[0]*b[2]) % q, (a[0]*b[1]-a[1]*b[0]) % q]
    return cr != [0, 0, 0]

def greedy_cap(q, w, target, rng):
    pts = [(X, Y, Z) for X in range(w) for Y in range(w) for Z in range(w)]
    rng.shuffle(pts)
    S = []
    for p in pts:
        if all(not (not aff_indep(p, s1, s2, q)) for s1, s2 in itertools.combinations(S, 2)):
            S.append(p)
            if len(S) >= target: break
    return S

# (1) real constants: fraction of allowed shifts
for H in []:
    q = nextprime(2000*H*H - 1)
    for qq in [q, nextprime(7*q), nextprime(60*q)]:
        w = qq // (1000*H*H)
        A1 = allowed_a1(qq, H, w)
        frac = len(A1) / qq
        print(f"H={H} q={qq} w={w}: allowed a1 fraction = {frac:.4f} (>=1/2: {frac>=0.5}); union bound 3H(6Hw+1)/q = {3*H*(6*H*w+1)/qq:.4f}", flush=True)

# (2) exclusion logic (needs only 3Hw<q/2 and def of A); S = random no-three-collinear subset of the box
rng = random.Random(1)
cases = []
for q, H, w, tgt in cases:
    assert 3*H*w < q/2
    S = greedy_cap(q, w, tgt, rng)
    A1 = allowed_a1(q, H, w)
    X = short_x(H)
    viol = 0; checked = 0; zero_in_V = 0
    for trial in range(3):
        a = (rng.choice(A1), rng.randrange(q), rng.randrange(q))
        Sa = [tuple((a[i]+v[i]) % q for i in range(3)) for v in S]
        if (0, 0, 0) in Sa: zero_in_V += 1
        for u in itertools.product(Sa, repeat=3):
            ai = aff_indep(*u, q)
            for x in X:
                if sum(x) == 0 and not ai: continue
                if all((x[0]*u[0][i] + x[1]*u[1][i] + x[2]*u[2][i]) % q == 0 for i in range(3)):
                    viol += 1
                checked += 1
    print(f"q={q} H={H} w={w}: |S|={len(S)} |allowed a1|/q={len(A1)/q:.3f} zero-in-V={zero_in_V} relations checked={checked} violations={viol}", flush=True)

# (3) negative control: an a1 just OUTSIDE A must admit a relation for some S in the box (shows the instrument can fail)
q, H, w = 1009, 2, 20
bad_a1 = [a1 for a1 in range(q) if a1 not in set(allowed_a1(q, H, w))]
found = False
for a1 in bad_a1[:50]:
    for m in range(1, 3*H+1):
        if normq(m*a1, q) <= 3*H*w:
            # try to realise m*a1 = -sum x_i v_i with |x|<=H, v_i in [0,w)
            for x in short_x(H):
                if sum(x) != m: continue
                for v in itertools.product(range(w), repeat=3):
                    if (m*a1 + sum(xi*vi for xi, vi in zip(x, v))) % q == 0:
                        found = (a1, m, x, v); break
                if found: break
        if found: break
    if found: break
print("negative control (disallowed shift admits a first-coordinate relation):", found)
