"""Brute force for the ternary basis A = {2a+1 : a in X} ∪ {4a : a in X, a>=1}, X = ternary digits in {0,1}.
Instrument 1: 0/1-knapsack with a cap on the number of summands, on Python big-int bitsets.
Outputs: order-2 check (repetition allowed), exception sets for <=3 and <=4 DISTINCT summands."""
import sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
def X_upto(n):
    xs = [0]
    p = 1
    while p <= n:
        xs += [x + p for x in xs if x + p <= n]
        p *= 3
    return sorted(xs)
X = X_upto(N)
A = sorted(set([2*a+1 for a in X if 2*a+1 <= N] + [4*a for a in X if a >= 1 and 4*a <= N]))
mask = (1 << (N+1)) - 1
# order 2, repetition allowed: B1 = A, B2 = A+A
bitA = 0
for e in A: bitA |= 1 << e
two = 0
for e in A: two |= bitA << e
two &= mask
ord2 = bitA | two
def zeros(x):
    """positions 1..N whose bit is 0, via one conversion to a bit string (LSB first)"""
    s = bin(x)[2:][::-1].ljust(N+1, '0')
    return [n for n in range(1, N+1) if s[n] == '0']
miss2 = zeros(ord2)
print(f"N={N} |X|={len(X)} |A|={len(A)}; not a sum of <=2 elements (repetition allowed): {miss2[:20]} (count {len(miss2)})")
# distinct summands: layers[k] = bitset of sums of exactly k distinct elements
K = 4
layers = [1] + [0]*K
for e in A:
    for k in range(K, 0, -1):
        layers[k] |= (layers[k-1] << e) & mask
le3 = layers[1] | layers[2] | layers[3]
le4 = le3 | layers[4]
exc3 = zeros(le3)
exc4 = zeros(le4)
pred = []
p = 2
while p <= N:
    pred.append(p); p *= 3
print("exceptions for <=3 distinct:", exc3)
print("predicted {2*3^j}:        ", pred, "MATCH" if exc3 == pred else "MISMATCH")
print("exceptions for <=4 distinct:", exc4)
