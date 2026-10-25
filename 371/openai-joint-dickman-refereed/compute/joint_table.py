# joint-law table at 1e6/1e8/1e10 vs rho(1/a)rho(1/b) and a HEURISTIC second-order product (label (c)): local density of
# P(n) <= n^a near n ≈ rho(u) - gamma*rho(u-1)/log n (u = 1/a), averaged over n <= X with mean 1/log n ≈ 1/(log X - 1). Output joint_table_1e10.txt
import numpy as np, math
exec(open('readhist.py').read().split("if __name__")[0].replace("sys.argv[1]","'hist_1e10.bin'"))
h=1e-4; U=np.arange(0,60+h/2,h); R=np.ones_like(U); k1=int(round(1/h))
for i in range(k1+1,len(U)): R[i]=R[i-1]+h*(-R[i-1-k1]/U[i-1]-R[i-k1]/U[i])/2
rho=lambda u: float(np.interp(u,U,R)); g=0.5772156649015329
def corr(a,X): u=1/a; return rho(u)-g*rho(u-1)/(math.log(X)-1)
print("joint law: counted share of 2<=n<=X with P(n)<=n^a and P(n+1)<=n^b, vs Theorem 1.1's limit and a heuristic second-order product")
print(f"{'a':>4} {'b':>4} | {'X=1e6':>9} {'X=1e8':>9} {'X=1e10':>9} | {'rho*rho':>9} | {'2nd-order@1e10':>14} | ratio(count/2nd-order)")
for A,B in [(0.3,0.3),(0.5,0.5),(0.3,0.7),(0.5,0.7),(0.7,0.7),(0.9,0.9)]:
    v=[joint(list(decs).index(10**k),A,B)/10**k for k in (6,8,10)]
    p=rho(1/A)*rho(1/B); s=corr(A,1e10)*corr(B,1e10)
    print(f"{A:>4} {B:>4} | {v[0]:>9.6f} {v[1]:>9.6f} {v[2]:>9.6f} | {p:>9.6f} | {s:>14.6f} | {v[2]/s:.4f}")
print("marginals (first coordinate):")
for A in (0.3,0.5,0.7):
    v=[C[list(decs).index(10**k),:int(round(100*A))+1,:].sum()/10**k for k in (6,8,10)]
    print(f"  a={A}: {v[0]:.6f} {v[1]:.6f} {v[2]:.6f} | rho(1/a)={rho(1/A):.6f} | 2nd-order@1e10={corr(A,1e10):.6f}")
