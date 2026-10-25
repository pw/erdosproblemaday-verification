#!/usr/bin/env python3
"""Confirm the closed form t0(alpha) = min_{k>=0} (2^k+1)/alpha^k EXACTLY, and probe the
ambiguous (phi, 2.5) cofinite cell deeply for both conventions."""
from fractions import Fraction
import lab

PHI = lab.PHI


def F(x):
    return Fraction(x)


def t0_formula(alpha, kmax=14):
    return min(F(2 ** k + 1) / (alpha ** k) for k in range(0, kmax + 1))


print("=" * 80)
print("CONFIRM closed form t0(alpha) = min_{k>=0} (2^k+1)/alpha^k")
print("  for each alpha: tf = formula; require entire_cert(tf*(1-eps)) PROVEN")
print("  and greedy_entire(tf*(1+eps), 40 terms) FAILS (a gap at the boundary)")
print("=" * 80)
eps = Fraction(1, 100000)
mismatch = 0
tested = 0
a = F("101/100")
while a < F(2):
    tf = t0_formula(a)
    below = tf - eps
    above = tf + eps
    cb = lab.entire_cert_0indexed(below, a)
    ga = lab.greedy_entire(above, a, n_terms=40, start=0)
    tested += 1
    ok = cb["proven"] and (not ga["entire"])
    if not ok:
        mismatch += 1
        print(f"  MISMATCH alpha={float(a):.4f} tf={float(tf):.6f} "
              f"proven_below={cb['proven']} fails_above={not ga['entire']}")
    a += Fraction(1, 100)
# also a few irrational-ish rationals near the transitions and near phi
for als in ["1618/1000", "1666/1000", "1800/1000", "1889/1000", "1941/1000",
            "1970/1000", "1985/1000", "1999/1000", "11/10", "13/10", "149/100"]:
    a = F(als)
    tf = t0_formula(a)
    cb = lab.entire_cert_0indexed(tf - eps, a)
    ga = lab.greedy_entire(tf + eps, a, n_terms=40, start=0)
    tested += 1
    ok = cb["proven"] and (not ga["entire"])
    if not ok:
        mismatch += 1
        print(f"  MISMATCH alpha={als} tf={float(tf):.6f} proven_below={cb['proven']} "
              f"fails_above={not ga['entire']} (gap@{ga.get('gap_at')})")
    else:
        # show the binding k (argmin) for interest
        ks = [k for k in range(15) if F(2 ** k + 1) / (a ** k) == tf]
        print(f"  ok alpha={float(a):.4f} tf={float(tf):.6f} binding k={ks}")
print(f"\n  TESTED {tested}, MISMATCHES {mismatch}")

print()
print("=" * 80)
print("PROBE (alpha=phi-ish 1618/1000, t=5/2) deep, both conventions + lemma5")
print("=" * 80)
a = F("1618/1000")
t = F("5/2")
for start, name in [(0, "0-idx"), (1, "1-idx")]:
    counts = []
    for N in (100_000, 200_000, 400_000, 800_000, 1_600_000):
        terms = lab.floors(t, a, max_val=N, start=start)
        bits = lab.subsetsum_bits(terms, N)
        miss = N - bin(bits >> 1).count("1")
        counts.append((N, miss))
    stab = "STABLE->cofinite?" if counts[-1][1] == counts[-2][1] == counts[-3][1] else "GROWING->incomplete"
    print(f"  {name}: missing@N = {counts}  => {stab}")
    c = lab.lemma5_cert(t, a, max_r=40, start=start)
    if c and c.get("interval_len") is not None:
        print(f"       lemma5: CERTIFIED cofinite at r={c['r']} (len {c['interval_len']} >= {c['s_next']})")
    elif c and c.get("status") == "horizon":
        print(f"       lemma5: horizon before trigger")
    else:
        print(f"       lemma5: no cert in max_r=40")
