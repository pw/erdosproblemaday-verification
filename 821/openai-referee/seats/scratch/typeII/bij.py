# Toy check of the determinant parametrization (6.15)-(6.18) and its converse.
from math import gcd
B=60
A=set()
for e in range(1,B):
  for n in range(1,B):
    # m n = 2 e h + 1
    sols=[]
    for m in range(1,4*B):
      if (m*n-1)%(2*e)==0 and m*n>1:
        h=(m*n-1)//(2*e)
        if h>=1: sols.append((m,h))
    for (m,h) in sols:
      for (mp,hp) in sols:
        if m!=mp: A.add((e,n,m,mp,h,hp))
fwd={}
bad_coprime=0
for (e,n,m,mp,h,hp) in A:
  assert (mp-m)%(2*e)==0
  k=(mp-m)//(2*e)
  assert k!=0 and hp-h==k*n and m*hp-mp*h==k
  assert (mp-m)%(2*abs(k))==0 and (mp-m)//(2*k)>0
  if gcd(m,k)!=1: bad_coprime+=1
  fwd[(e,n,m,mp,h,hp)]=(k,m,mp,h,hp)
print("A size",len(A),"forward images with gcd(m,k)>1:",bad_coprime)
# converse: every (k,m,mp,h,hp) with conditions and gcd(m,k)=1 must come from A (within ranges)
img=set(fwd.values())
cnt=0;fail=0;fail_nc=0
for k in range(-20,21):
  if k==0: continue
  for m in range(1,4*B):
    for mp in range(1,4*B):
      if (mp-m)%(2*abs(k)) or (mp-m)//(2*k)<=0: continue
      e=(mp-m)//(2*k)
      if e>=B: continue
      for h in range(1,3*B):
        # m h' = m' h + k
        if (mp*h+k)%m: continue
        hp=(mp*h+k)//m
        if hp<1: continue
        if gcd(m,k)==1:
          cnt+=1
          assert m*(hp-h)==k*(2*e*h+1)
          assert (2*e*h+1)%m==0
          n=(2*e*h+1)//m
          assert hp-h==k*n and mp*n==2*e*hp+1
          if n<B and (k,m,mp,h,hp) not in img: fail+=1
        else:
          # check whether converse fails without coprimality
          if (2*e*h+1)%m!=0: fail_nc+=1
print("converse checked",cnt,"failures",fail,"; non-coprime tuples where m does not divide 2eh+1:",fail_nc)
