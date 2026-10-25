import json,glob
from fractions import Fraction
D="/home/exedev/MathDyad/erdos203/"
prim={}
for f in glob.glob(D+"pool_*.json"):
    for r in json.load(open(f))["pool"]: prim[r["p"]]=r["e"]
print("union primes",len(prim))
sub=json.load(open(D+"subsets_S7.json"))
S7={5:4,7:6,11:10,13:12,17:16,19:18,31:30}
lossS7=Fraction(4,4)  # placeholder
from fractions import Fraction as F
sumS7=sum(F(1,e) for e in S7.values()); lossfull=float(sumS7-F(303336,518400))
listed=[30240,40320,45360,50400,55440,60480,65520]
rows=[]
for N in range(30001,65521):
    B=[p for p,e in S7.items() if N%e==0]; key=",".join(map(str,B))
    loss=lossfull if len(B)==7 else sub[key]["loss"]
    lb=sum(1/e for p,e in prim.items() if N%e==0)
    covered_by_listed=any(M%N==0 for M in listed)
    rows.append((lb-loss,lb,loss,N,covered_by_listed))
rows.sort(reverse=True)
print("N in (30000,65520] with LB(density)-loss(S7 cap pool) >= 0.95, not a divisor of a computed excluded pool:")
for q,lb,loss,N,c in rows[:40]:
    if not c: print(N, "LB dens %.4f loss %.4f  LB-loss %.4f"%(lb,loss,q))
bad=[r for r in rows if r[0]>=1 and not r[4]]
print("count with LB-loss>=1 (Theorem B provably cannot exclude):",len(bad), [r[3] for r in bad][:20])
