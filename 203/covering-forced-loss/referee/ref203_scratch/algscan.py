import csv, json, glob
from fractions import Fraction as F
D="/home/exedev/MathDyad/erdos203/"
S6={5:4,7:6,11:10,13:12,17:16,19:18}
ALW=0.0511363031
U6=1583/2700
rows={}
for f in ["scanN.tsv","scanN2.tsv"]:
    for r in csv.DictReader(open(D+f),delimiter="\t"): rows[int(r["N"])]=float(r["density"])
for f in glob.glob(D+"pool_*.json"):
    d=json.load(open(f)); rows[d["N"]]=float(sum(F(1,r["e"]) for r in d["pool"]))
bad=[]
for N,dens in sorted(rows.items()):
    s=sum(1/e for p,e in S6.items() if N%e==0)
    q=U6+ALW+dens-s
    if q>=1: bad.append((N,round(dens,4),round(q,4),[p for p,e in S6.items() if N%e]))
print("N where the README-described (monotone S6) algebraic bound does NOT exclude:",bad)
# what free-set-only bound gives for pools with empty S6 intersection
