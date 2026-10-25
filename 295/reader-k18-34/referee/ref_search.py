"""Referee's own re-implementation of the pruned DFS described in proofs.md §1-§3
(written from the lemma statements, not from his code). Integer cross-multiplication
only. Modes: first-witness / enumerate-all; prime prune on/off; quadratic prune on/off.
"""
import sys, math, time, json
from functools import lru_cache

def gcd(a,b): return math.gcd(a,b)

@lru_cache(maxsize=None)
def H(d,t):
    n,m = 0,1
    for j in range(t):
        x = d+j
        n,m = n*x+m, m*x
        g = gcd(n,m); n//=g; m//=g
    return n,m

def geq(n,m,a,b):  # n/m >= a/b
    return n*b >= a*m

def add_units(n,m,xs):
    for x in xs:
        n,m = n*x+m, m*x
    g=gcd(n,m); return n//g, m//g

def forced_bound(d,t,forced):
    """max sum of reciprocals of t distinct integers >= d that contain every element of
    `forced` (a set of distinct integers >= d, |forced|<=t)."""
    k = len(forced)
    assert k <= t and all(f >= d for f in forced)
    rest = []
    x = d
    while len(rest) < t-k:
        if x not in forced: rest.append(x)
        x += 1
    # rest is a run of consecutive integers except possibly skipping forced elements
    n,m = 0,1
    return add_units(n,m, list(forced)+rest)

def small_primes(n):
    out=[]; p=2
    while p*p<=n:
        if n%p==0:
            out.append(p)
            while n%p==0: n//=p
        p += 1 if p==2 else 2
    if n>1: out.append(n)
    return out

class S:
    def __init__(self, prime=True, quad=True, enum_all=False, memo=True, audit_two=False):
        self.prime=prime; self.quad=quad; self.enum_all=enum_all; self.use_memo=memo and not enum_all
        self.audit_two=audit_two
        self.c=dict(nodes=0,two_nodes=0,two_prunes=0,two_candidates=0,pprunes=0,hprunes=0,mhits=0,
                    audit_two_solutions_in_pruned=0, two_full_candidates=0)
        self.failed=set(); self.sols=[]

    def prime_obstruct(self,d,t,a,b,primes):
        for p in primes:
            if b % p: continue
            M=1; v=b
            while v % p == 0: M*=p; v//=p
            q1 = -(-d//M)*M; q2 = q1+M
            n,m = forced_bound(d,t,(q1,q2)) if t>=2 else (0,1)
            if t>=2 and geq(n,m,a,b): continue      # >=2 multiples of p^e still possible
            c = (v*pow(a,-1,p)) % p                 # requires p∤a (a/b reduced)
            r = M*c; mod = M*p
            q = r if r >= d else r + (-(-(d-r)//mod))*mod
            assert q >= d and q % mod == r and q-mod < d
            n,m = forced_bound(d,t,(q,))
            if not geq(n,m,a,b): return True
        return False

    def two(self,d,a,b,prefix):
        self.c['two_nodes']+=1
        lo = max(d, b//a+1)
        hi_full = (2*b-1)//a          # x<y  =>  a/b < 2/x  =>  x < 2b/a
        hi = hi_full
        if self.quad and a*a > 4*b:
            Dl = a*a-4*b; s = math.isqrt(Dl)
            if s*s < Dl: s += 1
            hi = min(hi, (a-s)//2)
        found=[]
        if hi < lo:
            self.c['two_prunes']+=1
            if self.audit_two:
                for x in range(lo, hi_full+1):
                    self.c['two_full_candidates']+=1
                    y,rm = divmod(b*x, a*x-b)
                    if rm==0 and y>x: self.c['audit_two_solutions_in_pruned']+=1
            return []
        for x in range(lo, hi+1):
            self.c['two_candidates']+=1
            y,rm = divmod(b*x, a*x-b)
            if rm==0 and y>x:
                found.append((x,y))
                if not self.enum_all: return found
        if self.audit_two and self.quad:
            for x in range(hi+1, hi_full+1):
                y,rm = divmod(b*x, a*x-b)
                if rm==0 and y>x: self.c['audit_two_solutions_in_pruned']+=1
        return found

    def dfs(self,d,t,a,b,primes,prefix):
        self.c['nodes']+=1
        if a<=0: return False
        if t==1:
            if a==1 and b>=d:
                self.sols.append(prefix+(b,)); return not self.enum_all
            return False
        if t==2:
            f=self.two(d,a,b,prefix)
            for xy in f: self.sols.append(prefix+xy)
            return bool(f) and not self.enum_all
        h=H(d,t)
        if not geq(h[0],h[1],a,b):
            self.c['hprunes']+=1; return False
        key=(a,b,d,t)
        if self.use_memo and key in self.failed:
            self.c['mhits']+=1; return False
        if self.prime and self.prime_obstruct(d,t,a,b,primes):
            self.c['pprunes']+=1; return False
        lo=max(d,b//a+1)
        # largest x with H(x,t) >= a/b, x <= t*b//a
        L,R = lo-1, (t*b)//a
        while L<R:
            mid=(L+R+1)//2
            hn,hm=H(mid,t)
            if geq(hn,hm,a,b): L=mid
            else: R=mid-1
        nsol=len(self.sols)
        for x in range(lo,L+1):
            na=a*x-b; nb=b*x; g=gcd(na,nb); na//=g; nb//=g
            np_ = primes | frozenset(small_primes(x)) if self.prime else primes
            if self.dfs(x+1,t-1,na,nb,np_,prefix+(x,)): return True
        if self.use_memo and len(self.sols)==nsol and len(self.failed)<200000: self.failed.add(key)
        return False

def run(N,t,**kw):
    s=S(**kw); t0=time.time()
    r=s.dfs(N,t,1,1,frozenset(),())
    return s, r, time.time()-t0

if __name__=='__main__':
    N=int(sys.argv[1]); t=int(sys.argv[2])
    kw=dict(prime='noprime' not in sys.argv, quad='noquad' not in sys.argv,
            enum_all='all' in sys.argv, audit_two='audit' in sys.argv, memo='nomemo' not in sys.argv)
    s,r,el=run(N,t,**kw)
    print(json.dumps(dict(N=N,t=t,kw=kw,witness=r,nsols=len(s.sols),first=list(s.sols[0]) if s.sols else None,
                          counters=s.c,failed=len(s.failed),sec=round(el,1))))
