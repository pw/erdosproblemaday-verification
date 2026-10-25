#!/usr/bin/env python3
"""Frontier: for every N with a computed complete pool density, decide whether a covering with lcm(e_p) = N is excluded
(pure) by U(S7 ∩ pool(N)) + density(N) − Σ_{S7∩pool(N)} 1/e < 1, and (algebraic, m = t^{N0}) by
maxU_alg(S6) + ALW + density(N) − Σ_{S6∩pool(N)} 1/e < 1, ALW = Σ_{odd prime q ≥ 7} 1/q² = 0.051136.
Reports every N NOT excluded, and the largest contiguous excluded range."""
import json, csv, glob
from fractions import Fraction
S7={5:4,7:6,11:10,13:12,17:16,19:18,31:30}; S6={p:e for p,e in S7.items() if p!=31}
sub=json.load(open("subsets_S7.json")); alg=json.load(open("algsweep_5_7_11_13_17_19.json"))
maxU_alg=max(v["U"] for v in alg.values()); ALW=0.051136
sum6=sum(1/e for e in S6.values())
rows={}
for f in ["scanN.tsv","scanN2.tsv","scanN3.tsv"]:
    try:
        for r in csv.DictReader(open(f),delimiter="\t"): rows[int(r["N"])]=(float(r["density"]),r["status"])
    except FileNotFoundError: pass
for f in glob.glob("pool_*.json"):
    d=json.load(open(f)); rows[d["N"]]=(float(sum(Fraction(1,r["e"]) for r in d["pool"])),"complete" if d["complete"] else "INCOMPLETE")
pure_fail=[]; alg_fail=[]; pending=[]; ALWC={}
for N,(dens,st) in sorted(rows.items()):
    B7=[p for p,e in S7.items() if N%e==0]; key=",".join(map(str,B7))
    if key not in sub: pending.append((N,key)); continue
    U=sub[key]["U"]; s7=sum(1/S7[p] for p in B7)
    q_pure=U+dens-s7
    B6=[p for p in B7 if p!=31]; s6=sum(1/S6[p] for p in B6)
    import os
    bf="algsweep_%s.json"%("_".join(map(str,B6)))
    bf31="algsweep_%s.json"%("_".join(map(str,B7)))
    if os.path.exists(bf31):   # exact sweep for the block incl. 31
        U_b=max(v["U"] for v in json.load(open(bf31)).values()); s_b=sum(1/S7[p] for p in B7); src="exact:"+bf31
    elif os.path.exists(bf):
        U_b=max(v["U"] for v in json.load(open(bf)).values()); s_b=s6; src="exact:"+bf
    else:
        U_b=maxU_alg; s_b=s6; src="monotone-S6"
    from math import lcm as _lcm
    from sympy import primerange
    blk=B7 if src.endswith(bf31) else B6
    L=1
    for p in blk: L=_lcm(L,p-1)
    # ALW_block = sum_{odd prime q, q ∤ L} 1/q^2 (q ≤ 10^5 explicitly; tail beyond 10^5 < 1e-5 added)
    if L not in ALWC: ALWC[L]=sum(1/q**2 for q in primerange(3,100000) if L%q!=0)+1e-5
    alw_b=ALWC[L]
    q_alg=U_b+alw_b+dens-s_b
    if q_pure>=1 or "UNFACTORED" in st: pure_fail.append((N,round(dens,4),round(q_pure,4),st))
    if q_alg>=1 or "UNFACTORED" in st: alg_fail.append((N,round(dens,4),round(q_alg,4),st,src,round(alw_b,4)))
Nmax=max(n for n in rows if n<=30000 and all(k<=n for k in rows if k<=n))
contig=max(rows)
for n in range(1,max(rows)+1):
    if n not in rows: contig=n-1; break
print("N values with data:",len(rows),"; contiguous from 1 to",contig,"; pending subsets:",pending[:5],len(pending))
if pending:
    print("CANNOT SEE: subset table incomplete — refusing to print a frontier"); raise SystemExit(2)
print("maxU_alg(S6) =",maxU_alg,"  alg threshold for full S6 block: density <",round(1-ALW-maxU_alg+sum6,5))
print("PURE covering NOT excluded (N, density, union bound):",pure_fail)
print("ALGEBRAIC variant NOT excluded:",alg_fail)
pf=[n for n,*_ in pure_fail if n<=contig]; af=[n for n,*_ in alg_fail if n<=contig]
print("pure: every N <=",contig,"excluded" if not pf else f"EXCEPT {pf}")
print("alg : every N <=",contig,"excluded" if not af else f"EXCEPT {af}")
