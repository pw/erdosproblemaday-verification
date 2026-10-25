import sys, itertools, time
from hcheck import admissible
def has_admissible(A, k):
    return any(admissible(S) for S in itertools.combinations(sorted(A), k))
for N in [int(x) for x in sys.argv[1:]]:
    A = list(range(-N, N + 1)); t0 = time.time()
    k = 1
    while has_admissible(A, k + 1): k += 1
    print(f"H([-{N},{N}]) = {k}   (n={len(A)}, {time.time()-t0:.1f}s)", flush=True)
