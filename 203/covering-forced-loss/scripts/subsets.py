#!/usr/bin/env python3
"""U(B) for every subset B of the block S7 = {5,7,11,13,17,19,31} (exact brute force via maxunion), written to
subsets_S7.json as {"5,7,11": {"U":..,"loss":..,"T":..}}. Singletons: U = 1/e. Empty: 0."""
import json, subprocess, itertools
from fractions import Fraction
pool={r["p"]:r for r in json.load(open("pool_5040.json"))["pool"]}
S=[5,7,11,13,17,19,31]
res={"":{"U":0.0,"loss":0.0}}
for p in S: res[str(p)]={"U":1/pool[p]["e"],"loss":0.0}
subs=[c for r in range(2,len(S)+1) for c in itertools.combinations(S,r)]
subs.sort(key=lambda c:(len(c),c))
for c in subs:
    key=",".join(map(str,c)); fn="sub_"+"_".join(map(str,c))+".txt"
    open(fn,"w").write("".join(f"{pool[p]['e']} {pool[p]['u']} {pool[p]['v']}\n" for p in c))
    out=subprocess.run(["nice","-n","19","./maxunion",fn],capture_output=True,text=True).stdout
    mx=[l for l in out.splitlines() if l.startswith("MAX")][0]; cov=int(mx.split("covered=")[1].split()[0]); T=int(out.split("T=")[1].split()[0])
    s=sum(Fraction(1,pool[p]["e"]) for p in c)
    res[key]={"U":cov/(T*T),"U_frac":f"{cov}/{T*T}","loss":float(s-Fraction(cov,T*T)),"T":T}
    print(key,res[key],flush=True)
    json.dump(res,open("subsets_S7.json","w"),indent=1)
print("done")
