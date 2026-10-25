#!/usr/bin/env python3
"""Draw a uniform random sample of H1 orbits from the 13,351 the paper certifies, with the published CNF
sha256 for each, and write table files in v2cnf's input format.

Independent re-derivations here (not copied from their tooling): the 24-pair order, the tag rule
(sha1 of the sorted nonzero table, first 16 hex) and the union of the four evidence sets are recomputed
and cross-checked against the inventory: every receipt tag must occur in the inventory exactly once.
"""
import csv, hashlib, json, random, sys
from pathlib import Path

R = Path.home() / "MathDyad/subs-1019/85/dl/receipts/research/problems/erdos-85-wip-01"
INV = Path("/tmp/erdos85-1019/repo/proofs/Proofs/Certificates/h1_orbit_inventory.compact")
OUT = Path(sys.argv[1]); N = int(sys.argv[2]); SEED = int(sys.argv[3])
PAIRS = [(c, j) for c in range(8) for j in range(c + 1, 8) if j != (c ^ 1)]
assert len(PAIRS) == 24

inv = {}
for line in INV.read_text().splitlines():
    v = list(map(int, line.split()))
    assert len(v) == 25, v
    table = {p: x for p, x in zip(PAIRS, v[1:]) if x}
    tag = hashlib.sha1(json.dumps(sorted(table.items())).encode()).hexdigest()[:16]
    assert tag not in inv, "duplicate tag " + tag
    inv[tag] = (v[0], table)
print("inventory orbits:", len(inv))

ev = {}
for r in csv.DictReader(open(R / "h1_bank_check_20261006/receipts/h1_bank_check_receipts.tsv"), delimiter="\t"):
    assert r["status"] == "VERIFIED"
    ev[r["tag"]] = ("bank", r["cnf_sha256"])
for r in csv.DictReader(open(R / "h1_cert_full_20261001/receipts/h1_cert_census_receipts.tsv"), delimiter="\t"):
    t = r["id"].removeprefix("h1_")
    assert t not in ev
    ev[t] = ("census", r["cnf_sha256"])
for line in open(R / "h1_cert_full_20261001/receipts/historical96_cake_lpr_receipts.jsonl"):
    r = json.loads(line)
    assert r["tag"] not in ev and r["status"] == "CAKE_LPR_VERIFIED", r["status"]
    ev[r["tag"]] = ("historical", r["cnf_sha256_expected"])
ev["81494a6ef36d3ec9"] = ("hardest", None)
print("evidence orbits:", len(ev), {k: sum(1 for x in ev.values() if x[0] == k) for k in ("bank", "census", "historical", "hardest")})
missing = [t for t in ev if t not in inv]
print("evidence tags absent from inventory:", len(missing))
assert not missing

rng = random.Random(SEED)
pool = sorted(t for t in ev if ev[t][0] != "hardest")
pick = rng.sample(pool, N)
OUT.mkdir(parents=True, exist_ok=True)
rows = []
for t in pick:
    prof, table = inv[t]
    (OUT / f"{t}.table.json").write_text(json.dumps([[list(k), v] for k, v in sorted(table.items())]))
    rows.append({"tag": t, "set": ev[t][0], "profile": prof, "cnf_sha256": ev[t][1]})
(OUT / "sample.json").write_text(json.dumps({"seed": SEED, "n": N, "pool": len(pool), "rows": rows}, indent=1))
for r in rows:
    print(r["tag"], r["set"], r["profile"], r["cnf_sha256"][:16])
