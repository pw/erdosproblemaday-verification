#!/usr/bin/env python3
"""Tally a campaign against classes_all.tsv (referee obj. 2). Exit 0 only if every one of the 13,351 (j, M) keys has
a DONE row (kissat: 'UNSAT'; drat: 's UNSATISFIABLE' + 's VERIFIED' + a CNF hash); exit 3 on any SAT; exit 1 otherwise.
Prints per-case counts of done / pending / other verdicts."""
import sys, collections
mode = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else f"runs/campaign_{mode}.tsv"
keys = [tuple(l.split("\t")[:2]) for l in open("classes_all.tsv") if l.strip()]
assert len(keys) == 13351 and len(set(keys)) == 13351
done, other, sat = set(), collections.Counter(), []
for l in open(out):
    f = l.rstrip("\n").split("\t")
    if len(f) < 3: continue
    k = (f[0], f[1])
    if (mode == "kissat" and f[2] == "UNSAT") or (mode == "drat" and f[2] == "s UNSATISFIABLE" and len(f) > 4 and f[3] == "s VERIFIED" and len(f[4]) == 16):
        done.add(k)
    else:
        other[f[2][:24]] += 1
        if f[2].startswith("SAT") or f[2] == "s SATISFIABLE": sat.append(k)
stray = done - set(keys)
for j in "01234":
    kj = [k for k in keys if k[0] == j]
    print(f"case {j}: {sum(1 for k in kj if k in done)}/{len(kj)} done")
print(f"total done {len(done & set(keys))}/13351; stray keys {len(stray)}; non-done rows by verdict {dict(other)}")
if sat: print("SAT CELLS:", sat); sys.exit(3)
sys.exit(0 if len(done & set(keys)) == 13351 and not stray else 1)
