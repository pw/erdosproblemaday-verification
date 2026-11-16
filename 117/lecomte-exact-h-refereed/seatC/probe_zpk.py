"""probe_zpk.py -- class-2 groups with NON-elementary central quotient.
A = Z/q^{k} x ... x Z/p^{j} (q = p^2), commutator beta: A x A -> (Z/q)^e alternating biadditive,
beta_l(x,y) = x^T M_l y mod q with M_l antisymmetric, zero diagonal, and entries M_ij divisible by p
whenever coordinate i or j is a Z/p coordinate (well-definedness).  G = A x (Z/q)^e,
(x,c)(y,d) = (x+y, c+d+B(x,y)), B(x,y) = sum_{i<j} M_ij x_i y_j; [g,h] = beta(x,y); G/Z = A/rad(beta).

usage: python3 probe_zpk.py p n_big n_small e count seed0 out.jsonl
   (A = (Z/p^2)^n_big x (Z/p)^n_small)
Same certificate logic as probe.py: a_ub (verified colouring) <= T(omega_lb) and z <= (T(omega_lb)-1)^2.
"""
import sys, json, random, time
import numpy as np
from graphlib import T, check_clique, check_colouring, c_clique, c_heurclique, c_dsatur, c_tabu, colour_sat


def main():
    p, nb, ns, e, count, seed0, out = (int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]),
                                       int(sys.argv[5]), int(sys.argv[6]), sys.argv[7])
    q = p * p
    mods = [q] * nb + [p] * ns
    d = nb + ns
    N = 1
    for m_ in mods:
        N *= m_
    X = np.zeros((N, d), dtype=np.int64)
    for idx in range(N):
        t = idx
        for i, m_ in enumerate(mods):
            X[idx, i] = t % m_
            t //= m_
    with open(out, 'a') as f:
        for s in range(seed0, seed0 + count):
            t0 = time.time()
            rnd = random.Random(s * 7919 + p * 31 + nb * 7 + ns * 3 + e)
            Ms = []
            for _ in range(e):
                M = np.zeros((d, d), dtype=np.int64)
                for i in range(d):
                    for j in range(i + 1, d):
                        x = rnd.randrange(q)
                        if mods[i] == p or mods[j] == p:
                            x = p * rnd.randrange(p)
                        M[i, j] = x
                        M[j, i] = (-x) % q
                Ms.append(M)
            nonc = np.zeros((N, N), dtype=bool)
            for M in Ms:
                nonc |= ((X @ M @ X.T) % q) != 0
            # well-definedness check: beta(x + n_i e_i, y) == beta(x, y)
            for M in Ms:
                for i, m_ in enumerate(mods):
                    assert ((m_ * M[i, :]) % q == 0).all()
            rad = ~nonc.any(axis=1)
            z = N // int(rad.sum())
            classes = {}
            for v in range(N):
                if not rad[v]:
                    classes.setdefault(np.packbits(nonc[v]).tobytes(), v)
            reps = list(classes.values())
            k = len(reps)
            rec = {'p': p, 'A': 'Z%d^%d x Z%d^%d' % (q, nb, p, ns), 'e': e, 'seed': s, 'z': z, 'k': k}
            if k == 0:
                rec.update({'omega_lb': 1, 'a_ub': 1, 'T': 1, 'cert_a': True, 'cert_z': True})
            else:
                sub = nonc[np.ix_(reps, reps)]
                adj = [int(sum(1 << int(j) for j in np.nonzero(sub[i])[0])) for i in range(k)]
                C = c_heurclique(k, adj, 200 if k <= 255 else 60, s)
                Cx, pr = c_clique(k, adj, 20.0, len(C) + 1)
                if Cx is not None:
                    C = Cx
                w = len(C)
                assert check_clique(adj, C)
                t = T(w)
                col = c_dsatur(k, adj)
                a_ub = max(col) + 1
                how = 'dsatur'
                if a_ub > t:
                    c2 = c_tabu(k, adj, t, max(20000, int(4e8 // (k * t))), 1)
                    if c2 is not None:
                        col, a_ub, how = c2, max(c2) + 1, 'tabu'
                if a_ub > t and k <= 400:
                    c3 = colour_sat(k, adj, t, C)
                    if c3 is not None:
                        col, a_ub, how = c3, max(c3) + 1, 'sat'
                assert check_colouring(k, adj, col)
                a_lb = w
                if a_ub >= t:
                    full = (1 << k) - 1
                    cadj = [(~adj[v]) & full & ~(1 << v) for v in range(k)]
                    I, pra = c_clique(k, cadj, 60.0, 0)
                    if pra:
                        a_lb = max(w, -(-k // len(I)))
                rec.update({'omega_lb': w, 'omega_proven': pr, 'a_ub': a_ub, 'a_lb': a_lb, 'a_ub_method': how, 'T': t,
                            'cert_a': a_ub <= t, 'cert_z': z <= (t - 1) ** 2 if w >= 3 else True})
            rec['secs'] = round(time.time() - t0, 2)
            if not (rec['cert_a'] and rec['cert_z']):
                rec['matrices'] = [M.tolist() for M in Ms]
            f.write(json.dumps(rec) + '\n')
            f.flush()
            print(json.dumps({k_: rec[k_] for k_ in rec if k_ != 'matrices'}))
            sys.stdout.flush()


if __name__ == '__main__':
    main()
