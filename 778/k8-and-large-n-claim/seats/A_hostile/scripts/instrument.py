#!/usr/bin/env python3
"""Hostile numerical instrument for Didin-Pimenov (1:2) clique game, Lemma 1 bookkeeping.

Exact arithmetic. P_U = K * p_U with K = (4/3)^(3H/5) (common to all U),
p_U = (3/4)^{x_U} (5/6)^{f_U} while 5 x_U < 3H, else 0.
Values are pairs (alpha, beta) meaning alpha + beta*K; compared exactly via K^5 = (4/3)^(3H).

Weights are RECOMPUTED FROM THE DEFINITION after every move; the update table is
then asserted against the recomputed values (so the table is tested, not assumed).
"""
import itertools, random, sys
from fractions import Fraction as F
MUT = None   # negative-control mutations: one_edge | min_danger | danger_P5 | base54 | qbase2

class Ctx:
    def __init__(s, n, a, l, use_Q=True, use_P=True):
        s.n, s.a, s.l = n, a, l
        s.use_Q, s.use_P = use_Q, use_P
        s.edges = list(itertools.combinations(range(n), 2))
        s.eid = {e: i for i, e in enumerate(s.edges)}
        s.E = len(s.edges)
        s.h = a * (a - 1) // 2
        s.H = l * (l - 1) // 2
        s.K5 = F(4, 3) ** (3 * s.H)          # K^5
        s.Asets = [[s.eid[p] for p in itertools.combinations(A, 2)] for A in itertools.combinations(range(n), a)]
        s.Usets = [[s.eid[p] for p in itertools.combinations(U, 2)] for U in itertools.combinations(range(n), l)]
        s.A_of = [[] for _ in range(s.E)]
        s.U_of = [[] for _ in range(s.E)]
        for i, A in enumerate(s.Asets):
            for e in A: s.A_of[e].append(i)
        for i, U in enumerate(s.Usets):
            for e in U: s.U_of[e].append(i)

    # exact comparison of alpha+beta*K
    def cmp(s, x, y):
        da, db = x[0] - y[0], x[1] - y[1]
        if db == 0: return (da > 0) - (da < 0)
        if da == 0: return (db > 0) - (db < 0)
        if (da > 0) == (db > 0): return 1 if da > 0 else -1
        # opposite signs: compare |da| vs |db| K  <=> |da|^5 vs |db|^5 K^5
        lhs, rhs = abs(da) ** 5, abs(db) ** 5 * s.K5
        if lhs == rhs: return 0      # impossible unless K rational; handled
        bigger_alpha = lhs > rhs
        if da > 0: return 1 if bigger_alpha else -1
        else: return -1 if bigger_alpha else 1

    def weights(s, own):
        Q = []
        for A in s.Asets:
            if any(own[e] == 2 for e in A): Q.append(F(0))
            else: Q.append(F(1, (2 if MUT == 'qbase2' else 3) ** sum(1 for e in A if own[e] == 0)))
        P = []
        for U in s.Usets:
            x = sum(1 for e in U if own[e] == 2); f = sum(1 for e in U if own[e] == 0)
            if 5 * x >= 3 * s.H: P.append(F(0))
            else: P.append((F(4, 5) if MUT == 'base54' else F(3, 4)) ** x * F(5, 6) ** f)
        if not s.use_Q: Q = [F(0)] * len(Q)
        if not s.use_P: P = [F(0)] * len(P)
        return Q, P

    def phi(s, Q, P): return (sum(Q, F(0)), sum(P, F(0)))

    def danger(s, e, Q, P):
        return (sum((Q[i] for i in s.A_of[e]), F(0)), sum((P[i] for i in s.U_of[e]), F(0)) / (5 if MUT == 'danger_P5' else 10))

