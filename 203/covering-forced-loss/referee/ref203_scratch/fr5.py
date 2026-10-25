import csv, json, glob, os
from fractions import Fraction as F
D="/home/exedev/MathDyad/erdos203/"
S7={5:4,7:6,11:10,13:12,17:16,19:18,31:30}
ALW=0.0511363031
rows={}
for f in ["scanN.tsv","scanN2.tsv"]:
    for r in csv.DictReader(open(D+f),delimiter="\t"): rows[int(r["N"])]=float(r["density"])
for f in glob.glob(D+"pool_*.json"):
    d=json.load(open(f)); rows[d["N"]]=float(sum(F(1,r["e"]) for r in d["pool"]))
worst=[]
for N,dens in rows.items():
    B7=[p for p,e in S7.items() if N%e==0]; B6=[p for p in B7 if p!=31]
    for B in (B7,B6):
        fn=D+"algsweep_%s.json"%"_".join(map(str,B))
        if B and os.path.exists(fn):
            U=max(v["U"] for v in json.load(open(fn)).values())
            from math import lcm
            L=1
            for p in B: L=lcm(L,p-1)
            miss = (0.04 if L%5 else 0)+(1/9 if L%3 else 0)
            q=U+ALW+dens-sum(1/S7[p] for p in B)
            worst.append((q+miss,q,N,B,L,miss)); break
worst.sort(reverse=True)
print("top corrected bounds among N using an exact sub-block file:")
for w in worst[:8]: print("N=%d block=%s LCM=%d frontier_q=%.4f missing_free=%.3f corrected=%.4f"%(w[2],w[3],w[4],w[1],w[5],w[0]))
print("any corrected >=1 with N<=30000:",[ (w[2],round(w[0],4)) for w in worst if w[0]>=1 and w[2]<=30000])
