#!/usr/bin/env python3
"""Check 3: Lemma 4.3 (conditional digit estimate), exact.

Setting: B prime, h = B^k, r | L, L < B. Entry (i,c) of C is sum_u d_{icu} B^u with d_{icu} uniform on
{a in [1,L]: a == res_{icu} (mod r)}, all 9k digits independent; b = min B-adic valuation of the 2x2
minors (capped at k).  Claim (4.5): Pr(b >= j | prescription) <= (r/L)^(4j) for every prescription
(i.e. every fixed label triple, repeated labels allowed); (4.6): E[D] <= 1 + sum theta^j <= 1/(1-theta),
theta = B (r/L)^4.

b >= j depends only on the digits u < j, so Pr(b >= j) is computed EXACTLY by enumerating all
(L/r)^(9j) digit choices at positions u < j (chunked), for:
  - j = 1: EVERY prescription (all r^9 lowest-digit residue patterns);
  - j >= 2: structured prescriptions (all-0, all-1, construction-induced from the d=1 encoding incl.
    repeated labels) + random ones.
Monte-Carlo cross-check of the exact counter on one case (instrument control).
Mutations (must be REJECTED, i.e. produce Pr > bound):
  Mshared3: all three labels equal AND the three columns SHARE one digit draw (paper: fresh digits) -> b = k.
  Mshared2: two columns share one digit draw.
  Mexp: claimed exponent 5j instead of 4j (checks how tight the 4j bound is on the worst prescription).
  ML (hypothesis L < B dropped): reported, not asserted.
"""
import itertools, random, time
import numpy as np

def minors_zero_mod(E, mod):
    # E: (n, 9) entries -> boolean all 2x2 minors == 0 mod `mod`
    M = E.reshape(-1, 3, 3)
    ok = np.ones(len(E), dtype=bool)
    for (i1, i2) in ((0, 1), (0, 2), (1, 2)):
        for (j1, j2) in ((0, 1), (0, 2), (1, 2)):
            mn = (M[:, i1, j1] * M[:, i2, j2] - M[:, i1, j2] * M[:, i2, j1]) % mod
            ok &= (mn == 0)
    return ok

def entry_values(res_entry, j, B, r, L):
    """res_entry: list over u of residues; return all values sum_{u<j} d_u B^u (array)."""
    opts = []
    for u in range(j):
        opts.append([x for x in range(1, L + 1) if x % r == res_entry[u] % r])
    vals = [sum(dg * B ** u for u, dg in enumerate(combo)) for combo in itertools.product(*opts)]
    return np.array(vals, dtype=np.int64)

def exact_prob(res, j, B, r, L, shared=None):
    """res[e][u] residues for entries e = 3*i + c. shared: optional map entry -> entry whose digits it copies.
    Returns exact Pr(b >= j)."""
    mod = B ** j
    vals = [entry_values(res[e], j, B, r, L) for e in range(9)]
    free = [e for e in range(9) if not (shared and e in shared)]
    sizes = [len(vals[e]) for e in free]
    total = int(np.prod(sizes, dtype=np.int64))
    # chunk over the first few free entries
    cnt = 0
    head = free[:3]; tail = free[3:]
    if tail:
        tail_grid = np.array(np.meshgrid(*[np.arange(len(vals[e])) for e in tail], indexing='ij')).reshape(len(tail), -1).T
    else:
        tail_grid = np.zeros((1, 0), dtype=np.int64)
    for hcombo in itertools.product(*[range(len(vals[e])) for e in head]):
        E = np.zeros((len(tail_grid), 9), dtype=np.int64)
        for pos, e in enumerate(head): E[:, e] = vals[e][hcombo[pos]]
        for pos, e in enumerate(tail): E[:, e] = vals[e][tail_grid[:, pos]]
        if shared:
            for e, src in shared.items(): E[:, e] = E[:, src]
        cnt += int(minors_zero_mod(E, mod).sum())
    return cnt / total, cnt, total

def mc_prob(res, j, B, r, L, n, rng):
    mod = B ** j
    E = np.zeros((n, 9), dtype=np.int64)
    for e in range(9):
        for u in range(j):
            opts = np.array([x for x in range(1, L + 1) if x % r == res[e][u] % r])
            E[:, e] += opts[rng.integers(0, len(opts), n)] * B ** u
    return minors_zero_mod(E, mod).mean()

def construction_prescriptions(r, k):
    """d=1, T=1, k=2 encoding: row1 pos0 == 1, row2 pos0 == xi, row3 pos1 == xi^2, others 0.
    Return dict name -> res (9 entries x k positions), for all label triples incl. repeats."""
    out = {}
    if k != 2: return out
    for xs in itertools.product(range(r), repeat=3):
        res = [[0] * k for _ in range(9)]
        for c, xi in enumerate(xs):
            res[0 * 3 + c][0] = 1
            res[1 * 3 + c][0] = xi % r
            res[2 * 3 + c][1] = (xi * xi) % r
        out[f"labels{xs}"] = res
    return out

