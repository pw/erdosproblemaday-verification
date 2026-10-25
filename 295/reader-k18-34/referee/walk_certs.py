import math, sys
sys.path.insert(0,'/tmp/erdos295-referee')
from ref_search import S, H, geq, small_primes, forced_bound
certs = {
 'Bae34 (N=18)': [18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,43,44,45,46,48,50,52,54,63,275,14143068,10457416992],
 'ours35 (N=18)': [18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,42,43,44,45,48,50,52,54,63,640,337280,1735650,68479214496],
 'ours k17=32': [17,18,19,20,21,22,23,24,25,26,27,28,29,30,32,33,34,35,36,38,39,42,43,44,45,48,50,52,54,63,1735650,68479214496],
 'A192881 a16=30': [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,32,33,34,36,38,39,40,42,43,44,50,52,54,1735650,68479214496],
 'a15=28': [15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,31,32,33,35,36,38,39,40,44,48,52,33599412,130917600],
 'a13=25': [13,14,15,16,17,18,19,20,21,23,24,25,26,27,28,29,30,32,35,40,41,44,46,58449600,6548068942272],
 'a11=21': [11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,561,71820,1315600],
}
def vp(n,p):
    e=0
    while n%p==0: n//=p; e+=1
    return e
s=S()
shown=0
for name,C in certs.items():
    N=C[0]; k=len(C)
    a,b=1,1; d=N; fired=[]; uniq_examples=[]
    for i in range(k):
        t=k-i; rem=C[i:]
        # the state before choosing C[i]: residual a/b, t terms, lower bound d
        if t>=3:
            hn,hm=H(d,t)
            if not geq(hn,hm,a,b): fired.append(('harmonic',i))
            lo=max(d,b//a+1)
            if not (lo<=C[i]<= (t*b)//a): fired.append(('interval',i))
            hn,hm=H(C[i],t)
            if not geq(hn,hm,a,b): fired.append(('Hx',i))
            primes=frozenset(p for x in C[:i] for p in small_primes(x))
            if s.prime_obstruct(d,t,a,b,primes): fired.append(('prime',i))
        if t==2:
            x=C[i]
            if a*a>4*b:
                Dl=a*a-4*b; sq=math.isqrt(Dl); sq+=(sq*sq<Dl)
                if x>(a-sq)//2 or (a-sq)//2 < max(d,b//a+1): fired.append(('quad',i))
                tightq = (x==(a-sq)//2)
            else: tightq=None
            primes=frozenset(p for x_ in C[:i] for p in small_primes(x_))
            if s.prime_obstruct(d,t,a,b,primes): fired.append(('prime2',i))
        # p-adic lemma on the real remaining set
        if b>1:
            for p in small_primes(b) if b<10**30 else [p for p in set(q for x in C[:i] for q in small_primes(x)) if b%p==0]:
                e=vp(b,p); M=p**e
                mult=[x for x in rem if x%M==0]
                if not mult: fired.append(('NO MULTIPLE',i,p,e))
                elif len(mult)==1:
                    x=mult[0]; v=b//M; c=(v*pow(a,-1,p))%p
                    ok = vp(x,p)==e and x%(M*p)==(M*c)%(M*p)
                    if not ok: fired.append(('CONGRUENCE FAIL',i,p,e,x))
                    if e>=2 and len(uniq_examples)<3: uniq_examples.append((t,f'{p}^{e}',x,f'{M*c} mod {M*p}'))
        # step
        x=C[i]; a,b=a*x-b,b*x; g=math.gcd(a,b); a//=g; b//=g; d=x+1
        if a==0: break
    print(f"{name}: k={k}, final residual {a}/{b}; prune/lemma violations along the path: {fired or 'none'}"
          + (f"; quadratic bound at t=2 tight: {tightq}" ))
    print("    unique-multiple examples (t_remaining, p^e, x, predicted class):", uniq_examples)
