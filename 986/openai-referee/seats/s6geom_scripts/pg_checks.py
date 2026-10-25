import itertools, random, sys
import numpy as np

def proj_points(q, n):
    """normalized representatives of PG(n-1,q) as tuples of length n (first nonzero coord = 1)."""
    pts=[]
    for v in itertools.product(range(q), repeat=n):
        if all(c==0 for c in v): continue
        f=next(c for c in v if c!=0)
        if f==1: pts.append(v)
    return pts

def dot(a,b,q): return sum(x*y for x,y in zip(a,b))%q

def check_incidence(q,j):
    n=j+1
    P=proj_points(q,n); H=P  # dual points same reps
    M=np.array([[1 if dot(a,b,q)==0 else 0 for b in H] for a in P],dtype=np.int64)
    Q=lambda r: sum(q**i for i in range(r+1)) if r>=0 else 0
    assert len(P)==Q(j)
    MMt=M@M.T
    expect=q**(j-1)*np.eye(len(P),dtype=np.int64)+Q(j-2)*np.ones((len(P),len(P)),dtype=np.int64)
    assert (MMt==expect).all(), "MM^T identity fails"
    pj=Q(j-1)/Q(j)
    rng=np.random.default_rng(1)
    for t in range(20):
        w=rng.normal(size=len(P))
        lhs=((M.T@w - pj*w.sum())**2).sum()
        rhs=q**(j-1)*((w**2).sum()-w.sum()**2/Q(j))
        assert abs(lhs-rhs)<1e-6*max(1,abs(rhs)), (lhs,rhs)
        # mixing bound on random sets
        S=rng.random(len(P))<rng.random(); T=rng.random(len(P))<rng.random()
        e=int(S.astype(int)@M@T.astype(int))
        assert abs(e-pj*S.sum()*T.sum())<=q**((j-1)/2)*np.sqrt(S.sum()*T.sum())+1e-9
    print(f"incidence identity + mixing OK q={q} j={j}")

def check_flag_graph(q,d,N,trials,rng):
    n=d+1
    P=proj_points(q,n)
    flags=[(a,b) for a in P for b in P if dot(a,b,q)==0]
    import networkx as nx
    worst=0
    for t in range(trials):
        st=[flags[rng.randrange(len(flags))] for _ in range(N)]
        G=nx.Graph(); G.add_nodes_from(range(N))
        for i in range(N):
            for k in range(i+1,N):
                ai,bi=st[i]; ak,bk=st[k]
                if dot(ai,bk,q)==0 and dot(ak,bi,q)!=0: G.add_edge(i,k)
        w=max(len(c) for c in nx.find_cliques(G))
        worst=max(worst,w)
        assert w<=d, f"clique {w} > d={d}"
        # consistency reversal symmetry on random subsets that are independent sets
    print(f"flag graph q={q} d={d} N={N}: max clique over {trials} trials = {worst} (<= d)")

def check_rect(q,d):
    n=d+1
    P=proj_points(q,n)
    Q=lambda r: sum(q**i for i in range(r+1)) if r>=0 else 0
    # random subspaces U of dual space given by spanning vectors
    rng=random.Random(2)
    for r in range(1,d+1):
        for t in range(3):
            while True:
                B=[tuple(rng.randrange(q) for _ in range(n)) for _ in range(r)]
                # rank check
                import sympy
                Mx=sympy.Matrix(B)
                if Mx.rank(iszerofunc=lambda x: x % q == 0)==r: break
            # points of U (dual): normalized vectors in span
            span=set()
            for coeffs in itertools.product(range(q),repeat=r):
                v=tuple(sum(c*b[i] for c,b in zip(coeffs,B))%q for i in range(n))
                if any(v):
                    f=next(c for c in v if c); inv=pow(f,q-2,q)
                    span.add(tuple(x*inv%q for x in v))
            Uperp=[a for a in P if all(dot(a,b,q)==0 for b in B)]
            assert len(span)==Q(r-1) and len(Uperp)==Q(d-r), (len(span),Q(r-1),len(Uperp),Q(d-r))
            assert len(span)*len(Uperp)<=4*q**(d-1)
    print(f"rectangle sizes Q_(r-1)Q_(d-r) <= 4q^(d-1) OK q={q} d={d}")

if __name__=="__main__":
    for q,j in [(3,2),(5,2),(7,2),(3,3),(5,3),(3,4)]:
        check_incidence(q,j)
    rng=random.Random(5)
    check_flag_graph(3,2,60,30,rng)
    check_flag_graph(2,3,60,30,rng)
    check_flag_graph(3,3,80,20,rng)
    check_rect(5,3); check_rect(3,4)
