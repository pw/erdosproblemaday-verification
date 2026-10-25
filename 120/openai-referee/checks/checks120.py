#!/usr/bin/env python3
"""Decorrelated finite checks of the combinatorial core of OpenAI's geometric Erdős-similarity construction (family 084).
Written from the paper's definitions only (no shared code with the paper or the Lean). Each check prints PASS/FAIL."""
import math, random, itertools, sys, resource
resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))  # hard 4 GB cap: an earlier run of this script reached 20.6 GB RSS and was SIGTERMed by earlyoom (03:55Z)
from fractions import Fraction as Fr
random.seed(20261014)
fails=0
def check(name, ok, detail=""):
    global fails
    print(("PASS " if ok else "FAIL ")+name+(("  :: "+detail) if detail else ""))
    if not ok: fails+=1

# ---- (2.3) the measure sum: 12 * sum_k p_k max(1,2^k), p_k = eta 4^{-|k|}/64 ---------------------------------
def sum23(terms=200):
    s=Fr(0)
    for k in range(-terms,terms+1):
        pk=Fr(1,64)/Fr(4)**abs(k)
        s+=12*pk*max(1,Fr(2)**k)
    return s
s=sum23(); check("(2.3) 12*sum p_k max(1,2^k) -> 7/16 (as a multiple of eta)", abs(float(s)-7/16)<1e-30, f"{float(s):.17f} vs {7/16}")
check("(2.3) < eta", s<1)

# ---- grids: c, N_b, (3.1), monotone, nesting; Lemma 3.3 inequality 1/N_b < (1-q) q^b -------------------------
def N_b(q,b):
    c=4/(1-q); x=c*q**(-b); return 2**math.ceil(math.log2(x))
for q in [0.03,0.1,1/3,0.5,2/3,0.9,0.97,0.999]:
    c=4/(1-q)
    ok31=all(c*q**(-b) <= N_b(q,b) < 2*c*q**(-b) for b in range(1,60))
    okmono=all(N_b(q,b+1)>=N_b(q,b) for b in range(1,60))
    oksep=all(1/N_b(q,b) < (1-q)*q**b for b in range(1,60))
    check(f"(3.1)+monotone+Lemma3.3 cell-width inequality, q={q}", ok31 and okmono and oksep)

# ---- windows: lay out preorder windows, check Lemma 3.1 b*_e - a_e + 1 <= 2 r_h, and a_e = b' + g + 1 ----------
def layout(M,d,g,r0,n0=1):
    # heights: leaves 0, root d. edges leaving a vertex of height h have window length r_h
    r={1:r0}; sigma={1:M*r0+(M-1)*g}
    for h in range(2,d+1):
        r[h]=max(r0, g+sigma[h-1]); sigma[h]=M*(r[h]+g+sigma[h-1])+(M-1)*g
    edges=[]  # (id, height_of_parent, parent_id, child_index)
    nxt=[n0]
    def rec(parent_h, parent_id):
        # list children edges in preorder: edge then its subtree
        for i in range(1,M+1):
            eid=len(edges); edges.append({'h':parent_h,'parent':parent_id,'i':i})
            e=edges[eid]
            e['a']=nxt[0]; e['b']=e['a']+r[parent_h]-1; nxt[0]=e['b']+1+g
            if parent_h-1>=1:
                start=len(edges); rec(parent_h-1, eid); e['sub']=(start,len(edges))
            else: e['sub']=(eid+1,eid+1)
    rec(d, -1)
    for e in edges:
        s,t=e['sub']; e['bstar']=max([e['b']]+[edges[j]['b'] for j in range(s,t)])
    return r,sigma,edges
for M in [2,3,4]:
    for d in [1,2,3]:
        for g in [1,3]:
            for r0 in [1,5]:
                r,sigma,edges=layout(M,d,g,r0)
                K=sum(M**l for l in range(1,d+1))
                okK=(len(edges)==K)
                ok31=all(e['bstar']-e['a']+1 <= 2*r[e['h']] for e in edges)
                # gap convention: consecutive windows in preorder have a_{e} = b_{prev} + g + 1
                okgap=all(edges[j]['a']==edges[j-1]['b']+g+1 for j in range(1,len(edges)))
                # endpoints increase along preorder; and lemma 3.1 equality form for h>=2: span = r_h+g+sigma_{h-1}
                okinc=all(edges[j]['b']>edges[j-1]['b'] for j in range(1,len(edges)))
                okspan=all((e['bstar']-e['a']+1)==(r[e['h']]+g+sigma[e['h']-1] if e['h']>=2 else r[1]) for e in edges)
                # sigma_h equals the actual span of a height-h subtree's windows incl gaps
                oksig=True
                for e in edges:
                    s,t=e['sub']
                    if t>s:
                        span=edges[t-1]['b']-edges[s]['a']+1  # hmm: windows of subtree rooted at child = edges s..t-1
                        oksig = oksig and (span==sigma[e['h']-1])
                check(f"Lemma 3.1 + preorder window bookkeeping M={M} d={d} g={g} r0={r0} (K={K})", okK and ok31 and okgap and okinc and okspan and oksig)

