#!/usr/bin/env python3
"""Independent graph6/bitset verification of the 59-edge witness."""

from hashlib import sha256


J_GRAPH6 = "JiQC@{}N`{?"


def decode_graph6(encoded):
    """Decode the short graph6 form (n <= 62) without external libraries."""
    values = [ord(char) - 63 for char in encoded]
    if not values or not 0 <= values[0] <= 62:
        raise ValueError("only short graph6 strings are supported")
    n = values[0]
    need = n * (n - 1) // 2
    expected_characters = 1 + (need + 5) // 6
    if len(values) != expected_characters:
        raise ValueError("noncanonical graph6 length")
    stream = []
    for value in values[1:]:
        if not 0 <= value <= 63:
            raise ValueError("invalid graph6 character")
        stream.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    if len(stream) < need:
        raise ValueError("truncated graph6 string")
    if any(stream[need:]):
        raise ValueError("nonzero graph6 padding")

    adjacency = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if stream[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return adjacency


def edge_count(adjacency):
    return sum(mask.bit_count() for mask in adjacency) // 2


def complement(adjacency):
    n = len(adjacency)
    universe = (1 << n) - 1
    return [universe & ~(mask | (1 << vertex)) for vertex, mask in enumerate(adjacency)]


def maximum_clique_size(adjacency):
    """Exact include/exclude search over a candidate bitset."""
    best = 0

    def search(size, candidates):
        nonlocal best
        if size + candidates.bit_count() <= best:
            return
        if not candidates:
            best = max(best, size)
            return

        while candidates:
            if size + candidates.bit_count() <= best:
                return
            bit = candidates & -candidates
            vertex = bit.bit_length() - 1
            search(size + 1, candidates & adjacency[vertex])
            candidates ^= bit
        best = max(best, size)

    search(0, (1 << len(adjacency)) - 1)
    return best


def disjoint_union(*graphs):
    total = sum(len(graph) for graph in graphs)
    result = [0] * total
    offset = 0
    for graph in graphs:
        for vertex, mask in enumerate(graph):
            shifted = 0
            while mask:
                bit = mask & -mask
                neighbor = bit.bit_length() - 1
                shifted |= 1 << (offset + neighbor)
                mask ^= bit
            result[offset + vertex] = shifted
        offset += len(graph)
    return result


def complete_graph(n):
    universe = (1 << n) - 1
    return [universe ^ (1 << vertex) for vertex in range(n)]


def edge_digest(adjacency):
    edges = []
    for u, mask in enumerate(adjacency):
        for v in range(u + 1, len(adjacency)):
            if mask & (1 << v):
                edges.append(f"{u}-{v}")
    payload = f"n={len(adjacency)};" + ";".join(edges)
    return sha256(payload.encode("ascii")).hexdigest()


def main():
    if not __debug__:
        raise RuntimeError("run this verifier without Python -O")
    j = decode_graph6(J_GRAPH6)
    assert len(j) == 11
    assert all(not (mask & (1 << vertex)) for vertex, mask in enumerate(j))
    assert all(
        bool(j[u] & (1 << v)) == bool(j[v] & (1 << u))
        for u in range(len(j))
        for v in range(len(j))
    )
    assert edge_count(j) == 26
    j_omega = maximum_clique_size(j)
    j_alpha = maximum_clique_size(complement(j))
    assert (j_omega, j_alpha) == (2, 5)

    g = disjoint_union(
        complete_graph(5),
        complete_graph(5),
        complete_graph(5),
        complement(j),
    )
    assert len(g) == 26
    assert edge_count(g) == 59
    g_omega = maximum_clique_size(g)
    g_alpha = maximum_clique_size(complement(g))
    assert (g_omega, g_alpha) == (5, 5)

    # Compute the same lower-bound arithmetic without sharing code with the
    # first verifier: T_5(26) has parts 6,5,5,5,5.
    complete_edges = 26 * 25 // 2
    within_parts = 6 * 5 // 2 + 4 * (5 * 4 // 2)
    turan = complete_edges - within_parts
    extremal_non_5_partite = turan - 26 // 5 + 1
    lower = complete_edges - extremal_non_5_partite
    assert (complete_edges, turan, extremal_non_5_partite, lower) == (325, 270, 266, 59)

    print("graph6/bitset verifier: PASS")
    print(f"J graph6={J_GRAPH6!r}")
    print(f"J: vertices={len(j)} edges={edge_count(j)} omega={j_omega} alpha={j_alpha}")
    print(f"G: vertices={len(g)} edges={edge_count(g)} omega={g_omega} alpha={g_alpha}")
    print(f"complement arithmetic: K26={complete_edges}, t_5={turan}, p_5={extremal_non_5_partite}, lower={lower}")
    print(f"G edge digest={edge_digest(g)}")


if __name__ == "__main__":
    main()
