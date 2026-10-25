#!/usr/bin/env python3
"""Erdős #203 — the COARSE-TORUS test (rank-2 member of the quotient family; the line lemma is the rank-1 member).

For T ≥ 1 let G = (Z/T)^2.  The image of L_p = {u k + v l ≡ 0 (mod e_p)} in G is the lattice
    S_p = { (k,l) mod T : u k + v l ≡ 0 (mod i_p) },   i_p := gcd(T, e_p),
because T Z^2 maps onto gcd(T,e_p)·Z/e_p (gcd(u,v,e_p) = 1, the character is onto).  So a coset C_p of L_p projects
onto ONE of the i_p cosets {u k + v l ≡ c (mod i_p)} of G, and the density of C_p inside that coset is
    w_p := i_p / e_p   (the intensity).
Hence if ∪ C_p = Z^2 then every cell x ∈ G satisfies   W(x) := Σ_{p : x ∈ coset_p} w_p ≥ 1.
(Average over G of W is Σ 1/e_p.  For i_p = e_p the coset is exact and w_p = 1; for gcd(T,e_p) = 1 the prime is a
constant 1/e_p on every cell.)   V_T(P) := max over coset choices of min over cells of W(x)  — exact rational;
V_T < 1 ⇒ no #203 covering uses a subset of P.   Monotone in T along divisibility (T | T' ⇒ V_{T'} ≤ V_T),
and projecting G → Z/T (forget k) is the line lemma in direction (1,0) coarsened to M' = T (so V_T ≤ that value).

Instruments: CP-SAT (max z) with every witness re-counted exactly on the full torus by an independent numpy loop;
brute force for tiny instances; --selftest checks the lattice-image claim by direct enumeration and runs two
synthetic controls (a pool that covers must give V = 1; drop one coset and V = 0).
"""
import json, sys, argparse, itertools, time
from math import gcd
from fractions import Fraction as F
from functools import reduce
import numpy as np

def lcm(a,b): return a*b//gcd(a,b)

def instance(pool, T):
    E = F(0); lum=[]
    for q in pool:
        e,u,v = q['e'],q['u'],q['v']
        i = gcd(T, e)
        if i == 1: E += F(1,e)
        else: lum.append((q['p'], e, u % i, v % i, i, F(i,e)))
    return E, lum

def cells_of(lum, T):
    """For each lumpy prime: integer array over the T×T torus giving (u k + v l) mod i for every cell."""
    k = np.arange(T).reshape(T,1); l = np.arange(T).reshape(1,T)
    return [((u*k + v*l) % i).astype(np.int64) for (_,_,u,v,i,_) in lum]

def recount(E, lum, T, c):
    S = reduce(lcm, [w.denominator for *_,w in lum] + [E.denominator], 1)
    W = np.full((T,T), int(E*S), dtype=np.int64)
    for arr,(p,e,u,v,i,w),cp in zip(cells_of(lum,T), lum, c):
        W[arr == cp] += int(w*S)
    return F(int(W.min()), S), F(int(W.sum()), S*T*T)

def cpsat(E, lum, T, time_limit=600, workers=4, fix_first=True, hint=None):
    from ortools.sat.python import cp_model
    S = reduce(lcm, [w.denominator for *_,w in lum] + [E.denominator], 1)
    m = cp_model.CpModel()
    x = [[m.NewBoolVar(f"x{j}_{c}") for c in range(i)] for j,(_,_,_,_,i,_) in enumerate(lum)]
    for xs in x: m.AddExactlyOne(xs)
    if fix_first and lum:
        # translations of the torus act transitively on the cosets of the first prime iff its character is onto Z/i,
        # which holds (gcd(u,v,i)=1); fix it to 0.
        m.Add(x[0][0] == 1)
    Eint = int(E*S); wint=[int(w*S) for *_,w in lum]
    z = m.NewIntVar(0, Eint + sum(wint), "z")
    arrs = cells_of(lum, T)
    for k in range(T):
        for l in range(T):
            m.Add(sum(wint[j]*x[j][int(arrs[j][k,l])] for j in range(len(lum))) + Eint >= z)
    m.Maximize(z)
    if hint is not None:
        for j,cp in enumerate(hint):
            for c in range(lum[j][4]): m.AddHint(x[j][c], 1 if c==cp else 0)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = time_limit; s.parameters.num_workers = workers
    st = s.Solve(m); name = s.StatusName(st)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        c = [next(cc for cc in range(lum[j][4]) if s.Value(x[j][cc])) for j in range(len(lum))]
        return name, F(int(s.ObjectiveValue()), S), F(int(s.BestObjectiveBound()), S), c, s.WallTime()
    return name, None, None, None, s.WallTime()

