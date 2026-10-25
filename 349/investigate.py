#!/usr/bin/env python3
"""Round-4 open questions, driven by the exact checker.

(A) exact shape / asymptotic of the entire-complete boundary t0(alpha):
    for each alpha, find t0 (largest t with no early gap => entire, alpha<2), AND the index k of
    the first greedy constraint that binds just above t0 (the binding early-gap constraint), plus
    the last clean prefix at t0 -- so we can read off the exact floor-inequality that governs the
    boundary in each alpha-regime.

(B) cofinite-completeness region for alpha in [phi,2): does 0-indexed push past t0 (and past t=2)?
    Discriminator (robust to the covered-tail artifact): count missing integers in [1,N] at
    N=100k/200k/400k. If the count STABILIZES (same at all three) the gaps are finite => cofinitely
    complete (empirical). If it GROWS, gaps recur => not cofinitely complete. entire_cert = proven.
"""
from fractions import Fraction
import lab

PHI = lab.PHI


def F(x):
    return Fraction(x)


def t0_and_binding(alpha, t_lo=F(1), t_hi=F("1999/1000"), step=2000, nterms=40):
    """Linear scan for t0 (max t with greedy no-gap through nterms), then binding k above it."""
    best = None
    for i in range(step + 1):
        t = t_lo + (t_hi - t_lo) * Fraction(i, step)
        if lab.greedy_entire(t, alpha, n_terms=nterms, start=0)["entire"]:
            best = t
    if best is None:
        return None, None, None, None
    # binding constraint just above t0
    t_above = min(best + Fraction(3, 1000), F("1999/1000"))
    terms = lab.floors(t_above, alpha, n_terms=nterms, start=0)
    C = 0
    bind_k = None
    bind_detail = None
    for k, s in enumerate(terms):
        if s == 0:
            continue
        if s > C + 1:
            bind_k = k
            bind_detail = (s, C + 1)  # term vs the +1 ceiling it exceeded
            break
        C += s
    clean_prefix = lab.floors(best, alpha, n_terms=(bind_k or 6), start=0)
    return float(best), bind_k, bind_detail, clean_prefix


def cofinite_verdict(alpha, t):
    """entire / cofinite-empirical / incomplete, via missing-count stabilization."""
    c = lab.entire_cert_0indexed(t, alpha)
    if c["proven"]:
        return "ENTIRE(proven)", 0, 0, 0, 1
    counts = []
    tails = []
    for N in (100_000, 200_000, 400_000):
        terms = lab.floors(t, alpha, max_val=N, start=0)
        bits = lab.subsetsum_bits(terms, N)
        present = bin(bits >> 1).count("1")
        counts.append(N - present)
        r = lab.gap_to_N(t, alpha, N=N, start=0)
        tails.append(r["covered_tail_from"])
    m1, m2, m4 = counts
    if m2 == m4 and m1 == m2:
        verdict = f"COFINITE-emp (gaps={m4})"
    elif m4 > m2 > m1:
        verdict = "INCOMPLETE (gaps recur)"
    elif m4 == m2:
        verdict = f"COFINITE-emp? (gaps={m4}, check deeper)"
    else:
        verdict = f"unclear ({m1},{m2},{m4})"
    return verdict, m1, m2, m4, tails[-1]


if __name__ == "__main__":
    print("=" * 96)
    print("(A)  t0(alpha) + binding early-gap constraint  (0-indexed entire-complete boundary)")
    print("=" * 96)
    print(f"{'alpha':>7} {'t0':>8} {'bindk':>6} {'term>C+1':>12} {'clean prefix at t0'}")
    print("-" * 96)
    for als in ["1.05", "1.1", "1.2", "1.3", "1.4", "1.45", "1.5", "1.55", "1.6", "1.618",
                "1.65", "1.7", "1.72", "1.75", "1.78", "1.8", "1.83", "1.85", "1.88", "1.9",
                "1.92", "1.95", "1.97", "1.99"]:
        a = F(als)
        t0, bk, bd, pref = t0_and_binding(a)
        if t0 is None:
            print(f"{als:>7} {'none':>8}")
            continue
        bds = f"{bd[0]}>{bd[1]}" if bd else "-"
        print(f"{als:>7} {t0:>8.4f} {str(bk):>6} {bds:>12}   {pref}")

    print()
    print("=" * 96)
    print("(B)  cofinite-completeness in [phi,2): 0-indexed, does it push past t0 / past t=2?")
    print("     (1-idx col = same point on 1-indexed, for the free-transfer / Prop-3 contrast)")
    print("=" * 96)
    print(f"{'alpha':>7} {'t':>6} {'0-idx verdict':>26} {'miss@400k':>10} {'tail@400k':>10} {'1-idx miss@400k':>15}")
    print("-" * 96)
    grid = [("1.618", [1.5, 1.8, 1.85, 2.0, 2.5]),
            ("1.7", [1.5, 1.7, 1.72, 2.0, 2.5]),
            ("1.75", [1.4, 1.6, 1.62, 2.0, 2.5]),
            ("1.8", [1.3, 1.5, 1.54, 2.0, 2.5]),
            ("1.85", [1.2, 1.4, 1.41, 2.0]),
            ("1.9", [1.1, 1.3, 1.3, 2.0]),
            ("1.95", [1.05, 1.16, 1.16, 2.0])]
    for als, ts in grid:
        a = F(als)
        for tv in ts:
            t = F(tv)
            v, m1, m2, m4, tail = cofinite_verdict(a, t)
            # 1-indexed missing at 400k
            t1 = lab.floors(t, a, max_val=400_000, start=1)
            b1 = lab.subsetsum_bits(t1, 400_000)
            miss1 = 400_000 - bin(b1 >> 1).count("1")
            print(f"{als:>7} {tv:>6.2f} {v:>26} {m4:>10} {tail:>10} {miss1:>15}")
        print()
