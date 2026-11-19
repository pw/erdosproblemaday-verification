import json, collections
import sys
for tag, key in [(t, "Q_target" if t == "tilt" else "Qp_psi") for t in (sys.argv[1:] or ["tilt", "plant"])]:
    c = json.load(open(f"ctrl_{tag}.json"))
    qphi = c["Q_phistar"] if tag == "tilt" else c["Qp_phistar"]
    tgt = c[key]
    rs = [json.loads(l) for l in open(f"csearch_N1096_{tag}.jsonl")]
    print(f"== control {tag}: Q'(phi*)={qphi:.12f}, planted target={tgt:.12f} (target better by {qphi-tgt:.3e}); {len(rs)} runs")
    by = collections.defaultdict(list)
    for r in rs: by[r["method"]].append(r)
    for m, L in sorted(by.items()):
        hit = sum(r["Q"] <= tgt + 1e-10 for r in L); beat = sum(r["Q"] < qphi - 1e-10 for r in L)
        stuck = sum(r["ham"] == 0 for r in L)
        b = min(r["Q"] for r in L)
        print(f"  {m:5s} runs={len(L):4d} best={b:.12f} reached-target={hit} ({100*hit/len(L):.1f}%) beat-phi*={beat} ({100*beat/len(L):.1f}%) ended-exactly-at-±phi*={stuck}")
        fam = collections.defaultdict(list)
        for r in L: fam[r["fam"]].append(r)
        print("        " + "; ".join(f"{f}: {sum(r['Q'] <= tgt + 1e-10 for r in v)}/{len(v)}" for f, v in sorted(fam.items())))
