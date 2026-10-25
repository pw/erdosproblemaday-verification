# (a) grid {1..t}^d: count distinct squared distances exactly; compare with d(t-1)^2 and n^{2/d}=t^2
import itertools
for d in (3, 4):
    for t in range(2, 7):
        # squared distance between two grid points = sum of d squares of coordinate differences in {0..t-1}
        diffs = range(0, t)
        sq = set()
        for v in itertools.product(diffs, repeat=d):
            s = sum(x*x for x in v)
            if s > 0:
                sq.add(s)
        n = t**d
        D = len(sq)
        bound = d*(t-1)**2
        # brute-force cross-check on actual point pairs for small cases
        if n <= 1296:
            pts = list(itertools.product(range(1, t+1), repeat=d))
            sq2 = set()
            for i in range(len(pts)):
                pi = pts[i]
                for j in range(i+1, len(pts)):
                    pj = pts[j]
                    sq2.add(sum((a-b)**2 for a, b in zip(pi, pj)))
            assert sq2 == sq, (d, t)
            chk = "pairs-checked"
        else:
            chk = "diff-vectors"
        print(f"d={d} t={t} n={n:5d} |Delta|={D:3d} <= d(t-1)^2={bound:3d}: {D<=bound}  ratio |Delta|/n^(2/d) = {D/t**2:.4f}  ({chk})")
