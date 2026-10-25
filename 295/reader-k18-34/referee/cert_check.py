# Independent certificate checker: running exact sum num/den via cross-multiplication
# and gcd reduction; no fractions module, no lcm.
import sys
from math import gcd

D = [18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,43,44,45,46,
     48,50,52,54,63,275,14143068,10457416992]

def check(ds, N=18, k=None):
    reasons = []
    if any(type(d) is not int for d in ds): reasons.append("non-int")
    if len(set(ds)) != len(ds): reasons.append("not distinct")
    if min(ds) < N: reasons.append("min < N")
    if k is not None and len(ds) != k: reasons.append("wrong length")
    num, den = 0, 1
    for d in ds:
        # num/den + 1/d = (num*d + den)/(den*d)
        num, den = num*d + den, den*d
        g = gcd(num, den); num //= g; den //= g
    if (num, den) != (1, 1): reasons.append(f"sum = {num}/{den} != 1")
    return (not reasons), (num, den), reasons

ok, s, r = check(D, 18, 34)
print("certificate:", "PASS" if ok else "FAIL", "len", len(D), "min", min(D), "sum", s, r)
# surgery check by same method
def ssum(ds):
    num, den = 0, 1
    for d in ds:
        num, den = num*d + den, den*d
        g = gcd(num, den); num //= g; den //= g
    return num, den
old=[42,640,337280,1735650,68479214496]; new=[46,275,14143068,10457416992]
print("surgery old", ssum(old), "new", ssum(new), "equal", ssum(old)==ssum(new))
ours35=[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,42,43,44,45,48,50,52,54,63,640,337280,1735650,68479214496]
print("our 35-set sum", ssum(ours35), "len", len(ours35))
derived = sorted((set(ours35)-set(old))|set(new))
print("derived == D:", derived == D)
# negative controls
for i, delta in [(31, 1), (33, 1), (33, -1), (0, 0)]:
    E = list(D)
    if delta == 0:
        E[0] = 17  # min-violation with sum change
    else:
        E[i] += delta
    ok2, s2, r2 = check(E, 18, 34)
    print("negative control", i, delta, "->", "PASS(BAD)" if ok2 else "REJECT", r2[:2] if r2 else "", )
# duplicate control: replace 275 by 46 (duplicate)
E = list(D); E[31] = 46
print("dup control ->", check(E,18,34)[0], check(E,18,34)[2][:1])
