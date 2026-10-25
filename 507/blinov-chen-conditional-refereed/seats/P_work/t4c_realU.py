import sys, random
sys.path.insert(0, '/tmp/oaimath/191b/seats/P_work')
import t2_norm as T2
random.seed(11)
r = 37
uval = T2.find_root_u(r)[0]
K, csum, dnorm, Zvec = T2.build(r, uval, list(range(9)))
tags = [0, 1, 3, 4, 9]
words = sorted(sum(((m >> j) & 1)*3**j for j in range(12)) for m in range(4096))
norm = [c for c in words if 10 <= c < 204391]
LOW = 40   # only low coefficients matter; norm positions start at 10 (fill them with random residues to be generic)
def top_digits(xi, normres):
    A = [r]*LOW; Q = [r]*LOW
    A[0] = 1
    for s, t in enumerate(tags): Q[t] = xi[s] if xi[s] else r
    for c in norm:
        if c < LOW:
            A[c] = normres[(c, 1)] or r; Q[c] = normres[(c, 2)] or r
    return A, Q
def U_coeffs(Al, Ql, Am, Qm, n):
    return [sum(Al[i]*Qm[n_-i] - Am[i]*Ql[n_-i] for i in range(n_+1)) for n_ in range(n)]
ok = 0; tot = 0
for trial in range(2000):
    lam = tuple(random.randrange(r) for _ in range(5))
    mu = list(lam)
    s = random.randrange(5)
    mu[s] = (mu[s] + random.randrange(1, r)) % r
    for s2 in range(s+1, 5):
        if random.random() < 0.5: mu[s2] = random.randrange(r)
    mu = tuple(mu)
    resl = {(c, i): random.randrange(r) for c in norm if c < LOW for i in (1, 2)}
    resm = {(c, i): random.randrange(r) for c in norm if c < LOW for i in (1, 2)}
    Al, Ql = top_digits(lam, resl); Am, Qm = top_digits(mu, resm)
    a = tags[s]
    U = U_coeffs(Al, Ql, Am, Qm, 12)
    good = all(U[n] == 0 for n in range(a)) and 0 < abs(U[a]) < r and all(1 <= x <= r for x in Al + Ql + Am + Qm)
    ok += good; tot += 1
print(f'real tag layout, r={r}: U_n=0 for n<a and 0<|U_a|<r in {ok}/{tot} random (lambda,mu) pairs')
# CONTROL: put row-1 residue 1 at position 1 instead of 0 (A_0 = r): the leading coefficient picks up a factor r / shifts
bad = 0
for trial in range(200):
    lam = tuple(random.randrange(r) for _ in range(5)); mu = list(lam); s = 0
    mu[0] = (mu[0] + 1) % r; mu = tuple(mu)
    resl = {(c, i): random.randrange(r) for c in norm if c < LOW for i in (1, 2)}
    Al, Ql = top_digits(lam, resl); Am, Qm = top_digits(mu, resl)
    Al = [r] + Al[1:]; Am = [r] + Am[1:]  # mutated: no unit constant term
    U = U_coeffs(Al, Ql, Am, Qm, 12)
    bad += not (0 < abs(U[0]) < r)
print(f'CONTROL A_0=r (no residue-1 tag): |U_a|<r fails in {bad}/200 (must be >0)')
