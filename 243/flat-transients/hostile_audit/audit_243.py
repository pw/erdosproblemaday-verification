#!/usr/bin/env python3
"""Independent hostile audit for the proposed Problem 243 partial result.

This file deliberately imports nothing from /tmp/erdos243_attack.  It uses
only exact integers/Fractions and replays the constructed rational directly
or modulo a product of *future* numerators.  In particular, the long replay
does not use the claimed recurrence e' = centered(e*a^2, c-e).
"""

from __future__ import annotations

import hashlib
import math
import sys
from fractions import Fraction
from itertools import product
from math import gcd
from random import Random


def centered(value: int, modulus: int) -> int:
    """Representative in [-modulus/2, modulus/2), including the lower tie."""
    assert modulus > 0
    r = value % modulus
    if 2 * r >= modulus:
        r -= modulus
    assert -modulus <= 2 * r < modulus
    return r


def decode(c: int, d: int) -> tuple[int, int]:
    """Return the centered gap numerator e and pseudo-greedy denominator a."""
    assert c > 0 and d > 0
    e = centered(d, c)
    a = (d - e) // c + 1
    assert d == c * (a - 1) + e
    assert a >= 1
    return e, a


def direct_step(c: int, d: int) -> tuple[int, int, int, int]:
    e, a = decode(c, d)
    c2, d2 = c - e, d * a
    assert c2 > 0 and d2 > 0
    assert Fraction(c2, d2) == Fraction(c, d) - Fraction(1, a)
    return c2, d2, e, a


def trial_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    q = 3
    while q * q <= n:
        if n % q == 0:
            return False
        q += 2
    return True


def prime_after(n: int) -> int:
    q = n + 1
    while not trial_prime(q):
        q += 1
    return q


def make_construction(L: int, h: int, p: int | None = None) -> dict[str, object]:
    assert L >= 1 and h != 0
    if p is None:
        p = prime_after((L + 2) * abs(h))
    assert trial_prime(p) and p > (L + 2) * abs(h)

    # These are c_1,...,c_L; the next numerator is p.
    cs = [p + (L - j) * h for j in range(L)]
    assert cs[-1] == p + h
    assert all(c > 2 * abs(h) for c in cs + [p])

    P = math.prod(cs)
    coefficient = (pow(h, L - 1, p) * (math.factorial(L) % p)) % p
    assert gcd(coefficient, p) == 1
    residue = (-pow(coefficient, -1, p)) % p
    assert 1 <= residue < p
    T = residue + 3 * p
    d = P * T + h
    c = cs[0]

    assert d > 0
    assert gcd(c, d) == gcd(c, h) == gcd(p, h) == 1
    assert d % p == 0
    e, a = decode(c, d)
    assert e == h
    assert a == math.prod(cs[1:]) * T + 1 >= 3
    return {"L": L, "h": h, "p": p, "cs": cs, "P": P, "T": T,
            "c": c, "d": d, "a": a}


def direct_construction_audit(L: int, h: int) -> str:
    """Materialize the true enormous denominators for a short construction."""
    con = make_construction(L, h)
    c, d = int(con["c"]), int(con["d"])
    initial = Fraction(c, d)
    terms: list[Fraction] = []
    previous_a = 0

    for j in range(L):
        c2, d2, e, a = direct_step(c, d)
        assert e == h
        assert c == con["cs"][j]
        assert a > previous_a
        previous_a = a
        terms.append(Fraction(1, a))
        c, d = c2, d2

    assert c == con["p"]
    terminal_e, terminal_a = decode(c, d)
    assert terminal_e == 0 and d % c == 0
    assert terminal_a > previous_a
    # The whole absorbing Sylvester tail, starting at terminal_a.
    tail = Fraction(1, terminal_a - 1)
    assert sum(terms, Fraction(0)) + tail == initial

    # Materialize three zero-gap steps and check strict increase and recurrence.
    a = terminal_a
    for _ in range(3):
        c2, d2, e, got_a = direct_step(c, d)
        assert e == 0 and got_a == a
        next_e, next_a = decode(c2, d2)
        assert next_e == 0
        assert next_a == a * a - a + 1 > a
        c, d, a = c2, d2, next_a

    return f"L={L},h={h},p={con['p']},c1={con['c']},T={con['T']}"


