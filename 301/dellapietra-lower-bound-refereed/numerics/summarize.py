#!/usr/bin/env python3
"""Tables from the saved outputs in out/ (no recomputation). Exact integers; decimals via Fraction."""
import os
import re
from fractions import Fraction

NS = [10**5, 10**6, 10**7, 10**8, 10**9, 10**10, 10**11]


def dec(q, d=5):
    s = "-" if q < 0 else ""
    q = abs(q)
    n = q.numerator * 10**d // q.denominator
    return f"{s}{n // 10**d}.{n % 10**d:0{d}d}"


def simple_rows():
    print("== Step 3: simple construction (full top half, L-rough heads, delete conflicting heads) ==")
    print("N | L | rough heads | deleted | deleted frac | |A| | excess |A|/N-1/2 | relations")
    for N in NS:
        fn = f"out/simple_N{N}.txt"
        if not os.path.exists(fn) or os.path.getsize(fn) == 0:
            continue
        for line in open(fn):
            m = re.match(r"L=(\d+)\s+(\d+) (\d+) (\d+) (\d+) (-?\d+) \S+ \S+ ?(\d+)?", line)
            if not m:
                continue
            L, H, D, K, A, tw = map(int, m.groups()[:6])
            R = m.group(7)
            print(f"1e{len(str(N))-1} | {L} | {H} | {D} | {dec(Fraction(D, H))} | {A} | {dec(Fraction(tw, 2 * N))} | {R}")


ROW = re.compile(r"L=(\d+) Ah=(\S+) Kh=(\S+) At=(\S+) Kt=(\S+) \| (\d+) (\d+) \| (\d+) (\d+) (\d+) \| (\d+) (-?\d+)")


def regular_rows():
    data = {}
    for N in NS:
        fn = f"out/regular_N{N}.txt"
        if not os.path.exists(fn):
            continue
        for line in open(fn):
            m = ROW.match(line)
            if m:
                L, ah, kh, at, kt = m.group(1, 2, 3, 4, 5)
                T, loss, Hr, C, kept, A, tw = map(int, m.group(6, 7, 8, 9, 10, 11, 12))
                data[(N, int(L), ah, kh, at, kt)] = (T, loss, Hr, C, kept, A, tw)
    return data


def regular_tables(data):
    print()
    print("== Step 4: regularity construction ==")
    fams = [("1.5", "1.5"), ("2", "2"), ("1.0001", "1.16312")]
    picks = [("0", "inf"), ("1", "inf"), ("2", "inf"), ("inf", "2"), ("inf", "3"), ("1", "2"), ("2", "2"), ("2", "3"), ("3", "3"), ("3", "4"), ("inf", "4"), ("inf", "inf")]
    for L in [7, 13, 23]:
        for ah, at in fams:
            print(f"-- L={L}, A_h={ah}, A_t={at}.  cells: excess  [top loss/N, regular heads kept/N, conflicted share of regular heads]")
            print("K_h,K_t | " + " | ".join(f"1e{len(str(N))-1}" for N in NS if (N, L, ah, "inf", at, "inf") in data))
            for kh, kt in picks:
                cells = []
                for N in NS:
                    r = data.get((N, L, ah, kh, at, kt))
                    if not r:
                        continue
                    T, loss, Hr, C, kept, A, tw = r
                    cells.append(f"{dec(Fraction(tw, 2 * N))} [{dec(Fraction(loss, N), 4)}, {dec(Fraction(kept, N), 4)}, {dec(Fraction(C, Hr) if Hr else Fraction(0), 3)}]")
                print(f"{kh},{kt} | " + " | ".join(cells))
            # best finite (K_h,K_t) in the grid {0..4}^2, vs no regularity
            best = []
            for N in NS:
                if (N, L, ah, "inf", at, "inf") not in data:
                    continue
                cand = [(data[(N, L, ah, kh, at, kt)][6], kh, kt) for kh in "01234" for kt in "01234"]
                tw, kh, kt = max(cand)
                tw0 = data[(N, L, ah, "inf", at, "inf")][6]
                best.append(f"1e{len(str(N))-1}: best finite (K_h,K_t)=({kh},{kt}) excess {dec(Fraction(tw, 2 * N))} vs no-regularity {dec(Fraction(tw0, 2 * N))}")
            print("   " + "\n   ".join(best))


if __name__ == "__main__":
    simple_rows()
    regular_tables(regular_rows())


def beats_simple(data):
    print()
    print("== Does ANY regularity row (all 16 (A_h,A_t) pairs, K_h,K_t in {0,1,2,3,4,inf}) beat no-regularity? ==")
    keys = sorted({(N, L) for (N, L, *_rest) in data})
    for N, L in keys:
        base = data[(N, L, "2", "inf", "2", "inf")][6]
        rows = [(v[6], k) for k, v in data.items() if k[0] == N and k[1] == L and not (k[3] == "inf" and k[5] == "inf")]
        tw, k = max(rows)
        print(f"N=1e{len(str(N))-1} L={L}: best regularity row {k[2:]} 2|A|-N={tw} vs no-regularity {base}: "
              f"{'BEATS' if tw > base else 'does not beat'} (difference {tw - base})")


beats_simple(regular_rows())
