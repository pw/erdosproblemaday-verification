import sys; sys.path.insert(0, '.')
from fractions import Fraction as Fr
c = [Fr(-1, 2), Fr(1), Fr(-1, 2)]
def labels(cv, K, z2): return [int(((ci*z2) % 2) * K // 2) for ci in cv]
def scan(cv, K, step_x=97, step_y=131):
    N = full = rel = 0
    for xn in range(0, 4000):
        x = Fr(xn, step_x)
        for yn in range(-300, 301, 3):
            y = Fr(yn, step_y)
            if y*y > x: continue
            N += 1
            n2 = [x, x+2*y+1, x+4*y+4]
            L = [labels(cv, K, z) for z in n2]
            if L[0] == L[1] == L[2]: full += 1
            if all(L[i][i] == L[0][i] for i in range(3)): rel += 1
    return N, full, rel
print('K=3 (N, monochromatic, proof-relevant):', scan(c, 3), flush=True)
