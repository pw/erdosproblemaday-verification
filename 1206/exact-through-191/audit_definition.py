#!/usr/bin/env python3
"""Independent arithmetic/certificate audit for Erdős #1206, N=132..191.

This script deliberately does not share code with verify_exact.cpp.  It
reconstructs all equal sums of two cubes, checks every displayed upper witness
both as a hypergraph cover and directly as a Sidon set, and pins the canonical
N=191 edge list by SHA-256.  The C++ verifier separately proves every lower
bound by exhaustive search.
"""

from collections import defaultdict
from hashlib import sha256


ROWS = (
    (132, 133, 21, (2,10,29,30,33,36,42,44,45,51,54,58,59,63,66,72,76,90,94,102,110)),
    (134, 137, 22, (2,4,6,10,33,36,42,50,51,54,58,60,63,64,66,72,76,90,92,99,110,116)),
    (138, 143, 23, (2,6,10,27,30,33,36,42,50,51,54,58,59,60,63,66,72,76,90,94,110,116,138)),
    (144, 155, 24, (1,2,4,10,18,24,33,36,42,48,50,51,54,58,60,63,72,76,84,90,92,95,99,120)),
    (156, 160, 25, (1,2,4,18,24,33,36,48,50,51,58,60,63,69,72,76,80,90,92,99,116,120,138,142,156)),
    (161, 164, 26, (1,2,4,6,10,18,23,24,33,36,42,50,51,54,58,60,63,72,76,90,92,102,108,132,138,156)),
    (165, 165, 27, (1,2,4,6,10,18,22,23,24,33,36,42,50,51,54,63,72,76,90,92,100,102,108,114,132,138,156)),
    (166, 171, 28, (2,4,6,10,14,18,23,24,27,32,33,36,38,42,50,58,60,64,72,76,80,84,90,92,108,132,150,156)),
    (172, 173, 29, (2,4,10,12,14,18,23,24,33,36,42,44,48,50,58,60,64,71,72,76,84,90,92,99,108,135,150,156,165)),
    (174, 179, 30, (1,2,4,6,10,14,18,23,24,33,36,42,48,50,51,58,60,71,72,76,84,90,92,99,108,156,164,165,166,174)),
    (180, 185, 31, (2,4,10,14,18,23,24,33,36,42,44,48,50,51,58,60,64,66,71,72,76,84,90,92,99,108,141,150,156,165,166)),
    (186, 191, 32, (2,4,10,18,23,30,33,36,42,48,50,51,55,58,59,60,63,64,66,71,72,76,90,99,120,136,138,150,156,165,166,168)),
)

EXPECTED_EDGE_DIGEST_191 = (
    "644dadc2aa52bddd902f03811acff745e129add6406fac5a09be5099852fb081"
)


def collision_data(n):
    groups = defaultdict(list)
    for a in range(1, n + 1):
        for b in range(a, n + 1):
            groups[a**3 + b**3].append((a, b))
    edges = set()
    for representations in groups.values():
        for i in range(1, len(representations)):
            for j in range(i):
                edges.add(tuple(sorted(set(representations[i] + representations[j]))))
    return groups, tuple(sorted(edges))


def direct_sidon_check(n, cover):
    roots = sorted(set(range(1, n + 1)).difference(cover))
    seen = {}
    for i, a in enumerate(roots):
        for b in roots[i:]:
            value = a**3 + b**3
            assert value not in seen, (value, seen[value], (a, b))
            seen[value] = (a, b)
    return len(roots), len(seen)


def main():
    assert ROWS[0][0] == 132 and ROWS[-1][1] == 191
    assert all(a[1] + 1 == b[0] for a, b in zip(ROWS, ROWS[1:]))

    for lo, hi, tau, cover in ROWS:
        assert len(cover) == tau
        assert tuple(sorted(set(cover))) == cover
        assert cover[0] >= 1 and cover[-1] <= hi
        groups, edges = collision_data(hi)
        chosen = set(cover)
        assert all(chosen.intersection(edge) for edge in edges)
        root_count, sum_count = direct_sidon_check(hi, cover)
        assert root_count == hi - tau
        assert sum_count == root_count * (root_count + 1) // 2
        print(
            f"N={lo}..{hi}: tau={tau}, upper witness at {hi} checked; "
            f"pairs={hi * (hi + 1) // 2}, groups={len(groups)}, "
            f"collision_edges={len(edges)}, retained={root_count}"
        )

    groups, edges = collision_data(191)
    collision_groups = [group for group in groups.values() if len(group) > 1]
    canonical = "\n".join(",".join(map(str, edge)) for edge in edges).encode()
    digest = sha256(canonical).hexdigest()
    assert 191 * 192 // 2 == 18_336
    assert len(groups) == 18_212
    assert len(collision_groups) == 124
    assert max(map(len, collision_groups)) == 2
    assert len(edges) == 124
    assert {len(edge) for edge in edges} == {4}
    assert len({vertex for edge in edges for vertex in edge}) == 164
    assert digest == EXPECTED_EDGE_DIGEST_191
    print(
        "N=191 canonical edge audit: pairs=18336, sums=18212, "
        "collision_groups=124, edges=124, active_vertices=164, "
        f"digest={digest}"
    )
    print("ARITHMETIC AND UPPER-CERTIFICATE AUDIT PASSED")


if __name__ == "__main__":
    main()
