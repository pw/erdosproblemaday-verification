import json,glob,sys
from fractions import Fraction as F
D=sys.argv[1]
prim={}
for f in glob.glob(D+"/pool_*.json"):
    for r in json.load(open(f))["pool"]: prim[r["p"]]=r["e"]
sub=json.load(open(D+"/subsets_S7.json"))
S7={5:4,7:6,11:10,13:12,17:16,19:18,31:30}
listed=[30240,40320,45360,50400,55440,60480,65520]
rows=[]
for N in range(30001,65521):
    if N in listed: continue
    B=[p for p,e in S7.items() if N%e==0]; key=",".join(map(str,B))
    loss=sub[key]["loss"]
    lb=sum(1/e for p,e in prim.items() if N%e==0)   # lower bound on density(N) from known primes
    rows.append((lb-loss,lb,loss,N, any(M%N==0 for M in listed)))
rows.sort(reverse=True)
print("known-prime count",len(prim))
for r in rows[:12]: print("N=%d  LBdens=%.4f loss=%.4f LB-loss=%.4f divides-a-computed-pool=%s"%(r[3],r[1],r[2],r[0],r[4]))
