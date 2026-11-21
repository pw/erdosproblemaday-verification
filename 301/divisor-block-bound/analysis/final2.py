#!/usr/bin/env python3
"""Certified divisor-block bounds for Erdos #301, two chains:
  chain 1: 5040 -> 55440 (x11) -> 720720 (x13)
  chain 2: 10080 -> 110880 (x11) -> 1441440 (x13);  10080's tail also bounded by h_5040(t) + h_315(t/32)
Exact values come from: dfs/*.out (C depth-first search), profile/*.log + partial_*.json (CP-SAT, lazy cuts),
profile/scip_*.log (SCIP re-check of CP-SAT 'jump' verdicts). A value is CONFIRMED when two independent
programs give it (DFS = CP-SAT, or CP-SAT jump re-checked infeasible by SCIP / CP-SAT grow with a witness we
re-check). Version A uses confirmed values only; version B every exact value. Lower bounds elsewhere.
C_M = 1 - delta_M W_M  (= delta_M * sum of 1/d over the divisors where F steps up, since delta_M sigma(M)/M = 1).
"""
import re, os, sys, json, glob
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bound import divisors, delta, step_eval, W_of
B = os.path.expanduser("~/MathDyad/erdos301")

def parse_out(path):
    prof, wit, verd = {}, {}, {}
    for line in open(path):
        m = re.match(r"\s*d=\s*(\d+)\s+(grow|jump)\s+F=\s*(\d+)", line)
        if not m: continue
        d = int(m.group(1)); prof[d] = int(m.group(3)); verd[d] = m.group(2)
        w = re.search(r"wit=([\d,]+)", line)
        if w: wit[d] = [int(x) for x in w.group(1).split(",")]
    return prof, wit, verd

def is_free(A, M):
    A = sorted(A)
    for i, a in enumerate(A):
        target = M // a; sums = {0}
        for b in A[i + 1:]:
            v = M // b; sums |= {s + v for s in sums if s + v <= target}
            if target in sums: return False
    return True

def h_from(M, prof):
    D = divisors(M); h = {}
    for i, d in enumerate(D):
        if d not in prof: break
        h[d] = i + 1 - prof[d]
    return h

def load(M):
    dfs = [p for p in glob.glob(f"{B}/dfs/p{M}_*.out")] + ([f"{B}/dfs/p{M}.out"] if os.path.exists(f"{B}/dfs/p{M}.out") else [])
    cps = glob.glob(f"{B}/profile/run*_{M}_*.log")
    best = lambda paths: max(((parse_out(p), p) for p in paths), key=lambda x: len(x[0][0]), default=(({}, {}, {}), None))
    (dp, dw, dv), dpath = best(dfs)
    (cp, cw, cv), cpath = best(cps)
    # CP-SAT witnesses + SCIP from JSON / scip logs
    cwj = {}
    for j in glob.glob(f"{B}/profile/partial_{M}_*.json"):
        J = json.load(open(j)); cwj.update({int(k): v for k, v in J.get("witnesses", {}).items()})
    scip_ok = set(); scip_bad = set()
    for s in glob.glob(f"{B}/profile/scip_{M}*.log"):
        for line in open(s):
            m = re.match(r"jump d=(\d+) F_before=(\d+): SCIP (\S+) (OK|DISAGREE)", line)
            if m: (scip_ok if m.group(4) == "OK" else scip_bad).add(int(m.group(1)))
    badw = [d for d, A in dw.items() if not (len(A) == dp[d] and max(A) == d and all(M % x == 0 for x in A) and is_free(A, M))]
    badw += [("cp", d) for d, A in cwj.items() if not (len(A) == cp.get(d, -1) and max(A) == d and is_free(A, M))]
    common = sorted(set(dp) & set(cp)); dis = [d for d in common if dp[d] != cp[d]]
    hd, hc = h_from(M, dp), h_from(M, cp)
    # external confirmations: a published prefix constant from an independent program (Della Pietra C++,
    # Orakwue's two C99 engines) that our DFS prefix reproduces exactly confirms every value up to T.
    EXTERNAL = {5040: [(5040, Fr(15437, 19344))], 2520: [(2520, Fr(839, 1040))], 1680: [(1680, Fr(4865, 5952))],
                10080: [(504, Fr(3481, 4368)), (1008, Fr(2233, 2808))]}
    ext_T = 0; ext_log = []
    for T, Cpub in EXTERNAL.get(M, []):
        if hd and max(hd) >= T:
            pre = {d: v for d, v in hd.items() if d <= T}
            Cours = 1 - delta(M) * W_of(M, lower(M, pre, []))
            ext_log.append((T, str(Cours), str(Cpub), Cours == Cpub))
            if Cours == Cpub: ext_T = max(ext_T, T)
    # confirmed prefix: walk divisors in order while each step is confirmed
    D = divisors(M); conf = {}
    for i, d in enumerate(D):
        ok = d <= ext_T and d in hd
        if d in dp and d in cp and dp[d] == cp[d]: ok = True
        elif d in cp and cv.get(d) == "jump" and d in scip_ok: ok = True
        elif d in cp and cv.get(d) == "grow" and d in cwj: ok = True
        if not ok: break
        conf[d] = hd.get(d, hc.get(d))
    either = dict(hc); either.update(hd)
    # prefix consistency: either must be a prefix where both agree on overlap
    info = dict(M=M, dfs=os.path.basename(dpath) if dpath else None, dfs_through=max(hd) if hd else 0,
                cpsat=os.path.basename(cpath) if cpath else None, cpsat_through=max(hc) if hc else 0,
                overlap_through=max(common) if common else 0, disagreements=dis, bad_witnesses=badw,
                scip_confirmed=len(scip_ok), scip_disagree=sorted(scip_bad), external=ext_log, confirmed_through=max(conf) if conf else 0)
    return conf, either, info

