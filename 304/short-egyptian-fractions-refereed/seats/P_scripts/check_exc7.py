import pickle
from fractions import Fraction
import importlib.util, sys
res = pickle.load(open('/tmp/oaimath/025/seats/P_scripts/expansions7.pkl','rb'))
def sf(s):
    for a in range(2, int(s**0.5)+1):
        if s % a == 0: return a
for t in res[7]:
    s, v = t[-2], t[-1]
    if v in (s+1, s*(s+1)):
        a = sf(s); b = s//a
        new = tuple(sorted(list(t[:-2]) + [s+a, b*(s+a), v]))
        ok = len(set(new)) == 8 and sum(Fraction(1,n) for n in new) == 1 and v in new
        # also check every factorization a*b=s works
        allok = True
        for a2 in range(2, s):
            if s % a2 == 0 and s//a2 >= 2:
                b2 = s//a2
                n2 = tuple(sorted(list(t[:-2]) + [s+a2, b2*(s+a2), v]))
                allok &= len(set(n2)) == 8 and sum(Fraction(1,n) for n in n2) == 1
        print(t, 's=',s,'v=',v, 'case', 'v=s+1' if v==s+1 else 'v=s(s+1)', '->', new, ok, 'all factorizations ok:', allok)
