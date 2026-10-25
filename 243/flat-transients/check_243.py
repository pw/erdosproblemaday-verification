#!/usr/bin/env python3
"""Self-contained exact checker for the Problem 243 transient theorem.

No third-party packages and no local imports are used.  Every mathematical
check uses integers or fractions.Fraction; floating point is never used.
"""

from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from random import Random


def centered_residue(value: int, modulus: int) -> int:
    """The unique e with e == value (mod modulus) and -m/2 <= e < m/2."""
    assert modulus > 0
    residue = value % modulus
    return residue if 2 * residue < modulus else residue - modulus


def nearest_integer_up(frac: Fraction) -> int:
    """Nearest integer to a nonnegative fraction; half-integers round up."""
    assert frac >= 0
    return (2 * frac.numerator + frac.denominator) // (2 * frac.denominator)


@dataclass(frozen=True)
class FullState:
    c: int
    d: int
    e: int
    a: int


def full_state(c: int, d: int) -> FullState:
    assert c > 0 and d > 0
    e = centered_residue(d, c)
    a = (d - e) // c + 1
    assert a == nearest_integer_up(Fraction(d, c)) + 1
    assert Fraction(e, c) == Fraction(d, c) + 1 - a
    return FullState(c, d, e, a)


def direct_step(state: FullState) -> FullState:
    """One direct exact rational step, independent of modular orbit code."""
    c, d, e, a = state.c, state.d, state.e, state.a
    assert d == c * (a - 1) + e
    nxt = full_state(c - e, d * a)
    assert Fraction(nxt.c, nxt.d) == Fraction(c, d) - Fraction(1, a)
    return nxt


def direct_orbit(c: int, d: int, steps: int) -> list[FullState]:
    states = [full_state(c, d)]
    for _ in range(steps):
        states.append(direct_step(states[-1]))
    return states


@dataclass(frozen=True)
class CompactState:
    index: int
    c: int
    e: int
    a_mod_next_c: int

    @property
    def abs_epsilon(self) -> Fraction:
        return Fraction(abs(self.e), self.c)


def eval_a_mod(
    a0: int,
    cs: list[int],
    es: list[int],
    target_index: int,
    modulus: int,
) -> int:
    """Evaluate a_target modulo modulus via exact backwards moduli."""
    if modulus == 1:
        return 0
    mods = [0] * (target_index + 1)
    mods[target_index] = modulus
    for i in range(target_index - 1, -1, -1):
        mods[i] = cs[i + 1] * mods[i + 1]

    value = a0 % mods[0]
    for i in range(target_index):
        next_mod = mods[i + 1]
        divisor = cs[i + 1]
        numerator = es[i] * value * value - es[i + 1]
        assert numerator % divisor == 0
        q = numerator // divisor
        value = (value * (value - 1) + q + 1) % next_mod
    return value % modulus


def modular_orbit(c0: int, e0: int, a0: int, steps: int) -> list[CompactState]:
    """Exact orbit using e' = centered(e*a^2 mod (c-e))."""
    assert c0 > 0 and -c0 <= 2 * e0 < c0
    cs, es = [c0], [e0]
    out: list[CompactState] = []
    for n in range(steps + 1):
        c, e = cs[n], es[n]
        next_c = c - e
        a_mod = eval_a_mod(a0, cs, es, n, next_c)
        out.append(CompactState(n, c, e, a_mod))
        if n == steps:
            break
        es.append(centered_residue(e * a_mod * a_mod, next_c))
        cs.append(next_c)
    return out


