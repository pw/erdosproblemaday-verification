import random
from fractions import Fraction as F
from math import floor, ceil
exec(open('arith_sup.py').read().split("eps=F(1,10**15)")[0])
random.seed(7); bad=0; n=0
for m in range(4,31):
    for trial in range(6):
        lo=F(2,m+1); hi=F(2,m)
        delta = lo + (hi-lo)*F(random.randint(1,10**6),10**6)
        h,_=worst(delta, 60*(m+1)); h2,_=worst(delta,60*(m+1),False)
        n+=1
        if max(h,h2)>floor(2/delta)-1: bad+=1; print("VIOL",m,delta,h,h2)
    h,_=worst(F(2,m+1)+F(1,10**15), 60*(m+1),False)
    if h>m-1: bad+=1; print("VIOL lim",m,h)
print("random deltas",n,"violations",bad)
