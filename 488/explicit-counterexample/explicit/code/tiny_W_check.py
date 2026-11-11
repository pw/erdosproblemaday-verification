# containment control for bracketsW: exact M_A(WT) and |A| by enumeration for y=61, small T (Liu's p=61 example family)
import sys
def primes_upto(y): return [p for p in range(2,y+1) if all(p%d for d in range(2,int(p**.5)+1))]
P=primes_upto(61); q=67
def smooth(x):
    out=[1]
    for p in P:
        new=[]
        for s in out:
            t=s
            while t<=x: new.append(t); t*=p
        out=new
    return sorted(out)
import bisect
T=int(sys.argv[1]); W=int(sys.argv[2])
S=smooth(W*T)
psi=lambda x: bisect.bisect_right(S,x)
A=psi(q*T)-psi(T)
rough=[1]+[u for u in range(q,W) if all(u%d for d in range(2,int(u**.5)+1))]
M=sum(max(0,psi(W*T//u)-psi(T)) for u in rough)
print(f"exact y=61 T={T} W={W}: |A|={A} M(WT)={M} ratio={q*T*M/(W*T*A):.9f}")
