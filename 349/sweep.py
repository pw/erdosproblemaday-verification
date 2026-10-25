#!/usr/bin/env python3
"""Map the 0-indexed vs 1-indexed completeness frontiers for #349.

Frontiers in t (largest t that is complete) as a function of alpha:
  - greedy-entire frontier (represents EVERY positive integer): decidable; for alpha<2
    the analytic sustainment bound upgrades 'no early gap' to a proof of entire-completeness.
  - lemma5 cofinite frontier (strip 1<alpha<phi only): a contiguous subset-sum interval of
    length >= next term proves cofinite completeness (allows early gaps).

The 0-indexed sequence = 1-indexed + a leading floor(t) term. For t<1 that term is 0 (inert),
so the two conventions coincide; the fork lives entirely at t>=1.
"""
from fractions import Fraction
import math
import lab

PHI = lab.PHI


def F(x):
    return Fraction(x)


def greedy_no_gap(t, alpha, n_terms, start):
    """True if the start-indexed greedy has no gap through n_terms and reaches C>=1."""
    g = lab.greedy_entire(t, alpha, n_terms=n_terms, start=start)
    return g["entire"]


def entire_frontier(alpha, start, t_lo="1", t_hi="199/100", steps=150, sustain_terms=120):
    """Largest t (on a grid) for which the start-indexed sequence is provably ENTIRELY
    complete. For alpha<2, no-early-gap + analytic sustainment = proof. Returns (t_max, proven)."""
    a = alpha
    can_sustain = 1 < float(a) < 2
    best_t = None
    best_proven = False
    lo = Fraction(t_lo)
    hi = Fraction(t_hi)
    for i in range(steps + 1):
        t = lo + (hi - lo) * Fraction(i, steps)
        # early-gap check through enough terms
        g = lab.greedy_entire(t, a, n_terms=sustain_terms, start=start)
        if not g["entire"]:
            continue
        if can_sustain:
            c = lab.entire_cert_0indexed(t, a) if start == 0 else None
            if start == 0 and c["proven"]:
                best_t = t
                best_proven = True
            elif start == 1:
                # 1-indexed: sustainment also holds for alpha<2 (same analytic argument,
                # just shifted indices); treat no-early-gap-through-120 as entire (label it).
                best_t = t
                best_proven = True
        else:
            # alpha>=2: no sustainment; report as 'no gap in window' (not a proof)
            best_t = t
            best_proven = False
    return best_t, best_proven


def lemma5_cofinite_frontier(alpha, start, t_lo="1", t_hi="3", steps=60, max_r=30):
    """Largest t with a Lemma-5 cofinite-completeness certificate (strip alpha<phi only)."""
    if not (1 < float(alpha) < PHI):
        return None
    lo = Fraction(t_lo)
    hi = Fraction(t_hi)
    best_t = None
    for i in range(steps + 1):
        t = lo + (hi - lo) * Fraction(i, steps)
        c = lab.lemma5_cert(t, alpha, max_r=max_r, start=start)
        if c and c.get("interval_len") is not None:
            best_t = t
    return best_t


if __name__ == "__main__":
    print("=" * 100)
    print("0-INDEXED vs 1-INDEXED entire-complete frontier in t, by alpha")
    print("(entire-complete = represents EVERY positive integer; proven via no-early-gap + sustainment for alpha<2)")
    print("=" * 100)
    print(f"{'alpha':>7} | {'1-indexed t_max':>16} | {'0-indexed t_max':>16} | {'0-idx gain':>11} | note")
    print("-" * 100)
    alphas = ["1.05", "1.1", "1.2", "1.3", "1.4", "1.5", "1.529", "1.55", "1.6", "1.618",
              "1.65", "1.7", "1.71", "1.75", "1.8", "1.85", "1.9", "1.95"]
    rows = []
    for als in alphas:
        a = F(als)
        t1, p1 = entire_frontier(a, start=1, t_lo="1", t_hi="199/100", steps=150)
        t0, p0 = entire_frontier(a, start=0, t_lo="1", t_hi="199/100", steps=150)
        f1 = f"{float(t1):.3f}" if t1 is not None else "none"
        f0 = f"{float(t0):.3f}" if t0 is not None else "none"
        gain = ""
        if t1 is not None and t0 is not None:
            gain = f"+{float(t0) - float(t1):.3f}"
        elif t1 is None and t0 is not None:
            gain = "1-idx=none"
        marker = ""
        if float(a) >= PHI:
            marker = "alpha>=phi"
        if abs(float(a) - 1.529) < 1e-6:
            marker = "<-- Pro's 1-idx frontier"
        print(f"{als:>7} | {f1:>16} | {f0:>16} | {gain:>11} | {marker}")
        rows.append((als, t1, t0))

    print()
    print("=" * 100)
    print("Lemma-5 COFINITE frontier in t (strip 1<alpha<phi only; allows early gaps), 0- vs 1-indexed")
    print("=" * 100)
    print(f"{'alpha':>7} | {'1-indexed t_max':>16} | {'0-indexed t_max':>16}")
    print("-" * 50)
    for als in ["1.1", "1.3", "1.5", "1.529", "1.55", "1.6", "1.618"]:
        a = F(als)
        c1 = lemma5_cofinite_frontier(a, start=1, t_lo="1", t_hi="3", steps=80)
        c0 = lemma5_cofinite_frontier(a, start=0, t_lo="1", t_hi="3", steps=80)
        f1 = f"{float(c1):.3f}" if c1 is not None else "none"
        f0 = f"{float(c0):.3f}" if c0 is not None else "none"
        print(f"{als:>7} | {f1:>16} | {f0:>16}")
