# Positive control: exact restricted order on actual integer sets (0/1 knapsack, min #distinct summands),
# compared with the model formula used in census.c.
import numpy as np, sys
INF=10**6
def min_distinct(A, N):
    c=np.full(N+1, INF, dtype=np.int64); c[0]=0
    for a in sorted(A):
        if a>N: break
        old=c.copy()
        np.minimum(c[a:], old[:N+1-a]+1, out=c[a:])
    return c
def model_order(M, D, E):
    T=sorted(set(D)|set(E)); dist=[-1]*M; dist[0]=0; q=[0]
    for u in q:
        for k in T:
            v=(u+k)%M
            if dist[v]<0: dist[v]=dist[u]+1; q.append(v)
    assert min(dist)>=0
    return max(min(1+dist[(r-d)%M] for d in D) for r in range(M))
def test(name, M, D, E, N):
    A=[n for n in range(1,N+1) if n%M in D]
    for e in E:
        k=0
        while True:
            v=M*(3**k)+e     # lacunary members of class e (powers of 3 scale)
            if v>N: break
            A.append(v); k+=1
    c=min_distinct(set(A), N)
    window=c[N//2:]
    print(f"{name}: M={M} D={D} E={E} N={N}: exact max over [N/2,N] = {window.max()}, model = {model_order(M,D,E)}, "
          f"floor bound = {2*M//len(D)-1}, ceil bound = {-(-2*M//len(D))-1}")
N=int(sys.argv[1]) if len(sys.argv)>1 else 30000
test("0,1 mod 6", 6, [0,1], [], N)
test("0,1 mod 7", 7, [0,1], [], N)
test("{0} + sparse 1 mod 5", 5, [0], [1], N)
test("{1} + sparse 0 mod 6", 6, [1], [0], N)
test("{0,2} + sparse 1 mod 8", 8, [0,2], [1], N)
test("{0,1,3} mod 7", 7, [0,1,3], [], N)
test("{0,1,2} mod 12 + sparse 4", 12, [0,1,2], [4], N)
