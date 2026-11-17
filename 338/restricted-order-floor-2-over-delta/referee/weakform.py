# Is the separate-integer form |Y| >= |P|+|S|-1 (|P|>=ceil(i*x), |S|>=ceil(x)) load-bearing for the floor version?
# Replace it by the weak (ENS-style) form |Y| >= ceil((i*+1)x) - 1 and see whether floor(2/delta)-1 still holds.
from fractions import Fraction as F
from math import floor, ceil
def cdiv(a,b): return -(-a//b)
eps=F(1,10**15); bad=[]
for m in range(4,80):
    d=F(2,m+1)+eps; worst=0; arg=None
    for i in range(1,floor(1/d)+1):
        for g in range(2,12*(m+1)):
            x=d*g; s=max(2,ceil(x)); Y=ceil((i+1)*x)-1
            if Y>g: continue
            a=g-Y; h=i+1+cdiv(a,cdiv(s,2))
            if h>worst: worst=h; arg=(g,i,Y,s,a)
    if worst>m-1: bad.append((m,worst,arg))
print("m with weak-form worst case > floor bound:",len(bad), bad[:6])
