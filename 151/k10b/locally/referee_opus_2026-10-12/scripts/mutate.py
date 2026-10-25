# Mutation tests on locally.py: does the M8 / Q3 output change when the search is deliberately broken?
import sys, io, contextlib, networkx as nx
sys.path.insert(0,"/home/exedev/MathDyad/erdos151/locally"); import locally
def run(X, nm, patch):
    S=locally.Search(locally.make_X(X), nm); patch(S)
    with contextlib.redirect_stdout(io.StringIO()): S.run()
    return sorted(G.number_of_nodes() for G in S.found)
def over_quotient(S):           # add a non-automorphism to the quotient set (i -> 3i mod 8 for M8; any swap for Q3)
    extra = tuple((3*i)%S.k for i in range(S.k)) if S.k==8 else None
    S.auts = S.auts + [extra]
def no_existing(S):              # never reuse an existing undecided vertex in a free slot
    of=S.fill
    def f(adj, non, closed, v, K, pos, slots, i, assign, U, newcount): return of(adj, non, closed, v, K, pos, slots, i, assign, [], newcount)
    S.fill=f
def drop_last_embedding(S):      # lose one Aut-orbit representative whenever there are >= 2
    oe=S.embeddings
    def e(K, adj, non):
        r=oe(K, adj, non); return r[:-1] if len(r)>=2 else r
    S.embeddings=e
for X in ["M8","Q3"]:
    print(X, "unmutated:", run(X, 41, lambda S: None), flush=True)
    for name,p in [("over_quotient",over_quotient),("no_existing",no_existing),("drop_last_embedding",drop_last_embedding)]:
        print(X, name, ":", run(X, 41, p), flush=True)
