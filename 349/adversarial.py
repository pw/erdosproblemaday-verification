#!/usr/bin/env python3
"""Adversarial reviewer harness for the entire-completeness theorem."""
from fractions import Fraction
import lab

def F(x): return Fraction(x)

# ---------------------------------------------------------------------------
# PART A: monotonicity, optimized (iterate powers, check bracket directly).
# Hunt (a,t,n), 1<a<2, t>=1, with f(n)>=0 but f(n+1)<f(n).
# ---------------------------------------------------------------------------
def monotonicity_hunt():
    viol = checked = 0
    for aden in (50, 200):
        for anum in range(aden + 1, 2 * aden):       # a in (1,2)
            a = Fraction(anum, aden)
            c = 2 - a
            am1 = a - 1
            for tden in (10, 50):
                for tnum in range(tden, 3 * tden):   # t in [1,3)
                    t = Fraction(tnum, tden)
                    p = a                            # a^(n+1), n=0 -> a^1
                    for n in range(0, 40):
                        checked += 1
                        term = t * p * c             # t*a^(n+1)*(2-a)
                        fn = term - Fraction(n) * am1 - t
                        if fn >= 0:
                            # bracket for f(n+1)-f(n) sign = term - 1
                            if term < 1:            # would make f decrease
                                viol += 1
                                if viol <= 5:
                                    print("MONO VIOLATION", float(a), float(t), n,
                                          "term=", float(term))
                        p *= a
    print(f"[A] monotonicity: checked={checked} violations={viol}")
    return viol

# ---------------------------------------------------------------------------
# PART B: direct induction-step check on ACTUAL sequence values.
# For a certified point, verify s_{n+1} <= C_n + 1 for n = M..M+K using the
# real floor sequence (independent of the f(n) analytic bound).
# ---------------------------------------------------------------------------
def direct_induction_check(t, a, M, K=200):
    terms = lab.floors(t, a, n_terms=M + K + 2, start=0)
    C = sum(terms[:M + 1])          # C_M = sum_{k<=M} s_k
    worst = None                    # most-negative slack (s_{n+1} - (C_n+1))
    for n in range(M, M + K + 1):
        s_next = terms[n + 1]
        slack = (C + 1) - s_next    # need >= 0
        if worst is None or slack < worst:
            worst = slack
        if slack < 0:
            return {"ok": False, "at_n": n, "C_n": C, "s_next": s_next, "slack": slack}
        C += s_next
    return {"ok": True, "min_slack": worst}

# ---------------------------------------------------------------------------
# PART C: full counterexample sweep.
# ---------------------------------------------------------------------------
def sweep(alphas, ts, N, do_gap=True, verbose=True):
    proven_pts = []
    fails = []
    for als in alphas:
        a = F(als)
        for tts in ts:
            t = F(tts)
            c = lab.entire_cert_0indexed(t, a)
            if not c["proven"]:
                continue
            proven_pts.append((tts, als, c["M"]))
            # (i) direct induction check on real values
            d = direct_induction_check(t, a, c["M"])
            if not d["ok"]:
                fails.append(("INDUCTION", tts, als, d))
                if verbose:
                    print(f"!!! INDUCTION FAIL t={tts} a={als} n={d['at_n']} "
                          f"C_n={d['C_n']} s_next={d['s_next']} slack={d['slack']}")
            # (ii) empirical gap to large N
            if do_gap:
                g = lab.gap_to_N(t, a, N=N, start=0)
                if g["max_gap"] != 0:
                    fails.append(("GAP", tts, als, g))
                    if verbose:
                        print(f"!!! GAP t={tts} a={als} N={N} max_gap={g['max_gap']} "
                              f"first@{g['first_max_gap_at']} tail_from={g['covered_tail_from']}")
    if verbose:
        print(f"[C] sweep: {len(proven_pts)} certified points, {len(fails)} failures (N={N})")
    return proven_pts, fails

if __name__ == "__main__":
    print("=" * 70)
    print("PART A: monotonicity hunt")
    print("=" * 70)
    monotonicity_hunt()

    print()
    print("=" * 70)
    print("PART B+C: certified-point sweep, direct induction + gap_to_N")
    print("=" * 70)
    # danger zone alpha in [1.85,1.99] plus a broad spread; t in [1,2)
    alphas = ["1.01","1.05","1.1","1.2","1.3","1.4","1.5","1.55","1.6","1.618",
              "1.65","1.7","1.75","1.8","1.82","1.84","1.85","1.86","1.87","1.88",
              "1.9","1.92","1.95","1.97","1.99"]
    ts = ["1","21/20","11/10","23/20","6/5","5/4","13/10","27/20","7/5","3/2",
          "8/5","17/10","9/5","19/10","39/20","99/50"]
    pts, fails = sweep(alphas, ts, N=300000)
    print("\ncertified points found:", len(pts))
    for tts, als, M in pts:
        print(f"   t={tts:>7} a={als:>6} M={M}")
    print("\nTOTAL FAILURES:", len(fails))
