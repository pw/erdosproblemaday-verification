#!/usr/bin/env python3
"""Trend of the simple construction from saved out/simple_N*.txt: deleted fraction of heads vs N.

Deleted fractions are exact rationals from the saved counts; the slope against log log N uses
floats (descriptive only, decides nothing).  Also: deleted share by Omega(a) for L=7, to show
where the creep comes from.
"""
import math
import os
import re
from fractions import Fraction

NS = [10**k for k in range(5, 12)]


def load(N):
    fn = f"out/simple_N{N}.txt"
    if not os.path.exists(fn) or os.path.getsize(fn) == 0:
        return None
    rows, om = {}, {}
    for line in open(fn):
        m = re.match(r"L=(\d+)\s+(\d+) (\d+) (\d+) (\d+) (-?\d+)", line)
        if m:
            L, H, D, K, A, tw = map(int, m.groups())
            rows[L] = (H, D, A, tw)
        m = re.match(r"Omega(\d+) (\d+) (\d+) (\d+)", line)
        if m:
            k, h, d, _ = map(int, m.groups())
            om[k] = (h, d)
    return rows, om


def main():
    data = {N: load(N) for N in NS}
    data = {N: v for N, v in data.items() if v}
    for L in [7, 11, 13, 17, 23]:
        print(f"L={L}: N, deleted fraction, excess, d(deleted frac)/d(loglog N) vs previous decade, "
              f"(1-deleted)*rough_heads/N")
        prev = None
        for N, (rows, _) in sorted(data.items()):
            H, D, A, tw = rows[L]
            f = Fraction(D, H)
            ll = math.log(math.log(N))
            slope = "" if prev is None else f"{(float(f) - prev[0]) / (ll - prev[1]):.4f}"
            print(f"  1e{len(str(N))-1}  {float(f):.5f}  {float(Fraction(tw, 2 * N)):.5f}  {slope}  "
                  f"{float(Fraction(H - D, N)):.5f}")
            prev = (float(f), ll)
    print("L=7 deleted share by Omega(a) (heads with that Omega; share deleted):")
    ks = sorted({k for _, (_, om) in data.items() for k in om})
    print("  Omega | " + " | ".join(f"1e{len(str(N))-1}" for N in sorted(data)))
    for k in ks:
        cells = []
        for N in sorted(data):
            h, d = data[N][1].get(k, (0, 0))
            cells.append(f"{h}:{float(Fraction(d, h)) if h else 0:.3f}")
        print(f"  {k} | " + " | ".join(cells))
    print("L=7 mean Omega of heads:", ", ".join(
        f"1e{len(str(N))-1}: {float(Fraction(sum(k * h for k, (h, d) in om.items()), sum(h for h, d in om.values()))):.3f}"
        for N, (_, om) in sorted(data.items())))


if __name__ == "__main__":
    main()