def feas(E, lum, T, time_limit=600, workers=4, fix_first=True):
    """Pure feasibility: is there a coset choice with W(cell) >= 1 on EVERY cell?  INFEASIBLE ⇒ V_T < 1 ⇒ excluded."""
    from ortools.sat.python import cp_model
    S = reduce(lcm, [w.denominator for *_,w in lum] + [E.denominator], 1)
    m = cp_model.CpModel()
    x = [[m.NewBoolVar(f"x{j}_{c}") for c in range(i)] for j,(_,_,_,_,i,_) in enumerate(lum)]
    for xs in x: m.AddExactlyOne(xs)
    if fix_first and lum: m.Add(x[0][0] == 1)
    Eint = int(E*S); wint=[int(w*S) for *_,w in lum]
    arrs = cells_of(lum, T)
    for k in range(T):
        for l in range(T):
            m.Add(sum(wint[j]*x[j][int(arrs[j][k,l])] for j in range(len(lum))) + Eint >= S)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = time_limit; s.parameters.num_workers = workers
    st = s.Solve(m); name = s.StatusName(st)
    c = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        c = [next(cc for cc in range(lum[j][4]) if s.Value(x[j][cc])) for j in range(len(lum))]
    return name, c, s.WallTime()

def brute(E, lum, T, limit=2_000_000):
    cfg = 1
    for *_,i,_ in lum: cfg *= i
    if cfg > limit: return None
    S = reduce(lcm, [w.denominator for *_,w in lum] + [E.denominator], 1)
    arrs = cells_of(lum, T); wint=[int(w*S) for *_,w in lum]
    masks = [[(a == c) for c in range(i)] for a,(_,_,_,_,i,_) in zip(arrs, lum)]
    base = np.full((T,T), int(E*S), dtype=np.int64); best=-1; bc=None
    for c in itertools.product(*[range(i) for *_,i,_ in lum]):
        W = base.copy()
        for j,cp in enumerate(c): W[masks[j][cp]] += wint[j]
        mn = int(W.min())
        if mn > best: best, bc = mn, c
    return F(best,S), list(bc)

def lattice_image_check(pool, T):
    """Direct enumeration: the set {(k,l) mod T : u k + v l ≡ 0 (mod e)} must equal {u k + v l ≡ 0 (mod gcd(T,e))}."""
    bad=0
    for q in pool:
        e,u,v = q['e'],q['u'],q['v']; i = gcd(T,e)
        img=set()
        R = lcm(T,e)
        for k in range(R):
            for l in range(R):
                if (u*k+v*l) % e == 0: img.add((k%T, l%T))
        pred = {(k,l) for k in range(T) for l in range(T) if (u*k+v*l) % i == 0}
        if img != pred: bad += 1; print("LATTICE IMAGE MISMATCH", q['p'], e, u, v, T, len(img), len(pred))
    return bad == 0

def selftest(args):
    import glob
    pool = json.load(open('pool_720.json'))['pool']
    ok = lattice_image_check(pool, 12) and lattice_image_check(pool, 10)
    print("lattice-image check (720 pool, T=12 and T=10):", "PASS" if ok else "FAIL")
    # synthetic covering: two 'primes' sharing the lattice k ≡ 0 (mod 2) — cosets 0 and 1 cover Z^2
    cov = [{"p":"a","e":2,"u":1,"v":0},{"p":"b","e":2,"u":1,"v":0}]
    E,lum = instance(cov, 4); name,V,bd,c,wt = cpsat(E,lum,4,30,2); rc,avg = recount(E,lum,4,c)
    print("synthetic cover: V =", V, "recount", rc, "(must be 1)"); ok = ok and V == 1 and rc == 1
    E,lum = instance(cov[:1], 4); name,V,bd,c,wt = cpsat(E,lum,4,30,2)
    print("one coset only: V =", V, "(must be 0)"); ok = ok and V == 0
    # brute vs cpsat on the 720 pool, T = 12 (exact cosets for 5,7,13 (e | 12), coarse for the rest)
    sub = pool[:7]   # {5,7,11,13,17,19,31}: product of gcd(12,e_p) small enough for brute force
    E,lum = instance(sub, 12); name,V,bd,c,wt = cpsat(E,lum,12,60,2); br = brute(E,lum,12)
    rc,avg = recount(E,lum,12,c)
    print("720 pool first 7 primes, T=12: cpsat", name, V, "recount", rc, "brute", br[0] if br else None, "avg", avg)
    ok = ok and br is not None and br[0] == V and rc == V
    E,lum = instance(pool, 12); name,V,bd,c,wt = cpsat(E,lum,12,60,2); rc,avg = recount(E,lum,12,c)
    print("720 pool all 15, T=12: cpsat", name, V, "recount", rc, "avg", avg, "(density 641/720)"); ok = ok and rc == V and avg == F(641,720)
    # consistency with the line lemma: V_T ≤ V_line((1,0), M'=T)  (projection forgets k)
    sys.path.insert(0, 'lines'); import linelemma as LL
    Ei,lumi,Mi,evi = LL.instance(pool,(1,0),12); namei,Vi,bdi,ti,wti = LL.cpsat(Ei,lumi,Mi,60,2)
    print("line lemma (1,0) at M'=12:", Vi, " torus T=12:", V, " (torus ≤ line required)"); ok = ok and V <= Vi
    print("SELFTEST", "PASS" if ok else "FAIL"); return 0 if ok else 2

