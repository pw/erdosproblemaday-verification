#!/usr/bin/env python3
"""Cold audit of A382397(66), using pair sums rather than differences."""

from itertools import combinations
from math import comb

N = 66
CPP_WITNESSES = (
    (21, 25, 31, 40, 43, 60),
    (15, 22, 34, 37, 43, 54),
    (16, 23, 35, 38, 44, 55),
    (12, 23, 29, 32, 44, 51),
    (13, 24, 30, 33, 45, 52),
    (7, 24, 27, 36, 42, 46),
)


def pair_sums(a):
    return [a[i] + a[j] for i in range(len(a)) for j in range(i, len(a))]


def is_sidon_by_sums(a):
    sums = pair_sums(a)
    return len(sums) == len(set(sums))


def insertion_is_sidon(a, x):
    return is_sidon_by_sums(tuple(sorted(a + (x,))))


def is_maximal_by_trial(a, n):
    members = set(a)
    return all(not insertion_is_sidon(a, x) for x in range(1, n + 1) if x not in members)


def sum_collision_blocked_set(a):
    sums = set(pair_sums(a))
    blocked = set(a)
    for s in sums:
        for mark in a:
            blocked.add(s - mark)
        if s % 2 == 0:
            blocked.add(s // 2)
    return blocked


def run_containing_hull(a, blocked):
    lo, hi = a[0], a[-1]
    if any(x not in blocked for x in range(lo, hi + 1)):
        return None
    while lo - 1 in blocked:
        lo -= 1
    while hi + 1 in blocked:
        hi += 1
    return lo, hi


def collision_certificate(a, x):
    old = {}
    for i in range(len(a)):
        for j in range(i, len(a)):
            old.setdefault(a[i] + a[j], (a[i], a[j]))
    for mark in a:
        if x + mark in old:
            b, c = old[x + mark]
            return f"{x}+{mark}={b}+{c}"
    if 2 * x in old:
        b, c = old[2 * x]
        return f"{x}+{x}={b}+{c}"
    raise AssertionError((a, x))


def audit_lower_bound():
    all_stats = []
    total_placements = 0
    for k in range(1, 6):
        raw = 0
        sidon = 0
        hull_covered = 0
        placements = 0
        best_run = 0
        best_marks = None
        best_interval = None
        for tail in combinations(range(1, N), k - 1):
            raw += 1
            ruler = (0,) + tail
            if not is_sidon_by_sums(ruler):
                continue
            sidon += 1
            blocked = sum_collision_blocked_set(ruler)
            run = run_containing_hull(ruler, blocked)
            if run is None:
                continue
            hull_covered += 1
            lo, hi = run
            length = hi - lo + 1
            if length > best_run:
                best_run = length
                best_marks = ruler
                best_interval = run
            for shift in range(N - ruler[-1]):
                domain = range(-shift, N - shift)
                if all(x in blocked for x in domain):
                    placements += 1
        assert raw == comb(N - 1, k - 1)
        total_placements += placements
        row = (k, raw, sidon, hull_covered, placements, best_run, best_marks, best_interval)
        all_stats.append(row)
        print(
            f"k={k} raw={raw} sidon_by_sums={sidon} "
            f"hull_covered={hull_covered} placements_N={placements} "
            f"best_run={best_run} best_marks={best_marks} best_interval={best_interval}"
        )
    assert total_placements == 0
    return all_stats


def audit_witnesses():
    seen = set()
    for witness in CPP_WITNESSES:
        assert witness not in seen
        seen.add(witness)
        assert len(witness) == 6
        assert len(set(witness)) == 6
        assert min(witness) >= 1 and max(witness) <= N
        assert is_sidon_by_sums(witness)
        assert is_maximal_by_trial(witness, N)
        certificates = [
            collision_certificate(witness, x)
            for x in range(1, N + 1)
            if x not in witness
        ]
        assert len(certificates) == N - 6
        print(f"witness={witness} direct_trial_maximal=YES")
    first = CPP_WITNESSES[0]
    print("first_witness_collision_certificate:")
    for x in range(1, N + 1):
        if x not in first:
            print(f"  x={x}: {collision_certificate(first, x)}")


if __name__ == "__main__":
    print("Independent sum-based audit for A382397(66)")
    audit_lower_bound()
    audit_witnesses()
    print("CONCLUSION a(66)=6")
