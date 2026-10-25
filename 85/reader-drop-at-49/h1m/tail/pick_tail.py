#!/usr/bin/env python3
"""Tail probe (2026-10-20 00Z erdos seat): the authors' HARDEST H1 orbits (census set, by their census CaDiCaL seconds,
plus the one they call 'hardest') mapped to OUR miss-matrix cells, so our encoding can be timed where theirs was slowest.
Tag rule + relabelling phi + canonical form are those of ../../sample_h1.py and ../referee/rowmatch_authors.py
(refereed); the mapped cell must be a row of classes_all.tsv or we stop."""
import csv, hashlib, json, itertools, sys
from pathlib import Path
R = Path.home() / "MathDyad/subs-1019/85/dl/receipts/research/problems/erdos-85-wip-01"
INV = Path("/tmp/erdos85-1019/repo/proofs/Proofs/Certificates/h1_orbit_inventory.compact")
H1M = Path.home() / "MathDyad/erdos85/h1m"
K = int(sys.argv[1]) if len(sys.argv) > 1 else 24
PAIRS = [(X, Y) for X in range(8) for Y in range(X + 1, 8) if Y != X ^ 1]
def E_ours(j): return [2 if (p < j or s == 0) else 1 for p in range(4) for s in (0, 1)]
def tomat(flat):
    M = [[0] * 8 for _ in range(8)]
    for (X, Y), v in zip(PAIRS, flat): M[X][Y] = M[Y][X] = v
    return M
def act(g, flat):
    M = tomat(flat); Nn = [[0] * 8 for _ in range(8)]
    for X in range(8):
        for Y in range(8): Nn[g[X]][g[Y]] = M[X][Y]
    return tuple(Nn[X][Y] for X, Y in PAIRS)
inv = {}
for line in INV.read_text().splitlines():
    v = list(map(int, line.split())); assert len(v) == 25
    table = {p: x for p, x in zip(PAIRS, v[1:]) if x}
    tag = hashlib.sha1(json.dumps(sorted(table.items())).encode()).hexdigest()[:16]
    inv[tag] = (v[0], tuple(v[1:]))
ours = {}
for l in open(H1M / "classes_all.tsv"):
    f = l.rstrip("\n").split("\t"); ours[(int(f[0]), tuple(map(int, f[1].split(","))))] = f[1]
census = [(float(r["census_cadical_seconds"]), r["id"].removeprefix("h1_"), float(r["solver_cpu_seconds"]))
          for r in csv.DictReader(open(R / "h1_cert_full_20261001/receipts/h1_cert_census_receipts.tsv"), delimiter="\t")]
census.sort(reverse=True)
picks = [(None, "81494a6ef36d3ec9", None)] + census[:K]
Gs = {}
for j in range(5):
    Gs[j] = [g for g in itertools.permutations(range(8))
             if all(g[X ^ 1] == g[X] ^ 1 for X in range(8)) and all(E_ours(j)[g[X]] == E_ours(j)[X] for X in range(8))]
out = []
for cs, tag, cpu in picks:
    a, T = inv[tag]; j = 4 - a
    phi = [None] * 8
    for p in range(4):
        if p < a: phi[2 * p], phi[2 * p + 1] = 2 * (j + p) + 1, 2 * (j + p)
        else: phi[2 * p], phi[2 * p + 1] = 2 * (p - a), 2 * (p - a) + 1
    rep = min(act(g, act(phi, T)) for g in Gs[j])
    key = (j, rep)
    assert key in ours, f"{tag}: mapped cell not in classes_all.tsv"
    out.append((j, ours[key], tag, cs, cpu))
    print(f"{j}\t{ours[key]}\t{tag}\tcensus_cadical_s={cs}\tsolver_cpu_s={cpu}")
print(f"# {len(out)} cells, {len(set((o[0], o[1]) for o in out))} distinct", file=sys.stderr)
