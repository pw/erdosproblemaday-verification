# Proof-relevant check + negative controls for the parity argument of Prop 2.4 (collinear {0,1,2}).
from fractions import Fraction as Fr
c = [Fr(-1, 2), Fr(1), Fr(-1, 2)]   # sum c_i|b_i|^2 = -1 on every copy
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
            # proof-relevant: label_i(b_i) == label_i(b_1) for every i
            if all(L[i][i] == L[0][i] for i in range(3)): rel += 1
    return N, full, rel
print('paper colouring K=2s+1=7      :', scan(c, 7))
# negative control 1: halve the weights -> sum = -1/2 (not an odd integer): argument breaks, expect hits
print('neg ctrl, weights/2, K=7      :', scan([x/2 for x in c], 7))
# negative control 2: too few intervals (K=2 -> |eps|<1 each, sum up to 2): expect hits
print('neg ctrl, K=2                 :', scan(c, 2))
# threshold sweep: proof needs (s-1)*2/K < 1, i.e. K >= 5 for s=3 (paper takes K=2s+1=7, conservative)
for K in range(2, 8):
    print('K=%d' % K, scan(c, K))
# negative control 3: a weight vector that does NOT satisfy the moment identities (sum c_i a_i != 0)
print('neg ctrl, wrong weights (1,-1,0), K=7:', scan([Fr(1), Fr(-1), Fr(0)], 7))