# ---- (4.3) no-default probability, Lemma 3.2 density bound, (5.5) existence --------------------------------------
def nodefault_exact(M,d,trials=200000):
    cnt=0
    for _ in range(trials):
        ok=True
        for _ in range(d):
            if all(random.getrandbits(1)==0 for _ in range(M-1)): ok=False; break
        cnt+=ok
    return cnt/trials
for M,d in [(2,3),(3,2),(4,4)]:
    est=nodefault_exact(M,d); ex=(1-2**(1-M))**d
    check(f"(4.3) P(no default) = (1-2^(1-M))^d  M={M} d={d}", abs(est-ex)<4*math.sqrt(ex*(1-ex)/200000)+1e-9, f"MC {est:.4f} exact {ex:.4f}")
# (5.5): for q, p pick smallest M with p(M-1)/2 > 2 log(1/q); in LOG space find r* with log D - alpha r < log p for all r >= r* (search to 10^6)
def logD(M,q,r):
    c=4/(1-q)
    L=2*r*math.log(1/q)                       # log q^{-2r}
    log_inner = L + math.log(2*c) + math.log1p(math.exp(-L)/(2*c))   # log(1+2c q^{-2r})
    log_main  = math.log(2*(M-1)*r) + log_inner                      # log(2(M-1) r (1+2c q^{-2r}))
    return log_main + math.log1p(4*math.exp(-log_main))              # log(4 + main)
for q,p in [(0.5,0.1),(0.5,0.5),(0.9,0.2),(1/3,0.05),(0.99,0.3)]:
    M=2
    while p*(M-1)/2 <= 2*math.log(1/q): M+=1
    alpha=p*(M-1)/2; slack=alpha-2*math.log(1/q)
    # f(r)=logD - alpha r is eventually decreasing (slope -> -slack <0); find first r with f(r)<log p and f decreasing afterwards
    rstar=None; prev=None
    for r in range(1,10**6):
        f=logD(M,q,r)-alpha*r
        if f<math.log(p) and prev is not None and f<prev and r>50:  # decreasing and below
            rstar=r; break
        prev=f
    # verify monotone decrease beyond r* on a sample
    okdec = rstar is not None and all(logD(M,q,r+1)-alpha*(r+1) < logD(M,q,r)-alpha*r for r in range(rstar, rstar+2000))
    check(f"(5.5) r* exists q={q} p={p} (M={M}, alpha={alpha:.4f} > 2log(1/q)={2*math.log(1/q):.4f}, slack={slack:.4f})", okdec, f"r*={rstar}")
# ---- Toy construction (EXACT rational arithmetic): Monte Carlo of Lemma 4.3 + Lemma 4.2 implication + Lemma 4.1 density --------
def N_b_exact(q,b):
    # smallest power of two >= c q^{-b}, c=4/(1-q), exact
    x=Fr(4)/(1-q)/q**b; N=1
    while N<x: N*=2
    return N
def key_exact(N,z): return math.floor(N*(z-math.floor(z)))
def auto_g(q,M,d):
    K=sum(M**l for l in range(1,d+1)); c=Fr(4)/(1-q); g=1
    while 4*K*c*q**(g+1) >= Fr(1,2): g+=1
    return g
def build_instance(q,M,d,g,r0):
    n0=1
    while 2*q**n0>Fr(1,4): n0+=1
    r,sigma,edges=layout(M,d,g,r0,n0=n0)
    for e in edges: e['N']=N_b_exact(q,e['b'])
    return r,edges,n0
def children_of(edges,parent): return [j for j,e in enumerate(edges) if e['parent']==parent]
def route(edges,sel,term,z,M,start_parent=-1):
    parent=start_parent
    while True:
        kids=children_of(edges,parent)
        if not kids:   # start_parent itself is a leaf edge
            L=parent; k=key_exact(edges[L]['N'],z)
            return L, term.setdefault((L,k), 1 if random.random()<P else 0)
        chosen=None
        for e in kids[:-1]:
            k=key_exact(edges[e]['N'],z)
            bit=sel.setdefault((e,k), random.getrandbits(1))
            if bit==1: chosen=e; break
        if chosen is None: chosen=kids[-1]
        parent=chosen
        if not children_of(edges,chosen):
            L=chosen; k=key_exact(edges[L]['N'],z)
            return L, term.setdefault((L,k), 1 if random.random()<P else 0)
