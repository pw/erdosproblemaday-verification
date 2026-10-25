#!/usr/bin/env python3
"""Check the printed marginal totals in Burrell dissertation Table 3-3."""

row_totals = [
    1, 9_121, 780_707, 8_055_007, 745_221_348,
    48_006_401_770, 726_896_356, 2_965, 13, 0,
]
column_totals = [
    2, 48_803_495_722, 680_273_368, 3_453_439, 132_495,
    11_567, 642, 49, 5, 1,
]
printed_grand_total = 49_487_367_289

print("sum of printed row totals:", sum(row_totals))
print("printed grand total:", printed_grand_total)
print("sum of printed column totals:", sum(column_totals))
assert sum(row_totals) == printed_grand_total - 1
assert sum(column_totals) == printed_grand_total + 1

# Exponent-p class 1 means elementary abelian. At order 2^10 there is one
# such group, of Frattini rank 10. Correcting that blank/zero row and the
# printed class-1 column total reconciles both margins with the theorem.
row_totals[9] = 1
column_totals[0] = 1
assert sum(row_totals) == sum(column_totals) == printed_grand_total
print("reconciled after rank-10/class-1 cell=1 and class-1 total=1")
