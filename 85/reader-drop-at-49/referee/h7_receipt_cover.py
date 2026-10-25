#!/usr/bin/env python3
"""Referee: per cube, does the collected receipt table name every leaf index 0..N-1 (N from inputs.json)
exactly once plus one cover row, with one leaf (F9_t0 #249) closed only via the split table?"""
import csv, io, json, subprocess, sys
from collections import Counter
C = "/home/exedev/MathDyad/subs-1019/85/dl/receipts/research/problems/erdos-85-wip-01/h7_hsb_campaign_20261008/receipts/collected"
inp = json.load(open("/tmp/erdos85-1019/h7tools/inputs.json"))
allbad = 0
for name, c in sorted(inp["cubes"].items()):
    raw = subprocess.run(["zstd", "-dc", f"{C}/{name}.receipts.tsv.zst"], capture_output=True, check=True).stdout.decode()
    rows = list(csv.DictReader(io.StringIO(raw), delimiter="\t"))
    leaves = Counter(r["leaf"] for r in rows)
    covers = leaves.pop("cover", 0)
    ids = set(int(k) for k in leaves)
    N = c["leaves"]
    missing = sorted(set(range(N)) - ids); extra = sorted(ids - set(range(N)))
    dups = [k for k, v in leaves.items() if v > 1]
    cover_ok = covers == 1 and any(r["leaf"] == "cover" and r["cnf_sha256"] == c["cover_cnf_sha256"] for r in rows)
    bad = bool(missing or extra or not cover_ok)
    allbad += bad
    print(f"{name}: N={N} rows={len(rows)} covers={covers} cover_hash_ok={cover_ok} missing={missing[:5]}{'...' if len(missing)>5 else ''} extra={extra[:3]} dups={len(dups)}")
raw = subprocess.run(["zstd", "-dc", f"{C}/cube_F9_t0.split-receipts.tsv.zst"], capture_output=True, check=True).stdout.decode()
rows = list(csv.DictReader(io.StringIO(raw), delimiter="\t"))
kinds = Counter((r["leaf"], r["kind"]) for r in rows)
print("split rows", len(rows), kinds, "distinct subleaf idx", len({r['index'] for r in rows if r['kind']=='subleaf'}))
specs = [json.loads(l) for l in open(f"{C}/split-specs.jsonl")]
print("split specs", len(specs), [ (s.get('cube'), s.get('leaf'), len(s.get('clauses',[])), s.get('split_sha256','')[:12]) for s in specs][:5])
used = {r["split_sha256"] for r in rows}
print("split sha used by receipts", [u[:12] for u in used])
sp = [s for s in specs if s.get("split_sha256") in used]
if sp:
    cl = sp[0]["clauses"]
    sub = {int(r["index"]): r["clause"] for r in rows if r["kind"] == "subleaf"}
    agree = all(" ".join(map(str, cl[i])) == sub.get(i) for i in range(len(cl)))
    print("subleaf clause strings match spec:", agree, "n", len(cl))
    # do the 256 blocking clauses form a complete case split (every assignment of their vars falsifies one)?
    import itertools
    vs = sorted({abs(l) for c in cl for l in c})
    print("vars in split", len(vs))
print("cubes with problems:", allbad)
