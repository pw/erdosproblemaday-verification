#!/usr/bin/env python3
"""Definition-level audit of the new lower-bound witnesses for #425."""

from itertools import combinations


WITNESSES = {
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
EXPECTED = {52: 27, 53: 28, 56: 29, 59: 30, 61: 31}


def main() -> None:
    for n, values in WITNESSES.items():
        assert len(values) == EXPECTED[n]
        assert len(set(values)) == len(values)
        assert list(values) == sorted(values)
        assert 1 <= values[0] and values[-1] <= n

        owner = {}
        for a, b in combinations(values, 2):
            product = a * b
            assert product not in owner, (n, product, owner[product], (a, b))
            owner[product] = (a, b)
        expected_products = len(values) * (len(values) - 1) // 2
        assert len(owner) == expected_products
        print(
            f"n={n} size={len(values)} strict_pairs={expected_products} "
            f"distinct_products={len(owner)} min_product={min(owner)} "
            f"max_product={max(owner)} OK"
        )
    print("DEFINITION-LEVEL WITNESS AUDIT PASSED")


if __name__ == "__main__":
    main()
