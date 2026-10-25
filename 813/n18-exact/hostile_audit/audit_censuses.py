#!/usr/bin/env python3
"""Pure-stdlib hostile regeneration/audit of the #813 frozen censuses."""

import argparse
from itertools import combinations
import shutil
import subprocess
import tempfile
from pathlib import Path


def executable(*names):
    for name in names:
        path = shutil.which(name)
        if path:
            return path
    raise RuntimeError(f"none of these executables is on PATH: {names}")


GENG = executable("nauty-geng", "geng")
SHORTG = executable("nauty-shortg", "shortg")


def decode_graph6(line):
    values = [byte - 63 for byte in line.strip()]
    n = values[0]
    assert 0 <= n <= 62
    bits = []
    for value in values[1:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adj = [0] * n
    cursor = 0
    for v in range(1, n):
        for u in range(v):
            if bits[cursor]:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
            cursor += 1
    return adj


def clique(adj, vertices):
    return all(adj[u] >> v & 1 for u, v in combinations(vertices, 2))


def independent(adj, vertices):
    return all(not (adj[u] >> v & 1) for u, v in combinations(vertices, 2))


def valid_h(adj):
    vertices = range(len(adj))
    if any(clique(adj, four) for four in combinations(vertices, 4)):
        return False
    for seven in combinations(vertices, 7):
        if not any(clique(adj, three) for three in combinations(seven, 3)):
            return False
    return True


def alpha_at_most(adj, bound):
    return not any(independent(adj, subset)
                   for subset in combinations(range(len(adj)), bound + 1))


def valid_m(adj):
    return alpha_at_most(adj, 2) and not any(
        clique(adj, five) for five in combinations(range(len(adj)), 5)
    )


def lines(path):
    with open(path, "rb") as src:
        return {line.strip() for line in src if line.strip()}


def shortg_line_set(graphs):
    with tempfile.TemporaryDirectory(prefix="audit-erdos813-shortg-") as directory:
        source = Path(directory) / "source.g6"
        target = Path(directory) / "target.g6"
        source.write_bytes(b"".join(line + b"\n" for line in sorted(graphs)))
        subprocess.run([SHORTG, "-q", str(source), str(target)], check=True)
        return lines(target)


parser = argparse.ArgumentParser()
parser.add_argument("bundle", type=Path)
args = parser.parse_args()
bundle = args.bundle.resolve()
assert (bundle / "MANIFEST.sha256").is_file()

for n in (7, 8, 9):
    process = subprocess.Popen([GENG, "-q", str(n)], stdout=subprocess.PIPE)
    total = 0
    h = set()
    h_alpha = set()
    m = set()
    assert process.stdout is not None
    for raw in process.stdout:
        line = raw.strip()
        total += 1
        adj = decode_graph6(line)
        if valid_h(adj):
            h.add(line)
            if alpha_at_most(adj, 3):
                h_alpha.add(line)
        if n in (7, 8) and valid_m(adj):
            m.add(line)
    assert process.wait() == 0

    filtered_path = bundle / "censuses" / f"census_n{n}_alpha3.g6"
    assert h_alpha == lines(filtered_path)
    print(
        f"H n={n} all_unlabeled={total} valid={len(h)} "
        f"alpha3={len(h_alpha)} exact_line_sets=PASS"
    )

    if n == 7:
        assert shortg_line_set(m) == shortg_line_set(
            lines(bundle / "censuses" / "census_m7_canonical.g6")
        )
        print(f"M n=7 valid={len(m)} exact_canonical_iso_set=PASS")
    if n == 8:
        assert shortg_line_set(m) == shortg_line_set(
            lines(bundle / "censuses" / "census_m8_canonical.g6")
        )
        print(f"M n=8 valid={len(m)} exact_canonical_iso_set=PASS")

# The independently audited order-10 H census is small enough to refilter.
base10 = bundle / "prior_delta10" / "census_n10.g6"
direct10 = bundle / "prior_delta10" / "direct_n10_canon.g6"
assert base10.read_bytes() == direct10.read_bytes()
h10 = lines(base10)
h10_alpha = {
    line for line in h10 if alpha_at_most(decode_graph6(line), 3)
}
assert h10_alpha == lines(bundle / "censuses" / "census_n10_alpha3.g6")
print(
    f"H n=10 base={len(h10)} alpha3={len(h10_alpha)} "
    "direct_parent_byte_match=PASS exact_line_set=PASS"
)
