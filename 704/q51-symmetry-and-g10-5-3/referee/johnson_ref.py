# Referee: v^T E_i v for v = 1_W in J(13,5), exactly, via E_i = prod_{j!=i} (A - th_j)/(th_i - th_j), A = A_1 (|x∩y|=4).
import ast, re
from itertools import combinations
from fractions import Fraction
from sympy import factorint
src = open('../wstruct.py').read()
W = {frozenset(x-1 for x in s) for s in ast.literal_eval(re.search(r'^W0 = (\[.*\])$', src, re.M).group(1))}
V = [frozenset(c) for c in combinations(range(13), 5)]; I = {s: i for i, s in enumerate(V)}
nb = [[I[(s - {x}) | {y}] for x in s for y in range(13) if y not in s] for s in V]
assert all(len(l) == 40 for l in nb)
def A(u): return [sum(u[j] for j in nb[i]) for i in range(len(V))]
v = [1 if s in W else 0 for s in V]
th = [(5-i)*(8-i)-i for i in range(6)]; print('eigenvalues', th)
# eigenvalue check: A has exactly these eigenvalues -> prod (A - th_j) v = 0
u = v[:]
for t in th: u = [a - t*b for a, b in zip(A(u), u)]
print('prod_j (A - th_j) v == 0:', all(x == 0 for x in u))
vals = []
for i in range(6):
    u = [Fraction(x) for x in v]
    for j in range(6):
        if j == i: continue
        u = [(a - th[j]*b) / (th[i]-th[j]) for a, b in zip(A(u), u)]
    vals.append(sum(a*b for a, b in zip(u, v)))
print('v^T E_i v =', [str(x) for x in vals], ' sum =', sum(vals))
ps = set()
for x in vals: ps |= set(factorint(x.numerator)) | set(factorint(x.denominator))
print('primes in numerators/denominators:', sorted(ps), ' > 13:', sorted(p for p in ps if p > 13))
# inner distribution of W
from collections import Counter
print('inner distribution (|x∩y| : ordered pairs):', sorted(Counter(len(x&y) for x in W for y in W).items()))
