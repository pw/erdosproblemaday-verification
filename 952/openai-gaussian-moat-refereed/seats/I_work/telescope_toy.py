# Seat I: toy-scale check of Lemma 8.1 (common-law entropy telescope) + negative control.
# Fixed deterministic self-avoiding walk with steps in {+1,+i,-i} (D=1, K_D=5 incl. zero).
# Time law: t uniform on {0,...,N-1} (stands in for t_*; translate by a changes law by a/N in TV).
# Batches: selected signed Gaussian factors; residue of z=x+iy mod pi_(p,r) is x + r*y mod p, r^2=-1.
# Words W_L(t) = increments z_{t+1}-z_t,...,z_{t+L}-z_{t+L-1}; L_j powers of two, nondecreasing.
# Checks: (i) block step a_{j+1} <= b_j + eps_j  (ii) sum_j (a_j-b_j) <= log K_D + sum eps
# Negative control: drop the nesting (condition on nothing): sum_j I(X_j;W_{L_j})/L_j can exceed log K_D.
import math, random, collections, sys
import sympy

def walk(n, seed):
    rnd = random.Random(seed)
    x, y = 0, 0; last = 'h'
    pts = [(0, 0)]
    for _ in range(n):
        if last == 'h':
            mv = rnd.choice(['h', 'u', 'd'])
        elif last == 'u':
            mv = rnd.choice(['h', 'u'])
        else:
            mv = rnd.choice(['h', 'd'])
        if mv == 'h': x += 1
        elif mv == 'u': y += 1
        else: y -= 1
        last = mv
        pts.append((x, y))
    assert len(set(pts)) == len(pts)          # self-avoiding
    return pts

def sqrt_m1(p):
    for g in range(2, p):
        r = pow(g, (p-1)//4, p)
        if (r*r) % p == p-1:
            return r
    raise ValueError

def H(counter, n):
    return -sum(c/n*math.log(c/n) for c in counter.values())

def hcond(A, B, n):     # H(A|B) for lists of hashable labels over the uniform time set
    return H(collections.Counter(zip(A, B)), n) - H(collections.Counter(B), n)

def binent(e):
    return 0.0 if e <= 0 else -e*math.log(e)-(1-e)*math.log(1-e)

def run(label, batches_primes, lengths, N, seed=1, sign_seed=7):
    Lmax = max(lengths)
    pts = walk(N + 2*Lmax + 2, seed)
    rnd = random.Random(sign_seed)
    # one selected signed factor per prime (fair random sign)
    factors = []
    for batch in batches_primes:
        fs = []
        for p in batch:
            r = sqrt_m1(p)
            if rnd.random() < 0.5: r = p - r
            fs.append((p, r))
        factors.append(fs)
    inc = [(pts[t+1][0]-pts[t][0], pts[t+1][1]-pts[t][1]) for t in range(len(pts)-1)]
    def X(j, t):
        x, y = pts[t]
        return tuple((x + r*y) % p for (p, r) in factors[j])
    def Q(j, t):   # residues of batches 0..j-1 (j batches)
        return tuple(X(i, t) for i in range(j))
    def W(L, t):
        return tuple(inc[t:t+L])
    n = len(factors)
    times = range(N)
    a = []; b = []; uncond = []
    for j in range(n):
        L = lengths[j]
        Wl = [W(L, t) for t in times]
        Qprev = [Q(j, t) for t in times]
        Qcur = [Q(j+1, t) for t in times]
        aj = hcond(Wl, Qprev, N)/L
        bj = hcond(Wl, Qcur, N)/L
        Xj = [X(j, t) for t in times]
        unc = (H(collections.Counter(Wl), N) - hcond(Wl, Xj, N))/L
        a.append(aj); b.append(bj); uncond.append(unc)
    # continuity error for shifting a block by offset a < L_{j+1}: TV = a/N; alphabet of the
    # joint (block, residue vector) restricted to the image of N+Lmax times: <= N+2Lmax points.
    logA = math.log(N + 2*Lmax)
    eps = []
    for j in range(n-1):
        e = (lengths[j+1]-1)/N
        eps.append(2*binent(e) + 2*e*logA)
    print(f"== {label}: N={N}, primes per batch={[list(bt) for bt in batches_primes]}, L={lengths}")
    ok = True
    for j in range(n):
        line = f"   j={j+1}: charge a_j-b_j={a[j]-b[j]:.5f}  a_j={a[j]:.5f}  b_j={b[j]:.5f}  uncond I/L={uncond[j]:.5f}"
        if j+1 < n:
            step_ok = a[j+1] <= b[j] + eps[j] + 1e-12
            ok &= step_ok
            line += f"   [a_{j+2} - b_{j+1} = {a[j+1]-b[j]:+.5f} <= eps={eps[j]:.4f}: {step_ok}]"
        print(line)
    tot = sum(a[j]-b[j] for j in range(n))
    print(f"   nested telescope sum = {tot:.5f}  vs log K_D + sum eps = {math.log(5)+sum(eps):.5f}"
          f"  -> {'HOLDS' if tot <= math.log(5)+sum(eps) else 'VIOLATED'}; all block steps ok: {ok}")
    print(f"   NEGATIVE CONTROL un-nested sum_j I(X_j;W_Lj)/L_j = {sum(uncond):.5f}"
          f"  {'> log K_D (control fires: nesting is load-bearing)' if sum(uncond) > math.log(5) else '<= log K_D'}\n")

def split_primes(lo, k):
    out = []; p = lo
    while len(out) < k:
        p = sympy.nextprime(p)
        if p % 4 == 1: out.append(p)
    return out

N = 20000
# (A) paper-like small-information regime: p moderate, words short relative to sqrt(p)
run("A: moderate primes", [split_primes(400, 2), split_primes(800, 2), split_primes(1600, 2), split_primes(3200, 2)],
    [1, 2, 4, 8], N)
# (B) huge primes: one residue determines z_t hence t hence the whole word
run("B: huge primes (residue pins the time)", [split_primes(10**12, 1), split_primes(2*10**12, 1),
    split_primes(4*10**12, 1), split_primes(8*10**12, 1)], [1, 2, 4, 8], N)
# (C) intermediate: several batches jointly pin the time
run("C: intermediate primes", [split_primes(60, 1), split_primes(150, 1), split_primes(300, 1),
    split_primes(700, 1), split_primes(1500, 1)], [1, 2, 4, 4, 8], N)
