#!/usr/bin/env python3
"""Referee check: is the H1 evidence set EXACTLY the Lean capacity-filtered inventory (as a set of
(profile, table)), not just the same count?  Re-implements Lean's oneHighTableCrossMissCapacity and
oneHighInventoryRowTable from the .lean source, independently of sample_h1.py."""
import csv, hashlib, json, sys
from pathlib import Path
R = Path.home()/"MathDyad/subs-1019/85/dl/receipts/research/problems/erdos-85-wip-01"
INV = Path("/tmp/erdos85-1019/repo/proofs/Proofs/Certificates/h1_orbit_inventory.compact")
PAIRS = [(c, j) for c in range(8) for j in range(8) if c < j and j != (c ^ 1)]
assert len(PAIRS) == 24
def get(tab, c, j): return tab.get((min(c, j), max(c, j)), 0)
def capacity(tab):
    return all(get(tab, a, b ^ 1) + get(tab, b, a ^ 1) <= 5 for (a, b) in PAIRS)
def tag(tab):
    nz = {p: x for p, x in tab.items() if x}
    return hashlib.sha1(json.dumps(sorted(nz.items())).encode()).hexdigest()[:16]
rows = []
for line in INV.read_text().split("\n"):
    f = line.split(" ")
    try: v = [int(x) for x in f]
    except ValueError: continue
    if len(v) != 25 or not (0 <= v[0] < 5): continue
    rows.append((v[0], dict(zip(PAIRS, v[1:]))))
print("raw rows", len(rows))
cap = [(p, t) for p, t in rows if capacity(t)]
print("capacity rows", len(cap), "removed", len(rows) - len(cap))
from collections import Counter
print("per profile", sorted(Counter(p for p, _ in cap).items()))
captag = {}
for p, t in cap:
    k = tag(t); assert k not in captag, k; captag[k] = p
alltag = {tag(t): p for p, t in rows}
# evidence
ev = {}
def add(t, kind, prof):
    ev.setdefault(t, []).append((kind, prof))
for r in csv.DictReader(open(R/"h1_bank_check_20261006/receipts/h1_bank_check_receipts.tsv"), delimiter="\t"):
    if r["status"] != "VERIFIED": print("bank non-verified", r["tag"], r["status"]); continue
    add(r["tag"], "bank", None)
man = {}
for line in open(R/"h1_bank_check_20261006/receipts/bank_manifest.jsonl"):
    m = json.loads(line); ps = {c["p"] for c in m["candidates"]}; man[m["tag"]] = ps
for r in csv.DictReader(open(R/"h1_cert_full_20261001/receipts/h1_cert_census_receipts.tsv"), delimiter="\t"):
    if r["status"] != "CERTIFIED": print("census non-certified", r["id"], r["status"]); continue
    add(r["id"].removeprefix("h1_"), "census", int(r["profile"]))
for line in open(R/"h1_cert_full_20261001/receipts/historical96_cake_lpr_receipts.jsonl"):
    r = json.loads(line)
    if r["status"] != "CAKE_LPR_VERIFIED": print("hist non-verified", r["tag"], r["status"]); continue
    add(r["tag"], "historical", r.get("profile"))
add("81494a6ef36d3ec9", "hardest", None)
print("evidence tags", len(ev), Counter(k for v in ev.values() for k, _ in v))
dup = {t: v for t, v in ev.items() if len(v) > 1}
print("tags with >1 evidence rows", len(dup), list(dup.items())[:5])
E, C = set(ev), set(captag)
print("evidence - capacity:", len(E - C), sorted(E - C)[:10])
print("capacity - evidence:", len(C - E), sorted(C - E)[:10])
print("evidence tags in raw inventory but capacity-removed:", len((E - C) & set(alltag)))
# profile agreement
bad = []
for t, v in ev.items():
    for kind, p in v:
        if p is None and kind == "bank":
            ps = man.get(t)
            if ps is None: bad.append((t, kind, "no manifest")); continue
            if {int(x) for x in ps} != {captag.get(t)}: bad.append((t, kind, ps, captag.get(t)))
        elif p is not None and p != captag.get(t): bad.append((t, kind, p, captag.get(t)))
print("profile disagreements:", len(bad), bad[:10])
print("bank tags w/o manifest:", sum(1 for t, v in ev.items() if any(k=='bank' for k,_ in v) and t not in man))