def rand_fr(bits=60): return Fr(random.getrandbits(bits), 2**bits)
def run_toy(q,M,d,r0,p,samples,want_h=None):
    global P; P=p
    g=auto_g(q,M,d)
    r,edges,n0=build_instance(q,M,d,g,r0)
    def stable(x):
        for jj in range(1,len(edges)):
            bprev=edges[jj-1]['b']; Nb=N_b_exact(q,bprev); a=edges[jj]['a']
            lo=x; hi=x+2*q**a
            gmin=math.floor(lo*Nb)+1
            if Fr(gmin,Nb)<=hi: return False
        return True
    x=None; tries=0
    while x is None and tries<100000:
        tries+=1; cand=rand_fr()
        if stable(cand): x=cand
    assert x is not None, "no stable center found"
    t=1+rand_fr(100)
    while True:
        exposed={}
        for jj,e in enumerate(edges):
            if e['i']<M: exposed[(jj,key_exact(e['N'],x))]=random.getrandbits(1)
        parent=-1; U=None
        while True:
            kids=children_of(edges,parent)
            if not kids: break
            chosen=None
            for e in kids[:-1]:
                if exposed[(e,key_exact(edges[e]['N'],x))]==1: chosen=e; break
            if chosen is None: U=parent; break
            parent=chosen
        if U is not None:
            kk=children_of(edges,U); hU=edges[kk[0]]['h']
            if want_h is None or hU==want_h: break
    kids=children_of(edges,U); h=edges[kids[0]]['h']; rr=r[h]; nondef=kids[:-1]
    fail=0; viol=0; dens=0; densN=0
    for s_ in range(samples):
        sel=dict(exposed); term={}
        allfail=True
        for ei in nondef:
            e=edges[ei]
            for n in range(e['a'],e['b']+1):
                y=x+t*q**n
                bit=sel.setdefault((ei,key_exact(e['N'],y)), random.getrandbits(1))
                Q=0
                if bit==1:
                    L,inB=route(edges,sel,term,y,M,start_parent=ei); Q=inB
                if Q==1:
                    allfail=False
                    L2,inB2=route(edges,sel,term,y,M,start_parent=-1)
                    if inB2!=1: viol+=1
        fail+=allfail
        if s_<500:
            z=rand_fr(); L,inB=route(edges,sel,term,z,M); dens+=inB; densN+=1
    est=fail/samples; ex=(1-p/2)**((M-1)*rr); sd=math.sqrt(ex*(1-ex)/samples)
    return est,ex,sd,viol,dens/densN,rr,h,len(edges),g,tries
for (q,M,d,r0,p,wh) in [(Fr(1,2),3,1,2,0.5,None),(Fr(1,3),2,1,3,0.5,None),(Fr(7,10),4,1,1,0.4,None),(Fr(1,2),3,2,2,0.5,1)]:
    est,ex,sd,viol,dens,rr,h,K,g,tries=run_toy(q,M,d,r0,p,1000,want_h=wh)
    check(f"Lemma 4.3 MC q={q} M={M} d={d} g={g} r0={r0} p={p} (U height {h}, r={rr}, K={K}, stable after {tries} draws)", abs(est-ex)<=4*sd+1e-9, f"MC {est:.4f} exact {ex:.4f} (4sd={4*sd:.4f})")
    check(f"Lemma 4.2 implication Q=1 => y in B, same instance", viol==0, f"violations {viol}")
    check(f"Lemma 4.1 density ~ p, same instance", abs(dens-p)<0.05, f"{dens:.3f} vs {p}")

# ---- Lemma 5.1 breakpoints: count distinct key vectors at resolution b* over t in [1,2] vs D_{M,q}(r) ------------------
for (q,M,d,r0) in [(Fr(1,2),3,2,2),(Fr(1,3),2,2,3)]:
    g=auto_g(q,M,d); r,edges,n0=build_instance(q,M,d,g,r0)
    for parent in [-1]+[j for j,e in enumerate(edges) if children_of(edges,j)]:
        kids=children_of(edges,parent); h=edges[kids[0]]['h']; rr=r[h]
        x=rand_fr()
        pts=[(ei,n) for ei in kids[:-1] for n in range(edges[ei]['a'],edges[ei]['b']+1)]
        # breakpoints: t where x+t q^n hits a lattice point of Gamma_{b*}; count them exactly
        # count breakpoints arithmetically per pair (distinct values <= the sum); never materialise the set (the root vertex has ~q^{-2r} of them)
        total=0
        for ei,n in pts:
            Nb=N_b_exact(q,edges[ei]['bstar'])
            lo=x+q**n; hi=x+2*q**n
            k0=math.ceil(lo*Nb); k1=math.floor(hi*Nb)
            cnt=max(0,k1-k0+1); total+=cnt
            if not cnt<=1+q**n*Nb: check("(5.3) per-pair count",False)
        T=2*(total+2)  # recorded values + endpoints 1,2, doubled for midpoints (upper bound form)
        Dv=float(4+2*(M-1)*rr*(1+2*(Fr(4)/(1-q))*q**(-2*rr)))
        check(f"Lemma 5.1 |T| <= D_(M,q)(r)  q={q} vertex-height {h} r={rr}", T<=Dv, f"|T|<={T} D={Dv:.1f}")
print("FAILS:",fails)
