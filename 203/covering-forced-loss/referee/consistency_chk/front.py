import json,csv,glob,os,sys
from fractions import Fraction as F
from math import lcm
D=sys.argv[1]; os.chdir(D)
S7={5:4,7:6,11:10,13:12,17:16,19:18,31:30}
sub=json.load(open("subsets_S7.json"))
alg_full=json.load(open("algsweep_5_7_11_13_17_19.json")); maxU=max(v["U"] for v in alg_full.values())
ALW=0.4522474200410654985-0.25-1/9-0.04
rows={}
for f in ["scanN.tsv","scanN2.tsv"]:
    for r in csv.DictReader(open(f),delimiter="\t"): rows[int(r["N"])]=float(r["density"])
for f in glob.glob("pool_*.json"):
    d=json.load(open(f)); rows[d["N"]]=float(sum(F(1,r["e"]) for r in d["pool"]))
worst_pure=(-9,None); worst_alg=(-9,None); worst_alg5=(-9,None); used=set()
fails5=[]
for N,dens in sorted(rows.items()):
    B7=[p for p,e in S7.items() if N%e==0]; key=",".join(map(str,B7))
    q=sub[key]["U"]+dens-sum(1/S7[p] for p in B7)
    if N<=30000 and q>worst_pure[0]: worst_pure=(q,N)
    B6=[p for p in B7 if p!=31]
    bf31="algsweep_%s.json"%"_".join(map(str,B7)); bf="algsweep_%s.json"%"_".join(map(str,B6))
    if os.path.exists(bf31): U=max(v["U"] for v in json.load(open(bf31)).values()); s=sum(1/S7[p] for p in B7); src=bf31; blk=B7
    elif os.path.exists(bf): U=max(v["U"] for v in json.load(open(bf)).values()); s=sum(1/S7[p] for p in B6); src=bf; blk=B6
    else: U=maxU; s=sum(1/S7[p] for p in B6); src="mono"; blk=None
    qa=U+ALW+dens-s
    # missing free sets: odd q in {3,5} not dividing lcm(p-1 : p in blk) (exact sub-block sweeps only)
    extra=0
    if blk is not None:
        L=1
        for p in blk: L=lcm(L,p-1)
        for qq in (3,5):
            if L%qq: extra+=1/qq**2
        if L%4: extra+=1/16
    used.add((src,extra))
    if N<=30000 and qa>worst_alg[0]: worst_alg=(qa,N,src)
    if N<=30000 and qa+extra>worst_alg5[0]: worst_alg5=(qa+extra,N,src,extra)
    if N<=30000 and qa+extra>=1: fails5.append((N,round(dens,4),round(qa,4),round(qa+extra,4),src))
print("N count",len(rows))
print("worst pure union bound N<=30000:",worst_pure)
print("worst alg union bound N<=30000 (as frontier.py):",worst_alg)
print("worst alg with missing free sets credited:",worst_alg5)
print("alg FAILS once missing free sets credited:",len(fails5),fails5[:10])
print("sources used:",sorted(used,key=str))
print("--- big N")
for N in sorted(n for n in rows if n>30000):
    dens=rows[N]
    B7=[p for p,e in S7.items() if N%e==0]; key=",".join(map(str,B7))
    q=sub[key]["U"]+dens-sum(1/S7[p] for p in B7)
    B6=[p for p in B7 if p!=31]
    qa=maxU+ALW+dens-sum(1/S7[p] for p in B6)
    print(N, "%.6f"%dens, "pure %.4f"%q, "excl" if q<1 else "NOT", " alg %.4f"%qa, "excl" if qa<1 else "NOT")
print("alg threshold full S6:", 1-ALW-maxU+sum(1/S7[p] for p in [5,7,11,13,17,19]))
print("ALW",ALW)
print("85.5 check:", sub["5,7,11,13,17,19,31"]["U"]+143/140-sum(1/e for e in S7.values()))
print("1.16625-1.163041=",1.16625-21493/18480)
