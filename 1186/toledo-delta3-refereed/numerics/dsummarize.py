import json, sys, collections
from common import BLOCKS
def coarse(col, minfrac=0.01):
    """run-length encode, then absorb runs shorter than minfrac*n into the previous run (noise filter)."""
    n = len(col); runs = []
    for c in col:
        if runs and runs[-1][0] == c: runs[-1][1] += 1
        else: runs.append([c, 1])
    changed = True
    while changed:
        changed = False
        for i, (c, L) in enumerate(runs):
            if L < minfrac * n and len(runs) > 1:
                j = i - 1 if i > 0 else i + 1
                runs[j][1] += L; del runs[i]
                # merge equal neighbours
                k = 0
                while k < len(runs) - 1:
                    if runs[k][0] == runs[k + 1][0]: runs[k][1] += runs[k + 1][1]; del runs[k + 1]
                    else: k += 1
                changed = True; break
    return [(c, round(L * 548 / n, 1)) for c, L in runs]
for fn in sys.argv[1:]:
    rs = [json.loads(l) for l in open(fn)]
    n = rs[0]["n"]
    print(f"== {fn}: n={n}, {len(rs)} runs; 117n^2/2192 - n/2 = {117*n*n/2192 - n/2:.2f}; 117/2192 = {117/2192:.6f}")
    by = collections.defaultdict(list)
    for r in rs: by[(r["method"], r["fam"])].append(r)
    for key, L in sorted(by.items()):
        vs = sorted(r["V"] for r in L)
        print(f"  {key[0]:4s}/{key[1]:7s} runs={len(L):3d} min V={vs[0]} (V/n^2={vs[0]/n/n:.6f}) median V={vs[len(vs)//2]} #hitting-min={sum(v==min(r['V'] for r in rs) for v in vs)}")
    b = min(rs, key=lambda r: r["V"])
    print(f"  overall min V={b['V']} V/n^2={b['V']/n/n:.6f}; exact runs={b['nruns']}; coarse blocks (548ths):", coarse([1 if c == '+' else -1 for c in b["col"]]))
    if b["runs"]: print("  exact runs (sign,len):", b["runs"])
