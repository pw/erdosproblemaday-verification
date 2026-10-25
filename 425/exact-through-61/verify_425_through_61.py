#!/usr/bin/env python3
"""Exact standard-library certification of Erdős #425 through n=61.

This extends the existing certified frontier F(50)=26.  We independently
regenerate every obstruction through 61 in two ways, re-prove F(50)=26, and
run exact cover nonexistence searches only at the right endpoints of new
constant plateaus.  At every jump a displayed strict-pair witness, together
with F(n) <= F(n-1)+1, proves the upper and lower bounds at once.
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import hashlib
import sys
from time import perf_counter


BASE = Path(__file__).resolve().with_name("base_erdos425_wave9i_verify.py")
BASE_SHA256 = "a61198b50ed274ca06969b22ea7ba4d5522b74f9388130e28046b93af7d0f322"
spec = spec_from_file_location("base425", BASE)
assert spec is not None and spec.loader is not None
base = module_from_spec(spec)
sys.modules[spec.name] = base
spec.loader.exec_module(base)


EXPECTED = {
    50: 26,
    51: 26,
    52: 27,
    53: 28,
    54: 28,
    55: 28,
    56: 29,
    57: 29,
    58: 29,
    59: 30,
    60: 30,
    61: 31,
}

WITNESSES = {
    50: (1, 3, 7, 11, 16, 17, 19, 23, 25, 26, 27, 29, 31,
         34, 35, 36, 37, 39, 40, 41, 42, 43, 44, 45, 47, 49),
    52: (1, 7, 12, 13, 17, 18, 19, 23, 25, 27, 29, 31, 32, 33,
         35, 37, 38, 40, 41, 42, 43, 44, 45, 47, 49, 51, 52),
    53: (1, 7, 12, 13, 17, 18, 19, 23, 25, 27, 29, 31, 32, 33,
         35, 37, 38, 40, 41, 42, 43, 44, 45, 47, 49, 51, 52, 53),
    56: (1, 4, 9, 10, 17, 19, 21, 23, 25, 29, 31, 32, 35, 37, 38,
         39, 41, 43, 44, 45, 47, 48, 49, 51, 52, 53, 54, 55, 56),
    59: (1, 8, 11, 19, 20, 21, 23, 29, 31, 34, 35, 37, 39, 41, 43,
         44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59),
    61: (1, 4, 9, 10, 19, 21, 23, 25, 29, 31, 32, 34, 35, 37, 39,
         41, 43, 44, 45, 46, 47, 49, 51, 52, 53, 54, 55, 56, 57, 59, 61),
}

# To prove F(h)=k at a plateau's right endpoint h, reject a cover of
# H_h with h-k-1 vertices.  The lower witness comes from its first endpoint.
UPPER_DECISIONS = ((50, 26), (51, 26), (55, 28), (58, 29), (60, 30))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    wall = perf_counter()
    assert sha256(BASE) == BASE_SHA256

    by_products = base.edges_by_equal_product_pairs(61)
    by_quads = base.edges_by_four_subsets(61)
    assert by_products == by_quads
    print(f"edge generators agree: |E(H_61)|={len(by_products)}", flush=True)

    for n, witness in WITNESSES.items():
        assert len(witness) == EXPECTED[n]
        assert min(witness) >= 1 and max(witness) <= n
        assert len(set(witness)) == len(witness)
        assert base.has_distinct_strict_pair_products(witness)
        products = {
            a * b for i, a in enumerate(witness) for b in witness[i + 1:]
        }
        assert len(products) == len(witness) * (len(witness) - 1) // 2
        print(f"witness n={n} size={len(witness)} products={len(products)} OK",
              flush=True)

    for n, value in UPPER_DECISIONS:
        budget = n - value - 1
        search = base.CoverSearch(n, by_products)
        cover, stats = search.run(budget)
        assert cover is None
        print(
            f"upper n={n}: no cover of size <= {budget}; "
            f"nodes={stats.nodes} memo={stats.memo_states} "
            f"seconds={stats.seconds:.6f}",
            flush=True,
        )

    # Fill each plateau from its left witness and right-end upper decision.
    plateaus = ((50, 51, 26), (52, 52, 27), (53, 55, 28),
                (56, 58, 29), (59, 60, 30), (61, 61, 31))
    reconstructed = {}
    for lo, hi, value in plateaus:
        for n in range(lo, hi + 1):
            reconstructed[n] = value
    assert reconstructed == EXPECTED

    # Singleton jump plateaus use the elementary inequality
    # F(n) <= F(n-1)+1 and the checked witness at n.
    for n in (52, 53, 56, 59, 61):
        assert EXPECTED[n] == EXPECTED[n - 1] + 1
        assert len(WITNESSES[n]) == EXPECTED[n]

    print("table:", " ".join(f"F({n})={EXPECTED[n]}" for n in EXPECTED),
          flush=True)
    print(f"wall_seconds={perf_counter() - wall:.6f}", flush=True)
    print("VERIFIED", flush=True)


if __name__ == "__main__":
    main()