def play(ctx, bella, rng, stats, tag):
    own = [0] * ctx.E
    free = set(range(ctx.E))
    viol = []
    def V(msg):
        viol.append(f"[{tag}] {msg}")
    # Bella opening
    Q0, P0 = ctx.weights(own)
    z = bella(ctx, own, free, Q0, P0, rng)
    own[z] = 1; free.discard(z)
    Q, P = ctx.weights(own)
    # initial-weight bounds from the paper (with n replaced by actual set counts)
    if ctx.use_Q and sum(Q) > 3 * len(ctx.Asets) * F(1, 3 ** ctx.h): V("initial sum Q exceeds 3 C(n,a) 3^-h")
    if ctx.use_P and sum(P) > F(6, 5) * len(ctx.Usets) * F(5, 6) ** ctx.H: V("initial sum P exceeds (6/5)C(n,l)theta^H")
    phi_init = ctx.phi(Q, P)
    stats['games'] += 1
    while free:
        phi_round_start = ctx.phi(Q, P)
        # Chingiz: two edges (or fewer if fewer remain)
        for k in range(1 if MUT == 'one_edge' else 2):
            if not free: break
            ds = {e: ctx.danger(e, Q, P) for e in free}
            best = None
            for e in free:
                if best is None or ctx.cmp(ds[e], ds[best]) * (-1 if MUT == 'min_danger' else 1) > 0: best = e
            maxes = [e for e in free if ctx.cmp(ds[e], ds[best]) == 0]
            c = rng.choice(sorted(maxes))
            phi_before = ctx.phi(Q, P)
            own[c] = 2; free.discard(c)
            Qn, Pn = ctx.weights(own)
            # update table, Chingiz column
            for i in ctx.A_of[c]:
                if Qn[i] != 0: V(f"Q_A not zeroed by Chingiz edge {ctx.edges[c]}")
            for i in ctx.U_of[c]:
                if Pn[i] > F(9, 10) * P[i]: V(f"P_U not <= 9/10 P_U under Chingiz edge {ctx.edges[c]}")
            for i in range(len(Q)):
                if c not in ctx.Asets[i] and Qn[i] != Q[i]: V("Q of set not containing e changed")
            for i in range(len(P)):
                if c not in ctx.Usets[i] and Pn[i] != P[i]: V("P of set not containing e changed")
            phi_after = ctx.phi(Qn, Pn)
            drop = (phi_before[0] - phi_after[0], phi_before[1] - phi_after[1])
            if ctx.cmp(drop, ds[c]) < 0: V(f"Chingiz edge {ctx.edges[c]} decreased Phi by LESS than its danger")
            stats['chingiz_edges'] += 1
            # danger of every remaining free edge non-increasing, BOTH summands
            for e in free:
                dn = ctx.danger(e, Qn, Pn)
                if dn[0] > ds[e][0] or dn[1] > ds[e][1]: V(f"danger of free edge {ctx.edges[e]} increased after Chingiz move")
                stats['danger_monotone_checks'] += 1
            Q, P = Qn, Pn
        if not free:
            stats['truncated_endings'] += 1
            if ctx.cmp(ctx.phi(Q, P), phi_round_start) > 0: V("Phi increased over truncated last round")
            break
        # Bella
        z = bella(ctx, own, free, Q, P, rng)
        dstar = ctx.danger(z, Q, P)
        phi_before = ctx.phi(Q, P)
        own[z] = 1; free.discard(z)
        Qn, Pn = ctx.weights(own)
        for i in ctx.A_of[z]:
            if Qn[i] != 3 * Q[i]: V(f"Q_A not tripled by Bella edge")
        for i in ctx.U_of[z]:
            if Pn[i] != F(6, 5) * P[i]: V(f"P_U not x6/5 by Bella edge")
        phi_after = ctx.phi(Qn, Pn)
        inc = (phi_after[0] - phi_before[0], phi_after[1] - phi_before[1])
        if ctx.cmp(inc, (2 * dstar[0], 2 * dstar[1])) != 0: V("Bella increase != 2 d*(z) exactly")
        stats['bella_exact_checks'] += 1
        Q, P = Qn, Pn
        if ctx.cmp(ctx.phi(Q, P), phi_round_start) > 0: V(f"Phi INCREASED over a complete round")
        stats['complete_rounds'] += 1
    phi_end = ctx.phi(Q, P)
    if ctx.cmp(phi_end, phi_init) > 0: V("Phi_end > Phi_init")
    # terminal implications (contrapositive form: property fails => Phi >= 1)
    one = (F(1), F(0))
    noC_A = [A for A in ctx.Asets if all(own[e] == 1 for e in A)]
    lowU = [U for U in ctx.Usets if 5 * sum(1 for e in U if own[e] == 2) < 3 * ctx.H]
    if ctx.use_Q and noC_A and ctx.cmp(phi_end, one) < 0: V("a-set with no Chingiz edge but Phi_end < 1")
    if ctx.use_P and lowU and ctx.cmp(phi_end, one) <= 0: V("l-set with e_C < 3H/5 but Phi_end <= 1")
    if ctx.cmp(phi_init, one) < 0:
        stats['phi_init_below_1'] += 1
        if ctx.use_Q and noC_A: V("Phi_init<1 yet Bella got an a-clique")
        if ctx.use_P and lowU: V("Phi_init<1 yet some l-set has e_C < 3H/5")
    stats['bella_has_a_clique'] += bool(noC_A)
    stats['some_lowU'] += bool(lowU)
    return viol

