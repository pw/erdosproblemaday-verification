# Rigor check for the knapsack brackets: the floored/ceiled log2-weights must satisfy
#   Wf = floor(R*log2 p)  <=>  2^Wf <= p^R < 2^(Wf+1)     and   Wc = Wf + 1  (R*log2 p is irrational)
# verified with exact integer arithmetic (no floating point), for every R used.
# Negative control: a deliberately perturbed weight (Wf+1 as "floor") must be caught.
from math import floor, ceil, log2
def primes_below(n):
    s = bytearray([1])*n; s[0]=s[1]=0
    for i in range(2,int(n**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(n) if s[i]]
S = [p for p in primes_below(257) if p != 2]
def check(R, perturb=False):
    bad = 0; mind = 1.0
    for p in S:
        wf = floor(log2(p)*R) + (1 if perturb and p == 3 else 0); wc = ceil(log2(p)*R)
        pR = p**R
        if not ((1 << wf) <= pR < (1 << (wf+1))): bad += 1      # exact floor test
        if wc != wf + 1 and not perturb: bad += 1               # ceil = floor+1 (never an integer)
        x = log2(p)*R; mind = min(mind, abs(x - round(x)))
    return bad, mind
for R in (256, 2048, 8192, 32768, 65536):
    bad, mind = check(R)
    print(f"R={R}: weight violations={bad}  (min float distance of R*log2 p to an integer = {mind:.3e})")
bad, _ = check(2048, perturb=True)
print(f"NEGATIVE control (p=3 weight bumped by 1 at R=2048): violations={bad} (must be >=1)")
