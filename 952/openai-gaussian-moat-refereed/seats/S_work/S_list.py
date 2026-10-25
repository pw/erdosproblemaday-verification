# Seat S: Monte Carlo test of the "small list" step of Theorem 5.2 ((5.9)) at parameters where (5.5) actually holds,
# with a negative control showing that conditional independence of the n trials given A=a is load-bearing.
# Setting: one coordinate, group Z/p, a fixed a with conditional displacement law nu_a having (tau',beta') coverage:
# nu_a = uniform on Z/p minus a set E (|E| < p^{1-beta'}), zero on E.  K any set of size u_p = ceil(p^{1-beta}).
# List L = {x : #{l : x + h_l in K} <= n (tau+delta) u_p/p}.  Claim: with prob >= 1 - p exp(-delta^2 n p^{-beta}/2)
# (<= delta/100 by (5.5)) the list has fewer than |E|/delta elements (< p^{1-beta'/2} by (5.5b)).
import numpy as np, math, sys
ADV = len(sys.argv) > 2
rng = np.random.default_rng(5)
p = 4001
import sys
beta, betap = 0.5, float(sys.argv[1]) if len(sys.argv)>1 else 0.25
tau, delta = 0.25, 1/64
taup = tau + 4*delta
u = math.ceil(p**(1-beta))
Esize = math.ceil(p**(1-betap)) - 1          # |E| < p^{1-beta'}
assert Esize < p**(1-betap)
# n from (5.5): p exp(-delta^2 n p^{-beta}/2) <= delta/100
n = math.ceil(2*math.log(100*p/delta)/(delta**2 * p**(-beta)))
print(f"beta'={betap} adversarialK={ADV} p={p} u={u} |E|={Esize} n={n}  (5.5b) delta^-1={1/delta:.0f} < p^(beta'/2)={p**(betap/2):.2f}? {1/delta < p**(betap/2)}")
# (5.5b) fails at this small p (needs p^(beta'/2) > 64, i.e. p > 64^8); we test the list-size bound |L| <= |E|/delta directly.
thr = n*(tau+delta)*u/p
def trial(independent=True):
    E = rng.choice(p, Esize, replace=False)
    nu = np.full(p, 1.0); nu[E] = 0.0; nu /= nu.sum()
    assert (nu[nu > 0] >= taup/p).all()                        # (tau',beta') coverage of nu_a
    K = rng.choice(p, u, replace=False)
    if ADV:  # adversarial K: half of K is a translate of part of E, so some x are genuinely exceptional
        x0 = int(rng.integers(p)); K = np.unique(np.concatenate([(E[:u//2] + x0) % p, K[:u - u//2]]))
    if independent:
        hist = rng.multinomial(n, nu)                          # n iid trials given A=a
    else:
        h1 = rng.choice(p, p=nu); hist = np.zeros(p, dtype=np.int64); hist[h1] = n   # all trials equal (dependent)
    ind = np.zeros(p); ind[K] = 1.0
    # count_x = sum_v hist[v] * 1{x+v in K} = circular correlation
    cnt = np.rint(np.real(np.fft.ifft(np.conj(np.fft.fft(hist)) * np.fft.fft(ind)))).astype(np.int64)
    # cnt[x] = sum_v hist[v] ind[x+v]
    L = np.nonzero(cnt <= thr)[0]
    # exceptional candidates: |(K-x) cap E| > delta*u
    Eind = np.zeros(p); Eind[E] = 1.0
    ov = np.rint(np.real(np.fft.ifft(np.fft.fft(ind) * np.conj(np.fft.fft(Eind))))).astype(np.int64)  # ov[x]=#{k in K: k-x in E}
    exc = set(np.nonzero(ov > delta*u)[0].tolist())
    return len(L), set(L.tolist()) <= exc, len(exc)
for mode in (True, False):
    sizes = []; inside = 0; R = 40
    for _ in range(R):
        s, ok, ne = trial(mode); sizes.append(s); inside += ok
    print(("INDEPENDENT trials" if mode else "NEGATIVE CONTROL (dependent trials)"),
          f": max|L|={max(sizes)} bound |E|/delta={Esize/delta:.0f}  list within exceptional set in {inside}/{R}")
