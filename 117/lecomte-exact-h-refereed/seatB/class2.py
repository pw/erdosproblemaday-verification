#!/usr/bin/env python3
"""Binary class-two test bed.  An alternating map beta: F2^nu x F2^nu -> F2^e (common radical 0)
is realised by the class-2 group V x W with (v,w)(v',w') = (v+v', w+w'+gamma(v,v')), gamma = upper
triangle of beta; its central quotient is V and lifts of v,v' commute iff beta(v,v')=0.
So omega(P), a(P) can be computed on V\{0}.  We sample random beta, classify the case of Section 5
(radicals of scalar forms: nonabelian / abelian rank-two / abelian noncentral / all central, one or
several components) and check a <= T(omega), with strictness for omega>=9 outside the one-component model."""
import random, itertools, sys, networkx as nx
from ortools.sat.python import cp_model
sys.path.insert(0, '.')
from solve import T

def rank2(rows, n):
    rows = [r for r in rows]; rk = 0
    for bit in range(n):
        piv = None
        for i in range(rk, len(rows)):
            if rows[i] >> bit & 1: piv = i; break
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        for i in range(len(rows)):
            if i != rk and rows[i] >> bit & 1: rows[i] ^= rows[rk]
        rk += 1
    return rk

def form_val(B, v, w, nu):
    # B: list of nu row-bitmasks of an alternating matrix; value v^T B w
    s = 0
    for i in range(nu):
        if v >> i & 1: s ^= bin(B[i] & w).count('1') & 1
    return s

def random_alt(nu, rng):
    B = [0] * nu
    for i in range(nu):
        for j in range(i + 1, nu):
            if rng.random() < 0.5:
                B[i] |= 1 << j; B[j] |= 1 << i
    return B

def comm_structure(Bs, nu):
    n = 1 << nu
    # value of beta(v,w) as an e-bit integer
    def beta(v, w):
        r = 0
        for k, B in enumerate(Bs):
            if form_val(B, v, w, nu): r |= 1 << k
        return r
    return beta

def solve_graph(Vs, commutes, tl=60):
    H = nx.Graph(); H.add_nodes_from(Vs)
    for i, v in enumerate(Vs):
        for w in Vs[i+1:]:
            if commutes(v, w): H.add_edge(v, w)
    maxab = [frozenset(c) for c in nx.find_cliques(H)]
    m2 = cp_model.CpModel(); y = [m2.NewBoolVar('') for _ in maxab]
    cov = {v: [] for v in Vs}
    for i, c in enumerate(maxab):
        for v in c: cov[v].append(y[i])
    for v in Vs: m2.AddBoolOr(cov[v])
    m2.Minimize(sum(y)); s2 = cp_model.CpSolver(); s2.parameters.max_time_in_seconds = 120; s2.parameters.num_workers = 4
    r2 = s2.Solve(m2)
    assert r2 in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    a = int(round(s2.ObjectiveValue()))   # exact if OPTIMAL, else an upper bound (a valid cover)
    chosen = [maxab[i] for i in range(len(maxab)) if s2.Value(y[i])]
    assert set().union(*chosen) >= set(Vs)
    m = cp_model.CpModel(); x = {v: m.NewBoolVar('') for v in Vs}
    for c in maxab: m.Add(sum(x[v] for v in c) <= 1)
    m.Maximize(sum(x.values())); s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 4
    r = s.Solve(m)
    cl = [v for v in Vs if s.Value(x[v])]
    for i, u in enumerate(cl):
        for w in cl[i+1:]: assert not commutes(u, w)
    return len(cl), r == cp_model.OPTIMAL, a, len(maxab)

def classify(Bs, nu):
    """Section-5 case for the class-2 group: every scalar form is a nonzero combination of the B_k.
    Radical of a form = rad(form) in V (plus Z). Radical abelian iff beta vanishes on rad x rad.
    Central iff rad = 0."""
    e = len(Bs); cases = []
    for mask in range(1, 1 << e):
        C = [0] * nu
        for k in range(e):
            if mask >> k & 1: C = [C[i] ^ Bs[k][i] for i in range(nu)]
        rk = rank2(C, nu)
        # radical vectors
        rad = [v for v in range(1 << nu) if all(form_val(C, v, 1 << j, nu) == 0 for j in range(nu))]
        ab = all(all(form_val(B, u, w, nu) == 0 for B in Bs) for u in rad for w in rad)
        cases.append((rk, len(rad), ab))
    if any(not ab for rk, nr, ab in cases): return 'nonabelian-radical'
    if any(rk == 2 for rk, nr, ab in cases): return 'rank-two'
    if any(nr > 1 for rk, nr, ab in cases): return 'abelian-noncentral'
    return 'central-1comp' if e == 1 else 'central-several'

if __name__ == '__main__':
    seed = int(sys.argv[1]); trials = int(sys.argv[2]); nus = [int(t) for t in sys.argv[3].split(',')]
    rng = random.Random(seed)
    for t in range(trials):
        nu = rng.choice(nus)
        e = rng.choice(range(1, min(nu * (nu - 1) // 2, 6) + 1))
        Bs = [random_alt(nu, rng) for _ in range(e)]
        # drop dependent forms and the common radical
        if rank2([int(''.join(str(form_val(B, 1 << i, 1 << j, nu)) for i in range(nu) for j in range(nu)), 2) for B in Bs], nu * nu) < e:
            continue
        beta = comm_structure(Bs, nu)
        Vall = list(range(1, 1 << nu))
        crad = [v for v in Vall if all(beta(v, 1 << j) == 0 for j in range(nu))]
        if crad: continue   # keep only beta with zero common radical so that V = P/Z(P)
        commutes = lambda v, w: beta(v, w) == 0
        om, ex, a, nmax = solve_graph(Vall, commutes)
        case = classify(Bs, nu)
        flag = 'ok'
        if a > T(om): flag = '*** VIOLATION' if ex else 'OPEN'
        elif ex and om >= 9 and a == T(om) and case != 'central-1comp': flag = '*** EQUALITY OUTSIDE MODEL'
        print(f"nu={nu} e={e} case={case} omega={om}{'' if ex else '+'} a={a} T={T(om)} N<=2nu:{om<=2*nu} {flag}", flush=True)
