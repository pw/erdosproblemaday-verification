# Seat T numeric 2: exact evaluation of the finite density sums A_delta (printed eq. (20)) for two
# one-dimensional factors, compared with the main term of Proposition 5.1 (printed eqs. (13),(14)).
# Scale: F(log d / ell) with ell = log N, support d <= N (budget 1 per factor). The Fourier evaluation of
# A_delta in printed Section 5.2 uses no support budget -- the budget only enters Lemma 5.3 -- so this
# tests the analytic half of Prop 5.1 at finite ell.
import numpy as np, math, sys

def sieve(N):
    mu = np.ones(N + 1, np.int8); phi = np.arange(N + 1, dtype=np.int64)
    isp = np.ones(N + 1, bool); isp[:2] = False
    for p in range(2, N + 1):
        if isp[p]:
            isp[2 * p::p] = False
            mu[p::p] *= -1
            mu[p * p::p * p] = 0
            phi[p::p] -= phi[p::p] // p
    mu[0] = 0
    return mu, phi, np.nonzero(isp)[0]

def bump(x):  # smooth bump on (0,1), flat to all orders at 0 and 1
    out = np.zeros_like(x); m = (x > 0) & (x < 1)
    out[m] = np.exp(-1.0 / (x[m] * (1 - x[m])))
    return out

xs = np.linspace(0, 1, 200001); bx = bump(xs)
cum = np.concatenate([[0], np.cumsum((bx[1:] + bx[:-1]) / 2 * np.diff(xs))]); tot = cum[-1]

def F_face(x):  # F(x) = int_x^1 bump ;  -F' = bump vanishes at 0 (face-vanishing case)
    return np.interp(np.clip(x, 0, 1), xs, tot - cum) * (x <= 1)

I_face = float(np.sum((bx[1:]**2 + bx[:-1]**2) / 2 * np.diff(xs)))

def F_poly(x):  # (1-x)^4 : -F'(0) = 4 (non face-vanishing case)
    return np.where(x <= 1, (1 - np.clip(x, 0, 1))**4, 0.0)

I_poly = 16 / 7.0

def prime_divisors(D):
    return [p for p in range(2, D + 1) if D % p == 0 and all(p % q for q in range(2, p))]

def h_of(es, PR, N):  # h(e) = prod_{p|e}(p-2), e squarefree
    h_e = np.ones(len(es)); rem = es.copy()
    for p in PR:
        if p * p > N:
            break
        m = (rem % p == 0)
        h_e[m] *= (p - 2); rem[m] //= p
    big = rem > 1
    h_e[big] *= (rem[big] - 2)
    return h_e

def run(N, Ffun, Deltas, mDeltas, mu, phi, PR):
    d = np.arange(N + 1); ell = math.log(N)
    Fv = np.zeros(N + 1); Fv[1:] = Ffun(np.log(d[1:]) / ell)
    a = np.zeros(N + 1); a[1:] = mu[1:] * Fv[1:] / d[1:]
    sq = np.nonzero(mu)[0]
    y = np.zeros(N + 1)
    for e in sq:
        y[e] = a[e::e].sum()
    res = {'same': float(np.sum(phi[sq] * y[sq]**2))}
    for D in Deltas:  # distinct shifts, difference D: A = sum_e y(e)^2 sum_{g|(e,D)} g mu(e/g)
        w = mu[sq].astype(float).copy()
        for g in range(2, D + 1):
            if D % g == 0 and mu[g] != 0:
                m = (sq % g == 0)
                w[m] += g * mu[sq[m] // g]
        res[('dist', D)] = float(np.sum(w * y[sq]**2))
    for D in mDeltas:  # marked: same shift a1, mark a0, a1-a0=D. A_1 = sum_{(e,D)=1} h(e) yt(e)^2
        ok = np.ones(N + 1, bool)
        for p in prime_divisors(D):
            ok[::p] = False
        at = np.zeros(N + 1); at[1:] = np.where(ok[1:], mu[1:] * Fv[1:] / phi[1:], 0.0)
        es = sq[ok[sq]]
        yt = np.zeros(N + 1)
        for e in es:
            yt[e] = at[e::e].sum()
        res[('marked', D)] = float(np.sum(h_of(es, PR, N) * yt[es]**2))
    return ell, res

C2 = 0.6601618158468696
def S2(D):
    if D % 2:
        return 0.0
    v = 2 * C2
    for p in prime_divisors(D):
        if p > 2:
            v *= (p - 1) / (p - 2)
    return v

Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 10**6
mu_all, phi_all, PR = sieve(Nmax)
print(f"I_face=int(F')^2={I_face:.6e}  I_poly={I_poly:.6f}", flush=True)
Ns = [10**3, 10**4, 10**5, 10**6] + ([Nmax] if Nmax > 10**6 else [])
for N in Ns:
    for name, Ff, If, Fp0 in [("face", F_face, I_face, 0.0), ("poly", F_poly, I_poly, 4.0)]:
        ell, r = run(N, Ff, [1, 2, 6], [2, 6], mu_all[:N + 1], phi_all[:N + 1], PR)
        line = f"N={N:.0e} ell={ell:6.2f} {name}: ell*A_same/int={ell*r['same']/If:.4f} (pred 1)"
        for D in [1, 2, 6]:
            line += f" | D={D}: ell^2*A={ell**2*r[('dist',D)]:+.4f} (pred {S2(D)*Fp0**2:.3f})"
        for D in [2, 6]:
            line += f" | mk D={D}: ell*A1/int={ell*r[('marked',D)]/If:.4f} (pred {S2(D):.4f})"
        print(line, flush=True)
