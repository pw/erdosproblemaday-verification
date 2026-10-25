import itertools
def aps(N): return [(a,a+d,a+2*d,a+3*d) for a in range(N) for d in range(1,N) if a+3*d<N]
for N in range(4,8):
    A=aps(N)
    def good(c): return all(len({c[i] for i in ap})>=3 for ap in A)
    H=next(q for q in range(1,N+1) if any(good(c) for c in itertools.product(range(q),repeat=N)))
    hE=max(k for k in range(2,N+1) if all(not good(c) for c in itertools.product(range(k),repeat=N) if len(set(c))==k))
    # literal reading: some pair of distinct nonempty parts whose union contains an AP
    def bad_literal(c,k): return any(set(c[i] for i in ap)<= {x,y} for ap in A for x in range(k) for y in range(k) if x!=y)
    hL=max(k for k in range(2,N+1) if all(bad_literal(c,k) for c in itertools.product(range(k),repeat=N) if len(set(c))==k))
    print(f"N={N}: H={H}  h_E(at-most-two)={hE}  h_E(literal distinct nonempty)={hL}  H==h_E+1: {H==hE+1 and hE==hL}")