def run(pool, T, args, label):
    E, lum = instance(pool, T)
    dens = E + sum(w/i for *_,i,w in lum)
    prod = 1
    for *_,i,_ in lum: prod *= i
    out = {"label":label, "T":T, "E":str(E), "E_f":float(E), "density":str(dens), "density_f":float(dens),
           "lumpy":len(lum), "cells":T*T, "prod_i":prod}
    if args.feas:
        name,c,wt = feas(E,lum,T,args.time,args.workers)
        out["feas"] = {"status":name, "c":c, "wall":wt}
        if c is not None:
            rc,avg = recount(E,lum,T,c); out["feas"]["recount_min"]=str(rc); out["feas"]["recount_ok"]=(rc>=1)
            if rc < 1: print("!! FEAS WITNESS FAILS RECOUNT", label, T, rc, file=sys.stderr)
        out["verdict"] = {"INFEASIBLE":"EXCLUDED (no coset choice reaches 1 on every cell)", "OPTIMAL":"not excluded (witness re-counted)",
                          "FEASIBLE":"not excluded (witness re-counted)"}.get(name, "UNDECIDED (time limit)")
        print(json.dumps(out), flush=True); return out
    name,V,bd,c,wt = cpsat(E,lum,T,args.time,args.workers)
    out["cpsat"] = {"status":name, "V":str(V) if V is not None else None, "V_f":float(V) if V is not None else None,
                    "bound":str(bd) if bd is not None else None, "bound_f":float(bd) if bd is not None else None, "c":c, "wall":wt}
    if c is not None:
        rc,avg = recount(E,lum,T,c); out["cpsat"]["recount"]=str(rc); out["cpsat"]["recount_ok"]=(rc==V); out["cpsat"]["witness_avg"]=str(avg)
        if rc != V: print("!! RECOUNT MISMATCH", label, T, rc, V, file=sys.stderr)
    if args.brute:
        br = brute(E,lum,T,args.brute_limit)
        if br is not None:
            out["brute"]={"V":str(br[0]),"c":br[1],"agrees_cpsat":(br[0]==V)}
            if br[0]!=V: print("!! BRUTE/CPSAT DISAGREE", label, T, br[0], V, file=sys.stderr)
    if V is None: verdict="UNDECIDED (no solution found in time)"
    elif name=="OPTIMAL": verdict = "EXCLUDED" if V<1 else "not excluded (witness re-counted)"
    elif V>=1: verdict = "not excluded (feasible witness)"
    elif bd<1: verdict = f"EXCLUDED by bound (proven max ≤ {float(bd):.4f} < 1; best found {float(V):.4f})"
    else: verdict = f"UNDECIDED (best {float(V):.4f} < 1, bound {float(bd):.4f})"
    out["verdict"]=verdict
    print(json.dumps(out), flush=True); return out

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("pool", nargs="?"); ap.add_argument("--T", default="60")
    ap.add_argument("--time", type=float, default=600); ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--brute", action="store_true"); ap.add_argument("--brute-limit", type=int, default=2_000_000)
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--feas", action="store_true", help="hard W>=1 on every cell; INFEASIBLE = excluded")
    args=ap.parse_args()
    if args.selftest: sys.exit(selftest(args))
    d=json.load(open(args.pool)); pool=d["pool"]; N=d["N"]
    for Ts in args.T.split(","):
        run(pool, int(Ts), args, f"N={N}")