def lower(M, exact, parents):
    """parents: list of (Mc, lbc, scale) giving h_M(t) >= sum lbc(t/scale) ... each item is a decomposition (list)."""
    D = divisors(M); lb = {}; run = 0
    for d in D:
        v = exact.get(d, 0)
        for decomp in parents:
            v = max(v, sum(step_eval(lbc, divisors(Mc), Fr(d, s)) for (Mc, lbc, s) in decomp))
        run = max(run, v); lb[d] = run
    return lb

if __name__ == "__main__":
    data = {M: load(M) for M in (315, 3465, 45045, 5040, 55440, 720720, 10080, 110880, 1441440)}
    for M in data: print(data[M][2])
    report = {}
    for ver, k in (("A_confirmed", 0), ("B_all_exact", 1)):
        ex = {M: data[M][k] for M in data}
        for Mo in (315, 3465, 45045): ex[Mo] = data[Mo][k]  # odd parts: full profiles, DFS + CP-SAT
        lb315 = lower(315, ex[315], []); lb3465 = lower(3465, ex[3465], []); lb45045 = lower(45045, ex[45045], [])
        lb5 = lower(5040, ex[5040], [])
        lb55 = lower(55440, ex[55440], [[(5040, lb5, 1), (5040, lb5, 11)]])
        lb72 = lower(720720, ex[720720], [[(55440, lb55, 1), (55440, lb55, 13)]])
        lb10 = lower(10080, ex[10080], [[(5040, lb5, 1), (315, lb315, 32)]])
        lb110 = lower(110880, ex[110880], [[(10080, lb10, 1), (10080, lb10, 11)], [(55440, lb55, 1), (3465, lb3465, 32)]])
        lb144 = lower(1441440, ex[1441440], [[(110880, lb110, 1), (110880, lb110, 13)], [(720720, lb72, 1), (45045, lb45045, 32)]])
        for M, lb in ((5040, lb5), (55440, lb55), (720720, lb72), (10080, lb10), (110880, lb110), (1441440, lb144)):
            W = W_of(M, lb); C = 1 - delta(M) * W
            print(f"{ver}: M={M:>8} exact/confirmed through {max(ex[M]) if ex[M] else 0:>5}  W>={float(W):.9f}  C<={C}  = {float(C):.10f}")
            report.setdefault(ver, {})[M] = dict(W=str(W), C=str(C), Cf=float(C), through=max(ex[M]) if ex[M] else 0)
    json.dump({"info": {M: data[M][2] for M in data}, "bounds": report}, open(f"{B}/analysis/final2.json", "w"), indent=1, default=str)
