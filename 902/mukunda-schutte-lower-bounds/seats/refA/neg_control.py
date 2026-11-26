# Negative control for check_counting: break the planted structure and confirm failures appear.
import sys
sys.path.insert(0, '/home/exedev/MathDyad/subs-1126/902/refA')
import check_counting as cc
import numpy as np
orig = cc.planted
def broken(seed):
    A, P, R, O = orig(seed)
    # reverse one arc inside R: breaks 5-regularity of T[R]
    x, z = R[0], [r for r in R if A[R[0], r]][0]
    A[x, z], A[z, x] = 0, 1
    return A, P, R, O
cc.planted = broken
bad, J, qs = cc.run(0)
kinds = sorted(set(b[0] for b in bad))
print("negative control failure kinds:", kinds, "count", len(bad))
