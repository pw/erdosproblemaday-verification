# Why the rank-2 factorization (3.1) is load-bearing: in R^3 (rank-3 form, no factorization into two linear forms over any field)
# the weak pinned statement is FALSE: the k x k x k grid has <= 3(k-1)^2 distinct squared distances at EVERY pin, i.e. O(n^{2/3}).
# Same computation in R^2 (rank 2, factorizable) for comparison: every pin of the k x k grid sees ~ n/sqrt(log n) distances.
import math
def pinned_counts(pts):
    out = []
    for x in pts:
        out.append(len({sum((a-b)**2 for a,b in zip(x,y)) for y in pts if y != x}))
    return min(out), max(out)
for k in (6, 10, 14):
    P3 = [(i,j,l) for i in range(k) for j in range(k) for l in range(k)]; n3 = len(P3)
    mn, mx = pinned_counts(P3)
    print(f"R^3 grid k={k:2d} n={n3:5d}: distinct sq-distances per pin in [{mn},{mx}]  vs n^(2/3)={n3**(2/3):.0f}  n^0.9={n3**0.9:.0f}")
for k in (20, 40, 60):
    P2 = [(i,j) for i in range(k) for j in range(k)]; n2 = len(P2)
    mn, mx = pinned_counts(P2)
    print(f"R^2 grid k={k:2d} n={n2:5d}: distinct sq-distances per pin in [{mn},{mx}]  vs n/sqrt(log n)={n2/math.sqrt(math.log(n2)):.0f}")
