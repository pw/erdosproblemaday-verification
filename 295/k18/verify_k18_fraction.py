#!/usr/bin/env python3
"""Exact Fraction second-lineage check for the Erdos #295 finite frontier.

This is the banked runs/erdos295_wave5r_verify.py algorithm with exactly one
algorithmic change: in the interior-denominator loop, a pruned child implies
all later children are pruned (tail(d+1,t) + 1/d is strictly decreasing in d),
so `continue` becomes `break`.  That is a theorem, not a heuristic, and it
does not change the set of visited states or any counter.

Everything else -- Python bignum Fractions, the naive linear scan for the
last two terms, exact tail comparisons with no floating point -- is the
banked lineage, deliberately different from the C++ implementation
(GMP arithmetic, double-interval filters, tau-aware divisor solver).

Parallelism: depth-2 task split + multiprocessing.  For a completed
unsatisfiable search, counter totals are independent of the split.  This
frozen copy is used for the k(18) >= 33 computation; the program remains
generic in its CLI arguments.
"""
import sys
from fractions import Fraction
from functools import lru_cache
from multiprocessing import Pool
from time import perf_counter


@lru_cache(maxsize=None)
def maximum_tail(lower, terms):
    return sum((Fraction(1, lower + i) for i in range(terms)), start=Fraction(0))


def search(minimum, terms, root=Fraction(1)):
    counters = {"states": 0, "two_states": 0, "two_cand": 0}
    witness = []

    def finish_with_two(remainder, lower):
        counters["two_states"] += 1
        a, b = remainder.numerator, remainder.denominator
        first_x = max(lower, b // a + 1)
        last_x = (2 * b) // a
        for x in range(first_x, last_x + 1):
            counters["two_cand"] += 1
            num, den = a * x - b, b * x
            if den % num == 0:
                y = den // num
                if y > x:
                    witness.extend([x, y])
                    return True
        return False

    def visit(remainder, lower, left):
        counters["states"] += 1
        if maximum_tail(lower, left) < remainder:
            return False
        if left == 1:
            if remainder.numerator == 1 and remainder.denominator >= lower:
                witness.append(remainder.denominator)
                return True
            return False
        if left == 2:
            return finish_with_two(remainder, lower)
        first_d = max(lower, remainder.denominator // remainder.numerator + 1)
        last_d = (left * remainder.denominator) // remainder.numerator
        for d in range(first_d, last_d + 1):
            new_remainder = remainder - Fraction(1, d)
            if maximum_tail(d + 1, left - 1) < new_remainder:
                break  # monotone: tail(d+1,t)+1/d strictly decreases in d
            if visit(new_remainder, d + 1, left - 1):
                witness.insert(0, d)
                return True
        return False

    found = visit(root, minimum, terms)
    return found, counters, witness


def depth2_tasks(minimum, terms):
    """Enumerate depth-2 surviving states exactly as visit() would."""
    tasks = []
    top = {"states": 0}
    R0 = Fraction(1)
    top["states"] += 1  # root
    assert not (maximum_tail(minimum, terms) < R0)
    fd = max(minimum, R0.denominator // R0.numerator + 1)
    ld = (terms * R0.denominator) // R0.numerator
    for d1 in range(fd, ld + 1):
        R1 = R0 - Fraction(1, d1)
        if maximum_tail(d1 + 1, terms - 1) < R1:
            break
        top["states"] += 1  # d1-state
        fd2 = max(d1 + 1, R1.denominator // R1.numerator + 1)
        ld2 = ((terms - 1) * R1.denominator) // R1.numerator
        for d2 in range(fd2, ld2 + 1):
            R2 = R1 - Fraction(1, d2)
            if maximum_tail(d2 + 1, terms - 2) < R2:
                break
            tasks.append((d1, d2, R2))
    return tasks, top["states"]


def run_task(args):
    d1, d2, R2, terms = args
    found, c, wit = search(d2 + 1, terms - 2, root=R2)
    if found:
        wit = [d1, d2] + wit
    return found, c, wit


def main():
    minimum, terms, procs = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    t0 = perf_counter()
    if procs == 1:
        found, c, wit = search(minimum, terms)
        total = c
    else:
        tasks, top_states = depth2_tasks(minimum, terms)
        # NOTE: depth2 tasks enumerated leftmost-first; leftmost are biggest.
        print(f"tasks={len(tasks)} top_states={top_states}", flush=True)
        total = {"states": top_states, "two_states": 0, "two_cand": 0}
        found, wit = False, []
        with Pool(procs) as pool:
            for f, c, w in pool.imap_unordered(
                    run_task, [(d1, d2, R2, terms) for d1, d2, R2 in tasks],
                    chunksize=1):
                for k in ("states", "two_states", "two_cand"):
                    total[k] += c[k]
                if f and not found:
                    found, wit = True, w
    el = perf_counter() - t0
    print(f"min={minimum} terms={terms} found={found}")
    print(f"recursive_states={total['states']} two_term_states={total['two_states']} "
          f"two_term_candidates={total['two_cand']}")
    print(f"seconds={el:.1f}")
    if found:
        s = sum((Fraction(1, d) for d in wit), start=Fraction(0))
        print(f"WITNESS: {wit}")
        print(f"WITNESS_CHECK sum==1: {s == 1} distinct_increasing: "
              f"{wit == sorted(set(wit))} count={len(wit)} min_ok={wit[0] >= minimum}")


if __name__ == "__main__":
    main()