# Bella strategies
def b_random(ctx, own, free, Q, P, rng): return rng.choice(sorted(free))
def _maxby(ctx, free, key, rng, sign=1):
    best = None; bl = []
    for e in sorted(free):
        k = key(e)
        if best is None or ctx.cmp(k, best) * sign > 0: best, bl = k, [e]
        elif ctx.cmp(k, best) == 0: bl.append(e)
    return rng.choice(bl)
def b_maxdanger(ctx, own, free, Q, P, rng): return _maxby(ctx, free, lambda e: ctx.danger(e, Q, P), rng, 1)
def b_mindanger(ctx, own, free, Q, P, rng): return _maxby(ctx, free, lambda e: ctx.danger(e, Q, P), rng, -1)
def b_cliquey(ctx, own, free, Q, P, rng):   # maximise Q-part only (pure clique builder)
    return _maxby(ctx, free, lambda e: (sum((Q[i] for i in ctx.A_of[e]), F(0)), F(0)), rng, 1)
def b_density(ctx, own, free, Q, P, rng):   # attack Chingiz density: maximise P-part only
    return _maxby(ctx, free, lambda e: (F(0), sum((P[i] for i in ctx.U_of[e]), F(0))), rng, 1)

STRATS = {'random': b_random, 'maxdanger': b_maxdanger, 'mindanger': b_mindanger, 'cliquey': b_cliquey, 'density': b_density}

def run(configs, games_random, games_adv, seed=778):
    rng = random.Random(seed)
    allv = []
    report = []
    for (n, a, l, uq, up) in configs:
        ctx = Ctx(n, a, l, uq, up)
        stats = dict(games=0, chingiz_edges=0, danger_monotone_checks=0, bella_exact_checks=0, complete_rounds=0,
                     truncated_endings=0, phi_init_below_1=0, bella_has_a_clique=0, some_lowU=0)
        for name, strat in STRATS.items():
            G = games_random if name == 'random' else games_adv
            for g in range(G):
                v = play(ctx, strat, rng, stats, f"n={n} a={a} l={l} Q={uq} P={up} bella={name} g={g}")
                allv += v
        line = (f"n={n} a={a} l={l} (h={ctx.h}, H={ctx.H}, 3H/5={F(3*ctx.H,5)}) families Q={uq} P={up}: " +
                ", ".join(f"{k}={v}" for k, v in stats.items()))
        print(line, flush=True); report.append(line)
    return allv, report

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'main'
    if mode == 'main':
        cfg = [(n, a, l, True, True) for n in (6, 7, 8, 9) for a in (3, 4) for l in (4, 5)]
        v, _ = run(cfg, games_random=60, games_adv=15)
    elif mode == 'qonly':
        # Q-family alone, parameters where initial Phi_Q < 1 genuinely holds (Erdos-Selfridge regime)
        cfg = [(7, 4, 4, True, False), (8, 4, 4, True, False), (9, 4, 4, True, False), (10, 4, 4, True, False)]
        v, _ = run(cfg, games_random=60, games_adv=15)
    elif mode.startswith('mut:'):
        MUT = mode[4:]
        globals()['MUT'] = MUT
        cfg = [(7, 4, 4, True, True), (8, 3, 5, True, True), (8, 4, 4, True, False)]
        v, _ = run(cfg, games_random=8, games_adv=2)
        kinds = {}
        for x in v:
            k = x.split('] ', 1)[1].split(' {')[0]
            k = ''.join(ch for ch in k if not ch.isdigit())
            kinds[k] = kinds.get(k, 0) + 1
        print("MUTATION", MUT, "violation kinds:", kinds)
    elif mode == 'big':
        cfg = [(10, 4, 5, True, True), (10, 3, 4, True, True)]
        v, _ = run(cfg, games_random=10, games_adv=3)
    print(f"VIOLATIONS: {len(v)}")
    for x in v[:50]: print("  ", x)
