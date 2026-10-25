import math, random, sys, itertools
sys.path.insert(0, '/tmp/erdos295-referee')
from ref_search import S, forced_bound, geq, small_primes, run

# ---------- §3: two-term tail quadratic condition ----------
B = int(sys.argv[1]) if len(sys.argv)>1 else 600
nsol=0; tight=0; bad=0; iffbad=0; boundbad=0; quad_cases=0; at_bound=0
for b in range(1, B+1):
    for a in range(1, 2*b):
        if math.gcd(a,b)!=1: continue
        lo = b//a+1; hi=(2*b-1)//a
        rootfloor=None
        if a*a>4*b:
            Dl=a*a-4*b; s=math.isqrt(Dl); s+= (s*s<Dl); rootfloor=(a-s)//2
        for x in range(max(lo,1), hi+1):
            den=a*x-b
            if den<=0: continue
            y,rm=divmod(b*x,den)
            is_sol = (rm==0 and y>x)
            g=math.gcd(x,b)
            div = (g*g) % den == 0
            # equivalence: y integer  <=>  (ax-b) | g^2   (for x in the candidate range, y>x automatic since x<2b/a)
            if (rm==0) != div: iffbad+=1
            if is_sol:
                nsol+=1
                f=x*x-a*x+b
                if f<0: bad+=1
                if f==0: tight+=1
                if rootfloor is not None:
                    quad_cases+=1
                    if x>rootfloor: boundbad+=1
                    if x==rootfloor: at_bound+=1
print(f"§3: a/b with b<={B}, a<2b: {nsol} two-term solutions; f(x)<0 violations={bad}; "
      f"f(x)=0 (root exactly integral) cases={tight}; y-integral<=>(ax-b)|g^2 mismatches={iffbad}; "
      f"a^2>4b solutions={quad_cases}, of which x>(a-s)//2 (bound violated)={boundbad}, x==(a-s)//2 (bound tight)={at_bound}")

# ---------- §2: p-adic forced-denominator lemma on random sets ----------
random.seed(295)
def vp(n,p):
    e=0
    while n%p==0: n//=p; e+=1
    return e
checked=0; exactly_one=0; cong_bad=0; val_bad=0; none_bad=0; boundA_bad=0; boundB_bad=0; prune_false=0
ex_examples=[]
s=S()
for trial in range(20000):
    D=random.randint(2,40); t=random.randint(2,9)
    pool=list(range(D, D+random.choice([15,40,120])))
    # sprinkle in multiples of prime powers
    for _ in range(random.randint(0,3)):
        p=random.choice([2,3,5,7,11,13]); e=random.randint(1,4)
        pool.append((p**e)*random.randint(1,30)+0)
    pool=[x for x in set(pool) if x>=D]
    if len(pool)<t: continue
    Sset=sorted(random.sample(pool,t))
    num,den=0,1
    for x in Sset:
        num,den=num*x+den,den*x
    g=math.gcd(num,den); a,b=num//g,den//g
    for p in small_primes(b):
        e=vp(b,p); M=p**e
        mult=[x for x in Sset if x%M==0]
        checked+=1
        if not mult: none_bad+=1; continue
        q1=-(-D//M)*M; q2=q1+M
        if len(mult)>=2:
            n_,m_=forced_bound(D,t,(q1,q2))
            if not geq(n_,m_,a,b): boundA_bad+=1
        else:
            exactly_one+=1
            x=mult[0]
            if vp(x,p)!=e: val_bad+=1
            v=b//M; c=(v*pow(a,-1,p))%p
            if x % (M*p) != (M*c)%(M*p): cong_bad+=1
            r=M*c; mod=M*p; q = r if r>=D else r+(-(-(D-r)//mod))*mod
            n_,m_=forced_bound(D,t,(q,))
            if not geq(n_,m_,a,b): boundB_bad+=1
            if len(ex_examples)<6 and e>=2: ex_examples.append((Sset,a,b,p,e,x,c))
    primes=frozenset(p for x in Sset for p in small_primes(x))
    if s.prime_obstruct(D,t,a,b,primes): prune_false+=1
print(f"§2: {checked} (set, p^e||b) pairs; no-multiple violations={none_bad}; exactly-one cases={exactly_one}; "
      f"valuation!=e={val_bad}; congruence failures={cong_bad}; >=2-case bound violated={boundA_bad}; "
      f"exactly-one bound violated={boundB_bad}; prime_obstruct fired on a REAL set={prune_false}")
for ex in ex_examples[:4]:
    Sset,a,b,p,e,x,c=ex
    print(f"   example: S={Sset} sum={a}/{b}, p^e={p}^{e}||b, unique multiple x={x}=p^e*{x//p**e}, "
          f"predicted x ≡ {p**e*c} mod {p**(e+1)}: {x%(p**(e+1))}")
