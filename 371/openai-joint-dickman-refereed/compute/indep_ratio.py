# independence ratio joint(a,b)/(marg_n(a)*marg_{n+1}(b)) at X = 10^k from hist_1e10.bin (bins k = ceil(100u)); output indep_ratio_1e10.txt
import numpy as np
exec(open('readhist.py').read().split("if __name__")[0].replace("sys.argv[1]","'hist_1e10.bin'"))
print("independence ratio  joint(a,b) / (marg_n(a) * marg_{n+1}(b)), all counted at the same X (1.0 = independent)")
print(f"{'a':>4} {'b':>4} | " + " ".join(f"{'X=1e'+str(k):>8}" for k in (4,6,8,10)))
for A,B in [(0.3,0.3),(0.5,0.5),(0.3,0.7),(0.7,0.3),(0.5,0.7),(0.7,0.7),(0.9,0.9)]:
    row=[]
    for k in (4,6,8,10):
        d=list(decs).index(10**k); i=int(round(100*A)); j=int(round(100*B)); X=10**k
        row.append((C[d,:i+1,:j+1].sum()/X)/((C[d,:i+1,:].sum()/X)*(C[d,:,:j+1].sum()/X)))
    print(f"{A:>4} {B:>4} | "+" ".join(f"{r:>8.4f}" for r in row))