def future_product_replay(L: int, h: int, p: int | None = None) -> tuple[str, str]:
    """Long exact replay without the e*a^2 recurrence or huge d_n.

    If D is known modulo c_n*c_{n+1}*..., division of D-e_n by c_n
    determines a_n modulo the product of all future c's.  This gives a direct
    replay of d_{n+1}=d_n*a_n while keeping only a modular representative.
    Four terminal copies of p are included to audit absorption as well.
    """
    con = make_construction(L, h, p)
    cs = list(con["cs"]) + [int(con["p"])] * 4
    modulus = math.prod(cs)
    dmod = int(con["d"]) % modulus
    records: list[str] = []

    for j, c in enumerate(cs):
        expected = h if j < L else 0
        observed = centered(dmod, c)
        assert observed == expected
        records.append(f"{j}:{c}:{observed}:{dmod % c}")
        if j + 1 == len(cs):
            break
        assert modulus % c == 0
        future = modulus // c
        assert (dmod - observed) % c == 0
        amod = ((dmod - observed) // c + 1) % future
        # Changing the representative of dmod changes this quotient by a
        # multiple of `future`, so the update is representation-independent.
        dmod = (dmod * amod) % future
        modulus = future

    assert modulus == cs[-1]
    serial = "\n".join(records)
    return hashlib.sha256(serial.encode()).hexdigest(), (
        f"L={L},h={h},p={con['p']},c1={con['c']},digits(P)={len(str(con['P']))}"
    )


def audit_transition_identity() -> int:
    """Derive the next state directly on a box that includes all tie cases."""
    checked = 0
    for c in range(1, 71):
        possible_e = range(-(c // 2), (c + 1) // 2)
        for e in possible_e:
            for a in range(1, 81):
                d = c * (a - 1) + e
                if d <= 0:
                    continue
                c2, d2, got_e, got_a = direct_step(c, d)
                assert (got_e, got_a) == (e, a)
                e2, a2 = decode(c2, d2)
                assert e2 == centered(e * a * a, c - e)
                q, remainder = divmod(e * a * a - e2, c - e)
                assert remainder == 0
                assert a2 == a * (a - 1) + q + 1
                checked += 1
    return checked


def audit_random_unreduced_states() -> int:
    """Check that no hidden coprimality assumption enters the dynamics."""
    rng = Random(0x243A11D17)
    checked = 0
    for _ in range(5000):
        c = rng.randrange(1, 501)
        d = rng.randrange(1, 1_000_001)
        for _ in range(5):
            c2, d2, e, a = direct_step(c, d)
            e2, a2 = decode(c2, d2)
            assert e2 == centered(e * a * a, c2)
            assert a2 == a * (a - 1) + (e * a * a - e2) // c2 + 1
            c, d = c2, d2
            checked += 1
    return checked


def audit_eta_delta() -> int:
    cases = 0
    etas = [Fraction(1, 3), Fraction(2, 101), Fraction(1, 10_000)]
    deltas = [Fraction(1, 5), Fraction(3, 1000), Fraction(1, 100_000)]
    for L, eta, delta, sign in product((1, 9, 37), etas, deltas, (-1, 1)):
        # For h=sign, min(c_j) is at least p-L.  The +2 makes both
        # inequalities strict before moving to the next prime.
        bound = max(
            L + 2,
            L + eta.denominator // eta.numerator + 2,
            L + L * delta.denominator // delta.numerator + 2,
        )
        p = prime_after(bound)
        con = make_construction(L, sign, p)
        eps = [Fraction(1, c) for c in con["cs"]]
        assert all(x < eta for x in eps)
        assert sum(eps, Fraction(0)) < delta
        cases += 1
    return cases


def audit_c_to_infinity_logic() -> int:
    """Finite analogue of |e_n|>=1 => c_n>=1/|epsilon_n|."""
    checked = 0
    for c in range(1, 100):
        for e in range(-(c // 2), (c + 1) // 2):
            if e == 0:
                continue
            eps = abs(Fraction(e, c))
            assert c >= Fraction(1, eps)
            checked += 1
    return checked


def main() -> None:
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)

    print(f"transition_box=PASS states={audit_transition_identity()}")
    print(f"random_unreduced=PASS transitions={audit_random_unreduced_states()}")

    direct_records = []
    for h in (-13, -2, -1, 1, 2, 13):
        for L in (1, 2, 4, 7):
            direct_records.append(direct_construction_audit(L, h))
    direct_digest = hashlib.sha256("\n".join(direct_records).encode()).hexdigest()
    print(f"direct_both_signs=PASS cases={len(direct_records)} sha256={direct_digest}")

    long_records = []
    for L, h, p in ((512, -1, None), (512, 1, None), (1000, -1, 1_001_003)):
        digest, label = future_product_replay(L, h, p)
        long_records.append(f"{label},trace_sha256={digest}")
        print(f"future_product_replay=PASS {long_records[-1]}")

    print(f"eta_delta=PASS cases={audit_eta_delta()}")
    print(f"c_to_infinity_inequality=PASS states={audit_c_to_infinity_logic()}")
    print("HOSTILE AUDIT PASSED")


if __name__ == "__main__":
    main()
