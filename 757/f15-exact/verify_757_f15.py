#!/usr/bin/env python3
"""
Standalone exact verifier for the wave-7k report on Erdős problem #757.

No external packages, SAT solver, floating point, or network access are used.

What is verified from scratch:
  * the (4,5)-property and exact largest-Sidon-subset size of every
    construction used for 1 <= n <= 15;
  * the new 12-point block and its complete 3-term-AP hypergraph;
  * all arithmetic in the finite Henning--Yeo lower-bound corollary;
  * an independent exhaustive seven-point obstruction calculation.

What is deliberately NOT reproved here:
  * Gyárfás--Lehel's F_7-freeness theorem for AP hypergraphs of (4,5)-sets;
  * Henning--Yeo's theorem 17*tau <= 5*n + 3*m.
Those named theorems are explicit hypotheses of the lower-bound arithmetic.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product


A12 = (
    0, 97, 161, 194, 227, 322, 374, 454, 521, 534, 547, 720
)

A14 = (
    0, 136, 200, 243, 246, 249, 272,
    286, 298, 323, 400, 528, 596, 1056,
)

A15 = A14 + (1057,)

EXPECTED_F = {
    1: 1,
    2: 2,
    3: 2,
    4: 3,
    5: 4,
    6: 4,
    7: 5,
    8: 5,
    9: 6,
    10: 6,
    11: 7,
    12: 7,
    13: 8,
    14: 8,
    15: 9,
}

# One explicit extremal construction for each order.  Most are induced
# subsets of A12; orders 10, 13, and 14 use the Ma--Tang A14 block.
CONSTRUCTIONS = {
    1: (0,),
    2: (0, 97),
    3: (0, 97, 194),
    4: (0, 97, 161, 194),
    5: (0, 97, 161, 194, 227),
    6: (0, 97, 161, 194, 227, 322),
    7: (0, 97, 161, 194, 227, 322, 374),
    8: (0, 97, 161, 194, 227, 322, 454, 547),
    9: (0, 97, 161, 194, 227, 322, 374, 454, 534),
    10: (200, 243, 246, 249, 272, 286, 298, 323, 400, 528),
    11: (0, 97, 161, 194, 227, 322, 374, 454, 521, 534, 547),
    12: A12,
    13: (0, 136, 200, 243, 246, 249, 272,
         286, 298, 323, 400, 528, 596),
    14: A14,
    15: A15,
}

EXPECTED_A12_AP_EDGES = (
    (0, 1, 3),
    (0, 2, 5),
    (0, 4, 7),
    (1, 5, 10),
    (2, 3, 4),
    (4, 6, 8),
    (5, 8, 11),
    (6, 7, 9),
    (6, 10, 11),
    (8, 9, 10),
)


def pairwise(iterable):
    return combinations(iterable, 2)


def is_sidon(values):
    """Standard Sidon condition: all x+y for x <= y are distinct."""
    values = tuple(sorted(values))
    seen = {}
    for i, x in enumerate(values):
        for y in values[i:]:
            total = x + y
            if total in seen:
                return False
            seen[total] = (x, y)
    return True


def is_weak_sidon(values):
    """All sums of two distinct elements are distinct."""
    values = tuple(sorted(values))
    seen = {}
    for i, j in combinations(range(len(values)), 2):
        total = values[i] + values[j]
        if total in seen:
            return False
        seen[total] = (i, j)
    return True


def max_sidon(values):
    """Exhaustively compute h(A), returning (h, one witness)."""
    values = tuple(sorted(values))
    for size in range(len(values), -1, -1):
        for subset in combinations(values, size):
            if is_sidon(subset):
                return size, subset
    raise AssertionError("The empty set should have been Sidon")


def check_45(values):
    """
    Check every four-subset directly.
    Returns (ok, minimum number of distances, number of checked quadruples).
    """
    values = tuple(sorted(values))
    minimum = None
    count = 0
    for quad in combinations(values, 4):
        count += 1
        distances = {abs(x - y) for x, y in pairwise(quad)}
        minimum = (
            len(distances) if minimum is None
            else min(minimum, len(distances))
        )
        if len(distances) < 5:
            return False, len(distances), count
    return True, minimum, count


def ap_edges(values):
    """All index triples i<j<k with a_i+a_k=2*a_j."""
    values = tuple(values)
    return tuple(
        (i, j, k)
        for i, j, k in combinations(range(len(values)), 3)
        if values[i] + values[k] == 2 * values[j]
    )


def edge_family_is_linear(edges):
    return all(
        len(set(e1).intersection(e2)) <= 1
        for e1, e2 in combinations(edges, 2)
    )


def alpha_at_most_4_on_7(edges):
    """For a 3-graph on [7], test whether every five-set contains an edge."""
    edge_sets = tuple(frozenset(e) for e in edges)
    return all(
        any(e.issubset(five) for e in edge_sets)
        for five in map(frozenset, combinations(range(7), 5))
    )


def matrix_rank(rows, width):
    """Exact row rank over Q."""
    mat = [[Fraction(x) for x in row] for row in rows]
    pivot_row = 0
    for col in range(width):
        pivot = next(
            (r for r in range(pivot_row, len(mat)) if mat[r][col] != 0),
            None,
        )
        if pivot is None:
            continue
        mat[pivot_row], mat[pivot] = mat[pivot], mat[pivot_row]
        scale = mat[pivot_row][col]
        mat[pivot_row] = [x / scale for x in mat[pivot_row]]
        for r in range(len(mat)):
            if r == pivot_row or mat[r][col] == 0:
                continue
            scale = mat[r][col]
            mat[r] = [
                x - scale * y for x, y in zip(mat[r], mat[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def solve_unique(rows, rhs, width):
    """Solve a square full-rank rational system exactly; otherwise return None."""
    mat = [
        [Fraction(x) for x in row] + [Fraction(value)]
        for row, value in zip(rows, rhs)
    ]
    pivot_row = 0
    pivot_cols = []
    for col in range(width):
        pivot = next(
            (r for r in range(pivot_row, len(mat)) if mat[r][col] != 0),
            None,
        )
        if pivot is None:
            continue
        mat[pivot_row], mat[pivot] = mat[pivot], mat[pivot_row]
        scale = mat[pivot_row][col]
        mat[pivot_row] = [x / scale for x in mat[pivot_row]]
        for r in range(len(mat)):
            if r == pivot_row or mat[r][col] == 0:
                continue
            scale = mat[r][col]
            mat[r] = [
                x - scale * y for x, y in zip(mat[r], mat[pivot_row])
            ]
        pivot_cols.append(col)
        pivot_row += 1

    for row in mat:
        if all(x == 0 for x in row[:width]) and row[width] != 0:
            return None
    if len(pivot_cols) != width:
        return None

    solution = [Fraction(0) for _ in range(width)]
    for r, col in enumerate(pivot_cols):
        solution[col] = mat[r][width]
    return tuple(solution)


def first_weak_sidon_collision(values):
    seen = {}
    for i, j in combinations(range(len(values)), 2):
        total = values[i] + values[j]
        if total in seen:
            return seen[total], (i, j), total
        seen[total] = (i, j)
    return None


def ap_equation_row(edge, n=7):
    i, j, k = edge
    row = [0] * n
    row[i] = 1
    row[j] = -2
    row[k] = 1
    return row


def verify_constructions():
    print("Exact construction audit")
    print("n  claimed_h  computed_h  min_4pt_distances  witness")
    for n in range(1, 16):
        values = CONSTRUCTIONS[n]
        assert len(values) == n
        assert tuple(sorted(set(values))) == values
        ok, minimum, _ = check_45(values)
        assert ok
        computed, witness = max_sidon(values)
        assert computed == EXPECTED_F[n]
        minimum_text = "vacuous" if minimum is None else str(minimum)
        print(f"{n:2d} {EXPECTED_F[n]:10d} {computed:11d} "
              f"{minimum_text:>18s}  {witness}")

    ok12, minimum12, quads12 = check_45(A12)
    assert ok12 and minimum12 == 5 and quads12 == 495
    assert is_weak_sidon(A12)
    assert ap_edges(A12) == EXPECTED_A12_AP_EDGES
    assert edge_family_is_linear(ap_edges(A12))
    h12, witness12 = max_sidon(A12)
    assert h12 == 7
    assert witness12 == (0, 97, 161, 227, 374, 534, 547)
    print()
    print("A12 direct certificate:")
    print("  checked quadruples =", quads12)
    print("  minimum distinct distances =", minimum12)
    print("  AP edges =", ap_edges(A12))
    print("  h(A12) =", h12)
    print("  Sidon-7 witness =", witness12)

    ok14, minimum14, quads14 = check_45(A14)
    assert ok14 and minimum14 == 5 and quads14 == 1001
    h14, witness14 = max_sidon(A14)
    assert h14 == 8
    print()
    print("A14 independent recheck:")
    print("  checked quadruples =", quads14)
    print("  minimum distinct distances =", minimum14)
    print("  h(A14) =", h14)
    print("  Sidon-8 witness =", witness14)

    ok15, minimum15, quads15 = check_45(A15)
    assert ok15 and minimum15 == 5 and quads15 == 1365
    signed_hist15 = Counter(
        len({x - y for x in quad for y in quad})
        for quad in combinations(A15, 4)
    )
    assert signed_hist15 == {11: 144, 13: 1221}
    assert is_weak_sidon(A15)
    h15, witness15 = max_sidon(A15)
    assert h15 == 9
    assert all(1057 not in tuple(A15[i] for i in edge)
               for edge in ap_edges(A15))
    assert ap_edges(A15) == ap_edges(A14)
    assert edge_family_is_linear(ap_edges(A15))
    ten_subsets = tuple(combinations(A15, 10))
    assert len(ten_subsets) == 3003
    assert all(not is_sidon(subset) for subset in ten_subsets)
    # Audit all 2^15 subsets, rather than only stopping when max_sidon finds
    # its first maximum witness.
    sidon_counts15 = {
        size: sum(is_sidon(subset) for subset in combinations(A15, size))
        for size in range(16)
    }
    assert sidon_counts15 == {
        0: 1, 1: 15, 2: 105, 3: 443, 4: 1221,
        5: 2242, 6: 2696, 7: 2012, 8: 832, 9: 143,
        10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0,
    }
    print()
    print("A15 exact finite extension:")
    print("  checked quadruples =", quads15)
    print("  minimum distinct distances =", minimum15)
    print("  live |B-B| histogram =", dict(sorted(signed_hist15.items())))
    print("  h(A15) =", h15)
    print("  Sidon-9 witness =", witness15)
    print("  all 3003 ten-subsets are non-Sidon")
    print("  all 32768 subsets audited; Sidon counts =", sidon_counts15)
    print("  AP edge list is unchanged from A14")


def verify_finite_lower_bound_arithmetic():
    """
    Check the arithmetic consequence of the two named theorems:

      17*tau <= 5*n+3*m,  m <= n-2

    gives tau <= floor((8*n-6)/17) and hence
    h >= n-floor((8*n-6)/17), for n>=2.
    """
    print()
    print("Finite lower-bound arithmetic (named theorem treated as input)")
    print("n  floor((8n-6)/17)  HY_lower  final_lower  construction_h")
    for n in range(1, 16):
        if n == 1:
            tau_upper = 0
            hy_lower = 1
        else:
            tau_upper = (8 * n - 6) // 17
            hy_lower = n - tau_upper
            assert 17 * tau_upper <= 8 * n - 6
            assert 17 * (tau_upper + 1) > 8 * n - 6
        # The sole extra small-order argument is f(5)>=4.
        final_lower = 4 if n == 5 else hy_lower
        assert final_lower == EXPECTED_F[n]
        computed_h, _ = max_sidon(CONSTRUCTIONS[n])
        assert final_lower == computed_h
        print(f"{n:2d} {tau_upper:18d} {hy_lower:9d} "
              f"{final_lower:12d} {computed_h:15d}")

    # From scratch: a linear 3-graph on five vertices has at most two edges.
    triples5 = tuple(combinations(range(5), 3))
    max_linear_edges = 0
    for mask in range(1 << len(triples5)):
        edges = tuple(
            triples5[i] for i in range(len(triples5)) if (mask >> i) & 1
        )
        if edge_family_is_linear(edges):
            max_linear_edges = max(max_linear_edges, len(edges))
    assert max_linear_edges == 2
    print("Verified separately: max edges in a linear 3-graph on 5 vertices = 2")


def verify_seven_point_obstruction():
    """
    Exhaust all possible ordered AP hypergraphs for seven points under the
    two elementary necessary conditions:
      * at most one AP has each possible midpoint a_j (1<=j<=5);
      * the AP hypergraph is linear.

    If h<=4, every five vertices contain an AP.  Exact equation solving then
    shows that only four of the surviving patterns can occur in strict order,
    and every one forces a weak-Sidon collision.
    """
    n = 7
    choices_by_midpoint = [
        [None] + [
            (i, j, k)
            for i in range(j)
            for k in range(j + 1, n)
        ]
        for j in range(1, n - 1)
    ]

    total = 0
    linear_count = 0
    alpha_small_count = 0
    ordered = []

    for choice in product(*choices_by_midpoint):
        total += 1
        edges = tuple(edge for edge in choice if edge is not None)
        if not edge_family_is_linear(edges):
            continue
        linear_count += 1
        if not alpha_at_most_4_on_7(edges):
            continue
        alpha_small_count += 1

        rows = [ap_equation_row(edge, n) for edge in edges]
        assert len(edges) == 5
        assert matrix_rank(rows, n) == 5

        # Affine normalization a_0=0, a_6=1.
        row0 = [0] * n
        row0[0] = 1
        row6 = [0] * n
        row6[6] = 1
        normalized = solve_unique(
            rows + [row0, row6],
            [0] * len(rows) + [0, 1],
            n,
        )
        if normalized is None:
            continue
        if all(normalized[i] < normalized[i + 1] for i in range(n - 1)):
            collision = first_weak_sidon_collision(normalized)
            ordered.append((edges, normalized, collision))

    assert total == 29160
    assert linear_count == 2364
    assert alpha_small_count == 48
    assert len(ordered) == 4
    assert all(collision is not None for _, _, collision in ordered)

    expected_coordinates = {
        (
            Fraction(0), Fraction(1, 5), Fraction(3, 10),
            Fraction(2, 5), Fraction(1, 2), Fraction(3, 5), Fraction(1),
        ),
        (
            Fraction(0), Fraction(1, 4), Fraction(3, 8),
            Fraction(1, 2), Fraction(5, 8), Fraction(3, 4), Fraction(1),
        ),
        (
            Fraction(0), Fraction(3, 10), Fraction(2, 5),
            Fraction(1, 2), Fraction(3, 5), Fraction(7, 10), Fraction(1),
        ),
        (
            Fraction(0), Fraction(2, 5), Fraction(1, 2),
            Fraction(3, 5), Fraction(7, 10), Fraction(4, 5), Fraction(1),
        ),
    }
    assert {coordinates for _, coordinates, _ in ordered} == expected_coordinates

    print()
    print("Independent n=7 exhaustive obstruction")
    print("  midpoint-labelled candidates =", total)
    print("  linear candidates =", linear_count)
    print("  linear candidates with alpha<=4 =", alpha_small_count)
    print("  strictly ordered normalized solutions =", len(ordered))
    for edges, coordinates, collision in ordered:
        print("  edges:", edges)
        print("    coordinates:", coordinates)
        print("    forced weak-Sidon collision:", collision)
    print("  weak-Sidon survivors = 0")


def main():
    verify_constructions()
    verify_finite_lower_bound_arithmetic()
    verify_seven_point_obstruction()
    print()
    print("PASS: all construction, table, arithmetic, and n=7 checks succeeded")


if __name__ == "__main__":
    main()