def run_params(B, k, r, L, rng, nrand_presc, label="", exhaustive_j1=True, maxj=None, hyp_ok=True):
    t0 = time.time()
    bound = lambda j: (r / L) ** (4 * j)
    theta = B * (r / L) ** 4
    maxj = maxj or k
    print(f"\n=== {label} B={B} k={k} r={r} L={L}  (L<B: {L < B}, r|L: {L % r == 0}); theta={theta:.4f} ===")
    worst = {}
    # j = 1 over ALL prescriptions (lowest digit residues), vectorized by enumerating per prescription
    if exhaustive_j1:
        maxp = 0.0; argmax = None
        for pres in itertools.product(range(r), repeat=9):
            res = [[pres[e]] + [0] * (k - 1) for e in range(9)]
            p, c, tot = exact_prob(res, 1, B, r, L)
            if p > maxp: maxp, argmax = p, pres
        worst[1] = maxp
        print(f"  j=1, all {r**9} prescriptions: max Pr(b>=1) = {maxp:.6g} vs bound (r/L)^4 = {bound(1):.6g} "
              f"-> {'OK' if maxp <= bound(1) + 1e-15 else 'VIOLATED'}; argmax lowest-digit residues {argmax}; "
              f"Mexp (r/L)^5={(r/L)**5:.6g}: {'REJECTED (max exceeds it)' if maxp > (r/L)**5 else 'not rejected'}")
    # structured + random prescriptions, all j up to maxj, plus E[D]
    pres_list = dict(construction_prescriptions(r, k))
    pres_list["all0"] = [[0] * k for _ in range(9)]
    pres_list["all1"] = [[1 % r] * k for _ in range(9)]
    for t in range(nrand_presc):
        pres_list[f"rand{t}"] = [[rng.integers(0, r) for _ in range(k)] for _ in range(9)]
    # repeated label patterns: column prescriptions equal (labels equal) but fresh digits
    col = [[rng.integers(0, r) for _ in range(k)] for _ in range(3)]
    pres_list["3equal_labels_fresh"] = [col[e // 3][:] for e in range(9)]
    viol = 0; maxratio = 0.0; EDmax = 0.0
    for name, res in pres_list.items():
        probs = {}
        for j in range(1, maxj + 1):
            p, c, tot = exact_prob(res, j, B, r, L)
            probs[j] = p
            if p > bound(j) + 1e-15: viol += 1
            maxratio = max(maxratio, p / bound(j))
            worst[j] = max(worst.get(j, 0), p)
        if maxj == k:
            ED = sum(B ** j * (probs.get(j, 1.0 if j == 0 else 0) - probs.get(j + 1, 0)) for j in range(1, k + 1)) + (1 - probs[1])
            EDmax = max(EDmax, ED)
    print(f"  {len(pres_list)} structured/random prescriptions, j=1..{maxj}: violations of (4.5): {viol}; "
          f"max Pr/bound = {maxratio:.4f}; worst Pr by j: { {j: f'{v:.4g}' for j, v in worst.items()} }")
    if maxj == k:
        print(f"  max exact E[D] = {EDmax:.6f} vs (4.6) bound 1+sum theta^j = {1 + sum(theta ** j for j in range(1, k + 1)):.6f} "
              f"<= 1/(1-theta) = {1 / (1 - theta) if theta < 1 else float('inf'):.6f}")
    # mutations: shared digits
    res = pres_list["3equal_labels_fresh"]
    for j in range(1, maxj + 1):
        sh3 = {1: 0, 2: 0, 4: 3, 5: 3, 7: 6, 8: 6}   # columns 2,3 copy column 1 digits
        p3, _, _ = exact_prob(res, j, B, r, L, shared=sh3)
        sh2 = {1: 0, 4: 3, 7: 6}                      # column 2 copies column 1
        p2, _, _ = exact_prob(res, j, B, r, L, shared=sh2)
        print(f"  MUTATION shared digits j={j}: 3 shared Pr={p3:.4g}, 2 shared Pr={p2:.4g} vs bound {bound(j):.4g} -> "
              f"{'REJECTED' if p3 > bound(j) else 'not rejected'} / {'REJECTED' if p2 > bound(j) else 'not rejected'}")
    print(f"  [{time.time() - t0:.1f}s]")
    return worst

def main():
    rng = np.random.default_rng(4317)
    # instrument control: exact vs Monte Carlo on one case
    res = [[int(rng.integers(0, 2)) for _ in range(2)] for _ in range(9)]
    pe, _, _ = exact_prob(res, 1, 5, 2, 4)
    pm = mc_prob(res, 1, 5, 2, 4, 400000, rng)
    print(f"instrument control (B=5,r=2,L=4,j=1): exact {pe:.5f} vs MC {pm:.5f}")
    pe2, _, _ = exact_prob(res, 2, 5, 2, 4)
    pm2 = mc_prob(res, 2, 5, 2, 4, 2000000, rng)
    print(f"instrument control (B=5,r=2,L=4,j=2): exact {pe2:.6f} vs MC {pm2:.6f}")
    run_params(5, 2, 2, 4, rng, 40, label="P1")
    run_params(7, 2, 3, 6, rng, 40, label="P2")
    run_params(11, 2, 2, 8, rng, 6, label="P3 (L/r=4)", exhaustive_j1=True, maxj=1)
    run_params(5, 3, 2, 4, rng, 2, label="P4 (k=3, j<=2 exact)", exhaustive_j1=False, maxj=2)
    # j = 3 exact for P4 on one random prescription (8^9 = 1.3e8 configs, chunked)
    t0 = time.time()
    res = [[int(rng.integers(0, 2)) for _ in range(3)] for _ in range(9)]
    p, c, tot = exact_prob(res, 3, 5, 2, 4)
    print(f"  P4 j=3 exact on one prescription: Pr(b>=3) = {p:.4g} ({c}/{tot}) vs bound {(1/2)**12:.4g} [{time.time()-t0:.0f}s]")
    # hypothesis L < B dropped (reported, not asserted)
    run_params(3, 2, 2, 4, rng, 20, label="ML hypothesis L<B DROPPED", hyp_ok=False)

if __name__ == "__main__":
    main()
