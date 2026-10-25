# Battery of exact checks of Lemma 3.7 (memory identity) on toy instances.
import sys, time
from fractions import Fraction as Fr
import itertools
import field as F
from model import Toy
RAW = frozenset(); C0 = frozenset({0})
P4 = [5, 7, 17, 19]          # 7 | 19-5, 5 | 17-7  -> endpoint / pending hits occur
P5 = [5, 7, 17, 19, 29]      # 5 | 29-19 as well
P6 = [5, 7, 17, 19, 29, 31]
ID2 = [(0, 1)]; ID3 = [(0, 1, 2)]
results = []
def run(tag, **kw):
    t0 = time.time()
    toy = Toy(**kw)
    L = toy.lhs(); R = toy.rhs_full()
    ok = (L == R)
    results.append((tag, ok))
    print(f"[{'EQUAL' if ok else 'DIFFER'}] {tag}\n    paths={toy._npaths} stats={toy.stats} memo={len(toy.memo)} ({time.time()-t0:.1f}s)"
          f"\n    LHS = {F.fmt(L)}\n    RHS = {F.fmt(R)}\n    LHS ~ {F.approx(L):.10g}", flush=True)
    return toy, L, R
which = sys.argv[1] if len(sys.argv) > 1 else 'A'
if which == 'A':
    for (q, rho, th, ks) in [(Fr(1,2), Fr(9,10), 1, [1,1]), (Fr(1,4), Fr(3,4), 3, [2,3]),
                             (Fr(4,9), Fr(5,6), 2, [1,4]), (Fr(1,9), Fr(3,5), 1, [3,1])]:
        run(f"A raw N=2 P={P4} q={q} rho={rho} theta={th}/8 k={ks}",
            P=P4, J=1, ell=1, patterns=[RAW], N=2, q=q, rho=rho, theta_num=th, kseq=ks, seed=11)
if which == 'B':
    for (q, rho, th, ks, sd) in [(Fr(1,2), Fr(9,10), 1, [1,1], 21), (Fr(1,4), Fr(3,4), 3, [2,1], 22)]:
        run(f"B raw+cmp(C={{0}}) N=2 P={P5} q={q} rho={rho} theta={th}/8 k={ks} full Sym",
            P=P5, J=1, ell=1, patterns=[RAW, C0], N=2, q=q, rho=rho, theta_num=th, kseq=ks, seed=sd)
if which == 'C':
    for (q, rho, th, ks) in [(Fr(1,2), Fr(9,10), 1, [1,1,1,1]), (Fr(1,4), Fr(3,4), 3, [1,2,1,2]),
                             (Fr(4,9), Fr(5,6), 1, [2,1,3,1])]:
        run(f"C raw N=4 P={P4} q={q} rho={rho} theta={th}/8 k={ks} full Sym",
            P=P4, J=1, ell=1, patterns=[RAW], N=4, q=q, rho=rho, theta_num=th, kseq=ks, seed=31)
if which == 'D':
    for (seq, ks, sd) in [([0,1,0,0], [1,1,1,1], 41), ([1,0,0,1], [1,1,2,1], 42), ([0,0,1,0], [2,1,1,1], 43)]:
        run(f"D N=4 P={P5} patterns per edge={seq} (0=raw,1=cmp) identity perms q=1/2 rho=9/10 theta=1/8 k={ks}",
            P=P5, J=1, ell=1, patterns=[RAW, C0], N=4, q=Fr(1,2), rho=Fr(9,10), theta_num=1, kseq=ks, seed=sd,
            edge_patterns=[[x] for x in seq], edge_perms=[ID2]*4)
if which == 'E':
    run(f"E M=3 (J=2,l=1) N=2 P={P6} cmp C={{0}} on both edges (1 shared + 1 free), identity perms, q=1/2",
        P=P6, J=2, ell=1, patterns=[RAW, C0], N=2, q=Fr(1,2), rho=Fr(9,10), theta_num=1, kseq=[1,1], seed=51,
        edge_patterns=[[1],[1]], edge_perms=[ID3]*2)
    run(f"E M=3 (J=2,l=1) N=2 P={P5} raw+cmp both edges, identity perms, q=1/4",
        P=P5, J=2, ell=1, patterns=[RAW, C0], N=2, q=Fr(1,4), rho=Fr(3,4), theta_num=3, kseq=[1,2], seed=52,
        edge_perms=[ID3]*2)
C01 = frozenset({0, 1})
if which == 'F':
    run(f"F J=2,l=0 (M=2) N=2 P={P5} patterns raw(2 shared) + C={{0,1}} (2 free labels, may coincide), identity perms, q=1/2",
        P=P5, J=2, ell=0, patterns=[RAW, C01], N=2, q=Fr(1,2), rho=Fr(9,10), theta_num=1, kseq=[1,1], seed=61,
        edge_perms=[ID2]*2)
    run(f"F J=2,l=0 (M=2) N=4 P={P5} pattern seq [C01,raw,raw,C01], identity perms, q=1/4",
        P=P5, J=2, ell=0, patterns=[RAW, C01], N=4, q=Fr(1,4), rho=Fr(3,4), theta_num=3, kseq=[1,1,1,1], seed=62,
        edge_patterns=[[1],[0],[0],[1]], edge_perms=[ID2]*4)
print("SUMMARY", which, [(t.split()[0], ok) for t, ok in results])
