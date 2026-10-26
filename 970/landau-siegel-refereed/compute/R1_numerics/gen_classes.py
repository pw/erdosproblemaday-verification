"""Sanity test: generalised Frobenius divisibility for ALL four classes (my extension, not in the paper).
Predicted lower bound for v_p(Nm Delta)/4:
 id:        sum floor(a1/p)+floor(a2/p)+floor(a3/p)
 sigma:     a1 (needs p>H) + a2
 sigma*tau: a1 (needs p>H) + a3
 tau:       a2 + a3
Negative control: the paper's first-coordinate bound sum floor(a1/p) for tau-class primes (should fail sometimes)."""
import sys, math
sys.path.insert(0, '.')
from lemma7 import run, mk, sig, st, mulmat, int_det, vp, legendre
d, N, H = map(int, sys.argv[1:4])
mul, th, ret, M = run(d, N, H)
def pw(x,k):
    r=(1,0,0,0)
    for _ in range(k): r=mul(r,x)
    return r
rows = [[mul(mul(pw(t,a[0]), pw(sig(t),a[1])), pw(st(t),a[2])) for t in th] for a in ret]
big = [[0]*(4*M) for _ in range(4*M)]
for i in range(M):
    for j in range(M):
        m = mulmat(d, rows[i][j])
        for r in range(4):
            for c in range(4):
                big[4*i+r][4*j+c] = m[r][c]
nm = int_det(big)
print(f"d={d} N={N} H={H} M={M} max a=({max(a[0] for a in ret)},{max(a[1] for a in ret)},{max(a[2] for a in ret)}) Nm!=0:{nm!=0}")
bad = 0
for p in [3,5,7,11,13,17,19,23]:
    if abs(d) % p == 0: continue
    chi = legendre(d,p); two = legendre(2,p)
    cls = {(-1,1):'sigma',(-1,-1):'sigma*tau',(1,1):'id',(1,-1):'tau'}[(chi,two)]
    f = lambda x: x//p
    g1 = sum(f(a[0]) for a in ret) if (cls=='id' or p>H) else 0
    if cls=='id': E = sum(f(a[0])+f(a[1])+f(a[2]) for a in ret)
    elif cls=='sigma': E = (g1 if p>H else 0) + sum(f(a[1]) for a in ret)
    elif cls=='sigma*tau': E = (g1 if p>H else 0) + sum(f(a[2]) for a in ret)
    else: E = sum(f(a[1])+f(a[2]) for a in ret)
    paper = sum(f(a[0]) for a in ret)
    v = vp(nm,p)
    ok = v >= 4*E
    bad += (not ok)
    print(f"  p={p:2d} class={cls:9s} v_p={v:3d} 4*E_gen={4*E:3d} {'OK' if ok else 'FAIL'} | paper-form 4*sum floor(a1/p)={4*paper:3d} {'holds' if v>=4*paper else 'fails'}")
print("generalised-bound failures:", bad)
