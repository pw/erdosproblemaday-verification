#!/usr/bin/env python3
"""End-to-end control of the WHOLE pipeline (normalisation + R1 + R1b + class SB + high-perm SB) on the small
analogues n = d^2 (low degree d, high degree d+1, where the same saturation argument holds), against a DIRECT
encoding with no normalisation, no R1/R1b and no SB (c4cnf on all pairs, exactly h vertices of degree d+1).
For every (d, h): pipeline verdict must equal direct verdict; every SAT model from either side is re-checked."""
import itertools, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fsenc, c4cnf
KIS = [str(Path.home() / "MathDyad/tools/kissat/build/kissat"), "-q"]
CAD = ["/usr/bin/cadical", "-q"]
CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
def solve(cnf, var, name, n, fixed, target_all):
    path = f"/tmp/erdos85-fs/small/{name}.cnf"; cnf.to_file(path)
    res = []
    for s in (KIS, CAD):
        t0 = time.time()
        out = subprocess.run(["timeout", str(CAP), "nice", "-n", "19"] + s + [path], capture_output=True, text=True).stdout
        v = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "UNKNOWN"
        note = ""
        if v == "SAT":
            model = [int(t) for l in out.splitlines() if l.startswith("v ") for t in l[2:].split()]
            degs, mc = c4cnf.check_graph(n, list(fixed) + c4cnf.decode(model, var))
            note = f"model degrees_ok={all(degs[u]==target_all[u] for u in range(n))} maxcodeg={mc}"
        res.append((s[0].split('/')[-1], v, round(time.time() - t0, 1), note))
    return res
Path("/tmp/erdos85-fs/small").mkdir(parents=True, exist_ok=True)
d = int(sys.argv[1]); n = d * d
lts = {0: [[]]}
if d >= 6:   # linear triple systems on h points up to iso, small h only (by brute force + canonical form)
    pass
for h in range(1, d + 3):
    if (d * n + h) % 2: continue
    Ts = [[]]
    if d >= 6:
        Ts = []
        seen = set()
        trip = list(itertools.combinations(range(h), 3))
        for t in range(0, h * (h - 1) // 6 + 1):
            for sysT in itertools.combinations(trip, t):
                if any(len(set(a) & set(b)) > 1 for a, b in itertools.combinations(sysT, 2)): continue
                key = min(tuple(sorted(tuple(sorted(p[x] for x in b)) for b in sysT)) for p in itertools.permutations(range(h)))
                if key in seen: continue
                seen.add(key); Ts.append([list(b) for b in key])
    cells = [(T, fsenc.stratum_gen(n, d, h, T)) for T in Ts]
    cells = [(T, c) for T, c in cells if c is not None]
    if not cells: continue
    # direct
    tgt = {v: (d + 1 if v < h else d) for v in range(n)}
    cnf, var, F, adjS = c4cnf.build(n, [], [], tgt)
    direct = solve(cnf, var, f"d{d}_h{h}_direct", n, [], tgt)
    print(f"d={d} h={h} DIRECT", direct, flush=True)
    pipe = []
    for T, (H, fixed, target, blocks) in cells:
        cnf, var, F, adjS, st, cls = fsenc.build(n, H, fixed, target, highs=H, sb="all", r1=True, r1b=True, hdeg=d + 1)
        # high-side SB: all transpositions of highs that preserve the block multiset
        perms = []
        for a, b in itertools.combinations(range(h), 2):
            sig = list(range(h)); sig[a], sig[b] = b, a
            try:
                perms.append(fsenc.high_perm(h, h, blocks, sig))
            except AssertionError:
                pass
        top = max([abs(l) for c in cnf.clauses for l in c] + [len(var)])
        top, nc = fsenc.add_perm_sb(cnf, var, n, perms, top)
        tall = {v: (d + 1 if v < h else d) for v in range(n)}
        r = solve(cnf, var, f"d{d}_h{h}_T{len(T)}_{len(pipe)}", n, fixed, tall)
        pipe.append(r)
        print(f"d={d} h={h} T={T} PIPELINE classes={st['sb_classes']} highperms={len(perms)}", r, flush=True)
    dv = {v for _, v, _, _ in direct} - {"UNKNOWN"}
    pv = set()
    for r in pipe:
        pv |= {v for _, v, _, _ in r} - {"UNKNOWN"}
    pip = "SAT" if "SAT" in pv else ("UNSAT" if pv == {"UNSAT"} and all(any(v == "UNSAT" for _, v, _, _ in r) for r in pipe) else "UNKNOWN")
    print(f"d={d} h={h} AGREE={dv == {pip}} direct={dv} pipeline={pip}", flush=True)
