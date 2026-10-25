#!/usr/bin/env python3
"""Finite audits for the Round 4 claims c_6 = c_7 = 2.

The uniform proof is in the article. This standard-library program is a
bug-finding check for its matching, gcd-product, and distinctness steps.
"""

from itertools import combinations
from math import gcd, prod


def matching(neighbors):
    """Return a matching saturating every left key, or None."""
    left = sorted(neighbors, key=lambda a: (len(neighbors[a]), a))

    def search(index, used, result):
        if index == len(left):
            return result.copy()
        a = left[index]
        for b in neighbors[a]:
            if b in used:
                continue
            used.add(b)
            result[a] = b
            answer = search(index + 1, used, result)
            if answer is not None:
                return answer
            del result[a]
            used.remove(b)
        return None

    return search(0, set(), {})


def full_neighbors(A, lower, upper):
    """All positive multiples of each modulus in an inclusive block."""
    graph = {}
    for a in A:
        first = ((lower + a - 1) // a) * a
        graph[a] = tuple(range(first, upper + 1, a))
    return graph


def bracketing_neighbors(A, t):
    """The consecutive-multiple edges around t + M + 1/2."""
    M = max(A)
    twice_center = 2 * (t + M) + 1
    graph = {}
    for a in A:
        lower = a * (twice_center // (2 * a))
        upper = lower + a
        assert t + 1 <= lower < twice_center / 2 < upper <= t + 2 * M
        graph[a] = (lower, upper)
    return graph


def minimal_deficient(A, graph):
    for size in range(1, len(A) + 1):
        for S in combinations(A, size):
            N = {b for a in S for b in graph[a]}
            if len(N) < size:
                return S, N
    return None


def repaired_cover(A, lower, upper):
    """Implement the c6/c7 proof on one finite divisibility graph."""
    graph = full_neighbors(A, lower, upper)
    full = matching(graph)
    if full is not None:
        cover = tuple(full.values())
        assert len(cover) == len(set(cover)) == len(A)
        assert prod(cover) % prod(A) == 0
        return cover, "matching"

    deficient = minimal_deficient(A, graph)
    assert deficient is not None
    S, N_set = deficient
    N = tuple(sorted(N_set))
    assert len(S) in (6, 7)
    assert len(N) == len(S) - 1

    # Minimality makes every deletion match bijectively onto the fixed N(S).
    for omitted in S:
        subgraph = {a: graph[a] for a in S if a != omitted}
        submatching = matching(subgraph)
        assert submatching is not None
        assert set(submatching.values()) == N_set

    g = gcd(*S)
    assert prod(N) * g % prod(S) == 0
    assert max(A) >= len(S) * g

    if len(S) == len(A):
        candidates = [
            z for z in range(lower, upper + 1) if z % g == 0 and z not in N_set
        ]
        assert candidates
        cover = N + (candidates[0],)
    else:
        assert len(A) == 7 and len(S) == 6
        (a0,) = set(A) - set(S)
        outside = [y for y in graph[a0] if y not in N_set]
        assert outside
        y = outside[0]
        candidates = [
            z
            for z in range(lower, upper + 1)
            if z % g == 0 and z not in N_set and z != y
        ]
        assert candidates
        cover = N + (y, candidates[0])

    assert len(cover) == len(set(cover)) == len(A)
    assert prod(cover) % prod(A) == 0
    return cover, "repair"


def merge_congruences(a, m, b, n):
    """Generalized CRT merge for the explicit matching obstruction."""
    g = gcd(m, n)
    assert (b - a) % g == 0
    reduced_n = n // g
    inverse = pow(m // g, -1, reduced_n)
    k = ((b - a) // g * inverse) % reduced_n
    modulus = m * reduced_n
    return (a + m * k) % modulus, modulus


def explicit_obstructions():
    """Rebuild the s=2,t=3 van Doorn-Li-Tang five-neighbor example."""
    D, base = 60, 370
    A6 = tuple(base + i + j * D for i in (1, 2) for j in (1, 2, 3))
    assert A6 == (431, 491, 551, 432, 492, 552)

    x0, modulus = 0, 1
    for i in (1, 2):
        for j in (1, 2, 3):
            x0, modulus = merge_congruences(
                x0, modulus, i, base + i + j * D
            )

    x = x0 - base
    lower, upper = x + 1, x + 2 * max(A6) - 1

    graph6 = full_neighbors(A6, lower, upper)
    assert matching(graph6) is None
    assert len({b for values in graph6.values() for b in values}) == 5
    cover6, route6 = repaired_cover(A6, lower, upper)
    assert route6 == "repair"

    # The same six-set is a minimal obstruction after adding a seventh modulus.
    A7 = A6 + (2,)
    graph7 = full_neighbors(A7, lower, upper)
    assert matching(graph7) is None
    cover7, route7 = repaired_cover(A7, lower, upper)
    assert route7 == "repair"
    return A6, cover6, A7, cover7


def exhaustive_small_blocks():
    counts = {6: 0, 7: 0}
    repairs = {6: 0, 7: 0}
    bracketing_repairs = 0
    for n in (6, 7):
        max_M = 17 if n == 6 else 14
        for M in range(n + 1, max_M + 1):
            for prefix in combinations(range(2, M), n - 1):
                A = prefix + (M,)
                last_t = 3 * M if n == 6 else M
                for t in range(last_t + 1):
                    counts[n] += 1
                    if n == 6:
                        bracket_graph = bracketing_neighbors(A, t)
                        if matching(bracket_graph) is None:
                            bracketing_repairs += 1
                            vertices = tuple(
                                sorted(
                                    {
                                        b
                                        for values in bracket_graph.values()
                                        for b in values
                                    }
                                )
                            )
                            assert len(vertices) == 5
                            g = gcd(*vertices)
                            assert prod(vertices) * g % prod(A) == 0
                            extras = [
                                z
                                for z in range(t + 1, t + 2 * M + 1)
                                if z % g == 0 and z not in vertices
                            ]
                            assert extras
                            assert prod(vertices + (extras[0],)) % prod(A) == 0
                    _, route = repaired_cover(A, t + 1, t + 2 * M)
                    repairs[n] += route == "repair"
    assert counts[6] == 382_096
    assert bracketing_repairs == 7
    return counts, repairs, bracketing_repairs


def main():
    counts, repairs, bracketing_repairs = exhaustive_small_blocks()
    A6, cover6, A7, cover7 = explicit_obstructions()
    print("small translated blocks checked:", counts)
    print("full-graph repairs needed in small grid:", repairs)
    print("bracketing Hall failures repaired:", bracketing_repairs)
    print("explicit c6 obstruction:", A6)
    print("explicit c6 repaired cover:", cover6)
    print("explicit c7 obstruction:", A7)
    print("explicit c7 repaired cover:", cover7)
    print("ALL C6/C7 REPAIR CHECKS PASSED")


if __name__ == "__main__":
    main()
