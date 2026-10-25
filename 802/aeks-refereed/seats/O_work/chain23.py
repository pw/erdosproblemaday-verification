# Check every intermediate inequality of the proof of Lemma 2.3 on real instances:
# maximizer w (multi-start), disjoint S,D with e^{-x} <= s <= e^x, t <= e^x, multiplier law from Lemma 2.2
# on G[S] with eps=e^{-8x}, k=e^{4x}. Verify: (2.2) identity per realization, E[F(w)-F(q)] >= 0,
# (2.6), vertex-term bound t + k A_r x s, and the final e_w <= A_r x s + e^{-4x}(s^2 + t + t^2/2) <= (A_r+3) x s.
import sys, math, random
from fractions import Fraction as Fr
import numpy as np, networkx as nx
sys.path.insert(0, '/tmp/oaimath/184/seats/O_work/scripts')
from maxim import global_max, F
from lemma22 import multipliers, b_r
from crossmass import make_Kr_free

def Mform(A, a):
    return 0.5 * a @ A @ a

rng = random.Random(11)
r = 4
Ar = 4 + 8 * (r - 2) + (1 + r * (r - 2)) * math.log(2)
worst = {}
nchk = 0; bad = []
for g in range(40):
    n = rng.randint(6, 11)
    G = make_Kr_free(n, rng.choice([0.5, 0.7, 0.9]), r, rng)
    A, w, val, res, loc, _ = global_max(G, nrand=30, seed=g)
    nodes = list(range(n))
    for trial in range(15):
        x = rng.choice([1.0, 1.5, 2.0])
        lab = [rng.randrange(3) for _ in nodes]
        S = [v for v in nodes if lab[v] == 0]; D = [v for v in nodes if lab[v] == 1]
        s = w[S].sum(); t = w[D].sum()
        if not S or not (math.exp(-x) <= s <= math.exp(x)) or t > math.exp(x):
            continue
        eps = math.exp(-8 * x); k = math.exp(4 * x)
        H = nx.Graph(); H.add_nodes_from(S); H.add_edges_from((a, b) for a, b in G.edges() if a in S and b in S)
        wF = {v: Fr(float(w[v])) for v in S}
        law = multipliers(H, S, wF, r, Fr(eps), 'random', rng)
        sind = np.zeros(n); sind[S] = 1
        e_SD = sum(w[u] * w[v] for u in S for v in D if A[u, v])
        EFdiff = 0.0; Evert = 0.0; EMq = 0.0
        for p, m in law:
            p = float(p)
            mv = np.zeros(n)
            for v in S: mv[v] = float(m[v])
            q = w.copy(); q[S] = (1 + k * mv[S]) * w[S]; q[D] = 0.0
            # vertex terms of (2.2)
            with np.errstate(divide='ignore', invalid='ignore'):
                vt = np.where(q > 0, q * np.log(np.where(q > 0, q, 1) / w) - q + w, w)
            Mq = Mform(A, q - w)
            direct = F(A, w) - F(A, q)
            ident = vt.sum() + Mq
            if abs(direct - ident) > 1e-9 * max(1, abs(direct)):
                bad.append(('(2.2) identity', direct, ident))
            EFdiff += p * direct; Evert += p * vt.sum(); EMq += p * Mq
        nchk += 1
        checks = {
            'E[F(w)-F(q)] >= 0': EFdiff >= -1e-9 * max(1, abs(EFdiff)),
            '(2.6)': EMq <= k * k * eps * s * s + 0.5 * t * t - k * e_SD + 1e-9 * k * max(1, e_SD),
            'vertex <= t + k A x s': Evert <= t + k * Ar * x * s + 1e-9,
            'final': e_SD <= Ar * x * s + math.exp(-4 * x) * (s * s + t + t * t / 2) + 1e-12,
            'final2': e_SD <= (Ar + 3) * x * s,
        }
        for kname, okk in checks.items():
            if not okk: bad.append((kname, g, trial, x, s, t, e_SD, EFdiff, EMq, Evert))
        # slack recording
        for kname, val_ in [('EFdiff/(k s)', EFdiff / (k * s)), ('e_SD/(x s)', e_SD / (x * s))]:
            worst[kname] = max(worst.get(kname, -1e99), val_) if kname == 'e_SD/(x s)' else min(worst.get(kname, 1e99), val_)
print('instances checked:', nchk, ' failures:', len(bad))
for b in bad[:10]: print(b)
print('min E[F(w)-F(q)]/(k s) =', worst.get('EFdiff/(k s)'), '  max e_w(S,D)/(x s) =', worst.get('e_SD/(x s)'), ' vs A_4+3 =', Ar + 3)
