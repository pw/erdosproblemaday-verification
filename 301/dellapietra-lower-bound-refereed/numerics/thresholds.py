#!/usr/bin/env python3
"""Integer thresholds for (L,A,K)-regularity, certified.

n is (L,A,K)-regular iff for every x >= L:
    Omega_L(n,x) <= A*log(log x / log L) + K.
With q_1 <= q_2 <= ... the prime factors of n that are >= L (with multiplicity),
this is equivalent to: for every j,  j - K <= floor(A*log(log q_j/log L)) =: m*(q_j).
And m*(q) = max{m >= 0 : q >= L^(exp(m/A))} = #{m >= 1 : q >= ceil(L^(exp(m/A)))}.

So membership needs only the integers thr(L,A,m) = ceil(L^(exp(m/A))).
We compute them twice (stdlib decimal at 110 digits, mpmath at 130 digits),
require the two to agree, and require the real value to sit at least 1e-40
(relative) away from the nearest integer, so the ceiling is certified.

Output: one line per threshold "L A_index m thr" (A_index into A_LIST), up to thr > 10^13.
"""
from decimal import Decimal, getcontext
from fractions import Fraction
import sys

import mpmath

A_LIST = [Fraction(10001, 10000), Fraction(14539, 12500), Fraction(3, 2), Fraction(2, 1)]
L_LIST = [7, 11, 13, 17, 19, 23]
CAP = 10**13


def thr_decimal(L, A, m):
    getcontext().prec = 110
    e = (Decimal(m * A.denominator) / Decimal(A.numerator)).exp()
    v = (Decimal(L).ln() * e).exp()
    return v


def thr_mpmath(L, A, m):
    mpmath.mp.dps = 130
    e = mpmath.exp(mpmath.mpf(m * A.denominator) / A.numerator)
    return mpmath.power(L, e)


def main():
    out = []
    for L in L_LIST:
        for ai, A in enumerate(A_LIST):
            m = 1
            while True:
                vd = thr_decimal(L, A, m)
                vm = thr_mpmath(L, A, m)
                cd = int(vd.to_integral_value(rounding="ROUND_CEILING"))
                cm = int(mpmath.ceil(vm))
                if cd != cm:
                    print(f"DISAGREE L={L} A={A} m={m}: {cd} {cm}", file=sys.stderr)
                    return 1
                # distance from the nearest integer, relative
                getcontext().prec = 110
                frac = vd - vd.to_integral_value(rounding="ROUND_FLOOR")
                dist = min(frac, 1 - frac)
                if dist <= vd * Decimal("1e-40"):
                    print(f"TOO CLOSE TO INTEGER L={L} A={A} m={m}", file=sys.stderr)
                    return 1
                out.append((L, ai, m, cd))
                if cd > CAP:
                    break
                m += 1
    print("# L A_index m ceil(L^exp(m/A));  A_LIST = " + ", ".join(f"{a.numerator}/{a.denominator}" for a in A_LIST))
    for row in out:
        print(*row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
