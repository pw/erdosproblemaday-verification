#!/usr/bin/env python3
"""Final certified computation for Erdos #301 (divisor-block bound). Reads every profile source, checks the two
programs agree on their overlap, re-checks every DFS 'grow' witness is solution-free with separate Python code,
checks the reader's claimed excess intervals against the exact excess, and prints the bound chain
5040 -> 55440 -> 720720 in two versions: (A) exact values only where BOTH programs computed them, (B) where either did.
"""
import re, sys, json, os
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bound import divisors, delta, step_eval, W_of
BASE = os.path.expanduser("~/MathDyad/erdos301")
SRC = {5040: ["dfs/p5040_v2full.out", "dfs/p5040_v2.out", "dfs/p5040.out", "profile/run_5040.log"],
       55440: ["dfs/p55440_0.out", "profile/run_55440_1000.log"],
       720720: ["dfs/p720720_2000.out", "profile/run_720720_300.log"]}

def parse(path):
    prof, wit = {}, {}
    for line in open(os.path.join(BASE, path)):
        m = re.match(r"\s*d=\s*(\d+)\s+(grow|jump)\s+F=\s*(\d+)", line)
        if not m: continue
        d = int(m.group(1)); prof[d] = int(m.group(3))
        w = re.search(r"wit=([\d,]+)", line)
        if w: wit[d] = [int(x) for x in w.group(1).split(",")]
    return prof, wit

def is_free(A, M):
    A = sorted(A)
    for i, a in enumerate(A):
        target = M // a; sums = {0}
        for b in A[i + 1:]:
            v = M // b
            sums |= {s + v for s in sums if s + v <= target}
            if target in sums: return False
    return True

def prefix_exact(M, prof):
    D = divisors(M); h = {}
    for i, d in enumerate(D):
        if d not in prof: break
        h[d] = i + 1 - prof[d]
    return h

out = {}; exactA = {}; exactB = {}
for M, paths in SRC.items():
    progs = {}
    for p in paths:
        if not os.path.exists(os.path.join(BASE, p)): continue
        prof, wit = parse(p)
        kind = "dfs" if p.startswith("dfs") else "cpsat"
        if kind not in progs or len(prof) > len(progs[kind][0]): progs[kind] = (prof, wit, p)
    # agreement on overlap (all files, pairwise vs the longest of each kind)
    a, b = progs.get("dfs"), progs.get("cpsat")
    common = sorted(set(a[0]) & set(b[0])) if a and b else []
    dis = [d for d in common if a[0][d] != b[0][d]]
    # witness check (DFS witnesses: size must equal F and be free and inside the prefix and contain d)
    badw = []
    for d, A in a[1].items():
        if not (len(A) == a[0][d] and d in A and max(A) == d and all(M % x == 0 for x in A) and is_free(A, M)): badw.append(d)
    ha = prefix_exact(M, a[0]); hb = prefix_exact(M, b[0]) if b else {}
    both = {d: ha[d] for d in ha if d in hb and hb[d] == ha[d]}
    either = dict(hb); either.update(ha)
    exactA[M] = both; exactB[M] = either
    out[M] = dict(dfs_file=a[2], dfs_through=max(ha), cpsat_file=b[2] if b else None, cpsat_through=max(hb) if hb else None,
                  overlap_through=max(common) if common else None, disagreements=dis, dfs_witnesses=len(a[1]), bad_witnesses=badw)
    print(M, out[M])

def chain(exact):
    res = {}; prev = None
    for M, p in ((5040, None), (55440, 11), (720720, 13)):
        D = divisors(M); lb = {}; run = 0
        for d in D:
            v = exact[M].get(d, 0)
            if prev:
                Mc, lbc = prev; Dc = divisors(Mc)
                v = max(v, step_eval(lbc, Dc, d) + step_eval(lbc, Dc, Fr(d, p)))
            run = max(run, v); lb[d] = run
        W = W_of(M, lb); C = 1 - delta(M) * W
        res[M] = (W, C, lb); prev = (M, lb)
    return res

for name, ex in (("A (both programs)", exactA), ("B (either program)", exactB)):
    r = chain(ex)
    for M in (5040, 55440, 720720):
        W, C, _ = r[M]
        print(f"{name}: M={M} exact_through={max(ex[M])} W>={W} ({float(W):.9f}) C<={C} ({float(C):.10f})")
    out[name] = {str(M): {"W": str(r[M][0]), "C": str(r[M][1]), "Cf": float(r[M][1])} for M in r}

# excess over baseline + reader intervals
h5 = exactB[5040]; D5 = divisors(5040); h55 = exactB[55440]; D55 = divisors(55440); h72 = exactB[720720]
def excess(hM, Dc, hc, p):
    return {d: hM[d] - (step_eval(hc, Dc, d) + step_eval(hc, Dc, Fr(d, p))) for d in sorted(hM)}
ex55 = excess(h55, D5, h5, 11); ex72 = excess(h72, D55, h55, 13)
print("excess 55440:", {d: v for d, v in ex55.items() if v})
print("excess 720720:", {d: v for d, v in ex72.items() if v})
reader = [(55440, 36, 42, 1), (55440, 55, 77, 1), (55440, 77, 80, 2), (55440, 80, 84, 1), (55440, 84, 90, 2), (55440, 90, 105, 1), (720720, 65, 66, 1)]
for M, x, y, inc in reader:
    ex = ex55 if M == 55440 else ex72; D = divisors(M)
    pts = [d for d in D if x <= d < y]
    # value on [x,y) is the step value at each divisor in it; also the value carried in from below x
    carried = step_eval(ex, D, x)
    vals = [step_eval(ex, D, d) for d in pts]
    ok = all(v >= inc for v in vals) and carried >= inc
    print(f"reader M={M} [{x},{y}) +{inc}: exact excess on interval {vals} -> {'HOLDS' if ok else 'FAILS'}")
json.dump(out, open(os.path.join(BASE, "analysis/final.json"), "w"), indent=1, default=str)
