#!/usr/bin/env python3
"""CORRECTED cofinite/entire re-measurement after the skeptic caught the 4M-horizon
false-negative and the too-low-N stabilization trap.

Fixes vs the old investigate.py:
  - cofinite_probe tracks the LARGEST unrepresented integer L (not just the count) and
    declares cofinite only when L is STABLE across doublings that exceed it (so a last gap
    at 2.87M can't hide behind a 1.6M probe ceiling).
  - lemma5 uses a RAISED horizon (default 200M) so it doesn't bail at r=27.
  - entire_intervals maps the entire-complete t-set (greedy no-gap) so we can see the
    disconnectivity / t=1-exclusion the skeptic reported.
"""
from fractions import Fraction
import lab

PHI = lab.PHI


def F(x):
    return Fraction(x)


def lemma5(t, alpha, start, maxr=70, horizon=200_000_000):
    terms = lab.floors(t, alpha, n_terms=maxr + 2, start=start)
    bits = 1
    for r in range(maxr + 1):
        cap = sum(terms[:r + 1])
        if cap > horizon:
            return {"status": "horizon", "cap": cap, "r": r}
        mask = (1 << (cap + 1)) - 1
        bits &= mask
        s = terms[r]
        if 0 < s <= cap:
            bits |= (bits << s)
            bits &= mask
        L = lab.longest_run_length(bits)
        if L >= terms[r + 1]:
            _, X = lab.longest_run(bits, cap)
            return {"status": "certified", "r": r, "X": X, "L": L, "snext": terms[r + 1]}
    return {"status": "no_cert_in_maxr"}


def cofinite_probe(t, alpha, start, N0=262144, cap_max=67108864):
    """Robust cofinite test. Returns verdict + (last_gap, gaps) when stable."""
    N = N0
    prev_L = -1
    stable = 0
    last = None
    while N <= cap_max:
        terms = lab.floors(t, alpha, max_val=N, start=start)
        bits = lab.subsetsum_bits(terms, N)
        zeros = (~bits) & ((1 << (N + 1)) - 1) & ~1  # missing positives <= N
        L = (zeros.bit_length() - 1) if zeros else 0
        count = N - bin(bits >> 1).count("1")
        last = {"N": N, "L": L, "count": count}
        if L == 0 and prev_L == 0:
            return {"verdict": "ENTIRE-emp (no gap to %d)" % N, **last}
        # stable once L stops moving AND current N has passed well beyond L
        if L == prev_L and L != 0 and L < N // 2:
            stable += 1
        else:
            stable = 0
        if stable >= 2:
            return {"verdict": "COFINITE-emp", "last_gap": L, "gaps": count, **last}
        prev_L = L
        N *= 2
    return {"verdict": "STILL-GROWING-at-%d (likely incomplete; unproven)" % cap_max, **(last or {})}


def entire_intervals(alpha, t_lo=F(1), t_hi=None, step=4000, nterms=70):
    """Map t-intervals where the 0-indexed sequence is ENTIRE-complete (greedy no-gap)."""
    if t_hi is None:
        # upper bound = T(alpha)
        t_hi = min(F(2 ** k + 1) / (alpha ** k) for k in range(0, 25))
    intervals = []
    in_run = False
    run_lo = None
    prev_t = None
    for i in range(step + 1):
        t = t_lo + (t_hi - t_lo) * Fraction(i, step)
        g = lab.greedy_entire(t, alpha, n_terms=nterms, start=0)
        ok = g["entire"]
        if ok and not in_run:
            in_run = True
            run_lo = t
        elif not ok and in_run:
            in_run = False
            intervals.append((float(run_lo), float(prev_t)))
        prev_t = t
    if in_run:
        intervals.append((float(run_lo), float(t_hi)))
    return intervals


if __name__ == "__main__":
    print("=" * 92)
    print("COFINITE re-probe (robust) + lemma5 (raised horizon) on the key points")
    print("=" * 92)
    pts = [
        ("1618/1000", "5/2", 0, "cross-check skeptic 0-idx"),
        ("1618/1000", "5/2", 1, "cross-check skeptic 1-idx (was my false neg)"),
        ("9/5", "1", 0, "marquee 0-idx (1,1.8) entire?"),
        ("9/5", "1", 1, "marquee 1-idx (1,1.8) -- Prop3 says incomplete"),
        ("19/10", "1", 0, "0-idx (1,1.9) expect incomplete (gap 12)"),
        ("17/10", "2", 0, "0-idx (1.7,2) OPEN"),
        ("18/10", "2", 0, "0-idx (1.8,2) OPEN"),
        ("19/10", "2", 0, "0-idx (1.9,2) OPEN"),
        ("18/10", "2", 1, "1-idx (1.8,2) Prop3 incomplete x-check"),
    ]
    for als, tv, st, note in pts:
        a, t = F(als), F(tv)
        cp = cofinite_probe(t, a, st)
        l5 = lemma5(t, a, st) if float(a) < float(PHI) else {"status": "n/a (alpha>=phi)"}
        print(f"  a={als:>9} t={tv:>3} start={st} [{note}]")
        print(f"      cofinite_probe: {cp}")
        print(f"      lemma5:         {l5}")

    print()
    print("=" * 92)
    print("ENTIRE-complete t-intervals (greedy no-gap) -- confirm disconnectivity / t=1 exclusion")
    print("=" * 92)
    for als in ["18/10", "187/100", "19/10", "195/100", "199/100"]:
        a = F(als)
        ivs = entire_intervals(a, step=6000)
        t1ok = lab.greedy_entire(F(1), a, n_terms=70, start=0)["entire"]
        print(f"  alpha={als:>7} (={float(a):.4f}) t=1 entire={t1ok}  intervals={ivs}")
