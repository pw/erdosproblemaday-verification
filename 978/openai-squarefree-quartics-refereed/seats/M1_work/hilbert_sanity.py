# Sanity: bigraded HF of (d-2) forms of bidegree (k,1) in C[a_1..a_d, b_1..b_d] (regular sequence)
# vs the leading form R(A,B) of Lemma 5.1 (used to build H, H_a, H_b in the certificate).
from math import comb, factorial
from fractions import Fraction as F
def HF(d, A, B):
    k = d-2; tot = 0
    for i in range(d-1):
        a, b = A-k*i, B-i
        if a < 0 or b < 0: continue
        tot += (-1)**i * comb(d-2, i) * comb(a+d-1, d-1) * comb(b+d-1, d-1)
    return tot
def R(d, A, B):
    k = d-2
    return F(sum(comb(d,j)*comb(d-2,j-1)*k**(j-1)*A**(d-j)*B**j for j in range(1,d)), factorial(d))
for d in range(4, 9):
    out = []
    for s in [200, 800, 3200]:
        A, B = s, s//2
        out.append(float(F(HF(d,A,B)) / R(d,A,B)))
    print(d, ["%.5f" % x for x in out])