def is_prime_trial(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def next_prime_trial(n: int) -> int:
    n = max(2, n)
    while not is_prime_trial(n):
        n += 1
    return n


@dataclass(frozen=True)
class Construction:
    length: int
    h: int
    p: int
    c0: int
    product: int
    multiplier: int
    d0: int
    a0: int


def construct(length: int, h: int, p: int | None = None) -> Construction:
    """L copies of the centered residue h, followed by absorbing residue 0."""
    assert length >= 1 and h != 0
    if p is None:
        p = next_prime_trial((length + 2) * abs(h) + 1)
    assert is_prime_trial(p) and p > (length + 2) * abs(h)

    c0 = p + length * h
    cs = [c0 - j * h for j in range(length)]
    assert cs[-1] - h == p and min(cs + [p]) > 2 * abs(h)
    product = 1
    for c in cs:
        product *= c

    factorial = 1
    for k in range(2, length + 1):
        factorial *= k
    coefficient = pow(h, length - 1, p) * (factorial % p) % p
    assert gcd(coefficient, p) == 1
    multiplier = (-pow(coefficient, -1, p)) % p + 4 * p
    assert multiplier >= 2
    d0 = product * multiplier + h
    assert d0 > 0 and gcd(c0, d0) == 1
    a0 = (d0 - h) // c0 + 1
    assert a0 >= 3
    return Construction(length, h, p, c0, product, multiplier, d0, a0)


def independent_trace_check(c0: int, d0: int, trace: list[CompactState]) -> None:
    """Replay d modulo c_0...c_N without using the e*a^2 recurrence."""
    modulus = 1
    for state in trace:
        modulus *= state.c
    d = d0 % modulus
    for i, state in enumerate(trace):
        assert state.index == i
        assert centered_residue(d, state.c) == state.e
        if i + 1 == len(trace):
            break
        assert trace[i + 1].c == state.c - state.e
        next_modulus = modulus // state.c
        assert (d - state.e) % state.c == 0
        a_mod = ((d - state.e) // state.c + 1) % next_modulus
        assert a_mod % trace[i + 1].c == state.a_mod_next_c
        d = d * a_mod % next_modulus
        modulus = next_modulus


def check_random_direct_vs_modular() -> None:
    rng = Random(243)
    for _ in range(1000):
        c = rng.randrange(1, 200)
        d = rng.randrange(1, 100_000)
        direct = direct_orbit(c, d, 8)
        compact = modular_orbit(c, direct[0].e, direct[0].a, 8)
        for full, mod in zip(direct, compact):
            assert (full.c, full.e) == (mod.c, mod.e)
            assert full.a % (full.c - full.e) == mod.a_mod_next_c


def check_transition_box() -> int:
    count = 0
    for c in range(1, 81):
        for e in range(-(c // 2), (c + 1) // 2):
            for a in range(2, 101):
                d = c * (a - 1) + e
                if d <= 0:
                    continue
                old, new = direct_orbit(c, d, 1)
                new_c = c - e
                expected_e = centered_residue(e * a * a, new_c)
                q = (e * a * a - expected_e) // new_c
                assert new.c == new_c and new.e == expected_e
                assert new.a == a * (a - 1) + q + 1
                assert -new.c <= 2 * new.e < new.c
                assert Fraction(new.c, new.d) == Fraction(old.c, old.d) - Fraction(1, a)
                count += 1
    return count


def check_construction_grid() -> int:
    count = 0
    for h in (-31, -11, -5, -2, -1, 1, 2, 5, 11, 31):
        for length in (1, 2, 3, 5, 10, 25, 50, 100):
            con = construct(length, h)
            trace = modular_orbit(con.c0, h, con.a0, length + 3)
            assert con.d0 == con.product * con.multiplier + h
            for j in range(length):
                assert (trace[j].c, trace[j].e) == (con.c0 - j * h, h)
                assert -trace[j].c <= 2 * h < trace[j].c
            assert all(state.c == con.p and state.e == 0 for state in trace[length:])
            independent_trace_check(con.c0, con.d0, trace)
            if length <= 10:
                direct = direct_orbit(con.c0, con.d0, length + 1)
                assert [(x.c, x.e) for x in direct] == [
                    (x.c, x.e) for x in trace[: length + 2]
                ]
                assert all(direct[j].a < direct[j + 1].a for j in range(len(direct) - 1))
                terminal = direct[length]
                assert terminal.e == 0
                assert direct[length + 1].a == terminal.a * terminal.a - terminal.a + 1
                prefix = sum((Fraction(1, s.a) for s in direct[:length]), Fraction(0))
                sylvester_tail = Fraction(1, terminal.a - 1)
                assert prefix + sylvester_tail == Fraction(con.c0, con.d0)
            count += 1
    return count


def check_eta_delta_grid() -> int:
    count = 0
    etas = (Fraction(1, 2), Fraction(1, 10), Fraction(1, 100), Fraction(1, 1000))
    deltas = (Fraction(1, 3), Fraction(1, 20), Fraction(1, 200))
    for eta in etas:
        for delta in deltas:
            for h in (-1, 1):
                for length in (1, 7, 31):
                    threshold = max(
                        (length + 2) * abs(h) + 1,
                        length * abs(h) + abs(h) * eta.denominator // eta.numerator + 2,
                        length * abs(h) + length * abs(h) * delta.denominator // delta.numerator + 2,
                    )
                    con = construct(length, h, next_prime_trial(threshold))
                    trace = modular_orbit(con.c0, h, con.a0, length)
                    prefix = trace[:length]
                    assert all(s.e == h and s.abs_epsilon < eta for s in prefix)
                    assert sum((s.abs_epsilon for s in prefix), Fraction(0)) < delta
                    assert trace[length].e == 0
                    count += 1
    return count


def check_large_certificate() -> str:
    length, h, p = 1000, -1, 1_001_003
    con = construct(length, h, p)
    trace = modular_orbit(con.c0, h, con.a0, length)
    assert all(s.e == h and s.abs_epsilon < Fraction(1, 1_000_000) for s in trace[:length])
    assert trace[length].e == 0
    independent_trace_check(con.c0, con.d0, trace)
    serial = "\n".join(f"{s.index},{s.c},{s.e},{s.a_mod_next_c}" for s in trace)
    return hashlib.sha256(serial.encode()).hexdigest()


def main() -> None:
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    check_random_direct_vs_modular()
    print("random_direct_vs_modular=PASS trials=1000 steps=8")
    print(f"finite_transition_box=PASS states={check_transition_box()}")
    print(f"construction_grid=PASS cases={check_construction_grid()}")
    print(f"eta_delta_grid=PASS cases={check_eta_delta_grid()}")
    digest = check_large_certificate()
    print(
        "large_certificate: L=1000 h=-1 p=1001003 c0=1000003 "
        f"digits(P)=6001 trace_sha256={digest}"
    )
    print("ALL EXACT CHECKS PASSED")


if __name__ == "__main__":
    main()
