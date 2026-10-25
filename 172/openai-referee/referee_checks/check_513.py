# Numerical sanity check of the one-step Cauchy-Schwarz bound behind (5.13):
# |E_{x,v} psi(v) prod_{w subset [d]} h(x + w.v)| <= sqrt(E psi^2) * ||h||_{U^{d+1}}^{2^d}
import numpy as np, itertools
rng = np.random.default_rng(3)
def gowers_pow(h, k):   # ||h||_{U^k}^{2^k} on Z/q, h real
    q = len(h); tot = 0.0
    for x in range(q):
        for v in itertools.product(range(q), repeat=k):
            pr = 1.0
            for w in itertools.product((0,1), repeat=k):
                pr *= h[(x + sum(a*b for a, b in zip(w, v))) % q]
            tot += pr
    return tot / q**(k+1)
worst = 0.0
for trial in range(25):
    q = int(rng.integers(5, 10)); d = 2
    h = rng.uniform(-1, 1, q) * (rng.uniform() < 0.5) + (rng.uniform(-1, 1, q) if rng.uniform() < 0.5 else 0)
    h = np.clip(h, -1, 1)
    psi = rng.uniform(0, 1, (q, q)) ** 3; psi = psi / psi.mean()
    cube = 0.0
    for x in range(q):
        for v1 in range(q):
            for v2 in range(q):
                pr = 1.0
                for w in itertools.product((0,1), repeat=d):
                    pr *= h[(x + w[0]*v1 + w[1]*v2) % q]
                cube += psi[v1, v2] * pr
    cube /= q**3
    rhs = np.sqrt((psi**2).mean()) * gowers_pow(h, d+1) ** 0.5
    worst = max(worst, abs(cube) / rhs if rhs > 0 else 0)
print("max ratio |cube| / (||psi||_2 ||h||_{U^3}^4) over 25 trials:", round(worst, 4), "(<= 1 expected)")
