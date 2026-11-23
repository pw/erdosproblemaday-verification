#!/usr/bin/env python3
"""Second, independent implementation of the regularity construction (pure Python, small N).

Straight from the definitions: trial-division factorisation; Omega_L(n,x) evaluated at every
x in {primes >= L dividing n} (the only places the left side jumps); the inequality
    Omega_L(n,x) <= A log(log x/log L) + K
decided by integers via the certified thresholds thr(L,A,m) = ceil(L^exp(m/A)):
    Omega <= floor(A log(log x/log L)) + K,  floor(...) = #{m>=1: x >= thr(L,A,m)}.
Conflicts by the (b-a)(c-a) = a^2 route with membership in T (not the r,s route of regular.c).
usage: regular_xcheck.py N L A_index K_h A_index K_t
"""
import sys

A_NAMES = ["1.0001", "1.16312", "1.5", "2"]


def load_thr(path):
    thr = {}
    for line in open(path):
        if line.startswith("#"):
            continue
        L, ai, m, v = line.split()
        thr.setdefault((int(L), int(ai)), []).append(int(v))
    return thr


def factor(n):
    out, d = [], 2
    while d * d <= n:
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            out.append((d, e))
        d += 1
    if n > 1:
        out.append((n, 1))
    return out


def regular(n, L, thr, K):
    big = [(p, e) for p, e in factor(n) if p >= L]
    omega = 0
    for p, e in big:                      # ascending primes
        omega += e                        # Omega_L(n, x) at x = p
        floor_alog = sum(1 for t in thr if p >= t)
        if omega > floor_alog + K:
            return False
    return True


def divisors_of_square(a):
    ds = [1]
    for p, e in factor(a):
        ds = [d * p**j for d in ds for j in range(2 * e + 1)]
    return ds


def main():
    N, L, ah, Kh, at, Kt = map(int, sys.argv[1:7])
    thr = load_thr(sys.argv[7] if len(sys.argv) > 7 else "out/thresholds.txt")
    th_h, th_t = thr[(L, ah)], thr[(L, at)]
    M = (N + 1) // 2
    T = {b for b in range(M, N + 1) if regular(b, L, th_t, Kt)}
    H = [a for a in range(1, N + 1) if 3 * a > N and 2 * a < N
         and all(a % p for p in range(2, L)) and regular(a, L, th_h, Kh)]
    gamma = 0
    for a in H:
        for d in divisors_of_square(a):
            if d < a and a + d in T and a + a * a // d in T:
                gamma += 1
                break
    size = len(T) + len(H) - gamma
    print(f"N={N} L={L} Ah={A_NAMES[ah]} Kh={Kh} At={A_NAMES[at]} Kt={Kt}: |T|={len(T)} |H|={len(H)} "
          f"conflicted={gamma} kept={len(H) - gamma} |A|={size} 2|A|-N={2 * size - N}")


if __name__ == "__main__":
    main()
